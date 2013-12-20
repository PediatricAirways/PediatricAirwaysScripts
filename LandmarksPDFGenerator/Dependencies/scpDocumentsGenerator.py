# General import

import sys

# Classes import



# Functions import

import fctOthers

# Main

print("--------------------------------------------------------------------------------")
print("----------------- Landmarks PDF Generator - Document Generator -----------------")
print("--------------------------------------------------------------------------------")

# Test arguments

if len(sys.argv) < 8:

    print("Error: Not enough arguments")
    print("--------------------------------------------------------------------------------")
    print("Argument 1: Path to dependencies")
    print("Argument 2: Path to inputs directory")
    print("Argument 3: Path to (reduced) file inputs")
    print("Argument 4: Image level")
    print("Argument 5: Image window")
    print("Argument 6: Zoom ratio")
    print("Argument 7: Increment in mm")
    print("--------------------------------------------------------------------------------")
    quit()

else:

    dependenciesDirectoryPath = sys.argv[1]
    inputsDirectoryPath = sys.argv[2]
    inputsFilePath = sys.argv[3]
    window = float(sys.argv[4])
    level = float(sys.argv[5])
    zoomRatio = float(sys.argv[6])
    increment = float(sys.argv[7])

    print("Path to dependencies: {0}".format(dependenciesDirectoryPath))
    print("Path to inputs directory: {0}".format(inputsDirectoryPath))
    print("Path to file inputs: {0}".format(inputsFilePath))
    print("Image level: {0}".format(window))
    print("Image window: {0}".format(level))
    print("Zoom ratio: {0}".format(zoomRatio))
    print("Increment [mm]: {0}".format(increment))

# Algorithm

print("--------------------------------------------------------------------------------")
print("Processing:")
print("--------------------------------------------------------------------------------")

# Create the mapping array for names

mappingArray = []

mappingArray.append(["Columella",  "Columella"])
mappingArray.append(["LeftAlaRim", "Left Ala Rim"])
mappingArray.append(["NasalSpine", "Nasal Spine"])
mappingArray.append(["NoseTip", "Nose Tip"])
mappingArray.append(["PosteriorInferiorVomerCorner", "Choana"])
mappingArray.append(["PyrinaAperture", "Pyrina Aperture"])
mappingArray.append(["RightAlaRim", "Right Ala Rim"])
mappingArray.append(["Subglottic", "Subglottis"])
mappingArray.append(["TracheaCarina", "Trachea Carina"])
mappingArray.append(["TVC", "True Vocal Cord"])
mappingArray.append(["EpiglottisTip", "Tip of Epiglottis"])
mappingArray.append(["TongueBase", "Base of Tongue"])

# Create the inputs list

inputsCases = fctOthers.createListFromListFile(inputsFilePath)

# Process the inputs list

for inputTemp in inputsCases:

    imageFilePath = inputsDirectoryPath + inputTemp + "/" + inputTemp + "_INPUT.nrrd"
    landmarksFilePath = inputsDirectoryPath + inputTemp + "/" + inputTemp + "_LANDMARKS.txt"
    outputDirectoryPath = inputsDirectoryPath + inputTemp + "/LandmarksViewer/"

    print("Case number: {0}".format(inputTemp))
    print("Image: {0}".format(imageFilePath))
    print("Landmarks: {0}".format(landmarksFilePath))
    print("Outputs path: {0}".format(outputDirectoryPath))
    print("................................................................................")

    # Create the landmarks list

    rawLandmarks = []
    landmarks = []

    rawLandmarks = fctOthers.createListFromListFile(landmarksFilePath)

    for rawLandmark in rawLandmarks:
        parts = rawLandmark.split(' ')
        if len(parts) == 5:
            landmarks.append([parts[0], round(float(parts[2]), 3), round(float(parts[3]), 3), round(float(parts[4]), 3)])

    # Create the HTML file

    htmfFilePath = fctOthers.generateHTML(dependenciesDirectoryPath, inputsDirectoryPath, inputTemp, landmarks, level, window, zoomRatio, increment, mappingArray)

    print("LandmarksViewer.html file generated")

    # Create the PDF file

    pdfFilePath = htmfFilePath[:-4] + "pdf"

    fctOthers.generatePDF(htmfFilePath, pdfFilePath)

    print("LandmarksViewer.pdf file generated")

    print("--------------------------------------------------------------------------------")

# Quit

quit()