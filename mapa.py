import pygame
import pytmx
from settings import *

# CLASSE DE COLISÃO #
class Bloco(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        # retangulo de cada tile #
        self.rect = pygame.Rect(x, y, largura, altura)

class Mapa:
    def __init__(self, arquivo_tmx): # carrega o arquivo do tiled #
        self.tmx_data = pytmx.load_pygame(arquivo_tmx, pixelalpha=True)
        self.plataformas = pygame.sprite.Group() 
        self.ler_camadas_colisao()

    def ler_camadas_colisao(self):
        nomes_camadas = ["Platform", "Bridge", "Water"] # tiles com colisão baseado na categoria do tiled #

        for nome in nomes_camadas:
            try:
                camada = self.tmx_data.get_layer_by_name(nome)
                
                for x, y, gid in camada:
                    if gid != 0: 
                        pixel_x = x * self.tmx_data.tilewidth
                        pixel_y = y * self.tmx_data.tileheight
                        
                        novo_bloco = Bloco(pixel_x, pixel_y, self.tmx_data.tilewidth, self.tmx_data.tileheight)
                        self.plataformas.add(novo_bloco)
                        
            except ValueError:
                print(f"Value Error :<, olha o módulo de mapa aí pfv.")

    # RENDER DO MAPA (VISUAL :P)
    def render(self, tela, offset):
        for camada in self.tmx_data.visible_layers:
            if isinstance(camada, pytmx.TiledTileLayer):
                for x, y, gid in camada:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        px = (x * self.tmx_data.tilewidth) - offset[0]
                        py = (y * self.tmx_data.tileheight) - offset[1]
                        tela.blit(tile, (px, py))