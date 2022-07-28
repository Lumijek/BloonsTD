from balloons.balloon import Balloon
import pygame


class YellowBalloon(Balloon):
    def __init__(self, x=None, y=None, path_index=None):
        super().__init__(x, y, path_index)
        self.img = pygame.image.load(
            "images/balloon_images/yellowballoon.png"
        ).convert_alpha()
        img_size = (33,37)
        self.img = pygame.transform.smoothscale(self.img, img_size)
        self.health = 4
        self.damage = 4
        self.spawn = ["2green"]
        self.id = "yellow"
