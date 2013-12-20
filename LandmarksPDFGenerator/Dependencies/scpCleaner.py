# General import

import sys
import shutil

# Classes import



# Functions import

import fctOthers

# Main

print("--------------------------------------------------------------------------------")
print("---------------------- Landmarks PDF Generator - Cleaner -----------------------")
print("--------------------------------------------------------------------------------")

# Test arguments

if len(sys.argv) < 2:

    print("Error: Not enough arguments")
    print("--------------------------------------------------------------------------------")
    print("Argument 1: Path to inputs directory")
    print("Argument 2: Path to file inputs")
    print("--------------------------------------------------------------------------------")
    quit()

else:

    inputsDirectoryPath = sys.argv[1]
    inputsFilePath = sys.argv[2]

    print("Path to inputs directory: {0}".format(inputsDirectoryPath))
    print("Path to file inputs: {0}".format(inputsFilePath))

# Algorithm

print("--------------------------------------------------------------------------------")
print("Processing:")
print("--------------------------------------------------------------------------------")

# Create the inputs list

inputsCases = fctOthers.createListFromListFile(inputsFilePath)

# Process the inputs list

for inputTemp in inputsCases:

    landmarksViewerDirectoryPath = inputsDirectoryPath + inputTemp + "/LandmarksViewer/"
    landmarksViewerFilePath = landmarksViewerDirectoryPath + "LandmarksViewer.pdf"

    print("Case number: {0}".format(inputTemp))
    print("LandmarksViewer: {0}".format(landmarksViewerFilePath))
    print("................................................................................")

    # Move file

    newFilePath = inputsDirectoryPath + inputTemp + "/" + inputTemp + "_LANDMARKS.pdf"
    shutil.copy(landmarksViewerFilePath, newFilePath)

    print("LandmarksViewer.pdf moved to {0}_LANDMARKS.pdf".format(inputTemp))

    # Remove working directory

    shutil.rmtree(landmarksViewerDirectoryPath)

    print("{0}removed".format(landmarksViewerDirectoryPath))

    print("--------------------------------------------------------------------------------")

# Quit

quit()