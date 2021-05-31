class Football:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.playerWBall = -1
        self.speed = 0.0
        self.HOrA = "X"
        self.matchStatus = "undefined"

    def populate(self, values):
        self.x = int(values[0])
        self.y = int(values[1])
        self.playerWBall = int(values[2])
        self.speed = float(values[3])
        self.HOrA = values[4]
        self.matchStatus = values[5]
