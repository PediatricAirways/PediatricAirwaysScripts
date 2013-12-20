# General import

import sys
import os

# Paths definition

sys.path.insert(0, './Dependencies/')

# Classes import

from clsGeometry import geometry

# Functions import

import fctOthers

# Main

os.system('clear')

print("--------------------------------------------------------------------------------")
print("------------------------------ Numbers Generator -------------------------------")
print("--------------------------------------------------------------------------------")

# Test arguments

if len(sys.argv) < 3:

    print("Error: Not enough arguments")
    print("--------------------------------------------------------------------------------")
    print("Argument 1: Path to inputs directory")
    print("Argument 2: Path to (reduced) inputs list file")
    print("--------------------------------------------------------------------------------")
    quit()

else:

    inputsDirectoryPath = sys.argv[1]
    inputsFilePath = sys.argv[2]

    print("Path to inputs directory: {0}".format(inputsDirectoryPath))
    print("Input case: {0}".format(inputsFilePath))

# Algorithm

print("--------------------------------------------------------------------------------")
print("Processing:")
print("--------------------------------------------------------------------------------")

inputsList = fctOthers.createListFromListFile(inputsFilePath)

for inputTemp in inputsList:

    # Get the post-processing files

    inputDirectoryPath = inputsDirectoryPath + inputTemp + "/"
    postProcessingDirectoryPath = inputDirectoryPath + "PostProcessing/"

    coordinatesFilePath = postProcessingDirectoryPath + "IsoSurface" + inputTemp + "/" + inputTemp + "_MeanAndNormal.txt"
    landmarksIdFilePath = postProcessingDirectoryPath + "IsoSurface" + inputTemp + "/" + inputTemp + "_LandmarksIdOnCenterline.txt"
    areaFilePath = postProcessingDirectoryPath + "Contour" + inputTemp + "/" + inputTemp + "_Area.txt"
    perimeterFilePath = postProcessingDirectoryPath + "Contour" + inputTemp + "/" + inputTemp + "_Perimeter.txt"

    print("Coordinates: {0}".format(coordinatesFilePath))
    print("Landmarks ID: {0}".format(landmarksIdFilePath))
    print("Area: {0}".format(areaFilePath))
    print("Perimeter: {0}".format(perimeterFilePath))

    print("................................................................................")

    measurementsFilePath = inputDirectoryPath + inputTemp + "_MEASUREMENTS.txt"
    extraMeasurementsFilePath = inputDirectoryPath + inputTemp + "_EXTRA_MEASUREMENTS.txt"
    geometryFilePath = inputDirectoryPath + inputTemp + "_GEOMETRY.txt"

    print("Measurements file generated: {0}".format(measurementsFilePath))
    print("Extra measurements file generated: {0}".format(extraMeasurementsFilePath))
    print("Geometry file generated: {0}".format(geometryFilePath))

    g = geometry()
    g.createGeometryFromFiles(coordinatesFilePath, perimeterFilePath, areaFilePath, landmarksIdFilePath)

    g.saveGeometry(geometryFilePath)
    g.saveMeasurements(measurementsFilePath)
    g.saveExtraMeasurements(extraMeasurementsFilePath)

    print("--------------------------------------------------------------------------------")