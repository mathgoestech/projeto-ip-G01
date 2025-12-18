import pygame
from settings import * # importa todas as constantes de settings.py

class Glinda():
    def __init__(self):
        pass

class Inimigos():
    def __init__(self):
        pass

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
            return True # avisa ao main.py pra congelar o timer
        return False # não aconteceu colisão

    def render(self, tela, offset):
        # desconta o movimento da câmera, garantindo que o item fique preso ao mapa, não à tela
        tela.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))
