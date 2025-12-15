import pygame
import sys # módulo necessário para sair do programa
from settings import * # importa todas as constantes de settings.py
from classes import Elphaba # importa apenas a classe do player (por enquanto)
from HUD import * # importa todas as funções de HUD.py

pygame.init()

# === CONFIGURAÇÃO DA JANELA ===
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption(título)

# === CARREGAMENTO E CONFIGURAÇÃO DO FUNDO ===
BG = pygame.image.load('imagens/backgrounds/emerald-city-path.jpg')
tela_fundo = pygame.transform.scale(BG, (tela_largura, tela_altura))

# === INSTANCIAÇÃO DE OBJETOS (POO) ===
piso_y = tela_altura # define a altura vertical que o player considera como o chão (limite inferior da tela)
elphaba = Elphaba(elph_x, piso_y) # cria o objeto Elphaba, passando os dados de inicialização
player = pygame.sprite.Group()
player.add(elphaba)

# === FUNÇÃO DE RENDERIZAÇÃO (DRAW) ===
def draw():

    tela.blit(tela_fundo, (0, 0)) # desenha a imagem de fundo na posição (0, 0) para cobrir a tela inteira

    player.draw(tela) # desenha a Elphie

    # HUD: chamadas para desenhar os elementos da interface
    desenhar_vida(tela, elphaba)
    desenhar_mana(tela, elphaba)
    desenhar_timer(tela, tempo_restante)
    desenhar_contadores(tela, elphaba)

    pygame.display.update() # atualiza o conteúdo da tela inteira, mostrando o novo frame

# === INICIALIZAÇÃO DO TEMPO E CONTROLE DE LOOP ===
tempo_total = 120 # duração total do jogo em segundos (2 minutos - ajuste se necessário)
tempo_inicial_ms = pygame.time.get_ticks() # registra o tempo em milissegundos a partir do início do loop
clock = pygame.time.Clock() # limita a taxa de quadros por segundo

# === GAME LOOP PRINCIPAL ===
while True:
    for event in pygame.event.get(): # itera sobre todos os eventos registrados pelo Pygame
        if event.type == pygame.QUIT: # fecha o jogo quando o 'X' da janela é clicado
            pygame.quit() # desinicializa todos os módulos do Pygame
            sys.exit() # sai do programa
    
    tempo_decorrido = (pygame.time.get_ticks() - tempo_inicial_ms) / 1000 # calcula o tempo em segundos que passou desde o início
    tempo_restante = tempo_total - tempo_decorrido # timer
    
    if tempo_restante <= 0:
        # LÓGICA DE FIM DE JOGO (GAME OVER)
        pass

    player.update() # atualização do sprite da Elphaba

    draw()
    clock.tick(fps) # limita o loop para rodar em 60 fps