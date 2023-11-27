from typing import Any
import pygame
from settings import *
from entity import Entity
from utility import *

class Monster(Entity):
    def __init__(self, monsterName, pos, groups, obstacleSprites, damagePlayer):
        
        super().__init__(groups)
        self.spriteType = 'enemy'
        
        self.importGraphics(monsterName)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frameIndex]
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-30, -30)
        self.obstacleSprites = obstacleSprites
        
        self.monsterName = monsterName
        monsterInfo = monster_data[self.monsterName]
        self.health = monsterInfo['health']
        self.exp = monsterInfo['exp']
        self.speed = monsterInfo['speed']
        self.attackDamage = monsterInfo['damage']
        self.resistance = monsterInfo['resistance']
        self.attackRadius = monsterInfo['attack_radius']
        self.noticeRadius = monsterInfo['notice_radius']
        self.attackType = monsterInfo['attack_type']
        
        self.canAttack = True
        self.attackTime = None
        self.attackCooldown = 400
        self.damagePlayer = damagePlayer
        
        self.vulnerable = True
        self.hitTime = None
        self.invincibilityDuration = 300
        
    def importGraphics(self, name):
        self.animations = {'idle': [], 'move':[], 'attack': []}
        main_path = f'Game/graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def getPlayerDistanceDirection(self, player):
        
        monsterVec = pygame.math.Vector2(self.rect.center)
        playerVec = pygame.math.Vector2(player.rect.center)
        distance = (playerVec - monsterVec).magnitude()
        
        if distance > 0:
            direction = (playerVec - monsterVec).normalize()
        else:
            direction = pygame.math.Vector2()
                
        return (distance, direction)

    def getStatus(self, player):
        distance = self.getPlayerDistanceDirection(player)[0]
        
        if distance <= self.attackRadius and self.canAttack:
            if self.status != 'attack':
                self.frameIndex = 0
            self.status = 'attack'
        elif distance <= self.noticeRadius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attackTime = pygame.time.get_ticks()
            self.damagePlayer(self.attackDamage, self.attackType)
        elif self.status == 'move':
            self.direction = self.getPlayerDistanceDirection(player)[1]
        else:
            self.direction = pygame.math.Vector2()
            
    def animate(self):
        animation = self.animations[self.status]
        
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
        
        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        if not self.vulnerable:
            alpha = self.waveValue()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        
    def cooldown(self):
        currentTime = pygame.time.get_ticks()
        if not self.canAttack:
            if currentTime - self.attackTime >= self.attackCooldown:
                self.canAttack = True
                
        if not self.vulnerable:
            if currentTime - self.hitTime >= self.invincibilityDuration:
                self.vulnerable = True
                
    def getDamage(self, player, attackType):
        if self.vulnerable:
            self.direction = self.getPlayerDistanceDirection(player)[1]
            if attackType == 'weapon':
                self.health -= player.getFullWeaponDamage()
            else:
                pass
            
            self.hitTime = pygame.time.get_ticks()
            self.vulnerable = False
        
    def checkDeath(self):
        if self.health <= 0:
            self.kill()
            
    def hitReaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hitReaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.checkDeath()
        
    def monsterUpdate(self, player):
        self.getStatus(player)
        self.actions(player)