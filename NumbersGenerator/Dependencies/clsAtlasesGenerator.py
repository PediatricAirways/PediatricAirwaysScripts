# Import

import os
import numpy
from matplotlib import pyplot

from clsAtlas import atlas

# Class definition

class atlasesGenerator:

    # Constructors

    def __init__(self, atlasType, dataBaseCRL, directoryPath):

        self.atlasType = atlasType
        self.medianLandmarks = dataBaseCRL.getMedianLandmarks()
        self.atlases = []

        if atlasType == "age":

            self.directoryPath = directoryPath + "AGE_ATLAS/"

            [ageMin, ageMax] = dataBaseCRL.getAgeBounds()

            self.valueBounds = [ageMin, ageMax]

            for ageTemp in range(ageMin, ageMax + 1):

                atlasTemp = atlas("age", ageTemp, dataBaseCRL, self.directoryPath)

                self.atlases.append(atlasTemp)

                print("--------------------------------------------------------------------------------")
                print("Type: age")
                print("Age: {0}".format(ageTemp))

        elif atlasType == "weight":

            self.directoryPath = directoryPath + "WEIGHT_ATLAS/"

            [weightMin, weightMax] = dataBaseCRL.getWeightBounds()

            self.valueBounds = [weightMin, weightMax]

            for weightTemp in range(weightMin, weightMax + 1):

                atlasTemp = atlas("weight", weightTemp, dataBaseCRL, self.directoryPath)

                self.atlases.append(atlasTemp)

                print("--------------------------------------------------------------------------------")
                print("Type: weight")
                print("Weight: {0}".format(weightTemp))

    # Others

    def saveGeometries(self, geometriesDirectoryPath = False):

        for atlasTemp in self.atlases:
            print("................................................................................")
            print("Save geometries for atlas {0}".format(atlasTemp.getValue()))
            atlasTemp.saveGeometries(geometriesDirectoryPath)

    def plotGeometries(self, graphsDirectoryPath = False):

        for atlasTemp in self.atlases:
            print("................................................................................")
            print("Plot geometries for atlas {0}".format(atlasTemp.getValue()))
            atlasTemp.plotGeometries(graphsDirectoryPath)

    def plotAtlases(self, graphsDirectoryPath = False):

        for atlasTemp in self.atlases:
            print("................................................................................")
            print("Plot atlases for atlas {0}".format(atlasTemp.getValue()))
            atlasTemp.plotAtlas(graphsDirectoryPath)

    def plotSummaryAtlases(self, directoryPath = False):

        self.plotPercentileAtlases(5, directoryPath)
        self.plotPercentileAtlases(25, directoryPath)
        self.plotPercentileAtlases(50, directoryPath)
        self.plotPercentileAtlases(75, directoryPath)
        self.plotPercentileAtlases(95, directoryPath)

    def plotPercentileAtlases(self, percentile, directoryPath = False):

        fig, ax = pyplot.subplots(3, 1, sharey = False)
        pyplot.subplots_adjust(hspace = 0.5)

        if self.atlasType == "age":
            fig.suptitle("Age atlas")
        elif self.atlasType == "weight":
            fig.suptitle("Weight atlas")

        # Plots

        self.plotQuantityAtlases(percentile, "perimeter", ax[0])
        self.plotQuantityAtlases(percentile, "area", ax[1])
        self.plotQuantityAtlases(percentile, "hydraulicDiameter", ax[2])

        # Save plot

        if directoryPath == False:
            directoryPath = self.directoryPath

        if(percentile == 5):
            plotFilePath = directoryPath + "ATLASES_0" + str(percentile) + "P.png"
        else:
            plotFilePath = directoryPath + "ATLASES_" + str(percentile) + "P.png"

        r = 1.5
        fig.set_size_inches(r * 9, r * 12)
        fig.savefig(plotFilePath, dpi = r * 2 * fig.dpi)
        fig.clf()
        pyplot.close()

    def plotQuantityAtlases(self, percentile, quantity, ax):

        X = []
        Y = []
        Z = []

        if self.atlasType == "age":
            color = "g"
        elif self.atlasType == "weight":
            color = "b"

        # Create the series

        for atlasTemp in self.atlases:

            # Get the values

            [XTemp, YTemp] = atlasTemp.getGeometry(percentile).getInterpolatedSerie(quantity, "position")

            # Add the values

            X.append(XTemp)
            Y.append(YTemp)
            Z.append(atlasTemp.getValue())

        # Plot the series

        for i in range(len(X)):
            ax.plot(X[i], Y[i], color = color, alpha = self.getOpacity(Z[i]))

        # Plot the landmarks

        landmarksLineStyle = "solid" #"dashdot"
        landmarksLineColor = "k"

        for landmarkTemp in self.medianLandmarks.getLandmarksList():
            ax.axvline(x = landmarkTemp.getAbscissa("position"), linestyle = landmarksLineStyle, color = landmarksLineColor)

        # Plot parameters

        ax.grid(True)

    def getOpacity(self, value):

        percentageMin = 0.25
        percentageMax = 1.0

        valueMin = float(self.valueBounds[0])
        valueMax = float(self.valueBounds[1])

        a = (percentageMax - percentageMin) / (valueMax - valueMin)
        b = 0.5 * ((percentageMax + percentageMin) - a * (valueMax + valueMin))

        opacity = a * value + b

        return opacity