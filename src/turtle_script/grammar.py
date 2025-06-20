from colorama import Fore
from table_parser_ll1 import Terminal
from table_parser_ll1 import NonTerminal
from table_parser_ll1 import Grammar, LL1Table, LL1ParserTable, Tokenizer

# --- TERMINAIS DA GRAMATICA ---

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
op_mais = Terminal("op_mais", r"\+", repr="+")
op_menos = Terminal("op_menos", r"-", repr="-")
op_multiplicacao = Terminal("op_multiplicacao", r"\*", repr="*")
op_div = Terminal("op_div", r"/", repr="/")
op_igualdade = Terminal("op_igualdade", r"==", repr="==")
op_diferente = Terminal("op_diferente", r"!=", repr="!=")
op_menor_ou_igual = Terminal("op_menor_ou_igual", r"<=", repr="<=")
op_maior_ou_igual = Terminal("op_maior_ou_igual", r">=", repr=">=")
op_menor_que = Terminal("op_menor_que", r"<", repr="<")
op_maior_que = Terminal("op_maior_que", r">", repr=">")
op_modulo = Terminal("op_modulo", r"%", repr="%")
op_e = Terminal("op_e", r"&&", repr="&&")
op_ou = Terminal("op_ou", r"\|\|", repr="||")
op_nao = Terminal("op_nao", r"!", repr="!")
identificador = Terminal("identificador", r"[a-zA-Z_][a-zA-Z_0-9]*")
dois_pontos = Terminal("dois_pontos", r":", repr=":")
ponto_virgula = Terminal("ponto_virgula", r";", repr=";")
ponto = Terminal("ponto", r"\.", repr=".")
virgula = Terminal("virgula", r",", repr=",")
abre_parenteses = Terminal("abre_parenteses", r"\(", repr="(")
fecha_parenteses = Terminal("fecha_parenteses", r"\)", repr=")")
op_atribuicao = Terminal("op_atribuicao", r"=", repr="=")
quebra_linha = Terminal("quebra_linha", r"\n")

terminals = [
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


# --- NAO TERMINAIS DA GRAMATICA ---

Programa = NonTerminal("Programa")
Bloco = NonTerminal("Bloco")
Declaracoes = NonTerminal("Declaracoes")
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
OrExpr = NonTerminal("OrExpr")
OrExprTail = NonTerminal("OrExprTail")
AndExpr = NonTerminal("AndExpr")
AndExprTail = NonTerminal("AndExprTail")
NotExpr = NonTerminal("NotExpr")
AddExpr = NonTerminal("AddExpr")
AddExprTail = NonTerminal("AddExprTail")
MulExpr = NonTerminal("MulExpr")
MulExprTail = NonTerminal("MulExprTail")
UnaryExpr = NonTerminal("UnaryExpr")
Primary = NonTerminal("Primary")

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
    OrExpr,
    OrExprTail,
    AndExpr,
    AndExprTail,
    NotExpr,
    AddExpr,
    AddExprTail,
    MulExpr,
    MulExprTail,
    Primary,
]

# --- PRODUÇÕES DA GRAMATICA ---
productions = [
    # --- Programa ---
    Programa >> [kw_inicio_bloco, Declaracoes, Comandos, kw_fim_bloco],
    # --- Declaracoes ---
    Declaracoes >> [DeclaracaoVariavel, Declaracoes],
    Declaracoes >> [],
    DeclaracaoVariavel >> [kw_var, Tipo, dois_pontos, Identificadores, ponto_virgula],
    Identificadores >> [identificador, IdentificadoresR],
    IdentificadoresR >> [virgula, identificador, Atribuicao, Primary, virgula, Primary],
    IdentificadoresR >> [],
    Atribuicao >> [op_atribuicao],
    Atribuicao >> [virgula, identificador, op_atribuicao, Primary, virgula],
    # --- Tipo ---
    Tipo >> [kw_inteiro],
    Tipo >> [kw_real],
    Tipo >> [kw_texto],
    Tipo >> [kw_logico],
    # --- Comandos ---
    Comandos >> [Comando, Comandos],
    Comandos >> [],
    # --- Comando ---
    Comando >> [Atribuicao],
    Comando >> [Condicional],
    Comando >> [LacoRepeticao],
    Comando >> [Movimento],
    Comando >> [ControleCaneta],
    Comando >> [ControleTela],
    # --- Atribuicao ---
    Atribuicao >> [identificador, op_atribuicao, Expr, ponto_virgula],
    # --- Condicional (SE) ---
    Condicional >> [kw_se, Expr, kw_entao, Comandos, Senao, kw_fim_se, ponto_virgula],
    Senao >> [kw_senao, Comandos],
    Senao >> [],
    # --- LacoRepeticao ---
    LacoRepeticao >> [Repita],
    LacoRepeticao >> [Enquanto],
    # --- LacoRepeticao (Repita) ---
    Repita >> [kw_repita, Expr, kw_vezes, Comandos, kw_fim_repita, ponto_virgula],
    # --- LacoRepeticao (Enquanto) ---
    Enquanto >> [kw_enquanto, Expr, kw_faca, Comandos, kw_fim_enquanto, ponto_virgula],
    # --- Movimento ---
    Movimento >> [cmd_avancar, Expr, ponto_virgula],
    Movimento >> [cmd_recuar, Expr, ponto_virgula],
    Movimento >> [cmd_girar_direita, Expr, ponto_virgula],
    Movimento >> [cmd_girar_esquerda, Expr, ponto_virgula],
    Movimento >> [cmd_ir_para, Expr, Expr, ponto_virgula],
    # --- Controle da caneta ---
    ControleCaneta >> [cmd_levantar_caneta, ponto_virgula],
    ControleCaneta >> [cmd_abaixar_caneta, ponto_virgula],
    ControleCaneta >> [cmd_definir_cor, Expr, ponto_virgula],
    ControleCaneta >> [cmd_definir_espessura, Expr, ponto_virgula],
    # --- Controle de tela ---
    ControleTela >> [cmd_limpar_tela, ponto_virgula],
    ControleTela >> [cmd_cor_de_fundo, Expr, ponto_virgula],
    # --- Expressões --- (Aritméticas e Lógicas)
    Expr >> [OrExpr],
    OrExpr >> [AndExpr, OrExprTail],
    OrExprTail >> [op_ou, AndExpr, OrExprTail],
    OrExprTail >> [],
    AndExpr >> [NotExpr, AndExprTail],
    AndExprTail >> [op_e, NotExpr, AndExprTail],
    AndExprTail >> [],
    NotExpr >> [op_nao, NotExpr],
    NotExpr >> [AddExpr],
    AddExpr >> [MulExpr, AddExprTail],
    AddExprTail >> [op_mais, MulExpr, AddExprTail],
    AddExprTail >> [op_menos, MulExpr, AddExprTail],
    AddExprTail >> [op_igualdade, MulExpr, AddExprTail],
    AddExprTail >> [op_diferente, MulExpr, AddExprTail],
    AddExprTail >> [op_menor_ou_igual, MulExpr, AddExprTail],
    AddExprTail >> [op_maior_ou_igual, MulExpr, AddExprTail],
    AddExprTail >> [op_menor_que, MulExpr, AddExprTail],
    AddExprTail >> [op_maior_que, MulExpr, AddExprTail],
    AddExprTail >> [],
    MulExpr >> [Primary, MulExprTail],
    MulExprTail >> [op_multiplicacao, Primary, MulExprTail],
    MulExprTail >> [op_div, Primary, MulExprTail],
    MulExprTail >> [op_modulo, Primary, MulExprTail],
    MulExprTail >> [],
    Primary >> [abre_parenteses, Expr, fecha_parenteses],
    Primary >> [inteiro],
    Primary >> [identificador],
    Primary >> [real],
    Primary >> [texto],
    Primary >> [logico],
]


grammar = Grammar(
    start_symbol=Programa,
    terminals=terminals,
    non_terminals=non_terminals,
    productions=productions,
)

if __name__ == "__main__":
    print("--------------")
    print("Gramática")
    print("--------------")
    print(grammar)

    text = """
    inicio
        var inteiro : a, b, c = 3, 1, a;
        teste = "teste";
        se 1 * ( verdadeiro  != falso + 12) entao
            // negação
            avancar ! verdadeiro;
            avancar ! (verdadeiro);
            avancar ! (verdadeiro || falso);
            avancar ! (verdadeiro && falso);
            avancar  (verdadeiro == 1);
            
        senao
            girar_direita 10;
        fim_se;
    fim
    """

    tokens = Tokenizer.tokenize(text, grammar)

    print(Fore.RED + "Tokens encontrados:")
    for token in tokens:
        print(Fore.BLUE + token.terminal.name, end=": ")
        print(Fore.YELLOW + token.lexeme)

    ll1_table = LL1Table(grammar)
    ll1_parser_table = LL1ParserTable(ll1_table, Programa)
    parsed = ll1_parser_table.parse(tokens)

    print("-" * 30)

    if parsed:
        print(Fore.GREEN + "Análise sintática bem-sucedida!")
    else:
        print(Fore.RED + "Erro na análise sintática!")
    print("-" * 30)
