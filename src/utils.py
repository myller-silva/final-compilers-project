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

    if isinstance(node, tuple):
        label, children = node
        print(format_prefix(prefix, is_last) + str(label))
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
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
