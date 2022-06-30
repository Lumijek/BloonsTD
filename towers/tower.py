import math
import pygame

from sqlalchemy import false

class Tower:
    def __init__(self, x, y):
        self.length = None
        self.height = None
        self.x = x
        self.y = y
        self.rangeR = 100
        self.price = None
        self.damage = None
        self.velocity = 2
        self.img = pygame.image.load("images/tower_images/tt.png")
        self.img = pygame.transform.scale(self.img, (60, 60))
        self.reload_tick = [0, 20] # number of frames to wait before shooting again
        self.is_reloading = False

    def in_range(self, balloon):
        xDiff = balloon.getX() - self.x
        yDiff = balloon.getY() - self.y
        if xDiff ** 2 + yDiff ** 2 <= self.rangeR ** 2:
            return True
        else:
            return False

    def is_tower_reloading(self):
        return self.is_reloading

    def reload(self):
        if self.is_reloading:
            self.reload_tick[0] += 1
            if self.reload_tick[0] == self.reload_tick[1]:
                self.reload_tick[0] = 0
                self.is_reloading = False

    def can_shoot(self):

        if self.reload_tick[0] == 0:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def shoot(self, bullet, balloon):
        # if splash = true, will be called in here as well
        if self.in_range(balloon.getX(), balloon.getY()):
            bullet(balloon)

    def getX(self):
        return self.xCoord

    def getY(self):
        return self.yCoord

    def getX(self):
        return self.x

    def getY(self):
        return self.y



            
