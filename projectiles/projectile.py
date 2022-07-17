import math
import numpy as np
import pygame


class Projectile:
    def __init__(self, starting_x, starting_y):
        self.x = starting_x
        self.y = starting_y
        self.velocity = 500
        self.img = pygame.image.load("images/projectile_images/d1.png")
        self.img = pygame.transform.scale(
            self.img, (self.img.get_width() * 0.4, self.img.get_height() * 0.4)
        )
        self.img = pygame.transform.rotate(self.img, -130)
        self.angle = None
        self.tot_dis = 300
        self.dis_traveled = 0
        self.dead = False

    def projectile_target(self, balloon, path, path_index, delta_time):
        rangeBX = balloon.get_x()
        rangeBY = balloon.get_y()
        diffX = rangeBX - self.x
        diffY = rangeBY - self.y
        run = True
        count = 0
        while run:

            count += 1

            if (count * self.velocity * delta_time) ** 2 >= diffX**2 + diffY**2:
                run = False
                diffX += balloon.get_x_velocity() * delta_time
                diffY += balloon.get_y_velocity() * delta_time
                tempX = rangeBX + balloon.get_x_velocity() * (count) * delta_time
                tempY = rangeBY + balloon.get_y_velocity() * (count) * delta_time
                if self.inCheck(
                    path[path_index][0],
                    path[path_index][1],
                    path[path_index + 1][0],
                    path[path_index + 1][1],
                    tempX,
                    tempY,
                ):
                    self.angle = math.atan2(diffY, diffX)
                    self.img = pygame.transform.rotate(
                        self.img, -math.degrees(self.angle)
                    )
                    self.mask = pygame.mask.from_surface(self.img)
                    return True

                else:
                    return False

            diffX += balloon.get_x_velocity() * delta_time
            diffY += balloon.get_y_velocity() * delta_time
            if count >= 600:
                run = False
                self.angle = 0
                print("here")

    def show_dis(self, balloon):
        return math.sqrt(
            (balloon.get_x() - self.x) ** 2 + (balloon.get_y() - self.y) ** 2
        )

    def move_projectile(self, delta_time):
        if self.angle != None:
            self.x += math.cos(self.angle) * self.velocity * delta_time
            self.y += math.sin(self.angle) * self.velocity * delta_time
            self.dis_traveled += self.velocity * delta_time

    def draw(self, screen, delta_time):
        screen.blit(self.img, (self.x, self.y))
        self.move_projectile(delta_time)

    def projectile_dead(self):
        if self.dis_traveled >= self.tot_dis or self.dead == True:
            return True
        return False

    def inCheck(self, x1, y1, x2, y2, x, y):
        if x > max(x1, x2) or x < min(x1, x2):
            return False
        elif y > max(y1, y2) or y < min(y1, y2):
            return False
        else:
            return True

    def get_mask(self):
        return self.mask

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def kill_projectile(self):
        self.dead = True
