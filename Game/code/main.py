import pygame, sys
from settings import *
from ui import UI
from level import Level

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Laberinto de las sombras')
        self.clock  = pygame.time.Clock()
        self.level = Level()

        self.ui = UI()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(color='#78dcec')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()