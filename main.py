import math
from random import seed

from numpy.random.mtrand import randint
from tensorflow.python.keras.applications.densenet import layers

from Grapher import Grapher
from Football import Football
from Helper import Helper
from SaveLoad import SaveLoad
from PitchDetails import PitchDetails
from PointOfInterest import PointOfInterest
from lineCrossing import lineCrossing
import numpy as np
from numpy import ones,vstack
from numpy.linalg import lstsq
import math

#TesorFlow Model impoerts
import tensorflow as tf
import pathlib
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#change this to alter the rounding on tenserflow data
np.set_printoptions(precision=4)

# setup
helper = Helper()
dataHandler = SaveLoad()
grap = Grapher()

fileNames = 'yourDevice/DataExtractor/Files.txt'
dataAddress = 'yourDevice/soccer data/'
metaDataAddress = 'yourDevice/soccer data/'
RANDOMEVENTS = 20
DensityASplitCount = 6
INFINITY = 10000
CHANCEBGoalExtra = 5 # in metter
CHANCEBClosestDisRemoval = 10 # in metter

def readDocs():
    fileNamesFile = open(fileNames, 'r')
    fileNamesList = fileNamesFile.readlines()

    for filename in fileNamesList:
        if filename != "END":
            filename = filename[0:(len(filename)-1)]
            dataLocation = dataAddress + filename + "/" + filename[1:len(filename)] + ".dat"
            metaDataLocation = metaDataAddress + filename + "/" + filename[1:len(filename)] + "_metadata.xml"
            readOneDoc(dataLocation,metaDataLocation,filename)

def testExtractionEvents():
    fileNamesFile = open(fileNames, 'r')
    fileNamesList = fileNamesFile.readlines()
    i = 0
    for filename in fileNamesList:
        if i ==1:
            break
        i+=1
        filename = filename[0:(len(filename) - 1)]
        dataLocation = dataAddress + filename + "/" + filename[1:len(filename)] + ".dat"
        metaDataLocation = metaDataAddress + filename + "/" + filename[1:len(filename)] + "_metadata.xml"
        readOneDoc(dataLocation, metaDataLocation, filename)

def attributeExtractionStart():
    fileNamesFile = open(fileNames, 'r')
    fileNamesList = fileNamesFile.readlines()
    attributes = dataHandler.loadAllObjects()
    for filename in fileNamesList:
        if filename != "END":
            filename = filename[0:(len(filename) - 1)]
            dataLocation = dataAddress + filename + "/" + filename[1:len(filename)] + ".dat"
            metaDataLocation = metaDataAddress + filename + "/" + filename[1:len(filename)] + "_metadata.xml"
            attributesUpdata(dataLocation, metaDataLocation, filename,attributes)

def metaDataExtraction(dataLocation,metaDataLocation):
    # opens the metaDataFile extracts info needed.
    file1 = open(metaDataLocation, 'r')
    metadataLine = file1.readlines()
    fieldInfo = []
    footballPitch = PitchDetails()
    metadata = metadataLine[0].split()
    temp = metadata[6].split('"')
    fieldInfo.append(float(temp[1]))
    temp = metadata[7].split('"')
    fieldInfo.append(float(temp[1]))
    temp = metadata[8].split('"')
    fieldInfo.append(float(temp[1]))
    temp = metadata[9].split('"')
    fieldInfo.append(float(temp[1]))
    footballPitch.populateFull(fieldInfo)

    # metadata on halfs of match time
    temp = metadata[11].split('"')
    firstHalfStart = int(temp[1])
    temp = metadata[14].split('"')
    secondHalfStart = int(temp[1])
    timeframes = [firstHalfStart, secondHalfStart]
    print("1 start " + str(firstHalfStart))
    print("2 start " + str(secondHalfStart))

    file1 = open(dataLocation, 'r')
    count = 0

    while True:
        count += 1
        # Get next line from file
        line = file1.readline()
        curentFrame = line.split(":")
        if count == 1:
            timeframes.append(int(curentFrame[0]))
        if int(curentFrame[0]) == firstHalfStart:
            break
        # end of file is reached
        if not line:
            break

    file1 = open(dataLocation, 'r')
    # start of data extraction
    allMatchData = file1.readlines()
    matchData = allMatchData[count::25]  # 25 frames per second

    # Goalys
    goalys = getGoalys(matchData)
    # Events Goals
    file1.close()
    return [matchData,footballPitch,timeframes,goalys]

def readOneDoc(dataLocation,metaDataLocation,filename):
    metadataInfo = metaDataExtraction(dataLocation,metaDataLocation)
    dataHandler.saveObjects(extractFeatures(metadataInfo[0], metadataInfo[1],metadataInfo[2],metadataInfo[3]),filename)

def attributesUpdata(dataLocation,metaDataLocation,filename,attributes):
    metadataInfo = metaDataExtraction(dataLocation, metaDataLocation)
    for elm in attributes:
        if elm[0] == filename:
            dataHandler.saveObjects(attributeExtraction(elm[1][1],elm[1][0],metadataInfo[0], metadataInfo[1], metadataInfo[2], metadataInfo[3]),
                            filename)


#time frames [0] firstHalfStart [1] secondhalfStart [2] first frame of match
#matchData all the data of the match in play
#footballPitch, dimensions of the pitch and info on the pitch + functions
#starting goalys [0] right side, [1] left side
def extractFeatures(matchData,footballPitch,timeframes,startingGoalys):
    helper.findXMaxMin(matchData)
    helper.findYMaxMin(matchData)
    helper.findSpeedMaxMin(matchData)
    i = 0
    intresting = []
    goals = []
    print("extracting Events")
    while i < len(matchData):
        if i != 0:
            # Corrners
            if isCorner(matchData[i], matchData[i - 1], footballPitch,timeframes, startingGoalys):
                intresting.append(PointOfInterest(matchData[i], 1, i, helper.frameToTime(matchData[i],timeframes)))

            # FreeKick
            if isFreeKick(i, matchData[i], matchData[i - 1], matchData, footballPitch, timeframes, startingGoalys):
                intresting.append(PointOfInterest(matchData[i], 2, i, helper.frameToTime(matchData[i],timeframes)))

            # goals
            goals = isGoal(i, footballPitch, matchData, goals, timeframes)

            # isShotOnGoal
            if isShotOnGoal(i,footballPitch,matchData[i]):
                intresting.append(PointOfInterest(matchData[i], 3, i, helper.frameToTime(matchData[i],timeframes)))

            # isShotOnGoal2
            if isShotOnGoal2(i,footballPitch,matchData[i], matchData[i - 1],startingGoalys,timeframes):
                intresting.append(PointOfInterest(matchData[i], 4, i, helper.frameToTime(matchData[i],timeframes)))
        if i%1000 == 0:
            print(str((i/len(matchData))*100)+"%")
        i += 1
    print("1/3 Complete")
    print("Finding Attributes")
    # Random
    random = getRandomEvents(matchData,timeframes)
    random = attributesExtraction(random, matchData, footballPitch, timeframes, startingGoalys)
    for e in random:
       intresting.append(e)

    return attributeExtraction(goals,intresting,matchData,footballPitch,timeframes,startingGoalys)

def attributeExtraction(goals,intresting,matchData,footballPitch,timeframes,startingGoalys):
    # CleanData
    intresting = helper.cleanData(intresting, matchData)
    goals = helper.cleanData(goals, matchData)

    # print Goals
    printGoals(goals, timeframes)

    # Extracct Attributes
    goals = attributesExtraction(goals, matchData, footballPitch, timeframes, startingGoalys)
    intresting = attributesExtraction(intresting, matchData, footballPitch, timeframes, startingGoalys)

    print("2/3 Complete")
    print("One Match Compleate")
    return [intresting, goals]

def printGoals(goals,time):
    for goal in goals:
        print("GOAL")
        print("TimeStap: " + str(helper.frameToTime(goal.getFrameNum(),time)))

def postProssessing():
    attributes = dataHandler.loadAllObjects()
    dataHandler.saveAsArff(attributes)
    dataHandler.saveAsArffNoX(attributes, [2, 3, 5])
    dataHandler.saveAsArffNoX(attributes, [4, 1, 3, 0])
    dataHandler.saveAsArffNoX(attributes, [4, 2, 3, 0])
    dataHandler.saveAsArffNoX(attributes, [4, 2, 1, 3])
    dataHandler.saveAsArffNoX(attributes, [0, 2, 1, 3])
    dataHandler.cVSHack(attributes)
    fancyGraphs(attributes)

#gets the goalys at the start of the match
def getGoalys(matchData):
    firstFrame = matchData[0]
    players = helper.playersToObj(firstFrame)
    print(players[0].x)
    players.sort(key=lambda x: x.x, reverse=True)

    noRefs =[]

    for player in players:
        if player.teamId != 4:
            noRefs.append(player)

    return [noRefs[0],noRefs[len(noRefs)-1]]

#id: 1
def isCorner(frame,previuesFrame,footballPitch,timeframes,goally):
    ballStatus1 = helper.ballToObject(previuesFrame)
    ballStatus2 = helper.ballToObject(frame)
    if ballStatus1.matchStatus == 'Dead':
        if ballStatus2.matchStatus == 'Alive':
            if footballPitch.ballInCorner(ballStatus1):
                #Check if nearest player is in enemy side
                if helper.isTheNererstPlayerAttacking(frame,footballPitch,timeframes,goally):
                    return True
    return False

#id: 2
def isFreeKick(i, frame, previuesFrame, matchData, footballPitch,timeframes,goaly):
    ballStatus1 = helper.ballToObject(previuesFrame)
    ballStatus2 = helper.ballToObject(frame)
    if ballStatus1.matchStatus == 'Dead':
        if ballStatus2.matchStatus == 'Alive':
            before = helper.xFramesBeforeAndAfter(60, matchData, 1, i)
            if helper.wasBallStillForX(before, 15, 30):
                before = helper.xFramesBeforeAndAfter(60, matchData, 60, i)
                isBackAtCenter = False
                for frame in before:
                    if footballPitch.BallCloseToCenter(helper.ballToObject(frame)):
                        isBackAtCenter = True
                        break
                if isBackAtCenter == False:
                    if helper.isTheNererstPlayerAttacking(frame, footballPitch, timeframes, goaly):
                        return True

#id: 0
def isGoal(i, footballPitch, matchData, goals, timeframes):
    frame = matchData[i]
    previuesFrame = matchData[i-1]
    if helper.isGameRestart(frame,previuesFrame): #match resumed
        viewBack = helper.xFramesBeforeRestart(matchData, INFINITY, i, 1)
        deadVeiw = helper.DeadFramesBeforeRestart(matchData,i)
        if viewBack[0] != False:
            if helper.ballCrossGoal(viewBack,footballPitch) or helper.ballCrossGoal(deadVeiw,footballPitch): #Ball Cross the Goal line
                viewAhead = helper.xFramesBeforeAndAfter(60, matchData, 20, i)
                isBackAtCenter = False
                for frame in viewAhead:
                    if footballPitch.BallCloseToCenter(helper.ballToObject(frame)):
                        isBackAtCenter = True
                        break
                if isBackAtCenter: #was the ball back at the center
                    #viewAhead = helper.xFramesAfterRestart(matchData,450,i)
                    #helper.pitchReset(viewAhead)

                    frameId = helper.frameId(frame)
                    if len(goals) == 0:
                        actualpoint = helper.pointBeforeRestart(matchData,i)  - 1
                        frames = helper.xFramesBeforeAndAfterWithinMatch(50, matchData, 50, actualpoint)
                        goal = PointOfInterest(frames, 0, actualpoint, helper.frameToTime(matchData[actualpoint],timeframes))
                        goal.setFrameNum(frameId)
                        goals.append(goal)
                    else:
                        isIn = False
                        for goal in goals:
                            if goal.getFrameNum() == frameId:
                                isIn = True
                        if isIn != True:
                            actualpoint = helper.pointBeforeRestart(matchData, i) - 1
                            frames = helper.xFramesBeforeAndAfterWithinMatch(50, matchData, 50, actualpoint)
                            goal = PointOfInterest(frames, 0, actualpoint, helper.frameToTime(matchData[actualpoint],timeframes))
                            goal.setFrameNum(frameId)
                            goals.append(goal)
                            return goals
                    return goals
                return goals
        return goals
    return goals

#id: 3
def isShotOnGoal(i,footballPitch,frame):
    ball = helper.ballToObject(frame)
    if ball.matchStatus == "Alive":
        if helper.ballCrossGoalPlus(frame,footballPitch,20):
            return True

#id: 4
def isShotOnGoal2(i,footballPitch,frame,nextFrame,goalys,timeframes):
    ball = helper.ballToObject(frame)
    if ball.matchStatus == "Alive":
        player = helper.findClosestToBall(frame)
        if(int(helper.curntFrameNum(frame)) > timeframes[1]):
            if(player.x > 0):
                if(player.teamId != goalys[0].teamId):
                    if ballHeadingToGoal(footballPitch, frame, nextFrame, goalys[0], player):
                        return True
            else:
                if(player.teamId != goalys[1].teamId):
                    if ballHeadingToGoal(footballPitch, frame, nextFrame, goalys[1], player):
                        return True
        else:
            if (player.x < 0):
                if (player.teamId != goalys[0].teamId):
                    if ballHeadingToGoal(footballPitch, frame, nextFrame, goalys[0], player):
                        return True
            else:
                if (player.teamId != goalys[1].teamId):
                    if ballHeadingToGoal(footballPitch, frame, nextFrame, goalys[1], player):
                        return True

#id: 5
def getRandomEvents(matchData,timeframes):
    seed(1)
    upper = len(matchData)

    values = randint(0,upper,RANDOMEVENTS)
    ranEvents =[]
    for val in values:
        ranEvents.append(PointOfInterest(matchData[val], 5, val, helper.frameToTime(matchData[val],timeframes)))
    ranEvents = helper.cleanData(ranEvents,matchData)
    return ranEvents

def ballHeadingToGoal(footballPitch,frame,nextFrame,goaly,player):
    ball1 = helper.ballToObject(frame)
    ball2 = helper.ballToObject(nextFrame)
    xdiif = ball1.x - ball2.x
    ydiff = ball1.y - ball2.y
    if ball1.speed < 1500:
        return False
    if xdiif == 0 and ydiff == 0:
        return False

    while True:
        ball1.x += xdiif
        ball1.y += ydiff

        closet = helper.findClosestToPoint(frame,ball1)
        if closet.getUid != player.getUid() and goaly.getUid != player.getUid:
            if helper.findClosestToBallPoint(frame,ball1) < footballPitch.scleToRecorded(CHANCEBClosestDisRemoval):
                return False
        if footballPitch.isOutOfBounds(ball1):
            #if ball1.x > footballPitch.scleToRecorded(footballPitch.x) or ball1.x < -footballPitch.scleToRecorded(footballPitch.x):
            #    return True
            #else:
            #    return False
            return helper.ballinGoalPlus(ball1, footballPitch, CHANCEBGoalExtra)

#Exract attributes
def attributesExtraction(events, matchData,footballPitch,timeframes, startingGoalys):
    events = TeamAssosiation(footballPitch, events, matchData,timeframes,startingGoalys)
    events = DensityA(footballPitch, events, matchData, 1)
    events = Erraticmovement(footballPitch, events, matchData, timeframes, startingGoalys)
    events = markingScore(timeframes, startingGoalys, footballPitch, events, matchData)
    events = AttackingPressure(footballPitch,events,matchData)
    events = DeffendingPressure(footballPitch,events,matchData)
    return events

#used to mark Attacking team and defending team and associate event with
def TeamAssosiation(footballPitch, points, matchData, timeframes, goaly):
    for event in points:
        frames = helper.xFramesBeforeAndAfterWithinMatch(50, matchData, 30, event.getmatchDataPostion())
        split = []
        j = 0

        while j < 2:
            split.append(0)
            j += 1
        for frame in frames:
            football = helper.ballToObject(frame)
            split[footballPitch.whatQuadrantI(football.x, 2)] += 1
        #first half
        firsthalf = True
        if int(helper.frameId(frames[0])) >= int(timeframes[1]):
            firsthalf = False

        #assighning
        if split[0] > split[1]:
            if split[0] / (split[0] + split[1]) > 0.55:
                if firsthalf:
                    event.setAttackingId(goaly[0].teamId, -1)
                    event.setDefendersId(goaly[1].teamId, 1)
                else:
                    event.setAttackingId(goaly[1].teamId, -1)
                    event.setDefendersId(goaly[0].teamId, 1)
        else:
            if split[1] / (split[0] + split[1]) > 0.55:
                if firsthalf:
                    event.setAttackingId(goaly[1].teamId, 1)
                    event.setDefendersId(goaly[0].teamId, -1)
                else:
                    event.setAttackingId(goaly[0].teamId, 1)
                    event.setDefendersId(goaly[1].teamId, -1)
    return points

#is the density of the players in a given secotion of a field
def DensityA(footballPitch, points, matchData, teamid):
    i = 0
    while i < len(points):
        # get Frames
        frames = helper.xFramesBeforeAndAfterWithinMatch(50, matchData, 30, points[i].getmatchDataPostion())
        total = []
        if len(frames) == 0:
            frames = helper.xFramesBeforeAndAfterWithinMatch(50, matchData, 30, points[i].getmatchDataPostion())
        # has frames continue
        for frame in frames:
            # players to obj
            players = helper.playersToObj(frame)
            split = []
            j = 0
            while j < DensityASplitCount:
                split.append(0)
                j += 1
            for player in players:
                if player.teamId == teamid or teamid == -1:
                    if player.teamId != -1:
                            #print(footballPitch.whatQuadrantI(player.x,6))
                            #print(split[0])
                        split[footballPitch.whatQuadrantI(player.x, DensityASplitCount)] += 1
            total.append(split)
        if len(total) == 0:
            print("aww Suger !*&$^!")
        points[i].populateQuadrants(total, teamid)
        points[i].setcompressedQ(helper.getCompressedDensityA(points[i].getQuadants()))
        i += 1
    return points

#is the density of the players in a given secotion of a field
def AttackingPressure(footballPitch, points, matchData):
    i = 0
    while i < len(points):
        # get Frames
        teamid = points[i].getAttackingId()
        frames = helper.xFramesBeforeAndAfterWithinMatch(60, matchData, 3, points[i].getmatchDataPostion())
        total = []
        if len(frames) == 0:
            frames = helper.xFramesBeforeAndAfterWithinMatch(60, matchData, 3, points[i].getmatchDataPostion())
        # has frames continue
        for frame in frames:
            # players to obj
            players = helper.playersToObj(frame)
            split = []
            j = 0
            while j < DensityASplitCount:
                split.append(0)
                j += 1
            for player in players:
                if player.teamId == teamid or teamid == -1:
                    if player.teamId != -1:
                        split[footballPitch.whatQuadrantI(player.x, DensityASplitCount)] += 1
            total.append(split)
        if len(total) == 0:
            print("aww Suger !*&$^!")
        points[i].populateQuadrantsAttackers(total)
        points[i].setCompressedQAttackers(helper.getCompressedQuadrantsOneDir(points[i].getAttackingDir(),points[i].getQuadrantsAttackers()))
        i += 1
    return points

#is the density of the players in a given secotion of a field
def DeffendingPressure(footballPitch, points, matchData):
    i = 0
    while i < len(points):
        # get Frames
        teamid = points[i].getDefendersId()
        frames = helper.xFramesBeforeAndAfterWithinMatch(60, matchData, 1, points[i].getmatchDataPostion())
        total = []
        if len(frames) == 0:
            frames = helper.xFramesBeforeAndAfterWithinMatch(60, matchData, 1, points[i].getmatchDataPostion())
        # has frames continue
        for frame in frames:
            # players to obj
            players = helper.playersToObj(frame)
            split = []
            j = 0
            while j < DensityASplitCount:
                split.append(0)
                j += 1
            for player in players:
                if player.teamId == teamid or teamid == -1:
                    if player.teamId != -1:
                        split[footballPitch.whatQuadrantI(player.x, DensityASplitCount)] += 1
            total.append(split)
        if len(total) == 0:
            print("aww Suger !*&$^!")
        points[i].populateQuadrantsDefenders(total)
        points[i].setCompressedQDefenders(helper.getCompressedQuadrantsOneDir(points[i].getDefendersDir(),points[i].getQuadrantsDefenders()))
        i += 1
    return points

def DensityB():
    print("not here Yet")

def markingScore(timeframes,startingGoalys,footballPitch,points,matchData):
    i = 0
    while i < len(points):
        frames = helper.xFramesBeforeAndAfterWithinMatch(60, matchData, 5, points[i].getmatchDataPostion())
        total = []
        try:
            if frames[0] != False:
                #for tests
                #if i == 4:
                #    print("holaUp")
                for frame in frames:
                    firsthalf = True
                    if int(helper.frameId(frame)) >= int(timeframes[1]):
                        firsthalf = False
                    players = helper.playersToObj(frame)
                    team = helper.findClosestToBall(frame)
                    #debug

                    #get Defenders
                    teams = helper.splitPlayersTwoTeam(players, team.teamId)
                    teamDeffend = teams[1]  # defenders in defenders side
                    #get Attackers in enmy field
                    players = helper.splitPitchAttackingSide(players,team.teamId,startingGoalys,firsthalf)
                    teams = helper.splitPlayersTwoTeam(players,team.teamId)
                    teamAttack = teams[0]   #Attackers in defenders side
                    #if len(teamAttack) == 0:
                    #    print("o No")
                    marking = []
                    for Attacker in teamAttack:
                        marking.append([Attacker,helper.findClosestPlayersToPlayer(Attacker,teamDeffend,2)])
                    # (pA1,[p1,p2])
                    marking = helper.removeToX(marking,2)
                    # (def.uid , dis , atc.uid)
                    #if i == 4:
                        #print("len: " + str(len(marking)))
                    score = helper.getMarkScore(marking,footballPitch)
                    total.append(score)
            if len(total) > 1:
                #grap.dotAndLine(total,i)
                points[i].setMarking(helper.MMMSTDR1(total))
            else:
                print("#uckThis!123412^&()(")
            i += 1
        except:
            points.pop(i)
    return points

#is how much the ball moved before the goal
def Erraticmovement(footballPitch,points,matchData,timeframes,startingGoalys):
    i = 0
    while i < len(points):
        #print("1: " +helper.frameId(points[i].getFrame()))
        #print("2: " +helper.frameId(matchData[points[i].getmatchDataPostion()]))
        frames = helper.xFramesBeforeAndAfterWithinMatch(60, matchData, 60, points[i].getmatchDataPostion())
        changeX = []
        changeY = []
        changeS = []
        previous = Football()
        j = 0
        if frames[0] == False:
            points[i].setEratic(-1, -1, -1, -1)
            print("NOt GOod")
        if frames[0] != False:
            for frame in frames:
                if j == 0:
                    previous = helper.ballToObject(frame)
                    j += 1
                else:
                    current = helper.ballToObject(frame)
                    changeX.append(previous.x - current.x)
                    changeY.append(previous.y - current.y)
                    changeS.append(previous.speed - current.speed)
                    previous = current
            try:
                if len(changeX) != 0:
                    avgChangeX = sum(changeX)/len(changeX)
                    avgChangeY = sum(changeY)/len(changeY)
                    avgChangeS = sum(changeS)/len(changeS)
                    XVector = []
                    YVector = []
                    SVector = []
                    j = 0
                    while j < len(changeX):
                        XVector.append(abs(abs(changeX[j]) - abs(avgChangeX)))
                        YVector.append(abs(abs(changeY[j]) - abs(avgChangeY)))
                        SVector.append(abs(abs(changeS[j]) - abs(avgChangeS)))
                        j += 1
                    EraticChangeX = sum(XVector) / j
                    EraticChangeY = sum(YVector) / j
                    EraticChangeS = sum(SVector) / j
                    toatlEratic  = EraticChangeX/2 + EraticChangeY + EraticChangeS/5

                    points[i].setTeamIdToEvent(helper.witchTeamIsAssosiated(frames[0],footballPitch,timeframes,startingGoalys))
                    points[i].setEratic(EraticChangeX,EraticChangeY,EraticChangeS,toatlEratic)
                else:
                    points[i].setEratic(-1, -1, -1, -1)
                i+= 1
            except:
                points.pop(i)
        #print("Eratic % " + str((i/len(points))*100))
    return points

def fancyGraphs(attribute):
    gra = Grapher()
    #all matches together with all types Erratic
    values = gra.ErraticXYExtraction(attribute,-1, [5])
    gra.compareByTypeDotPlot(values[0],values[1], values[2])

    values = gra.ErraticXYExtraction(attribute, -1, [-1])
    gra.compareByTypeDotPlot(values[0], values[1], values[2])

    #Eratic Spped and Toatal
    values2 = gra.ErraticSpeedTotalExtraction(attribute, -1, [0,3])
    gra.compareByTypeDotPlot(values2[0], values2[1], values2[2])

    #Eratoc Spped and Toatal with all types Erratic
    values2 = gra.ErraticSpeedTotalExtraction(attribute, -1, [-1])
    gra.compareByTypeDotPlot(values2[0], values2[1], values2[2])

    # Eratic 3d of X, Y ,speed
    gra.compareByType3dDotPlot(values[0], values[1], values2[0], values2[2])

    # Eratic all matches together with all types
    values = gra.ErraticXYExtraction(attribute, -1, [0,1,2,3,4])
    gra.compareByTypeDotPlot(values[0], values[1], values[2])

    # Eratic all matches together with given types
    values = gra.ErraticXYExtraction(attribute, -1, [0, 1, 3])
    gra.compareByTypeDotPlot(values[0], values[1], values[2])

    # Eratic
    values2 = gra.ErraticSpeedTotalExtraction(attribute, -1, [0, 1, 3])
    gra.compareByTypeDotPlot(values2[0], values2[1], values2[2])

    # Eratic 3d
    gra.compareByType3dDotPlot(values[0], values[1], values2[0], values2[2])

    #eratic not so popular
    values = gra.ErraticXYExtraction(attribute, -1, [0, 2, 4])
    gra.compareByTypeDotPlot(values[0], values[1], values[2])

    # pi chart
    values = gra.allreturnByType(attribute,-1)
    gra.PiChartVal(values)

    #Pressure
    dat = gra.allTypePressureScoreExtract(attribute, -1, 3)
    gra.CompareNhistogram(dat, [5], [0, 2], "Attacking")
    dat = gra.allTypePressureScoreExtract(attribute, -1, 3)
    gra.CompareNhistogram(dat, [5], [1, 2], "Defending")
    dat = gra.allTypePressureScoreExtract(attribute, -1, 2)
    gra.CompareNhistogram(dat, [5], [1, 2], "")

    #density 
    dat = gra.allTypeDensityScoreExtract(attribute,-1,0)
    gra.CompareNhistogram(dat, [5], [0, 1],"Density")

    #all matches marking score histogram brakdown by event type
    dat = gra.allTypeMarkScoreExtract(attribute,-1,0)
    gra.CompareNhistogram(dat,[2,5],"Marking score")

    dat = gra.allTypeMarkScoreExtract(attribute, -1, 0)
    gra.CompareNhistogram(dat, [5], [0, 1], "Marking score")

    dat = gra.allTypeMarkScoreExtract(attribute, -1, 0)
    gra.CompareNhistogram(dat, [4,2,5], "Marking score")
   

if __name__ == '__main__':
    #only needs to be done once.
    #has to be run wenever a event or atribute changes.
    #readDocs()

    #Updates the attributes
    #attributeExtractionStart()

    #testReading
    #testExtractionEvents()

    #postProssessing
    postProssessing()

    #
    grap.finished()


