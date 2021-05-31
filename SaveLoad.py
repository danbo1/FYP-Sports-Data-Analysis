import pickle as pic
import csv
import pandas as pd
from Grapher import Grapher
fileFolder = 'yourDevice/DataExtractor/pikeleObj/'
testAddress = 'yourDevice/DataExtractor/pikeleObj/g987632.dat'
fileNames = 'yourDevice/DataExtractor/Files.txt'
cvsResults = 'results.csv'
TYPES = ["Goal", "Corners", "free_Kick", "ChanceA", "ChanceB", "Random"]
class SaveLoad:

    #Save a single set of results to a given File !!! Will overide The Previuse"
    def saveObjects(self,list,id):
        fileLocation = fileFolder + id + ".dat"
        with open(fileLocation,"wb") as file:
            pic.dump(list,file)
        print("3/3 Complete")
        print("************************************************************************")
        print("\n \n")

    # Test the loading of files
    def testLoad(self):
        with open(testAddress, "rb") as file:
            return pic.load(file)

    #load a single object given the id
    def loadObjects(self, id):
        fileLocation = fileFolder + id + ".dat"
        with open(fileLocation, "rb") as file:
            return pic.load(file)

    #loads all the objects
    def loadAllObjects(self):
        fileNamesFile = open(fileNames, 'r')
        fileNamesList = fileNamesFile.readlines()
        data = []
        for filename in fileNamesList:
            if filename != "END":
                filename = filename[0:(len(filename) - 1)]
                data.append([filename,self.loadObjects(filename)])
        return data

    #output to cvs for tensorflow hack
    def cVSHack(self,data):
        train_labels = ["X", "Y", "Speed", "Total", "isGoal"]
        X, Y, Z, Y2, test, isTest = [], [], [], [], [], []
        j =0
        for set in data:
            pointOfInt = set[1][1]
            for goal in pointOfInt:
                eratic = goal.getEratic()
                eratic.append(goal.getType())
                eratic.append(goal.getTeamIdToEvent())
                eratic.append(str(set[0]))
                eratic.append(goal.getTeamIdToEvent() + j)

                test.append(eratic)

                X.append(eratic[0])
                Y.append(eratic[1])
                Z.append(goal.getType())

            pointOfInt = set[1][0]
            for event in pointOfInt:
                eratic = event.getEratic()
                eratic.append(event.getType())
                eratic.append(event.getTeamIdToEvent())
                eratic.append(str(set[0]))
                eratic.append(event.getTeamIdToEvent()+ j)

                test.append(eratic)

                X.append(eratic[0])
                Y.append(eratic[1])
                Z.append(event.getType())
            j+=2

        #gra = Grapher()
        #gra.compareByTypeDotPlot(X,Y,Z)
        #plt.plot(X1, Y1, 'ro', label='GOAL')
        #plt.plot(X2, Y2, 'bo', label='EVENT')
        #plt.legend(loc='best')
        #plt.show()

        path = fileFolder + cvsResults
        with open(path, mode='w', newline='') as results:
            out_w = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #out_w.writerow([train_labels[0], train_labels[1], train_labels[2], train_labels[3], train_labels[4]])
            for elm in test:
                #out_w.writerow([elm[0], elm[1], elm[2], elm[3], elm[4]])
                out_w.writerow([elm[0], elm[1], elm[2], elm[3], elm[4],elm[5],elm[6],elm[7]])

    #testload for tensorflow format
    def loadForTensor(self):
        path = fileFolder + cvsResults
        train_labels = ["X", "Y", "Speed", "Total", "isGoal"]
        Eratic = pd.read_csv(path,names=[train_labels[0], train_labels[1], train_labels[2], train_labels[3], train_labels[4]])
        Eratic.head()

        return Eratic

    #arff output
    def saveAsArff(self, data):
        fileLocation = fileFolder + "AllMatches" + ".arff"
        with open(fileLocation, "w") as file:
            self.ArffHeader(file)
            for section in data:
                goals = section[1][1]
                events = section[1][0]
                for event in events:
                    goals.append(event)
                for event in goals:
                    line = self.eventToArffLine(event,[-1])
                    file.write(line)
        file.close()

    def saveAsArffNoX(self, data, doNotAdd):
        line = ""
        for elm in doNotAdd:
            line += "[" + str(elm) + "]"
        fileLocation = fileFolder + "AllMatchesNo"+ line + ".arff"
        with open(fileLocation, "w") as file:
            self.ArffHeader(file)
            for section in data:
                goals = section[1][1]
                for event in goals:
                    line = self.eventToArffLine(event, doNotAdd)
                    if line != False:
                        file.write(line)
        file.close()

    def ArffHeader(self,file):
        file.write("@RELATION GoalChances\n")
        file.write("\n")

        line = "{"
        for type in TYPES:
            line += type + ","
        line = line[0:(len(line)-1)]
        line += "}"

        file.write("@ATTRIBUTE Type " + line +"\n")
        #file.write("@ATTRIBUTE TeamId NUMERIC\n")

        file.write("@ATTRIBUTE ErraticX NUMERIC\n")
        file.write("@ATTRIBUTE ErraticY NUMERIC\n")
        file.write("@ATTRIBUTE ErraticS NUMERIC\n")
        file.write("@ATTRIBUTE ErraticT NUMERIC\n")

        file.write("@ATTRIBUTE MarkingMean NUMERIC\n")
        file.write("@ATTRIBUTE MarkingMedan NUMERIC\n")
        file.write("@ATTRIBUTE MarkingMode NUMERIC\n")
        file.write("@ATTRIBUTE MarkingSTDD NUMERIC\n")
        file.write("@ATTRIBUTE MarkingRange NUMERIC\n")

        file.write("@ATTRIBUTE DensityMean NUMERIC\n")
        file.write("@ATTRIBUTE DensityMedan NUMERIC\n")
        file.write("@ATTRIBUTE DensityMode NUMERIC\n")
        file.write("@ATTRIBUTE DensitySTDD NUMERIC\n")
        file.write("@ATTRIBUTE DensityRange NUMERIC\n")

        file.write("@ATTRIBUTE initalChangeAttack NUMERIC\n")
        file.write("@ATTRIBUTE midChangeAttack NUMERIC\n")
        file.write("@ATTRIBUTE endChangeAttack NUMERIC\n")
        file.write("@ATTRIBUTE TotalChangeAttack NUMERIC\n")

        file.write("@ATTRIBUTE initalChangeDefence NUMERIC\n")
        file.write("@ATTRIBUTE midChangeDefence NUMERIC\n")
        file.write("@ATTRIBUTE endChangeDefence NUMERIC\n")
        file.write("@ATTRIBUTE TotalChangeDefence NUMERIC\n")

        file.write("@ATTRIBUTE TimeOfEvent NUMERIC\n")
        file.write("\n")
        file.write("@DATA\n")

    def eventToArffLine(self, event, types):
        type = event.getType()
        dontAdd = False
        for check in types:
            if type == check:
                dontAdd = True
        if dontAdd == True:
            return False
        line = ""
        #Type [1]
        line += str(TYPES[event.getType()]) + ","
        #line += str(event.getTeamIdToEvent()) + ","
        #Eratic [4]
        temp = event.getEratic()
        for val in temp:
            line += str(val) + ","
        # Marking  [5]
        temp = event.getMarking()
        for val in temp:
            line += str(val) + ","
        # DensityA  [5]
        temp = event.getcompressedQ()
        for val in temp:
            line += str(val) + ","
        # AttackQ [4]
        temp = event.getCompressedQAttackers()
        for val in temp:
            line += str(val) + ","
        # DefenceQ [4]
        temp = event.getCompressedQDefenders()
        for val in temp:
            line += str(val) + ","
        #TimeStamp [1]
        line += str(event.getTimestamp()) + "\n"
        return line

