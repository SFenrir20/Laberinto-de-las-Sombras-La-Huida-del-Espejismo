import pygame, sys
from settings import *
from tile import Tile
from monster import Monster
from player import Player
from utility import *
from weapon import Weapon
from ui import UI
from monster import Monster

class Level:
    def __init__(self):
        self.displaySurface = pygame.display.get_surface()

        self.visibleSprites = YSortCameraGroup()
        self.obstaclesSprites = pygame.sprite.Group()
        
        self.currentAttack = None
        self.attackSprites = pygame.sprite.Group()
        self.attackableSprites = pygame.sprite.Group()
        
        self.gameStart = False

        self.createMap()
        
        self.ui = UI()

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
                        if style == 'entities':
                            if col == 'f': monster_name = 'spirit'
                            elif col == 'r': monster_name = 'racoon'
                            Monster(monster_name, (x,y), [self.visibleSprites, self.attackableSprites], self.obstaclesSprites, self.damagePlayer)

                            
        self.player = Player((192, 192), [self.visibleSprites], self.obstaclesSprites, self.createAttack, self.destroyAttack)

    def createAttack(self):
        self.currentAttack = Weapon(self.player, [self.visibleSprites, self.attackSprites])
        
    def destroyAttack(self):
        if self.currentAttack:
            self.currentAttack.kill()
        self.currentAttack = None
    
    def playerAttackLogic(self):
        if self.attackSprites:
            for attackSprite in self.attackSprites:
                collisionSprites = pygame.sprite.spritecollide(attackSprite, self.attackableSprites, False)
                if collisionSprites:
                    for targetSprite in collisionSprites:
                        targetSprite.getDamage(self.player, attackSprite.spriteType)
    
    def damagePlayer(self, amount, attackType):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurtTime = pygame.time.get_ticks()
            
    def showGameOverScreen(self):
        if not self.player.estaVivoooo:
            
            self.background = pygame.image.load('Game/graphics/menu/lose_1.jpg').convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
            
            self.gameOver = pygame.image.load('Game/graphics/menu/gameOver.png').convert_alpha()
            self.gameOverRect = self.gameOver.get_rect(center=(WIDTH // 2, HEIGTH // 2))
            
            self.buttonQuit = pygame.image.load('Game/graphics/menu/quit.png').convert_alpha()
            self.buttonQuitRect = self.buttonQuit.get_rect(topleft=(15, HEIGTH - 50))
            
            self.displaySurface.blit(self.background, (0, 0))
            self.displaySurface.blit(self.gameOver, self.gameOverRect)
            self.displaySurface.blit(self.buttonQuit, self.buttonQuitRect)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.buttonQuitRect.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()
    
    def mainMenu(self):
        if not self.gameStart:
            
            self.background_image = pygame.image.load('Game/graphics/menu/Scream_inicio.png').convert()
            self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGTH))

            self.menu_image = pygame.image.load('Game/graphics/menu/Menu2.png').convert_alpha()
            self.menu_rect = self.menu_image.get_rect(center=(WIDTH // 2, 15))

            self.button_new_game = pygame.image.load('Game/graphics/menu/NewGame.png').convert_alpha()
            self.button_new_game_rect = self.button_new_game.get_rect(center=(WIDTH // 2, HEIGTH // 2))

            self.button_quit = pygame.image.load('Game/graphics/menu/quit.png').convert_alpha()
            self.button_quit_rect = self.button_quit.get_rect(topleft=(15, HEIGTH - 50))
            
            self.displaySurface.blit(self.background_image, (0, 0))
            self.displaySurface.blit(self.menu_image, self.menu_rect)
            self.displaySurface.blit(self.button_new_game, self.button_new_game_rect)
            self.displaySurface.blit(self.button_quit, self.button_quit_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.button_new_game_rect.collidepoint(mouse_pos):
                        self.gameStart = True
                    elif self.button_quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
    
    def run(self):
        self.mainMenu()
        if self.gameStart:
            self.visibleSprites.customDraw(self.player)
            self.visibleSprites.update()
            self.visibleSprites.monsterUpdate(self.player)
            self.playerAttackLogic()
            self.ui.display(self.player)
        self.showGameOverScreen()
        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.halfWidth = self.displaySurface.get_size()[0] // 2
        self.halfHeight = self.displaySurface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    
    def customDraw(self, player):
        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offsetPos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offsetPos)
    
    def monsterUpdate(self, player):
        monsterSprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'spriteType') and sprite.spriteType == 'enemy']
        for monster in monsterSprites:
            monster.monsterUpdate(player)