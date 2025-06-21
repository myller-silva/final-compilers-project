from colorama import Fore
from grammar import grammar
from table_parser_ll1 import (
    Terminal,
    NonTerminal,
    Tokenizer,
    LL1Table,
    LL1ParserTable,
    Symbol,
)
from anytree import RenderTree

if __name__ == "__main__":

    print("--------------")
    print("Gramática")
    print("--------------")
    length = 90
    print(Fore.YELLOW + "-" * length)
    print(Fore.YELLOW + "Turtle Script Grammar".center(length, "-"))
    print(Fore.YELLOW + "-" * length)

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
            right += {
                Terminal: t_color + f"{sym.repr} ",
                NonTerminal: non_t_color + f"{sym} ",
                Symbol: Fore.LIGHTBLACK_EX + f"{sym} ",
            }[type(sym)]
        print(right)

    text = """
    inicio
        var inteiro : a, b, c = (3 || 1 ), 1, a;
        teste = "teste";
        se 1 * ( verdadeiro  != falso + 12) entao
            // negação
            avancar ! verdadeiro;
            avancar  (12);
        senao
            girar_direita 10;
        fim_se;
    fim
    """

    print(Fore.RED + "Tokens encontrados:")
    tokens = Tokenizer.tokenize(text, grammar)
    for token in tokens:
        print(Fore.BLUE + token.terminal.name, end=": ")
        print(Fore.YELLOW + token.lexeme)

    ll1_table = LL1Table(grammar)
    ll1_parser_table = LL1ParserTable(ll1_table, grammar.start_symbol)

    parsed, parsed_productions = ll1_parser_table.parse(tokens)

    print("-" * 30)
    print(
        {
            False: Fore.RED + "Erro na análise sintática!",
            True: Fore.GREEN + "Análise sintática bem-sucedida!",
        }[parsed]
    )

    print("-" * 30)
    print(Fore.YELLOW + "Árvore de Derivação:")
    derivation_tree = ll1_parser_table.build_derivation_tree(parsed_productions)
    for pre, fill, node in RenderTree(derivation_tree):
        cor = Fore.BLACK if isinstance(node.name, NonTerminal) else Fore.RED
        print(f"{pre}{cor}{node.name}")
    print("-" * 30)
