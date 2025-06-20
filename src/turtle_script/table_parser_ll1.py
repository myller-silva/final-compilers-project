import re
import pandas as pd
from collections import defaultdict
from colorama import Fore, Style, init


init(autoreset=True)


class Symbol:
    def __init__(self, name: str, repr: str = None):
        self.name = name
        self.repr = repr if repr is not None else name

    def __repr__(self):
        return f"{self.repr}"

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def __hash__(self):
        return hash((self.name, type(self)))


class NonTerminal(Symbol):
    def __rshift__(self, rhs):
        """
        Define a produção A >> [B, c] ou A >> B.
        Permite que o lado direito seja um símbolo ou uma lista de símbolos.
        """
        if isinstance(rhs, list):
            return Production(self, rhs)
        elif isinstance(rhs, Symbol):
            return Production(self, [rhs])
        else:
            raise TypeError("O lado direito deve ser um símbolo ou lista de símbolos.")


class Terminal(Symbol):
    def __init__(self, name: str, regex: str = None, repr: str = None):
        super().__init__(name, repr)
        self.regex = regex if regex is not None else f"{name}"


class Production:
    def __init__(self, lhs: NonTerminal, rhs: list[Symbol]):
        assert isinstance(
            lhs, NonTerminal
        ), f"Lado esquerdo 'lhs' deve ser um '{NonTerminal.__name__}' mas recebeu '{type(lhs).__name__}'."
        assert all(
            isinstance(sym, Symbol) for sym in rhs
        ), f"Lado direito 'rhs' deve ser uma lista de '{Symbol.__name__}'."
        self.lhs, self.rhs = lhs, rhs

    def __repr__(self):
        arrow = "→"
        rhs_str = " ".join(map(str, self.rhs)) if self.rhs else str(Grammar.EPSILON)
        return f"{self.lhs} {arrow} {rhs_str}"

    def __eq__(self, other):
        if isinstance(other, Production):
            return self.lhs == other.lhs and self.rhs == other.rhs
        return False

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs)))


class Grammar:
    EPSILON = Symbol("ε")
    EOF = Terminal("EOF", "$")

    def __init__(
        self,
        start_symbol: NonTerminal,
        terminals: list[Terminal] = [EOF],
        non_terminals: list[NonTerminal] = [],
        productions: list[Production] = [],
    ):
        self.start_symbol = start_symbol
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions

        self._validate_productions()
        self.first_sets = self.compute_first_sets()
        self.follow_sets = self.compute_follow_sets()

    def _validate_productions(self):
        """Valida as produções da gramática."""
        erros = []
        for prod in self.productions:
            if not isinstance(prod, Production):
                erros.append(f"Expected Production but got '{type(prod).__name__}'")
            if prod.lhs not in self.non_terminals:
                erros.append(f"LHS '{prod.lhs}' is not in non_terminals list")
            for sym in prod.rhs:
                if isinstance(sym, Terminal) and sym not in self.terminals:
                    erros.append(f"Terminal '{sym}' is not in terminals list")
                elif isinstance(sym, NonTerminal) and sym not in self.non_terminals:
                    erros.append(f"NonTerminal '{sym}' is not in non_terminals list")
        if erros:
            raise ValueError("Errors in productions:\n" + "\n".join(erros))

    def __repr__(self):
        productions_str = "\n".join(map(str, self.productions))
        return f"Grammar:\nStart Symbol: {self.start_symbol}\nProductions:\n{productions_str}"

    def compute_first_sets(self):
        """Calcula os conjuntos FIRST para cada não terminal da gramática."""
        first = defaultdict(set)

        def first_of(symbol):
            """Calcula o conjunto FIRST para um símbolo."""
            if isinstance(symbol, Terminal):
                return {symbol}
            return first[symbol]

        changed = True
        while changed:
            changed = False
            for prod in self.productions:
                lhs, rhs = prod.lhs, prod.rhs
                original_size = len(first[lhs])

                if len(rhs) == 1 and rhs[0] == Grammar.EPSILON:
                    first[lhs].add(Grammar.EPSILON)
                else:
                    nullable = True
                    for symbol in rhs:
                        symbol_first = first_of(symbol)
                        first[lhs].update(symbol_first - {Grammar.EPSILON})
                        if Grammar.EPSILON not in symbol_first:
                            nullable = False
                            break
                    if nullable:
                        first[lhs].add(Grammar.EPSILON)

                if len(first[lhs]) > original_size:
                    changed = True
        return first

    def compute_follow_sets(self):
        """Calcula os conjuntos FOLLOW para cada não terminal da gramática."""
        follow = defaultdict(set)
        follow[self.start_symbol].add(Grammar.EOF)
        changed = True
        while changed:
            changed = False
            for prod in self.productions[::-1]:
                lhs, rhs = prod.lhs, prod.rhs
                trailer = follow[lhs].copy()
                for i in reversed(range(len(rhs))):
                    symbol = rhs[i]
                    if isinstance(symbol, NonTerminal):
                        original_size = len(follow[symbol])
                        follow[symbol].update(trailer)
                        if Grammar.EPSILON in self.first_sets[symbol]:
                            trailer = trailer.union(
                                self.first_sets[symbol] - {Grammar.EPSILON}
                            )
                        else:
                            trailer = self.first_sets[symbol] - {Grammar.EPSILON}
                        if len(follow[symbol]) > original_size:
                            changed = True
                    elif isinstance(symbol, Terminal):
                        trailer = {symbol}
        return follow

    def first_rhs(self, symbols: list[Symbol]) -> set:
        """Calcula o conjunto FIRST para uma sequência de símbolos (lado direito de uma produção)."""
        result = set()
        for sym in symbols:
            if isinstance(sym, Terminal):
                result.add(sym)
                break
            elif isinstance(sym, NonTerminal):
                result.update(self.first_sets[sym] - {Grammar.EPSILON})
                if Grammar.EPSILON not in self.first_sets[sym]:
                    break
        else:
            result.add(Grammar.EPSILON)
        return result


class Token:
    def __init__(self, terminal: Terminal, lexeme: str):
        self.terminal = terminal
        self.lexeme = lexeme

    def __repr__(self):
        return f"Token({self.terminal.name}, '{self.lexeme}')"

    def __str__(self):
        return f"{self.terminal.name}: '{self.lexeme}'"

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.terminal == other.terminal and self.lexeme == other.lexeme
        return False

    def __hash__(self):
        return hash((self.terminal, self.lexeme))


class Tokenizer:
    def __init__(self):
        super().__init__()

    @staticmethod
    def tokenize(text: str, grammar: Grammar) -> list[Token]:
        """Tokeniza o texto de entrada usando a gramática fornecida."""
        tokens = []
        # Ignorar comentários
        comment_pattern = r"//.*?$"
        text = re.sub(comment_pattern, "", text, flags=re.MULTILINE)

        # Construir o regex de tokenização
        token_patterns = [
            (token.name, token.regex)
            for token in grammar.terminals
            if isinstance(token, Terminal)
        ]
        token_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_patterns)
        match_token = re.compile(token_regex).match
        # Tokenização:
        position, line_number = 0, 1
        terminals = Tokenizer._get_terminals(grammar)
        while position < len(text):
            # Pular espaços em branco
            ws_match = re.match(r"\s+", text[position:])
            if ws_match:
                ws = ws_match.group(0)
                line_number += ws.count("\n")
                position += len(ws)
                continue
            match = match_token(text, position)
            if match is None:
                snippet = text[position : position + 10]
                raise RuntimeError(
                    f"Erro de tokenização na linha {line_number}, posição {position}, trecho: '{snippet}'"
                )
            position = match.end()
            token_type = match.lastgroup
            lexeme = match.group(token_type)
            tokens.append(Token(terminals.get(token_type), lexeme=lexeme))
        return tokens

    @staticmethod  # TODO: talvez transferir esse método para a classe Grammar, ou criar uma classe diferente.
    def _get_terminals(grammar: Grammar) -> dict[str, Terminal]:
        """Retorna um dicionário de terminais da gramática."""
        return {
            terminal.name: terminal
            for terminal in grammar.terminals
            if isinstance(terminal, Terminal)
        }


class LL1Table:  # TODO: LANCAR ERRO QUANDO TIVER UMA NOVA PRODUÇÃO PARA UMA CELULA JÁ PREENCHIDA
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.table = self._build_table()

    def _build_table(self):
        """
        Constrói a tabela LL(1) para a gramática fornecida.
        Retorna um dicionário onde as chaves são tuplas (não_terminal, terminal)
        e os valores são as produções correspondentes.
        Se uma célula já estiver preenchida, lança um erro.
        """

        table = dict()

        def raise_error(lhs, terminal, prod):
            error = f"Erro: célula ({lhs}, {terminal}) já preenchida com {table[(lhs, terminal)]} ao tentar inserir {prod}."
            raise ValueError(error)

        for prod in self.grammar.productions:
            lhs, rhs = prod.lhs, prod.rhs
            first_of_rhs = self.grammar.first_rhs(rhs)
            for terminal in first_of_rhs:
                if terminal != Grammar.EPSILON:
                    if (lhs, terminal) in table:
                        raise_error(lhs, terminal, prod)
                    table[(lhs, terminal)] = prod
            if Grammar.EPSILON in first_of_rhs:
                for terminal in self.grammar.follow_sets[lhs]:
                    if (lhs, terminal) in table:
                        raise_error(lhs, terminal, prod)
                    table[(lhs, terminal)] = prod
        return table

    def to_dataframe(self):
        """Converte a tabela LL(1) em um DataFrame do pandas."""
        df = pd.DataFrame.from_dict(self.table, orient="index")
        df.index = pd.MultiIndex.from_tuples(
            df.index, names=["NonTerminal", "Terminal"]
        )
        df = df.unstack()
        return df


class LL1ParserTable:
    def __init__(self, table: LL1Table, start_symbol: NonTerminal):
        self.table = table.table
        self.start_symbol = start_symbol

    def parse(self, tokens: list[Token]):
        """Realiza o parsing LL(1) para a lista de tokens fornecida."""
        # TODO: CRIAR ARVORE SINTATICA ABSTRATA (AST)
        token_EOF = Token(Grammar.EOF, "$")
        if not tokens or tokens[-1].terminal != Grammar.EOF:
            tokens.append(token_EOF)  # Adiciona o token EOF

        stack = [Grammar.EOF, self.start_symbol]
        input_tokens = tokens[:]
        cursor = 0
        # print(f"\nIniciando parsing LL(1) para entrada: {tokens}")
        while stack:
            top = stack.pop()
            current_token = (
                input_tokens[cursor] if cursor < len(input_tokens) else token_EOF
            )
            current_token, lexeme = (current_token.terminal, current_token.lexeme)
            # print(f"Pilha: {[str(s) for s in stack[::-1]]} | Próximo token: {current_token}")

            if isinstance(top, Terminal) or top == Grammar.EOF:
                if top == current_token:
                    # print(f"Consome token: {current_token}")
                    cursor += 1
                else:
                    print(f"Erro: esperado {top}, encontrado {current_token}")
                    return False
            elif isinstance(top, NonTerminal):
                prod = self.table.get((top, current_token))
                if prod:
                    # print(f"Aplica produção: {prod}")
                    rhs = prod.rhs
                    if not (len(rhs) == 1 and rhs[0] == Grammar.EPSILON):
                        for symbol in reversed(rhs):
                            stack.append(symbol)
                else:
                    print(f"Erro: nenhuma produção para ({top}, {current_token})")
                    return False
            else:
                print(f"Erro: símbolo desconhecido na pilha: {top}")
                return False
        if cursor == len(input_tokens):
            # print("Parsing bem-sucedido!")
            return True
        else:
            # print("Erro: tokens restantes após esvaziar a pilha.")
            return False


# ----------------------
# Exemplo de uso
# ----------------------
if __name__ == "__main__":
    # Definição dos símbolos
    S, A, B = [NonTerminal(name) for name in ["S", "A", "B"]]
    a, b, c, d = [Terminal(name) for name in ["a", "b", "c", "d"]]

    # Definição da gramática
    productions = [
        S >> [a, A, B, b],
        A >> [c],
        A >> [],
        B >> [d],
        B >> [],
    ]

    grammar = Grammar(
        start_symbol=S,
        terminals=[a, b, c, d],
        non_terminals=[S, A, B],
        productions=productions,
    )

    print(Fore.YELLOW + "Produções:")
    for prod in grammar.productions:
        print(prod)

    print(Fore.YELLOW + "\nTerminais da gramática:")
    print(grammar.terminals)
    print(Fore.YELLOW + "Não terminais da gramática:")
    print(grammar.non_terminals)

    print(Fore.YELLOW + "\nConjuntos FIRST:")
    for nt, first in grammar.first_sets.items():
        print(Fore.CYAN + f"{nt}:", Style.RESET_ALL, first)
    print(Fore.YELLOW + "\nConjuntos FOLLOW:")
    for nt, follow in grammar.follow_sets.items():
        print(Fore.CYAN + f"{nt}:", Style.RESET_ALL, follow)

    ll1_table = LL1Table(grammar)
    df = ll1_table.to_dataframe()
    print(Fore.YELLOW + "\nTabela LL(1) como DataFrame:")
    print(df)

    tokens = Tokenizer.tokenize("acdb", grammar)
    parser = LL1ParserTable(ll1_table, S)
    print(Fore.YELLOW + "\nTestando parsing LL(1):")
    parsed = parser.parse(tokens)
    if parsed:
        print(Fore.GREEN + "ACEITA." + Style.RESET_ALL)
    else:
        print(Fore.RED + "REJEITADA." + Style.RESET_ALL)
