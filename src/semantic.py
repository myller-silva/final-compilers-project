def verificar_uso_variavel_antes_declaracao(no, contexto, erros):
    if isinstance(no, tuple) and no[0] == "Fator":
        filhos = no[1]
        if len(filhos) == 2 and filhos[0] == "IDENTIFICADOR":
            nome_var = filhos[1]
            if nome_var not in contexto["variaveis_declaradas"]:
                erros.append(f"Variável '{nome_var}' usada antes de ser declarada.")


def registrar_variaveis(no, contexto, erros):
    if isinstance(no, tuple) and no[0] == "Declaracao":
        filhos = no[1]
        tipo, nome = filhos  # ex: ['INTEIRO', 'x']
        contexto["variaveis_declaradas"].add(nome)


class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.contexto = {
            "variaveis_declaradas": set(),
        }
        self.verificacoes = [
            registrar_variaveis,
            verificar_uso_variavel_antes_declaracao,
        ]
        self.erros = []

    def add_verification(self, func):
        self.verificacoes.append(func)

    def analyze(self):
        self._traverse_nodes(self.ast)
        return self.erros

    def _traverse_nodes(self, no):
        for verificacao in self.verificacoes:
            verificacao(no, self.contexto, self.erros)

        if isinstance(no, tuple):
            _, filhos = no
            self._traverse_nodes(filhos)
        elif isinstance(no, list):
            for filho in no:
                self._traverse_nodes(filho)
