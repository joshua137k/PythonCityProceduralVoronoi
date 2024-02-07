import pygame
import math
# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Tamanho da tela
LARGURA, ALTURA = 800, 600

# Inicialize o Pygame
pygame.init()

def distancia_euclidiana(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

 
def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "r") as f:
            conteudo = f.read()
            return eval(conteudo)
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return []


def main():
    # Crie a janela/tela
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Desenho de Pontos")

    # Leitura do arquivo e ordenação dos pontos
    roads = ler_arquivo("roads.txt")
    if not roads:
        return

    # Inicialização do arquivo de saída
    l = "{"
    for i,road in enumerate(roads):
        l +=str(i)+":["
        for r in road:
            a = "'Vector2({},{})'".format(r[0][0], r[0][1])
            b = "'Vector2({},{})'".format(r[1][0], r[1][1])
            c = "[{},{}]".format(a, b)
            l += c + ","
        l = l[:-1]
        l +="],"
    l = l[:-1]
    l+="}"



    with open("teste/ro.txt", "w") as f:
        f.write(l)

    # Fonte
    font = pygame.font.Font(None, 36)

    # Loop principal do jogo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Limpe a tela

        tela.fill(BRANCO)

    # Desenhe linhas entre os pontos
        for road in roads:
            for r in road:
                pygame.draw.line(tela, PRETO ,r[0], r[1])

    # Atualize a tela
        pygame.display.flip()

    # Encerre o Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
