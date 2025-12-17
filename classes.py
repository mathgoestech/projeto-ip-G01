import pygame
from settings import * # importa todas as constantes de settings.py

class Elphaba(pygame.sprite.Sprite):
    def __init__(self, elph_x, tela_altura):
        super().__init__()

        # PROPRIEDADES BÁSICAS E DE ESTADO
        self.width = elph_largura
        self.height = elph_altura
        self.speed = elph_velocidade # velocidade horizontal

        # ATRIBUTOS DE HUD (STATUS DO PLAYER)
        self.max_hearts = 8
        self.hearts = self.max_hearts # vida atual, inicializada com o máximo
        self.max_mana = 16
        self.mana = self.max_mana # mana atual, inicializada com o máximo

        # SISTEMA DE INVENTÁRIO (ITENS COLETADOS)
        self.pocoes_coletadas = 0 
        self.grimorios_coletados = 0 
        self.relogios_coletados = 0 
        
        # DEFINIÇÃO DAS ANIMAÇÕES
        self.animations = {
            'idle': pygame.transform.scale(
                pygame.image.load('imagens/sprites/elphaba/elphaba-parada-lado.png'),
                (self.width, self.height)
            ),
            'atirando': pygame.transform.scale(
                pygame.image.load('imagens/sprites/elphaba/elphaba-atirando.png'),
                (self.width, self.height)
            ),
            'andando': [
                pygame.transform.scale(
                    pygame.image.load('imagens/sprites/elphaba/elphaba-andando-1.png'),
                    (self.width, self.height)
                ),
                pygame.transform.scale(
                    pygame.image.load('imagens/sprites/elphaba/elphaba-andando-2.png'),
                    (self.width, self.height)
                )
            ],
            'pulando': [
                pygame.transform.scale(
                    pygame.image.load('imagens/sprites/elphaba/elphaba-pulo-1.png'),
                    (self.width, self.height)
                ),
                pygame.transform.scale(
                    pygame.image.load('imagens/sprites/elphaba/elphaba-pulo-2.png'),
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
        self.is_shooting = False
        self.direction = 1 # 1 para direita, -1 para esquerda (usado para espelhamento)

        # VARIÁVEIS DE CONTROLE DE ANIMAÇÃO
        self.current_frame = 0 # índice do frame atual
        self.animation_speed = 0.1 # velocidade de transição de frames (ajuste se necessário)

        self.can_shoot = True
        self.shoot_cooldown = 30 # tempo de espera entre disparos (em frames) >> 30 frames equivalem a 0.5s
        self.cooldown_timer = 0 # contador regressivo do cooldown

    def processar_entrada(self, disparo_ataque):
        keys = pygame.key.get_pressed() # verifica quais teclas estão sendo pressionadas
        TECLA_ESQUERDA = keys[pygame.K_LEFT]
        TECLA_DIREITA = keys[pygame.K_RIGHT]
        TECLA_CIMA = keys[pygame.K_UP]
        TECLA_ESPAÇO = keys[pygame.K_SPACE]

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
        if TECLA_ESPAÇO:
            self.atirar(disparo_ataque)

    def aplicar_física(self):
        if self.is_jumping:
            self.rect.y -= self.jump_velocity # diminui y pela velocidade vertical atual
            self.jump_velocity -= self.gravity # aplica a gravidade, desacelerando a velocidade na subida
            if self.jump_velocity < -self.jump_height: # acaba quando a velocidade vertical atinge o valor negativo da força inicial do pulo
                self.is_jumping = False
                self.jump_velocity = self.jump_height # reseta a velocidade para o próximo pulo
                self.rect.y = self.ground_y # garante que o player pouse exatamente no chão

    def controlar_cooldown(self):
        if not self.can_shoot:
            self.cooldown_timer -= 1
            if self.cooldown_timer <= 0:
                self.can_shoot = True
                self.cooldown_timer = 0

    def atirar(self, disparo_ataque):
        # verifica se a Elphie pode atirar E se ela tem mana suficiente
        if self.can_shoot and self.mana >= 2:
            
            # o disparo deve começar FORA do hitbox da Elphie para evitar colisões instantâneas
            x_disparo = self.rect.centerx + (self.rect.width // 2) * self.direction # multiplica por 1 (direita) ou -1 (esquerda), garantindo que o feitiço comece na direção correta
            y_disparo = self.rect.centery + 70 

            novo_disparo = Ataque(x_disparo, y_disparo, self.direction) # cria a instância do novo feitiço
            disparo_ataque.add(novo_disparo) # adiciona ao grupo de feitiços ativos
            
            self.mana -= novo_disparo.mana_cost # subtrai o custo de mana
            self.can_shoot = False # impede novos disparos imediatamente
            self.cooldown_timer = self.shoot_cooldown
            self.is_shooting = True
            self.animation_timer = 8

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
        elif self.is_shooting:
            self.image = self.animations['atirando']

            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.is_shooting = False
        else:
            self.image = self.animations['idle']
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False) # garante que a Elphaba esteja virada para a última direção

    def update(self, disparo_ataque): # esse método é chamado automaticamente por 'player.update()' no main.py a cada frame
        self.processar_entrada(disparo_ataque)
        self.aplicar_física()
        self.controlar_cooldown()
        self.animar_sprites()

    def reset(self): # reseta os valores para reiniciar o jogo com os valores padrão
        self.rect.x = elph_x
        self.rect.y = self.ground_y
        self.hearts = self.max_hearts
        self.mana = self.max_mana
        self.is_jumping = False
        self.is_moving = False
        self.is_shooting = False

    def render(self, tela, offset=(0, 0)):
        tela.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))

    def rect(self):
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)


class Ataque(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        # PROPRIEDADES DO FEITIÇO
        self.damage = 1
        self.speed = 5
        self.direction = direction # herda a direção da Elphie
        self.mana_cost = 2
        self.dist_percorrida = 0
        self.alcance_max = 800 # o feitiço vai sumir depois de viajar 800 pixels

        # VARIÁVEIS DE CONTROLE DE ANIMAÇÃO
        self.current_frame = 0
        self.animation_speed = 0.2

        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f'imagens/sprites/ataque/comet{i + 1}.png'), 
                (128, 128)
            )
            for i in range(14)
        ]

        # CONFIGURAÇÃO DE IMAGEM INICIAL E RECT
        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_rect() 
        self.rect.center = (x, y) # centraliza o feitiço no ponto de disparo

    def animar_sprites(self):
        self.current_frame += self.animation_speed

        if self.current_frame >= len(self.frames):
            self.current_frame = 0 

        frame_idx = int(self.current_frame)
        imagem_atual = self.frames[frame_idx]

        if self.direction == -1:
            imagem_atual = pygame.transform.flip(imagem_atual, True, False)

        self.image = imagem_atual

    def update(self):
        self.animar_sprites()
        
        deslocamento = self.speed * self.direction
        self.rect.x += deslocamento # move o feitiço horizontalmente a cada frame
        self.dist_percorrida += abs(deslocamento)
        
        if self.dist_percorrida > self.alcance_max:
            self.kill() # o feitiço agora é destruído com base na distância percorrida

class Glinda():
    def __init__(self):
        pass

class Inimigos():
    def __init__(self):
        pass

class Coletáveis():
    def __init__(self):
        pass


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