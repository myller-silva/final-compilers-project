import turtle
#---Configuração Padrão --
screen = turtle.Screen()
t = turtle.Turtle()
screen.title('Resultado-Exemplo 3')
#--- Codigo Gerado pelo Compilador--
lado = 0
cor = ""
lado = 5
screen.bgcolor("black")
t.width(2)
for _ in range(50):
    t.color("cyan")
    t.forward(lado)
    t.right(90)
    lado = (lado + 5)
#--- Finalizacao--
turtle.done()