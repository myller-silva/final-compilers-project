from anytree import Node
from table_parser_ll1 import Token


class Generator:
    def __init__(self):
        self.variables = {}  # Armazena as variáveis declaradas
        self.python_code = []  # Lista para armazenar as linhas de código Python
        self.indentation_level = 0  # Nível de indentação atual

    def generate(self, ast: Node, title='Turtle Script') -> str:
        """Gera código Python a partir da AST."""
        self.python_code = []
        self.variables = {}
        self.indentation_level = 0

        # Adiciona imports e inicialização
        self._add_line("import turtle")
        self._add_line("#---Configuração Padrão --")
        self._add_line("screen = turtle.Screen()")
        self._add_line("t = turtle.Turtle()")
        self._add_line(f"screen.title('{title}')")
        self._add_line("#--- Codigo Gerado pelo Compilador--")

        # Processa a AST
        self._process_node(ast)

        # Adiciona código de finalização
        self._add_line("#--- Finalizacao--")
        self._add_line("turtle.done()")

        return "\n".join(self.python_code)

    def _add_line(self, line: str):
        """Adiciona uma linha de código com a indentação apropriada."""
        if line.strip() == "":
            self.python_code.append("")
        else:
            indent = "    " * self.indentation_level
            self.python_code.append(indent + line)

    def _get_node_name(self, node: Node) -> str:
        """Obtém o nome correto de um nó (lexeme se for Token, name caso contrário)."""
        if isinstance(node.name, Token):
            return node.name.lexeme
        return str(node.name)

    def _process_node(self, node: Node):
        """Processa um nó da AST recursivamente."""
        if isinstance(node.name, Token):
            # Verifica se é um token de comando que precisa ser processado especialmente
            token_name = node.name.terminal.name

            # Declarações e atribuições
            if token_name == "dois_pontos":
                self._process_declaration(node)
                return
            elif token_name == "op_atribuicao":
                self._process_assignment(node)
                return
            # Estruturas de controle
            elif token_name == "kw_se":
                self._process_conditional(node)
                return
            elif token_name == "kw_senao":
                self._process_else(node)
                return
            elif token_name == "kw_repita":
                self._process_repeat(node)
                return
            elif token_name == "kw_enquanto":
                self._process_while(node)
                return
            # Comandos de movimento
            elif token_name == "cmd_avancar":
                self._process_forward(node)
                return
            elif token_name == "cmd_recuar":
                self._process_backward(node)
                return
            elif token_name == "cmd_girar_direita":
                self._process_turn_right(node)
                return
            elif token_name == "cmd_girar_esquerda":
                self._process_turn_left(node)
                return
            elif token_name == "cmd_ir_para":
                self._process_goto(node)
                return
            # Comandos de caneta
            elif token_name == "cmd_levantar_caneta":
                self._process_pen_up(node)
                return
            elif token_name == "cmd_abaixar_caneta":
                self._process_pen_down(node)
                return
            # Comandos de configuração
            elif token_name == "cmd_definir_cor":
                self._process_set_color(node)
                return
            elif token_name == "cmd_definir_espessura":
                self._process_set_width(node)
                return
            elif token_name == "cmd_limpar_tela":
                self._process_clear(node)
                return
            elif token_name == "cmd_cor_de_fundo":
                self._process_bg_color(node)
                return
            # Operações
            elif token_name == "op_mais":
                return self._process_binary_operation(node, "+")
            elif token_name == "op_menos":
                return self._process_binary_operation(node, "-")
            elif token_name == "op_multiplicacao":
                return self._process_binary_operation(node, "*")
            elif token_name == "op_div":
                return self._process_binary_operation(node, "/")
            elif token_name == "op_modulo":
                return self._process_binary_operation(node, "%")
            elif token_name == "op_igualdade":
                return self._process_binary_operation(node, "==")
            elif token_name == "op_diferente":
                return self._process_binary_operation(node, "!=")
            elif token_name == "op_menor_que":
                return self._process_binary_operation(node, "<")
            elif token_name == "op_maior_que":
                return self._process_binary_operation(node, ">")
            elif token_name == "op_menor_ou_igual":
                return self._process_binary_operation(node, "<=")
            elif token_name == "op_maior_ou_igual":
                return self._process_binary_operation(node, ">=")
            elif token_name == "op_e":
                return self._process_logical_operation(node, "and")
            elif token_name == "op_ou":
                return self._process_logical_operation(node, "or")
            elif token_name == "op_nao":
                return self._process_unary_operation(node, "not")
            else:
                # Para outros tokens, retorna a representação
                return self._process_token(node.name)

        # Para nós não-token, usa o nome do nó
        node_name = self._get_node_name(node)

        # Processa o nó Program
        if node_name == "Program":
            self._process_program(node)
            return

        # Declarações de variáveis - verifica se é um token de dois pontos
        if isinstance(node.name, Token) and node.name.terminal.name == "dois_pontos":
            self._process_declaration(node)
            return

        # Atribuições - verifica se é um token de atribuição
        if isinstance(node.name, Token) and node.name.terminal.name == "op_atribuicao":
            self._process_assignment(node)
            return

        # Estruturas de controle - verifica se são tokens de palavras-chave
        if isinstance(node.name, Token) and node.name.terminal.name == "kw_se":
            self._process_conditional(node)
            return

        if isinstance(node.name, Token) and node.name.terminal.name == "kw_senao":
            self._process_else(node)
            return

        if isinstance(node.name, Token) and node.name.terminal.name == "kw_repita":
            self._process_repeat(node)
            return

        if isinstance(node.name, Token) and node.name.terminal.name == "kw_enquanto":
            self._process_while(node)
            return

        # Operações - verifica se são tokens de operadores
        if isinstance(node.name, Token):
            token_name = node.name.terminal.name
            if token_name == "op_mais":
                return self._process_binary_operation(node, "+")
            elif token_name == "op_menos":
                return self._process_binary_operation(node, "-")
            elif token_name == "op_multiplicacao":
                return self._process_binary_operation(node, "*")
            elif token_name == "op_div":
                return self._process_binary_operation(node, "/")
            elif token_name == "op_modulo":
                return self._process_binary_operation(node, "%")
            elif token_name == "op_igualdade":
                return self._process_binary_operation(node, "==")
            elif token_name == "op_diferente":
                return self._process_binary_operation(node, "!=")
            elif token_name == "op_menor_que":
                return self._process_binary_operation(node, "<")
            elif token_name == "op_maior_que":
                return self._process_binary_operation(node, ">")
            elif token_name == "op_menor_ou_igual":
                return self._process_binary_operation(node, "<=")
            elif token_name == "op_maior_ou_igual":
                return self._process_binary_operation(node, ">=")
            elif token_name == "op_e":
                return self._process_logical_operation(node, "and")
            elif token_name == "op_ou":
                return self._process_logical_operation(node, "or")
            elif token_name == "op_nao":
                return self._process_unary_operation(node, "not")

        # Processamento genérico para nós não específicos
        return self._process_generic_node(node)

    def _process_token(self, token: Token) -> str:
        """Processa um token e retorna sua representação em Python."""
        token_name = token.terminal.name
        lexeme = token.lexeme

        if token_name == "identificador":
            return lexeme
        elif token_name == "inteiro":
            return lexeme
        elif token_name == "real":
            return lexeme
        elif token_name == "texto":
            return lexeme  # Já vem com aspas
        elif token_name == "logico":
            return "True" if lexeme == "verdadeiro" else "False"
        else:
            return lexeme

    def _process_program(self, node: Node):
        """Processa o nó do programa principal."""
        for child in node.children:
            result = self._process_node(child)
            # Se o resultado não é None e não é uma string vazia, pode ser que precise ser processado
            # como um comando no nível do programa

    def _process_declaration(self, node: Node):
        """Processa uma declaração de variável (nó ':')."""
        # Estrutura: : -> tipo -> variáveis...
        if len(node.children) >= 2:
            # O primeiro filho é o tipo, os demais são variáveis
            type_node = node.children[0]
            var_type = self._process_node(type_node)
            variables = []

            # Processa todas as variáveis
            i = 1
            while i < len(node.children):
                child = node.children[i]
                child_name = self._get_node_name(child)

                if child_name == "=":
                    # Chegou na parte de atribuição, para aqui
                    break

                var_name = self._process_node(child)
                variables.append(var_name)
                self.variables[var_name] = var_type
                i += 1

            # Inicializa as variáveis
            for var in variables:
                if var_type == "inteiro":
                    self._add_line(f"{var} = 0")
                elif var_type == "real":
                    self._add_line(f"{var} = 0.0")
                elif var_type == "texto":
                    self._add_line(f'{var} = ""')
                elif var_type == "logico":
                    self._add_line(f"{var} = False")

            # Se há atribuições na declaração (como: var inteiro: i, j = a, b;)
            if i < len(node.children):
                # Processa as atribuições iniciais
                j = 0
                for k in range(i + 1, len(node.children)):
                    if j < len(variables):
                        value = self._process_node(node.children[k])
                        self._add_line(f"{variables[j]} = {value}")
                        j += 1

    def _process_assignment(self, node: Node):
        """Processa uma atribuição de variável (nó '=')."""
        if len(node.children) >= 2:
            var_name = self._process_node(node.children[0])
            expr_value = self._process_node(node.children[1])
            self._add_line(f"{var_name} = {expr_value}")

    def _process_conditional(self, node: Node):
        """Processa um comando condicional ('se')."""
        if len(node.children) >= 2:
            condition = self._process_node(node.children[0])
            self._add_line(f"if {condition}:")
            self.indentation_level += 1

            # Processa comandos do bloco então (todos os filhos exceto o último se for 'senao')
            for i in range(1, len(node.children)):
                child = node.children[i]
                if self._get_node_name(child) == "senao":
                    # Volta a indentação e processa o senão
                    self.indentation_level -= 1
                    self._process_node(child)
                    return
                else:
                    self._process_node(child)

            self.indentation_level -= 1

    def _process_else(self, node: Node):
        """Processa o bloco senão."""
        self._add_line("else:")
        self.indentation_level += 1

        for child in node.children:
            self._process_node(child)

        self.indentation_level -= 1

    def _process_repeat(self, node: Node):
        """Processa um loop repita."""
        if len(node.children) >= 1:
            times = self._process_node(node.children[0])
            self._add_line(f"for _ in range({times}):")
            self.indentation_level += 1

            # Processa comandos do loop (todos os filhos exceto o primeiro)
            for i in range(1, len(node.children)):
                self._process_node(node.children[i])

            self.indentation_level -= 1

    def _process_while(self, node: Node):
        """Processa um loop enquanto."""
        if len(node.children) >= 1:
            condition = self._process_node(node.children[0])
            self._add_line(f"while {condition}:")
            self.indentation_level += 1

            # Processa comandos do loop (todos os filhos exceto o primeiro)
            for i in range(1, len(node.children)):
                self._process_node(node.children[i])

            self.indentation_level -= 1

    def _process_forward(self, node: Node):
        """Processa comando avancar."""
        if len(node.children) > 0:
            distance = self._process_node(node.children[0])
            self._add_line(f"t.forward({distance})")
        else:
            self._add_line("t.forward(10)")  # valor padrão

    def _process_backward(self, node: Node):
        """Processa comando recuar."""
        if len(node.children) > 0:
            distance = self._process_node(node.children[0])
            self._add_line(f"t.backward({distance})")
        else:
            self._add_line("t.backward(10)")

    def _process_turn_right(self, node: Node):
        """Processa comando girar_direita."""
        if len(node.children) > 0:
            angle = self._process_node(node.children[0])
            self._add_line(f"t.right({angle})")
        else:
            self._add_line("t.right(90)")

    def _process_turn_left(self, node: Node):
        """Processa comando girar_esquerda."""
        if len(node.children) > 0:
            angle = self._process_node(node.children[0])
            self._add_line(f"t.left({angle})")
        else:
            self._add_line("t.left(90)")

    def _process_goto(self, node: Node):
        """Processa comando ir_para."""
        if len(node.children) >= 2:
            x = self._process_node(node.children[0])
            y = self._process_node(node.children[1])
            self._add_line(f"t.goto({x}, {y})")

    def _process_pen_up(self, node: Node):
        """Processa comando levantar_caneta."""
        self._add_line("t.penup()")

    def _process_pen_down(self, node: Node):
        """Processa comando abaixar_caneta."""
        self._add_line("t.pendown()")

    def _process_set_color(self, node: Node):
        """Processa comando definir_cor."""
        if len(node.children) > 0:
            color = self._process_node(node.children[0])
            self._add_line(f"t.color({color})")

    def _process_set_width(self, node: Node):
        """Processa comando definir_espessura."""
        if len(node.children) > 0:
            width = self._process_node(node.children[0])
            self._add_line(f"t.width({width})")

    def _process_clear(self, node: Node):
        """Processa comando limpar_tela."""
        self._add_line("t.clear()")

    def _process_bg_color(self, node: Node):
        """Processa comando cor_de_fundo."""
        if len(node.children) > 0:
            color = self._process_node(node.children[0])
            self._add_line(f"screen.bgcolor({color})")

    def _process_binary_operation(self, node: Node, operator: str):
        """Processa operações binárias."""
        if len(node.children) >= 2:
            left = self._process_node(node.children[0])
            right = self._process_node(node.children[1])
            return f"({left} {operator} {right})"
        return ""

    def _process_logical_operation(self, node: Node, operator: str):
        """Processa operações lógicas."""
        if len(node.children) >= 2:
            left = self._process_node(node.children[0])
            right = self._process_node(node.children[1])
            return f"({left} {operator} {right})"
        return ""

    def _process_unary_operation(self, node: Node, operator: str):
        """Processa operações unárias."""
        if len(node.children) >= 1:
            operand = self._process_node(node.children[0])
            return f"{operator} {operand}"
        return ""

    def _process_generic_node(self, node: Node):
        """Processamento genérico para nós não específicos."""
        if not node.children:
            return str(node.name) if hasattr(node, "name") else ""

        # Para nós com filhos, retorna o primeiro filho se for um valor simples
        if len(node.children) == 1:
            return self._process_node(node.children[0])

        # Para múltiplos filhos, processa todos e junta
        result_parts = []
        for child in node.children:
            part = self._process_node(child)
            if part and str(part).strip():
                result_parts.append(str(part))

        return " ".join(result_parts) if result_parts else ""
