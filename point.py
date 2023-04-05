from random import randint
import pygame
 
class Point(pygame.sprite.Sprite):
    def __init__(self, pos, mass, color, isFixed=False):
        super().__init__()
        self.isFixed = isFixed
        self.isDead = False
        self.pos = pos
        x = pos[0]
        y = pos[1]
        height = 2
        width = 2
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.old_pos = [x, y]
        self.mass = mass

    def reset_pos(self):
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.old_pos = [self.x, self.y]
        self.isDead = False

    def render_pos(self):
        if not self.isFixed:
            self.rect.x = self.x - self.rect.w//2
            self.rect.y = self.y - self.rect.h//2