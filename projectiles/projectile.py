import math
import pygame


class Projectile:
    def __init__(self, starting_x, starting_y):
        self.x = starting_x
        self.y = starting_y
        self.velocity = 20
        self.img = None
        self.angle = None
        self.tot_dis = 300
        self.dis_traveled = 0

    def projectile_target(self, balloon):
        diffX = balloon.get_x() - self.x
        diffY = balloon.get_y() - self.y
        run = True
        count = 0
        while run:

            count += 1

            if (count * self.velocity) ** 2 >= diffX**2 + diffY**2:
                run = False
                diffX += balloon.get_x_velocity()
                diffY += balloon.get_y_velocity()
                self.angle = math.atan2(diffY, diffX)

            diffX += balloon.get_x_velocity()
            diffY += balloon.get_y_velocity()
            if count >= 600:
                run = False
                self.angle = 0

    def show_dis(self, balloon):
        return math.sqrt(
            (balloon.get_x() - self.x) ** 2 + (balloon.get_y() - self.y) ** 2
        )

    def move_projectile(self):
        if self.angle != None:
            self.x += math.cos(self.angle) * self.velocity
            self.y += math.sin(self.angle) * self.velocity
            self.dis_traveled += self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, "BLACK", (self.x, self.y), 5)
        self.move_projectile()

    def projectile_dead(self):
        if self.dis_traveled >= self.tot_dis:
            return True
        return False