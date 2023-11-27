import pygame, sys
from settings import *

class UI:
    def __init__(self):
        self.displaySurface = pygame.display.get_surface()
        
        self.healthBarRect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energyBarRect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
    
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