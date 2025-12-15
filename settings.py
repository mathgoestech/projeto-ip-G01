import pygame
pygame.font.init() # inicializa o módulo de fontes do Pygame

# === DEFINIÇÕES GERAIS (TELA, TÍTULO, FPS) ===
tela_largura = 1000
tela_altura = 600
título = 'Resgate RelâmpagOZ'
fps = 60 # determina a velocidade máxima de atualização da tela

# === PROPRIEDADES BASE DA ELPHIE (PLAYER) ===
elph_velocidade = 3 # determina o quão rápida a Elphie se move na horizontal
elph_largura = 300
elph_altura = 300
elph_x = 100
elph_y = 200

# === FÍSICA DO MOVIMENTO VERTICAL (GRAVIDADE E PULO) ===
gravidade = 0.8 # aceleração vertical aplicada a cada frame
pulo_altura = 20 # força inicial (velocidade vertical negativa)

# === CONFIGURAÇÕES DO HUD (HEADS-UP DISPLAY) ===
cor_branca = (255, 255, 255)
cor_vermelha = (200, 0, 0)
cor_amarela = (255, 215, 0)
cor_rosa = (224, 60, 138)

fonte = pygame.font.Font(None, 30) # objeto de fonte padrão, tamanho 30

# === CARREGAMENTO DE ÍCONES DE COLETÁVEIS ===
icone_grimorio = pygame.transform.scale(
    pygame.image.load('imagens/sprites/coletáveis/relogio dragao/pixil-frame-0.png'),
    (24, 24)
)
icone_relogio = pygame.transform.scale(
    pygame.image.load('imagens/sprites/coletáveis/relogio dragao/pixil-frame-0.png'),
    (24, 24)
)
icone_pocao = pygame.transform.scale(
    pygame.image.load('imagens/sprites/coletáveis/pocao de cura/pixil-frame-0.png'),
    (24, 24)
)
