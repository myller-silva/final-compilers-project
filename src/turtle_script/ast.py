from grammar import *
from table_parser_ll1 import (
    LL1Table,
    LL1ParserTable,
    Tokenizer,
    Production,
    Terminal,
    NonTerminal,
)
from colorama import Fore
from anytree import RenderTree, Node, PreOrderIter
from copy import deepcopy
from itertools import chain


def is_empty(node: Node) -> bool:
    """Check if a node is empty (has no children or is epsilon)."""
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


def f_programa(root: Node) -> Node:
    _, declaracoes, comandos, _ = root.children
    declaracoes = f_declaracoes(declaracoes)
    comandos = f_comandos(comandos)
    children = []
    if declaracoes:
        children.append(declaracoes)
    if comandos:
        children.append(comandos)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return children[0]
    return Node(root.name, children=children)


def f_declaracoes(root: Node) -> list:
    if is_empty(root):
        return None
    d_variavel, ds = root.children
    d_variavel = f_declaracao_variavel(d_variavel)
    ds = f_declaracoes(ds)
    if not ds:
        return [d_variavel]
    return [d_variavel] + [ds]


def f_declaracao_variavel(root: Node) -> Node:
    _, tipo, atribuir_variavel, _ = root.children
    tipo = f_tipo(tipo)
    atribuir_variavel = f_atribuir_variavel(atribuir_variavel)
    op_att, children_att = atribuir_variavel
    return Node(op_att.name, children=[tipo] + children_att)


def f_tipo(root: Node) -> Node:
    """Process the type of a variable."""
    kw = root.children[0]
    return Node(kw.name)


def f_atribuir_variavel(root: Node) -> Node:
    op_att, identificadores, atribuicaoidentificadores = root.children
    identificadores = f_identificadores(identificadores)
    atribuicaoidentificadores = f_atribuicao_identificadores(atribuicaoidentificadores)
    children = [identificadores, atribuicaoidentificadores]
    children = flatten(children)
    return op_att, children


def f_identificadores(root: Node) -> list:
    """Retorna lista de identificadores."""
    id, idR = root.children
    idR = f_identificadoresR(idR)
    if not idR:
        return [id]
    return [id] + idR


def f_identificadoresR(root: Node) -> list:
    """Retorna lista de identificadores adicionais."""
    if is_empty(root):
        return []
    _, id, idR = root.children
    idR = f_identificadoresR(idR)
    if not idR:
        return [id]
    return [id] + idR


def f_atribuicao_identificadores(root: Node) -> list:
    if is_empty(root):
        return []
    _, expr, aiR = root.children
    expr = f_expr(expr)
    aiR = f_atribuicao_identificadoresR(aiR)
    if not aiR:
        return [expr]
    return [expr] + aiR


def f_atribuicao_identificadoresR(root: Node) -> Node:
    if is_empty(root):
        return []
    _, expr, aiR = root.children
    expr = f_expr(expr)
    aiR = f_atribuicao_identificadoresR(aiR)
    if not aiR:
        return [expr]
    return [expr] + aiR


def f_comandos(root: Node) -> list:
    """Process commands in the program."""
    if is_empty(root):
        return []
    cmd, cmds = root.children
    cmd = f_comando(cmd)
    cmds = f_comandos(cmds)
    if not cmds:
        return [cmd]
    return [cmd] + cmds


def f_comando(root: Node) -> Node:
    child = root.children[0]
    if child.name == AtribuirValor:
        return f_atribuir_valor(child)
    elif child.name == Condicional:
        return f_condicional(child)
    elif child.name == LacoRepeticao:
        return f_laco_repeticao(child)
    elif child.name == Movimento:
        return f_movimento(child)
    elif child.name == ControleCaneta:
        return f_controle_caneta(child)
    elif child.name == ControleTela:
        return f_controle_tela(child)
    else:
        return child


def f_atribuir_valor(root: Node) -> Node:
    """Process an assignment command."""
    id, op, expr, _ = root.children
    expr = f_expr(expr)
    return Node(op.name, children=[id, expr])


def f_condicional(root: Node) -> Node:
    """Process a conditional command."""
    se, expr, _, cmds, senao, _, _ = root.children
    expr = f_expr(expr)
    cmds = f_comandos(cmds)
    senao = f_senao(senao)
    children = [expr, cmds]
    if senao:
        children.append(senao)
    children = flatten(children)
    return Node(se.name, children=children)


def f_senao(root: Node) -> Node:
    if is_empty(root):
        return None
    senao, cmds = root.children
    cmds = f_comandos(cmds)
    cmds = flatten(cmds)
    return Node(senao.name, children=cmds)


def f_laco_repeticao(root: Node) -> Node:
    """Process a loop command."""
    child = root.children[0]
    if child.name in [Repita, Enquanto]:
        _, expr, _, cmds, _, _ = child.children
        expr = f_expr(expr)
        cmds = f_comandos(cmds)
        children = [expr, cmds]
        children = flatten(children)
        return Node(child.name, children=children)
    return child


def f_movimento(root: Node) -> Node:
    """Process a movement command."""
    if len(root.children) == 4:
        cmd, expr1, expr2, _ = root.children
        expr1 = f_expr(expr1)
        expr2 = f_expr(expr2)
        return Node(cmd.name, children=[expr1, expr2])
    cmd, expr, _ = root.children
    return Node(cmd.name, children=[f_expr(expr)])


def f_controle_caneta(root: Node) -> Node:
    """Process a pen control command."""
    if len(root.children) == 2:
        cmd, _ = root.children
        return Node(cmd.name)
    cmd, expr, _ = root.children
    expr = f_expr(expr)
    return Node(cmd.name, children=[expr])


def f_controle_tela(root: Node) -> Node:
    """Process a screen control command."""
    if len(root.children) == 2:
        cmd, _ = root.children
        return Node(cmd.name)
    cmd, expr, _ = root.children
    expr = f_expr(expr)
    return Node(cmd.name, children=[expr])


def f_expr(root: Node) -> Node:
    or_expr = root.children[0]
    return f_or_expr(or_expr)


def f_or_expr(root: Node) -> Node:
    and_expr, or_expr_tail = root.children
    and_expr = f_and_expr(and_expr)
    or_expr_tail = f_or_expr_tail(or_expr_tail)
    if isinstance(or_expr_tail, tuple):
        op, right = or_expr_tail
        return Node(op.name, children=[and_expr, right])
    children = []
    if and_expr:
        children.append(and_expr)
    if or_expr_tail:
        children.append(or_expr_tail)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return children[0]
    return Node(root.name, children=children)


def f_and_expr(root: Node) -> Node:
    not_expr, and_expr_tail = root.children
    not_expr = f_not_expr(not_expr)
    and_expr_tail = f_and_expr_tail(and_expr_tail)
    if isinstance(and_expr_tail, tuple):
        op, right = and_expr_tail
        return Node(op.name, children=[not_expr, right])
    children = []
    if not_expr:
        children.append(not_expr)
    if and_expr_tail:
        children.append(and_expr_tail)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return children[0]
    return Node(root.name, children=children)


def f_and_expr_tail(root: Node) -> Node:
    if is_empty(root):
        return None
    op, mulexpr, and_expr_tail = root.children
    mulexpr = f_expr(mulexpr)
    and_expr_tail = f_and_expr_tail(and_expr_tail)
    children = [mulexpr]
    if and_expr_tail:
        children.append(and_expr_tail)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return op, children[0]
    return op, Node(root.name, children=children)


def f_not_expr(root: Node) -> Node:
    if len(root.children) == 1:
        add_expr = root.children[0]
        return f_add_expr(add_expr)

    op, not_expr = root.children
    not_expr = f_not_expr(not_expr)
    return Node(op.name, children=[not_expr])


def f_add_expr(root: Node) -> Node:
    mul_expr, add_expr_tail = root.children
    mul_expr = f_mul_expr(mul_expr)
    add_expr_tail = f_add_expr_tail(add_expr_tail)
    if isinstance(add_expr_tail, tuple):
        op, right = add_expr_tail
        return Node(op.name, children=[mul_expr, right])
    children = []
    if mul_expr:
        children.append(mul_expr)
    if add_expr_tail:
        children.append(add_expr_tail)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return children[0]
    return Node(root.name, children=children)


def f_add_expr_tail(root: Node) -> Node:
    if is_empty(root):
        return None
    op, mul_expr, add_expr_tail = root.children
    mul_expr = f_mul_expr(mul_expr)
    add_expr_tail = f_add_expr_tail(add_expr_tail)
    if isinstance(add_expr_tail, tuple):
        op2, add_expr_tail = add_expr_tail
        return op, Node(op2.name, children=[mul_expr, add_expr_tail])
    children = []
    if mul_expr:
        children.append(mul_expr)
    if add_expr_tail:
        children.append(add_expr_tail)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return op, children[0]
    return op, Node(root.name, children=children)


def f_mul_expr(root: Node) -> Node:
    primary, mul_expr_tail = root.children
    primary = f_primary(primary)
    mul_expr_tail = f_mul_expr_tail(mul_expr_tail)
    if isinstance(mul_expr_tail, tuple):
        op, right = mul_expr_tail
        return Node(op.name, children=[primary, right])
    children = []
    if primary:
        children.append(primary)
    if mul_expr_tail:
        children.append(mul_expr_tail)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return children[0]
    return Node(root.name, children=children)


def f_mul_expr_tail(root: Node) -> Node:
    if is_empty(root):
        return None
    op, primary, mul_expr_tail = root.children
    primary = f_primary(primary)
    mul_expr_tail = f_mul_expr_tail(mul_expr_tail)
    children = [primary]
    if mul_expr_tail:
        children.append(mul_expr_tail)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return op, children[0]
    return op, Node(root.name, children=children)


def f_primary(root: Node) -> Node:
    if len(root.children) == 1:
        # Se for um único filho, é um primário simples
        return Node(name=root.children[0].name)
    _, expr, _ = root.children
    expr = f_expr(expr)
    return expr


def f_or_expr_tail(root: Node) -> Node:
    if is_empty(root):
        return None
    op, expr, or_expr_tail = root.children
    expr = f_expr(expr)
    or_expr_tail = f_or_expr_tail(or_expr_tail)
    children = [expr]
    if or_expr_tail:
        children.append(or_expr_tail)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return op, children[0]

    return op, Node(root.name, children=children)


# Exemplo de texto para análise
# TODO: ERROR: girar_direita 90 + 1  + 0010 - 12 * 7 / 0;
# text = """
# inicio
#     // Desenha as quatro arestas do quadrado
#     avancar 150;
#     girar_direita 90;
#     avancar 150;
#     girar_direita 90;
#     avancar 150;
#     girar_direita 90;
#     avancar 150;
#     girar_direita 90;
# fim
# """

# text = """
# inicio
#     var inteiro : tamanho_lado ;
#     tamanho_lado = 200;

#     // Desenha uma estrela de 5 pontas
#     avancar tamanho_lado ;
#     girar_direita 144;

#     avancar tamanho_lado ;
#     girar_direita 144;

#     avancar tamanho_lado ;
#     girar_direita 144;

#     avancar tamanho_lado ;
#     girar_direita 144;

#     avancar tamanho_lado ;
#     girar_direita 144;
# fim
# """

text = """
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

# Tabela LL(1)
ll1_table = LL1Table(grammar=grammar)

# Parser LL(1)
parser = LL1ParserTable(table=ll1_table, start_symbol=grammar.start_symbol)

# Tokenização
tokens = Tokenizer.tokenize(text, grammar=grammar)

# Derivação
parsed, derivation_tree_root = parser.parse(tokens)
root_copy = deepcopy(derivation_tree_root)

# print("ÁRVORE DE DERIVAÇÃO(antes):")
# for pre, fill, node in RenderTree(derivation_tree_root):
#     print(
#         f"{pre}"
#         + {
#             True: Fore.YELLOW + f"{node.name}" + Fore.RESET,
#             False: Fore.BLACK + f"{node.name}" + Fore.RESET,
#         }[node.is_leaf]
#     )

print(
    {
        True: Fore.GREEN + "Análise sintática bem-sucedida!" + Fore.RESET,
        False: Fore.RED + "Erro na análise sintática." + Fore.RESET,
    }[parsed]
)

print("Árvore sintática abstrata:")
root_copy = deepcopy(derivation_tree_root)
ast_root = f_programa(derivation_tree_root)
for pre, fill, node in RenderTree(ast_root):
    print(
        f"{pre}"
        + {
            True: Fore.BLUE + f"{node.name}" + Fore.RESET,
            False: Fore.BLACK + f"{node.name}" + Fore.RESET,
        }[node.is_leaf]
    )


# print("ÁRVORE DE DERIVAÇÃO(depois):")
# for pre, fill, node in RenderTree(derivation_tree_root):
#     print(
#         f"{pre}"
#         + {
#             True: Fore.YELLOW + f"{node.name}" + Fore.RESET,
#             False: Fore.BLACK + f"{node.name}" + Fore.RESET,
#         }[node.is_leaf]
#     )

# # veriicar se a arvore de derivacao após as operacoes é igual a arvore de derivacao que foi copiada antes
# def are_trees_equal(node1: Node, node2: Node) -> bool:
#     """Compara se duas árvores são iguais em termos de estrutura e conteúdo."""
#     if node1.name != node2.name:
#         return False
#     if len(node1.children) != len(node2.children):

#         print(Fore.RED + f"Node {node1.name} children: {[child.name for child in node1.children]}" + Fore.RESET)
#         print(Fore.RED + f"Node {node2.name} children: {[child.name for child in node2.children]}" + Fore.RESET)
#         print()
#         return False
#     return all(are_trees_equal(c1, c2) for c1, c2 in zip(node1.children, node2.children))

# # Substituir a comparação atual pela nova função
# if are_trees_equal(derivation_tree_root, root_copy):
#     print(
#         Fore.GREEN
#         + "A árvore de derivação não foi alterada após as operações."
#         + Fore.RESET
#     )
# else:
#     print(
#         Fore.RED + "A árvore de derivação foi alterada após as operações." + Fore.RESET
#     )
