from colorama import Fore
from anytree import RenderTree, Node
from itertools import chain
from grammar import *
from table_parser_ll1 import LL1Table, LL1ParserTable, Token, Tokenizer


def is_empty(node: Node) -> bool:
    """Verifica se um nó é vazio (não possui filhos ou é epsilon)."""
    return len(node.children) == 0 or node.children[0] == Grammar.EPSILON


def flatten(items):
    """Achata uma lista de itens, processando apenas os elementos que são listas."""
    if not items:
        return []
    while any(isinstance(item, list) for item in items):
        items = list(
            chain.from_iterable(
                item if isinstance(item, list) else [item] for item in items
            )
        )
    return [item for item in items if item is not None]


def get_ast_root(derivation_tree_root: Node) -> Node:
    """Obtém a árvore sintática abstrata (AST) a partir da raiz da árvore de derivação."""
    return f_program(derivation_tree_root)


def f_program(root: Node) -> Node:
    """Processa o programa, que é o nó raiz da árvore de derivação."""
    _, decs, cmds, _ = root.children
    decs, cmds = f_declarations(decs), f_commands(cmds)
    children = []
    if decs:
        children.append(decs)
    if cmds:
        children.append(cmds)
    return Node(name=root.name, children=flatten(children))


def f_declarations(root: Node) -> list:
    """Processa as declarações de variáveis no programa."""
    if is_empty(root):
        return None
    var_dec, dec = root.children
    var_dec, dec = f_variable_declaration(var_dec), f_declarations(dec)
    if not dec:
        return [var_dec]
    return [var_dec] + [dec]


def f_variable_declaration(root: Node) -> Node:
    """Processa a declaração de uma variável."""
    _, type_node, assign_variable, _ = root.children
    type_node = f_type(type_node)
    op_att, children_att = f_assign_variable(assign_variable)
    return Node(op_att.name, children=[type_node] + children_att)


def f_type(root: Node) -> Node:
    """Processa o tipo de uma variável."""
    kw = root.children[0]
    return Node(kw.name)


def f_assign_variable(root: Node) -> Node:
    """Processa a atribuição de variáveis."""
    op_var_def, ids, ids_assignment = root.children
    ids, ids_assignment = f_identifiers(ids), f_identifiers_assignment(ids_assignment)
    children = [ids]
    if len(ids_assignment) != 0:
        children.append(Node(name=op_atribuicao))
    children.append(ids_assignment)
    return op_var_def, flatten(children)


def f_identifiers(root: Node) -> list:
    """Retorna lista de identificadores."""
    id, idR = root.children
    idR = f_identifiersR(idR)
    if not idR:
        return [id]
    return [id] + idR


def f_identifiersR(root: Node) -> list:
    """Retorna lista de identificadores adicionais."""
    if is_empty(root):
        return []
    _, id, idR = root.children
    idR = f_identifiersR(idR)
    if not idR:
        return [id]
    return [id] + idR


def f_identifiers_assignment(root: Node) -> list:
    """Processa a atribuição de identificadores."""
    if is_empty(root):
        return []
    _, expr, iaR = root.children
    expr, iaR = f_expr(expr), f_identifiers_assignmentR(iaR)
    if not iaR:
        return [expr]
    return [expr] + iaR


def f_identifiers_assignmentR(root: Node) -> Node:
    """Processa a atribuição de identificadores adicionais."""
    if is_empty(root):
        return []
    _, expr, iaR = root.children
    expr, iaR = f_expr(expr), f_identifiers_assignmentR(iaR)
    if not iaR:
        return [expr]
    return [expr] + iaR


def f_commands(root: Node) -> list:
    """Processa os comandos do programa."""
    if is_empty(root):
        return []
    cmd, cmds = root.children
    cmd, cmds = f_command(cmd), f_commands(cmds)
    if not cmds:
        return [cmd]
    return [cmd] + cmds


def f_command(root: Node) -> Node:
    """Processa um comando, despachando para a função apropriada conforme o tipo."""
    child = root.children[0]
    dispatch_map = {
        AssignValue: f_assign_value,
        Conditional: f_conditional,
        Loop: f_loop,
        Movement: f_generic_command,
        PenControl: f_generic_command,
        ScreenControl: f_generic_command,
    }
    handler = dispatch_map.get(child.name)
    if handler:
        return handler(child)
    return child


def f_assign_value(root: Node) -> Node:
    """Processa o comando de atribuição de valor."""
    id, op, expr, _ = root.children
    expr = f_expr(expr)
    return Node(op.name, children=[id, expr])


def f_conditional(root: Node) -> Node:
    """Processa o comando condicional (SE)."""
    if_, expr, _, cmds, else_, _, _ = root.children
    expr, cmds, else_ = f_expr(expr), f_commands(cmds), f_else(else_)
    if else_:
        return Node(if_.name, children=flatten([expr, cmds, else_]))
    return Node(if_.name, children=flatten([expr, cmds]))


def f_else(root: Node) -> Node:
    """Processa o comando ELSE (SENÃO) do comando condicional (SE)."""
    if is_empty(root):
        return None
    else_, cmds = root.children
    cmds = f_commands(cmds)
    return Node(else_.name, children=flatten(cmds))


def f_loop(root: Node) -> Node:
    """Processa um comando de loop (REPETIR ou ENQUANTO)."""
    child = root.children[0]
    _op, expr, _, cmds, _, _ = child.children
    return Node(_op.name, children=flatten([f_expr(expr), f_commands(cmds)]))


def f_generic_command(root: Node) -> Node:
    """Processa um comando qualquer que seja de:
    movimento, controle de caneta ou controle de tela.
    """
    if len(root.children) == 2:
        cmd, _ = root.children
        return Node(cmd.name)
    if len(root.children) == 3:
        cmd, expr, _ = root.children
        return Node(cmd.name, children=[f_expr(expr)])
    cmd, expr1, expr2, _ = root.children
    return Node(cmd.name, children=[f_expr(expr1), f_expr(expr2)])


def f_expr(root: Node) -> Node:
    """Processa uma expressão, despachando para a função apropriada."""
    or_expr = root.children[0]
    return f_or_expr(or_expr)


def f_or_expr(root: Node) -> Node:
    """Processa uma expressão lógica OR."""
    and_expr, or_expr_tail = root.children
    and_expr, or_expr_tail = f_and_expr(and_expr), f_or_expr_tail(or_expr_tail)
    if or_expr_tail is None:
        return and_expr
    op, right = or_expr_tail
    return Node(op.name, children=[and_expr, right])


def f_or_expr_tail(root: Node) -> tuple[Node, Node] | None:
    """Processa a parte final de uma expressão lógica OR."""
    if is_empty(root):
        return None
    op1, and_expr, or_expr_tail = root.children
    and_expr, or_expr_tail = f_and_expr(and_expr), f_or_expr_tail(or_expr_tail)
    if or_expr_tail is None:
        return op1, and_expr
    op2, right = or_expr_tail
    return op1, Node(op2.name, children=[and_expr, right])


def f_and_expr(root: Node) -> Node:
    """Processa uma expressão lógica AND."""
    not_expr, and_expr_tail = root.children
    not_expr, and_expr_tail = f_not_expr(not_expr), f_and_expr_tail(and_expr_tail)
    if and_expr_tail is None:
        return not_expr
    op, right = and_expr_tail
    return Node(op.name, children=[not_expr, right])


def f_and_expr_tail(root: Node) -> tuple[Node, Node] | None:
    """Processa a parte final de uma expressão lógica AND."""
    if is_empty(root):
        return None
    op, not_expr, and_expr_tail = root.children
    not_expr, and_expr_tail = f_not_expr(not_expr), f_and_expr_tail(and_expr_tail)
    if and_expr_tail is None:
        return op, not_expr
    op2, right = and_expr_tail
    return op, Node(op2.name, children=[not_expr, right])


def f_not_expr(root: Node) -> Node:
    """Processa uma expressão lógica NOT."""
    if len(root.children) == 1:
        return f_add_expr(root.children[0])
    op, not_expr = root.children
    return Node(op.name, children=[f_not_expr(not_expr)])


def f_add_expr(root: Node) -> Node:
    """Processa uma expressão de adição."""
    mul_expr, add_expr_tail = root.children
    mul_expr, add_expr_tail = f_mul_expr(mul_expr), f_add_expr_tail(add_expr_tail)
    if add_expr_tail is None:
        return mul_expr
    op, right = add_expr_tail
    return Node(op.name, children=[mul_expr, right])


def f_add_expr_tail(root: Node) -> tuple[Node, Node] | None:
    """Processa a parte final de uma expressão de adição."""
    if is_empty(root):
        return None
    op, mul_expr, add_expr_tail = root.children
    mul_expr, add_expr_tail = f_mul_expr(mul_expr), f_add_expr_tail(add_expr_tail)
    if add_expr_tail is None:
        return op, mul_expr
    op2, right = add_expr_tail
    return op, Node(op2.name, children=[mul_expr, right])


def f_mul_expr(root: Node) -> Node:
    """Processa uma expressão de multiplicação."""
    primary, mul_expr_tail = root.children
    primary, mul_expr_tail = f_primary(primary), f_mul_expr_tail(mul_expr_tail)
    if mul_expr_tail is None:
        return primary
    op, right = mul_expr_tail
    return Node(op.name, children=[primary, right])


def f_mul_expr_tail(root: Node) -> tuple[Node, Node] | None:
    """Processa a parte final de uma expressão de multiplicação."""
    if is_empty(root):
        return None
    op, primary, mul_expr_tail = root.children
    primary, mul_expr_tail = f_primary(primary), f_mul_expr_tail(mul_expr_tail)
    if mul_expr_tail is None:
        return op, primary
    op2, right = mul_expr_tail
    return op, Node(op2.name, children=[primary, right])


def f_primary(root: Node) -> Node:
    """Processa um elemento primário de uma expressão."""
    if len(root.children) == 1:
        return Node(name=root.children[0].name)
    _, expr, _ = root.children
    return f_expr(expr)


if __name__ == "__main__":
    script_samples = []
    # INPUT 1
    script_samples.append(
        """
    inicio
        // Desenha as quatro arestas do quadrado
        avancar 150;
        girar_direita 90;
        avancar 150;
        girar_direita 90;
        avancar 150;
        girar_direita 90;
        avancar 150;
        girar_direita 90;
    fim
    """
    )

    # INPUT 2
    script_samples.append(
        """
    inicio
        var inteiro : tamanho_lado ;
        tamanho_lado = 200;

        // Desenha uma estrela de 5 pontas
        avancar tamanho_lado ;
        girar_direita 144;

        avancar tamanho_lado ;
        girar_direita 144;

        avancar tamanho_lado ;
        girar_direita 144;

        avancar tamanho_lado ;
        girar_direita 144;

        avancar tamanho_lado ;
        girar_direita 144;
    fim
    """
    )

    # INPUT 3
    script_samples.append(
        """
    inicio
        var inteiro : lado ;
        var texto : cor ;

        lado = 5;
        cor_de_fundo "black";
        definir_espessura 2;

        repita 50 vezes
            // Muda a cor da linha a cada iteracao
            definir_cor "cyan";

            // Desenha e aumenta o lado
            avancar lado ;
            girar_direita 90;
            lado = lado + 5;
        fim_repita;
    fim
    """
    )
    # Tabela LL(1)
    ll1_table = LL1Table(grammar=grammar)
    # Parser LL(1)
    parser = LL1ParserTable(table=ll1_table, start_symbol=grammar.start_symbol)

    for script_input in script_samples:
        print(Fore.YELLOW + "=" * 50 + Fore.RESET)
        # Tokenização
        tokens = Tokenizer.tokenize(script_input, grammar=grammar)
        # Parsing
        parsed, derivation_tree_root = parser.parse(tokens)
        if not parsed:
            print(Fore.RED + "Erro na análise sintática." + Fore.RESET)
            continue
        else:
            print(Fore.GREEN + "Análise sintática bem-sucedida!" + Fore.RESET)
        print("AST:")
        ast_root = get_ast_root(derivation_tree_root)
        for pre, fill, node in RenderTree(ast_root):
            print(
                f"{pre}"
                + {True: Fore.BLUE, False: Fore.BLACK}[isinstance(node.name, Token)]
                + f"{node.name.lexeme if isinstance(node.name, Token) else node.name}"
                + Fore.RESET
            )
