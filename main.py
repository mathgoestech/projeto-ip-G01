import pygame
import sys # módulo necessário para sair do programa
from settings import * # importa todas as constantes de settings.py
from jogador import *
from objetos import *
from HUD import * # importa todas as funções de HUD.py

pygame.init()

# === CONFIGURAÇÃO DA JANELA ===
tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption(título)

# === MUSICAS === 
MUSICA_MENU = 'efeitos_sonoros/start.mp3' 
MUSICA_JOGO = 'efeitos_sonoros/trilha sonora.mp3' #a trilha do jogo 
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
tela_fundo1 = pygame.transform.scale(BG, (tela_largura, tela_altura))
tela_fundo2 = pygame.transform.scale(BG, (tela_largura, tela_altura))
fundos_loop = [tela_fundo, tela_fundo1, tela_fundo2]
fundos_pos = [0, -tela_largura, tela_largura]

# === INSTANCIAÇÃO DE OBJETOS (POO) ===
piso_y = tela_altura # define a altura vertical que o player considera como o chão (limite inferior da tela)
elphaba = Elphaba(elph_x, piso_y) # cria o objeto Elphaba
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

# === FUNÇÃO PRA MUSICA ===
def tocar_musica(caminho):
    pygame.mixer.music.stop()# para a musica atual
    pygame.mixer.music.load(caminho) # troca a musica
    pygame.mixer.music.set_volume(0.5)# volume
    pygame.mixer.music.play(-1) # toca em looping

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
        #por algum motivo o menu não tava renderizando as imagens, então eu tentei consertar????
        tela.blit(tela_menu, (0, 0))
        tela.blit(exit_button_img, (495, 480))
        tela.blit(start_button_img, (500, 350))
        pygame.display.update()

        if musica_atual != MUSICA_MENU: 
            tocar_musica(MUSICA_MENU) 
            musica_atual = MUSICA_MENU

    if start_button.desenhar_botao(tela): 
        estado = JOGANDO 
        tocar_musica(MUSICA_JOGO) 
        musica_atual = MUSICA_JOGO 
        tempo_inicial_ms = pygame.time.get_ticks() # agora zera o cronômetro quando o jogo começa # agora zera o cronômetro quando o jogo começa

    if exit_button.desenhar_botao(tela):
        pygame.quit()
        sys.exit()

    elif estado == JOGANDO:
    
        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicial_ms) / 1000 # calcula o tempo em segundos que passou desde o início
        tempo_restante = tempo_total - tempo_decorrido # timer
        
        if tempo_restante <= 0:
            # LÓGICA DE FIM DE JOGO (GAME OVER)
            estado = GAME_OVER

        camera[0] += (elphaba.rect.centerx - tela_largura / 2.5 - camera[0])
        camera[1] += (elphaba.rect.centery - tela_altura / 1.26 - camera[1])
        render_camera = (int(camera[0]), int(camera[1]))

        is_moving, direction = elphaba.is_moving, elphaba.direction
        if is_moving:
            scroller -= direction * elphaba.speed

        if scroller < -tela_largura or scroller > tela_largura:
            scroller = 0

        draw(scroller=scroller)
    
    elif estado == GAME_OVER:
        tela.fill((0, 0, 0))