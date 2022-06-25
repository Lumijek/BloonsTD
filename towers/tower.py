import math


class Tower:
    def __init__(self, length, height, xCoord, yCoord, rangeR, price, splash, damage):
        self.length = length
        self.height = height
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.rangeR = rangeR
        self.price = price
        self.splash = splash
        self.damage = damage

    def inRange(self, balloonX, balloonY):
        xDiff = balloonX - self.xCoord
        yDiff = balloonY - self.yCoord
        if xDiff**2 + yDiff**2 <= self.rangeR**2:
            return True
        else:
            return False

    # Thinking about this still
    """def splashRange(self,balloonX, balloonY,splashR):
        if self.splash:
            return True
        else:
            return False"""

    def shoot(self, bullet, balloon):
        # if splash = true, will be called in here as well
        if self.inRange(balloon.getX(), balloon.getY()):
            bullet(balloon)

    def getX(self):
        return self.xCoord

    def getY(self):
        return self.yCoord
