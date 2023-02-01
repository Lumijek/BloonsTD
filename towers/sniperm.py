import math
import pygame
from towers.tower import Tower
from projectiles.snprojectile import SProjectile


class SniperMonkey(Tower):
    img = pygame.image.load("images/tower_images/sniperm.png")
    img = pygame.transform.smoothscale(img, (90, 90))
    img = pygame.transform.rotozoom(img, 90, 1)

    t_range = 60
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
        self.reload_time = 1.2
        self.img.convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.id = "sniper"
        self.projectile = SProjectile

    def in_range(self, balloon_mask, balloon_coords):
        return True
