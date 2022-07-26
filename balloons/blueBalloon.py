from balloons.balloon import Balloon
import pygame


class BlueBalloon(Balloon):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load(
            "images/balloon_images/blueballoon.png"
        ).convert_alpha()
        img_size = (39, 41)
        self.img = pygame.transform.scale(self.img, img_size)
        self.health = 2
        self.damage = 2
        self.spawn = ["red"]
        self.id = "blue"

