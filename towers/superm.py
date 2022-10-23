import math
import pygame
from projectiles.superprojectile import SuperProjectile
from towers.tower import Tower


class SuperMonkey(Tower):

    img = pygame.image.load("images/tower_images/supermonkey.png")
    img = pygame.transform.smoothscale(img, (60, 60))
    img = pygame.transform.rotozoom(img, -90, 1)

    t_range = 175
    circ_img = pygame.Surface((t_range * 2, t_range * 2))
    pygame.draw.circle(circ_img, (0, 0, 1), (t_range, t_range), t_range)
    circ_img.set_colorkey("Black")
    circ_img.set_alpha(100)

    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.price = None
        self.damage = None
        self.img.convert_alpha()
        self.reload_time = 0.1
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.id = "super"
        self.projectile = SuperProjectile
