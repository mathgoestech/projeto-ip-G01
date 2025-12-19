import pygame
import sys # módulo necessário para sair do programa
from settings import * # importa todas as constantes de settings.py
from jogador import *
from objetos import *
from HUD import * # importa todas as funções de HUD.py
from mapa import Mapa # importa o mapa

pygame.init()

# === CONFIGURAÇÃO DA JANELA ===
tela = pygame.display.set_mode((tela_largura, tela_altura), pygame.SCALED | pygame.RESIZABLE, vsync=1)
pygame.display.set_caption(título)

# === MUSICAS === 
MUSICA_MENU = 'efeitos_sonoros/start.mp3' 
MUSICA_JOGO = 'efeitos_sonoros/trilha sonora.mp3' #a trilha do jogo 
musica_atual = None

#=== CARREGAMENTO DOS BOTÕES ===
start_button_img = pygame.image.load('imagens/buttons/botao-jogar.png').convert_alpha() 
exit_button_img = pygame.image.load('imagens/buttons/botao-sair.png').convert_alpha()
restart_button_img = pygame.image.load('imagens/buttons/botao-reiniciar.png').convert_alpha() #botão do restart (para o game over)
escala_botao = 0.5
restart_button = Button(245, 150, restart_button_img, escala_botao)
start_button = Button(245, 150, start_button_img, escala_botao)
exit_button = Button(245, 220, exit_button_img, escala_botao)

# === CARREGAMENTO DO MAPA === #
mapa_oz = Mapa('mapas/mapateste.tmx') 

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
elphaba = Elphaba(elph_x, 100) # cria o objeto Elphaba
player = pygame.sprite.Group()
player.add(elphaba)
disparo_ataque = pygame.sprite.Group()
itens = pygame.sprite.Group()
testando_hitbox1 = Relógio(500, 200)
testando_hitbox2 = Elixir(800, 200)
testando_hitbox3 = Grimmerie(1000, 200)
itens.add(testando_hitbox1, testando_hitbox2, testando_hitbox3)
camera = [0, 0] # posição inicial da câmera
scroller = 0
render_camera = [0, 0]

# === INICIALIZAÇÃO DO TEMPO E CONTROLE DE LOOP ===
tempo_total = 120 # duração total do jogo em segundos (2 minutos - ajuste se necessário)
tempo_inicial_ms = pygame.time.get_ticks() # registra o tempo em milissegundos a partir do início do loop
clock = pygame.time.Clock() # limita a taxa de quadros por segundo
tempo_congelado = 0
timer_pausado = False

# === FUNÇÃO DE RENDERIZAÇÃO (DRAW) ===
def draw(scroller=scroller):
    global timer_pausado, tempo_congelado

    for i in range(3):
        pos_x_parallax = (fundos_pos[i] - camera[0] * 0.5) 
        tela.blit(fundos_loop[i], (pos_x_parallax, 0 - camera[1]))

    mapa_oz.render(tela, render_camera)

    # desenha os ataques na tela com o offset da câmera
    for ataque in disparo_ataque:
        ataque.render(tela, offset=render_camera)

    elphaba.render(tela, offset=render_camera) # desenha a Elphaba na tela com o offset da câmera

    for item in itens:
        item.render(tela, render_camera) # desenha o item no mundo
        
        # checa a colisão e retorna True se a Elphaba tiver coletado o item
        if item.update(elphaba): 
            if item.item_type == 'relógio do dragão':
                timer_pausado = True # desativa temporariamente o timer
                tempo_congelado = pygame.time.get_ticks() + 5000 # calcula o momento exato em que o tempo deve voltar ao normal
            elif item.item_type == 'elixir da vida':
                elphaba.hearts = min(elphaba.hearts + 2, elphaba.max_hearts) # caso a vida máxima ainda esteja cheia, não recebe o bônus
            elif item.item_type == 'grimório da elphie':
                elphaba.mana = min(elphaba.mana + 4, elphaba.max_mana) # caso a magia máxima ainda esteja cheia, não recebe o bônus

            item.kill() # deleta o item do jogo

    # HUD 
    desenhar_vida(tela, elphaba)
    desenhar_mana(tela, elphaba)
    desenhar_timer(tela, tempo_restante)
    desenhar_contadores(tela, elphaba)

# === FUNÇÃO PRA MUSICA ===
def tocar_musica(caminho):
    global musica_atual
    if musica_atual != caminho:
        pygame.mixer.music.stop()# para a musica atual
        pygame.mixer.music.load(caminho)# troca a musica
        pygame.mixer.music.set_volume(0.5)# volume
        pygame.mixer.music.play(-1)# toca em looping
        musica_atual = caminho

# === FUNÇÃO SOM DE COLETA ===
from objetos import carregar_sons
carregar_sons()

# === Definindo estados ===
MENU = "menu"
JOGANDO = "jogando"
GAME_OVER = "game_over"
estado =  MENU

# === GAME LOOP PRINCIPAL ===
while True:
    tela.fill((0, 0, 0))
    for event in pygame.event.get(): # itera sobre todos os eventos registrados pelo Pygame
        if event.type == pygame.QUIT: # fecha o jogo quando o 'X' da janela é clicado
            pygame.quit() # desinicializa todos os módulos do Pygame
            sys.exit() # sai do programa
    
    if estado == MENU:
        tocar_musica(MUSICA_MENU)
        tela.blit(tela_menu, (0, 0))
        if start_button.desenhar_botao(tela): 
            estado = JOGANDO 
            tocar_musica(MUSICA_JOGO)
            tempo_inicial_ms = pygame.time.get_ticks()
        if exit_button.desenhar_botao(tela):
            pygame.quit()
            sys.exit()

    elif estado == JOGANDO:
        # ATUALIZAÇÕES DE LÓGICA
        player.update(disparo_ataque, mapa_oz.plataformas)
        disparo_ataque.update(mapa_oz.plataformas)

        # CÁLCULO DE CÂMERA E TEMPO
        if timer_pausado:
            if pygame.time.get_ticks() >= tempo_congelado: # verifica se já passou do limite de 5 segundos
                timer_pausado = False # reativa o timer normalmente
            else:
                # compensa o timer depois do efeito de congelamento, adicionando o tempo parado de volta
                tempo_inicial_ms += clock.get_time() 

        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicial_ms) / 1000
        tempo_restante = tempo_total - tempo_decorrido
        
        if tempo_restante <= 0: estado = GAME_OVER

        # cálculo da câmera
        camera[0] += (elphaba.rect.centerx - tela_largura / 2 - camera[0])
        camera[1] += (elphaba.rect.centery - tela_altura / 2 - camera[1])

        tamanho_tile = mapa_oz.tmx_data.tilewidth 
        largura_mapa_pixels = mapa_oz.tmx_data.width * tamanho_tile
        altura_mapa_pixels = mapa_oz.tmx_data.height * tamanho_tile

        # TRAVA DA CÂMERA
        camera[0] = max(0, min(camera[0], largura_mapa_pixels - tela_largura))
        camera[1] = max(0, min(camera[1], altura_mapa_pixels - tela_altura))

        render_camera = (int(camera[0]), int(camera[1]))

        # ajuste do Parallax
        if elphaba.is_moving:
            scroller -= elphaba.direction * elphaba.speed
        if scroller < -tela_largura or scroller > tela_largura:
            scroller = 0

        # DESENHO
        draw(scroller=scroller)

    elif estado == GAME_OVER:
        desenhar_game_over(tela)
        if restart_button.desenhar_botao(tela):
            estado = MENU
            elphaba.reset()
            disparo_ataque.empty()

        if exit_button.desenhar_botao(tela):
            pygame.quit()
            sys.exit()

    pygame.display.update() # Único update necessário
    clock.tick(fps)