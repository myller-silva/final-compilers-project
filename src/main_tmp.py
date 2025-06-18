from utils.text import custom_print

from others.table_parser_ll1 import *

E, X, T, Y, F = [NonTerminal(name) for name in ["E", "X", "T", "Y", "F"]]
non_terminals = [E, X, T, Y, F]
start_symbol = E

# Definindo os terminais
mais = Terminal("mais", r"\+")
mult = Terminal("mult", r"\*")
abre = Terminal("abre", r"\(")
fecha = Terminal("fecha", r"\)")
id = Terminal("id", r"[a-zA-Z_][a-zA-Z0-9_]*")
terminals = [mais, mult, abre, fecha, id, Grammar.EOF]

# Definindo as produções da gramática
productions = [
    Production(E, [T, X]),  # E -> T X
    Production(X, [mais, T, X]),  # X -> + T X
    Production(X, [Grammar.EPSILON]),  # X -> ε
    Production(T, [F, Y]),  # T -> F Y
    Production(Y, [mult, F, Y]),  # Y -> * F Y
    Production(Y, [Grammar.EPSILON]),  # Y -> ε
    Production(F, [abre, E, fecha]),  # F -> ( E )
    Production(F, [id]),  # F -> id
]

# Definindo a gramática
grammar = Grammar(
    start_symbol=start_symbol,
    terminals=terminals,
    non_terminals=non_terminals,
    productions=productions,
)

custom_print(" Gramatica ", border_char="*")
print(grammar, end="\n\n")

print("Terminais:", grammar.terminals, end="\n\n")

print("Não terminais:", grammar.non_terminals, end="\n\n")

custom_print("Produções: ", width=0, border_char="", color_code=35, end="")
custom_print(grammar.productions, width=0, border_char="", color_code=33, end="\n\n")


ll1_table = LL1Table(grammar)
print("LL(1) Table:")
ll1_table.print_table()



# # Exemplo de tokenização
text = "id +\n id *  \n( id + id )\n"
tokenizer = Tokenizer()
tokens = tokenizer.tokenize(text, grammar)
# tokens.append(Token(Grammar.EOF, "EOF"))  # Adiciona o token EOF
custom_print("Tokens", border_char="*", color_code=34)
for token in tokens:
    print(token)

# Sintaxe LL(1) Parser
custom_print("LL(1) Parser", border_char="*", color_code=32)
parser = LL1ParserTable(ll1_table, start_symbol=start_symbol)
parser.parse(tokens)
