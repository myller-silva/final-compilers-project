from table_parser_ll1 import Terminal, NonTerminal, Grammar

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

# NOTE: Novo comando adicionado
cmd_definir_velocidade = Terminal("cmd_definir_velocidade", r"\b(definir_velocidade)\b") 
# NOTE: Novo comando adicionado
cmd_desenhar_circulo = Terminal("cmd_desenhar_circulo", r"\b(desenhar_circulo)\b") 

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
    # NOTE: Novo comando adicionado
    cmd_definir_velocidade,
    # NOTE: Novo comando adicionado
    cmd_desenhar_circulo,
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

Program = NonTerminal("Program")
Declarations = NonTerminal("Declarations")
VariableDeclaration = NonTerminal("VariableDeclaration")
AssignVariable = NonTerminal("AssignVariable")
Identifiers = NonTerminal("Identifiers")
IdentifiersR = NonTerminal("IdentifiersR")
IdentifiersAssignment = NonTerminal("IdentifiersAssignment")
IdentifiersAssignmentR = NonTerminal("IdentifiersAssignmentR")
Commands = NonTerminal("Commands")
Command = NonTerminal("Command")
AssignValue = NonTerminal("AssignValue")
Conditional = NonTerminal("Conditional")
Else = NonTerminal("Else")
Loop = NonTerminal("Loop")
Repeat = NonTerminal("Repeat")
While = NonTerminal("While")
Movement = NonTerminal("Movement")
PenControl = NonTerminal("PenControl")
ScreenControl = NonTerminal("ScreenControl")
Type = NonTerminal("Type")

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
    Program,
    Declarations,
    VariableDeclaration,
    AssignVariable,
    Identifiers,
    IdentifiersR,
    IdentifiersAssignment,
    IdentifiersAssignmentR,
    Commands,
    Command,
    AssignValue,
    Conditional,
    Else,
    Loop,
    Repeat,
    While,
    Movement,
    PenControl,
    ScreenControl,
    Type,
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
    # --- Program ---
    Program >> [kw_inicio_bloco, Declarations, Commands, kw_fim_bloco],
    # --- Declarations ---
    Declarations >> [VariableDeclaration, Declarations],
    Declarations >> [],
    VariableDeclaration >> [kw_var, Type, AssignVariable, ponto_virgula],
    AssignVariable >> [dois_pontos, Identifiers, IdentifiersAssignment],
    Identifiers >> [identificador, IdentifiersR],
    IdentifiersR >> [virgula, identificador, IdentifiersR],
    IdentifiersR >> [],
    IdentifiersAssignment >> [op_atribuicao, Expr, IdentifiersAssignmentR],
    IdentifiersAssignment >> [],
    IdentifiersAssignmentR >> [virgula, Expr, IdentifiersAssignmentR],
    IdentifiersAssignmentR >> [],
    # --- Type ---
    Type >> [kw_inteiro],
    Type >> [kw_real],
    Type >> [kw_texto],
    Type >> [kw_logico],
    # --- Commands ---
    Commands >> [Command, Commands],
    Commands >> [],
    # --- Command ---
    Command >> [AssignValue],
    Command >> [Conditional],
    Command >> [Loop],
    Command >> [Movement],
    Command >> [PenControl],
    Command >> [ScreenControl],
    # --- AssignValue ---
    AssignValue >> [identificador, op_atribuicao, Expr, ponto_virgula],
    # --- Conditional (SE) ---
    Conditional >> [kw_se, Expr, kw_entao, Commands, Else, kw_fim_se, ponto_virgula],
    Else >> [kw_senao, Commands],
    Else >> [],
    # --- Loop ---
    Loop >> [Repeat],
    Loop >> [While],
    # --- Loop (Repeat) ---
    Repeat >> [kw_repita, Expr, kw_vezes, Commands, kw_fim_repita, ponto_virgula],
    # --- Loop (While) ---
    While >> [kw_enquanto, Expr, kw_faca, Commands, kw_fim_enquanto, ponto_virgula],
    # --- Movement ---
    Movement >> [cmd_avancar, Expr, ponto_virgula],
    Movement >> [cmd_recuar, Expr, ponto_virgula],
    Movement >> [cmd_girar_direita, Expr, ponto_virgula],
    Movement >> [cmd_girar_esquerda, Expr, ponto_virgula],
    Movement >> [cmd_ir_para, Expr, Expr, ponto_virgula],
    # NOTE: Novo comando adicionado
    Movement >> [cmd_desenhar_circulo, Expr, ponto_virgula],
    # --- PenControl ---
    PenControl >> [cmd_levantar_caneta, ponto_virgula],
    PenControl >> [cmd_abaixar_caneta, ponto_virgula],
    PenControl >> [cmd_definir_cor, Expr, ponto_virgula],
    PenControl >> [cmd_definir_espessura, Expr, ponto_virgula],
    # NOTE: Novo comando adicionado
    PenControl >> [cmd_definir_velocidade, Expr, ponto_virgula], 
    # --- ScreenControl ---
    ScreenControl >> [cmd_limpar_tela, ponto_virgula],
    ScreenControl >> [cmd_cor_de_fundo, Expr, ponto_virgula],
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
    start_symbol=Program,
    terminals=terminals,
    non_terminals=non_terminals,
    productions=productions,
)
