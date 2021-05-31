import pylab
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from sympy.stats.drv_types import numpy
from mpl_toolkits import mplot3d

class Grapher:
    COLOURS = ["ro","bo","yo","go","mo","ko"]
    COLOURS2 = ["red", "blue", "yellow", "green", "purple", "black", "cyan"]
    TYPES = ["Goal", "Corners", "Free Kick", "Chance A", "Chance B", "Random"]
    MMMSTDR1 = ["mean", "median", "mode", "std divation", "range"]
    PointInDef = ["start", "mid", "End"]
    def some(self):
        tes =0

    def dotAndLine(self,fit, i):
        l = [i for i in range(len(fit))]
        pylab.plot(l, fit, 'o')
        pylab.xlabel('Plot:' + str(i))
        # calc the trendline
        z = numpy.polyfit(l, fit, 1)
        p = numpy.poly1d(z)
        pylab.plot(l, p(l), "r--")
        pylab.plt.show()

    def compare2DotPlot(self,X1,Y1,X2,Y2,name1,name2):
        pylab.plot(X1, Y1, 'ro', label=name1)
        pylab.plot(X2, Y2, 'bo', label=name2)
        pylab.legend(loc='best')

        pylab.show()


    def compareByTypeDotPlot(self,X,Y,Z):
        i = 0
        while i < len(self.TYPES):
            j = 0
            Xlist = []
            Ylist = []
            while j < len(X):
                if Z[j] == i:
                    Xlist.append(X[j])
                    Ylist.append(Y[j])
                j += 1
            pylab.plot(Xlist,Ylist, self.COLOURS[i], label=self.TYPES[i])
            i += 1
        pylab.legend(loc='best')
        pylab.xlabel("Erratic: X")
        pylab.ylabel("Erratic: Y")
        pylab.show()

    def compareByType3dDotPlot(self,X,Y,Z,Type):
        i = 0
        ax = pylab.plt.axes(projection='3d')
        while i < len(self.TYPES):
            j = 0
            Xlist = []
            Ylist = []
            Zlist = []
            while j < len(X):
                if Type[j] == i:
                    Xlist.append(X[j])
                    Ylist.append(Y[j])
                    Zlist.append(Z[j])
                j += 1
            ax.plot3D(Xlist, Ylist, Zlist, self.COLOURS[i], label=self.TYPES[i])
            i += 1
        pylab.legend(loc='best')
        pylab.xlabel("Erratic: X")
        pylab.ylabel("Erratic: Y")
        ax.set_zlabel('Erratic: Speed')
        pylab.show()

    def singleLine(self,fit):
        l = [i for i in range(len(fit))]
        fig, ax = pylab.plt.subplots()  # Create a figure containing a single axes.
        i = 0
        ax.plot(l, fit)
        pylab.show()

    def multieLine(self,fit):
        l = [i for i in range(len(fit[0]))]
        fig, ax = pylab.plt.subplots()  # Create a figure containing a single axes.
        i = 0
        while i < len(fit):  # for the other lines
            ax.plot(l, fit[i])
            i += 1

    def PiChartVal(self,values):
        fig = pylab.plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('equal')
        labels = []
        for label in values:
            labels.append(label[1])
        piSegment = []
        for type in values:
            piSegment.append(len(type[0]))
        ax.pie(piSegment, labels=labels, autopct='%1.2f%%')
        pylab.plt.show()

    def allreturnByType(self, data, match):
        valuesToReturn = []
        i = 0
        while i < len(self.TYPES):
            valuesToReturn.append(self.returnByType(data, match, i))
            i += 1
        return valuesToReturn

    def returnByType(self, data, match, type):
        Values, Name = [], ""
        if match == -1:
            for set in data:
                pointOfInt = set[1][1]
                for goal in pointOfInt:
                    Gtype = goal.getType()
                    if Gtype == type or type == -1:
                        Values.append(goal)

                pointOfInt = set[1][0]
                for event in pointOfInt:
                    Etype = event.getType()
                    if Etype == type or type == -1:
                        Values.append(event)
        else:
            Name += " |Match:" + str(match)
            pointOfInt = data[match][1][1]
            for goal in pointOfInt:
                Gtype = goal.getType()
                if Gtype == type or type == -1:
                    Values.append(goal)

            pointOfInt = data[match][1][0]
            for event in pointOfInt:
                Etype = event.getType()
                if Etype == type or type == -1:
                    Values.append(event)
        if type != -1:
            Name += "" + str(self.TYPES[type])
        return [Values, Name]

    #array of points
    def Compare2histogram(self, pointsX, pointsY, graphName1, graphName2):
        n_bins = 20
        fig, axs = pylab.plt.subplots(1, 2, sharey=True, tight_layout=True)
        axs[0].hist(pointsX,color=self.COLOURS2[1], bins=n_bins)
        axs[0].set_xlabel(graphName1)
        axs[1].hist(pointsY,color=self.COLOURS2[2], bins=n_bins)
        axs[1].set_xlabel(graphName2)
        pylab.show()

    def CompareNhistogram(self, points, exception, tital):
        n_bins = 20
        fig, axs = pylab.plt.subplots(1, (len(points)-len(exception)), sharey=True, tight_layout=True)
        i = 0
        j = 0
        for point in points:
            add = True
            for check in exception:
                if j == check:
                    add = False
            if add == True:
                axs[i].hist(point[0], color=self.COLOURS2[i], bins=n_bins)
                axs[i].set_xlabel(point[1])
                i += 1
            j += 1
        axs[0].set_ylabel("Frequency Count")
        pylab.title("Test")
        pylab.show()

    def CompareNhistogram(self, points, exception, nonStand, tital):
        n_bins = 20
        fig, axs = pylab.plt.subplots(1, (len(points)-len(exception)), sharey=True, tight_layout=True)
        i = 0
        j = 0
        for point in points:
            add = True
            for check in exception:
                if j == check:
                    add = False
            if add == True:
                axs[i].hist(point[nonStand[0]], color=self.COLOURS2[i], bins=n_bins)
                axs[i].set_xlabel(point[nonStand[1]])
                i += 1
            j += 1
        axs[0].set_ylabel("Frequency Count")
        pylab.show()

    def ErraticXYExtraction(self, data, match, types):
        X, Y, Z = [], [], []
        if match == -1:
            for set in data:
                pointOfInt = set[1][1]
                for goal in pointOfInt:
                    eratic = goal.getEratic()
                    type = goal.getType()
                    add = False
                    for check in types:
                        if type == check or check == -1:
                            add = True
                            break
                    if add == True:
                        X.append(eratic[0])
                        Y.append(eratic[1])
                        Z.append(goal.getType())

                pointOfInt = set[1][0]
                for event in pointOfInt:
                    eratic = event.getEratic()
                    type = event.getType()
                    add = False
                    for check in types:
                        if type == check or check == -1:
                            add = True
                            break
                    if add == True:
                        X.append(eratic[0])
                        Y.append(eratic[1])
                        Z.append(event.getType())
        else:
            pointOfInt = data[match][1][1]
            for goal in pointOfInt:
                eratic = goal.getEratic()
                type = goal.getType()
                add = False
                for check in types:
                    if type == check or check == -1:
                        add = True
                        break
                if add == True:
                    X.append(eratic[0])
                    Y.append(eratic[1])
                    Z.append(goal.getType())

            pointOfInt = data[match][1][0]
            for event in pointOfInt:
                eratic = event.getEratic()
                type = event.getType()
                add = False
                for check in types:
                    if type == check or check == -1:
                        add = True
                        break
                if add == True:
                    X.append(eratic[0])
                    Y.append(eratic[1])
                    Z.append(event.getType())
        return [X, Y, Z]

    def ErraticSpeedTotalExtraction(self, data, match, types):
        speed, total, Z = [], [], []
        if match == -1:
            for set in data:
                pointOfInt = set[1][1]
                for goal in pointOfInt:
                    eratic = goal.getEratic()
                    type = goal.getType()
                    add = False
                    for check in types:
                        if type == check or check == -1:
                            add = True
                            break
                    if add == True:
                        speed.append(eratic[2])
                        total.append(eratic[3])
                        Z.append(goal.getType())

                pointOfInt = set[1][0]
                for event in pointOfInt:
                    eratic = event.getEratic()
                    type = event.getType()
                    add = False
                    for check in types:
                        if type == check or check == -1:
                            add = True
                            break
                    if add == True:
                        speed.append(eratic[2])
                        total.append(eratic[3])
                        Z.append(event.getType())
        else:
            pointOfInt = data[match][1][1]
            for goal in pointOfInt:
                eratic = goal.getEratic()
                type = goal.getType()
                add = False
                for check in types:
                    if type == check or check == -1:
                        add = True
                        break
                if add == True:
                    speed.append(eratic[2])
                    total.append(eratic[3])
                    Z.append(goal.getType())

            pointOfInt = data[match][1][0]
            for event in pointOfInt:
                eratic = event.getEratic()
                type = event.getType()
                add = False
                for check in types:
                    if type == check or check == -1:
                        add = True
                        break
                if add == True:
                    speed.append(eratic[2])
                    total.append(eratic[3])
                    Z.append(event.getType())
        return [speed, total, Z]

    def allTypeMarkScoreExtract(self, data, match, mmavg):
        valuesToReturn = []
        i = 0
        while i < len(self.TYPES):
            valuesToReturn.append(self.MarkingScoreExreaction(data,match,i,mmavg))
            i+=1
        return valuesToReturn

    def MarkingScoreExreaction(self, data, match, type, mmavg):
        Marking, Name = [], self.MMMSTDR1[mmavg]
        if match == -1:
            for set in data:
                pointOfInt = set[1][1]
                for goal in pointOfInt:
                    marks = goal.getMarking()
                    Gtype = goal.getType()
                    if Gtype == type or type == -1:
                        Marking.append(marks[mmavg])

                pointOfInt = set[1][0]
                for event in pointOfInt:
                    marks = event.getMarking()
                    Etype = event.getType()
                    if Etype == type or type == -1:
                        Marking.append(marks[mmavg])
        else:
            Name += " |Match:" + str(match)
            pointOfInt = data[match][1][1]
            for goal in pointOfInt:
                marks = goal.getMarking()
                Gtype = goal.getType()
                if Gtype == type or type == -1:
                    Marking.append(marks[mmavg])

            pointOfInt = data[match][1][0]
            for event in pointOfInt:
                marks = event.getMarking()
                Etype = event.getType()
                if Etype == type or type == -1:
                    Marking.append(marks[mmavg])
        if type != -1:
            Name += " " + str(self.TYPES[type])
        return [Marking, Name]

    def allTypePressureScoreExtract(self, data, match, point):
        valuesToReturn = []
        i = 0
        while i < len(self.TYPES):
            valuesToReturn.append(self.PressureScoreExreaction(data, match, i, point))
            i += 1
        return valuesToReturn

    def PressureScoreExreaction(self, data, match, type, point):
        Attacking, Defending, Name = [], [], ""
        if match == -1: ## getCompressedQDefenders ## getCompressedQAttackers
            for set in data:
                pointOfInt = set[1][1]
                for goal in pointOfInt:
                    marks = goal.getCompressedQAttackers()
                    marks2 = goal.getCompressedQDefenders()
                    Gtype = goal.getType()
                    if Gtype == type or type == -1:
                        Attacking.append(marks[point])
                        Defending.append(marks2[point])

                pointOfInt = set[1][0]
                for event in pointOfInt:
                    marks = goal.getCompressedQAttackers()
                    marks2 = goal.getCompressedQDefenders()
                    Etype = event.getType()
                    if Etype == type or type == -1:
                        Attacking.append(marks[point])
                        Defending.append(marks2[point])
        else:
            Name += " |Match:" + str(match)
            pointOfInt = data[match][1][1]
            for goal in pointOfInt:
                marks = goal.getCompressedQAttackers()
                marks2 = goal.getCompressedQDefenders()
                Gtype = goal.getType()
                if Gtype == type or type == -1:
                    Attacking.append(marks[point])
                    Defending.append(marks2[point])

            pointOfInt = data[match][1][0]
            for event in pointOfInt:
                marks = goal.getCompressedQAttackers()
                marks2 = goal.getCompressedQDefenders()
                Etype = event.getType()
                if Etype == type or type == -1:
                    Attacking.append(marks[point])
                    Defending.append(marks2[point])
        if type != -1:
            Name += " " + str(self.TYPES[type])
        return [Attacking, Defending, Name]

    def allTypeDensityScoreExtract(self, data, match, mmavg):
        valuesToReturn = []
        i = 0
        while i < len(self.TYPES):
            valuesToReturn.append(self.DensityScoreExreaction(data, match, i,  mmavg))
            i += 1
        return valuesToReturn

    def DensityScoreExreaction(self, data, match, type, mmavg):
        Attacking, Defending, Name = [], [], "" + self.MMMSTDR1[mmavg]
        if match == -1: ## getCompressedQDefenders ## getCompressedQAttackers
            for set in data:
                pointOfInt = set[1][1]
                for goal in pointOfInt:
                    marks = goal.getcompressedQ()
                    Gtype = goal.getType()
                    if Gtype == type or type == -1:
                        Attacking.append(marks[mmavg])

                pointOfInt = set[1][0]
                for event in pointOfInt:
                    marks = goal.getcompressedQ()
                    Etype = event.getType()
                    if Etype == type or type == -1:
                        Attacking.append(marks[mmavg])
        else:
            Name += " |Match:" + str(match)
            pointOfInt = data[match][1][1]
            for goal in pointOfInt:
                marks = goal.getcompressedQ()
                Gtype = goal.getType()
                if Gtype == type or type == -1:
                    Attacking.append(marks[mmavg])
            pointOfInt = data[match][1][0]
            for event in pointOfInt:
                marks = goal.getcompressedQ()
                Etype = event.getType()
                if Etype == type or type == -1:
                    Attacking.append(marks[mmavg])
        if type != -1:
            Name += " " + str(self.TYPES[type])
        return [Attacking, Name]

    def printByType(self, events, time, type, helper):
        for event in events:
            if event.getType() == type:
                print(self.TYPES[type])
                print("TimeStap: " + str(event.getTimestamp()))

    def finished(self):
        print("It Worked!!!!!")
        


