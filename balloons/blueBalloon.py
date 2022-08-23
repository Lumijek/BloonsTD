from balloons.balloon import Balloon
import pygame


class BlueBalloon(Balloon):
    def __init__(self, x=None, y=None, path_index=None):
        super().__init__(x, y, path_index)
        self.img = pygame.image.load(
            "images/balloon_images/blueballoon.png"
        ).convert_alpha()
        img_size = (29, 33)
        self.img = pygame.transform.smoothscale(self.img, img_size)
        self.mask = pygame.mask.from_surface(self.img)
        self.health = 2
        self.damage = 2
        self.spawn = ["1red"]
        self.id = "blue"
        self.velocity = 60
