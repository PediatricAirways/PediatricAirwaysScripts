# General imports

import datetime
from weasyprint import HTML

# Functions definition

def createListFromListFile(inputsFilePath):
    inputsFile = open(inputsFilePath)
    inputsList = []

    for lineTemp in inputsFile:
        inputsList.append(lineTemp)

    inputsFile.close()

    inputsList = map(lambda s: s.strip(), inputsList) #clean the \n

    return inputsList

def generateHTML(dependenciesDirectoryPath, inputsDirectoryPath, inputCase, landmarks, level, window, zoomRatio, increment, mappingArray):

    # Open HTML and CSS files

    htmlFilePath = inputsDirectoryPath + inputCase + "/LandmarksViewer/" + "LandmarksViewer.html"
    htmlFile = open(htmlFilePath, 'w')

    cssFile = open(dependenciesDirectoryPath + 'style.css', 'r')
    cssContent = cssFile.read()

    htmlPart1File = open(dependenciesDirectoryPath + 'part1.html', 'r')
    htmlPart2File = open(dependenciesDirectoryPath + 'part2.html', 'r')
    htmlPart3File = open(dependenciesDirectoryPath + 'part3.html', 'r')
    htmlPart4File = open(dependenciesDirectoryPath + 'part4.html', 'r')
    htmlPart5File = open(dependenciesDirectoryPath + 'part5.html', 'r')
    htmlPart6File = open(dependenciesDirectoryPath + 'part6.html', 'r')
    htmlPart7File = open(dependenciesDirectoryPath + 'part7.html', 'r')
    htmlPart8File = open(dependenciesDirectoryPath + 'part8.html', 'r')
    htmlPart1Content = htmlPart1File.read()
    htmlPart2Content = htmlPart2File.read()
    htmlPart3Content = htmlPart3File.read()
    htmlPart4Content = htmlPart4File.read()
    htmlPart5Content = htmlPart5File.read()
    htmlPart6Content = htmlPart6File.read()
    htmlPart7Content = htmlPart7File.read()
    htmlPart8Content = htmlPart8File.read()

    # Write

    currentDate = datetime.datetime.now()

    htmlFile.write(htmlPart1Content.format(inputCase, currentDate.day, currentDate.month, currentDate.year, window, level, zoomRatio, increment, cssContent))

    for landmarkTemp in landmarks:
        htmlFile.write(htmlPart2Content.format(getMappedValue(landmarkTemp[0], mappingArray), landmarkTemp[1], landmarkTemp[2], landmarkTemp[3]))

    htmlFile.write(htmlPart3Content)

    for landmarkTemp in landmarks:

        htmlFile.write(htmlPart4Content)

        htmlFile.write(htmlPart5Content.format(getMappedValue(landmarkTemp[0], mappingArray)))

        name = landmarkTemp[0]
        htmlFile.write(htmlPart6Content.format("", name))

        name = landmarkTemp[0] + str(zoomRatio) + "-" + str(increment)
        htmlFile.write(htmlPart6Content.format("-" + str(increment) + " mm", name))

        name = landmarkTemp[0] + str(zoomRatio) + "+0"
        htmlFile.write(htmlPart6Content.format("", name))

        name = landmarkTemp[0] + str(zoomRatio) + "+" + str(increment)
        htmlFile.write(htmlPart6Content.format("+" + str(increment) + " mm", name))

        htmlFile.write(htmlPart7Content)

    htmlFile.write(htmlPart8Content)

    # Close file

    htmlFile.close()

    # Return

    return htmlFilePath

def generatePDF(htmfFilePath, pdfFilePath):
    HTML(htmfFilePath).write_pdf(pdfFilePath)

def getMappedValue(value, mappingArray):

    for i in range(len(mappingArray)):
        if mappingArray[i][0] == value:
            return mappingArray[i][1]

    return value