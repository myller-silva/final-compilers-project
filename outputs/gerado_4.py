import turtle
#---Configuração Padrão --
screen = turtle.Screen()
t = turtle.Turtle()
screen.title('Resultado-Exemplo 4')
#--- Codigo Gerado pelo Compilador--
velocidade = 0
contador = 0
raio_atual = 0.0
velocidade = 1
raio_atual = 120.0
contador = 0
screen.bgcolor("black")
t.width(2)
t.penup()
t.goto(0, 0)
t.pendown()
for _ in range(21):
    t.speed(velocidade)
    if ((contador % 2) == 0):
        t.color("red")
    else:
        t.color("white")
    t.circle(raio_atual)
    raio_atual = (raio_atual - 12.0)
    contador = (contador + 1)
    velocidade = (velocidade + 2)
#--- Finalizacao--
turtle.done()