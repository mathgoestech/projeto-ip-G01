import pygame
from settings import *

#  FUNÇÃO P/ DESENHAR A BARRA DE VIDA #
def desenhar_vida(tela, elphaba):
    barra_largura = 60
    barra_altura = 8
    x_pos = 10 
    y_pos = 10 
    
    # CÁLCULO DA PORCENTAGEM E LARGURA ATUAL
    porcentagem_vida = elphaba.hearts / elphaba.max_hearts
    vida_atual_largura = int(barra_largura * porcentagem_vida) # converte a porcentagem em largura de pixel
    
    # DESENHO DA BARRA (FUNDO E PREENCHIMENTO)
    fundo_rect = (x_pos, y_pos, barra_largura, barra_altura)
    pygame.draw.rect(tela, cor_branca, fundo_rect, 1) # desenha a moldura da barra
    preenchimento_rect = (x_pos, y_pos, vida_atual_largura, barra_altura)
    pygame.draw.rect(tela, cor_rosa, preenchimento_rect) # desenha o preenchimento interno

    # DESENHO DO TEXTO NUMÉRICO
    fonte = pygame.font.Font('Fonts/PixeloidSans.ttf', 10)
    vida_texto = fonte.render(
        f'{elphaba.hearts}/{elphaba.max_hearts}', 
        True, 
        cor_preta
    )
    
    MARGEM_HORIZONTAL = 10 # espaço entre a barra e o número
    texto_altura = vida_texto.get_height() # centraliza o texto na altura da barra
    x_pos_texto = x_pos + barra_largura + MARGEM_HORIZONTAL
    y_pos_texto = y_pos + (barra_altura // 2) - (texto_altura // 2)
    
    tela.blit(vida_texto, (x_pos_texto, y_pos_texto))

# FUNÇÃO P/ DESENHAR O TIMER #
def desenhar_timer(tela, tempo_restante):
    tempo_restante = max(0, tempo_restante) # previne tempo negativo

    # conversão para o formato legível
    minutos = int(tempo_restante // 60)
    segundos = int(tempo_restante % 60)

    tempo_str = f'{minutos:02}:{segundos:02}' # formata a string (zero-padding)
    cor_tempo = cor_vermelha if tempo_restante <= 30 else cor_preta # muda a cor nos últimos 30 segundos

    # renderização do texto e posicionamento dinâmico
    tempo_texto = fonte.render(f"TIMER: {tempo_str}", True, cor_tempo)
    x_pos = tela_largura - tempo_texto.get_width() - 10 
    y_pos = 10 
    
    tela.blit(tempo_texto, (x_pos, y_pos))

# FUNÇÃO P/ DESENHAR A BARRA DE MANA @
def desenhar_mana(tela, elphaba):
    barra_largura = 120
    barra_altura = 8
    x_pos = 10 
    y_pos = 22
    
    # CÁLCULO DA PORCENTAGEM E LARGURA ATUAL
    porcentagem_mana = elphaba.mana / elphaba.max_mana
    mana_atual_largura = int(barra_largura * porcentagem_mana) # converte a porcentagem em largura de pixel
    
    # DESENHO DA BARRA (FUNDO E PREENCHIMENTO)
    fundo_rect = (x_pos, y_pos, barra_largura, barra_altura)
    pygame.draw.rect(tela, cor_branca, fundo_rect, 1) # desenha a moldura da barra
    preenchimento_rect = (x_pos, y_pos, mana_atual_largura, barra_altura)
    pygame.draw.rect(tela, cor_amarela, preenchimento_rect) # desenha o preenchimento interno
    
    # DESENHO DO TEXTO NUMÉRICO
    fonte = pygame.font.Font('Fonts/PixeloidSans.ttf', 10)
    mana_texto = fonte.render(
        f'{elphaba.mana}/{elphaba.max_mana}', 
        True, 
        cor_preta
    )

    MARGEM_HORIZONTAL = 10 # espaço entre a barra e o número
    texto_altura = mana_texto.get_height() # centraliza o texto na altura da barra
    x_pos_texto = x_pos + barra_largura + MARGEM_HORIZONTAL
    y_pos_texto = y_pos + (barra_altura // 2) - (texto_altura // 2)
    
    tela.blit(mana_texto, (x_pos_texto, y_pos_texto))

# FUNÇÃO DE CONTADORES DE COLETÁVEIS #
def desenhar_contadores(tela, elphaba):
    MARGEM_ESQUERDA = 10 
    y_inicial = 35
    y_espaçamento = 15 # distância vertical entre os itens

    # DEFINIÇÃO DA LISTA DE ITENS
    itens = [
        (icone_grimorio, "Grimórios", elphaba.grimorios_coletados),
        (icone_relogio, "Relógios", elphaba.relogios_coletados),
        (icone_pocao, "Poções", elphaba.pocoes_coletadas),
    ]
    
    y_atual = y_inicial
    
    # LOOP DE DESENHO
    for icone, nome, contagem_atual in itens:
        fonte = pygame.font.Font('Fonts/PixeloidSans-Bold.ttf', 10) # renderiza o texto
        texto_display = fonte.render(
            f'{nome}: {contagem_atual}', 
            True, 
            cor_preta
        )

        # MEDIDAS E ESPAÇAMENTOS
        texto_altura = texto_display.get_height()
        icone_largura = icone.get_width() 
        icone_altura = icone_largura # assume ícone quadrado (24x24)
        MARGEM_ICONE_TEXTO = 5 # espaçamento horizontal entre o ícone e o texto
    
        # POSICIONAMENTO HORIZONTAL (ALINHAMENTO À ESQUERDA)
        x_icone = MARGEM_ESQUERDA # posição fixa à esquerda
        x_texto = x_icone + icone_largura + MARGEM_ICONE_TEXTO

        # POSICIONAMENTO VERTICAL (CENTRALIZAÇÃO)
        centro_texto = texto_altura // 2
        centro_icone = icone_altura // 2
        y_icone = y_atual + centro_texto - centro_icone 
        
        tela.blit(icone, (x_icone, y_icone))
        tela.blit(texto_display, (x_texto, y_atual))
        
        y_atual += y_espaçamento # garante que os contadores fiquem um abaixo do outro

# FUNÇÃO GAME OVER #
def desenhar_game_over(tela):
    fonte = pygame.font.Font('Fonts/PixeloidSans.ttf', 32)
    texto = fonte.render("GAME OVER", True, cor_vermelha)
    rect = texto.get_rect(center=(tela_largura // 2, tela_altura // 2 - 50))
    tela.blit(texto, rect)

def desenhar_pausa(tela):
    # cria um retângulo preto transparente do tamanho da tela
    overlay = pygame.Surface((tela_largura, tela_altura))
    overlay.set_alpha(128) # define o nível de transparência
    overlay.fill((255, 255, 255))
    tela.blit(overlay, (0, 0))

    fonte = pygame.font.Font('Fonts/PixeloidSans.ttf', 32)
    texto = fonte.render("PAUSADO", True, cor_preta)
    rect = texto.get_rect(center=(tela_largura // 2, tela_altura // 2 - 50))
    tela.blit(texto, rect)

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int((height * scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def desenhar_botao(self, tela):
        action = False

        # pega a posição do mouse
        pos = pygame.mouse.get_pos()

        # verifica se o cursor está sobre o botão
        if self.rect.collidepoint(pos): #Verifica se o mouse está colidindo com o retângulo (rect) do botão
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # [0] acessa o botão esquerdo do mouse 
                self.clicked = True
                action = True
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # desenha o botão na tela
        tela.blit(self.image, (self.rect.x, self.rect.y))   
        return action
