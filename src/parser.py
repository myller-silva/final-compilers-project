class RecursiveDescentParser:
    def __init__(self, grammar: list[tuple[str, list[str]]], start_symbol: str, debug: bool = False):
        """
        Inicializa o parser com uma gramática e um símbolo inicial.

        Args:
            grammar: Lista de regras da gramática.
            start_symbol: Símbolo inicial da gramática.
        """
        self.debug = debug
        self.grammar = self._organize_grammar(grammar)
        self.start_symbol = start_symbol
        self.tokens: list[str] = []
        self.pos: int = 0

    def _organize_grammar(
        self, rules: list[tuple[str, list[str]]]
    ) -> dict[str, list[list[str]]]:
        """
        Organiza a gramática em um formato mais acessível.

        Args:
            rules: Lista de regras da gramática.

        Returns:
            Um dicionário com as regras organizadas.
        """
        grammar = {}
        for left, right in rules:
            if left not in grammar:
                grammar[left] = []
            grammar[left].append(right)
        return grammar

    def parse(self, tokens: list[tuple[str, str]]) -> tuple[str, list]:
        """
        Realiza a análise sintática dos tokens fornecidos.

        Args:
            tokens: Lista de tokens de entrada.

        Returns:
            Árvore sintática gerada.

        Raises:
            SyntaxError: Se houver erro de sintaxe.
        """
        try:  # Verifica se os tokens são válidos antes de processá-los
            self.tokens = tokens
        except IndexError:
            raise ValueError("Os tokens fornecidos não estão no formato esperado (tuplas com dois elementos).")

        self.pos = 0
        self.last_valid_token = None  # Armazena o último token válido
        success, tree = self._parse_symbol(self.start_symbol)
        if success and self.pos == len(self.tokens):
            return tree
        else:
            current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            raise SyntaxError(
                f"Erro de sintaxe perto de '{current_token[1]}' na posição {self.pos}. "
                f"Último token válido: '{self.last_valid_token[1]}'"
                f"Tokens restantes: {self.tokens[self.pos:]}. "
                f"Esperado: {self.start_symbol}."
            )

    def current(self) -> str | None:
        """Retorna o token atual ou None se não houver mais tokens."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _parse_symbol(self, symbol: str) -> tuple[bool, tuple | str | None]:
        """
        Tenta analisar um símbolo da gramática.

        Args:
            symbol: Símbolo a ser analisado.

        Returns:
            Um tuple indicando sucesso e o nó gerado.

        Raises:
            SyntaxError: Se houver erro de sintaxe.
        """
        if self.debug:
            print(f"{symbol} *** {self.current()}  ***  {symbol == self.current()} *** {self.pos}")
        if symbol not in self.grammar:  # terminal
            current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            if current_token and current_token[0] == symbol:
                self.last_valid_token = current_token  # Atualiza o último token válido
                self.pos += 1
                return True, symbol
            else:
                raise SyntaxError(
                    f"Erro de sintaxe: esperado '{symbol}', mas encontrado '{current_token[1]}' na posição {self.pos}."
                )

        for production in self.grammar[symbol]:
            snapshot = self.pos  # salva a posição atual para backtrack
            children = []
            success = True
            for sym in production:  # cada símbolo na produção
                try:
                    ok, node = self._parse_symbol(sym)
                except SyntaxError as e:
                    success = False
                    break
                if not ok:
                    success = False
                    break
                children.append(node)
            if success:
                return True, (symbol, children)
            self.pos = snapshot  # backtrack

        current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        raise SyntaxError(
            f"\nErro de sintaxe: não foi possível analisar '{symbol}' na posição {self.pos}. "
            f"\nToken atual: '{current_token[1] if current_token else 'EOF'}'. "
            f"\nUltimo token válido: '{self.last_valid_token[1] if self.last_valid_token else 'N/A'}'."
        )


# if __name__ == "__main__":
#     from utils import print_grammar, print_tree_nice
#     # Gramática de exemplo (Lista de Parênteses)
#     grammar = [
#         ("Alvo", ["Lista"]),
#         ("Lista", ["Par", "Lista"]),
#         ("Lista", ["Par"]),
#         ("Par", ["(", "Par", ")"]),
#         ("Par", ["(", ")"]),
#     ]
#     print("-- Gramática --")
#     print_grammar(grammar)

#     # Tokens de entrada
#     tokens = [ # chave / valor
#         ("(", "("),
#         (")", ")"),
#         ("(", "("),
#         (")", ")"),
#         ("(", "("),
#         (")", ")"),
#     ]
#     print("\n-- Tokens --")
#     print("Tokens:", " ".join([token[1] for token in tokens]))
#     print("\n-- Análise Sintática --")

#     parser = RecursiveDescentParser(grammar, "Alvo")

#     abstract_syntax_tree = parser.parse(tokens)
#     print_tree_nice(abstract_syntax_tree)


if __name__ == "__main__":
    from constants import *
    from tokenizer import Tokenizer
    from utils import print_grammar, print_tree_nice
    
    # Exemplo simples
    grammar = [
        ("Programa", ["Bloco"]),
        ("Bloco", [KW_INICIO_BLOCO, "Comandos", KW_FIM_BLOCO]),
        ("Bloco", []),
        ("Comandos", ["Comando", "Comandos"]),
        ("Comandos", []),
        ("Comando", [CMD_AVANCAR, INTEIRO, PONTO_VIRGULA]),
        ("Expressao", [INTEIRO]),
    ]
    print("-- Gramática --")
    print_grammar(grammar)

    word = """
    inicio
    avancar 10;
    fim
    """

    tokens = Tokenizer(word).tokenize()
    parser = RecursiveDescentParser(grammar, "Programa")
    abstract_syntax_tree = parser.parse(tokens)
    print("-- Árvore Sintática Abstrata --")
    print_tree_nice(abstract_syntax_tree)