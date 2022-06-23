import math
class Tower:
    def __init__(self,length,height,xCoord,yCoord,rangeR,price,splash):
        self.length = length
        self.height = height
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.rangeR = rangeR
        self.price = price
        self.splash = splash
    def inRange(self, balloonX, balloonY):
        xDiff = abs(balloonX-self.xCoord)
        yDiff = abs(balloonY-self.yCoord)
        if math.sqrt(xDiff**2 + yDiff**2)<=self.rangeR:
            return True
        else:
            return False
    def splashRange(self,balloonX, balloonY,splashR):
        