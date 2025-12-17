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

#=== CARREGAMENTO DO BOTÃO ===
start_button_img = pygame.image.load('imagens/buttons/start_button.png').convert_alpha() # o convert_alpha otimiza a imagem e mantém transparência
exit_button_img = pygame.image.load('imagens/buttons/exit_button.png').convert_alpha()
restart_button_img = pygame.image.load('imagens/buttons/restart_button.png').convert_alpha() #botão do restart (para o game over)

restart_button = Button(350, 300, restart_button_img, 0.5)
start_button = Button(350, 300, start_button_img, 0.5)
exit_button = Button(500, 300, exit_button_img, 0.5)

# === CARREGAMENTO E CONFIGURAÇÃO DO FUNDO ===
BG1 = pygame.image.load('imagens/backgrounds/fundocastelo.jpg')
tela_menu = pygame.transform.scale(BG1, (tela_largura, tela_altura))

BG = pygame.image.load('imagens/backgrounds/emerald-city-path.jpg')
tela_fundo = pygame.transform.scale(BG, (tela_largura, tela_altura))
tela_fundo1 = pygame.transform.scale(BG, (tela_largura, tela_altura))
tela_fundo2 = pygame.transform.scale(BG, (tela_largura, tela_altura))
fundos_loop = [tela_fundo, tela_fundo1, tela_fundo2]
fundos_pos = [0, -tela_largura, tela_largura]

# === INSTANCIAÇÃO DE OBJETOS (POO) ===
piso_y = tela_altura # define a altura vertical que o player considera como o chão (limite inferior da tela)
elphaba = Elphaba(elph_x, piso_y) # cria o objeto Elphaba, passando os dados de inicialização
player = pygame.sprite.Group()
player.add(elphaba)
disparo_ataque = pygame.sprite.Group()
camera = [0, 0] # posição inicial da câmera
scroller = 0

# === FUNÇÃO DE RENDERIZAÇÃO (DRAW) ===
def draw(scroller=scroller):

    for i in range(3):

        tela.blit(fundos_loop[i], (fundos_pos[i] + scroller, 0 - camera[1]))

    
    player.update(disparo_ataque) # atualização do sprite da Elphaba
    disparo_ataque.update()
    elphaba.render(tela, offset=render_camera) # desenha a Elphaba na tela com o offset da câmera
    # Desenha os ataques na tela com o offset da câmera
    for ataque in disparo_ataque:
        tela.blit(ataque.image, (ataque.rect.x - render_camera[0], ataque.rect.y - render_camera[1]))

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

        if start_button.desenhar_botao(tela):
            estado = JOGANDO 
            tempo_inicial_ms = pygame.time.get_ticks() # agora zera o cronômetro quando o jogo começa

        if exit_button.desenhar_botao(tela):
            pygame.quit()
            sys.exit()


    elif estado == JOGANDO:
    
        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicial_ms) / 1000 # calcula o tempo em segundos que passou desde o início
        tempo_restante = tempo_total - tempo_decorrido # timer

        camera[0] += (elphaba.rect.centerx - tela_largura / 4 - camera[0])
        camera[1] += (elphaba.rect.centery - tela_altura/1.33 - camera[1])
        render_camera = (int(camera[0]), int(camera[1]))

        if tempo_restante <= 0:
            # LÓGICA DE FIM DE JOGO (GAME OVER)
            estado = GAME_OVER

        is_moving, direction = elphaba.is_moving, elphaba.direction
        if is_moving:
            scroller -= direction * elphaba.speed

        if scroller < -tela_largura or scroller > tela_largura:
            scroller = 0

        draw(scroller=scroller)

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
    