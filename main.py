import pygame
import sys # módulo necessário para sair do programa
from settings import * # importa todas as constantes de settings.py
from classes import Elphaba # importa a Elphaba
from classes import Button
from HUD import * # importa todas as funções de HUD.py

pygame.init()

# === CONFIGURAÇÃO DA JANELA ===
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption(título)

# === MUSICAS === 
MUSICA_MENU = 'efeitos sonoros/start.mp3' 
MUSICA_JOGO = 'efeitos sonoros/trilha sonora.mp3' # a trilha do jogo 
musica_atual = None

#=== CARREGAMENTO DO BOTÃO ===
start_button_img = pygame.image.load('imagens/buttons/botao-jogar.png').convert_alpha() 
exit_button_img = pygame.image.load('imagens/buttons/botao-sair.png').convert_alpha()
restart_button_img = pygame.image.load('imagens/buttons/botao-reiniciar.png').convert_alpha() #botão do restart (para o game over)

restart_button = Button(350, 300, restart_button_img, 1)
start_button = Button(500, 350, start_button_img, 1)
exit_button = Button(495, 480, exit_button_img, 1)

# === CARREGAMENTO E CONFIGURAÇÃO DO FUNDO ===
BG1 = pygame.image.load('imagens/backgrounds/fundo-menuprincipal.png')
tela_menu = pygame.transform.scale(BG1, (tela_largura, tela_altura))

BG = pygame.image.load('imagens/backgrounds/emerald-city-path.jpg')
tela_fundo = pygame.transform.scale(BG, (tela_largura, tela_altura))

# === INSTANCIAÇÃO DE OBJETOS (POO) ===
piso_y = tela_altura # define a altura vertical que o player considera como o chão (limite inferior da tela)
elphaba = Elphaba(elph_x, piso_y) # cria o objeto Elphaba
player = pygame.sprite.Group()
player.add(elphaba)
disparo_ataque = pygame.sprite.Group()

# === FUNÇÃO PRA MUSICA === 
def tocar_musica(caminho, volume=0.5):
    pygame.mixer.music.stop() 
    pygame.mixer.music.load(caminho) 
    pygame.mixer.music.set_volume(volume) 
    pygame.mixer.music.play(-1)

# === FUNÇÃO DE RENDERIZAÇÃO (DRAW) ===
def draw():

    tela.blit(tela_fundo, (0, 0)) # desenha a imagem de fundo na posição (0, 0) para cobrir a tela inteira

    player.draw(tela) # desenha a Elphie
    disparo_ataque.draw(tela) # desenha os disparos de feitiços

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

# === Definindo estados ===
MENU = "menu"
JOGANDO = "jogando"
GAME_OVER = "game_over"
estado =  MENU
# === GAME LOOP PRINCIPAL ===
while True:
    for event in pygame.event.get(): # itera sobre todos os eventos registrados pelo Pygame
        if event.type == pygame.QUIT: # fecha o jogo quando o 'X' da janela é clicado
            pygame.quit() # desinicializa todos os módulos do Pygame
            sys.exit() # sai do programa
    
    if estado == MENU:
        tela.blit(tela_menu, (0, 0))

        if musica_atual != MUSICA_MENU:
            tocar_musica(MUSICA_MENU) 
            musica_atual = MUSICA_MENU

        if start_button.desenhar_botao(tela): 
            estado = JOGANDO
            tocar_musica(MUSICA_JOGO)
            musica_atual = MUSICA_JOGO
            tempo_inicial_ms = pygame.time.get_ticks()

        if exit_button.desenhar_botao(tela):
            pygame.quit()
            sys.exit()


    elif estado == JOGANDO:
    
        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicial_ms) / 1000 # calcula o tempo em segundos que passou desde o início
        tempo_restante = tempo_total - tempo_decorrido # timer
        
        if tempo_restante <= 0:
            # LÓGICA DE FIM DE JOGO (GAME OVER)
            estado = GAME_OVER

        player.update(disparo_ataque) # atualização do sprite da Elphaba
        disparo_ataque.update()

        draw()
    
    elif estado == GAME_OVER:
        tela.fill((0, 0, 0))

        desenhar_game_over(tela)

        if restart_button.desenhar_botao(tela):
            estado = MENU
            tempo_inicial_ms = None
            elphaba.reset() 
            disparo_ataque.empty()
        
        if exit_button.desenhar_botao(tela):
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(fps)
    