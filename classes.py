import pygame
from settings import *

class Elphaba(pygame.sprite.Sprite):
    def __init__(self, elph_x, tela_altura):
        super().__init__()

        self.width = elph_largura
        self.height = elph_altura
        self.speed = elph_velocidade # velocidade horizontal
        
        self.animations = {
            'idle': pygame.transform.scale(
                pygame.image.load('imagens/sprites/elphaba/elphie-parada-direita.png'),
                (self.width, self.height)
            ),
            'andando': [
                pygame.transform.scale(
                    pygame.image.load('imagens/sprites/elphaba/elphie-andando-direita1.png'),
                    (self.width, self.height)
                ),
                pygame.transform.scale(
                    pygame.image.load('imagens/sprites/elphaba/elphie-andando-direita2.png'),
                    (self.width, self.height)
                )
            ],
            'pulando': pygame.transform.scale(
                pygame.image.load('imagens/sprites/elphaba/elphie-pulo2.png'),
                (self.width, self.height)
            )
        }

        self.image = self.animations['idle']
        self.rect = self.image.get_rect()

        self.rect.x = elph_x
        self.rect.y = tela_altura - self.height # basicamente a coordenada do piso
        self.ground_y = self.rect.y # posição onde o objeto deve parar (o chão)

        self.gravity = gravidade
        self.jump_height = pulo_altura
        self.jump_velocity = self.jump_height # velocidade vertical inicial
        self.is_jumping = False
        self.is_moving = False
        self.direction = 1 # 1 para direita, -1 para esquerda
        self.current_frame = 0 # índice do frame atual da animação
        self.animation_speed = 0.2 # velocidade em que os frames mudam (ajuste conforme necessário)

    def processar_entrada(self):
        keys = pygame.key.get_pressed() # verifica quais teclas estão sendo pressionadas
        TECLA_ESQUERDA = keys[pygame.K_LEFT]
        TECLA_DIREITA = keys[pygame.K_RIGHT]
        TECLA_CIMA = keys[pygame.K_UP]

        self.is_moving = False
        if TECLA_ESQUERDA:
            self.rect.x -= self.speed # decrementa x, movendo para a esquerda
            self.is_moving = True
            self.direction = -1
        if TECLA_DIREITA:
            self.rect.x += self.speed # incrementa x, movendo para a direita
            self.is_moving = True
            self.direction = 1
        if TECLA_CIMA and not self.is_jumping:
            self.is_jumping = True # ativa o estado de pulo

    def aplicar_física(self):
        if self.is_jumping:
            self.rect.y -= self.jump_velocity # altera a coordenada y, movendo objeto/player para cima
            self.jump_velocity -= self.gravity # aplica a gravidade, desacelerando a velocidade do pulo na subida
            if self.jump_velocity < -self.jump_height: # termina quando a velocidade do pulo atinge o valor inicial de subida
                self.is_jumping = False
                self.jump_velocity = self.jump_height # reseta a velocidade para o próximo pulo
                self.rect.y = self.ground_y # garante que o player pouse no chão

    def animar_sprites(self):
        if self.is_jumping:
            self.image = self.animations['pulando']
        elif self.is_moving:
            self.current_frame += self.animation_speed # avança o contador de frames

            if self.current_frame >= len(self.animations['andando']):
                self.current_frame = 0 # garante que o contador volte para o início quando chegar ao fim da lista

            self.image = self.animations['andando'][int(self.current_frame)]

            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False) # espelha a imagem, caso vá para a esquerda
        else:
            self.image = self.animations['idle']
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.processar_entrada()
        self.aplicar_física()
        self.animar_sprites()

class feitiços():
    def __init__(self):
        pass

class inimigos():
    def __init__(self):
        pass

class coletáveis():
    def __init__(self):
        pass
