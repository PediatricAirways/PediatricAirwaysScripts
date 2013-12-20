# Imports

import math
import os
import numpy
from matplotlib import pyplot

from clsGeometry import geometry
from clsWeightedVector import weightedVector
from clsValues import values

# Global variables

samplesNumber = 500
sigmaAge = 30.0 #In monthes
sigmaWeight = 14.0 #In kilograms

# Class definition

class atlas:

    # Constructors

    def __init__(self, atlasType, value, dataBase, atlasDirectoryPath):

        self.atlasType = atlasType
        self.medianLandmarks = dataBase.getMedianLandmarks()

        if atlasType == "age":
            self.directoryPath = atlasDirectoryPath + str(value) + "_MONTHS/"
        elif atlasType == "weight":
            self.directoryPath = atlasDirectoryPath + str(value) + "_KILOGRAMS/"

        self.geometry5 = geometry()
        self.geometry25 = geometry()
        self.geometry50 = geometry()
        self.geometry75 = geometry()
        self.geometry95 = geometry()

        self.weightedVectorList = []

        if atlasType == "age":
            self.age = value
            self.weight = False
            self.createAtlasForAge(samplesNumber, sigmaAge, dataBase)

        elif atlasType == "weight":
            self.age = False
            self.weight = value
            self.createAtlasForWeight(samplesNumber, sigmaWeight, dataBase)

        self.createGeometries()

    def createAtlasForAge(self, samplesNumber, sigmaAge, dataBase):

        for positionTemp in createPositionsVector(0, 1, samplesNumber):
            self.weightedVectorList.append(weightedVector("age", self.age, sigmaAge, positionTemp, dataBase))

    def createAtlasForWeight(self, samplesNumber, sigmaWeight, dataBase):

        for positionTemp in createPositionsVector(0, 1, samplesNumber):
            self.weightedVectorList.append(weightedVector("weight", self.weight, sigmaWeight, positionTemp, dataBase))

    # Getters

    def getAtlasType(self):
        return self.atlasType

    def getMedianLandmarks(self):
        return self.medianLandmarks

    def getDirectoryPath(self):
        return self.directoryPath

    def getAge(self):
        return self.age

    def getWeight(self):
        return self.weight

    def getValue(self):
        if self.atlasType == "age":
            return self.age
        elif self.atlasType == "weight":
            return self.weight

    def getGeometry(self, percentile):
        if percentile == 5:
            return self.geometry5
        elif percentile == 25:
            return self.geometry25
        elif percentile == 50:
            return self.geometry50
        elif percentile == 75:
            return self.geometry75
        elif percentile == 95:
            return self.geometry95

    # Others

    def createGeometries(self):
        self.geometry5 = self.createGeometry(5)
        self.geometry25 = self.createGeometry(25)
        self.geometry50 = self.createGeometry(50)
        self.geometry75 = self.createGeometry(75)
        self.geometry95 = self.createGeometry(95)

    def createGeometry(self, percentile):

        geometryTemp = geometry()
        geometryTemp.setLandmarks(self.medianLandmarks)

        for i in range(len(self.weightedVectorList)):

            weightedVectorTemp = self.weightedVectorList[i]

            indexTemp = i
            positionTemp = weightedVectorTemp.getPosition()
            distanceTemp = -1
            perimeterTemp = weightedVectorTemp.getQuantityForPercentile("perimeter", percentile)
            areaTemp = weightedVectorTemp.getQuantityForPercentile("area", percentile)
            hydraulicDiameterTemp = weightedVectorTemp.getQuantityForPercentile("hydraulicDiameter", percentile)
            landmarkNameTemp = ""

            valuesTemp = values(indexTemp, positionTemp, distanceTemp, perimeterTemp, areaTemp, hydraulicDiameterTemp, landmarkNameTemp)

            geometryTemp.addValues(valuesTemp)

        geometryTemp.computeInterpolations()

        return geometryTemp

    def saveGeometries(self, geometriesDirectoryPath = False):

        if geometriesDirectoryPath == False:
            geometriesDirectoryPath = self.directoryPath + "GEOMETRIES/"

        if not os.path.exists(geometriesDirectoryPath):
            os.makedirs(geometriesDirectoryPath)

        self.geometry5.saveGeometry(geometriesDirectoryPath + "ATLAS_05P.txt")
        self.geometry25.saveGeometry(geometriesDirectoryPath + "ATLAS_25P.txt")
        self.geometry50.saveGeometry(geometriesDirectoryPath + "ATLAS_50P.txt")
        self.geometry75.saveGeometry(geometriesDirectoryPath + "ATLAS_75P.txt")
        self.geometry95.saveGeometry(geometriesDirectoryPath + "ATLAS_95P.txt")

    def plotGeometries(self, graphsDirectoryPath = False):

        if graphsDirectoryPath == False:
            graphsDirectoryPath = self.directoryPath + "GRAPHICS/"

        if not os.path.exists(graphsDirectoryPath):
            os.makedirs(graphsDirectoryPath)

        if self.atlasType == "age":
            unit = " months"
            markerColor = "g"
        elif self.atlasType == "weight":
            unit = " kilograms"
            markerColor = "b"

        value = self.getValue()
        abscissa = "position"
        showInterpolation = True

        self.geometry5.plotGeometry(abscissa, "-." + markerColor, showInterpolation, "Atlas 05% for " + str(value) + unit, graphsDirectoryPath + "ATLAS_05P.png")
        self.geometry25.plotGeometry(abscissa, "--" + markerColor, showInterpolation, "Atlas 25% for " + str(value) + unit, graphsDirectoryPath + "ATLAS_25P.png")
        self.geometry50.plotGeometry(abscissa, "-" + markerColor, showInterpolation, "Atlas 50% for " + str(value) + unit, graphsDirectoryPath + "ATLAS_50P.png")
        self.geometry75.plotGeometry(abscissa, "--" + markerColor, showInterpolation, "Atlas 75% for " + str(value) + unit, graphsDirectoryPath + "ATLAS_75P.png")
        self.geometry95.plotGeometry(abscissa, "-." + markerColor, showInterpolation, "Atlas 95% for " + str(value) + unit, graphsDirectoryPath + "ATLAS_95P.png")

    def plotAtlas(self, graphsDirectoryPath = False):

        fig, ax = pyplot.subplots(3, 1, sharey = False)
        pyplot.subplots_adjust(hspace = 0.5)

        if self.atlasType == "age":
            fig.suptitle("Atlas for {0} months".format(self.age))
        elif self.atlasType == "weight":
            fig.suptitle("Atlas for {0} kilograms".format(self.weight))

        # Plots

        self.plotQuantityAtlas("perimeter", ax[0])
        self.plotQuantityAtlas("area", ax[1])
        self.plotQuantityAtlas("hydraulicDiameter", ax[2])

        # Save plot

        if graphsDirectoryPath == False:
            graphsDirectoryPath = self.directoryPath + "GRAPHICS/"

        if not os.path.exists(graphsDirectoryPath):
            os.makedirs(graphsDirectoryPath)

        plotFilePath = graphsDirectoryPath + "ATLAS.png"

        r = 1.5
        fig.set_size_inches(r * 9, r * 12)
        fig.savefig(plotFilePath, dpi = r * 2 * fig.dpi)
        fig.clf()
        pyplot.close()

    def plotQuantityAtlas(self, quantity, ax):

        if self.atlasType == "age":
            markerColor = "g"
        elif self.atlasType == "weight":
            markerColor = "b"

        # Get the series

        [X5, Y5] = self.geometry5.getInterpolatedSerie(quantity, "position")
        [X25, Y25] = self.geometry25.getInterpolatedSerie(quantity, "position")
        [X50, Y50] = self.geometry50.getInterpolatedSerie(quantity, "position")
        [X75, Y75] = self.geometry75.getInterpolatedSerie(quantity, "position")
        [X95, Y95] = self.geometry95.getInterpolatedSerie(quantity, "position")

        # Plot the series

        ax.plot(X5, Y5, "-." + markerColor, label = quantity.title() + "05%")
        ax.plot(X25, Y25, "--" + markerColor, label = quantity.title() + "25%")
        ax.plot(X50, Y50, "-" + markerColor, label = quantity.title() + "50%")
        ax.plot(X75, Y75, "--" + markerColor, label = quantity.title() + "75%")
        ax.plot(X95, Y95, "-." + markerColor, label = quantity.title() + "95%")

        # Plot the landmarks

        landmarksLineStyle = "solid" #"dashdot"
        landmarksLineColor = "k"

        for landmark in self.medianLandmarks.getLandmarksList():
            ax.axvline(x = landmark.getAbscissa("position"), linestyle = landmarksLineStyle, color = landmarksLineColor)

        # Plot parameters

        if quantity == "perimeter" or quantity == "hydraulicDiameter":
            yLabel = quantity.title() + " (mm)"
        elif quantity == "area":
            yLabel = quantity.title() + " (mm2)"

        ax.set_title(quantity.title())
        ax.set_xlabel("Position")
        ax.set_ylabel(yLabel)
        ax.grid(True)
        ax.legend(loc = 1, prop = {'size': 10})

# Functions definition

def createPositionsVector(a, b, samplesNumber):

    positions = []

    increment = float((b - a) / float(samplesNumber))

    for i in range(samplesNumber + 1):
        positions.append(a + i * increment)

    return positions