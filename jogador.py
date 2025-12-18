import pygame
from settings import *

class Elphaba(pygame.sprite.Sprite):
    def __init__(self, elph_x, elph_y):
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
        
        #SOM DO ATAQUE
        self.som_ataque = pygame.mixer.Sound('efeitos_sonoros/barulho ataque.wav')
        self.som_ataque.set_volume(0.3)

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

        # IMAGEM E HITBOX (RECT) #
        self.image = self.animations['idle']

        largura_hitbox = self.width * 0.15
        altura_hitbox = self.height * 0.45
        
        self.rect = pygame.Rect(0, 0, largura_hitbox, altura_hitbox)

        # VARIÁVEIS DE FÍSICA E ESTADO DE MOVIMENTO
        self.gravity = gravidade
        self.jump_height = pulo_altura # força inivial do pulo
        self.jump_velocity = self.jump_height # velocidade vertical atual (começa com a força máxima do pulo)
        self.is_jumping = False
        self.is_moving = False
        self.is_shooting = False
        self.direction = 1 # 1 para direita, -1 para esquerda (usado para espelhamento)

        # VARIÁVEIS DE CONTROLE DE ANIMAÇÃO
        self.current_frame = 0 # índice do frame atual
        self.animation_speed = 0.1 # velocidade de transição de frames (ajuste se necessário)


        # COOLDOWN DO PODER #
        self.can_shoot = True
        self.shoot_cooldown = 30 # tempo de espera entre disparos (em frames) >> 30 frames equivalem a 0.5s
        self.cooldown_timer = 0 # contador regressivo do cooldown
        self.animation_timer = 0 

    def processar_entrada(self, disparo_ataque):
            keys = pygame.key.get_pressed()
            self.is_moving = False

            # MOVIMENTO LATERAL #
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
                self.is_moving = True
                self.direction = -1
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
                self.is_moving = True
                self.direction = 1

            # PULO #
            if keys[pygame.K_UP] and not self.is_jumping:
                self.is_jumping = True
                self.jump_velocity = -self.jump_height # Impulso para cima
            
            # ATAQUE #
            if keys[pygame.K_SPACE]:
                self.atirar(disparo_ataque)

    def aplicar_física(self, plataformas):
        # GRAVIDADE #
        self.jump_velocity += self.gravity
        self.rect.y += self.jump_velocity

        # COLISÃO VERTICAL #
        colisoes = pygame.sprite.spritecollide(self, plataformas, False)
        for bloco in colisoes:
            if self.jump_velocity > 0: # Caindo
                self.rect.bottom = bloco.rect.top
                self.jump_velocity = 0
                self.is_jumping = False
            elif self.jump_velocity < 0: # Subindo
                self.rect.top = bloco.rect.bottom
                self.jump_velocity = 0

    def controlar_cooldown(self):
        if not self.can_shoot:
            self.cooldown_timer -= 1
            if self.cooldown_timer <= 0:
                self.can_shoot = True
                self.cooldown_timer = 0

    def atirar(self, disparo_ataque):
        # verifica se a Elphie pode atirar E se ela tem mana suficiente
        if self.can_shoot and self.mana >= 2:
            
            x_disparo = self.rect.centerx + (self.width // 2 * self.direction) # multiplica por 1 (direita) ou -1 (esquerda), garantindo que o feitiço comece na direção correta
            y_disparo = self.rect.centery - 10 

            novo_disparo = Ataque(x_disparo, y_disparo, self.direction) # cria a instância do novo feitiço
            disparo_ataque.add(novo_disparo) # adiciona ao grupo de feitiços ativos
            
            self.mana -= novo_disparo.mana_cost # subtrai o custo de mana
            self.can_shoot = False # impede novos disparos imediatamente
            self.cooldown_timer = self.shoot_cooldown
            self.is_shooting = True
            self.animation_timer = 8
            self.som_ataque.play()# toca o som de atque

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

    def update(self, disparo_ataque, plataformas):
        self.processar_entrada(disparo_ataque)

        # COLISÃO HORIZONTAL #
        colisoes = pygame.sprite.spritecollide(self, plataformas, False)
        for bloco in colisoes:
            if self.direction > 0: # Indo para direita
                self.rect.right = bloco.rect.left
            elif self.direction < -0: # Indo para esquerda
                self.rect.left = bloco.rect.right

        self.aplicar_física(plataformas)
        
        self.controlar_cooldown()
        self.animar_sprites()

    def reset(self): # reseta os valores para reiniciar o jogo com os valores padrão
        self.rect.x = elph_x
        self.rect.y = elph_y
        self.hearts = self.max_hearts
        self.mana = self.max_mana
        self.jump_velocity = 0 # Reseta a velocidade de queda
        self.is_jumping = False
        self.is_moving = False
        self.is_shooting = False

    def render(self, tela, offset=(0, 0)):
        desenho_x = self.rect.centerx - (self.width / 2) - offset[0]
        desenho_y = self.rect.bottom - self.height - offset[1]
        
        tela.blit(self.image, (desenho_x, desenho_y))

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
        self.alcance_max = 250 # o feitiço vai sumir depois de viajar 250 pixels
        self.colidiu = False

        # VARIÁVEIS DE CONTROLE DE ANIMAÇÃO
        self.current_frame = 0
        self.animation_speed = 0.25

        tamanho_projetil = (48, 48)

        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f'imagens/sprites/ataque/comet{i + 1}.png'), 
                (tamanho_projetil)
            )
            for i in range(14)
        ]

        # CONFIGURAÇÃO DE IMAGEM INICIAL
        self.image = self.frames[int(self.current_frame)]

        # HITBOX DO FEITIÇO
        rect_original = self.image.get_rect()
        rect_original.center = (x, y)
        self.rect = rect_original.inflate(-47, -30) # reduz o tamanho da hitbox do feeitiço #

    def animar_sprites(self):
        self.current_frame += self.animation_speed

        # se a animação acabou destrói o objeto #
        if self.current_frame >= len(self.frames):
            self.kill()
            return
        
        frame_idx = int(self.current_frame)
        imagem_atual = self.frames[frame_idx]

        if self.direction == -1: # espelha pra esquerda #
            imagem_atual = pygame.transform.flip(imagem_atual, True, False)

        self.image = imagem_atual

    def update(self, plataformas=None):
        self.animar_sprites()
        
        if self.alive() and not self.colidiu: # se o projétil tiver ativo e não colidiu em nada, movimenta #
            deslocamento = self.speed * self.direction
            self.rect.x += deslocamento
            self.dist_percorrida += abs(deslocamento)
            
            # destruição por distância #
            if self.dist_percorrida > self.alcance_max:
                self.kill()

            # fica estático por colisão #
            if plataformas and pygame.sprite.spritecollideany(self, plataformas):
                self.colidiu = True 

    def render(self, tela, offset=(0, 0)): # função p/ sincronizar a hitbox do feitiço com a imagem real #
            posicao_desenho = self.image.get_rect(center=self.rect.center)
            tela.blit(self.image, (posicao_desenho.x - offset[0], posicao_desenho.y - offset[1]))

            