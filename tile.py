import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE)), z=LAYERS['main']):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.z = z

class Interaction(Tile):
    def __init__(self, pos, size, groups, name):
        surface = pygame.Surface(size)
        super().__init__(pos, groups, 'placeholder', surface)
        self.name = name