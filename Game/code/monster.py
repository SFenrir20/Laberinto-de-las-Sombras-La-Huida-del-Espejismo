import pygame
from settings import *

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        #self.image = pygame.image.load('Game/graphics/monsters/spawn/skeleton_spawn.png').convert_alpha()
        self.image = pygame.image.load('Game/graphics/monsters/skeleton/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-30, -10)