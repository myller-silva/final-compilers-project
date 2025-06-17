class RecursiveDescentParser:
    def __init__(
        self,
        grammar: list[tuple[str, list[str]]],
        start_symbol: str,
    ):
        """
        Inicializa o parser com uma gramática e um símbolo inicial.

        Args:
            grammar: Lista de regras da gramática.
            start_symbol: Símbolo inicial da gramática.
        """
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
        self.tokens = tokens

        self.pos = 0
        self.last_valid_token = None  # Armazena o último token válido
        success, tree = self._parse_symbol(self.start_symbol)
        if success and self.pos == len(self.tokens):
            return tree
        else:
            current_token = (
                self.tokens[self.pos] if self.pos < len(self.tokens) else None
            )
            raise SyntaxError(
                f"Erro de sintaxe perto de '{current_token[1]}' na posição {self.pos}. "
                f"Último token válido: '{self.last_valid_token[1]}'"
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
        if symbol not in self.grammar:  # terminal
            current_token = (
                self.tokens[self.pos] if self.pos < len(self.tokens) else None
            )
            if current_token and current_token[0] == symbol:
                self.last_valid_token = current_token  # Atualiza o último token válido
                self.pos += 1
                return True, current_token  # Retorna o token completo
            else:
                encontrado = current_token[1] if current_token else "EOF"
                raise SyntaxError(
                    f"Erro de sintaxe: esperado '{symbol}', mas encontrado '{encontrado}' na posição {self.pos}."
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


def transformar_lista_aplanada(simbolo_lista):
    def transform(filhos, derivacao_para_ast, ignorar, transformar):
        itens = []
        for filho in filhos:
            ast = derivacao_para_ast(filho, ignorar, transformar)
            if ast is None:
                continue
            # Se o filho também é o mesmo símbolo, aplainar
            if isinstance(ast, tuple) and ast[0] == simbolo_lista:
                itens.extend(ast[1])
            else:
                itens.append(ast)
        return (simbolo_lista, itens)

    return transform

def derivacao_para_ast(node, ignorar=None, transformar=None):
    """
    Converte uma árvore de derivação em uma árvore sintática abstrata (AST).
    - node: nó da árvore de derivação (tupla ou token)
    - ignorar: conjunto de símbolos/terminais a serem ignorados (ex: pontuação, palavras-chave)
    - transformar: dict opcional {simbolo: função(children) -> nó_ast}
    """
    if ignorar is None:
        ignorar = set()
    if transformar is None:
        transformar = dict()

    # Nó terminal (token): ('TIPO', 'valor')
    if isinstance(node, tuple) and len(node) == 2 and isinstance(node[1], str):
        tipo, valor = node
        if tipo in ignorar:
            return None
        # return node  # Ou só valor, se preferir
        return valor

    # Nó não-terminal: ('Simbolo', [filhos])
    if isinstance(node, tuple) and len(node) == 2 and isinstance(node[1], list):
        simbolo, filhos = node
        # Se houver função de transformação para este símbolo, use-a
        if simbolo in transformar:
            return transformar[simbolo](
                filhos, derivacao_para_ast, ignorar, transformar
            )
        # Caso padrão: processa filhos recursivamente, removendo os ignorados
        filhos_ast = []
        for filho in filhos:
            ast = derivacao_para_ast(filho, ignorar, transformar)
            if ast is not None:
                filhos_ast.append(ast)
        # Se só tem um filho, pode "colapsar" o nó
        if len(filhos_ast) == 1:
            return filhos_ast[0]
        # Se não tem filhos, retorna None
        if not filhos_ast:
            return None
        return (simbolo, filhos_ast)
    # Caso não reconhecido
    return node


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
#     tokens = [ # Simulando entrada tokenizada
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
        ("Comando", [CMD_AVANCAR, "Expressao", PONTO_VIRGULA]),
        ("Expressao", ["Literal", "ExpressaoR"]),
        ("Expressao", ["Literal", "ExpressaoR"]),
        ("ExpressaoR", [OP_MAIS, "Literal", "ExpressaoR"]),
        ("ExpressaoR", [OP_MULTIPLICACAO, "Literal", "ExpressaoR"]),
        ("ExpressaoR", []),
        ("Literal", [INTEIRO]),
        ("Literal", [IDENTIFICADOR]),
    ]
    print("-- Gramática --")
    print_grammar(grammar)

    word = """
    inicio
        avancar 10 ;
        avancar 11 + teste + 1;
    fim
    """

    tokens = Tokenizer(word).tokenize()
    parser = RecursiveDescentParser(grammar, "Programa")
    concret_tree = parser.parse(tokens)
    print("-- Árvore de Derivação --")
    print_tree_nice(concret_tree)

    print("\n-- Árvore Sintática Abstrata (AST) --")
    transformar = {
        "Comandos": transformar_lista_aplanada("Comandos"),
        "DeclaracoesVariaveis": transformar_lista_aplanada("DeclaracoesVariaveis"),
        "Expressao": transformar_lista_aplanada("Expressao"),
        # "ExpressaoR": transformar_lista_aplanada("ExpressaoR"),
    }
    ast = derivacao_para_ast(
        concret_tree,
        ignorar={  # Ignorar pontuação e palavras-chave
            PONTO_VIRGULA,
            KW_INICIO_BLOCO,
            KW_FIM_BLOCO,
        },
        transformar=transformar,
    )
    print_tree_nice(ast)
