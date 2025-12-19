import pygame
import random
from settings import * # importa todas as constantes de settings.py

# fUNÇÃO PRO SOM PRA COLETA
som_coleta = None
def carregar_sons():
    global som_coleta
    som_coleta = pygame.mixer.Sound('efeitos_sonoros/coletavel.wav')
    som_coleta.set_volume(0.3)

class Glinda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # CONTROLE DE ANIMAÇÃO DA GLINDA #
        self.current_frame = 0
        self.animation_speed = 0.2
        
        quantidade_frames = 73

        # imagens da animação da glinda #
        self.frames = []
        for i in range(quantidade_frames):
            img = pygame.image.load(f'imagens/sprites/glinda-idle/pixil-frame-{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (64, 64)) 
            self.frames.append(img)

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def animar(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

    def render(self, tela, offset):
        self.animar()
        tela.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))

class Inimigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # PROPRIEDADES BÁSICAS E DE ESTADO
        self.width = inimigo_largura
        self.height = inimigo_altura
        self.speed = inimigo_velocidade # velocidade de movimento
        self.health = 3 # vida inicial do inimigo (ajuste se necessário)

        # MOVIMENTO DE PATRULHA #
        self.patrol_distance = 30
        self.wait_time = 180
        self.speed = 2
        self.origin_x = x 
        self.timer_espera = 0     
        self.direction = 1        

        # DEFINIÇÃO DAS ANIMAÇÕES
        self.animations = {
            'idle' : pygame.transform.scale(
                pygame.image.load('imagens/sprites/macaco-voador/macaco_frente.png'),
                (self.width, self.height)
                ),
            'voando' : [
                pygame.transform.scale(
                pygame.image.load('imagens/sprites/macaco-voador/macaco_lado_frame1.png'),
                (self.width, self.height)
                ),
                pygame.transform.scale(
                pygame.image.load('imagens/sprites/macaco-voador/macaco_lado_frame2.png'),
                (self.width, self.height)
                ),
                pygame.transform.scale(
                pygame.image.load('imagens/sprites/macaco-voador/macaco_lado_frame3.png'),
                (self.width, self.height)
                ),
                pygame.transform.scale(
                pygame.image.load('imagens/sprites/macaco-voador/macaco_lado_frame4.png'),
                (self.width, self.height)
                ),
                pygame.transform.scale(
                pygame.image.load('imagens/sprites/macaco-voador/macaco_lado_frame5.png'),
                (self.width, self.height)
                )
            ]
        }

        # CONFIGURAÇÕES DE IMAGEM E HITBOX
        self.image = self.animations['idle']
        largura_hitbox = self.width * 0.30
        altura_hitbox = self.height * 0.45
        self.rect = pygame.Rect(0, 0, largura_hitbox, altura_hitbox)
        self.rect.center = (x, y)

        self.gravity = gravidade
        self.is_targeting = False
        self.flying = 0
        self.direction = 1 # 1 para direita, -1 para esquerda

        # VARIÁVEIS DE ANIMAÇÃO
        self.current_frame = 0
        self.animation_speed = 0.1

    def aplicar_fisica(self, plataformas):

        if pygame.sprite.spritecollideany(self, plataformas):
            self.rect.x -= self.direction * 5 
            self.timer_espera = self.wait_time
            self.direction *= -1

    def checar_colision(self, disparo):
        if self.rect.colliderect(disparo.rect):
            self.health -= 1
            disparo.kill()
            return True
        return False

    def animar_sprites(self):

        if self.timer_espera > 0:
            self.image = self.animations['idle']

        else:
            self.current_frame += self.animation_speed

            # loop de animação: se a sequência de frames chegar ao fim, volta pro início
            if self.current_frame >= len(self.animations['voando']): 
                self.current_frame = 0

            self.image = self.animations['voando'][int(self.current_frame)]

            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)


    def update(self, plataformas, disparo):

        # verifica colisão com o disparo
        for ataque in disparo:
            if self.checar_colision(ataque):
                self.kill()
                print("Inimigo atingido!")

        # caso de morte #
        if self.health <= 0: 
            self.kill()

        # timer da patrulha #
        if self.timer_espera > 0:
            self.timer_espera -= 1
            self.flying = 0 

        else:
            self.flying = 1 
            self.movimento = self.direction * self.speed
            self.rect.x += self.movimento

            # limite direito
            if self.rect.centerx > self.origin_x + self.patrol_distance:
                self.direction = -1 
                self.timer_espera = 180
            
            # limite esquerdo
            elif self.rect.centerx < self.origin_x - self.patrol_distance:
                self.direction = 1 
                self.timer_espera = 180

        self.aplicar_fisica(plataformas)
        self.animar_sprites()

    def reset(self):
        #MUDAR DPS
        self.rect.x = inimigos_pos[0][0]
        self.rect.y = inimigos_pos[0][1]
        self.health = 3
        self.is_targeting = False

    def render(self, tela, offset=(0, 0)):
        posicao_centro_x = self.rect.centerx - offset[0]
        posicao_centro_y = self.rect.centery - offset[1]

        rect_desenho = self.image.get_rect(center=(posicao_centro_x, posicao_centro_y))
        tela.blit(self.image, rect_desenho)

class Relógio(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.item_type = 'relógio do dragão'
        self.tempo_pausado = 5 # duração do efeito de congelamento (em segundos - ajuste se necessário)

        # CONFIGURAÇÃO DE ANIMAÇÃO
        self.current_frame = 0
        self.animation_speed = 0.1

        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f'imagens/sprites/coletáveis/relogio dragao/relogio-frame-{i}.png'),
                (24, 24)
            )
            for i in range(4)
        ]

        # CONFIGURAÇÕES DE IMAGEM E HITBOX
        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect()

        # COORDENADAS INICIAIS NO MAPA
        self.rect.x = x
        self.rect.y = y

    def animar_sprites(self):
        self.current_frame += self.animation_speed

        # loop de animação: se a sequência de frames chegar ao fim, volta pro início
        if self.current_frame >= len(self.frames): 
            self.current_frame = 0

        self.image = self.frames[int(self.current_frame)]

    def update(self, elphaba):
        self.animar_sprites()

        # verifica colisão entre os retângulos do relógio e da Elphaba
        if self.rect.colliderect(elphaba.rect):
            elphaba.relogios_coletados += 1
            som_coleta.play()
            return True # avisa ao main.py pra congelar o timer
        return False # não aconteceu colisão

    def render(self, tela, offset):
        # desconta o movimento da câmera, garantindo que o item fique preso ao mapa, não à tela
        tela.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))

class Elixir(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.item_type = 'elixir da vida'

        # CONFIGURAÇÃO DE ANIMAÇÃO
        self.current_frame = 0
        self.animation_speed = 0.1

        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f'imagens/sprites/coletáveis/pocao de cura/pocao-frame-{i}.png'),
                (24, 24)
            )
            for i in range(4)
        ]

        # CONFIGURAÇÕES DE IMAGEM E HITBOX
        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect()

        # COORDENADAS INICIAIS NO MAPA
        self.rect.x = x
        self.rect.y = y

    def animar_sprites(self):
        self.current_frame += self.animation_speed

        # loop de animação: se a sequência de frames chegar ao fim, volta pro início
        if self.current_frame >= len(self.frames): 
            self.current_frame = 0

        self.image = self.frames[int(self.current_frame)]

    def update(self, elphaba):
        self.animar_sprites()

        # verifica colisão entre os retângulos do elixir e da Elphaba
        if self.rect.colliderect(elphaba.rect):
            elphaba.pocoes_coletadas += 1
            som_coleta.play()
            return True # avisa ao main.py pra incrementar +2 na barra de vida
        return False # não aconteceu colisão

    def render(self, tela, offset):
        # desconta o movimento da câmera, garantindo que o item fique preso ao mapa, não à tela
        tela.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))

class Grimmerie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.item_type = 'grimório da elphie'

        # CONFIGURAÇÃO DE ANIMAÇÃO
        self.current_frame = 0
        self.animation_speed = 0.1

        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f'imagens/sprites/coletáveis/grimorio/grimorio_arte_principal{i + 1}.png'),
                (24, 24)
            )
            for i in range(2)
        ]

        # CONFIGURAÇÕES DE IMAGEM E HITBOX
        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect()

        # COORDENADAS INICIAIS NO MAPA
        self.rect.x = x
        self.rect.y = y

    def animar_sprites(self):
        self.current_frame += self.animation_speed

        # loop de animação: se a sequência de frames chegar ao fim, volta pro início
        if self.current_frame >= len(self.frames): 
            self.current_frame = 0

        self.image = self.frames[int(self.current_frame)]

    def update(self, elphaba):
        self.animar_sprites()

        # verifica colisão entre os retângulos do elixir e da Elphaba
        if self.rect.colliderect(elphaba.rect):
            elphaba.grimorios_coletados += 1
            som_coleta.play()
            return True # avisa ao main.py pra incrementar +4 na barra de mana
        return False # não aconteceu colisão

    def render(self, tela, offset):
        # desconta o movimento da câmera, garantindo que o item fique preso ao mapa, não à tela
        tela.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))
