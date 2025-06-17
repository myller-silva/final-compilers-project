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
parser = RecursiveDescentParser(grammar, "Programa")
derivation_tree = parser.parse(tokens)
custom_print(" Derivation Tree ", border_char="*")
print_anytree(derivation_tree)

custom_print(" Abstract Syntax Tree ", border_char="*")
to_flatten = ["Comandos", "DeclaracaoVariavel", "Expressao", "ExpressaoR"]
flattening_transforms = { key : parser.flatten_children_anytree(key) for key in to_flatten }
abstract_syntax_tree = parser.to_abstract_syntax_tree(
    derivation_tree,
    flattening_transforms=flattening_transforms,
    ignored_terms={PONTO_VIRGULA, KW_INICIO_BLOCO, KW_FIM_BLOCO},
)
print_anytree(abstract_syntax_tree)

# SEMANTIC ANALYSIS
