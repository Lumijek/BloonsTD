from balloons.balloon import Balloon
import pygame


class BlueBalloon(Balloon):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load("images/balloon_images/blueballoon.png")
        img_size = (23, 29)
        self.img = pygame.transform.scale(self.img, img_size)
        self.health = 2
        self.damage = 2
