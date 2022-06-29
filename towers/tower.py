import math

from sqlalchemy import false

class Tower:
    def __init__(self, x, y):
        self.length = None
        self.height = None
        self.x = x
        self.y = y
        self.rangeR = None
        self.price = None
        self.damage = None

    def inRange(self, balloon_x, balloon_y):
        xDiff = balloon_x - self.x
        yDiff = balloon_y - self.y
        if xDiff ** 2 + yDiff ** 2 <= self.rangeR ** 2:
            return True
        else:
            return False

    def shoot(self, bullet, balloon):
        # if splash = true, will be called in here as well
        if self.inRange(balloon.getX(), balloon.getY()):
            bullet(balloon)

    def getX(self):
        return self.xCoord

    def getY(self):
        return self.yCoord
    '''Returns position vector at which to "send" the dart'''
    def bulletTarget(self, balloon):
        diffX = self.x - balloon.getX()
        diffY = self.y - balloon.getY()
        run = True
        count = 0
        while run:
            count+=1
            if (count*self.velocity) ** 2 >= diffX ** 2 + diffY ** 2:
                run = False
                diffX += balloon.getXVel()
                diffY += balloon.getYVel()
                return math.atan(abs(diffY/diffX))
            diffX += balloon.getXVel()
            diffY += balloon.getYVel()
            if count >= 5:
                run = false
                return 0
            
