from Football import Football
from Player import Player

import math
import statistics
import numpy

standingThreshold = 7
variableFrame = 20


class Helper:

    # min an max of field on x
    def findXMaxMin(self, matchData):
        i = 0
        xMax = 0
        xMin = 0
        while i < len(matchData):
            ballStatus2 = self.ballToObject(matchData[i])
            if ballStatus2.x <= xMin:
                xMin = ballStatus2.x
            if ballStatus2.x >= xMax:
                xMax = ballStatus2.x
            i += 1
        print("xMax:" + str(xMax) + " xMin: " + str(xMin))

    # min an max of field on y
    def findYMaxMin(self, matchData):
        i = 0
        yMax = 0
        yMin = 0
        while i < len(matchData):
            ballStatus2 = self.ballToObject(matchData[i])
            if ballStatus2.y <= yMin:
                yMin = ballStatus2.y
            if ballStatus2.y >= yMax:
                yMax = ballStatus2.y
            i += 1
        print("yMax:" + str(yMax) + " yMin: " + str(yMin))

    # ball speed min and max
    def findSpeedMaxMin(self, matchData):
        i = 0
        SpeedMax = 0
        SpeedMin = 0
        while i < len(matchData):
            ballStatus2 = self.ballToObject(matchData[i])
            if ballStatus2.speed <= SpeedMin:
                SpeedMin = ballStatus2.speed
            if ballStatus2.speed >= SpeedMax:
                SpeedMax = ballStatus2.speed
            i += 1
        print("SpeedMax:" + str(SpeedMax) + " SpeedMin: " + str(SpeedMin))

    # converts frame to player obj
    def playersToObj(self, frame):
        temp = frame.split(":")
        players = temp[1].split(";")
        players.pop()
        count = 0
        playerObjs = []
        for player in players:
            if count == len(players):
                break
            temp = player.split(",")
            p = Player()
            p.populate(temp)
            if p.teamId != 4:
                playerObjs.append(p)
            count += 1
        return playerObjs

        # get frame num

    def curntFrameNum(self, frame):
        temp = frame.split(":")
        return temp[0]

        # converts frame to ball obj

    def ballToObject(self, frame):
        temp = frame.split(":")
        temp = temp[2].split(";")
        data = temp[0].split(",")

        ball = Football()
        ball.populate(data)
        return ball

        # get frame id

    def frameId(self, frame):
        return frame.split(":")[0]

    # converts frame to player obj
    def splitPlayersTwoTeam(self, players, teamid):
        teamA = []
        teamB = []
        for player in players:
            if player.teamId == teamid:
                teamA.append(player)
            else:
                teamB.append(player)
        return [teamA, teamB]

    # Retrieves players split by Team
    def onAttackingSide(self, players, teamid):
        teamA = []
        teamB = []
        for player in players:
            if player.teamId == teamid:
                teamA.append(player)
            else:
                teamB.append(player)
                break
        return [teamA, teamB]

    # Retrievs all players who are in the defending half/ half the attackers are in
    def splitPitchAttackingSide(self, players, teamid, goalys, fistHalf):
        if goalys[0].teamId == teamid:
            if fistHalf == True:
                return self.playersOnRightSidePitch(players)
            else:
                return self.playersOnLeftSidePitch(players)
        else:
            if fistHalf == True:
                return self.playersOnLeftSidePitch(players)
            else:
                return self.playersOnRightSidePitch(players)

    # players on the right side of the pitch
    def playersOnRightSidePitch(self, players):
        rightSidePlayers = []
        for player in players:
            if player.x >= 0:
                rightSidePlayers.append(player)
        return rightSidePlayers

    # players on the left side of the pitch
    def playersOnLeftSidePitch(self, players):
        leftSidePlayers = []
        for player in players:
            if player.x <= 0:
                leftSidePlayers.append(player)
        return leftSidePlayers

    # finds colsets player to ball
    def findClosestToBall(self, frame):
        players = self.playersToObj(frame)
        ball = self.ballToObject(frame)
        closest = players[0]
        closestDis = math.sqrt(pow(ball.x - players[0].x, 2) + pow(ball.y - players[0].y, 2))
        for player in players:
            tempDistance = math.sqrt(pow(ball.x - player.x, 2) + pow(ball.y - player.y, 2))
            if tempDistance < closestDis:
                closestDis = tempDistance
                closest = player
        return closest

    # finds closets player to point
    def findClosestToPoint(self, frame, point):
        players = self.playersToObj(frame)
        closest = players[0]
        closestDis = math.sqrt(pow(point.x - players[0].x, 2) + pow(point.y - players[0].y, 2))
        for player in players:
            tempDistance = math.sqrt(pow(point.x - player.x, 2) + pow(point.y - player.y, 2))
            if tempDistance < closestDis:
                closestDis = tempDistance
                closest = player
        return closest

    # finds distance of closst player to ball
    def findClosestToBallDistance(self, frame):
        players = self.playersToObj(frame)
        ball = self.ballToObject(frame)
        closest = players[0]
        closestDis = math.sqrt(pow(ball.x - players[0].x, 2) + pow(ball.y - players[0].y, 2))
        for player in players:
            tempDistance = math.sqrt(pow(ball.x - player.x, 2) + pow(ball.y - player.y, 2))
            if tempDistance < closestDis:
                closestDis = tempDistance
                closest = player
        return closestDis

    # finds distance of closest player to point
    def findClosestToBallPoint(self, frame, point):
        players = self.playersToObj(frame)
        closest = players[0]
        closestDis = math.sqrt(pow(point.x - players[0].x, 2) + pow(point.y - players[0].y, 2))
        for player in players:
            tempDistance = math.sqrt(pow(point.x - player.x, 2) + pow(point.y - player.y, 2))
            if tempDistance < closestDis:
                closestDis = tempDistance
                closest = player
        return closestDis

        # finds distance of closest player to point

    # finds the closest players to a given player
    def findClosestPlayersToPlayer(self, target, players, amount):
        closestPlay = []
        i = 0
        while i < amount:
            closestPlayDis = 0.0
            tempClosest = Player()
            j = 0
            baseLine = False
            for player in players:
                if j == 0 or baseLine != True:
                    if i != 0:
                        part = False
                        for close in closestPlay:
                            if close.uId == player.uId:
                                part = True
                        if part == False:
                            baseLine = True
                            closestPlayDis = self.distanceBetweenTwoP(player.x, player.y, target.x, target.y)
                            tempClosest = player
                    else:
                        baseLine = True
                        tempClosest = player
                        closestPlayDis = self.distanceBetweenTwoP(player.x, player.y, target.x, target.y)
                else:
                    newDis = self.distanceBetweenTwoP(player.x, player.y, target.x, target.y)
                    if newDis < closestPlayDis:
                        if i != 0:
                            part = False
                            for close in closestPlay:
                                if close.uId == player.uId:
                                    part = True
                            if part == False:
                                closestPlayDis = newDis
                                tempClosest = player
                        else:
                            closestPlayDis = newDis
                            tempClosest = player
                j += 1
            closestPlay.append(tempClosest)
            i += 1
        return closestPlay

    #removes players for defence need to rename the function
    def removeToX(self,table,amount):
        defenders = []
        for row in table:
            tempDefence = row[1]
            for player in tempDefence:
                newDis = self.distanceBetweenTwoP(row[0].x, row[0].y, player.x, player.y)
                defenders.append([player.getUid(),newDis,row[0].getUid()])
        defUID =[]
        while True:
            if len(defenders) == 0:
                break
            tempDefUid =[]
            curentUID = defenders[0][0]
            for defence in defenders:
                if defence[0] == curentUID:
                    tempDefUid.append(defence)

            if len(tempDefUid) <= amount:
                for player in tempDefUid:
                    defUID.append(player)
                    defenders.remove(player)
            else:
                toAdd = []
                max = 0
                for player in tempDefUid:
                    defenders.remove(player)
                while len(toAdd) < amount:
                    for player in tempDefUid:
                        if tempDefUid.index(player) == 0:
                            max = player[1]
                            temp = player
                        elif player[1] < max:
                            max = player[1]
                            temp = player
                    toAdd.append(temp)
                    tempDefUid.remove(temp)
                for player in toAdd:
                    defUID.append(player)
        return defUID

    # marking score calculation
    def getMarkScore(self,table,pitch):
        score = 0
        count = 0
        while True:
            if len(table) == 0:
                break
            tempDefUid =[] #defenders
            count += 1
            curentUID = table[0][2] #get attaket uid
            for defence in table: #get all defenders marking that player
                if defence[2] == curentUID:
                    tempDefUid.append(defence)

            toAdd = []
            max = 0
            for player in tempDefUid:
                table.remove(player) #remove the instances of the player from the list
            #f (p1*sum(D/d/n))
            while len(tempDefUid) != 0: #sorth them by distance
                for player in tempDefUid:
                    if tempDefUid.index(player) == 0:
                        max = player[1]
                        temp = player
                    elif player[1] < max:
                        max = player[1]
                        temp = player
                toAdd.append(temp)
                tempDefUid.remove(temp)
            tempScore = 0
            i =1
            for player in toAdd:
                value = pitch.scleToRecorded(pitch.xRecordLimit)
                if value > player[1]:
                    #tempScore = tempScore + (player[1]*(len(toAdd) -i))/(value-(value-player[1]))
                    tempScore = (player[1]/i) #/ (value - (value - player[1]))
                    #tempScore = tempScore + (player[1]/i) / (value - (value - player[1]))
                    #tempScore = tempScore + 1 - ((player[1] / i) / (value - (value - player[1])))
                    #tempScore = tempScore + 1 - ((player[1] * (len(toAdd) - i)) / (value - (value - player[1])))
                else:
                    tempScore = tempScore + 0
                i += 1
            score += tempScore
        if count == 0:
            return 0
        return score/(count) #normilized

    # game still alive
    def isFrameAlive(self, frame):
        temp = frame.split(":")
        temp = temp[2].split(";")
        data = temp[0].split(",")
        return data[2]

    # finds how close the
    # team true for same team false for opistie
    def findTemateDensitiy(self, frame, high, team):
        density = -1
        players = self.playersToObj(frame)
        highstPlayer = players[0]
        teammates = players
        closestTeamToBall = self.findClosestToBall(frame)
        for player in players:
            if (player.teamId == closestTeamToBall.teamId) == team:
                for teammate in teammates:
                    if teammate.teamId == player.teamId:
                        teammate.setDistance(self.distanceBetweenTwoP(player.x, player.y, teammate.x, teammate.y))
            teammates.sort(key=lambda x: x.distance, reverse=True)
            count = 0
            for teammate in teammates:
                if teammate.distance == 0:
                    break
                else:
                    count += 1
            i = 0
            count -= 1
            tempDensity = 0
            while i < high:
                tempDensity += teammates[count - i].distance
                i += 1

            if density == -1:
                density = tempDensity
                highstPlayer = player
            elif tempDensity > density:
                density = tempDensity
                highstPlayer = player

        return [density, highstPlayer]

    # distance between two points
    def distanceBetweenTwoP(self, x1, y1, x2, y2):
        return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))

    # true return Bool, False return num
    # checks how many are split between the two sides from football
    def moreToOneSide(self, frame, previuesFrame, footballPitch, boolOrNum):
        ballStatus = self.ballToObject(frame)
        ballStatusPast = self.ballToObject(previuesFrame)
        players = self.playersToObj(frame)
        countL = 0
        countR = 0
        for player in players:
            if player.x < ballStatus.x:
                countL += 1
            else:
                countR += 1
        leftPre = 0
        rightPre = 0
        if (countL != 0):
            leftPre = (countL / (countL + countR)) * 100
        if (countR != 0):
            rightPre = (countR / (countL + countR)) * 100
        # print("Left% " + str(leftPre) + "  Right% "+ str(rightPre))
        speed = abs(ballStatus.speed - ballStatusPast.speed)
        # print("\n")
        if boolOrNum:
            ballare = (footballPitch.scaleToMeter(ballStatus.x) / footballPitch.xRecordLimit)
            if ((leftPre > 75 and ballare < -40) or (rightPre > 75 and ballare > 40)):
                print("aww yea")
                return True
            else:
                return False
        else:
            return [leftPre, rightPre]

    # true return Bool, False return num
    # checks how many are split between the two sides from football
    def moreToOneSideSimple(self, frame, footballPitch, boolOrNum):
        ballStatus = self.ballToObject(frame)
        players = self.playersToObj(frame)
        countL = 0
        countR = 0
        for player in players:
            if player.x < ballStatus.x:
                countL += 1
            else:
                countR += 1
        leftPre = 0
        rightPre = 0
        if (countL != 0):
            leftPre = (countL / (countL + countR)) * 100
        if (countR != 0):
            rightPre = (countR / (countL + countR)) * 100
        if boolOrNum:
            ballare = (footballPitch.scaleToMeter(ballStatus.x) / footballPitch.xRecordLimit)
            if ((leftPre > 75 and ballare < -40) or (rightPre > 75 and ballare > 40)):
                print("aww yea")
                return True
            else:
                return False
        else:
            return [leftPre, rightPre]

    #dead #alive [adva,Trailing]
    def isGameRestart(self, frame, previuesFrame):
        previuesStatus1 = self.ballToObject(previuesFrame) #dead
        frameStatus2 = self.ballToObject(frame) #alive
        if previuesStatus1.matchStatus == 'Dead':
            if frameStatus2.matchStatus == 'Alive':
                return True
            return False
        return False

    #alive #dead  [Trailing,adva]
    def isGameEnd(self, frame, NextFrame):
        frameStatus1 = self.ballToObject(frame)
        NextStatus2 = self.ballToObject(NextFrame)
        if frameStatus1.matchStatus == 'Alive':
            if NextStatus2.matchStatus == 'Dead':
                return True
            return False
        return False

    # avg spped of the playes
    def curentAvrageSpeed(self, frame):
        players = self.playersToObj(frame)
        speed = 0
        count = 0
        for player in players:
            if player.teamId == 0 or player.teamId == 1:
                speed += player.speed
                count += 1
        speed = speed / count
        return speed

    # gets frames before a restart (looks Back)
    def xFramesBeforeRestart(self, matchData, amount, start, deadPrecent):
        steps = 0  # how many steps forward to the game starting again
        while True:
            if (start - 1 - steps) < 0: # not less then zero
                return [False]
            trailFrame = matchData[start - steps]
            previuesFrame = matchData[start - 1 - steps]
            if self.isGameEnd(previuesFrame, trailFrame): #did the game end
                start = start - steps
                i = 1
                while i < amount:
                    if start - (i+1) >= 0:
                        trailing = matchData[start - (i - 1)]  # the one behind "Alive"
                        advancing = matchData[start - i]  # "dead"
                        if self.isGameRestart(trailing, advancing):
                            break
                        i += 1
                    else:
                        break
                before = i
                # Extract events
                mod = matchData[(start - before):start + math.floor(steps*deadPrecent)]
                return mod
            steps += 1

    # how many frames before the restart
    def DeadFramesBeforeRestart(self,matchData,start):
        steps = 0  # how many steps forward to the game starting again
        while True:
            if (start - 1 - steps) < 0:  # not less then zero
                return [False]
            trailFrame = matchData[start - steps]
            previuesFrame = matchData[start - 1 - steps]
            if self.isGameEnd(previuesFrame, trailFrame):  # did the game end
                mod = matchData[(start - steps):start]
                return mod
            steps += 1

    # the frame postion before the restart
    def pointBeforeRestart(self, matchData, start):
        steps = 0  # how many steps forward to the game starting again
        while True:
            if (start - 1 - steps) < 0:  # not less then zero
                return [False]
            trailFrame = matchData[start - steps]
            previuesFrame = matchData[start - 1 - steps]
            if self.isGameEnd(previuesFrame, trailFrame):  # did the game end
                start = start - steps
                return start
            steps += 1

    # fixed and good now 10/10 conf
    def xFramesAfterRestart(self, matchData, amount, start):
        steps = 0  # how many steps forward to the game starting againn
        while True:
            if (start + (1 + steps)) >= len(matchData)-1:  # checks if it is out of bounds
                return [False]
            trailFrame = matchData[start + steps]
            nextFrame = matchData[start + 1 + steps]
            if self.isGameRestart(nextFrame, trailFrame):  # game is restarted? if yes
                i = 1
                start = start + steps
                while i < amount:
                    if start + i <= len(matchData)-1:
                        trailing = matchData[start + (i - 1)]  # the one behind "Alive"
                        advancing = matchData[start + i]  # "dead"
                        if self.isGameEnd(trailing, advancing):
                            break
                        i += 1
                    else:
                        break
                after = i
                # Extract events
                mod = matchData[start:(start + after)]
                return mod
            steps += 1

    #fixed and good now 10/10 conf
    def xFramesBeforeAndAfter(self, before, matchData, after, mid):
        # find before stop
        i = 1
        while i < before:
            if mid - (i+1) >= 0:
                i += 1
            else:
                break
        before = i
        # find after stop
        i = 1
        while i < after:
            if mid + i <= len(matchData)-1:
                i += 1
            else:
                break
        after = i
        # Extract events
        mod = matchData[(mid - before):(mid + after)]
        return mod

    #fixed and good now 10/10 conf
    def xFramesBeforeAndAfterWithinMatch(self, before, matchData, after, mid):
        #find before stop
        i = 1
        while i < before:
            if mid - (i+1) >= 0:
                trailing = matchData[mid - (i-1)] # the one behind "Alive"
                advancing = matchData[mid - i] # "dead"
                if self.isGameRestart(advancing, trailing):
                    break
                i += 1
            else:
                break
        before = i
        #find after stop
        i = 1
        while i < after:
            if mid + i <= (len(matchData)-1):
                trailing = matchData[mid + (i - 1)]  # the one behind "Alive"
                advancing = matchData[mid + i]  # "dead"
                if self.isGameEnd(trailing, advancing):
                    break
                i += 1
            else:
                break
        after = i
        #Extract events
        mod = matchData[(mid - before):(mid + after)]
        return mod

    # did players restart positions by simple 50 /50 split
    def pitchReset(self, frames):
        for frame in frames:
            avgSpeed = self.curentAvrageSpeed(frame)
            if avgSpeed < standingThreshold:
                split = self.moreToOneSideSimple(frame, [], False)
                if split[0] <= 53.5 and split[0] >= 47.5:
                    # print("restart")
                    return True

    #did the ball cross the goal
    def ballCrossGoal(self, frames, footballPitch):
        i = 0
        goalPoints = footballPitch.getGoalPostPoints()
        goalP1 = [goalPoints[0], goalPoints[1]]
        while i < len(frames):
            curntBall = self.ballToObject(frames[i])
            ballP1 = [curntBall.x, curntBall.y]
            if self.behindGoal(goalP1, ballP1):
                return True
            i += 1
        return False

    # did the ball cross the goal + some extra space
    def ballCrossGoalPlus(self, frames, footballPitch, extra):
        i = 0
        add = footballPitch.scleToRecorded(extra)
        goalPoints = footballPitch.getGoalPostPoints()
        goalP1 = [goalPoints[0], goalPoints[1] + add]
        while i < len(frames):
            if isinstance(frames, list) == False:
                curntBall = self.ballToObject(frames)
            else:
                curntBall = self.ballToObject(frames[i])
            ballP1 = [curntBall.x, curntBall.y]
            if self.behindGoal(goalP1, ballP1):
                return True
            i += 1
        return False

    # did the ball cross the goal + some extra space
    def ballinGoalPlus(self, ball, footballPitch, extra):
        i = 0
        add = footballPitch.scleToRecorded(extra)
        goalPoints = footballPitch.getGoalPostPoints()
        goalP1 = [goalPoints[0], goalPoints[1] + add]

        ballP1 = [ball.x, ball.y]
        if self.behindGoal(goalP1, ballP1):
            return True
        return False

    #is ball behined the goal?
    def behindGoal(self, goalP1, ballP1):
        if (ballP1[0] < 0):
            if (ballP1[0] < -goalP1[0] and ballP1[1] < goalP1[1] and ballP1[1] > -goalP1[1]):
                return True
        else:
            if (ballP1[0] > goalP1[0] and ballP1[1] < goalP1[1] and ballP1[1] > -goalP1[1]):
                return True
        return False

    # convers the frame to a time stamp
    def frameToTime(self, frame, timestamps):
        current = int(self.curntFrameNum(frame))
        diff = 0
        # if current > secondHalf:
        #    return 45 + (((current - firstFrame) - (secondHalf - firstFrame))/25)/60
        # else:
        #    return (((current-firstFrame) - (fistHalf-firstFrame))/25)/60
        fistHalf = timestamps[0]
        secondHalf = timestamps[1]
        firstFrame = timestamps[2]

        if current < secondHalf:
            return (current - fistHalf) / 60 / 25
        else:
            return ((current - fistHalf) / 60 / 25) #+ 45 + 15

    #chancge in ball speed
    def findBallSpeedChange(self, frame, nextFrame):
        ball1 = self.ballToObject(frame)
        ball2 = self.ballToObject(nextFrame)
        speed = ball1.speed - ball2.speed
        return speed

    #Assosiates an event to a team
    def witchTeamIsAssosiated(self,frame,footballPitch,timeframes,goaly):
        #players = self.playersToObj(frame)
        team = self.findClosestToBall(frame)

        firsthalf = True
        if int(self.frameId(frame)) >= int(timeframes[1]):
            firsthalf = False

        quadrant = footballPitch.whatQuadrantI(team.x,2)
        if firsthalf:
            if quadrant == 0:
                if team.teamId == goaly[1].teamId:
                    return goaly[0].teamId
                else:
                    return goaly[1].teamId
            if quadrant == 1:
                if team.teamId == goaly[1].teamId:
                    return goaly[1].teamId
                else:
                    return goaly[0].teamId
        else:
            if quadrant == 0:
                if team.teamId == goaly[1].teamId:
                    return goaly[1].teamId
                else:
                    return goaly[0].teamId
            if quadrant == 1:
                if team.teamId == goaly[0].teamId:
                    return goaly[0].teamId
                else:
                    return goaly[1].teamId

    # is the nearest plaer to the ball an attacking player
    def isTheNererstPlayerAttacking(self,frame,footballPitch,timeframes,goaly):
        team = self.findClosestToBall(frame)

        firsthalf = True
        if int(self.frameId(frame)) >= int(timeframes[1]):
            firsthalf = False

        quadrant = footballPitch.whatQuadrantI(team.x,2)
        if firsthalf:
            if quadrant == 0:
                if team.teamId == goaly[1].teamId:
                    return False
                else:
                    return True
            if quadrant == 1:
                if team.teamId == goaly[0].teamId:
                    return False
                else:
                    return True
        else:
            if quadrant == 0:
                if team.teamId == goaly[0].teamId:
                    return False
                else:
                    return True
            if quadrant == 1:
                if team.teamId == goaly[1].teamId:
                    return False
                else:
                    return True

    #cleans the data of unsutible fetures / duplicates
    def cleanData(self,data,matchData):
        i = 0
        returnPoints = []
        cut = []
        for point in data:
            returnPoints.append(point)
        while i < len(data):
            frames = self.xFramesBeforeAndAfterWithinMatch(60, matchData, 60, data[i].getmatchDataPostion())
            if len(frames) < 3:
                cut.append(data[i])
            i += 1
        for point in cut:
            returnPoints.remove(point)
        return returnPoints

    # was the ball stat still for X seconds
    def wasBallStillForX(self,frames,X,still):
        i = 0
        for frame in frames:
            ball = self.ballToObject(frame)
            wasStill =False
            if abs(ball.speed) < still:
                i += 1
                wasStill = True
            if wasStill == False:
                i = 0
            if i > X:
                return True
        return False

    #mean, median, mode, std divation, range,
    def MMMSTDR1(self,points):
        points.sort()
        mean = sum(points)/len(points)
        median = points[math.floor((len(points)/2))]
        mode = statistics.mode(points)
        stDev = statistics.stdev(points)
        variance = statistics.variance(points)
        range = points[(len(points)-1)]- points[0]
        return [mean,median,mode,stDev,range]

        ############################################################
        # comprstion of quadrants

    #get the denstiy A attribute
    def getCompressedDensityA(self, quadrants):
        change = []
        numOfQuad = len(quadrants)
        change = self.getDensityA(quadrants)
        if len(change) == 0:
            print("o no")
        change = self.MMMSTDR1(change)
        return change

############################################################################################
    # densistiy A , attacking pressure + defending pressure attributes
    # get the compressed quadrants in a given direction attribute
    def getCompressedQuadrantsOneDir(self, dir, quadrants):
        numOfQuad = len(quadrants)
        pergroup = math.floor(numOfQuad / 3)
        initalChange = self.getChangeOneWay(quadrants[0:pergroup], dir)
        midChange = self.getChangeOneWay(quadrants[pergroup:(pergroup * 2)], dir)
        endChange = self.getChangeOneWay(quadrants[(pergroup * 2):len(quadrants)], dir)
        totalChange = (initalChange + midChange + endChange) / 3
        return [initalChange, midChange, endChange, totalChange]

    def getDensityA(self, points):
        i = 0
        change = []
        sumcalk = []
        for instance in points:
            calk = 0
            split = len(instance)
            i = 0
            for val in instance:
                if i < split / 2:
                    present = (split / 2 + (i + 1)) / split
                    calk = calk + (present * (-1 * val))
                if i >= split / 2:
                    present = (i + 1) / split
                    calk = calk + (present * (1 * val))
                i += 1
            sumcalk.append(calk)
        return sumcalk

    def getChange(self, points):
        i = 0
        change = []
        while i < len(points):
            instance = []
            j = 0
            if i + 1 == len(points):
                break
            for val in points[i]:
                instance.append((val - points[i + 1][j]))
                j += 1
            change.append(instance)
            i += 1

        sumcalk = []
        for instance in change:
            calk = 0
            split = len(instance)
            i = 0
            for val in instance:
                if i < split / 2:
                    present = (split / 2 + (i + 1)) / split
                    calk = calk + (present * (-1 * val))
                if i >= split / 2:
                    present = (i + 1) / split
                    calk = calk + (present * (1 * val))
                i += 1
            sumcalk.append(calk)
        if sum(sumcalk) == 0:
            return 0
        retunVal = sum(sumcalk) / len(sumcalk)
        return retunVal

    def getChangeLeft(self, points):
        i = 0
        change = []
        while i < len(points):
            instance = []
            j = 0
            if i + 1 == len(points):
                break
            curentValues = points[i][::-1]
            netValues = points[i + 1][::-1]
            for val in curentValues:
                instance.append((val - netValues[j]))
                j += 1
            change.append(instance)
            i += 1
        return change

    def getChangeRight(self, points):
        i = 0
        change = []
        while i < len(points):
            instance = []
            j = 0
            if i + 1 == len(points):
                break
            for val in points[i]:
                instance.append((val - points[i + 1][j]))
                j += 1
            change.append(instance)
            i += 1
        return change

    def getChangeOneWay(self, points, Direction):
        if Direction == 1:
            change = self.getChangeRight(points)
        else:
            change = self.getChangeLeft(points)

        sumcalk = []
        for instance in change:
            calk = 0
            split = len(instance)
            i = 0
            for val in instance:
                present = (i + 1) / split
                calk = calk + (present * (1 * val))
                i += 1

            sumcalk.append(calk)
        if sum(sumcalk) == 0:
            return 0
        retunVal = sum(sumcalk) / len(sumcalk)
        return retunVal

