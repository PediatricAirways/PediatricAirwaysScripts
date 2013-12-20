# General imports

import sys
import os
import math

# Paths definition

sys.path.insert(0, './Dependencies/')

# Functions imports

import fctOthers

# Main

os.system('clear')

print("--------------------------------------------------------------------------------")
print("------------------------- Spreadsheet File Generator ---------------------------")
print("--------------------------------------------------------------------------------")

# Test arguments

if len(sys.argv) < 3:

    print("Error: Not enough arguments")
    print("--------------------------------------------------------------------------------")
    print("Argument 1: Path to inputs directory")
    print("Argument 2: Path to (reduced) list file")
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
    measurementsFilePath = inputDirectoryPath + inputTemp + "_MEASUREMENTS.txt"
    spreadsheetFilePath = inputDirectoryPath + inputTemp + "_SPREADSHEET.txt"

    print("Case: {0}".format(inputTemp))
    print("Measurements file: {0}".format(measurementsFilePath))
    print("Spreadsheet file: {0}".format(spreadsheetFilePath))

    print("................................................................................")

    measurementsFile = open(measurementsFilePath, 'r')
    measurementsList = measurementsFile.readlines()
    measurementsFile.close()

    spreadsheetContent = fctOthers.transformLine(measurementsList[0])
    spreadsheetContent += "\t\t"
    spreadsheetContent += fctOthers.transformLine(measurementsList[1])
    spreadsheetContent += "\t\t"
    spreadsheetContent += fctOthers.transformLine(measurementsList[2])
    spreadsheetContent += "\t\t"
    spreadsheetContent += fctOthers.transformLine(measurementsList[3])

    # Write spreadsheet file

    spreadsheetFile = open(spreadsheetFilePath, 'w')
    spreadsheetFile.write(spreadsheetContent)
    spreadsheetFile.close()

# Quit

quit()