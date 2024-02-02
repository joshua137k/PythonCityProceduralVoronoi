

import pygame
import re

# Inicialize o Pygame
pygame.init()

# Crie a janela/tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Desenho de Pontos")

# Abra o arquivo e encontre os pontos
with open("roads.txt", "r") as f:
    conteudo = f.read()
conteudo=conteudo.replace("array","")
roads = eval(conteudo)


l =""
for i in roads:
	a = str(i[0])
	b=str(i[1])

	a=a.replace("[","Vector2(").replace("]",")")
	b=b.replace("[","Vector2(").replace("]",")")
	c="["+a+"/"+b+"]"
	

	l+= c+"%"


l=l[:-1]

f = open("ro.txt","w")
f.write(l)
f.close()



font = pygame.font.Font(None, 36)  # Escolha a fonte e o tamanho desejados


def draw_voronoi_line(screen, start_point, end_point, color):
    pygame.draw.line(screen, color, start_point, end_point)


# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpe a tela
    tela.fill((255, 255, 255))

    # Desenhe linhas entre os pontos
    if len(roads) >= 2:
        for i,road in enumerate(roads):
            draw_voronoi_line(tela, road[0], road[1], (0,0,0))


    # Atualize a tela
    pygame.display.flip()

# Encerre o Pygame
pygame.quit()