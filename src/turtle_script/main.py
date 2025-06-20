from colorama import Fore
from grammar import grammar
from grammar import Terminal, NonTerminal
from grammar import Tokenizer, LL1Table, LL1ParserTable


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
            if isinstance(sym, Terminal):
                right += t_color + f"{sym.repr} "
            elif isinstance(sym, NonTerminal):
                right += non_t_color + f"{sym} "
        print(right)

    text = """
    inicio
        var inteiro : a, b, c = 3, 1, a;
        teste = "teste";
        se 1 * ( verdadeiro  != falso + 12) entao
            // negação
            avancar ! verdadeiro;
            avancar ! (verdadeiro);
            avancar ! (verdadeiro || falso);
            avancar ! (verdadeiro && falso);
            avancar  (verdadeiro == 1);
            
        senao
            girar_direita 10;
        fim_se;
    fim
    """

    tokens = Tokenizer.tokenize(text, grammar)

    print(Fore.RED + "Tokens encontrados:")
    for token in tokens:
        print(Fore.BLUE + token.terminal.name, end=": ")
        print(Fore.YELLOW + token.lexeme)

    ll1_table = LL1Table(grammar)
    ll1_parser_table = LL1ParserTable(ll1_table, grammar.start_symbol)
    parsed = ll1_parser_table.parse(tokens)

    print("-" * 30)

    if parsed:
        print(Fore.GREEN + "Análise sintática bem-sucedida!")
    else:
        print(Fore.RED + "Erro na análise sintática!")
    print("-" * 30)
