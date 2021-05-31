centerSpot = 9.15

class PitchDetails:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.xRecordLimit = 0.0
        self.yRecordLimit = 0.0
        self.scale = 50
        self.reduceByX = 0.0
        self.reduceByY = 0.0
        self.goalSize = 7.3152 #in Meters

    def populate(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def populateFull(self, data):
        self.x = float(data[0])
        self.y = float(data[1])
        self.xRecordLimit = float(data[2])
        self.yRecordLimit = float(data[3])
        self.reduceByX = self.xRecordLimit - self.x
        self.reduceByY = self.yRecordLimit - self.y

    def inArea(self, x1, y1, size, x2, y2):
        cornerXPos = (x1 + size)
        cornerXNeg = (x1 - size)
        cornerYPos = (y1 + size)
        cornerYNeg = (y1 - size)
        if (x2 <= cornerXPos) and (x2 >= cornerXNeg):
            if (y2 <= cornerYPos) and (y2 >= cornerYNeg):
                return True
            return False
        return False

    def ballInCorner(self, ball):
        ballX = self.scaleToMeter(ball.x)
        ballY = self.scaleToMeter(ball.y)
        if self.inArea(self.x, self.y, 2, ballX, ballY):
            return True
        if self.inArea(-self.x, self.y, 2, ballX, ballY):
            return True
        if self.inArea(-self.x, -self.y, 2, ballX, ballY):
            return True
        if self.inArea(self.x, -self.y, 2, ballX, ballY):
            return True
        return False

    def scaleToMeter(self, cor):
        if cor < 0:
            newCor = (cor / self.scale) #+ self.reduceByX
        else:
            newCor = (cor / self.scale) #- self.reduceByX
        return newCor

    def scleToRecorded(self, value):
        if value < 0:
            newValue = (value * self.scale) #+ self.reduceByX
        else:
            newValue = (value * self.scale) #- self.reduceByX
        return newValue

    def scaleToMeterY(self, cor):
        if cor < 0:
            newCor = (cor / self.scale) #+ self.reduceByY
        else:
            newCor = (cor / self.scale) #- self.reduceByY
        return newCor

    def scleToRecordedY(self, value):
        if value < 0:
            newValue = (value * self.scale) #+ self.reduceByY
        else:
            newValue = (value * self.scale) #- self.reduceByY
        return newValue

    def getGoalPostPoints(self):
        y1 =self.scleToRecordedY(self.goalSize/2)
        x = self.scleToRecorded(self.x -1)
        y2 =self.scleToRecordedY(-self.goalSize/2)
        return [x,y1,x,y2] # X1 Y1 X2,Y2

    def BallCloseToCenter(self, ball):
        area = self.scleToRecorded(centerSpot+1)
        if self.scleToRecorded(centerSpot+1) > ball.x > -self.scleToRecorded(centerSpot+1):
            if self.scleToRecorded(centerSpot+1) > ball.y > -self.scleToRecorded(centerSpot+1):
                return True
            return False
        return False

    def isOutOfBounds(self,ball):
        if ball.x > self.scleToRecorded(self.x) or ball.x < - self.scleToRecorded(self.x):
            return True
        if ball.y > self.scleToRecorded(self.y) or ball.y < - self.scleToRecorded(self.y):
            return True
        return False

    def whatQuadrantI(self, posx, i):
        x = self.scleToRecorded(self.xRecordLimit)
        split = (x*2)/i
        j = 0
        # is this needed?
        if posx == (split/2)*i:
            return i-1

        while j < (i/2):
            if split*j <= posx and split*(j+1) >= posx:
                return int(i/2) + j
            if -split*j >= posx and -split*(j+1) <= posx:
                return int(i/2) - (j+1)#3-j
            j += 1
        print("hello: "+str(posx)) #should never see this
        return j