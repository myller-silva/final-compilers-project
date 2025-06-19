import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from others.table_parser_ll1 import (
    Symbol,
    NonTerminal,
    Terminal,
    Production,
    Grammar,
    Tokenizer,
    LL1Table,
    LL1ParserTable,
    Token,
)


class TestSymbol(unittest.TestCase):
    def test_symbol_equality(self):
        """Testa a igualdade entre símbolos."""
        s1 = Symbol("X")
        s2 = Symbol("X")
        s3 = Symbol("Y")
        s4 = Symbol("x")
        s5 = Symbol("y")

        self.assertTrue(all(isinstance(s, Symbol) for s in [s1, s2, s3, s4, s5]))
        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s4, s5)
        self.assertNotEqual(s1, s4)
        self.assertNotEqual(s3, s5)
        self.assertNotEqual(s1, None)
        self.assertNotEqual(s2, None)

    def test_terminal_and_nonterminal(self):
        """Testa a criação e igualdade de Terminais e Não Terminais."""
        # TERMINAL
        a1, a2 = Terminal("a"), Terminal("a", r"a")
        b1, b2 = Terminal("b"), Terminal("b", r"b")

        self.assertTrue(all(isinstance(t, Terminal) for t in [a1, a2, b1, b2]))
        self.assertTrue(all([a1 == a2, b1 == b2]))
        self.assertFalse(all([a1 == b1, a2 == b2, a1 == b2, a2 == b1]))

        # NONTERMINAL
        A1, A2 = NonTerminal("A"), NonTerminal("A")
        B1, B2 = NonTerminal("B"), NonTerminal("B")

        self.assertTrue(all(isinstance(nt, NonTerminal) for nt in [A1, A2, B1, B2]))
        self.assertTrue(all([A1 == A2, B1 == B2]))
        self.assertFalse(all([A1 == B1, A2 == B2, A1 == B2, A2 == B1]))

        # TERMINAL vs NONTERMINAL
        self.assertNotEqual(a1, A1)
        self.assertNotEqual(a2, A2)
        self.assertNotEqual(b1, B1)
        self.assertNotEqual(b2, B2)
        self.assertNotEqual(a1, A1)
        self.assertNotEqual(a2, A2)


class TestProduction(unittest.TestCase):
    def test_production_repr(self):
        """Verifica se a representação de uma produção contém os símbolos corretos."""
        lhs = NonTerminal("S")
        rhs = [Terminal("a", r"a"), NonTerminal("A")]
        prod = Production(lhs, rhs)

        self.assertIn("S", repr(prod))
        self.assertIn("a", repr(prod))
        self.assertIn("A", repr(prod))

    def test_production_equality(self):
        """Verifica se duas produções são consideradas iguais."""
        lhs1 = NonTerminal("S")
        rhs1 = [Terminal("a", r"a"), NonTerminal("A")]
        prod1 = Production(lhs1, rhs1)

        lhs2 = NonTerminal("S")
        rhs2 = [Terminal("a", r"a"), NonTerminal("A")]
        prod2 = Production(lhs2, rhs2)

        self.assertEqual(prod1, prod2)

        lhs3 = NonTerminal("S")
        rhs3 = [Terminal("b", r"b"), NonTerminal("B")]
        prod3 = Production(lhs3, rhs3)

        self.assertNotEqual(prod1, prod3)

    def test_production_hash(self):
        """Verifica se o hash de uma produção é consistente."""
        lhs = NonTerminal("S")
        rhs = [Terminal("a", r"a"), NonTerminal("A")]
        prod = Production(lhs, rhs)
        self.assertEqual(hash(prod), hash((lhs, tuple(rhs))))


class BaseGrammarTest(unittest.TestCase):
    def setUp(self):
        self.E, self.X, self.T, self.Y, self.F = [
            NonTerminal(name) for name in ["E", "X", "T", "Y", "F"]
        ]
        self.non_terminals = [self.E, self.X, self.T, self.Y, self.F]
        self.start_symbol = self.E
        self.plus = Terminal("plus", r"\+")
        self.dot = Terminal("dot", r"\*")
        self.left_p = Terminal("left_paren", r"\(")
        self.right_p = Terminal("right_paren", r"\)")
        self.iden = Terminal("id", r"[a-zA-Z_][a-zA-Z0-9_]*")
        self.terminals = [
            self.plus,
            self.dot,
            self.left_p,
            self.right_p,
            self.iden,
            Grammar.EOF,
        ]

        self.productions = [
            Production(self.E, [self.T, self.X]),  # E -> T X
            Production(self.X, [self.plus, self.T, self.X]),  # X -> + T X
            Production(self.X, [Grammar.EPSILON]),  # X -> ε
            Production(self.T, [self.F, self.Y]),  # T -> F Y
            Production(self.Y, [self.dot, self.F, self.Y]),  # Y -> * F Y
            Production(self.Y, [Grammar.EPSILON]),  # Y -> ε
            Production(self.F, [self.left_p, self.E, self.right_p]),  # F -> ( E )
            Production(self.F, [self.iden]),  # F -> id
        ]

        self.grammar = Grammar(
            start_symbol=self.start_symbol,
            terminals=self.terminals,
            non_terminals=self.non_terminals,
            productions=self.productions,
        )


class TestGrammar(BaseGrammarTest):
    def test_first_sets(self):
        """Testa os conjuntos FIRST da gramática."""
        # E: {(, id}
        # T: {(, id}
        # X: {+, ε}
        # F: {(, id}
        # Y: {*, ε}
        first_E = self.grammar.first_sets[self.E]
        fist_T = self.grammar.first_sets[self.T]
        first_X = self.grammar.first_sets[self.X]
        first_Y = self.grammar.first_sets[self.Y]
        first_F = self.grammar.first_sets[self.F]

        first_E_expected = {self.left_p, self.iden}
        first_T_expected = {self.left_p, self.iden}
        first_X_expected = {self.plus, Grammar.EPSILON}
        first_Y_expected = {self.dot, Grammar.EPSILON}
        first_F_expected = {self.left_p, self.iden}

        self.assertEqual(first_E, first_E_expected)
        self.assertEqual(fist_T, first_T_expected)
        self.assertEqual(first_X, first_X_expected)
        self.assertEqual(first_Y, first_Y_expected)
        self.assertEqual(first_F, first_F_expected)

    def test_follow_sets(self):
        """Testa os conjuntos FOLLOW da gramática."""
        # E: {EOF, )},
        # F: {*, +, EOF, )},
        # Y: {+, EOF, )},
        # T: {+, EOF, )},
        # X: {EOF, )}
        follow_E = self.grammar.follow_sets[self.E]
        follow_F = self.grammar.follow_sets[self.F]
        follow_Y = self.grammar.follow_sets[self.Y]
        follow_T = self.grammar.follow_sets[self.T]
        follow_X = self.grammar.follow_sets[self.X]

        follow_E_expected = {Grammar.EOF, self.right_p}
        follow_F_expected = {self.dot, self.plus, Grammar.EOF, self.right_p}
        follow_Y_expected = {self.plus, Grammar.EOF, self.right_p}
        follow_T_expected = {self.plus, Grammar.EOF, self.right_p}
        follow_X_expected = {Grammar.EOF, self.right_p}

        self.assertEqual(follow_E, follow_E_expected)
        self.assertEqual(follow_F, follow_F_expected)
        self.assertEqual(follow_Y, follow_Y_expected)
        self.assertEqual(follow_T, follow_T_expected)
        self.assertEqual(follow_X, follow_X_expected)


class TestTokenizer(BaseGrammarTest):
    def setUp(self):
        super().setUp()

    def test_tokenize_valid(self):
        """Testa a tokenização de expressões válidas e inválidas."""
        tokenization_cases = [  # texto / quantidade de tokens esperados
            ("id + id * ( id + id )", 9),
            ("a + b * ( c + d )", 9),
            ("x * ( y + z )", 7),
            ("a + b * (c + d)", 9),
            ("a + b * (c + d) ", 9),
            ("a + b * (c + d)   ", 9),
            ("(a + b) * (c + d)", 11),
            ("(a+b)*(c+d)", 11),  # sem espaços
            ("(a+b)*(c+d)   ", 11),  # com espaços no final
            ("(a+b) * (c+d)", 11),  # com espaços entre os parênteses
            ("(a + b) * (c + d)", 11),  # com espaços entre os operadores e operandos
            ("(a + b) * (c + d)   ", 11),  # com espaços no final
        ]
        for text, expected_count in tokenization_cases:
            with self.subTest(text=text):
                tokens = Tokenizer.tokenize(text, self.grammar)
                # Verifica a quantidade de tokens
                self.assertEqual(len(tokens), expected_count)
                for token in tokens:
                    # Verifica se todos os tokens são instâncias de Token
                    self.assertIsInstance(token, Token)

    def test_tokenize_invalid(self):
        """Testa a tokenização de expressões inválidas."""
        error_cases = [
            "1abc",  # idenficador inválido
            "id + * ( id & id )",  # operador inválido
            "a + b * ( c + d ) @",  # caractere inválido no final
            "x 1 abc 12",  # número não definido na gramática
        ]
        for text in error_cases:
            with self.subTest(text=text):
                with self.assertRaises(RuntimeError):
                    Tokenizer.tokenize(text, self.grammar)


class TestLL1Table(BaseGrammarTest):
    def setUp(self):
        super().setUp()

    def test_ll1_table(self):
        """Testa se a tabela LL(1) é construída corretamente."""
        ll1_table = LL1Table(self.grammar)
        non_terminal_symbols = self.grammar.non_terminals
        for non_terminal in non_terminal_symbols:
            for symbol in self.grammar.first_sets[non_terminal]:
                if symbol != Grammar.EPSILON:
                    # Verifica se o par (não terminal, símbolo) está na tabela
                    self.assertIn((non_terminal, symbol), ll1_table.table)
                else:  # Se o simbolo for EPSILON, verificar se está na tabela de follow
                    for follow_symbol in self.grammar.follow_sets[non_terminal]:
                        prod = Production(non_terminal, [Grammar.EPSILON])  # ex: X -> ε
                        # O esperado é que o valor seja a produção do Terminal com EPSILON
                        self.assertEqual(
                            ll1_table.table.get((non_terminal, follow_symbol), None),
                            prod,
                            f"Esperado {Grammar.EPSILON} para {non_terminal} e {follow_symbol}",
                        )


class TestLL1ParserTable(BaseGrammarTest):
    def setUp(self):
        super().setUp()
        self.ll1_table = LL1Table(self.grammar)
        self.parser = LL1ParserTable(self.ll1_table, self.grammar.start_symbol)

    def test_parse_valid(self):
        valid_cases = [
            "id + id * ( id + id )",
            "a + b * ( c + d )",
            "x * ( y + z )",
            "a + b * (c + d)",
            "(a + b) * (c + d)",
        ]
        for case in valid_cases:
            with self.subTest(case=case):
                tokens = Tokenizer.tokenize(case, self.grammar)
                result = self.parser.parse(tokens)
                self.assertTrue(result)

    def test_parse_invalid(self):
        invalid_cases = [
            "())",
            ")(",
            "(id))",
            "",  # a gramatica não aceita o vazio
            "id + * ( id + id )",  # operador inválido
            "id * +  ( id + id )",  # operador inválido
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                tokens = Tokenizer.tokenize(case, self.grammar)
                result = self.parser.parse(tokens)
                self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
