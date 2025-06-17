from collections import defaultdict
from colorama import Fore, Style, init

init(autoreset=True)


class Symbol:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def __hash__(self):
        return hash((self.name, type(self)))


class NonTerminal(Symbol):
    pass


class Terminal(Symbol):
    pass


class Production:
    def __init__(self, lhs: NonTerminal, rhs: list[Symbol]):
        assert isinstance(lhs, NonTerminal), f"LHS must be a NonTerminal but got {type(lhs).__name__}"
        assert all(isinstance(sym, Symbol) for sym in rhs), "RHS must be a list of Symbols"
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        arrow = "→"
        rhs_str = " ".join(map(str, self.rhs)) if self.rhs else str(Grammar.EPSILON)
        return f"{self.lhs} {arrow} {rhs_str}"


class Grammar:
    EPSILON = Symbol("ε")
    EOF = Terminal("$")

    def __init__(self, productions: list[Production], start_symbol: NonTerminal):
        self.productions = productions
        self.start_symbol = start_symbol
        self.terminals = self._get_terminals()
        self.non_terminals = self._get_non_terminals()
        self.first_sets = self.compute_first_sets()
        self.follow_sets = self.compute_follow_sets()

    def _get_terminals(self):
        terminals = set({Grammar.EOF})
        for prod in self.productions:
            for sym in prod.rhs:
                if isinstance(sym, Terminal):
                    terminals.add(sym)
        return terminals

    def _get_non_terminals(self):
        non_terminals = set()
        for prod in self.productions:
            non_terminals.add(prod.lhs)
        return non_terminals

    def compute_first_sets(self):
        first = defaultdict(set)

        def first_of(symbol):
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


class LL1Table:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.table = self.build_ll1_table()

    def build_ll1_table(self):
        table = {}
        for prod in self.grammar.productions:
            lhs, rhs = prod.lhs, prod.rhs
            first_of_rhs = self.grammar.first_rhs(rhs)
            for terminal in first_of_rhs:
                if terminal != Grammar.EPSILON:
                    table[(lhs, terminal)] = prod
            if Grammar.EPSILON in first_of_rhs:
                for terminal in self.grammar.follow_sets[lhs]:
                    table[(lhs, terminal)] = prod
        return table

    def print_table(self):
        terminals = sorted(self.grammar.terminals, key=lambda x: x.name)
        non_terminals = sorted(self.grammar.non_terminals, key=lambda x: x.name)
        header = f"{'NT/T':>5}"
        for t in terminals:
            header += f"{Fore.CYAN}{str(t):>20}{Style.RESET_ALL}"
        print(header)
        print(Fore.YELLOW + "-" * (5 + 20 * len(terminals)) + Style.RESET_ALL)
        for nt in non_terminals:
            row = f"{Fore.CYAN}{str(nt):>5}{Style.RESET_ALL}"
            for t in terminals:
                prod = self.table.get((nt, t))
                if prod:
                    cell = f"{Fore.GREEN}{str(prod):>20}{Style.RESET_ALL}"
                else:
                    cell = f"{Fore.RED}{'':>20}{Style.RESET_ALL}"
                row += cell
            print(row)


class LL1ParserTable:
    def __init__(self, table: LL1Table, start_symbol: NonTerminal):
        self.table = table.table
        self.start_symbol = start_symbol

    def parse(self, tokens: list[Terminal]):
        stack = [Grammar.EOF, self.start_symbol]
        input_tokens = tokens[:]
        cursor = 0
        print(f"\nIniciando parsing LL(1) para entrada: {[str(t) for t in tokens]}")
        while stack:
            top = stack.pop()
            current_token = input_tokens[cursor] if cursor < len(input_tokens) else None
            print(
                f"Pilha: {[str(s) for s in stack[::-1]]} | Próximo token: {current_token}"
            )
            if isinstance(top, Terminal) or top == Grammar.EOF:
                if top == current_token:
                    print(f"Consome token: {current_token}")
                    cursor += 1
                else:
                    print(f"Erro: esperado {top}, encontrado {current_token}")
                    return False
            elif isinstance(top, NonTerminal):
                prod = self.table.get((top, current_token))
                if prod:
                    print(f"Aplica produção: {prod}")
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
            print("Parsing bem-sucedido!")
            return True
        else:
            print("Erro: tokens restantes após esvaziar a pilha.")
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
        Production(S, [a, A, B, b]),
        Production(A, [c]),
        Production(A, [Grammar.EPSILON]),
        Production(B, [d]),
        Production(B, [Grammar.EPSILON]),
    ]
    grammar = Grammar(productions, S)

    print("Produções:")
    for prod in grammar.productions:
        print(prod)
    print("\nTerminais da gramática:")
    print(grammar.terminals)
    print("Não terminais da gramática:")
    print(grammar.non_terminals)

    print("\nConjuntos FIRST:")
    for nt, first in grammar.first_sets.items():
        print(f"{nt}: {first}")
    print("\nConjuntos FOLLOW:")
    for nt, follow in grammar.follow_sets.items():
        print(f"{nt}: {follow}")

    ll1_table = LL1Table(grammar)
    print("\nTabela LL(1):")
    ll1_table.print_table()

    tokens = [a, b, Grammar.EOF]
    parser = LL1ParserTable(ll1_table, S)
    print("\nTestando parsing LL(1):")
    parser.parse(tokens)
