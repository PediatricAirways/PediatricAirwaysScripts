# Imports

import os
import numpy

from clsCase import case
from clsLandmarks import landmarks
from clsLandmark import landmark
from clsValues import values

class dataBase:

    # Constructors

    def __init__(self, name, type):

        self.name = name
        self.type = type
        self.cases = []

        self.medianLandmarks = landmarks()
        self.medianValues = False

    def createDataBase(self, inputsDirectoryPath, inputsFilePath):

        inputsFile = open(inputsFilePath)

        for lineTemp in inputsFile:

            lineTemp = lineTemp.rstrip('\n')
            parts = lineTemp.split(" ")

            nameTemp = parts[0]
            typeTemp = self.getType()
            genderTemp = parts[2]
            ageTemp = round(float(parts[3]), 0)
            weightTemp = round(float(parts[4]), 1)
            airwayClassTemp = parts[5]
            directoryPathTemp = inputsDirectoryPath + nameTemp + "/"

            caseTemp = case(nameTemp, typeTemp, genderTemp, ageTemp, weightTemp, airwayClassTemp, directoryPathTemp)

            self.cases.append(caseTemp)

    # Getters

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getCases(self):
        return self.cases

    def getMedianLandmarks(self):
        return self.medianLandmarks

    def getMedianValues(self):
        return self.medianValues

    # Setters

    def setMedianLandmarks(self, medianLandmarks):
        self.medianLandmarks = medianLandmarks

    def setMedianValues(self, medianValues):
        self.medianValues = medianValues

    # Others

    def computeMedianLandmarks(self):

        # Compute medians

        positionsNasalSpine = []
        positionsPosteriorInferiorVomerCorner = []
        positionsEpiglottisTip = []
        positionsTVC = []
        positionsSubglottic = []
        positionsMidTrachea = []
        positionsTracheaCarina = []

        airwaySizes = []

        for caseTemp in self.cases:

            positionsNasalSpine.append(caseTemp.getGeometry().getValuesByLandmarkName("NasalSpine").getPosition())
            positionsPosteriorInferiorVomerCorner.append(caseTemp.getGeometry().getValuesByLandmarkName("PosteriorInferiorVomerCorner").getPosition())
            positionsEpiglottisTip.append(caseTemp.getGeometry().getValuesByLandmarkName("EpiglottisTip").getPosition())
            positionsTVC.append(caseTemp.getGeometry().getValuesByLandmarkName("TVC").getPosition())
            positionsSubglottic.append(caseTemp.getGeometry().getValuesByLandmarkName("Subglottic").getPosition())
            positionsMidTrachea.append(caseTemp.getGeometry().getValuesByLandmarkName("MidTrachea").getPosition())
            positionsTracheaCarina.append(caseTemp.getGeometry().getValuesByLandmarkName("TracheaCarina").getPosition())

            airwaySizes.append(caseTemp.getGeometry().getAirwaySize())

        medianNasalSpine = numpy.median(numpy.array(positionsNasalSpine))
        medianPosteriorInferiorVomerCorner = numpy.median(numpy.array(positionsPosteriorInferiorVomerCorner))
        medianEpiglottisTip = numpy.median(numpy.array(positionsEpiglottisTip))
        medianTVC = numpy.median(numpy.array(positionsTVC))
        medianSubglottic = numpy.median(numpy.array(positionsSubglottic))
        medianMidTrachea = numpy.median(numpy.array(positionsMidTrachea))
        medianTracheaCarina = numpy.median(numpy.array(positionsTracheaCarina))

        medianAirwaySize = numpy.median(numpy.array(airwaySizes))

        # Set values

        self.medianLandmarks.addLandmark(landmark("NasalSpine", medianNasalSpine, medianNasalSpine * medianAirwaySize))
        self.medianLandmarks.addLandmark(landmark("PosteriorInferiorVomerCorner", medianPosteriorInferiorVomerCorner, medianPosteriorInferiorVomerCorner * medianAirwaySize))
        self.medianLandmarks.addLandmark(landmark("EpiglottisTip", medianEpiglottisTip, medianEpiglottisTip * medianAirwaySize))
        self.medianLandmarks.addLandmark(landmark("TVC", medianTVC, medianTVC * medianAirwaySize))
        self.medianLandmarks.addLandmark(landmark("Subglottic", medianSubglottic, medianSubglottic * medianAirwaySize))
        self.medianLandmarks.addLandmark(landmark("MidTrachea", medianMidTrachea, medianMidTrachea * medianAirwaySize))
        self.medianLandmarks.addLandmark(landmark("TracheaCarina", medianTracheaCarina, medianTracheaCarina * medianAirwaySize))

    def computeMedianValues(self, dataBaseCRL):

        ratiosPerimeter = []
        ratiosArea = []
        ratiosHydraulicDiameter = []

        for caseTemp in dataBaseCRL.getCases():

            ratioPerimeterTemp = caseTemp.getGeometry().getValuesByLandmarkName("Subglottic").getPerimeter() / caseTemp.getGeometry().getValuesByLandmarkName("MidTrachea").getPerimeter()
            ratioAreaTemp = caseTemp.getGeometry().getValuesByLandmarkName("Subglottic").getArea() / caseTemp.getGeometry().getValuesByLandmarkName("MidTrachea").getArea()
            ratioHydraulicDiameterTemp = caseTemp.getGeometry().getValuesByLandmarkName("Subglottic").getHydraulicDiameter() / caseTemp.getGeometry().getValuesByLandmarkName("MidTrachea").getHydraulicDiameter()

            ratiosPerimeter.append(ratioPerimeterTemp)
            ratiosArea.append(ratioAreaTemp)
            ratiosHydraulicDiameter.append(ratioHydraulicDiameterTemp)

        medianPerimeters = numpy.median(numpy.array(ratiosPerimeter))
        medianAreas = numpy.median(numpy.array(ratiosArea))
        medianHydraulicDiameters = numpy.median(numpy.array(ratiosHydraulicDiameter))

        self.medianValues = values(-1, -1, -1, medianPerimeters, medianAreas, medianHydraulicDiameters, "RatioScore")

    def computeRegistredGeometries(self):

        for caseTemp in self.cases:
            print("................................................................................")
            print("Compute the registred geometry for patient {0}".format(caseTemp.getNumber()))
            caseTemp.computeRegistredGeometry(self.medianLandmarks)

    def saveRegistredGeometries(self, registredGeometryDirectoryPath = False):

        for caseTemp in self.cases:
            print("................................................................................")
            print("Save the registred geometry for patient {0}".format(caseTemp.getNumber()))
            caseTemp.saveRegistredGeometry(registredGeometryDirectoryPath)

    def savePlots(self, graphsDirectoryPath = False):

        for caseTemp in self.cases:
            print("................................................................................")
            print("Save plots for patient {0}".format(caseTemp.getNumber()))
            caseTemp.savePlot(graphsDirectoryPath)

    def saveScores(self):

        for caseTemp in self.cases:
            print("................................................................................")
            print("Save scores for patient {0}".format(caseTemp.getNumber()))
            caseTemp.saveScores(self.medianValues)

    def computeInterpolations(self):

        for caseTemp in self.cases:
            print("................................................................................")
            print("Compute the interpolations for patient {0}".format(caseTemp.getNumber()))
            caseTemp.computeInterpolations()

    def getAgeBounds(self):

        minAge = +float("Inf")
        maxAge = -float("Inf")

        for caseTemp in self.cases:

            age = caseTemp.getAge()

            minAge = min(minAge, age)
            maxAge = max(maxAge, age)

        return [int(minAge), int(maxAge)]

    def getWeightBounds(self):

        minWeight = +float("Inf")
        maxWeight = -float("Inf")

        for caseTemp in self.cases:

            weight = caseTemp.getWeight()

            minWeight = min(minWeight, weight)
            maxWeight = max(maxWeight, weight)

        return [int(minWeight), int(maxWeight)]

    def computeAtlases(self, atlasType, dataBaseCRL):

        for caseTemp in self.cases:
            print("................................................................................")
            print("Compute atlases for patient {0}".format(caseTemp.getNumber()))
            caseTemp.computeAtlas(atlasType, dataBaseCRL)

    def plotComparisons(self, graphsDirectoryPath = False):

        for caseTemp in self.cases:
            print("................................................................................")
            print("Plot comparision for patient {0}".format(caseTemp.getNumber()))
            caseTemp.plotComparisons(graphsDirectoryPath)

    def display(self):

        print("{0} : {1}".format(self.getName(), self.getType()))

        print("--------------------------------------------------------------------------------")

        for caseTemp in self.cases:
            caseTemp.display()
            print("--------------------------------------------------------------------------------")

    def test(self):
        for caseTemp in self.cases:
            caseTemp.computeAtlasScores()