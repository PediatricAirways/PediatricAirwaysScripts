# Imports

import os
from matplotlib import pyplot
import numpy

from clsGeometry import geometry
from clsLandmarks import landmarks
from clsValues import values
from clsAtlas import atlas

# Class definition

class case:

    # Constructors

    def __init__(self, number, type, gender, age, weight, airwayClass, directoryPath):

        self.number = number #CT scan number
        self.type = type #CRL or SGS
        self.gender = gender #M or F
        self.age = age
        self.weight = weight
        self.airwayClass = airwayClass #Class of the CT scan

        self.directoryPath = directoryPath

        self.geometry = geometry() #Main geometry
        self.registredGeometry = geometry() #Geometry registred
        self.weightAtlas = False
        self.ageAtlas = False

        geometryFilePath = directoryPath + number + "_GEOMETRY.txt"

        self.geometry.openGeometry(geometryFilePath)

    # Getters

    def getNumber(self):
        return self.number

    def getType(self):
        return self.type

    def getGender(self):
        return self.gender

    def getAge(self):
        return self.age

    def getWeight(self):
        return self.weight

    def getAirwayClass(self):
        return self.airwayClass

    def getDirectoryPath(self):
        return self.directoryPath

    def getGeometry(self):
        return self.geometry

    def getRegistredGeometry(self):
        return self.registredGeometry

    def getAtlas(self, atlasType):
        if atlasType == "age":
            return self.ageAtlas
        elif atlasType == "weight":
            return self.weightAtlas

    # Others

    def computeRegistredGeometry(self, medianLandmarks):

        # Get the landmarks positions

        positionNasalSpine = self.getGeometry().getValuesByLandmarkName("NasalSpine").getAbscissa("position")
        positionPosteriorInferiorVomerCorner = self.getGeometry().getValuesByLandmarkName("PosteriorInferiorVomerCorner").getAbscissa("position")
        positionEpiglottisTip = self.getGeometry().getValuesByLandmarkName("EpiglottisTip").getAbscissa("position")
        positionTVC = self.getGeometry().getValuesByLandmarkName("TVC").getAbscissa("position")
        positionSubglottic = self.getGeometry().getValuesByLandmarkName("Subglottic").getAbscissa("position")
        positionMidTrachea = self.getGeometry().getValuesByLandmarkName("MidTrachea").getAbscissa("position")
        positionTracheaCarina = self.getGeometry().getValuesByLandmarkName("TracheaCarina").getAbscissa("position")

        positionMedianNasalSpine = medianLandmarks.getLandmarkByName("NasalSpine").getAbscissa("position")
        positionMedianPosteriorInferiorVomerCorner = medianLandmarks.getLandmarkByName("PosteriorInferiorVomerCorner").getAbscissa("position")
        positionMedianEpiglottisTip = medianLandmarks.getLandmarkByName("EpiglottisTip").getAbscissa("position")
        positionMedianTVC = medianLandmarks.getLandmarkByName("TVC").getAbscissa("position")
        positionMedianSubglottic = medianLandmarks.getLandmarkByName("Subglottic").getAbscissa("position")
        positionMedianMidTrachea = medianLandmarks.getLandmarkByName("MidTrachea").getAbscissa("position")
        positionMedianTracheaCarina = medianLandmarks.getLandmarkByName("TracheaCarina").getAbscissa("position")

        # Compute the registrations coefficients

        coefficientsSet1 = computeCoefficientsRegistration(positionNasalSpine, positionMedianNasalSpine, positionPosteriorInferiorVomerCorner, positionMedianPosteriorInferiorVomerCorner)
        coefficientsSet2 = computeCoefficientsRegistration(positionPosteriorInferiorVomerCorner, positionMedianPosteriorInferiorVomerCorner, positionEpiglottisTip, positionMedianEpiglottisTip)
        coefficientsSet3 = computeCoefficientsRegistration(positionEpiglottisTip, positionMedianEpiglottisTip, positionTVC, positionMedianTVC)
        coefficientsSet4 = computeCoefficientsRegistration(positionTVC, positionMedianTVC, positionSubglottic, positionMedianSubglottic)
        coefficientsSet5 = computeCoefficientsRegistration(positionSubglottic, positionMedianSubglottic, positionMidTrachea, positionMedianMidTrachea)
        coefficientsSet6 = computeCoefficientsRegistration(positionMidTrachea, positionMedianMidTrachea, positionTracheaCarina, positionMedianTracheaCarina)

        # Compute the registred geometry

        indexNasalSpine = self.getGeometry().getValuesByLandmarkName("NasalSpine").getIndex()
        indexPosteriorInferiorVomerCorner = self.getGeometry().getValuesByLandmarkName("PosteriorInferiorVomerCorner").getIndex()
        indexEpiglottisTip = self.getGeometry().getValuesByLandmarkName("EpiglottisTip").getIndex()
        indexTVC = self.getGeometry().getValuesByLandmarkName("TVC").getIndex()
        indexSubglottic = self.getGeometry().getValuesByLandmarkName("Subglottic").getIndex()
        indexMidTrachea = self.getGeometry().getValuesByLandmarkName("MidTrachea").getIndex()
        indexTracheaCarina = self.getGeometry().getValuesByLandmarkName("TracheaCarina").getIndex()

        for valuesTemp in self.geometry.getValuesList():

            indexTemp = valuesTemp.getIndex()
            positionTemp = valuesTemp.getPosition()
            distanceTemp = valuesTemp.getDistance()
            perimeterTemp = valuesTemp.getPerimeter()
            areaTemp = valuesTemp.getArea()
            hydraulicDiameterTemp = valuesTemp.getHydraulicDiameter()
            landmarkNameTemp = valuesTemp.getLandmarkName()

            if indexTemp <= indexPosteriorInferiorVomerCorner:
                positionRegistredTemp = positionTemp * coefficientsSet1[0] + coefficientsSet1[1]
            elif indexTemp <= indexEpiglottisTip:
                positionRegistredTemp = positionTemp * coefficientsSet2[0] + coefficientsSet2[1]
            elif indexTemp <= indexTVC:
                positionRegistredTemp = positionTemp * coefficientsSet3[0] + coefficientsSet3[1]
            elif indexTemp <= indexSubglottic:
                positionRegistredTemp = positionTemp * coefficientsSet4[0] + coefficientsSet4[1]
            elif indexTemp <= indexMidTrachea:
                positionRegistredTemp = positionTemp * coefficientsSet5[0] + coefficientsSet5[1]
            elif indexTemp <= indexTracheaCarina:
                positionRegistredTemp = positionTemp * coefficientsSet6[0] + coefficientsSet6[1]

            valuesTemp2 = values(indexTemp, positionRegistredTemp, distanceTemp, perimeterTemp, areaTemp, hydraulicDiameterTemp, landmarkNameTemp)

            self.registredGeometry.addValues(valuesTemp2)

        self.registredGeometry.landmarks = medianLandmarks

    def saveRegistredGeometry(self, registredGeometryDirectoryPath = False):

        if registredGeometryDirectoryPath == False:
            registredGeometryDirectoryPath = self.directoryPath

        registredGeometryFilePath = registredGeometryDirectoryPath + self.number + "_REGISTRED_GEOMETRY.txt"

        self.registredGeometry.saveGeometry(registredGeometryFilePath)

    def computeInterpolations(self):

        self.geometry.computeInterpolations()
        self.registredGeometry.computeInterpolations()

    def computeAtlas(self, atlasType, dataBaseCRL):

        print("................................................................................")

        if atlasType == "age":
            self.ageAtlas = atlas("age", self.age, dataBaseCRL, self.directoryPath)
        elif atlasType == "weight":
            self.weightAtlas = atlas("weight", self.weight, dataBaseCRL, self.directoryPath)
        elif atlasType == "both":
            self.ageAtlas = atlas("age", self.age, dataBaseCRL, self.directoryPath)
            self.weightAtlas = atlas("weight", self.weight, dataBaseCRL, self.directoryPath)

    def computeAtlasScore(self, quantity):

        [X5, Y5] = self.getAtlas("age").getGeometry(5).getSerie(quantity, "position")

        XReal = X5
        YReal = self.getGeometry().getInterpolations().getInterpolatesValues(quantity, "position", XReal)

        quantityAtlasScores = (YReal - Y5) / Y5

        quantityAtlasScore = min(quantityAtlasScores)

        return quantityAtlasScore

    def computeRatioScore(self, quantity, medianValues):

        ratioQuantity = self.getGeometry().getValuesByLandmarkName("Subglottic").getQuantity(quantity) / self.getGeometry().getValuesByLandmarkName("MidTrachea").getQuantity(quantity)

        ratioQuantityScore = 1.0 - ratioQuantity / medianValues.getQuantity(quantity)

        return ratioQuantityScore

    def display(self):

        print("Number: {0}".format(self.getNumber()))
        print("Type: {0}".format(self.getType()))
        print("Gender: {0}".format(self.getGender()))
        print("Age: {0}".format(self.getAge()))
        print("Weight: {0}".format(self.getWeight()))
        print("Airway class: {0}".format(self.getAirwayClasses()))

        print("................................................................................")

        self.getGeometry().display()

    # Plots

    def savePlot(self, graphsDirectoryPath = False):

        self.plotQuantity("perimeter", graphsDirectoryPath)
        self.plotQuantity("area", graphsDirectoryPath)
        self.plotQuantity("hydraulicDiameter", graphsDirectoryPath)

    def plotQuantity(self, quantity, graphsDirectoryPath = False):

        landmarksLineStyle = "solid" #"dashdot"
        landmarksLineColor = "k"

        fig, ax = pyplot.subplots(2, 1, sharey = True)
        pyplot.subplots_adjust(hspace = 0.5)
        fig.suptitle(quantity.title())

        #

        if quantity == "perimeter" or quantity == "hydraulicDiameter":
            yLabel = quantity.title() + " (mm)"
        elif quantity == "area":
            yLabel = quantity.title() + " (mm2)"

        # Plot unregistred geometry

        geometryTemp = self.getGeometry()

        [X, Y] = geometryTemp.getSerie(quantity, "distance")
        ax[0].plot(X, Y, 'xr', label = quantity.title())

        Xinterpolation = numpy.linspace(min(X), max(X), 100)
        Yinterpolation = geometryTemp.getInterpolations().getInterpolatesValues(quantity, "distance", Xinterpolation)
        ax[0].plot(Xinterpolation, Yinterpolation, '--r', label = quantity.title())

        for landmarkTemp in geometryTemp.getLandmarks().getLandmarksList():
            ax[0].axvline(x = landmarkTemp.getAbscissa("distance"), linestyle = landmarksLineStyle, color = landmarksLineColor)

        ax[0].set_title(quantity.title())
        ax[0].set_xlabel("Distance (mm)")
        ax[0].set_ylabel(yLabel)
        ax[0].set_xlim(min(X), max(X))
        ax[0].grid(True)
        ax[0].legend(loc = 4, prop = {'size': 10})

        # Plot registred geometry

        geometryTemp = self.getRegistredGeometry()

        [X, Y] = geometryTemp.getSerie(quantity, "position")
        ax[1].plot(X, Y, 'xr', label = quantity.title())

        Xinterpolation = numpy.linspace(min(X), max(X), 1000)
        Yinterpolation = geometryTemp.getInterpolations().getInterpolatesValues(quantity, "position", Xinterpolation)
        ax[1].plot(Xinterpolation, Yinterpolation, '--r', label = quantity.title())

        for landmarkTemp in geometryTemp.getLandmarks().getLandmarksList():
            ax[1].axvline(x = landmarkTemp.getAbscissa("position"), linestyle = landmarksLineStyle, color = landmarksLineColor)

        ax[1].set_title(quantity.title() + " registred")
        ax[1].set_xlabel("Position")
        ax[1].set_ylabel(yLabel)
        ax[1].set_xlim(min(X), max(X))
        ax[1].grid(True)
        ax[1].legend(loc = 4, prop = {'size': 10})

        # Save plot

        if graphsDirectoryPath == False:
            graphsDirectoryPath = self.directoryPath + self.number + "_GRAPHICS/"

        if not os.path.exists(graphsDirectoryPath):
            os.makedirs(graphsDirectoryPath)

        if quantity == "perimeter":
            plotFilePath = graphsDirectoryPath + self.number + "_PERIMETER.png"
        elif quantity == "area":
            plotFilePath = graphsDirectoryPath + self.number + "_AREA.png"
        elif quantity == "hydraulicDiameter":
            plotFilePath = graphsDirectoryPath + self.number + "_HYDRAULIC_DIAMETER.png"

        r = 1.5
        fig.set_size_inches(r * 9, r * 12)
        fig.savefig(plotFilePath, dpi = r * 2 * fig.dpi)
        fig.clf()
        pyplot.close()

    def plotComparisons(self, graphsDirectoryPath = False):

        fig, ax = pyplot.subplots(3, 1)
        pyplot.subplots_adjust(hspace = 0.5)
        fig.suptitle("Comparison with age and weight atlas")

        # Plot the perimeter

        self.plotComparision("perimeter", ax[0])
        self.plotComparision("area", ax[1])
        self.plotComparision("hydraulicDiameter", ax[2])

        # Save plot

        if graphsDirectoryPath == False:
            graphsDirectoryPath = self.directoryPath + self.number + "_GRAPHICS/"

        if not os.path.exists(graphsDirectoryPath):
            os.makedirs(graphsDirectoryPath)

        plotFilePath = graphsDirectoryPath + self.number + "_ATLAS.png"

        r = 1.5
        fig.set_size_inches(r * 9, r * 12)
        fig.savefig(plotFilePath, dpi = r * 2 * fig.dpi)

    def plotComparision(self, quantity, ax):

        landmarksLineStyle = "solid" #"dashdot"
        landmarksLineColor = "k"

        if quantity == "perimeter" or quantity == "hydraulicDiameter":
            yLabel = quantity.title() + " (mm)"
        elif quantity == "area":
            yLabel = quantity.title() + " (mm2)"

        # Plot the real values

        [X, Y] = self.registredGeometry.getSerie(quantity, "position")
        ax.plot(X, Y, 'xr', label = quantity.title())

        # Plot the interpolation

        Xinterpolation = numpy.linspace(min(X), max(X), 100)
        Yinterpolation = self.registredGeometry.getInterpolations().getInterpolatesValues(quantity, "position", Xinterpolation)
        ax.plot(Xinterpolation, Yinterpolation, '--r', label = quantity.title())

        # Plot the atlas

        if self.ageAtlas != False:
            [X5, Y5] = self.ageAtlas.getGeometry(5).getSerie(quantity, "position")
            [X25, Y25] = self.ageAtlas.getGeometry(25).getSerie(quantity, "position")
            [X50, Y50] = self.ageAtlas.getGeometry(50).getSerie(quantity, "position")
            [X75, Y75] = self.ageAtlas.getGeometry(75).getSerie(quantity, "position")
            [X95, Y95] = self.ageAtlas.getGeometry(95).getSerie(quantity, "position")

            ax.plot(X5, Y5, '-.g', label = "Age atlas 05%")
            ax.plot(X25, Y25, '--g', label = "Age atlas 25%")
            ax.plot(X50, Y50, '-g', label = "Age atlas 50%")
            ax.plot(X75, Y75, '--g', label = "Age atlas 75%")
            ax.plot(X95, Y95, '-.g', label = "Age atlas 95%")

        if self.weightAtlas != False:
            [X5, Y5] = self.weightAtlas.getGeometry(5).getSerie(quantity, "position")
            [X25, Y25] = self.weightAtlas.getGeometry(25).getSerie(quantity, "position")
            [X50, Y50] = self.weightAtlas.getGeometry(50).getSerie(quantity, "position")
            [X75, Y75] = self.weightAtlas.getGeometry(75).getSerie(quantity, "position")
            [X95, Y95] = self.weightAtlas.getGeometry(95).getSerie(quantity, "position")

            ax.plot(X5, Y5, '-.b', label = "Weight atlas 05%")
            ax.plot(X25, Y25, '--b', label = "Weight atlas 25%")
            ax.plot(X50, Y50, '-b', label = "Weight atlas 50%")
            ax.plot(X75, Y75, '--b', label = "Weight atlas 75%")
            ax.plot(X95, Y95, '-.b', label = "Weight atlas 95%")

        # Plot the landmarks

        for landmarkTemp in self.registredGeometry.getLandmarks().getLandmarksList():
            ax.axvline(x = landmarkTemp.getAbscissa("position"), linestyle = landmarksLineStyle, color = landmarksLineColor)

        # Plot parameters

        ax.set_title(quantity.title())
        ax.set_xlabel("Position")
        ax.set_ylabel(yLabel)
        ax.set_xlim(min(X), max(X))
        ax.grid(True)
        ax.legend(loc = 1, prop = {'size': 10})

    def saveScores(self, medianValues, directoryPath = False):

        nbDecimals = 5

        # Get the values

        ratioScorePerimeter = round(self.computeRatioScore("perimeter", medianValues), nbDecimals)
        ratioScoreArea = round(self.computeRatioScore("area", medianValues), nbDecimals)
        ratioScoreHydraulicDiameter = round(self.computeRatioScore("hydraulicDiameter", medianValues), nbDecimals)

        atlasScorePerimeter = round(self.computeAtlasScore("perimeter"), nbDecimals)
        atlasScoreArea = round(self.computeAtlasScore("area"), nbDecimals)
        atlasScoreHydraulicDiameter = round(self.computeAtlasScore("hydraulicDiameter"), nbDecimals)

        # Create the file

        if directoryPath == False:
            directoryPath = self.directoryPath

        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)

        scoresFilePath = directoryPath + self.number + "_SCORES.txt"

        scoresFile = open(scoresFilePath, "w")

        scoresFile.write("RatioScore : {0} {1} {2}\n".format(ratioScorePerimeter, ratioScoreArea, ratioScoreHydraulicDiameter))
        scoresFile.write("AtlasScore : {0} {1} {2}".format(atlasScorePerimeter, atlasScoreArea, atlasScoreHydraulicDiameter))

        scoresFile.close()

# Functions definition

def computeCoefficientsRegistration(positionLandmarkA, positionRegistredLandmarkA, positionLandmarkB, positionRegistredLandmarkB):

    a = (positionRegistredLandmarkB - positionRegistredLandmarkA) / (positionLandmarkB - positionLandmarkA)
    b = ((positionRegistredLandmarkA + positionRegistredLandmarkB) - a * (positionLandmarkA + positionLandmarkB)) / 2.0

    return [a, b]