from balloons.balloon import Balloon
import pygame


class RedBalloon(Balloon):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load("images/balloon_images/bb.png").convert_alpha()
        self.health = 1
        self.damage = 1
