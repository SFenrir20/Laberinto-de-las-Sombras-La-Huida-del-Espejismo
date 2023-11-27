import pygame
from settings import *
from tile import Tile
from monster import Monster
from player import Player
from utility import *
from weapon import Weapon
from ui import UI

class Level:
    def __init__(self, screen):
        self.ui = UI(screen)

        self.displaySurface = pygame.display.get_surface()

        self.visibleSprites = YSortCameraGroup()
        self.obstaclesSprites = pygame.sprite.Group()
        
        self.currentAttack = None

        self.createMap()
        
        self.ui = UI(screen)

    def createMap(self):
        layouts = {
            'base': BASE_WALLS,
            'interactive': INTERACTION_MAP,
            'entities': MONSTERS_MAP
        }
        graphics = {
            'wall': pygame.image.load('Game/graphics/wall/rock.png').convert_alpha(),
            'interactives': import_folder('Game/graphics/test/interactives')
        }
        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != ' ':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'base':
                            Tile((x, y), [self.visibleSprites, self.obstaclesSprites], 'walls', graphics['wall'])
                        if style == 'interactive':
                            surf = graphics['interactives'][int(col)]
                            Tile((x, y), [self.visibleSprites], 'interactive', surf)
                        if col == 'm':
                            Monster((x, y), [self.visibleSprites, self.obstaclesSprites])
                            
        self.player = Player((192, 192), [self.visibleSprites], self.obstaclesSprites, self.createAttack, self.destroyAttack)

    def createAttack(self):
        self.currentAttack = Weapon(self.player, [self.visibleSprites])
        
    def destroyAttack(self):
        if self.currentAttack:
            self.currentAttack.kill()
        self.currentAttack = None
    
    def run(self):
        self.visibleSprites.customDraw(self.player)
        self.visibleSprites.update()
        self.ui.display(self.player)
        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_size()[0] // 2
        self.halfHeight = self.displaySurface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        self.floorSurf = pygame.image.load('Game/graphics/tilemap/ground.png').convert()
        self.floorRect = self.floorSurf.get_rect(topleft = (0, 0))
    
    def customDraw(self, player):
        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight
        
        floorOffSetPos = self.floorRect.topleft - self.offset
        self.displaySurface.blit(self.floorSurf, floorOffSetPos)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offsetPos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offsetPos)