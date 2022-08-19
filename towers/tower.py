import math
import pygame


class Tower:
    img = pygame.image.load("images/tower_images/tt.png")
    img = pygame.transform.smoothscale(img, (60, 60))
    t_range = 100
    circ_img = pygame.Surface((t_range * 2, t_range * 2))
    pygame.draw.circle(circ_img, (0, 0, 1), (t_range, t_range), t_range)
    circ_img.set_colorkey("Black")
    circ_img.set_alpha(100)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.price = None
        self.damage = None
        self.img.convert_alpha()
        self.drawnImg = self.img
        self.nr = self.drawnImg.get_rect(center= (self.x, self.y))
        self.time_since_reload = 0  # time since last shot
        self.reload_time = 0.5
        self.is_reloading = False
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.range_mask = pygame.mask.from_surface(self.circ_img)
        self.id = [__class__.__name__]
        self.place_circ = False
        self.rotate_m = False
        self.angle = 0

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

    def reload(self, dt):
        self.time_since_reload += dt

    def can_shoot(self):

        if self.time_since_reload >= self.reload_time:
            self.time_since_reload = 0
            self.reloading = True
            return True
        return False

    def draw(self, screen):
        if self.place_circ:
            screen.blit(
                self.circ_img,
                (
                    self.x - self.circ_img.get_width() / 2,
                    self.y - self.circ_img.get_width() / 2,
                ),
            )
        if self.rotate_m:
            self.drawnImg, self.nr = self.rot()
            self.angle = 0
        screen.blit(self.drawnImg, self.nr)

    def get_center_x(self):
        return self.x - 10

    def get_center_y(self):
        return self.y - 10

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
    
    def projFired(self, angle):
        self.angle = angle
        self.rotate_m = True

    def rot(self):
        rotImg = pygame.transform.rotozoom(self.img, -math.degrees(self.angle-90), 1)
        newR=rotImg.get_rect(center = self.img.get_rect(center=(self.x, self.y)).center)
        self.rotate_m = False
        return rotImg, newR
