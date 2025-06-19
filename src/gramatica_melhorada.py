# TERMINAIS DA GRAMATICA
from others.table_parser_ll1 import Production, Terminal

# TODO: verificar se precisar usar os boundares (\b dos regex para evitar conflitos, ou se nao precisa)
# talvez precise pq to removendo os espaços em branco antes de tokenizar, mas nao sei se isso interfere no regex
comentario = Terminal("comentario", r"//.*")
espaco = Terminal("espaco", r"[ \t]+")

kw_var = Terminal("kw_var", r"\bvar\b")

kw_inteiro = Terminal("kw_inteiro", r"\binteiro\b")
kw_real = Terminal("kw_real", r"\breal\b")
kw_texto = Terminal("kw_texto", r"\btexto\b")
kw_logico = Terminal("kw_logico", r"\blogico\b")

kw_se = Terminal("kw_se", r"\bse\b")
kw_fim_se = Terminal("kw_fim_se", r"\bfim_se\b")
kw_entao = Terminal("kw_entao", r"\bentao\b")
kw_senao = Terminal("kw_senao", r"\bsenao\b")

kw_enquanto = Terminal("kw_enquanto", r"\benquanto\b")
kw_faca = Terminal("kw_faca", r"\bfaca\b")
kw_fim_enquanto = Terminal("kw_fim_enquanto", r"\bfim_enquanto\b")

kw_repita = Terminal("kw_repita", r"\brepita\b")
kw_vezes = Terminal("kw_vezes", r"\bvezes\b")
kw_fim_repita = Terminal("kw_fim_repita", r"\bfim_repita\b")

kw_inicio_bloco = Terminal("kw_inicio_bloco", r"\binicio\b")
kw_fim_bloco = Terminal("kw_fim_bloco", r"\bfim\b")

# TODO: com ou sem parenteses?
cmd_avancar = Terminal("cmd_avancar", r"\b(avancar)\b")
cmd_recuar = Terminal("cmd_recuar", r"\b(recuar)\b")
cmd_girar_direita = Terminal("cmd_girar_direita", r"\b(girar_direita)\b")
cmd_girar_esquerda = Terminal("cmd_girar_esquerda", r"\b(girar_esquerda)\b")
cmd_ir_para = Terminal("cmd_ir_para", r"\b(ir_para)\b")

cmd_levantar_caneta = Terminal("cmd_levantar_caneta", r"\b(levantar_caneta)\b")
cmd_abaixar_caneta = Terminal("cmd_abaixar_caneta", r"\b(abaixar_caneta)\b")
cmd_definir_cor = Terminal("cmd_definir_cor", r"\b(definir_cor)\b")
cmd_definir_espessura = Terminal("cmd_definir_espessura", r"\b(definir_espessura)\b")

cmd_limpar_tela = Terminal("cmd_limpar_tela", r"\b(limpar_tela)\b")
cmd_cor_de_fundo = Terminal("cmd_cor_de_fundo", r"\b(cor_de_fundo)\b")

real = Terminal("real", r"\d+\.\d+")
inteiro = Terminal("inteiro", r"\d+")
texto = Terminal("texto", r'"[^"]*"')
logico = Terminal("logico", r"\b(verdadeiro|falso)\b")

op_mais = Terminal("op_mais", r"\+")
op_menos = Terminal("op_menos", r"-")
op_multiplicacao = Terminal("op_multiplicacao", r"\*")
op_div = Terminal("op_div", r"/")
op_igualdade = Terminal("op_igualdade", r"==")
op_diferente = Terminal("op_diferente", r"!=")
op_menor_ou_igual = Terminal("op_menor_ou_igual", r"<=")
op_maior_ou_igual = Terminal("op_maior_ou_igual", r">=")
op_menor_que = Terminal("op_menor_que", r"<")
op_maior_que = Terminal("op_maior_que", r">")
op_modulo = Terminal("op_modulo", r"%")

# OPERADORES LOGICOS
op_e = Terminal("op_e", r"&&")
op_ou = Terminal("op_ou", r"\|\|")
op_nao = Terminal("op_nao", r"!")

identificador = Terminal("identificador", r"[a-zA-Z_][a-zA-Z_0-9]*")
dois_pontos = Terminal("dois_pontos", r":")
ponto_virgula = Terminal("ponto_virgula", r";")
ponto = Terminal("ponto", r"\.")
virgula = Terminal("virgula", r",")
abre_parenteses = Terminal("abre_parenteses", r"\(")
fecha_parenteses = Terminal("fecha_parenteses", r"\)")
op_atribuicao = Terminal("op_atribuicao", r"=")
quebra_linha = Terminal("quebra_linha", r"\n")

terminals = [
    comentario,
    espaco,
    kw_var,
    kw_inteiro,
    kw_real,
    kw_texto,
    kw_logico,
    kw_se,
    kw_fim_se,
    kw_entao,
    kw_senao,
    kw_enquanto,
    kw_faca,
    kw_fim_enquanto,
    kw_repita,
    kw_vezes,
    kw_fim_repita,
    kw_inicio_bloco,
    kw_fim_bloco,
    # TODO: com ou sem parenteses?
    cmd_avancar,
    cmd_recuar,
    cmd_girar_direita,
    cmd_girar_esquerda,
    cmd_ir_para,
    cmd_levantar_caneta,
    cmd_abaixar_caneta,
    cmd_definir_cor,
    cmd_definir_espessura,
    cmd_limpar_tela,
    cmd_cor_de_fundo,
    real,
    inteiro,
    texto,
    logico,
    op_mais,
    op_menos,
    op_multiplicacao,
    op_div,
    op_igualdade,
    op_diferente,
    op_menor_ou_igual,
    op_maior_ou_igual,
    op_menor_que,
    op_maior_que,
    op_modulo,
    # OPERADORES LOGICOS
    op_e,
    op_ou,
    op_nao,
    identificador,
    dois_pontos,
    ponto_virgula,
    ponto,
    virgula,
    abre_parenteses,
    fecha_parenteses,
    op_atribuicao,
    quebra_linha,
]


# NAO TERMINAIS DA GRAMATICA
from others.table_parser_ll1 import NonTerminal

Programa = NonTerminal("Programa")
Bloco = NonTerminal("Bloco")
Declaracoes = NonTerminal("Declaracoes")  # Declaracoes de Variaveis
DeclaracaoVariavel = NonTerminal("DeclaracaoVariavel")
Identificadores = NonTerminal("Identificadores")
IdentificadoresR = NonTerminal("IdentificadoresR")
Comandos = NonTerminal("Comandos")
Comando = NonTerminal("Comando")
Atribuicao = NonTerminal("Atribuicao")
Condicional = NonTerminal("Condicional")
Senao = NonTerminal("Senao")
LacoRepeticao = NonTerminal("LacoRepeticao")
Repita = NonTerminal("Repita")
Enquanto = NonTerminal("Enquanto")
Movimento = NonTerminal("Movimento")
ControleCaneta = NonTerminal("ControleCaneta")
ControleTela = NonTerminal("ControleTela")
Tipo = NonTerminal("Tipo")
Expr = NonTerminal("Expr")
# GRAMATICA DE EXPRESSAO ARITIMETICA:
# E -> T E'
# E' -> + T E' | - T E' | ε
# T -> F T'
# T' -> * F T' | / F T' | ε
# F -> NUM | ( E )
(
    ExprAritmetica, 
    Term, 
    Factor, 
    ExprAritmeticaR, 
    TermR, 
    Num
) = [
    NonTerminal(name)
    for name in [
        "ExprAritmetica", 
        "Term", 
        "Factor", 
        "ExprAritmeticaR", 
        "TermR", 
        "Num"
    ]
]
# GRAMATICA DE EXPRESSAO LOGICA:
# E  -> T E'
# E' -> OR T E' | ε
# T  -> F T'
# T' -> AND F T' | ε
# F  -> NOT F | C
# C  -> P C'
# C' -> == P | != P | < P | <= P | > P | >= P | ε
# P  -> ( E ) | IDENTIFICADOR | VERDADEIRO | FALSO
(
    ExprLogica,
    TermLogico,
    FactorLogico,
    Comparacao,
    ExprLogicaR,
    TermLogicoR,
    ComparacaoR,
    Primitivo,
) = [
    NonTerminal(name)
    for name in [
        "ExprLogica",
        "TermLogico",
        "FactorLogico",
        "Comparacao",
        "ExprLogicaR",
        "TermLogicoR",
        "ComparacaoR",
        "Primitivo",
    ]
]

non_terminals = [
    Programa,
    Bloco,
    Declaracoes,
    DeclaracaoVariavel,
    Identificadores,
    IdentificadoresR,
    Comandos,
    Comando,
    Atribuicao,
    Condicional,
    Senao,
    LacoRepeticao,
    Repita,
    Enquanto,
    Movimento,
    ControleCaneta,
    ControleTela,
    Tipo,
    Expr,
    ExprAritmetica,
    Term,
    Factor,
    ExprAritmeticaR,
    TermR,
    Num,
    ExprLogica,
    TermLogico,
    FactorLogico,
    Comparacao,
    Primitivo,
    ExprLogicaR,
    TermLogicoR,
    ComparacaoR,
    Primitivo,
]

# PRODUÇÕES DA GRAMATICA
from others.table_parser_ll1 import Production

productions = [
    # --- Programa ---
    Production(Programa, [Bloco]),
    Production(Bloco, [kw_inicio_bloco, Declaracoes, Comandos, kw_fim_bloco]),
    # --- Declaracoes ---
    Production(Declaracoes, [DeclaracaoVariavel, Declaracoes]),
    Production(Declaracoes, []),
    Production(DeclaracaoVariavel, [kw_var, Tipo, dois_pontos, Identificadores, ponto_virgula]),
    Production(Identificadores, [identificador, IdentificadoresR]),
    Production(IdentificadoresR, [virgula, Identificadores]),
    Production(IdentificadoresR, []),
    # Declarar variaveis tipo texto aqui tambem? por exemplo, text = "ola mundo";, ou deixar a declaracao de texto em qualquer parte do codigo? # TODO: perguntar ao professor
    # Production(DeclaracaoVariavel, [identificador, op_atribuicao, texto, ponto_virgula]) #ex: 'text = "ola mundo";'
    # --- Tipo --- 
    Production(Tipo, [kw_inteiro]),
    Production(Tipo, [kw_real]),
    Production(Tipo, [kw_texto]),
    Production(Tipo, [kw_logico]),
    # --- Comandos --- 
    Production(Comandos, [Comando, Comandos]),
    Production(Comandos, []),
    # --- Comando --- 
    Production(Comando, [Atribuicao]),
    Production(Comando, [Condicional]),
    Production(Comando, [LacoRepeticao]),
    Production(Comando, [Movimento]),
    Production(Comando, [ControleCaneta]),
    Production(Comando, [ControleTela]),
    # --- Atribuicao --- 
    Production(Atribuicao, [identificador, op_atribuicao, Expr, ponto_virgula]),
    # --- Condicional (SE) --- 
    Production(Condicional, [kw_se, ExprLogica, kw_entao, Comandos, Senao, kw_fim_se, ponto_virgula]),
    Production(Senao, [kw_senao, Comandos]),
    Production(Senao, []),
    # --- LacoRepeticao --- 
    Production(LacoRepeticao, [Repita]),
    Production(LacoRepeticao, [Enquanto]),
    # --- LacoRepeticao (Repita) --- 
    Production(Repita,[kw_repita, ExprAritmetica, kw_vezes, Comandos, kw_fim_repita, ponto_virgula]),
    #  --- LacoRepeticao (Enquanto) --- 
    Production(Enquanto,[kw_enquanto, ExprLogica, kw_faca, Comandos, kw_fim_enquanto, ponto_virgula]),
    
    # --- Movimento ---
    Production(Movimento, [cmd_avancar, ExprAritmetica, ponto_virgula]),
    Production(Movimento, [cmd_recuar, ExprAritmetica, ponto_virgula]),
    Production(Movimento, [cmd_girar_direita, ExprAritmetica, ponto_virgula]),
    Production(Movimento, [cmd_girar_esquerda, ExprAritmetica, ponto_virgula]),
    Production(Movimento, [cmd_ir_para, Expr, ExprAritmetica, ponto_virgula]),
    # --- Controle da caneta --- 
    Production(ControleCaneta, [cmd_levantar_caneta, ponto_virgula]),
    Production(ControleCaneta, [cmd_abaixar_caneta, ponto_virgula]),
    Production(ControleCaneta, [cmd_definir_cor, ExprAritmetica, ponto_virgula]),
    Production(ControleCaneta, [cmd_definir_espessura, ExprAritmetica, ponto_virgula]),
    # --- Controle de tela ---
    Production(ControleTela, [cmd_limpar_tela, ponto_virgula]),
    Production(ControleTela, [cmd_cor_de_fundo, Expr, ponto_virgula]),
    
    # --- Expressões --- (Aritméticas e Lógicas)
    Production(Expr, [ExprAritmetica]),
    Production(Expr, [ExprLogica]),
    
    # --- Expr Aritmetica ---
    Production(ExprAritmetica, [Term, ExprAritmeticaR]),
    Production(ExprAritmeticaR, [op_mais, Term, ExprAritmeticaR]),
    Production(ExprAritmeticaR, [op_menos, Term, ExprAritmeticaR]),
    Production(ExprAritmeticaR, []),
    Production(Term, [Factor, TermR]),
    Production(TermR, [op_multiplicacao, Factor, TermR]),
    Production(TermR, [op_div, Factor, TermR]),
    # Production(TermR, [op_modulo, Factor, TermR]), # TODO: verificar se coloco o modulo aqui
    Production(TermR, []),
    Production(Factor, [Num]),
    Production(Factor, [abre_parenteses, ExprAritmetica, fecha_parenteses]),
    Production(Num, [inteiro]),
    Production(Num, [real]),
    Production(Num, [identificador]),  # TODO: verificar depois se faz sentido colocar identificador aqui, mas provavelmente sim
    
    # --- Expr Lógica --- 
    Production(ExprLogica, [TermLogico, ExprLogicaR]),
    Production(ExprLogicaR, [op_ou, TermLogico, ExprLogicaR]),
    Production(ExprLogicaR, []),
    Production(TermLogico, [FactorLogico, TermLogicoR]),
    Production(TermLogicoR, [op_e, FactorLogico, TermLogicoR]),
    Production(TermLogicoR, []),
    Production(FactorLogico, [op_nao, FactorLogico]),
    Production(FactorLogico, [Comparacao]),
    Production(Comparacao, [Primitivo, ComparacaoR]),
    Production(ComparacaoR, [op_igualdade, Primitivo]),
    Production(ComparacaoR, [op_diferente, Primitivo]),
    Production(ComparacaoR, [op_menor_ou_igual, Primitivo]),
    Production(ComparacaoR, [op_maior_ou_igual, Primitivo]),
    Production(ComparacaoR, [op_menor_que, Primitivo]),
    Production(ComparacaoR, [op_maior_que, Primitivo]),
    Production(ComparacaoR, []),
    Production(Primitivo, [logico]),
    Production(Primitivo, [identificador]), # TODO Production(Primitivo, [identificador]), talvez dê ambiguidade pq a partir de ExprAritmetica pode chegar em Production(Num, [identificador]),
    Production(Primitivo, [abre_parenteses, ExprLogica, fecha_parenteses]), # TODO: pode causar ambiguidade se ExprAritmetica for Primitivo
    # Production(Primitivo, [ExprAritmetica]), # TODO: o primitivo de uma expressao o logica é uma expressao aritmetica, ou um idenficador, ou um logico
]

# TODO: adicionar a opcao de atribuir valor diretamente na declaracao da variavel, por exemplo: var inteiro : contador = 0;
# TODO: se tiver duas variaveis, que tenha duas atribuicoes, por exemplo: var inteiro : contador, preco = 1, 2;
# TODO: EXPR, ExprAritmetica, ExprLogica estão erradas, corrigir as produções.
# ERROR: nenhuma producao para (Comandos, EOF)
text = """
inicio
    var inteiro : passo;
    se verdadeiro entao
        avancar ((10+(10)));
    senao
        girar_direita 90;
    fim_se;
fim
"""
from others.table_parser_ll1 import Grammar, LL1Table, LL1ParserTable, Tokenizer

grammar = Grammar(
    start_symbol=Programa,
    terminals=terminals,
    non_terminals=non_terminals,
    productions=productions
)

print("--------------")
print("Gramática")
print("--------------")
print(grammar)

tokens = Tokenizer.tokenize(text, grammar)

ll1_table = LL1Table(grammar)
# ll1_table.print_table() # TODO: melhorar a impressao da tabela depois, talvez com dataframe pandas
ll1_parser_table = LL1ParserTable(ll1_table, Programa)
ll1_parser_table.parse(tokens)
print("--------------")

from utils.text import colorize_text
print(colorize_text("Tokens encontrados:", "red"))
for token in tokens:
    print(
        colorize_text(f"{token.terminal.name}", "blue"),
        colorize_text(f"{token.lexeme}", "yellow")
    )
