import math
import pygame

from sqlalchemy import false

class Tower:
    def __init__(self, x, y):
        self.length = None
        self.height = None
        self.x = x
        self.y = y
        self.rangeR = 100
        self.price = None
        self.damage = None
        self.velocity = 2
        self.img = pygame.image.load("images/tower_images/tt.png")
        self.img = pygame.transform.scale(self.img, (60, 60))
        self.bx = x
        self.by = y
        self.angle = None


    def inRange(self, balloon):
        xDiff = balloon.getX() - self.x
        yDiff = balloon.getY() - self.y
        if xDiff ** 2 + yDiff ** 2 <= self.rangeR ** 2:
            return True
        else:
            return False

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def shoot(self, bullet, balloon):
        # if splash = true, will be called in here as well
        if self.inRange(balloon.getX(), balloon.getY()):
            bullet(balloon)

    def getX(self):
        return self.xCoord

    def getY(self):
        return self.yCoord

    def bulletTarget(self, balloon):
        diffX = balloon.getX() - self.x
        diffY = balloon.getY() - self.y
        run = True
        count = 0
        while run:
            count += 1

            if (count * self.velocity) ** 2 >= diffX ** 2 + diffY ** 2:
                run = False
                diffX += balloon.getXVel()
                diffY += balloon.getYVel()
                return math.atan2(diffY, diffX)
            diffX += balloon.getXVel()
            diffY += balloon.getYVel()
            if count >= 600:
                run = False
                return 0

    def shoot_bullet(self, balloon, screen):
        if self.inRange(balloon) and balloon.mark == False:
            self.angle = self.bulletTarget(balloon)
            balloon.mark = True

    def move_bullet(self):
        if self.angle != None:
            self.bx += math.cos(self.angle) * self.velocity
            self.by += math.sin(self.angle) * self.velocity

    def draw2(self, screen, balloon):
        if self.angle != None:
            print(math.degrees(self.angle))
        self.shoot_bullet(balloon, screen)
        pygame.draw.circle(screen, "BLACK", (self.bx, self.by), 5)
        self.move_bullet()





            
