#!/bin/bash

# Variables

imageWidth="200"
imageHeight="200"

window="1500"
level="-300"

zoomRatio="4"

increment="1"

inputsDirectoryPath='/Users/felix/Projects/PediatricAirwaysScripts/LandmarksPDFGenerator/Data/'
inputsFilePath='/Users/felix/Projects/PediatricAirwaysScripts/LandmarksPDFGenerator/Data/inputsFile.txt'

# Clear

clear

# Create images

scriptFilePath='/Users/felix/Projects/PediatricAirwaysScripts/LandmarksPDFGenerator/Dependencies/scpImagesGenerator.py'
slicerExecPath='/Users/felix/Projects/Slicer-SuperBuild-Debug/Slicer-build/Slicer'

$slicerExecPath --disable-builtin-cli-modules --python-script $scriptFilePath $inputsDirectoryPath $inputsFilePath $imageWidth $imageHeight $window $level $zoomRatio $increment

# Create HTML and PDF documents

pythonExecPath='/usr/local/bin/python'
dependenciesDirectoryPath='/Users/felix/Projects/PediatricAirwaysScripts/LandmarksPDFGenerator/Dependencies/'
scriptFilePath='/Users/felix/Projects/PediatricAirwaysScripts/LandmarksPDFGenerator/Dependencies/scpDocumentsGenerator.py'

$pythonExecPath $scriptFilePath $dependenciesDirectoryPath $inputsDirectoryPath $inputsFilePath $window $level $zoomRatio $increment

# Clean the working directories

pythonExecPath='/usr/local/bin/python'
scriptFilePath='/Users/felix/Projects/PediatricAirwaysScripts/LandmarksPDFGenerator/Dependencies/scpCleaner.py'

$pythonExecPath $scriptFilePath $inputsDirectoryPath $inputsFilePath



