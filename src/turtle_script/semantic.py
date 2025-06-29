from colorama import Fore
from anytree import RenderTree
from anytree import Node
from grammar import *
from table_parser_ll1 import LL1Table, LL1ParserTable, Token, Tokenizer
from abstract_syntax_tree import get_ast_root


class SemanticProcessor:
    """Classe responsável por processar semanticamente o código fonte."""

    def __init__(self, grammar: Grammar, symbol_table: dict):
        self.grammar = grammar
        self.symbol_table = symbol_table

    def process(self, ast: Node) -> bool:
        """Processa a ast fornecida, realizando a análise semântica."""

        errors = []
        variable_declaration_errors = self._validate_declaration(ast, self.symbol_table)
        if variable_declaration_errors:
            errors.append({"Erros de declaração de variável": variable_declaration_errors})

        errors_types = self._validate_types(ast)
        if errors_types:
            errors.append({"Erros de tipos": errors_types})

        return errors
    
    def _validate_declaration(self, ast: Node, symbol_table: dict) -> list:
        """
        Verificação de Declaração de Variáveis
        
        A Tabela de Símbolos armazenará todas as variáveis declaradas, juntamente com seus tipos.
        
        Uso antes da declaração: Para cada variável encontrada em uma expressão ou atribuição, o analisador deve verificar se ela existe na Tabela de Símbolos. Caso contrário, um erro de "variável não declarada"deve ser reportado.
        
        Redeclaração de variável: Ao processar uma declaração, o analisador deve verificar se a variável já existe na Tabela de Símbolos. Se existir, um erro de "variável já declarada" deve ser emitido.
        """
        errors = []
        declaration_nodes = [node for node in ast.descendants if self.is_declaration(node)]
        # ERROS DE DECLARAÇÃO DE VARIÁVEIS
        for node in declaration_nodes:
            var_type_node, right = node.children[0], node.children[1:]
            index_of_op_att = self.index_of(right, op_atribuicao)
            if index_of_op_att < 0: # não tem atribuição
                if not all( # todos sao identificadores sem atribuicao inicial
                    isinstance(var, Node)
                    and isinstance(var.name, Token)
                    and var.name.terminal == identificador
                    for var in right):
                    errors.append(f"Apenas identificadores podem ser declarados.")
                    continue
                for var in right:
                    if var.name == op_atribuicao:
                        continue
                    if var.name.lexeme in symbol_table:
                        errors.append(f"Variável '{var.name.lexeme}' já declarada.")
                        continue
                    symbol_table[var.name.lexeme] = {"tipo": var_type_node.name.lexeme,}
            else:  # tem atribuição
                mid = len(right) // 2
                if len(right)% 2 != 1 or index_of_op_att != mid:
                    errors.append(f"Declaração deve ter a mesma quantidade de variaveis e valores.")
                    continue
                idens, values = right[:index_of_op_att], right[index_of_op_att + 1:]
                for iden, val in zip(idens, values):
                    if not isinstance(iden, Node) or not isinstance(iden.name, Token) or iden.name.terminal != identificador:
                        errors.append(f"Identificador inválido na declaração.")
                        continue
                    if iden.name.lexeme in symbol_table:
                        errors.append(f"Variável '{iden.name.lexeme}' já declarada.")
                        continue
                    value_expr_type = self._validate_expression(val)
                    if var_type_node.name.lexeme != value_expr_type:
                        errors.append(f"Tipo da variável '{iden.name.lexeme}' é '{var_type_node.name.lexeme}', mas o valor atribuído é do tipo '{value_expr_type}'.")
                        continue
                    symbol_table[iden.name.lexeme] = {"tipo": var_type_node.name.lexeme,}


        # ERROS DE USO DE VARIÁVEIS ANTES DA DECLARAÇÃO
        identifier_nodes = [node for node in ast.descendants if self.is_identifier(node)]
        for node in identifier_nodes:
            if node.name.lexeme not in symbol_table:
                errors.append(f"Variável '{node.name.lexeme}' não declarada antes do uso.")
        return errors

    def _validate_types(self, ast: Node) -> list:
        """
        Verificação de Tipos (Tipagem Estática)
        
        Atribuição: Em um comando de atribuição como x = y;, o tipo da variável y (ou do valor literal) deve ser compatível com o tipo da variável x, conforme registrado na Tabela de Símbolos. Um erro de "tipos incompatíveis"deve ser gerado se, por exemplo, tentar-se atribuir um texto a uma variável do tipo inteiro ou real .
        
        Argumentos de Comandos: Os tipos das expressões passadas como argumentos para os comandos devem ser validados. Por exemplo, o comando avancar espera um argumento do tipo inteiro. Se uma variável do tipo texto for fornecida, um erro semântico deve ser acusado.
        """

        errors = []
        # VALIDAÇÕES DE EXPRESSÕES EM ATRIBUIÇÕES
        att = [node for node in ast.descendants if self.is_atribution(node)]
        for node in att:
            iden_node, expr_node = node.children
            symbol_info = self.symbol_table.get(iden_node.name.lexeme)
            if symbol_info is None:
                errors.append(f"Variável '{iden_node.name.lexeme}' não declarada antes da atribuição.")
                continue
            info_type = symbol_info.get("tipo", None)
            type_expr = self._validate_expression(expr_node)
            if type_expr is None:
                errors.append(f"A expressão atribuida a variável '{iden_node.name.lexeme}' é inválida.")
                continue
            if info_type != type_expr:
                errors.append(f"A variável '{iden_node.name.lexeme}' é do tipo '{info_type}', mas a expressão é do tipo '{type_expr}'.")
                continue

        # VALIDAÇÕES DE EXPRESSÕES EM COMANDOS
        mapping_commands = {
            cmd_avancar: inteiro.name,
            cmd_recuar: inteiro.name,
            cmd_girar_direita: inteiro.name,
            cmd_girar_esquerda: inteiro.name,
            cmd_ir_para: (inteiro.name, inteiro.name),
            cmd_definir_cor: texto,
            cmd_definir_espessura: inteiro.name,
            cmd_cor_de_fundo: texto,
        }
        commands = [
            node
            for node in ast.descendants
            if isinstance(node.name, Token) and node.name.terminal in mapping_commands
        ]
        for node in commands:
            command_type = node.name.terminal
            expected_type = mapping_commands[command_type]
            expected_type = (
                (expected_type,) if isinstance(expected_type, str) else expected_type
            )
            expr_types = tuple(
                [self._validate_expression(child) for child in node.children]
            )
            if expected_type != expr_types:
                errors.append(f"Comando '{command_type.name}' espera argumentos do tipo '{expected_type}', mas recebeu '{expr_types}'.")
                continue

        # VALIDAÇÕES DE EXPRESSÕES EM CONDIÇÕES(SE, ENQUANTO, REPITA)
        mapping_conditions = {
            "se": logico.name,
            "enquanto": logico.name,
            "repita": inteiro.name,
        }
        conditional_nodes = [
            node
            for node in ast.descendants
            if isinstance(node.name, Token) and node.name.lexeme in mapping_conditions
        ]
        for node in conditional_nodes:
            expected_type = mapping_conditions[node.name.lexeme]
            expr = node.children[0]
            expr_type = self._validate_expression(expr)
            if expected_type != expr_type:
                errors.append(f"Condição '{node.name.lexeme}' espera um argumento do tipo '{expected_type}', mas recebeu '{expr_type}'.")
                continue
        return errors

    def _validate_expression(self, node: Node) -> str:
        if node.is_leaf and self.is_identifier(node):
            # se for identificador, tem que retornar o tipo do identificador na tabela de símbolos
            return self.symbol_table.get(node.name.lexeme, {}).get("tipo", None)

        if node.is_leaf and self.is_primitive(node):
            return node.name.terminal.name

        if self.is_arithmetic_operation(node):
            # se for operação aritmética, tem que validar os filhos
            left_type = self._validate_expression(node.children[0])
            right_types = [
                self._validate_expression(child) for child in node.children[1:]
            ]
            if left_type == "inteiro" and all(rt == "inteiro" for rt in right_types):
                return "inteiro"
            elif left_type == "real" or any(rt == "real" for rt in right_types):
                return "real"
            else:
                return None

        if self.is_comparison_operation(node):
            # se for operação de comparação, tem que validar os filhos
            left_type = self._validate_expression(node.children[0])
            right_types = [
                self._validate_expression(child) for child in node.children[1:]
            ]
            # right_type = _validate_expression(node.children[1])
            if left_type == "inteiro" and all(rt == "inteiro" for rt in right_types):
                return "logico"
            elif left_type == "real" and all(rt == "real" for rt in right_types):
                return "logico"
            elif left_type == "texto" and all(rt == "texto" for rt in right_types):
                return "logico"
            elif left_type == "logico" and all(rt == "logico" for rt in right_types):
                return "logico"
            else:
                return None

        if self.is_logical_operation(node):
            # se for operação lógica, tem que validar os filhos
            left_type = self._validate_expression(node.children[0])
            right_types = [self._validate_expression(child) for child in node.children[1:]]
            if left_type == "logico" and all(rt == "logico" for rt in right_types):
                return "logico"
            else:
                return None
        return None

    @staticmethod
    def index_of(children, terminal: Token | Node) -> int:
        """Retorna o índice do primeiro nó com o terminal especificado."""
        for i, child in enumerate(children):
            if isinstance(child.name, Token) and child.name.terminal == terminal:
                return i
            elif isinstance(child, Node) and child.name == terminal:
                return i
        return -1

    @staticmethod
    def is_atribution(node: Node) -> bool:
        """Verifica se o nó é uma atribuição."""
        return isinstance(node.name, Token) and node.name.terminal == op_atribuicao

    @staticmethod
    def is_declaration(node: Node) -> bool:
        """Verifica se o nó é uma declaração de variável."""
        # return node.name == dois_pontos.repr
        return isinstance(node.name, Token) and node.name.terminal == dois_pontos

    @staticmethod
    def is_identifier(node: Node) -> bool:
        """Verifica se o nó é um identificador."""
        return isinstance(node.name, Token) and node.name.terminal == identificador

    @staticmethod
    def is_arithmetic_operation(node: Node) -> bool:
        """Verifica se o nó é uma operação aritmética."""
        return isinstance(node.name, Token) and node.name.terminal in {
            op_mais,
            op_menos,
            op_multiplicacao,
            op_div,
            op_modulo,
        }

    @staticmethod
    def is_comparison_operation(node: Node) -> bool:
        """Verifica se o nó é uma operação de comparação."""
        return isinstance(node.name, Token) and node.name.terminal in {
            op_igualdade,
            op_diferente,
            op_menor_ou_igual,
            op_maior_ou_igual,
            op_menor_que,
            op_maior_que,
        }

    @staticmethod
    def is_logical_operation(node: Node) -> bool:
        """Verifica se o nó é uma operação lógica."""
        return isinstance(node.name, Token) and node.name.terminal in {
            op_e,
            op_ou,
            op_nao,
        }

    @staticmethod
    def is_primitive(node: Node) -> bool:
        """Verifica se o nó é um terminal primitivo (inteiro, real, texto, logico)."""
        return isinstance(node.name, Token) and node.name.terminal in {
            inteiro,
            real,
            texto,
            logico,
        }

if __name__ == "__main__":
    script_input = """
    inicio
        var inteiro: a, b;
        var inteiro: i, j = a, b;
        a = 1;
        repita 10 vezes
            avancar 10;
        fim_repita;
        se a > b entao
            avancar 100;
        senao
            avancar 50;
        fim_se;
        enquanto i < 10 faca
            avancar i;
            i = i + 1;
        fim_enquanto;
    fim
    """
    # Tabela LL(1)
    ll1_table = LL1Table(grammar=grammar)
    # Parser LL(1)
    parser = LL1ParserTable(table=ll1_table, start_symbol=grammar.start_symbol)

    print(Fore.YELLOW + "=" * 50 + Fore.RESET)
    # Tokenização
    tokens = Tokenizer.tokenize(script_input, grammar=grammar)
    # Parsing
    parsed, derivation_tree_root = parser.parse(tokens)
    if not parsed:
        print(Fore.RED + "Erro na análise sintática." + Fore.RESET)
        exit(1)
    else:
        print(Fore.GREEN + "Análise sintática bem-sucedida!" + Fore.RESET)

    print("AST:")
    ast_root = get_ast_root(derivation_tree_root)
    for pre, fill, node in RenderTree(ast_root):
        print(
            f"{pre}"
            + {True: Fore.BLUE, False: Fore.BLACK}[node.is_leaf]
            + f"{node.name.lexeme if isinstance(node.name, Token) else node.name}"
            + Fore.RESET
        )

    semantic_processor = SemanticProcessor(grammar, symbol_table={})
    print(Fore.YELLOW + "=" * 50 + Fore.RESET)
    errors = semantic_processor.process(ast_root)
    for error in errors:
        for key, value in error.items():
            print(Fore.RED + f"{key}:" + Fore.RESET)
            for msg in value:
                print(Fore.RED + f"  - {msg}" + Fore.RESET)
    sym_table = semantic_processor.symbol_table
    print(Fore.YELLOW + "=" * 50 + Fore.RESET)
    print("Tabela de Símbolos:")
    for var, info in sym_table.items():
        print(f"  - {var}: {info}")
