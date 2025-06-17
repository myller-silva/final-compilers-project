from anytree import RenderTree


def print_anytree(
    tree,
    color_terminal_type="\033[95m",
    color_terminal_value="\033[93m",
    color_reset="\033[0m",
):
    """Printa uma árvore formada com a biblioteca anytree."""
    for pre, _, node in RenderTree(tree):
        if ": " in node.name:  # Terminal: 'TIPO: valor'
            tipo, valor = node.name.split(": ", 1)
            print(
                f"{pre}{color_terminal_type}{tipo}{color_reset}",
                f"{color_terminal_value}{valor}{color_reset}"
                )
        else:
            print(f"{pre}{node.name}")


def print_tree_nice(node: tuple | str, prefix: str = "", is_last: bool = True) -> None:
    """
    Imprime uma árvore sintática em formato legível.

    Args:
        node: Nó da árvore a ser impresso.
        prefix: Prefixo para formatação.
        is_last: Indica se o nó é o último filho.
    """

    def format_prefix(prefix: str, is_last: bool) -> str:
        return prefix + ("└── " if is_last else "├── ")

    def is_token_tuple(node):
        """Verifica se o nó é uma tupla do tipo (str, str)."""
        return (
            isinstance(node, tuple)
            and len(node) == 2
            and isinstance(node[0], str)
            and isinstance(node[1], str)
        )

    if isinstance(node, tuple):
        label, children = node
        print(format_prefix(prefix, is_last) + str(label))
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            if is_token_tuple(child):
                print(
                    format_prefix(new_prefix, is_last_child)
                    + f"{child[0]} ── \033[92m{child[1]}\033[0m"
                )
            else:
                print_tree_nice(child, new_prefix, is_last_child)
    else:
        print(format_prefix(prefix, is_last) + str(node))


def print_grammar(grammar: list[tuple[str, list[str]]]) -> None:
    """
    Imprime a gramática de forma legível.

    Args:
        grammar: Lista de regras da gramática.
    """
    for left, right in grammar:
        if right == []:
            right = ["ε"]
        print(f"{left} -> {' '.join(right)}")


