import math
import pygame

class Tower:
    img = pygame.image.load("images/tower_images/tt.png")
    img = pygame.transform.smoothscale(img, (60, 60))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.price = None
        self.damage = None
        #self.img = pygame.image.load("images/tower_images/tt.png").convert_alpha()
        #self.img = pygame.transform.scale(self.img, (60, 60))
        self.img.convert_alpha()
        self.reload_tick = [0, 20]  # number of frames to wait before shooting again
        self.is_reloading = False
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.circ_img = pygame.Surface((self.range * 2, self.range * 2))
        pygame.draw.circle(self.circ_img, "GREY", (self.range, self.range), self.range)
        self.circ_img.set_alpha(120)
        self.range_mask = pygame.mask.from_surface(self.circ_img)

    def in_range(self, balloon_mask, balloon_coords):
        return not (
            balloon_mask.overlap(
                self.range_mask,
                (
                    self.x - self.circ_img.get_width() / 2 - balloon_coords[0],
                    self.y - self.circ_img.get_height() / 2 - balloon_coords[1],
                ),
            )
            == None
        )

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
        screen.blit(self.circ_img, (self.x - self.circ_img.get_width() / 2, self.y - self.circ_img.get_width() / 2))
        screen.blit(self.img, (self.x - self.width / 2, self.y - self.height / 2))

    def get_center_x(self):
        return self.x - 10

    def get_center_y(self):
        return self.y - 10

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
