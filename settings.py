import pygame
pygame.font.init() # inicializa o módulo de fontes do Pygame

# === DEFINIÇÕES GERAIS (TELA, TÍTULO, FPS) ===
tela_largura = 640
tela_altura = 360
título = 'Resgate RelâmpagOZ'
fps = 60 # determina a velocidade máxima de atualização da tela

# === PROPRIEDADES BASE DA ELPHIE (PLAYER) ===
elph_velocidade = 2.5 # determina o quão rápida a Elphie se move na horizontal
elph_largura = 64
elph_altura = 64
elph_x = 95
elph_y = 335

# === PROPRIEDADES DOS INIMIGOS ===
inimigo_velocidade = 1.5
inimigo_largura = 64
inimigo_altura = 64
inimigos_pos = [(225, 350), (402, 309), (523, 311), (661, 188), (1126, 241), (1446, 224), (1866, 250), (2127, 331), (2248, 306)]
inimigos_qnt = len(inimigos_pos)

# === FÍSICA DO MOVIMENTO VERTICAL (GRAVIDADE E PULO) ===
gravidade = 0.35 # aceleração vertical aplicada a cada frame
pulo_altura = 6 # força inicial (velocidade vertical negativa)

# === CONFIGURAÇÕES DO HUD (HEADS-UP DISPLAY) ===
cor_branca = (255, 255, 255)
cor_vermelha = (255, 0, 0)
cor_amarela = (255, 215, 0)
cor_rosa = (224, 60, 138)
cor_preta = (0, 0, 0)
cor_verde = (50, 205, 50) 

fonte = pygame.font.Font('Fonts/PixeloidSans-Bold.ttf', 12) # objeto de fonte padrão, tamanho 12


# === CARREGAMENTO DE ÍCONES DE COLETÁVEIS ===
icone_grimorio = pygame.transform.scale(
    pygame.image.load('imagens/sprites/coletáveis/grimorio/grimorio_arte_principal2.png'),
    (16, 16)
)
icone_relogio = pygame.transform.scale(
    pygame.image.load('imagens/sprites/coletáveis/relogio dragao/relogio-frame-0.png'),
    (16, 16)
)
icone_pocao = pygame.transform.scale(
    pygame.image.load('imagens/sprites/coletáveis/pocao de cura/pocao-frame-0.png'),
    (16, 16)
)
