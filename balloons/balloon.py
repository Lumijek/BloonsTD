import ast
import math
import pygame


class Balloon:
    def __init__(self, x=None, y=None, path_index=None):
        self.health = 1
        self.velocity = 100
        self.img = self.img = pygame.image.load(
            "images/balloon_images/greenballoon.png"
        ).convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (31, 35))
        self.path = []
        self.load()
        if not x:
            self.x = self.path[0][0]
            self.y = self.path[0][1]
            self.path_index = 0
        else:
            self.x = x
            self.y = y
            self.path_index = path_index
        self.ic = (self.x, self.y)
        self.move_distance = 0
        self.current_angle = 0
        self.damage = 1
        self.mask = pygame.mask.from_surface(self.img)
        self.id = None

    def load(self):
        path_coords = []
        with open("balloons/path.txt", "r") as f:
            for line in f:
                path_coords.append(line.strip())
        for coord in path_coords:
            self.path.append(ast.literal_eval(coord))

    def decrease_health(self, health_change):
        self.health -= health_change

    def draw(self, screen, delta_time):
        self.move(delta_time)
        screen.blit(self.img, (self.x - self.img.get_width() / 2, self.y - self.img.get_height() / 2))
        pygame.draw.circle(screen, "BLACK", (self.x, self.y), 3)
        # screen.blit(self.mask.to_surface(), (self.x - 11, self.y - 11))

    def show_path(self):
        return self.path

    def move(self, delta_time):
        x1, y1 = self.path[self.path_index]
        x2, y2 = self.path[self.path_index + 1]

        changex = x2 - x1
        changey = y2 - y1
        angle = math.atan2(changey, changex)

        self.x += math.cos(angle) * self.velocity * delta_time
        self.y += math.sin(angle) * self.velocity * delta_time
        self.current_angle = angle

        seg_dis_trav = math.sqrt((self.x - x1) ** 2 + (self.y - y1) ** 2)
        tot_seg_dis = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if seg_dis_trav > tot_seg_dis:
            self.path_index += 1
            if self.path_index == len(self.path) - 1:
                self.path_index = 0
                self.x, self.y = self.ic

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_x_velocity(self):
        return math.cos(self.current_angle) * self.velocity

    def get_y_velocity(self):
        return math.sin(self.current_angle) * self.velocity

    def get_velocity(self):
        return self.velocity

    def get_path_details(self):
        return self.path, self.path_index

    def is_collided(self, projectile_mask, projectile_coords):
        return not (
            projectile_mask.overlap(
                self.mask,
                (
                    self.x - self.img.get_width() / 2 - projectile_coords[0],
                    self.y - self.img.get_height() / 2 - projectile_coords[1],
                ),
            )
            == None
        )

    def is_killed(self):
        return (self.x, self.y, self.spawn, self.path_index)

