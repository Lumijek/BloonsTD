from balloons.balloon import Balloon
import pygame


class GreenBalloon(Balloon):
    def __init__(self, x=None, y=None, path_index=None):
        super().__init__(x, y, path_index)
        self.img = pygame.image.load(
            "images/balloon_images/greenballoon.png"
        ).convert_alpha()
        img_size = (31,35)
        self.img = pygame.transform.smoothscale(self.img, img_size)
        self.health = 3
        self.damage = 3
        self.spawn = ["1blue"]
        self.id = "green"
        self.velocity = 80
