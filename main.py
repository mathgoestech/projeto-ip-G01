import pygame
import sys

pygame.init()

# configurações da janela (resolução)
largura, altura = 1000, 600 # dimensões da janela em pixels
tela = pygame.display.set_mode((largura, altura)) # cria e exibe a janela principal do jogo
pygame.display.set_caption('Resgate RelâmpagOZ') # define o título que aparece na barra superior da janela

# propriedades base do objeto/player (elphaba)
largura_elph = 100
altura_elph = 200
velocidade_elph = 7 # determina o quão rápida a elphaba se move (velocidade horizontal em pixels/frame)

# carrega a imagem do arquivo e redimensiona ela para ter o mesmo tamanho da janela
tela_fundo = pygame.transform.scale(pygame.image.load('red_castle.jpg'), (largura, altura))

def draw(player): # função de renderização
    
    tela.blit(tela_fundo, (0, 0)) # desenha a imagem de fundo, limpando o rastro de movimentação
    pygame.draw.rect(tela, 'green', player) # desenha a elphaba (retângulo verde) na sua posição atual
    pygame.display.update() # atualiza o novo quadro renderizado para o monitor

def main():
    # inicializa o player
    player = pygame.Rect(200, altura - altura_elph, largura_elph, altura_elph) # posição inicial: x = 200, y = altura - altura_elph (coloca a base do objeto no "chão")

    # controle de tempo (fps)
    clock = pygame.time.Clock() # limita a taxa de quadros por segundo

    # variáveis de controle do pulo
    elph_pula = False
    gravidade = 1 # aceleração vertical em pixels/frame
    altura_pulo = 20 # altura máxima do pulo em pixels
    velocidade_pulo = altura_pulo # velocidade vertical atual

    # game loop (roda enquanto o jogo tá aberto)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # clicou no X da janela
                pygame.quit() # encerra o pygame
                sys.exit() # fecha o programa completamente

        keys = pygame.key.get_pressed() # verifica quais teclas estão sendo pressionadas

        # movimentação horizontal
        if keys[pygame.K_LEFT]:
            player.x -= velocidade_elph # decrementa x, movendo para a esquerda
        if keys[pygame.K_RIGHT]:
            player.x += velocidade_elph # incrementa x, movendo para a direita

        # mecanica do pulo
        if keys[pygame.K_UP] and not elph_pula:
            elph_pula = True # ativa o estado de pulo

        # física do pulo
        if elph_pula:
            player.y -= velocidade_pulo # altera a coordenada y, movendo objeto/player para cima
            velocidade_pulo -= gravidade # aplica a gravidade, desacelerando a velocidade do pulo na subida
            if velocidade_pulo < -altura_pulo: # termina quando a velocidade do pulo atinge o valor inicial de subida
                piso = altura - altura_elph
                player.y = piso
                elph_pula = False
                velocidade_pulo = altura_pulo # reseta a velocidade para o próximo pulo

        draw(player) # chama a função que desenha o cenário e os objetos na tela
        clock.tick(60) # controle de frame rate (60 fps)

# início do programa
if __name__ == '__main__':
    main()
