# General Imports

import sys
import os

# Paths definition

sys.path.insert(0, './Dependencies/')

# Functions import

import fctOthers

# Classes import

from clsDataBase import dataBase

# Main

os.system('clear')

print("--------------------------------------------------------------------------------")
print("------------------------------- Plots Generator --------------------------------")
print("--------------------------------------------------------------------------------")

# Test arguments

if len(sys.argv) < 6:

    print("Error: Not enough arguments")
    print("--------------------------------------------------------------------------------")
    print("Argument 1: Path to CRL inputs directory")
    print("Argument 2: Path to CRL (full) inputs list file")
    print("Argument 3: Path to SGS inputs directory")
    print("Argument 4: Path to SGS (full) inputs list file")
    print("Argument 5: Path to outputs directory")
    print("--------------------------------------------------------------------------------")
    quit()

else:

    inputsCRLDirectoryPath = sys.argv[1]
    inputsCRLFilePath = sys.argv[2]
    inputsSGSDirectoryPath = sys.argv[3]
    inputsSGSFilePath = sys.argv[4]
    outputsDirectoryPath = sys.argv[5]

    print("Path to CRL inputs directory: {0}".format(inputsCRLDirectoryPath))
    print("Path to CRL inputs list file: {0}".format(inputsCRLFilePath))
    print("Path to SGS inputs directory: {0}".format(inputsSGSDirectoryPath))
    print("Path to SGS inputs list file: {0}".format(inputsSGSFilePath))
    print("Path to outputs directory: {0}".format(outputsDirectoryPath))

# Algorithm

print("--------------------------------------------------------------------------------")
print("Creating database:")
print("--------------------------------------------------------------------------------")

# Create the database

dataBaseCRL = dataBase("DataBase CRL", "CRL ", inputsCRLDirectoryPath, inputsCRLFilePath)
dataBaseSGS = dataBase("DataBase SGS", "SGS ", inputsSGSDirectoryPath, inputsSGSFilePath)

dataBaseCRL.display()
dataBaseSGS.display()

print("--------------------------------------------------------------------------------")
print("Creating plots:")
print("--------------------------------------------------------------------------------")

# Create plots

CRLPatientsNumber = dataBaseCRL.getPatientsNumbers()
SGSPatientsNumber = dataBaseSGS.getPatientsNumbers()

titlePart = " (CRL, SGS) = ({0}, {1})".format(CRLPatientsNumber, SGSPatientsNumber)

## By Age

fctOthers.generatePlot("Perimeter by Age" + titlePart, "perimeter", "age", dataBaseCRL, dataBaseSGS, outputsDirectoryPath + "PerimeterByAge.png")
fctOthers.generatePlot("Area by Age" + titlePart, "area", "age", dataBaseCRL, dataBaseSGS, outputsDirectoryPath + "AreaByAge.png")
fctOthers.generatePlot("Hydraulic Diameter by Age" + titlePart, "hydraulicDiameter", "age", dataBaseCRL, dataBaseSGS,outputsDirectoryPath + "HydraulicDiameterByAge.png")

fctOthers.generatePlot2("Perimeter by Age" + titlePart, "perimeter", "age", dataBaseCRL, dataBaseSGS, outputsDirectoryPath + "Perimeter2ByAge.png")
fctOthers.generatePlot2("Area by Age" + titlePart, "area", "age", dataBaseCRL, dataBaseSGS, outputsDirectoryPath + "Area2ByAge.png")
fctOthers.generatePlot2("Hydraulic Diameter by Age" + titlePart, "hydraulicDiameter", "age", dataBaseCRL, dataBaseSGS,outputsDirectoryPath + "HydraulicDiameter2ByAge.png")

## By Weight

fctOthers.generatePlot("Perimeter by Weight" + titlePart, "perimeter", "weight", dataBaseCRL, dataBaseSGS, outputsDirectoryPath + "PerimeterByWeight.png")
fctOthers.generatePlot("Area by Weight" + titlePart, "area", "weight", dataBaseCRL, dataBaseSGS, outputsDirectoryPath + "AreaByWeight.png")
fctOthers.generatePlot("Hydraulic Diameter by Weight" + titlePart, "hydraulicDiameter", "weight", dataBaseCRL, dataBaseSGS, outputsDirectoryPath + "HydraulicDiameterByWeight.png")

fctOthers.generatePlot2("Perimeter by Weight" + titlePart, "perimeter", "weight", dataBaseCRL, dataBaseSGS, outputsDirectoryPath + "Perimeter2ByWeight.png")
fctOthers.generatePlot2("Area by Weight" + titlePart, "area", "weight", dataBaseCRL, dataBaseSGS, outputsDirectoryPath + "Area2ByWeight.png")
fctOthers.generatePlot2("Hydraulic Diameter by Weight" + titlePart, "hydraulicDiameter", "weight", dataBaseCRL, dataBaseSGS, outputsDirectoryPath + "HydraulicDiameter2ByWeight.png")