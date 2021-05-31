import math


class PointOfInterest:
    def __init__(self, frame, type, pos, timestamp):
        # the team that the event is assigned to
        self.teamIdToEvent = 0

        # the frame at witch the conditions were met
        self.frame = frame
        # the event Type
        self.type = type

        # the quadrants of players
        # the Density A attribute
        self.quadrants = []
        # team associated with Quadrants
        self.quadrantsTeamId = -1
        # the quadrants of players compressed
        # normalized Density A attribute
        self.compressedQ = []

        # Attack Flow
        self.quadrantsAttackers = []
        self.attackingId = -1
        self.attackDir = 3
        self.compressedQAttack = []

        # Defence Flow
        self.quadrantsDefenders = []
        self.defendingId = -1
        self.defendingDir = 3
        self.compressedQDefence = []

        # eratic measure attribute
        self.eratic = []
        # marking mean mode
        self.MarkingMMMSTDR1 = 0

        # matchData[matchDataPostion]
        self.matchDataPostion = pos
        # frame id
        self.frameNum = 0
        # the time it occurred at
        self.timestamp = timestamp

    ############################################################
    # the team that the event is assigned to
    def setTeamIdToEvent(self, id):
        self.teamIdToEvent = id

    def getTeamIdToEvent(self):
        return self.teamIdToEvent

    ############################################################
    # the frame at witch the conditions were met
    def getFrame(self):
        return self.frame

    ############################################################
    # the quadrants of players
    # the Density A attribute

    def populateQuadrants(self, populateQuadrants,teamId):
        self.quadrants = populateQuadrants
        self.quadrantsTeamId = teamId

    def getQuadants(self):
        return self.quadrants

    def setcompressedQ(self, compressedQ):
        self.compressedQ = compressedQ

    def getcompressedQ(self):
        return self.compressedQ

    ############################################################
    # Attack Flow

    def populateQuadrantsAttackers(self, quatrants):
        self.quadrantsAttackers = quatrants

    def getQuadrantsAttackers(self):
        return self.quadrantsAttackers

    def setCompressedQAttackers(self, compressedQ):
        self.compressedQAttack = compressedQ

    def getCompressedQAttackers(self):
        return self.compressedQAttack

    def setAttackingId(self,attackerId, attackDirection):
        self.attackingId = attackerId
        self.attackDir = attackDirection

    def getAttackingId(self):
        return self.attackingId

    def getAttackingDir(self):
        return self.attackDir

    ############################################################
    #Defence

    def populateQuadrantsDefenders(self, quatrants):
        self.quadrantsDefenders = quatrants

    def getQuadrantsDefenders(self):
        return self.quadrantsDefenders

    def setCompressedQDefenders(self, compressedQ):
        self.compressedQDefence = compressedQ

    def getCompressedQDefenders(self):
        return self.compressedQDefence

    def setDefendersId(self, DefenderId, defendingDirection):
        self.defendingId = DefenderId
        self.defendingDir = defendingDirection

    def getDefendersId(self):
        return self.defendingId

    def getDefendersDir(self):
        return self.defendingDir

    ############################################################
    #Marking

    def setMarking(self,MMMSTDR1):
        self.MarkingMMMSTDR1 = MMMSTDR1

    def getMarking(self):
        return self.MarkingMMMSTDR1

    ############################################################
    #Frame Num
    def setFrameNum(self, framenum):
        self.frameNum = framenum

    def getFrameNum(self):
        return self.frameNum

    ############################################################
    #Erratic

    def setEratic(self,x,y,s,total):
        self.eratic = [x,y,s,total]

    def getEratic(self):
        return self.eratic

    ############################################################
    #Helpfull Small Functions

    def setmatchDataPostion(self,pos):
        self.matchDataPostion = pos

    def getmatchDataPostion(self):
        return self.matchDataPostion

    def getTimestamp(self):
        return self.timestamp

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    def getType(self):
        return self.type

