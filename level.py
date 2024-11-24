import pygame 
import random
from settings import *
from support import *
from pytmx.util_pygame import load_pygame
from tile import Tile, Interaction
from player import Player
from debug import debug
from interface import UI
from transition import Transition

class Level:
    def __init__(self):
        # grab display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # play transition
        self.transition = Transition(self.reset, self.player)

        # user interface
        self.ui = UI()

    def create_map(self):
        tmx_data = load_pygame('./graphics/house/housemap.tmx')

        for x, y, surface in tmx_data.get_layer_by_name("Boundary").tiles():
            Tile((x * TILESIZE, y * TILESIZE), [self.obstacle_sprites], 'boundary', surface=surface, z=LAYERS['floor'])

        for layer in ['Ground']:
            for x, y, surface in tmx_data.get_layer_by_name(layer).tiles():
                Tile((x * TILESIZE, y * TILESIZE), [self.visible_sprites], 'floor', surface=surface, z=LAYERS['floor'])

        for layer in ['Wall', 'Furniture', 'Tabletop']:
            for x, y, surface in tmx_data.get_layer_by_name(layer).tiles():
                Tile((x * TILESIZE, y * TILESIZE), [self.visible_sprites, self.obstacle_sprites], 'floor', surface=surface, z=LAYERS['house'])

        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Bed":
                Interaction((obj.x,obj.y), (obj.width,obj.height), [self.interaction_sprites], obj.name)
        
        Tile(
            (0,0),
            [self.visible_sprites],
            'floor',
            surface=pygame.image.load('./graphics/house/ground.png').convert_alpha(),
            z=LAYERS['floor']
        )

        self.player = Player((400, 400), [self.visible_sprites], self.obstacle_sprites, self.interaction_sprites)

    def reset(self):
        self.player.day += 1
        self.player.hour = 8

    def run(self):
        # update & draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
        #debug(self.player.sleep)

        if self.player.sleep:
            self.transition.play()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        #self.floor_surface = pygame.image.load('./graphics/tilemap/ground.png').convert()
        #self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        #floor_offset_pos = self.floor_rect.topleft - self.offset 
        #self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)