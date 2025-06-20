from colorama import Fore
from grammar import grammar

length = 90
print(Fore.YELLOW + "-" * length)
print(Fore.YELLOW + "Turtle Script Grammar".center(length, "-"))
print(Fore.YELLOW + "-" * length)

from grammar import Terminal, NonTerminal
for rule in grammar.productions:
    left = rule.lhs.name
    t_color = Fore.RED
    non_t_color = Fore.LIGHTBLUE_EX
    arrow_color = Fore.LIGHTBLACK_EX
    print(non_t_color + f"{left:20}", end="")
    print(arrow_color + " → ", end="")
    right = ""
    if rule.rhs == []:
        right = t_color + "ε"
    for sym in rule.rhs:
        if isinstance(sym, Terminal):
            right += t_color + f"{sym.repr} "
        elif isinstance(sym, NonTerminal):
            right += non_t_color + f"{sym} "
    print(right)
