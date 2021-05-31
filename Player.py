class Player:
    def __init__(self):
        self.teamId = 0
        self.uId = 0
        self.backNum = 0
        self.x = 0.0
        self.y = 0.0
        self.speed = 0.0
        self.distance = -1

    def populate(self, values):
        self.teamId = int(values[0])
        self.uId = int(values[1])
        self.backNum = int(values[2])
        self.x = int(values[3])
        self.y = int(values[4])
        self.speed = float(values[5])

    #
    def setDistance(self,dis):
        self.distance =dis

    def getUid(self):
        return self.uId
