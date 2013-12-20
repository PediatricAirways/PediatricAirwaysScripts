# General import

import sys
import os
import warnings

# Paths definition

sys.path.insert(0, './Dependencies/')

# Classes import

from clsDataBase import dataBase
from clsAtlasesGenerator import atlasesGenerator
from clsAtlas import atlas

# Functions import

import fctOthers

# Main

os.system('clear')
warnings.simplefilter("ignore")

print("--------------------------------------------------------------------------------")
print("------------------------------- Atlas Generator --------------------------------")
print("--------------------------------------------------------------------------------")

# Test arguments

if len(sys.argv) < 7:

    print("Error: Not enough arguments")
    print("--------------------------------------------------------------------------------")
    print("Argument 1: Type of computation : 1 for AtlasScore, 2 for Age atlas, 3 for Weight atlas")
    print("Argument 2: Path to CRL inputs directory")
    print("Argument 3: Path to CRL (full) inputs list file")
    print("Argument 4: Path to SGS inputs directory")
    print("Argument 5: Path to SGS (full) inputs list file")
    print("Argument 6: Path to atlases directory")

    print("--------------------------------------------------------------------------------")
    quit()

else:

    typeOfComputation = int(sys.argv[1])
    inputsCRLDirectoryPath = sys.argv[2]
    inputsCRLFilePath = sys.argv[3]
    inputsSGSDirectoryPath = sys.argv[4]
    inputsSGSFilePath = sys.argv[5]
    atlasesDirectoryPath = sys.argv[6]

    print("Path to CRL inputs directory: {0}".format(inputsCRLDirectoryPath))
    print("Path to CRL inputs list file: {0}".format(inputsCRLFilePath))
    print("Path to SGS inputs directory: {0}".format(inputsSGSDirectoryPath))
    print("Path to SGS inputs list file: {0}".format(inputsSGSFilePath))
    print("Path to atlases directory: {0}".format(atlasesDirectoryPath))

# Algorithm

# Create the databases

print("--------------------------------------------------------------------------------")
print("Create databases")

dataBaseCRL = dataBase("DataBase CRL", "CRL")
dataBaseCRL.createDataBase(inputsCRLDirectoryPath, inputsCRLFilePath)

if typeOfComputation == 1:

    dataBaseSGS = dataBase("DataBase SGS", "SGS")
    dataBaseSGS.createDataBase(inputsSGSDirectoryPath, inputsSGSFilePath)

# Compute and save the registred geometries

print("--------------------------------------------------------------------------------")
print("Compute the registred geometries")

dataBaseCRL.computeMedianLandmarks()
dataBaseCRL.computeRegistredGeometries()
dataBaseCRL.computeInterpolations()
dataBaseCRL.saveRegistredGeometries()


if typeOfComputation == 1:

    dataBaseSGS.setMedianLandmarks(dataBaseCRL.getMedianLandmarks())
    dataBaseSGS.computeRegistredGeometries()
    dataBaseSGS.computeInterpolations()
    dataBaseSGS.saveRegistredGeometries()

# Plot the geometries

if typeOfComputation == 1:

    print("--------------------------------------------------------------------------------")
    print("Plot the registred geometries")

    dataBaseCRL.savePlots()
    dataBaseSGS.savePlots()

    print("--------------------------------------------------------------------------------")
    print("Save the ratio and (age) atlas score")

    dataBaseCRL.computeAtlases("both", dataBaseCRL)
    dataBaseCRL.computeMedianValues(dataBaseCRL)
    dataBaseCRL.saveScores()

    dataBaseSGS.computeAtlases("both", dataBaseCRL)
    dataBaseSGS.setMedianValues(dataBaseCRL.getMedianValues())
    dataBaseSGS.saveScores()

    print("--------------------------------------------------------------------------------")
    print("Plot the atlases comparison")

    dataBaseCRL.plotComparisons()
    dataBaseSGS.plotComparisons()

elif typeOfComputation == 2:

    print("--------------------------------------------------------------------------------")
    print("Create age atlas from the CRL database")

    # Create age atlas

    atlasesGeneratorAge = atlasesGenerator("age", dataBaseCRL, atlasesDirectoryPath)
    atlasesGeneratorAge.saveGeometries()
    atlasesGeneratorAge.plotGeometries()
    atlasesGeneratorAge.plotAtlases()
    atlasesGeneratorAge.plotSummaryAtlases()

elif typeOfComputation == 3:

    print("--------------------------------------------------------------------------------")
    print("Create weight atlas from the CRL database")

    # Create weight atlas

    atlasesGeneratorWeight = atlasesGenerator("weight", dataBaseCRL, atlasesDirectoryPath)
    atlasesGeneratorWeight.saveGeometries()
    atlasesGeneratorWeight.plotGeometries()
    atlasesGeneratorWeight.plotAtlases()
    atlasesGeneratorWeight.plotSummaryAtlases()

