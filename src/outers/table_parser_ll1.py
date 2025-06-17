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
    def __init__(self, lhs: NonTerminal, rhs: list):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        arrow = "→"
        rhs_str = " ".join(map(str, self.rhs)) if self.rhs else str(EPSILON)
        return f"{self.lhs} {arrow} {rhs_str}"


EPSILON = Symbol("ε")
EOF = Terminal("$")  # Símbolo de fim de arquivo (EOF)


def compute_first_sets(grammar: list[Production]):
    """Calcula os conjuntos FIRST para uma gramática livre de contexto."""
    first = defaultdict(set)

    def first_of(symbol):
        if isinstance(symbol, Terminal):
            return {symbol}
        return first[symbol]

    changed = True
    while changed:
        changed = False
        for prod in grammar:
            lhs, rhs = prod.lhs, prod.rhs
            original_size = len(first[lhs])

            if len(rhs) == 1 and rhs[0] == EPSILON:
                first[lhs].add(EPSILON)
            else:
                nullable = True
                for symbol in rhs:
                    symbol_first = first_of(symbol)
                    first[lhs].update(symbol_first - {EPSILON})
                    if EPSILON not in symbol_first:
                        nullable = False
                        break
                if nullable:
                    first[lhs].add(EPSILON)

            if len(first[lhs]) > original_size:
                changed = True

    return first



def compute_follow_sets(
    grammar: list[Production], start_symbol: NonTerminal, first_sets: dict
):
    """Calcula os conjuntos FOLLOW para uma gramática livre de contexto."""
    follow = defaultdict(set)
    follow[start_symbol].add(EOF)

    changed = True
    while changed:
        changed = False
        for prod in grammar[::-1]:  # Percorre as produções na ordem inversa
            lhs, rhs = prod.lhs, prod.rhs
            trailer = follow[lhs].copy()

            for i in reversed(
                range(len(rhs))
            ):  # Percorre o lado direito da produção de trás para frente
                symbol = rhs[i]

                if isinstance(symbol, NonTerminal):
                    original_size = len(follow[symbol])
                    follow[symbol].update(trailer)

                    if EPSILON in first_sets[symbol]:
                        trailer = trailer.union(first_sets[symbol] - {EPSILON})
                    else:
                        trailer = first_sets[symbol] - {EPSILON}

                    if len(follow[symbol]) > original_size:
                        changed = True

                elif isinstance(symbol, Terminal):
                    trailer = {symbol}  # trailer vira o próprio terminal

    return follow


# Exemplo de uso

S, A, B = [ NonTerminal(name) for name in ["S", "A", "B"]]
a, b, c, d = [ Terminal(name) for name in ["a", "b", "c", "d"]]


grammar = [
    Production(S, [a, A, B, b]),
    Production(A, [c]),
    Production(A, [EPSILON]),
    Production(B, [d]),
    Production(B, [EPSILON]),
]

for prod in grammar:
    print(prod)


def get_terminals(grammar):
    terminals = set({EOF})
    for prod in grammar:
        for sym in prod.rhs:
            if isinstance(sym, Terminal):
                terminals.add(sym)
    return terminals


def get_non_terminals(grammar):
    non_terminals = set()
    for prod in grammar:
        non_terminals.add(prod.lhs)
    return non_terminals


print("Terminais da gramática:")
terminals = get_terminals(grammar)
print(terminals)
print("Não terminais da gramática:")
non_terminals = get_non_terminals(grammar)
print(non_terminals)


first_sets = compute_first_sets(grammar)
follow_sets = compute_follow_sets(grammar, S, first_sets)


# -----------
print("\nConjuntos FIRST:")
for nt, first in first_sets.items():
    print(f"{nt}: {first}")

print("\nConjuntos FOLLOW:")
for nt, follow in follow_sets.items():
    print(f"{nt}: {follow}")


# ----------------------------
# Construção da tabela LL(1)
# ----------------------------


def first_rhs(symbols: list[Symbol], first_sets: dict[Symbol, set]) -> set:
    """Calcula o conjunto FIRST para uma sequência de símbolos (não terminais e terminais)."""

    result = set()
    for sym in symbols:
        if isinstance(sym, Terminal):
            result.add(sym)
            break
        elif isinstance(sym, NonTerminal):
            result.update(first_sets[sym] - {EPSILON})
            if EPSILON not in first_sets[sym]:
                break
    else:
        result.add(EPSILON)
    return result


def build_ll1_table(grammar, first_sets, follow_sets):
    table = {}

    for prod in grammar:
        lhs, rhs = prod.lhs, prod.rhs
        first_of_rhs = first_rhs(rhs, first_sets)

        for terminal in first_of_rhs:
            if terminal != EPSILON:
                table[(lhs, terminal)] = prod

        if EPSILON in first_of_rhs:
            for terminal in follow_sets[lhs]:
                table[(lhs, terminal)] = prod

    return table


ll1_table = build_ll1_table(grammar, first_sets, follow_sets)

def print_ll1_table(table, non_terminals, terminals):
    terminals = sorted(terminals, key=lambda x: x.name)
    non_terminals = sorted(non_terminals, key=lambda x: x.name)

    header = f"{'NT/T':>5}"
    for t in terminals:
        header += f"{Fore.CYAN}{str(t):>20}{Style.RESET_ALL}"
    print(header)
    print(Fore.YELLOW + "-" * (5 + 20 * len(terminals)) + Style.RESET_ALL)

    for nt in non_terminals:
        row = f"{Fore.CYAN}{str(nt):>5}{Style.RESET_ALL}"
        for t in terminals:
            prod = table.get((nt, t))
            if prod:
                cell = f"{Fore.GREEN}{str(prod):>20}{Style.RESET_ALL}"
            else:
                cell = f"{Fore.RED}{'':>20}{Style.RESET_ALL}"
            row += cell
        print(row)


print("\nTabela LL(1):")
print_ll1_table(ll1_table, non_terminals, terminals)


def ll1_parse(tokens, table, start_symbol):
    """
    tokens: lista de Terminals (incluindo EOF no final)
    table: tabela LL(1) (dict)
    start_symbol: símbolo inicial (NonTerminal)
    """
    stack = [EOF, start_symbol]
    input_tokens = tokens[:]
    cursor = 0
    print(f"\nIniciando parsing LL(1) para entrada: {[str(t) for t in tokens]}")
    while stack:
        top = stack.pop()
        current_token = input_tokens[cursor] if cursor < len(input_tokens) else None
        print(f"Pilha: {[str(s) for s in stack[::-1]]} | Próximo token: {current_token}")
        if isinstance(top, Terminal) or top == EOF:
            if top == current_token:
                print(f"Consome token: {current_token}")
                cursor += 1
            else:
                print(f"Erro: esperado {top}, encontrado {current_token}")
                return False
        elif isinstance(top, NonTerminal):
            prod = table.get((top, current_token))
            if prod:
                print(f"Aplica produção: {prod}")
                # Empilha da direita para esquerda
                rhs = prod.rhs
                if not (len(rhs) == 1 and rhs[0] == EPSILON):
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


# Exemplo de uso do parser LL(1)
test_input = [a, b, EOF]
print("\nTestando parsing LL(1):")
ll1_parse(test_input, ll1_table, S)
