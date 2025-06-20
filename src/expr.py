"""
# Expr        ::= OrExpr

# OrExpr      ::= AndExpr { "||" AndExpr }
# AndExpr     ::= NotExpr { "&&" NotExpr }
# NotExpr     ::= "!" NotExpr
#               | AddExpr

# AddExpr     ::= MulExpr { ("+" | "-") MulExpr }
# MulExpr     ::= UnaryExpr { ("*" | "/") UnaryExpr }
# UnaryExpr   ::= ("+" | "-")? Primary
# Primary     ::= "(" Expr ")"
#               | Identifier
#               | Literal

# Identifier  ::= [a-zA-Z_][a-zA-Z0-9_]*
# Literal     ::= [0-9]+

Expr         -> OrExpr
OrExpr       -> AndExpr OrExprTail
OrExprTail   -> "||" AndExpr OrExprTail
            | ε
AndExpr      -> NotExpr AndExprTail
AndExprTail  -> "&&" NotExpr AndExprTail
            | ε
NotExpr      -> "!" NotExpr
            | AddExpr
AddExpr      -> MulExpr AddExprTail
AddExprTail  -> "+" MulExpr AddExprTail
            | "-" MulExpr AddExprTail
            | ε
MulExpr      -> UnaryExpr MulExprTail
MulExprTail  -> "*" UnaryExpr MulExprTail
            | "/" UnaryExpr MulExprTail
            | ε
UnaryExpr    -> "+" UnaryExpr
            | "-" UnaryExpr
            | Primary
Primary      -> "(" Expr ")"
            | Identifier
            | Literal
Identifier   -> [a-zA-Z_][a-zA-Z0-9_]*
Literal      -> [0-9]+


"""

from others.table_parser_ll1 import NonTerminal, Terminal

# --- NON-TERMINALS ---
Expr = NonTerminal("Expr")
OrExpr = NonTerminal("OrExpr")
OrExprTail = NonTerminal("OrExprTail")
AndExpr = NonTerminal("AndExpr")
OrExprTail = NonTerminal("OrExprTail")
AndExprTail = NonTerminal("AndExprTail")
NotExpr = NonTerminal("NotExpr")
AndExprTail = NonTerminal("AndExprTail")
AddExpr = NonTerminal("AddExpr")
AddExprTail = NonTerminal("AddExprTail")
MulExpr = NonTerminal("MulExpr")
MulExprTail = NonTerminal("MulExprTail")
UnaryExpr = NonTerminal("UnaryExpr")
Primary = NonTerminal("Primary")
Identifier = NonTerminal("Identifier")
Literal = NonTerminal("Literal")

non_terminals = [
    Expr,
    OrExpr,
    OrExprTail,
    AndExpr,
    AndExprTail,
    NotExpr,
    AddExpr,
    AddExprTail,
    MulExpr,
    MulExprTail,
    UnaryExpr,
    Primary,
    Identifier,
    Literal,
]

import re
# --- TERMINALS ---
iden = Terminal("iden", r"[a-zA-Z_][a-zA-Z0-9_]*")
inteiro = Terminal("int", r"[0-9]+")
open_paren = Terminal("open_paren", re.escape("("))
close_paren = Terminal("close_paren", re.escape(")"))
op_plus = Terminal("op_plus", re.escape("+"))
op_minus = Terminal("op_minus", re.escape("-"))
op_mul = Terminal("op_mul", re.escape("*"))
op_div = Terminal("op_div", re.escape("/"))
op_or = Terminal("op_or", re.escape("||"))
op_and = Terminal("op_and", re.escape("&&"))
op_not = Terminal("op_not", re.escape("!"))

terminals = [
    iden,
    inteiro,
    op_or,
    op_and,
    op_not,
    op_plus,
    op_minus,
    op_mul,
    op_div,
    open_paren,
    close_paren,
]

# --- PRODUCTIONS ---
productions = [
    Expr >> [OrExpr],
    OrExpr >> [AndExpr, OrExprTail],
    OrExprTail >> [op_or, AndExpr, OrExprTail],
    OrExprTail >> [],  # ε
    AndExpr >> [NotExpr, AndExprTail],
    AndExprTail >> [op_and, NotExpr, AndExprTail],
    AndExprTail >> [],  # ε
    NotExpr >> [op_not, NotExpr],
    NotExpr >> [AddExpr],
    AddExpr >> [MulExpr, AddExprTail],
    AddExprTail >> [op_plus, MulExpr, AddExprTail],
    AddExprTail >> [op_minus, MulExpr, AddExprTail],
    AddExprTail >> [],  # ε
    MulExpr >> [UnaryExpr, MulExprTail],
    MulExprTail >> [op_mul, UnaryExpr, MulExprTail],
    MulExprTail >> [op_div, UnaryExpr, MulExprTail],
    MulExprTail >> [],  # ε
    UnaryExpr >> [op_plus, UnaryExpr],
    UnaryExpr >> [op_minus, UnaryExpr],
    UnaryExpr >> [Primary],
    Primary >> [open_paren, Expr, close_paren],
    Primary >> [Identifier],
    Primary >> [Literal],
    Identifier >> [iden],
    Literal >> [inteiro],
]

print("Productions:")
for prod in productions:
    print(prod)

from others.table_parser_ll1 import Grammar
from others.table_parser_ll1 import LL1Table, LL1ParserTable, Tokenizer

grammar = Grammar(
    start_symbol=Expr,
    terminals=terminals,
    non_terminals=non_terminals,
    productions=productions,
)

ll1_table = LL1Table(grammar=grammar)
parser = LL1ParserTable(table=ll1_table, start_symbol=grammar.start_symbol)

texts = [
    " a || !e && f * g / h + i - j",
    "x || y && z",
    "!(a + b) * c",
    "x + y * z - w / v",
    "a || b && c || d",
    "x * (y + z) - w / v",
    "!(x + y) * z || a && b",
    "x + (y - z) * (a / b)",
    "!(x || y) && (z + a) * b",
    "x + y * z - (w / v) || a && b",
    "((a + b) * c) || (d - e) && f",
    "x || (y && z) * (a + b)",
    "!(x + y) || (z * a) && b",
    "x * (y + z) - (w / v) || a && b",
    "!(a + b) * (c - d) || e && f * g / h + i - j",
]

from utils.text import colorize_text
print('--' * 20)
for text in texts:
    # print('--' * 20)
    tokens = Tokenizer.tokenize(text=text, grammar=grammar)

    parsed = parser.parse(tokens=tokens)  # Example input
    print(colorize_text(str(parsed), color="blue" if parsed else "red"))
    print('--' * 20)
    