import pygame
from settings import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.background_image = pygame.image.load('Game/graphics/menu/Scream_inicio.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGTH))

        self.menu_image = pygame.image.load('Game/graphics/menu/Menu2.png').convert_alpha()
        menu_width, menu_height = self.menu_image.get_width(), self.menu_image.get_height()
        self.menu_rect = self.menu_image.get_rect(center=(WIDTH // 2, menu_height // 2))
        
        self.button_new_game = pygame.image.load('Game/graphics/menu/NewGame.png').convert_alpha()
        new_game_width, new_game_height = self.button_new_game.get_width(), self.button_new_game.get_height()
        self.button_new_game_rect = self.button_new_game.get_rect(center=(WIDTH // 2, HEIGTH // 2))

        self.button_quit = pygame.image.load('Game/graphics/menu/quit.png').convert_alpha()
        quit_width, quit_height = self.button_quit.get_width(), self.button_quit.get_height()
        self.button_quit_rect = self.button_quit.get_rect(topleft=(15, HEIGTH - quit_height - 15))

        self.current_screen = "main_menu"
        self.game_started = False

        self.displaySurface = pygame.display.get_surface()
        
        self.healthBarRect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energyBarRect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)


    def render_main_menu(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.menu_image, self.menu_rect)
        self.screen.blit(self.button_new_game, self.button_new_game_rect)
        self.screen.blit(self.button_quit, self.button_quit_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.current_screen == "main_menu":
                    if self.button_new_game.get_rect(topleft=(15, 20)).collidepoint(mouse_pos):
                        self.game_started = True

                if self.button_quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

    def run(self):
        while True:
            self.handle_events()

            if self.game_started:
                self.current_screen = "gameplay"
            
            if self.current_screen == "main_menu":
                self.render_main_menu()

            elif self.current_screen == "gameplay":
                self.render_game()

            pygame.display.update()
            self.clock.tick(60)  # Framerate   

    
    def showBar(self, current, maxAmount, bgRect, color):
        pygame.draw.rect(self.displaySurface, UI_BG_COLOR, bgRect)
        
        ratio = current / maxAmount
        currentWidth = bgRect.width * ratio
        currentRect = bgRect.copy()
        currentRect.width = currentWidth
        
        pygame.draw.rect(self.displaySurface, color, currentRect)
        pygame.draw.rect(self.displaySurface, UI_BORDER_COLOR, bgRect, 3)
    
    
    def display(self, player):
        self.showBar(player.health, player.stats['health'], self.healthBarRect, HEALTH_COLOR)
        self.showBar(player.energy, player.stats['energy'], self.energyBarRect, ENERGY_COLOR)
        