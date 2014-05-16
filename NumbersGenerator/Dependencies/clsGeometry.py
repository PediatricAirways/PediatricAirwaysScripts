# Imports

import math
from matplotlib import pyplot
import numpy

from clsValues import values
from clsInterpolations import interpolations
from clsLandmarks import landmarks
from clsLandmark import landmark

# Class definition

class geometry:

    # Constructors

    def __init__(self):

        self.valuesList = []
        self.landmarks = landmarks()
        self.interpolations = interpolations()

    def createGeometryFromFiles(self, coordinatesFilePath, perimeterFilePath, areaFilePath, landmarksIdFilePath):

        # Open the files

        coordinatesFile = open(coordinatesFilePath)
        perimeterFile = open(perimeterFilePath)
        areaFile = open(areaFilePath)
        landmarksIdFile = open(landmarksIdFilePath)

        # Create list

        coordinates = coordinatesFile.readlines()
        coordinates.pop(0) #Remove first line

        perimeters = perimeterFile.readlines()
        perimeters.pop(0) #Remove first line

        areas = areaFile.readlines()
        areas.pop(0) #Remove first line

        landmarksIds = landmarksIdFile.readlines()
        landmarksIds.pop(0) #Remove first line
        print landmarksIds

        # Close the files

        coordinatesFile.close()
        perimeterFile.close()
        areaFile.close()
        landmarksIdFile.close()

        # Create the values

        nbCoordinates = len(coordinates)
        nbPerimeters = len(perimeters)
        nbAreas = len(areas)
        nbLandmarksIds = len(landmarksIds)

        if nbPerimeters == nbCoordinates and nbAreas == nbCoordinates:

            coordinatesArray = []

            for i in range(nbCoordinates):
                parts = coordinates[i].split(" ")
                coordinatesArray.append([float(parts[0]), float(parts[1]), float(parts[2])])

            for i in range(nbCoordinates):

                # Distance

                xCurrent = coordinatesArray[i][0]
                yCurrent = coordinatesArray[i][1]
                zCurrent = coordinatesArray[i][2]

                if i == 0:

                    distanceTemp = 0

                else:

                    xPrevious = coordinatesArray[i - 1][0]
                    yPrevious = coordinatesArray[i - 1][1]
                    zPrevious = coordinatesArray[i - 1][2]

                    distanceTemp = math.pow(xPrevious - xCurrent, 2)
                    distanceTemp += math.pow(yPrevious - yCurrent, 2)
                    distanceTemp += math.pow(zPrevious - zCurrent, 2)
                    distanceTemp = math.sqrt(distanceTemp)

                    distanceTemp += self.valuesList[i - 1].getDistance()

                # Perimeter

                perimeterTemp = float(perimeters[i])

                # Area

                areaTemp = float(areas[i])

                # Hydraulic Diameter

                if perimeterTemp != 0:
                    hydraulicDiameterTemp = 4.0 * areaTemp / perimeterTemp
                else:
                    hydraulicDiameterTemp = 0.0

                # Add the incomplete values

                valuesTemp = values(i, -1, distanceTemp, perimeterTemp, areaTemp, hydraulicDiameterTemp, "")
                self.valuesList.append(valuesTemp)

            # Position

            airwaySize = self.valuesList[nbCoordinates - 1].getDistance()

            for i in range(nbCoordinates):
                self.valuesList[i].setPosition(self.valuesList[i].getDistance() / airwaySize)

            # Landmarks

            if nbLandmarksIds == 6:

                self.valuesList[int(landmarksIds[0]) - 1].setLandmarkName("NasalSpine")
                self.valuesList[int(landmarksIds[1]) - 1].setLandmarkName("PosteriorInferiorVomerCorner")
                self.valuesList[int(landmarksIds[2]) - 1].setLandmarkName("EpiglottisTip")
                self.valuesList[int(landmarksIds[3]) - 1].setLandmarkName("TVC")
                self.valuesList[int(landmarksIds[4]) - 1].setLandmarkName("Subglottic")
                self.valuesList[int(landmarksIds[5]) - 1].setLandmarkName("TracheaCarina")
                self.valuesList[self.getMidTracheaIndex()].setLandmarkName("MidTrachea")

            else:

                print("Error : {0} should contain six landmarks, look at Subglottic landmark before pre-processing.")
                quit()

            # Landmarks class

            self.computeLandmarks()

        else:

            print("Error: Different sizes of files")

    def computeInterpolations(self):
        self.interpolations.computeInterpolations(self.valuesList)

    def computeLandmarks(self):

        for valuesTemp in self.valuesList:

                landmarkNameTemp = valuesTemp.getLandmarkName()

                if landmarkNameTemp != "":

                    landmarkPositionTemp = valuesTemp.getPosition()
                    landmarkDistanceTemp = valuesTemp.getDistance()

                    self.landmarks.addLandmark(landmark(landmarkNameTemp, landmarkPositionTemp, landmarkDistanceTemp))

    # Getters

    def getValuesList(self):
        return self.valuesList

    def getInterpolations(self):
        return self.interpolations

    def getAirwaySize(self):
        return self.valuesList[len(self.valuesList) - 1].getDistance()

    def getLandmarks(self):
        return self.landmarks

    # Others

    def addValues(self, values):
        self.valuesList.append(values)

    def getValuesByLandmarkName(self, landmarkName):

        for valuesTemp in self.valuesList:
            if valuesTemp.getLandmarkName() == landmarkName:
                return valuesTemp

        return -1

    def getMidTracheaIndex(self):

        distanceSubglottic = self.getValuesByLandmarkName("Subglottic").getDistance()
        distanceTracheaCarrina = self.getValuesByLandmarkName("TracheaCarina").getDistance()

        distanceMidTrachea = (distanceSubglottic + distanceTracheaCarrina) / 2.0

        indexMidTrachea = -1

        for i in range(len(self.valuesList)):
            if indexMidTrachea == -1:
                if self.valuesList[i].getDistance() <= distanceMidTrachea and self.valuesList[i + 1].getDistance() >= distanceMidTrachea:
                    indexMidTrachea = i

        if self.valuesList[indexMidTrachea + 1].getDistance() - distanceMidTrachea < distanceMidTrachea - self.valuesList[indexMidTrachea].getDistance():
            indexMidTrachea += 1

        return indexMidTrachea

    def getIndexRange(self, distanceRange, index):

        nbValues = len(self.valuesList)

        indexInferior = -1
        indexSuperior = -1

        distanceMin = self.valuesList[0].getDistance()
        distanceMax = self.valuesList[nbValues - 1].getDistance()

        distanceAtIndex = self.valuesList[index].getDistance()

        distanceInferior = max(distanceAtIndex - distanceRange / 2.0, distanceMin)
        distanceSuperior = min(distanceAtIndex + distanceRange / 2.0, distanceMax)

        for i in range(nbValues):
            if self.valuesList[i].getDistance() <= distanceInferior:
                indexInferior = i
            else:
                break

        for i in reversed(range(nbValues)):
            if self.valuesList[i].getDistance() >= distanceSuperior:
                indexSuperior = i
            else:
                break

        indexRange = [indexInferior, indexSuperior]

        return indexRange

    def getQuantityAverage(self, quantityName, landmarkName, distanceRange):

        quantity = 0

        indexLandmark = self.getValuesByLandmarkName(landmarkName).getIndex()

        if distanceRange == 0:

            quantity = self.valuesList[indexLandmark].getQuantity(quantityName)

        else:

            indexRange = self.getIndexRange(distanceRange, indexLandmark)

            for i in range(indexRange[0], indexRange[1] + 1):
                quantity += self.valuesList[i].getQuantity(quantityName)

            quantity /= len(range(indexRange[0], indexRange[1] + 1))

        return quantity

    def setLandmarks(self, landmarks):
        self.landmarks = landmarks

    def display(self):

        for valuesTemp in self.valuesList:
            valuesTemp.display()

    def saveGeometry(self, geometryFilePath):

        geometryFile = open(geometryFilePath, 'w')

        for valuesTemp in self.valuesList:
            geometryFile.write(valuesTemp.toString() + "\n")

        geometryFile.close()

    def openGeometry(self, geometryFilePath):

        geometryFile = open(geometryFilePath, 'r')

        # Create the geometry

        for lineTemp in geometryFile.readlines():

            parts = lineTemp.split(" ")

            indexTemp = int(parts[0])
            positionTemp = float(parts[2])
            distanceTemp = float(parts[3])
            perimeterTemp = float(parts[4])
            areaTemp = float(parts[5])
            hydraulicDiameterTemp = float(parts[6])
            if parts[7] != "\n":
                landmarkNameTemp = parts[7].rstrip('\n')
            else:
                landmarkNameTemp = ""

            valuesTemp = values(indexTemp, positionTemp, distanceTemp, perimeterTemp, areaTemp, hydraulicDiameterTemp, landmarkNameTemp)

            self.valuesList.append(valuesTemp)

        # Create the landmarks

        self.computeLandmarks()

    def saveMeasurements(self, measurementsFilePath):

        nbDecimals = 5

        # Get perimeters

        perimeterTVC = self.getQuantityAverage("perimeter", "TVC", 0)
        perimeterSubglottic = self.getQuantityAverage("perimeter", "Subglottic", 1.5)
        perimeterMidTrachea = self.getQuantityAverage("perimeter",  "MidTrachea", 15)
        perimeterRatio = perimeterSubglottic / perimeterMidTrachea

        # Get areas

        areaTVC = self.getQuantityAverage("area", "TVC", 0)
        areaSubglottic = self.getQuantityAverage("area", "Subglottic", 1.5)
        areaMidTrachea = self.getQuantityAverage("area", "MidTrachea", 15)
        areaRatio = areaSubglottic / areaMidTrachea

        # Get hydraulic diameter

        hydraulicDiameterTVC = self.getQuantityAverage("hydraulicDiameter", "TVC", 0)
        hydraulicDiameterSubglottic = self.getQuantityAverage("hydraulicDiameter", "Subglottic", 1.5)
        hydraulicDiameterMidTrachea = self.getQuantityAverage("hydraulicDiameter", "MidTrachea", 15)
        hydraulicDiameterRatio = hydraulicDiameterSubglottic / hydraulicDiameterMidTrachea

        # Create the file

        measurementsFile = open(measurementsFilePath, 'w')

        measurementsFile.write("TVC : {0} {1} {2}\n".format(round(perimeterTVC, nbDecimals), round(areaTVC, nbDecimals), round(hydraulicDiameterTVC, nbDecimals)))
        measurementsFile.write("Subglottic : {0} {1} {2}\n".format(round(perimeterSubglottic, nbDecimals), round(areaSubglottic, nbDecimals), round(hydraulicDiameterSubglottic, nbDecimals)))
        measurementsFile.write("MidTrachea : {0} {1} {2}\n".format(round(perimeterMidTrachea, nbDecimals), round(areaMidTrachea, nbDecimals), round(hydraulicDiameterMidTrachea, nbDecimals)))
        measurementsFile.write("Ratio : {0} {1} {2}\n".format(round(perimeterRatio, nbDecimals), round(areaRatio, nbDecimals), round(hydraulicDiameterRatio, nbDecimals)))

        measurementsFile.close()

    def saveExtraMeasurements(self, extraMeasurementsFilePath):

        nbDecimals = 5

        # Get perimeters

        perimeterNasalSpine = self.getQuantityAverage("perimeter", "NasalSpine", 0)
        perimeterPosteriorInferiorVomerCorner = self.getQuantityAverage("perimeter", "PosteriorInferiorVomerCorner", 0)
        perimeterEpiglottisTip = self.getQuantityAverage("perimeter",  "EpiglottisTip", 0)

        # Get areas

        areaNasalSpine = self.getQuantityAverage("area", "NasalSpine", 0)
        areaPosteriorInferiorVomerCorner = self.getQuantityAverage("area", "PosteriorInferiorVomerCorner", 0)
        areaEpiglottisTip = self.getQuantityAverage("area", "EpiglottisTip", 0)

        # Get hydraulic diameter

        hydraulicDiameterNasalSpine = self.getQuantityAverage("hydraulicDiameter", "NasalSpine", 0)
        hydraulicDiameterPosteriorInferiorVomerCorner = self.getQuantityAverage("hydraulicDiameter", "PosteriorInferiorVomerCorner", 0)
        hydraulicDiameterEpiglottisTip = self.getQuantityAverage("hydraulicDiameter", "EpiglottisTip", 0)

        # Create the file

        extraMeasurementsFile = open(extraMeasurementsFilePath, 'w')

        extraMeasurementsFile.write("NasalSpine : {0} {1} {2}\n".format(round(perimeterNasalSpine, nbDecimals), round(areaNasalSpine, nbDecimals), round(hydraulicDiameterNasalSpine, nbDecimals)))
        extraMeasurementsFile.write("PosteriorInferiorVomerCorner : {0} {1} {2}\n".format(round(perimeterPosteriorInferiorVomerCorner, nbDecimals), round(areaPosteriorInferiorVomerCorner, nbDecimals), round(hydraulicDiameterPosteriorInferiorVomerCorner, nbDecimals)))
        extraMeasurementsFile.write("EpiglottisTip : {0} {1} {2}\n".format(round(perimeterEpiglottisTip, nbDecimals), round(areaEpiglottisTip, nbDecimals), round(hydraulicDiameterEpiglottisTip, nbDecimals)))

        extraMeasurementsFile.close()

    def plotGeometry(self, abscissa, marker, showInterpolation, title, plotFilePath):

        fig, ax = pyplot.subplots(3, 1, sharey = False)
        pyplot.subplots_adjust(hspace = 0.5)
        fig.suptitle(title)

        # Plots

        self.plotQuantity(abscissa, "perimeter", marker, showInterpolation, ax[0])
        self.plotQuantity(abscissa, "area", marker, showInterpolation, ax[1])
        self.plotQuantity(abscissa, "hydraulicDiameter", marker, showInterpolation, ax[2])

        # Save plot

        r = 1.5
        fig.set_size_inches(r * 9, r * 12)
        fig.savefig(plotFilePath, dpi = r * 2 * fig.dpi)
        fig.clf()
        pyplot.close()

    def plotQuantity(self, abscissa, quantity, marker, showInterpolation, ax):

        if quantity == "perimeter" or quantity == "hydraulicDiameter":
            yLabel = quantity.title() + " (mm)"
        elif quantity == "area":
            yLabel = quantity.title() + " (mm2)"

        # Plot series

        if showInterpolation == False:

            [X, Y] = self.getSerie(quantity, abscissa)
            ax.plot(X, Y, marker, label = quantity.title())

        elif showInterpolation == True:

            [X, Y] = self.getInterpolatedSerie(quantity, abscissa)
            ax.plot(X, Y, '--r', label = quantity.title())

        # Plot landmarks

        landmarksLineStyle = "solid" #"dashdot"
        landmarksLineColor = "k"

        for landmarkTemp in self.landmarks.getLandmarksList():
            ax.axvline(x = landmarkTemp.getAbscissa(abscissa), linestyle = landmarksLineStyle, color = landmarksLineColor)

        # Plot parameters

        ax.set_title(quantity.title())
        ax.set_xlabel(abscissa.title())
        ax.set_ylabel(yLabel)
        ax.set_xlim(numpy.min(X), numpy.max(X))
        ax.grid(True)
        ax.legend(loc = 1, prop = {'size': 10})

    def getSerie(self, quantity, abscissa):

        X = []
        Y = []

        for valuesTemp in self.getValuesList():
            X.append(valuesTemp.getAbscissa(abscissa))
            Y.append(valuesTemp.getQuantity(quantity))

        X = numpy.array(X)
        Y = numpy.array(Y)

        return [X, Y]

    def getInterpolatedSerie(self, quantity, abscissa):

        [X, Y] = self.getSerie(quantity, abscissa)

        XInterpolation = X
        YInterpolation = self.getInterpolations().getInterpolatesValues(quantity, abscissa, XInterpolation)

        return [XInterpolation, YInterpolation]
