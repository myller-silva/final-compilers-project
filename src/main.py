from constants import *
from utils import print_grammar, print_tree_nice

from anytree import RenderTree
from tokenizer import Tokenizer
from parser import RecursiveDescentParser
from semantic import SemanticAnalyzer

from utils.grammar import grammar

print("-- Gramática --")
print_grammar(grammar)

word = """
inicio 

    //var inteiro: a, b, c;
    a = 10;
    avancar 10;

fim

"""

# print(word.strip())
print("\n-- Tokens de Entrada --")
tokens = Tokenizer(word).tokenize()
print(" ".join([f"{token[1]}" for token in tokens]))

print("\n-- Análise Sintática --")
parser = RecursiveDescentParser(grammar, "Programa")
abstract_syntax_tree = parser.parse(tokens)
# for pre, fill, node in RenderTree(abstract_syntax_tree):
#     print(f"{pre}{node.name}")
print_tree_nice(abstract_syntax_tree)

# print("\n-- Análise Semântica --")
# # from semantic import AnalisadorSemantico
# erros = SemanticAnalyzer(abstract_syntax_tree).analyze()
# print("Erros encontrados:" if erros else "Nenhum erro encontrado.")
# for erro in erros:
#     print("-", erro)

# print(abstract_syntax_tree)
