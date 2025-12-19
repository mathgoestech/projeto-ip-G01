import pygame
import sys # módulo necessário para sair do programa
from settings import * # importa todas as constantes de settings.py
from jogador import *
from objetos import *
from HUD import * # importa todas as funções de HUD.py
from mapa import Mapa # importa o mapa
from objetos import carregar_sons # importa a função do sons dos coletáveis
from objetos import som_hit_macaco # importa som do macaco

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
play_button_img = pygame.image.load('imagens/buttons/pausa verde.png').convert_alpha()
exit_button_img = pygame.image.load('imagens/buttons/botao-sair.png').convert_alpha()
restart_button_img = pygame.image.load('imagens/buttons/botao-reiniciar.png').convert_alpha() #botão do restart (para o game over)
escala_botao = 0.5
restart_button = Button(245, 150, restart_button_img, escala_botao)
start_button = Button(245, 150, start_button_img, escala_botao)
exit_button = Button(245, 220, exit_button_img, escala_botao)
play_button = Button(245, 150, play_button_img, escala_botao)

# === CARREGAMENTO DO MAPA === #
mapa_oz = Mapa('mapas/mapateste.tmx') 

def criar_itens():
    grupo_itens = pygame.sprite.Group()
    
    # Cria os relógios
    for pos in relogios_pos:
        grupo_itens.add(Relógio(pos[0], pos[1]))
    # Cria os elixires
    for pos in elixires_pos:
        grupo_itens.add(Elixir(pos[0], pos[1]))
    # Cria os grimórios
    for pos in grimorios_pos:
        grupo_itens.add(Grimmerie(pos[0], pos[1]))
    return grupo_itens

# === CARREGAMENTO E CONFIGURAÇÃO DO FUNDO ===
BG1 = pygame.image.load('imagens/backgrounds/fundo-menuprincipal.png')
tela_menu = pygame.transform.scale(BG1, (tela_largura, tela_altura))
BG = pygame.image.load('imagens/backgrounds/emerald-city-path.jpg')

# === INSTANCIAÇÃO DE OBJETOS (POO) ===
piso_y = tela_altura # define a altura vertical que o player considera como o chão (limite inferior da tela)
elphaba = Elphaba(elph_x, elph_y) # cria o objeto Elphaba
player = pygame.sprite.Group()
player.add(elphaba)

lista_inimigos = []
for i in range(inimigos_qnt):
    x, y = inimigos_pos[i]
    macaco = Inimigos(x, y)
    lista_inimigos.append(macaco)
inimigo = pygame.sprite.Group()
inimigo.add(lista_inimigos)
lista_inimigos_ativos = lista_inimigos.copy()

disparo_ataque = pygame.sprite.Group()
itens = pygame.sprite.Group()
itens = criar_itens()
glinda = Glinda(2300, 255)
camera = [0, 0] # posição inicial da câmera
render_camera = [0, 0]

# === INICIALIZAÇÃO DO TEMPO E CONTROLE DE LOOP ===
tempo_total = 60 # duração total do jogo em segundos (2 minutos - ajuste se necessário)
tempo_inicial_ms = pygame.time.get_ticks() # registra o tempo em milissegundos a partir do início do loop
clock = pygame.time.Clock() # limita a taxa de quadros por segundo
tempo_congelado = 0
timer_pausado = False

# === FUNÇÃO DE RENDERIZAÇÃO (DRAW) ===
def draw():
    global timer_pausado, tempo_congelado
    mapa_oz.render(tela, render_camera)

    #render dos inimigos
    for macaco in lista_inimigos_ativos:
        macaco.update(mapa_oz.plataformas, disparo_ataque)

        if macaco.health <= 0:
            lista_inimigos_ativos.remove(macaco)
        else:
            macaco.render(tela, offset=render_camera) # desenha o inimigo na tela com o offset da câmera

    # desenha os ataques na tela com o offset da câmera
    for ataque in disparo_ataque:
        ataque.render(tela, offset=render_camera)

    elphaba.render(tela, offset=render_camera) # desenha a Elphaba na tela com o offset da câmera
    glinda.render(tela, render_camera) # desenha a galinda #

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
        pygame.mixer.music.set_volume(0.25)# volume
        pygame.mixer.music.play(-1)# toca em looping
        musica_atual = caminho

# === COMANDO ENVOLVENDO SONS ===
carregar_sons()
som_hit_macaco()
game_over = pygame.mixer.Sound('efeitos_sonoros/game over.wav')
game_over.set_volume(0.5)
pausa = pygame.mixer.Sound('efeitos_sonoros/pausa.wav')
pausa.set_volume(0.5)
vitoria = pygame.mixer.Sound('efeitos_sonoros/vitoria.wav')
vitoria.set_volume(0.5)
hit_elphaba = pygame.mixer.Sound('efeitos_sonoros/hit_elphaba.wav')
hit_elphaba.set_volume(0.1)

# === DEFINIÇÃO DE ESTADOS ===
MENU = "menu"
JOGANDO = "jogando"
GAME_OVER = "game_over"
PAUSA = "pausa"
VITORIA = "vitoria"
estado = MENU

# === GAME LOOP PRINCIPAL ===
while True:
    tela.fill((0, 0, 0))

    for event in pygame.event.get(): # itera sobre todos os eventos registrados pelo Pygame

        if event.type == pygame.QUIT: # fecha o jogo quando o 'X' da janela é clicado
            pygame.quit() # desinicializa todos os módulos do Pygame
            sys.exit() # sai do programa

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if estado == JOGANDO:
                    estado = PAUSA
                    pausa.play()
                elif estado == PAUSA:
                    estado = JOGANDO
                    pygame.mixer.music.unpause()
                    pausa.play()

            if event.key == pygame.K_ESCAPE:
                if estado == GAME_OVER or estado == PAUSA or estado == JOGANDO:
                    estado = MENU
                elif estado == MENU:
                    pygame.quit()
                    sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: 
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                coord_mapa_x = mouse_x + render_camera[0]
                coord_mapa_y = mouse_y + render_camera[1]
                
                print(f"COORDENADA CLICADA: ({coord_mapa_x}, {coord_mapa_y})")
    
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

        # MORTE POR ÁGUA #
        if pygame.sprite.spritecollide(elphaba, mapa_oz.agua, False):
            elphaba.hearts = 0 # Zera a vida visualmente
            estado = GAME_OVER
            game_over.play()

        # COLISÃO E MORTE DOS INIMIGOS #
        for macaco in lista_inimigos_ativos[:]:
            if macaco.health <= 0:
                lista_inimigos_ativos.remove(macaco) # morte do macaco #
        colisoes_fisicas = pygame.sprite.spritecollide(elphaba, lista_inimigos_ativos, False)
        
        for inimigo in colisoes_fisicas:  # dano por encostar na elphie #
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - elphaba.ultimo_dano > elphaba.invencivel_timer:
                elphaba.hearts -= 1
                hit_elphaba.play()
                elphaba.ultimo_dano = tempo_atual 

            # colisão #
            if elphaba.rect.centerx < inimigo.rect.centerx:
                elphaba.rect.right = inimigo.rect.left
            else:
                elphaba.rect.left = inimigo.rect.right


        # CASO DE VITORIA #
        if elphaba.rect.colliderect(glinda.rect):
            estado = VITORIA
            vitoria.play()

        # CÁLCULO DE CÂMERA E TEMPO
        if timer_pausado:
            if pygame.time.get_ticks() >= tempo_congelado: # verifica se já passou do limite de 5 segundos
                timer_pausado = False # reativa o timer normalmente
            else:
                # compensa o timer depois do efeito de congelamento, adicionando o tempo parado de volta
                tempo_inicial_ms += clock.get_time() 

        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicial_ms) / 1000
        tempo_restante = tempo_total - tempo_decorrido
        
        if tempo_restante <= 0:
            estado = GAME_OVER
            game_over.play()

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

        # DESENHO
        draw()

    elif estado == VITORIA:
        tela.fill((0, 0, 0))
        desenhar_vitoria(tela)
        pygame.mixer.music.stop()

        if restart_button.desenhar_botao(tela):
            estado = MENU
            vitoria.stop()

            elphaba.reset()
            disparo_ataque.empty()
            itens.empty()
            
            lista_inimigos_ativos.clear()
            for i in range(inimigos_qnt):
                x, y = inimigos_pos[i]
                macaco = Inimigos(x, y)
                lista_inimigos_ativos.append(macaco)

            itens.empty() 
            itens = criar_itens() 


        if exit_button.desenhar_botao(tela):
            pygame.quit()
            sys.exit()

    elif estado == GAME_OVER:
        desenhar_game_over(tela)
        pygame.mixer.music.stop() # para a musica atual

        if restart_button.desenhar_botao(tela):
            estado = MENU
            game_over.stop()
            
            # limpa os sprites da partida anterior
            disparo_ataque.empty()
            itens.empty()

            # recria os itens
            itens.empty() # Limpa os velhos
            itens = criar_itens() # Cria os novos nas posições certas do settings

            elphaba.reset()

            # recria os inimigos
            lista_inimigos_ativos.clear()
            for i in range(inimigos_qnt):
                x, y = inimigos_pos[i]
                macaco = Inimigos(x, y)
                lista_inimigos_ativos.append(macaco)


        if exit_button.desenhar_botao(tela):
            pygame.quit()
            sys.exit()

    elif estado == PAUSA:
        draw() 
        desenhar_pausa(tela)
        pygame.mixer.music.pause() # pausa a musica

        # é a mesma lógica do timer congelado: incrementa o tempo inicial
        tempo_inicial_ms += clock.get_time()

        if play_button.desenhar_botao(tela):
            pausa.play()
            pygame.mixer.music.unpause() # despausa
            estado = JOGANDO

        if exit_button.desenhar_botao(tela):
            pygame.quit()
            sys.exit()

    pygame.display.update() # Único update necessário
    clock.tick(fps)