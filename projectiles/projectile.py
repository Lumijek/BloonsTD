import math
import pygame


class Projectile:
    def __init__(self, starting_x, starting_y):
        self.x = starting_x
        self.y = starting_y
        self.velocity = 15
        self.img = None
        self.angle = None

    def projectile_target(self, balloon, verbose=False):
        diffX = balloon.getX() - self.x
        diffY = balloon.getY() - self.y
        run = True
        count = 0
        while run:

            count += 1

            if (count * self.velocity) ** 2 >= diffX**2 + diffY**2:
                run = False
                diffX += balloon.getXVel()
                diffY += balloon.getYVel()
                self.angle = math.atan2(diffY, diffX)

            diffX += balloon.getXVel()
            diffY += balloon.getYVel()
            if count >= 600:
                if verbose == True:
                    print(diffX, diffY)
                run = False
                self.angle = 0

    def show_dis(self, balloon):
        return math.sqrt(
            (balloon.getX() - self.x) ** 2 + (balloon.getY() - self.y) ** 2
        )

    def move_projectile(self):
        if self.angle != None:
            self.x += math.cos(self.angle) * self.velocity
            self.y += math.sin(self.angle) * self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, "BLACK", (self.x, self.y), 5)
        self.move_projectile()
