from constants import *
grammar = [
    # Programa
    ("Programa", ["Bloco"]),
    # Bloco principal
    ("Bloco", [KW_INICIO_BLOCO, "DeclaracoesVariaveis", "Comandos", KW_FIM_BLOCO]),
    # Lista de declarações de variáveis
    ("DeclaracoesVariaveis", ["DeclaracaoVariavel", "DeclaracoesVariaveis"]),
    ("DeclaracoesVariaveis", []),  # ε
    (
        "DeclaracaoVariavel",
        [KW_VAR, "Tipo", DOIS_PONTOS, "ListaIdentificadores", PONTO_VIRGULA],
    ),
    # Permitindo múltiplos identificadores com atribuição opcional
    ("ListaIdentificadores", ["IdentificadorAtribuivel", "ListaIdentificadoresR"]),
    (
        "ListaIdentificadoresR",
        [VIRGULA, "IdentificadorAtribuivel", "ListaIdentificadoresR"],
    ),
    ("ListaIdentificadoresR", []),
    ("IdentificadorAtribuivel", [IDENTIFICADOR, "AtribuicaoOpcional"]),
    ("AtribuicaoOpcional", [OP_ATRIBUICAO, "Expressao"]),
    ("AtribuicaoOpcional", []),
    # Comandos
    ("Comandos", ["Comando", "Comandos"]),
    ("Comandos", []),  # ε (caso não haja mais comandos)
    ("Comando", ["Atribuicao"]),
    ("Comando", ["Movimento"]),
    ("Comando", ["ControleCaneta"]),
    ("Comando", ["ControleTela"]),
    ("Comando", ["Condicional"]),
    ("Comando", ["LacoRepeticao"]),
    # Atribuição
    ("Atribuicao", [IDENTIFICADOR, OP_ATRIBUICAO, "Expressao", PONTO_VIRGULA]),
    # Movimento
    ("Movimento", [CMD_AVANCAR, "Expressao", PONTO_VIRGULA]),
    ("Movimento", [CMD_RECUAR, "Expressao", PONTO_VIRGULA]),
    ("Movimento", [CMD_GIRAR_DIREITA, "Expressao", PONTO_VIRGULA]),
    ("Movimento", [CMD_GIRAR_ESQUERDA, "Expressao", PONTO_VIRGULA]),
    ("Movimento", [CMD_IRPARA, "Expressao", "Expressao", PONTO_VIRGULA]),
    # Controle da caneta
    ("ControleCaneta", [CMD_LEVANTAR_CANETA, PONTO_VIRGULA]),
    ("ControleCaneta", [CMD_ABAIXAR_CANETA, PONTO_VIRGULA]),
    ("ControleCaneta", [CMD_DEFINIR_COR, "Expressao", PONTO_VIRGULA]),
    ("ControleCaneta", [CMD_DEFINIR_ESPESSURA, "Expressao", PONTO_VIRGULA]),
    # Controle de tela
    ("ControleTela", [CMD_LIMPAR_TELA, PONTO_VIRGULA]),
    ("ControleTela", [CMD_COR_DE_FUNDO, "Expressao", PONTO_VIRGULA]),
    # Expressão
    ("Expressao", ["Termo", "ExpressaoR"]),
    ("ExpressaoR", [OP_MAIS, "Termo", "ExpressaoR"]),
    ("ExpressaoR", [OP_MENOS, "Termo", "ExpressaoR"]),
    ("ExpressaoR", []),  # ε (caso não haja mais termos)
    ("Termo", ["Fator", "TermoR"]),
    ("TermoR", [OP_MULTIPLICACAO, "Fator", "TermoR"]),
    ("TermoR", [OP_DIVISAO, "Fator", "TermoR"]),
    ("TermoR", [OP_MODULO, "Fator", "TermoR"]),
    ("TermoR", []),
    ("Fator", [INTEIRO]),
    ("Fator", [REAL]),
    ("Fator", [TEXTO]),  # TODO: melhorar depois
    ("Fator", [IDENTIFICADOR]),
    ("Fator", [ABRE_PARENTESES, "Expressao", FECHA_PARENTESES]),
    # Estrutura do SE
    ("Condicional", [KW_SE, "ExpressaoLogica", KW_ENTAO, "Comandos", KW_FIM_SE]),
    (
        "Condicional",
        [
            KW_SE,
            "ExpressaoLogica",
            KW_ENTAO,
            "Comandos",
            KW_SENAO,
            "Comandos",
            KW_FIM_SE,
        ],
    ),
    # Estrutura do Repita
    ("LacoRepeticao", ["LacoRepita"]),
    ("LacoRepeticao", ["LacoEnquanto"]),
    (
        "LacoRepita",
        [KW_REPITA, "Expressao", KW_VEZES, "Comandos", KW_FIM_REPITA, PONTO_VIRGULA],
    ),
    (
        "LacoEnquanto",
        [
            KW_ENQUANTO,
            "ExpressaoLogica",
            KW_FACA,
            "Comandos",
            KW_FIM_ENQUANTO,
            PONTO_VIRGULA,
        ],
    ),
    # Expressão lógica
    ("ExpressaoLogica", [ABRE_PARENTESES, "ExpressaoLogica", FECHA_PARENTESES]),
    ("ExpressaoLogica", ["Expressao", "OperadorLogico", "Expressao"]),
    ("OperadorLogico", [OP_IGUALDADE]),
    ("OperadorLogico", [OP_DIFERENTE]),
    ("OperadorLogico", [OP_MENOR_QUE]),
    ("OperadorLogico", [OP_MAIOR_QUE]),
    ("OperadorLogico", [OP_MENOR_OU_IGUAL]),
    ("OperadorLogico", [OP_MAIOR_OU_IGUAL]),
    # Tipos
    ("Tipo", [KW_INTEIRO]),
    ("Tipo", [KW_REAL]),
    ("Tipo", [KW_TEXTO]),
    ("Tipo", [KW_LOGICO]),
]