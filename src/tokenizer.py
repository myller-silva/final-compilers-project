# Tokenizador para a linguagem TurtleScript
import re
from constants import *


class Tokenizer:
    def __init__(self, source_code: str):
        """
        Inicializa o tokenizador com o código-fonte.

        Args:
            source_code: Código-fonte da linguagem TurtleScript.
        """
        self.source_code = source_code
        self.tokens: list[tuple[str, str]] = []

        # Definição dos padrões de tokenização
        self.token_patterns: list[tuple[str, str]] = [
            (
                COMENTARIO,
                r"//.*",
            ),  # Comentários (início com // e vão até o final da linha)
            # PALAVRAS-CHAVE
            (KW_VAR, r"\bvar\b"),
            (KW_INTEIRO, r"\binteiro\b"),
            (KW_REAL, r"\breal\b"),
            (KW_TEXTO, r"\btexto\b"),
            (KW_LOGICO, r"\blogico\b"),
            # SE
            (KW_SE, r"\bse\b"),
            (KW_FIM_SE, r"\bfim_se\b"),
            (KW_ENTAO, r"\bentao\b"),
            (KW_SENAO, r"\bsenao\b"),
            # ENQUANTO
            (KW_ENQUANTO, r"\benquanto\b"),
            (KW_FACA, r"\bfaca\b"),
            (KW_FIM_ENQUANTO, r"\bfim_enquanto\b"),
            # REPITA
            (KW_REPITA, r"\brepita\b"),
            (KW_VEZES, r"\bvezes\b"),
            (KW_FIM_REPITA, r"\bfim_repita\b"),
            # BLOCO
            (KW_INICIO_BLOCO, r"inicio"),
            (KW_FIM_BLOCO, r"fim"),
            # MOVIMENTO
            (CMD_AVANCAR, r"\b(avancar)\b"),
            (CMD_RECUAR, r"\b(recuar)\b"),
            (CMD_GIRAR_DIREITA, r"\b(girar_direita)\b"),
            (CMD_GIRAR_ESQUERDA, r"\b(girar_esquerda)\b"),
            (CMD_IRPARA, r"\b(ir_para)\b"),
            # CONTROLE DA CANETA
            (CMD_LEVANTAR_CANETA, r"\b(levantar_caneta)\b"),
            (CMD_ABAIXAR_CANETA, r"\b(abaixar_caneta)\b"),
            (CMD_DEFINIR_COR, r"\b(definir_cor)\b"),
            (CMD_DEFINIR_ESPESSURA, r"\b(definir_espessura)\b"),
            # CONTROLE DE TELA
            (CMD_LIMPAR_TELA, r"\b(limpar_tela)\b"),
            (CMD_COR_DE_FUNDO, r"\b(cor_de_fundo)\b"),
            # TIPOS DE DADOS
            (REAL, r"\d+\.\d+"),
            (INTEIRO, r"\d+"),
            (TEXTO, r'"[^"]*"'),
            (LOGICO, r"\b(verdadeiro|falso)\b"),
            # OPERADORES
            (OP_MAIS, r"\+"),
            (OP_MENOS, r"-"),
            (OP_MULTIPLICACAO, r"\*"),
            (OP_DIVISAO, r"/"),
            (OP_IGUALDADE, r"=="),
            (OP_DIFERENTE, r"!="),
            (OP_MENOR_OU_IGUAL, r"<="),
            (OP_MAIOR_OU_IGUAL, r">="),
            (OP_MENOR_QUE, r"<"),
            (OP_MAIOR_QUE, r">"),
            (OP_MODULO, r"%"),
            # OUTROS TOKENS
            (IDENTIFICADOR, r"[a-zA-Z_][a-zA-Z_0-9]*"),
            (DOIS_PONTOS, r":"),
            (PONTO_VIRGULA, r";"),
            (VIRGULA, r","),
            (PONTO, r"\."),
            (ABRE_PARENTESES, r"\("),
            (FECHA_PARENTESES, r"\)"),
            (OP_ATRIBUICAO, r"="),
            (QUEBRA_LINHA, r"\n"),
            (ESPACO, r"[ \t]+"),
        ]

    def tokenize(self) -> list[tuple[str, str]]:
        """
        Realiza a tokenização do código-fonte.

        Returns:
            Lista de tokens gerados a partir do código-fonte.

        Raises:
            RuntimeError: Se ocorrer um erro de tokenização.
        """
        # Compilação dos padrões
        token_regex = "|".join(
            f"(?P<{pair[0]}>{pair[1]})" for pair in self.token_patterns
        )
        match_token = re.compile(token_regex).match

        # Tokenização
        line_number = 1
        position = 0

        while position < len(self.source_code):
            match = match_token(self.source_code, position)
            if match is None:
                raise RuntimeError(
                    f"Erro de tokenização na linha {line_number} posição {position}"
                )
            position = match.end()
            token_type = match.lastgroup
            token_value = match.group(token_type)

            if token_type == "ESPACO":  # Ignora espaços e tabulações
                continue
            elif token_type == "COMENTARIO":  # Ignora comentários
                continue
            if (
                token_type == "QUEBRA_LINHA"
            ):  # Ignora quebras de linha e continua a contagem de linhas
                line_number += 1
            else:
                self.tokens.append((token_type, token_value))

        return self.tokens


if __name__ == "__main__":
    # Exemplo de uso (item 4.4 do enunciado do trabalho)
    source_code = """
    inicio
    var inteiro : passo , repeticoes ;
    var texto : cor_fundo , cor_linha , titulo ;
    var real : angulo_preciso ;
    var logico : desenhar_forma ;
    passo = 150;
    repeticoes = 5;
    titulo = "Desenho de uma Estrela";
    cor_fundo = "black";
    cor_linha = "blue";
    angulo_preciso = 144.0;
    desenhar_forma = verdadeiro ;
    fim
    """
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()
    print("Tokens encontrados:")
    for token in tokens:
        print(token)
