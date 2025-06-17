from utils.grammar import grammar
from utils.text import custom_print
from utils import print_grammar
from utils import print_anytree

from tokenizer import Tokenizer
from parser import RecursiveDescentParser
from constants import PONTO_VIRGULA, KW_INICIO_BLOCO, KW_FIM_BLOCO


# GRAMATICA
custom_print(" Gramatica ", border_char="*")
print_grammar(grammar)


# LEXICAL ANALYSIS
input_text = """
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
tokens = Tokenizer(input_text).tokenize()
custom_print(" Tokens ", border_char="*")
for token in tokens:
    print(token)


# SYNTAX ANALYSIS

# parser = RecursiveDescentParser(grammar=grammar, start_symbol="Programa")
parser = RecursiveDescentParser(grammar, "Programa")

derivation_tree = parser.parse(tokens)
custom_print(" Derivation Tree ", border_char="*")
print_anytree(derivation_tree)


# # # AST
# # # TODO: externalizar a função de transformação para ser mais genérica
# def flatten_list_transform(symbol_list):
#     """
#     Flattens nested lists of AST nodes for a given list symbol.
#     """

#     def transform(children, derivation_to_ast, ignore, transforms):
#         items = []
#         for child in children:
#             ast = derivation_to_ast(child, ignore, transforms)
#             if ast is None:
#                 continue
#             if isinstance(ast, tuple) and ast[0] == symbol_list:
#                 items.extend(ast[1])
#             else:
#                 items.append(ast)
#         return (symbol_list, items)

#     return transform


# Alias in Portuguese for compatibility
# transformar_lista_aplanada = flatten_list_transform


custom_print(" Abstract Syntax Tree ", border_char="*")

flattening_transforms = {
    # "Comandos": transformar_lista_aplanada("Comandos"),
    # "DeclaracaoVariavel": flatten_list_transform("DeclaracaoVariavel"),
    # "Expressao": flatten_list_transform("Expressao"),
    # "ExpressaoR": flatten_list_transform("ExpressaoR"),
    "Comandos": parser.flatten_children("Comandos"),
}

abstract_syntax_tree = parser.to_abstract_syntax_tree(
    derivation_tree,
    flattening_transforms=flattening_transforms,
    ignore={PONTO_VIRGULA, KW_INICIO_BLOCO, KW_FIM_BLOCO},
)
# print(abstract_syntax_tree)
print_anytree(abstract_syntax_tree)
# abstract_syntax_tree = derivacao_para_ast(
#     arvore_de_derivacao,
#     ignorar={PONTO_VIRGULA, KW_INICIO_BLOCO, KW_FIM_BLOCO},
#     transformar=transformar,
# )
# print_tree_nice(abstract_syntax_tree)
