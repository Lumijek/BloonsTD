from balloons.balloon import Balloon
import pygame


class RedBalloon(Balloon):
    def __init__(self, x, y, path_index):
        super().__init__(self, x, y, path_index)
        self.img = pygame.image.load("images/balloon_images/bb.png").convert_alpha()
        self.health = 1
        self.damage = 1
        self.id = "red"