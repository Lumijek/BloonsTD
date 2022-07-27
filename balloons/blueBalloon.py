from balloons.balloon import Balloon
import pygame


class BlueBalloon(Balloon):

    
    def __init__(self, x = None, y = None, path_index = None):
        super().__init__(x, y, path_index)
        self.img = pygame.image.load(
            "images/balloon_images/blueballoon.png"
        ).convert_alpha()
        img_size = (39, 41)
        self.img = pygame.transform.scale(self.img, img_size)
        self.health = 2
        self.damage = 2
        self.spawn = ["1red"]
        self.id = "blue"

