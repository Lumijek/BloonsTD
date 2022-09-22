from projectiles.projectile import Projectile
import math
import numpy as np
import pygame


class SProjectile(Projectile):
    def __init__(self, starting_x, starting_y):
        super().__init__(starting_x, starting_y)
        self.x = starting_x
        self.y = starting_y
        self.velocity = 1000
        self.img = None #pygame.image.load("images/projectile_images/d1.png").convert_alpha()
        #self.img = pygame.transform.smoothscale(
            #self.img, (self.img.get_width() * 0.4, self.img.get_height() * 0.4)
        #)
        #self.img = pygame.transform.rotozoom(self.img, -130, 1)
        self.angle = None
        self.tot_dis = 500
        self.dis_traveled = 0
        self.dead = False
        self.durability = 1
        self.id = "snproj"
    def projectile_target(self, balloon, path, path_index, delta_time):
        x, y = balloon.get_x(), balloon.get_y()
        diffX = x - self.x
        diffY = y - self.y
        self.angle = round(math.atan2(diffY, diffX), 4)
        return False