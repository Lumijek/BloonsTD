from projectiles.projectile import Projectile
import numpy as np
import math
import pygame
import time


class Boomerang(Projectile):
    def __init__(self, starting_x, starting_y):
        super().__init__(starting_x, starting_y)
        self.durability = 5
        rad = 6
        self.boomerang = pygame.Surface((rad * 2, rad * 2))
        pygame.draw.circle(self.boomerang, "RED", (rad, rad), rad)
        self.mask = pygame.mask.from_surface(self.boomerang)
        self.shot = False
        self.angle = None
        self.id = "boomerang"

    def f(self, t):
        return math.cos(2 * t) * math.cos(t)

    def g(self, t):
        return math.cos(2 * t) * math.sin(t)

    def get_curve(self, start, angle, time, dt, mode="radians"):
        scale = 200
        t = -math.pi / 4
        steps = int(time / dt)
        cos = math.cos(angle)
        sin = math.sin(angle)
        t_step = (math.pi / 2) / steps  # difference in start t and end t divided by 2
        l = []
        for i in range(steps):
            t += t_step
            x = self.f(t) * cos - self.g(t) * sin
            y = self.f(t) * sin + self.g(t) * cos
            l.append((x * scale + start[0], y * scale + start[1]))
        self.b_path = l
        self.i = 0
        self.i_max = steps
        self.shot = True

    def projectile_target(self, tower, balloon, path, path_index, delta_time):
        x, y = balloon.get_x(), balloon.get_y()
        diffX = x - self.x
        diffY = y - self.y
        self.angle = round(math.atan2(diffY, diffX), 4)
        var = self.get_curve([self.x, self.y], self.angle, 1, delta_time)
        tower.angle = round(self.angle, 3)
        tower.rotate_m = True
        tower.is_reloading = True
        return True

    def draw(self, screen, delta_time):
        if self.shot == True and self.i < self.i_max:
            screen.blit(
                self.boomerang, (self.b_path[self.i][0], self.b_path[self.i][1])
            )
            self.i += 1
        else:
            self.shot = False
