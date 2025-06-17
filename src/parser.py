from anytree import Node
import re


class RecursiveDescentParser:
    def __init__(
        self,
        grammar: list[tuple[str, list[str]]],
        start_symbol: str,
        debug: bool = False,
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
        self.debug = debug

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

    def parse(self, tokens: list[tuple[str, str]]):
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
        self.last_position = 0  # Armazena a última posição válida
        success, tree = self._parse_symbol(self.start_symbol, parent=None)
        if success and self.pos == len(self.tokens):
            return tree
        else:
            current_token = (
                self.tokens[self.pos] if self.pos < len(self.tokens) else None
            )
            raise SyntaxError(
                f"Erro de sintaxe perto de '{current_token[1]}' na posição {self.pos}. "
                f"Último token válido: '{self.last_valid_token[1]}'"
                f" na posição {self.last_position}."
            )

    def current(self) -> str | None:
        """Retorna o token atual ou None se não houver mais tokens."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _parse_symbol(self, symbol: str, parent=None):
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
                self.last_valid_token = current_token
                self.last_position = self.pos
                self.pos += 1
                node = Node(f"{symbol}: {current_token[1]}", parent=parent)
                return True, node  # Retorna o token completo
            else:
                encontrado = current_token[1] if current_token else "EOF"
                raise SyntaxError(
                    f"Erro de sintaxe: esperado '{symbol}', mas encontrado '{encontrado}' na posição {self.pos}."
                    f" Último token válido: '{self.last_valid_token[1]}'"
                    f" na posição {self.last_position}."
                )

        for production in self.grammar[symbol]:
            snapshot = self.pos  # salva a posição atual para backtrack
            children = []
            success = True
            node = Node(symbol, parent=parent)
            for sym in production:  # cada símbolo na produção
                try:
                    ok, child_node = self._parse_symbol(sym, parent=node)
                except SyntaxError as e:
                    success = False
                    break
                if not ok:
                    success = False
                    break
                children.append(child_node)
            if success:
                return True, node
            self.pos = snapshot  # backtrack

        current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        raise SyntaxError(
            f"Erro de sintaxe. "
            f"Último token válido: '{self.last_valid_token[1]}'"
            f" na posição {self.last_position}. "
        )

    @staticmethod
    def to_abstract_syntax_tree(
        node, ignored_terms=set(), flattening_transforms=set(), parent=None
    ):
        """
        Converte uma árvore de derivação em uma árvore sintática abstrata (AST).
        Args:
            node: Nó da árvore de derivação.
            ignored_terms: Conjunto de termos a serem ignorados.
            flattening_transforms: Mapeamento de transformações para aplanamento.
            parent: Nó pai na árvore AST.
        Returns:
            Um nó da árvore sintática abstrata (AST) ou None se o nó for ignorado.
        """

        label = node.name  # Nó terminal: formato 'TIPO: valor'
        if ": " in label:
            node_type, node_value = (
                re.match(r"^(.*?): (.*)$", label).groups()
                if ": " in label
                else (label, None)
            )
            if node_type in ignored_terms:
                return None
            return (
                Node(f"{node_type}: {node_value}", parent=parent)
                if node_value is not None
                else Node(node_type, parent=parent)
            )
        else:
            symbol_name = label
            filhos_nodes = list(node.children)
            child_ast_nodes = []
            for child in filhos_nodes:
                ast_child = RecursiveDescentParser.to_abstract_syntax_tree(
                    child, ignored_terms, flattening_transforms, parent=None
                )
                if ast_child is not None:
                    child_ast_nodes.append(ast_child)

            if (
                symbol_name in flattening_transforms
            ):  # Transformação customizada. A função de transformação deve criar e retornar um Node do anytree
                return flattening_transforms[symbol_name](
                    child_ast_nodes,
                    RecursiveDescentParser.to_abstract_syntax_tree,
                    ignored_terms,
                    flattening_transforms,
                    parent,
                )
            if not child_ast_nodes:
                return None
            ast_node = Node(symbol_name, parent=parent)
            for child in child_ast_nodes:
                child.parent = ast_node
            return ast_node

    @staticmethod
    def flatten_children_anytree(simbolo_lista):
        def transform(filhos, to_ast, ignorar, transformar, parent):
            itens = []
            for filho in filhos:
                if filho is None:
                    continue
                # Se o filho também é o mesmo símbolo, aplainar
                if isinstance(filho, Node) and filho.name == simbolo_lista:
                    itens.extend(list(filho.children))
                else:
                    itens.append(filho)
            if not itens:
                return None
            node = Node(simbolo_lista, parent=parent)
            for item in itens:
                item.parent = node
            return node
        return transform


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
    from utils import print_grammar
    from utils import print_anytree
    from utils.text import custom_print

    grammar = [
        ("Programa", ["Bloco"]),
        ("Bloco", [KW_INICIO_BLOCO, "Comandos", KW_FIM_BLOCO]),
        ("Bloco", []),
        ("Comandos", ["Comando", "Comandos"]),
        ("Comandos", []),
        ("Comando", [CMD_AVANCAR, "Expressao", PONTO_VIRGULA]),
        ("Expressao", ["Literal", "ExpressaoR"]),
        ("ExpressaoR", [OP_MAIS, "Literal", "ExpressaoR"]),
        ("ExpressaoR", [OP_MULTIPLICACAO, "Literal", "ExpressaoR"]),
        ("ExpressaoR", []),
        ("Literal", [INTEIRO]),
        ("Literal", [IDENTIFICADOR]),
    ]
    custom_print(" Gramática ", border_char="*")
    print_grammar(grammar)

    word = """
    inicio
        avancar 10 ;
        avancar 11 + teste + 1 +1 ; // semanticamente errado, mas sintaticamente correto
    fim
    """

    tokens = Tokenizer(word).tokenize()
    parser = RecursiveDescentParser(grammar, "Programa")
    derivation_tree = parser.parse(tokens)

    custom_print("Árvore de Derivação", border_char="*")
    print_anytree(derivation_tree)

    custom_print("Árvore Sintática Abstrata (AST)", border_char="*")
    to_flatten = ["Comandos", "DeclaracaoVariavel", "Expressao", "ExpressaoR"]
    flattening_transforms = {
        key: parser.flatten_children_anytree(key) 
        for key in to_flatten
    }
    ast_node = parser.to_abstract_syntax_tree(
        derivation_tree,
        ignored_terms={  # Ignorar pontuação e palavras-chave
            PONTO_VIRGULA,
            KW_INICIO_BLOCO,
            KW_FIM_BLOCO,
        },
        flattening_transforms=flattening_transforms,
        parent=None,
    )
    print_anytree(ast_node)
