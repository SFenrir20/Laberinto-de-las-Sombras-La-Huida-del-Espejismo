import pygame
from settings import *
from utility import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacleSprites, createAttack, destroyAttack):
        super().__init__(groups)
        self.image = pygame.image.load(
            'Game/graphics/player/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, -26)

        self.importPlayerAssets()
        self.status = 'down'
        self.frameIndex = 0
        self.animationSpeed = 0.15

        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attackCd = 100
        self.attackTime = None
        self.obstacleSprites = obstacleSprites
        
        self.createAttack = createAttack
        self.destroyAttack = destroyAttack
        self.weaponIndex = 0
        self.weapon = list(weapon_data.keys())[self.weaponIndex]
        
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 4}
        self.heath = self.stats['health']
        self.energy = self.stats['energy']
        self.health = self.stats['health']
        self.exp = 123
        self.speed = self.stats['speed']
        
    def importPlayerAssets(self):
        characterPath = 'Game/graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [],'right': [],
                'right_idle':[], 'left_idle':[], 'up_idle':[],'down_idle':[],
                'right_attack':[], 'left_attack':[],'up_attack':[],'down_attack':[]}
        for animation in self.animations.keys():
            fullPath = characterPath + animation
            self.animations[animation] = import_folder(fullPath)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
            

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0
            
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attackTime = pygame.time.get_ticks()
            self.createAttack()

    def getStatus(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacleSprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == 'vertical':
            for sprite in self.obstacleSprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        currentTime = pygame.time.get_ticks()
        if self.attacking:
            if currentTime - self.attackTime >= self.attackCd:
                self.attacking = False
                self.destroyAttack()

    def animate(self):
        animation = self.animations[self.status]
        
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
        
        self.image = animation[int(self.frameIndex)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.getStatus()
        self.animate()
        self.move(self.speed)
