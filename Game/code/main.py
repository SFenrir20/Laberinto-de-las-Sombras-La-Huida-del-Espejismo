import pygame, sys
from settings import *
from level import Level
from ui import UI

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Laberinto de las sombras')
        self.clock  = pygame.time.Clock()
        
        self.level = Level(self.screen)
        self.ui = UI(self.screen)
        
        self.game_started = False
        
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.ui.run()
        
            if self.ui.current_screen == "game_screen" and self.game_started:
                self.screen.fill(color='#78dcec')
                self.level.run()

            if self.ui.game_started:
                self.game_started = True
                self.ui.game_started = False

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGTH))
    ui = UI(screen)
    game = Game()
    game.run()