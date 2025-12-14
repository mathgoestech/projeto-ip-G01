import pygame
import sys
from settings import *
from classes import Elphaba

pygame.init()

# configurações da janela (criação do display e título)
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption(título)

# carrega a imagem do arquivo e redimensiona ela para ter o mesmo tamanho da janela
tela_fundo = pygame.transform.scale(
    pygame.image.load('imagens/backgrounds/red_castle.jpg'),
    (tela_largura, tela_altura)
)

# instanciação de objetos (POO)
piso_y = tela_altura
elphaba = Elphaba(elph_x, piso_y) # cria o objeto, passando os dados de inicialização
all_sprites = pygame.sprite.Group() # forma o grupo de sprites
all_sprites.add(elphaba) # adiciona a Elphaba ao grupo

def draw(): # função de renderização

    # redesenha a imagem de fundo e os sprites, atualizando o novo quadro
    tela.blit(tela_fundo, (0, 0))
    all_sprites.draw(tela)
    pygame.display.update()


# inicializa o player e redimensiona a imagem pra um tamanho adequado
player = pygame.image.load('imagens/sprites/elphaba/elphie-idle.png')
player = pygame.transform.scale(player, (elph_largura, elph_altura))

# controle de tempo (fps)
clock = pygame.time.Clock() # limita a taxa de quadros por segundo

# game loop (roda enquanto o jogo tá aberto)
while True:
    for event in pygame.event.get():
        # clicou no X da janela, fecha o jogo e o programa
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()

    all_sprites.update()
    draw() # chama a função que desenha o cenário e os objetos na tela
    clock.tick(fps) # controle de frame rate (60 fps)