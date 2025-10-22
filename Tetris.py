#antes de rodar o codigo siga o seguinte passo a passo
#1 - instale o python na sua maquina https://www.python.org/downloads/
#2 - instale a biblioteca pygame rodando o comando no terminal: pip install pygame

import pygame
import random

# Inicializa o Pygame
pygame.init()

# Tela
LARGURA = 450
ALTURA = 600
TAMANHO_BLOCO = 30
COLUNAS = 10
LINHAS = 20

# Tamanhos
AREA_JOGO = (TAMANHO_BLOCO * COLUNAS, TAMANHO_BLOCO * LINHAS)
AREA_TELA = (LARGURA, ALTURA)

# Cores
PRETO = (0, 0, 0)
CINZA = (50, 50, 50)
BRANCO = (255, 255, 255)
CORES = [
    (0, 255, 255),   # I
    (0, 0, 255),     # J
    (255, 165, 0),   # L
    (255, 255, 0),   # O
    (0, 255, 0),     # S
    (128, 0, 128),   # T
    (255, 0, 0)      # Z
]

# Peças
PEÇAS = [
    [[1, 1, 1, 1]],                             # I
    [[1, 0, 0], [1, 1, 1]],                     # J
    [[0, 0, 1], [1, 1, 1]],                     # L
    [[1, 1], [1, 1]],                           # O
    [[0, 1, 1], [1, 1, 0]],                     # S
    [[0, 1, 0], [1, 1, 1]],                     # T
    [[1, 1, 0], [0, 1, 1]]                      # Z
    # Peça U removida para não causar erro
]

tela = pygame.display.set_mode(AREA_TELA)
pygame.display.set_caption("Tetris V3")

# Grade vazia
def criar_grade():
    return [[PRETO for _ in range(COLUNAS)] for _ in range(LINHAS)]

# Peça
class Peca:
    def __init__(self, shape):  # Corrigido o nome do método para o construtor padrão
        self.shape = shape
        self.cor = random.choice(CORES)
        self.x = COLUNAS // 2 - len(shape[0]) // 2
        self.y = 0

    def girar(self):
        self.shape = [list(l) for l in zip(*self.shape[::-1])]

# Desenha a tela
def desenhar(tela, grade, peca, proxima, score):
    tela.fill(PRETO)

    # Grade
    for i in range(LINHAS):
        for j in range(COLUNAS):
            pygame.draw.rect(tela, grade[i][j],
                             (j * TAMANHO_BLOCO, i * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 0)

    # Peça atual
    for i, linha in enumerate(peca.shape):
        for j, bloco in enumerate(linha):
            if bloco:
                pygame.draw.rect(
                    tela,
                    peca.cor,
                    ((peca.x + j) * TAMANHO_BLOCO, (peca.y + i) * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
                )

    # Linhas da grade
    for i in range(LINHAS):
        pygame.draw.line(tela, CINZA, (0, i * TAMANHO_BLOCO), (AREA_JOGO[0], i * TAMANHO_BLOCO))
    for j in range(COLUNAS):
        pygame.draw.line(tela, CINZA, (j * TAMANHO_BLOCO, 0), (j * TAMANHO_BLOCO, AREA_JOGO[1]))

    # Próxima peça
    desenhar_proxima_peca(tela, proxima)

    # Pontuação
    fonte = pygame.font.SysFont("arial", 24)
    texto = fonte.render(f"Pontos: {score}", True, BRANCO)
    tela.blit(texto, (AREA_JOGO[0] + 20, 200))

    pygame.display.update()

def desenhar_proxima_peca(tela, peca):
    fonte = pygame.font.SysFont("arial", 20)
    texto = fonte.render("Próxima:", True, BRANCO)
    tela.blit(texto, (AREA_JOGO[0] + 20, 20))
    for i, linha in enumerate(peca.shape):
        for j, bloco in enumerate(linha):
            if bloco:
                pygame.draw.rect(
                    tela,
                    peca.cor,
                    (AREA_JOGO[0] + 20 + j * TAMANHO_BLOCO, 50 + i * TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO)
                )

def colidiu(peca, grade):
    for i, linha in enumerate(peca.shape):
        for j, bloco in enumerate(linha):
            if bloco:
                x = peca.x + j
                y = peca.y + i
                if x < 0 or x >= COLUNAS or y >= LINHAS:
                    return True
                if y >= 0 and grade[y][x] != PRETO:
                    return True
    return False

def fixar(peca, grade):
    for i, linha in enumerate(peca.shape):
        for j, bloco in enumerate(linha):
            if bloco:
                grade[peca.y + i][peca.x + j] = peca.cor

def limpar_linhas(grade):
    nova = [linha for linha in grade if any(cor == PRETO for cor in linha)]
    linhas_removidas = LINHAS - len(nova)
    for _ in range(linhas_removidas):
        nova.insert(0, [PRETO for _ in range(COLUNAS)])
    return nova, linhas_removidas

# Principal
def main():
    grade = criar_grade()
    relogio = pygame.time.Clock()
    queda = 0
    velocidade_normal = 0.5
    velocidade = velocidade_normal

    peca_atual = Peca(random.choice(PEÇAS))
    proxima_peca = Peca(random.choice(PEÇAS))
    score = 0
    rodando = True

    pressionado_desde = {}
    REPETICAO_DELAY = 500
    REPETICAO_INTERVAL = 50
    ultimo_movimento = {"esquerda": 0, "direita": 0, "baixo": 0}

    while rodando:
        tempo_passado = relogio.tick(60) / 1000
        queda += tempo_passado
        teclas = pygame.key.get_pressed()
        agora = pygame.time.get_ticks()

        # Movimento contínuo
        if teclas[pygame.K_LEFT]:
            if pygame.K_LEFT not in pressionado_desde:
                pressionado_desde[pygame.K_LEFT] = agora
                peca_atual.x -= 1
                if colidiu(peca_atual, grade):
                    peca_atual.x += 1
                ultimo_movimento["esquerda"] = agora
            else:
                duracao = agora - pressionado_desde[pygame.K_LEFT]
                if duracao > REPETICAO_DELAY and agora - ultimo_movimento["esquerda"] > REPETICAO_INTERVAL:
                    peca_atual.x -= 1
                    if colidiu(peca_atual, grade):
                        peca_atual.x += 1
                    ultimo_movimento["esquerda"] = agora
        else:
            pressionado_desde.pop(pygame.K_LEFT, None)

        if teclas[pygame.K_RIGHT]:
            if pygame.K_RIGHT not in pressionado_desde:
                pressionado_desde[pygame.K_RIGHT] = agora
                peca_atual.x += 1
                if colidiu(peca_atual, grade):
                    peca_atual.x -= 1
                ultimo_movimento["direita"] = agora
            else:
                duracao = agora - pressionado_desde[pygame.K_RIGHT]
                if duracao > REPETICAO_DELAY and agora - ultimo_movimento["direita"] > REPETICAO_INTERVAL:
                    peca_atual.x += 1
                    if colidiu(peca_atual, grade):
                        peca_atual.x -= 1
                    ultimo_movimento["direita"] = agora
        else:
            pressionado_desde.pop(pygame.K_RIGHT, None)

        if teclas[pygame.K_DOWN]:
            if pygame.K_DOWN not in pressionado_desde:
                pressionado_desde[pygame.K_DOWN] = agora
                peca_atual.y += 1
                if colidiu(peca_atual, grade):
                    peca_atual.y -= 1
                ultimo_movimento["baixo"] = agora
            else:
                duracao = agora - pressionado_desde[pygame.K_DOWN]
                if duracao > REPETICAO_DELAY and agora - ultimo_movimento["baixo"] > REPETICAO_INTERVAL:
                    peca_atual.y += 1
                    if colidiu(peca_atual, grade):
                        peca_atual.y -= 1
                    ultimo_movimento["baixo"] = agora
        else:
            pressionado_desde.pop(pygame.K_DOWN, None)

        if queda >= velocidade:
            peca_atual.y += 1
            if colidiu(peca_atual, grade):
                peca_atual.y -= 1
                fixar(peca_atual, grade)
                grade, linhas = limpar_linhas(grade)
                if linhas > 0:
                    score += 100 * linhas
                peca_atual = proxima_peca
                proxima_peca = Peca(random.choice(PEÇAS))
                if colidiu(peca_atual, grade):
                    print("Game Over")
                    rodando = False
            queda = 0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    peca_atual.girar()
                    if colidiu(peca_atual, grade):
                        for _ in range(3):
                            peca_atual.girar()

        desenhar(tela, grade, peca_atual, proxima_peca, score)

    pygame.quit()

main()