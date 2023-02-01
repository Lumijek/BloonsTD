from projectiles.projectile import Projectile
import math
import numpy as np
import pygame


class SuperProjectile(Projectile):
    def __init__(self, starting_x, starting_y):
        super().__init__(starting_x, starting_y)
        self.x = starting_x
        self.y = starting_y
        self.velocity = 800
        self.img = pygame.image.load("images/projectile_images/d1.png").convert_alpha()
        self.img = pygame.transform.smoothscale(
            self.img, (self.img.get_width() * 0.8, self.img.get_height() * 0.8)
        )
        self.img = pygame.transform.rotozoom(self.img, -130, 1)
        self.total_time = 0
        self.tot_dis = 400
        self.id = "superproj"

    def move_projectile(self, delta_time):
        self.total_time += delta_time
        if self.angle != None:
            if self.total_time < 0.07:
                self.x -= math.cos(self.angle) * self.velocity * delta_time
                self.y -= math.sin(self.angle) * self.velocity * delta_time
                self.dis_traveled -= self.velocity * delta_time
            else:
                self.x += math.cos(self.angle) * self.velocity * delta_time
                self.y += math.sin(self.angle) * self.velocity * delta_time
                self.dis_traveled += self.velocity * delta_time
