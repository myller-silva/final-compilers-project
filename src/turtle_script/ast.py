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
from itertools import chain


def is_empty(node: Node) -> bool:
    """Check if a node is empty (has no children or is epsilon)."""
    return len(node.children) == 0 or node.children[0] == Grammar.EPSILON


def flatten(items):
    """Achata uma lista de itens, processando apenas os elementos que são listas."""
    from itertools import chain

    return list(
        chain.from_iterable(
            item if isinstance(item, list) else [item] for item in items
        )
    )


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

    root.children = children
    return root


def f_declaracoes(root: Node) -> Node:
    """Process declarations in the program."""
    if is_empty(root):
        return None
    declaracaovariavel, declaracoes = root.children
    declaracaovariavel = f_declaracao_variavel(declaracaovariavel)
    declaracoes = f_declaracoes(declaracoes)
    children = []
    if declaracaovariavel:
        children.append(declaracaovariavel)
    if declaracoes:
        children.append(declaracoes)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return children[0]
    root.children = children
    return root


def f_declaracao_variavel(root: Node) -> Node:
    _, tipo, atribuir_variavel, _ = root.children

    atribuir_variavel = f_atribuir_variavel(atribuir_variavel)
    children = [tipo]
    if atribuir_variavel:
        children.append(atribuir_variavel)

    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return children[0]
    root.children = children
    return root


def f_atribuir_variavel(root: Node) -> Node:
    # TODO: Retornar lista? de identificadores e expressoes?
    _, identificadores, atribuicaoidentificadores = root.children
    identificadores = f_identificadores(identificadores)
    atribuicaoidentificadores = f_atribuicao_identificadores(atribuicaoidentificadores)
    children = []
    if identificadores:
        children.append(identificadores)
    if atribuicaoidentificadores:
        children.append(atribuicaoidentificadores)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return children[0]
    root.children = children
    return root


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
    # retornar lista de expressões
    # TODO
    if is_empty(root):
        return []
    _, expr, aiR = root.children
    expr = f_expr(expr)
    aiR = f_atribuicao_identificadoresR(aiR)
    if not aiR:
        return [expr]
    return [expr] + aiR


def f_atribuicao_identificadoresR(root: Node) -> Node:
    # TODO
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
        return child  # Placeholder for unknown command processing


def f_atribuir_valor(root: Node) -> Node:
    """Process an assignment command."""
    id, op, expr, _ = root.children
    expr = f_expr(expr)
    return Node(op.name, children=[id, expr])
    # return root  # Placeholder for assignment command processing


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
    return Node(
        se.name,
        children=children,
    )


def f_senao(root: Node) -> Node:
    if is_empty(root):
        return None
    senao, cmds = root.children
    cmds = f_comandos(cmds)
    return Node(
        senao.name,
        children=flatten(cmds) if cmds else [],
    )


def f_laco_repeticao(root: Node) -> Node:
    # TODO IMPLEMENTAR
    """Process a loop command."""
    return root  # Placeholder for loop command processing


def f_movimento(root: Node) -> Node:
    # TODO IMPLEMENTAR
    """Process a movement command."""
    return root  # Placeholder for movement command processing


def f_controle_caneta(root: Node) -> Node:
    # TODO IMPLEMENTAR
    """Process a pen control command."""
    return root  # Placeholder for pen control command processing


def f_controle_tela(root: Node) -> Node:
    # TODO IMPLEMENTAR
    """Process a screen control command."""
    return root  # Placeholder for screen control command processing


def f_expr(root: Node) -> Node:
    or_expr = root.children[0]
    return f_or_expr(or_expr)


def f_or_expr(root: Node) -> Node:
    and_expr, or_expr_tail = root.children
    and_expr = f_and_expr(and_expr)
    or_expr_tail = f_or_expr_tail(or_expr_tail)
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
    root.children = children
    return root


def f_and_expr(root: Node) -> Node:
    not_expr, and_expr_tail = root.children
    not_expr = f_not_expr(not_expr)
    and_expr_tail = f_and_expr_tail(and_expr_tail)
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
    root.children = children
    return root


def f_not_expr(root: Node) -> Node:
    # pass
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
    root.children = children
    # root.name = op_mais # TODO: VERIFICAR SE TEM QUE VIR DO FILHO OU DAQUI MESMO
    return root


def f_add_expr_tail(root: Node) -> Node:
    # TODO: FUNÇÃO PROVAVELMENTE ERRADA: O OPERADOR DEVE IR PARA O PAI DELE?
    if is_empty(root):
        return None
    op, mul_expr, add_expr_tail = root.children
    mul_expr = f_mul_expr(mul_expr)
    add_expr_tail = f_add_expr_tail(add_expr_tail)
    children = [mul_expr]
    if add_expr_tail:
        children.append(add_expr_tail)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return children[0]
    root.children = children
    # root.name = op.name  # Update the node name to the operator
    return root


def f_mul_expr(root: Node) -> Node:
    primary, mul_expr_tail = root.children
    primary = f_primary(primary)
    mul_expr_tail = f_mul_expr_tail(mul_expr_tail)
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
    root.children = children
    return root


def f_primary(root: Node) -> Node:
    # TODO: melhorar para lidar com o valor do primário
    # return Node(name=root.children[0].name)
    if len(root.children) == 1:
        # Se for um único filho, é um primário simples
        return Node(name=root.children[0].name)
    _, expr, _ = root.children
    expr = f_expr(expr)
    return expr


def f_mul_expr_tail(root: Node) -> Node:
    # TODO: RETORNAR COM O OPERADOR NO PAI DELE? PARA FACILITAR QUE O PAI TENHA O OPERADOR NA RAIZ?
    # return root
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
        return children[0]
    # root.name = op.name  # Update the node name to the operator
    # print("op.name:", op.name)
    root.children = children
    return root


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
        return children[0]
    
    root.children = children
    # root.name = op.name  # Update the node name to the operator
    return root


def f_and_expr_tail(root: Node) -> Node:
    if is_empty(root):
        return None
    _, mulexpr, and_expr_tail = root.children
    mulexpr = f_expr(mulexpr)
    and_expr_tail = f_and_expr_tail(and_expr_tail)
    children = [mulexpr]
    if and_expr_tail:
        children.append(and_expr_tail)
    children = flatten(children)
    if len(children) == 0:
        return None
    if len(children) == 1:
        return children[0]
    root.children = children


# Exemplo de texto para análise
text = """
inicio
    se verdadeiro entao
        a = 1; 
    //senao
        a = 2*(2+(4)-4/1);
    fim_se;
fim
"""
# Tabela LL(1)
ll1_table = LL1Table(grammar=grammar)

# Parser LL(1)
parser = LL1ParserTable(table=ll1_table, start_symbol=grammar.start_symbol)

# Tokenização
tokens = Tokenizer.tokenize(text, grammar=grammar)

# Derivação
parsed, derivation_prods = parser.parse(tokens)
print(
    {
        True: Fore.GREEN + "Análise sintática bem-sucedida!" + Fore.RESET,
        False: Fore.RED + "Erro na análise sintática." + Fore.RESET,
    }[parsed]
)

print(Fore.YELLOW + "Produções utilizadas na derivação:" + Fore.RESET)
for prod in derivation_prods:
    print(prod)

derivation_tree_root = parser.build_derivation_tree(derivation_prods)

for pre, fill, node in RenderTree(derivation_tree_root):
    print(
        f"{pre}"
        + {
            True: Fore.YELLOW + f"{node.name}" + Fore.RESET,
            False: Fore.BLACK + f"{node.name}" + Fore.RESET,
        }[isinstance(node.name, Terminal)]
    )

print("Árvore sintática abstrata:")
#FAZER UMA COPIA ANTES DE CHAMAR A FUNÇÃO PARA NÃO MUDAR A ARVORE DE DERIVAÇÃO
derivation_tree_root = derivation_tree_root 
ast_root = f_programa(derivation_tree_root)
for pre, fill, node in RenderTree(ast_root):
    print(
        f"{pre}"
        + {
            True: Fore.BLUE + f"{node.name}" + Fore.RESET,
            False: Fore.BLACK + f"{node.name}" + Fore.RESET,
        }[isinstance(node.name, Terminal)]
    )


# print("Árvore de derivacao novamente:")
# # ast_root = f_programa(derivation_tree_root)
# for pre, fill, node in RenderTree(derivation_tree_root):
#     print(
#         f"{pre}"
#         + {
#             True: Fore.YELLOW + f"{node.name}" + Fore.RESET,
#             False: Fore.BLACK + f"{node.name}" + Fore.RESET,
#         }[isinstance(node.name, Terminal)]
#     )
