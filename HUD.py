import pygame
from settings import * # importa todas as constantes de settings.py

def desenhar_vida(tela, elphaba):
    barra_largura = 96
    barra_altura = 15  

    x_pos = 10 
    y_pos = 20 
    
    # CÁLCULO DA PORCENTAGEM E LARGURA ATUAL
    porcentagem_vida = elphaba.hearts / elphaba.max_hearts
    vida_atual_largura = int(barra_largura * porcentagem_vida) # converte a porcentagem em largura de pixel
    
    # DESENHO DA BARRA (FUNDO E PREENCHIMENTO)
    fundo_rect = (x_pos, y_pos, barra_largura, barra_altura)
    pygame.draw.rect(tela, cor_branca, fundo_rect, 2) # desenha a moldura da barra
    preenchimento_rect = (x_pos, y_pos, vida_atual_largura, barra_altura)
    pygame.draw.rect(tela, cor_rosa, preenchimento_rect) # desenha o preenchimento interno

    # DESENHO DO TEXTO NUMÉRICO
    fonte = pygame.font.Font('Fonts/PixeloidSans.ttf', 16)
    vida_texto = fonte.render(
        f'{elphaba.hearts}/{elphaba.max_hearts}', 
        True, 
        cor_branca
    )
    
    MARGEM_HORIZONTAL = 10 # espaço entre a barra e o número
    texto_altura = vida_texto.get_height() # centraliza o texto na altura da barra
    x_pos_texto = x_pos + barra_largura + MARGEM_HORIZONTAL
    y_pos_texto = y_pos + (barra_altura // 2) - (texto_altura // 2)
    
    
    tela.blit(vida_texto, (x_pos_texto, y_pos_texto))

def desenhar_timer(tela, tempo_restante):
    tempo_restante = max(0, tempo_restante) # previne tempo negativo

    # conversão para o formato legível
    minutos = int(tempo_restante // 60)
    segundos = int(tempo_restante % 60)

    tempo_str = f'{minutos:02}:{segundos:02}' # formata a string (zero-padding)
    cor_tempo = cor_vermelha if tempo_restante <= 30 else cor_branca # muda a cor nos últimos 30 segundos

    # renderização do texto e posicionamento dinâmico
    tempo_texto = fonte.render(f"TIMER: {tempo_str}", True, cor_tempo)
    x_pos = tela_largura - tempo_texto.get_width() - 10 
    y_pos = 10 
    
    tela.blit(tempo_texto, (x_pos, y_pos))

def desenhar_mana(tela, elphaba):
    barra_largura = 192
    barra_altura = 15
    
    x_pos = 10 
    y_pos = 40 
    
    # CÁLCULO DA PORCENTAGEM E LARGURA ATUAL
    porcentagem_mana = elphaba.mana / elphaba.max_mana
    mana_atual_largura = int(barra_largura * porcentagem_mana) # converte a porcentagem em largura de pixel
    
    # DESENHO DA BARRA (FUNDO E PREENCHIMENTO)
    fundo_rect = (x_pos, y_pos, barra_largura, barra_altura)
    pygame.draw.rect(tela, cor_branca, fundo_rect, 2) # desenha a moldura da barra
    preenchimento_rect = (x_pos, y_pos, mana_atual_largura, barra_altura)
    pygame.draw.rect(tela, cor_amarela, preenchimento_rect) # desenha o preenchimento interno
    
    # DESENHO DO TEXTO NUMÉRICO
    fonte = pygame.font.Font('Fonts/PixeloidSans.ttf', 16)
    mana_texto = fonte.render(
        f'{elphaba.mana}/{elphaba.max_mana}', 
        True, 
        cor_branca
    )

    MARGEM_HORIZONTAL = 10 # espaço entre a barra e o número
    texto_altura = mana_texto.get_height() # centraliza o texto na altura da barra
    x_pos_texto = x_pos + barra_largura + MARGEM_HORIZONTAL
    y_pos_texto = y_pos + (barra_altura // 2) - (texto_altura // 2)
    
    tela.blit(mana_texto, (x_pos_texto, y_pos_texto))

def desenhar_contadores(tela, elphaba):
    MARGEM_ESQUERDA = 10 
    y_inicial = 65
    y_espaçamento = 25 # distância vertical entre os itens

    # DEFINIÇÃO DA LISTA DE ITENS
    itens = [
        (icone_grimorio, "Grimórios", elphaba.grimorios_coletados),
        (icone_relogio, "Relógios", elphaba.relogios_coletados),
        (icone_pocao, "Poções", elphaba.pocoes_coletadas),
    ]
    
    y_atual = y_inicial
    
    # LOOP DE DESENHO
    for icone, nome, contagem_atual in itens:
        fonte = pygame.font.Font('Fonts/PixeloidSans-Bold.ttf', 16) # renderiza o texto
        texto_display = fonte.render(
            f'{nome}: {contagem_atual}', 
            True, 
            cor_branca
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
