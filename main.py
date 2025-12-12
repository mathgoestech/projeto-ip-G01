import pygame
import sys
from settings import *

pygame.init()

# configurações da janela (criação do display e título)
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption(título)

# carrega a imagem do arquivo e redimensiona ela para ter o mesmo tamanho da janela
tela_fundo = pygame.transform.scale(
    pygame.image.load('imagens/backgrounds/red_castle.jpg'),
    (tela_largura, tela_altura)
)

def draw(player, x, y): # função de renderização

    # redesenha a imagem de fundo e a Elphaba na sua posição atual, atualizando o novo quadro
    tela.blit(tela_fundo, (0, 0))
    tela.blit(player, (x, y))
    pygame.display.update()


# inicializa o player e redimensiona a imagem pra um tamanho adequado
player = pygame.image.load('imagens/sprites/elphaba/elphie-idle.png')
player = pygame.transform.scale(player, (elph_largura, elph_altura))

# controle de tempo (fps)
clock = pygame.time.Clock() # limita a taxa de quadros por segundo

# variáveis de controle do pulo
elph_pula = False
velocidade_pulo = pulo_altura # velocidade vertical atual

# game loop (roda enquanto o jogo tá aberto)
while True:
    for event in pygame.event.get():
        # clicou no X da janela, fecha o jogo e o programa
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()

    keys = pygame.key.get_pressed() # verifica quais teclas estão sendo pressionadas

    # movimentação horizontal
    if keys[pygame.K_LEFT]:
        elph_x -= elph_velocidade # decrementa x, movendo para a esquerda
    if keys[pygame.K_RIGHT]:
        elph_x += elph_velocidade # incrementa x, movendo para a direita

    # mecânica do pulo
    if keys[pygame.K_UP] and not elph_pula:
        elph_pula = True # ativa o estado de pulo

    # física do pulo
    if elph_pula:
        elph_y -= velocidade_pulo # altera a coordenada y, movendo objeto/player para cima
        velocidade_pulo -= gravidade # aplica a gravidade, desacelerando a velocidade do pulo na subida
        if velocidade_pulo < -pulo_altura: # termina quando a velocidade do pulo atinge o valor inicial de subida
            piso = tela_altura - elph_altura
            elph_y = piso
            elph_pula = False
            velocidade_pulo = pulo_altura # reseta a velocidade para o próximo pulo

    draw(player, elph_x, elph_y) # chama a função que desenha o cenário e os objetos na tela
    clock.tick(60) # controle de frame rate (60 fps)