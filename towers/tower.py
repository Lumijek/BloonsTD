import math
import pygame


class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 300
        self.price = None
        self.damage = None
        self.img = pygame.image.load("images/tower_images/tt.png")
        self.img = pygame.transform.scale(self.img, (60, 60))
        self.reload_tick = [0, 20]  # number of frames to wait before shooting again
        self.is_reloading = False
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def in_range(self, balloon):
        x_change = balloon.get_x() - self.x
        y_change = balloon.get_y() - self.y
        if x_change ** 2 + y_change ** 2 <= self.range ** 2:
            return True
        else:
            return False

    def is_tower_reloading(self):
        return self.is_reloading

    def reload(self):
        if self.is_reloading:
            self.reload_tick[0] += 1
            if self.reload_tick[0] == self.reload_tick[1]:
                self.reload_tick[0] = 0
                self.is_reloading = False

    def can_shoot(self):

        if self.reload_tick[0] == 0:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

