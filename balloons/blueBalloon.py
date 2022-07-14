
from balloons.balloon import Balloon
import pygame
class BlueBalloon(Balloon):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load("images/balloon_images/blueballoon.png")
        self.health = 2
        self.damage = 2