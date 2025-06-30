#!/usr/bin/env python3
"""
Teste do gerador de código Python a partir da AST da linguagem Turtle Script.
"""

from colorama import Fore
from anytree import RenderTree
from grammar import grammar
from table_parser_ll1 import LL1Table, LL1ParserTable, Token, Tokenizer
from abstract_syntax_tree import get_ast_root
from generator import Generator
import os
import sys

# Adiciona o diretório src ao caminho para importar os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

output_path = "outputs"

if __name__ == "__main__":
    print(Fore.CYAN + "Testador do Gerador de Código Python" + Fore.RESET)
    print()

    # Carrega os arquivos de entrada
    input_files = [
        "./inputs/entrada1.txt",
        "./inputs/entrada2.txt",
        "./inputs/entrada3.txt",
    ]

    # Tabela LL(1)
    ll1_table = LL1Table(grammar=grammar)
    # Parser LL(1)
    parser = LL1ParserTable(table=ll1_table, start_symbol=grammar.start_symbol)
    # Gerador
    generator = Generator()

    for i, input_file in enumerate(input_files, 1):
        print(Fore.YELLOW + "=" * 60 + Fore.RESET)
        print(Fore.CYAN + f"Testando entrada {i}: {input_file}" + Fore.RESET)
        print(Fore.YELLOW + "=" * 60 + Fore.RESET)

        try:
            # Lê o arquivo de entrada
            with open(input_file, "r", encoding="utf-8") as f:
                script_input = f.read()

            print(Fore.BLUE + "Código fonte original:" + Fore.RESET)
            print(script_input)
            print("-" * 40)

            # Tokenização
            tokens = Tokenizer.tokenize(script_input, grammar=grammar)

            # Parsing
            parsed, derivation_tree_root = parser.parse(tokens)

            if not parsed:
                print(Fore.RED + "Erro na análise sintática." + Fore.RESET)
                continue
            else:
                print(Fore.GREEN + "Análise sintática bem-sucedida!" + Fore.RESET)

            # Gera AST
            ast_root = get_ast_root(derivation_tree_root)

            print(Fore.MAGENTA + "AST gerada:" + Fore.RESET)
            for pre, fill, node in RenderTree(ast_root):
                if isinstance(node.name, Token):
                    print(
                        f"{pre}{Fore.YELLOW}{node.name.lexeme} "
                        + Fore.BLACK
                        + f"({node.name.terminal})"
                        + Fore.RESET
                    )
                else:
                    print(f"{pre}{node.name}")

            print("-" * 40)

            # Gera código Python
            python_code = generator.generate(ast_root, f"Resultado-Exemplo {i}")

            print(Fore.GREEN + "Código Python gerado:" + Fore.RESET)
            print(python_code)

            # Salva o código gerado
            output_file = f"{output_path}/gerado_{i}.py"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(python_code)

            print(Fore.CYAN + f"Código salvo em: {output_file}" + Fore.RESET)

        except FileNotFoundError:
            print(Fore.RED + f"Arquivo não encontrado: {input_file}" + Fore.RESET)
        except Exception as e:
            print(Fore.RED + f"Erro durante o processamento: {e}" + Fore.RESET)

        print()
