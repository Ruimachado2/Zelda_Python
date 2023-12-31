import pygame
from random import choice

from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *

class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass'    : import_csv_layout('./map/map_Grass.csv'),
            'object'   : import_csv_layout('./map/map_Objects.csv')
        }

        graphics = {
            'grass'  : import_folder('./graphics/grass'),
            'object' : import_folder('./graphics/objects')
        }
        print(graphics)

        for style, layouts in layouts.items():
            for row_index, row in enumerate(layouts):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        
                        if style == 'boundary':
                            Tile( (x,y), [self.obstacle_sprites], 'invisible' )
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile( (x,y), [self.visible_sprites, self. obstacle_sprites], 'grass', random_grass_image )
                        if style == 'object':
                            surf = graphics['object'][int(col)]
                            Tile( (x,y), [self.visible_sprites, self. obstacle_sprites], 'object', surf )


                    #if col == 'x':
                    #    Tile((x,y),[self.visible_sprites, self.obstacle_sprites])

                    #if col == 'p':
                    #    self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)

        self.player = Player((2000,1400),[self.visible_sprites], self.obstacle_sprites)

                
    def run(self):
        #update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

    
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating floor
        self.floor_surface = pygame.image.load('./graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        # get offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)


        