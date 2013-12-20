# General imports

from matplotlib import pyplot

# Class imports



# Function import



# Class definition

class plot:

    # Constructors

    def __init__(self, name):

        self.name = name
        self.shareScale = [False, False]
        self.bounds = [[float("Inf"), -float("Inf")], [float("Inf"), -float("Inf")]]
        self.subPlots = []

    # Getters

    def getName(self):
        return self.name

    def getShareXScale(self):
        return self.shareScale[0]

    def getShareYScale(self):
        return self.shareScale[1]

    def getBounds(self):
        return self.bounds

    def getXBounds(self):
        return self.bounds[0]

    def getYBounds(self):
        return self.bounds[1]

    def getSubPlots(self):
        return self.subPlots

    # Setters

    def setShareXScale(self, bool):
        self.shareScale[0] = bool

    def setShareYScale(self, bool):
        self.shareScale[1] = bool

    # Others

    def addSubPlot(self, subPlot):
        self.subPlots.append(subPlot)
        self.computeBounds()

    def computeBounds(self):

        xMin = self.getXBounds()[0]
        xMax = self.getXBounds()[1]
        yMin = self.getYBounds()[0]
        yMax = self.getYBounds()[1]

        for subPlotTemp in self.getSubPlots():

            boundsTemp = subPlotTemp.getBounds()

            self.bounds[0][0] = min(xMin, boundsTemp[0][0])
            self.bounds[0][1] = max(xMax, boundsTemp[0][1])
            self.bounds[1][0] = min(yMin, boundsTemp[1][0])
            self.bounds[1][1] = max(yMax, boundsTemp[1][1])

    # Display & Save

    def plot(self):

        subPlots = self.getSubPlots()
        nbSubPlots = len(subPlots)

        fig, ax = pyplot.subplots(nbSubPlots, 1, sharex = self.getShareXScale(), sharey = self.getShareYScale())

        pyplot.subplots_adjust(hspace = 0.5)
        fig.suptitle(self.getName())

        for i in range(nbSubPlots):
            subPlots[i].plot(ax[i])

        pyplot.show()

    def save(self, fileName):

        subPlots = self.getSubPlots()
        nbSubPlots = len(subPlots)

        fig, ax = pyplot.subplots(nbSubPlots, 1, sharex = self.getShareXScale(), sharey = self.getShareYScale())

        pyplot.subplots_adjust(hspace = 0.5)
        fig.suptitle(self.getName())

        for i in range(nbSubPlots):
            subPlots[i].plot(ax[i])

        r = 1.5
        fig.set_size_inches(r * 9, r * 12)
        fig.savefig(fileName, dpi = r * 2 * fig.dpi)