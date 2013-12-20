# General imports

import numpy
from matplotlib import pyplot

# Class imports



# Function import



# Class definition

class subPlot:

    # Constructors

    def __init__(self, name, labels):

        self.name = name
        self.bounds = [[float("Inf"), -float("Inf")], [float("Inf"), -float("Inf")]]
        self.labels = labels
        self.series = []
        self.regressions = []
        self.tTest = False

    # Getters

    def getName(self):
        return self.name

    def getBounds(self):
        return self.bounds

    def getXBounds(self):
        return self.bounds[0]

    def getYBounds(self):
        return self.bounds[1]

    def getLabels(self):
        return self.labels

    def getXLabel(self):
        return self.labels[0]

    def getYLabel(self):
        return self.labels[1]

    def getSeries(self):
        return self.series

    def getRegressions(self):
        return self.regressions

    def getTTest(self):
        return self.tTest

    # Others

    def addSerie(self, serie):
        self.series.append(serie)
        self.computeBounds()

    def addRegression(self, regression):
        self.regressions.append(regression)

    def addTTest(self, tTest):
        self.tTest = tTest

    def computeBounds(self):

        xMin = self.getXBounds()[0]
        xMax = self.getXBounds()[1]
        yMin = self.getYBounds()[0]
        yMax = self.getYBounds()[1]

        for serieTemp in self.getSeries():

            boundsTemp = serieTemp.getBounds()

            self.bounds[0][0] = min(xMin, boundsTemp[0][0])
            self.bounds[0][1] = max(xMax, boundsTemp[0][1])
            self.bounds[1][0] = min(yMin, boundsTemp[1][0])
            self.bounds[1][1] = max(yMax, boundsTemp[1][1])

    # Displaying

    def plot(self, ax):

        nbDecimals = 5

        # Plot series

        for serieTemp in self.getSeries():

            if serieTemp.getGender() == "M":
                if serieTemp.getSurgery() == 0:
                    markerPart1 = "x"
                elif serieTemp.getSurgery() == 1:
                    markerPart1 = "1"
            elif serieTemp.getGender() == "F":
                if serieTemp.getSurgery() == 0:
                    markerPart1 = "+"
                elif serieTemp.getSurgery() == 1:
                    markerPart1 = "4"

            if serieTemp.getType() == "CRL":
                markerPart2 = "g"
            elif serieTemp.getType() == "SGS":
                markerPart2 = "r"

            X = []
            Y = []

            for value in serieTemp.getValues():
                X.append(value.getX())
                Y.append(value.getY())

            X = numpy.array(X)
            Y = numpy.array(Y)

            m = numpy.mean(Y)
            s = numpy.std(Y)

            serieLabel = serieTemp.getName() + " (m,s) = (" + str(round(m, nbDecimals)) + "," + str(round(s, nbDecimals)) + ")"

            ax.plot(X, Y, markerPart1 + markerPart2, label = serieLabel)
            pyplot.setp(ax.get_xticklabels(), visible = True)

        # Plot regressions

        for regression in self.getRegressions():

            if regression.getType() == "CRL":
                markerPart2 = "g"
            elif regression.getType() == "SGS":
                markerPart2 = "r"

            [a, b, r2] = regression.getParameters()

            X = self.getXBounds()
            X = numpy.array(X)

            Y = a * X + b

            regressionLabel = regression.getName() + " (a,b,r2) = (" + str(round(a, nbDecimals)) + "," + str(round(b, nbDecimals)) + "," + str(round(r2, nbDecimals)) + ")"

            ax.plot(X, Y, "--" + markerPart2, label = regressionLabel)

        # Set plot parameters

        pValue = round(self.getTTest().getPValue(), nbDecimals)

        ax.set_title(self.getName() + " (P-Value = " + str(pValue) + ")")

        ax.set_xlabel(self.getXLabel())
        ax.set_ylabel(self.getYLabel())

        ax.set_xlim(self.getXBounds())
        ax.set_ylim(self.getYBounds())

        ax.grid(True)

        #ax.legend(loc = 4, prop = {'size': 10})
        ax.legend(loc='upper center', bbox_to_anchor = (0.5, -0.15), ncol = 4, prop = {'size': 10})