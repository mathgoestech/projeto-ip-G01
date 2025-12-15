import pygame
from settings import * # importa todas as constantes de settings.py

class Elphaba(pygame.sprite.Sprite):
    def __init__(self, elph_x, tela_altura):
        super().__init__()

        # PROPRIEDADES BÁSICAS E DE ESTADO
        self.width = elph_largura
        self.height = elph_altura
        self.speed = elph_velocidade # velocidade horizontal

        # === ATRIBUTOS DE HUD (STATUS DO PLAYER) ===
        self.max_hearts = 5
        self.hearts = self.max_hearts # vida atual, inicializada com o máximo
        self.max_mana = 15
        self.mana = self.max_mana # mana atual, inicializada com o máximo

        # SISTEMA DE INVENTÁRIO (ITENS COLETADOS)
        self.pocoes_coletadas = 0 
        self.grimorios_coletados = 0 
        self.relogios_coletados = 0 
        
        # DEFINIÇÃO DAS ANIMAÇÕES
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
            'pulando': [
                pygame.transform.scale(
                    pygame.image.load('imagens/sprites/elphaba/2-elphie-pulo1.png'),
                    (self.width, self.height)
                ),
                pygame.transform.scale(
                    pygame.image.load('imagens/sprites/elphaba/elphie-pulo2.png'),
                    (self.width, self.height)
                )
            ]
        }

        # CONFIGURAÇÃO DE IMAGEM E RECT
        self.image = self.animations['idle'] # define o frame estático
        self.rect = self.image.get_rect() # cria o retângulo (rect) de colisão e posicionamento baseado no tamanho da imagem

        # POSICIONAMENTO INICIAL
        self.rect.x = elph_x
        self.rect.y = tela_altura - self.height # ajusta a posição y para que a base do sprite toque a altura do chão
        self.ground_y = self.rect.y # posição y do chão (limite inferior para pouso)

        # VARIÁVEIS DE FÍSICA E ESTADO DE MOVIMENTO
        self.gravity = gravidade
        self.jump_height = pulo_altura # força máxima do pulo
        self.jump_velocity = self.jump_height # velocidade vertical atual (começa com a força máxima do pulo)
        self.is_jumping = False
        self.is_moving = False
        self.direction = 1 # 1 para direita, -1 para esquerda (usado para espelhamento)

        # VARIÁVEIS DE CONTROLE DE ANIMAÇÃO
        self.current_frame = 0 # índice do frame atual
        self.animation_speed = 0.1 # velocidade de transição de frames (ajuste se necessário)

    def processar_entrada(self):
        keys = pygame.key.get_pressed() # verifica quais teclas estão sendo pressionadas
        TECLA_ESQUERDA = keys[pygame.K_LEFT]
        TECLA_DIREITA = keys[pygame.K_RIGHT]
        TECLA_CIMA = keys[pygame.K_UP]

        self.is_moving = False

        if TECLA_ESQUERDA:
            self.rect.x -= self.speed # decrementa x, movendo o retângulo para a esquerda
            self.is_moving = True
            self.direction = -1
        if TECLA_DIREITA:
            self.rect.x += self.speed # incrementa x, movendo o retângulo para a direita
            self.is_moving = True
            self.direction = 1
        if TECLA_CIMA and not self.is_jumping:
            self.is_jumping = True # ativa o estado de pulo

    def aplicar_física(self):
        if self.is_jumping:
            self.rect.y -= self.jump_velocity # diminui y pela velocidade vertical atual
            self.jump_velocity -= self.gravity # aplica a gravidade, desacelerando a velocidade na subida
            if self.jump_velocity < -self.jump_height: # acaba quando a velocidade vertical atinge o valor negativo da força inicial do pulo
                self.is_jumping = False
                self.jump_velocity = self.jump_height # reseta a velocidade para o próximo pulo
                self.rect.y = self.ground_y # garante que o player pouse exatamente no chão

    def animar_sprites(self):
        if self.is_jumping:
            if self.jump_velocity > 0: # se a velocidade for positiva, está subindo (usa o primeiro frame de pulo)
                self.image = self.animations['pulando'][0]
            else: # se a velocidade for negativa, está caindo (usa o segundo frame de pulo)
                self.image = self.animations['pulando'][1]
        elif self.is_moving:
            self.current_frame += self.animation_speed # avança o contador de frames

            if self.current_frame >= len(self.animations['andando']): # checa se o contador ultrapassou o total de frames na lista
                self.current_frame = 0 # reinicia o contador

            self.image = self.animations['andando'][int(self.current_frame)] # seleciona o frame atual

            if self.direction == -1: 
                self.image = pygame.transform.flip(self.image, True, False) # espelha a imagem para simular movimento na direção oposta
        else:
            self.image = self.animations['idle']
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False) # garante que a Elphaba esteja virada para a última direção

    def update(self): # esse método é chamado automaticamente por 'player.update()' no main.py a cada frame
        self.processar_entrada()
        self.aplicar_física()
        self.animar_sprites()

class Feitiços():
    def __init__(self):
        pass

class Inimigos():
    def __init__(self):
        pass

class Coletáveis():
    def __init__(self):
        pass
