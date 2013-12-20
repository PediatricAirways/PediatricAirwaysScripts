# General import

import sys
import os

# Class definition

class imagesGenerator:

    # Constructor

    def __init__(self):
        self.layoutManager = slicer.app.layoutManager()

        self.redWidget = self.layoutManager.sliceWidget('Red')
        self.redView = self.redWidget.sliceView()
        self.nodeRedView = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed')
        self.compositeNodeRedView = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceCompositeNodeRed')
        self.centerZ = 0
        self.defaultFieldOfRedView = [0, 0, 0]

        self.yellowWidget = self.layoutManager.sliceWidget('Yellow')
        self.yellowView = self.yellowWidget.sliceView()
        self.nodeYellowView = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeYellow')
        self.compositeNodeYellowView = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceCompositeNodeYellow')
        self.centerX = 0
        self.defaultFieldOfYellowView = [0, 0, 0]

        self.greenWidget = self.layoutManager.sliceWidget('Green')
        self.greenView = self.greenWidget.sliceView()
        self.nodeGreenView = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeGreen')
        self.compositeNodeGreenView = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceCompositeNodeGreen')
        self.centerY = 0
        self.defaultFieldOfGreenView = [0, 0, 0]

        self.sliceLogic = self.redWidget.sliceLogic() #Same for all

        self.box = slicer.vtkMRMLAnnotationROINode()

        slicer.mrmlScene.AddNode(self.box)

    # Functions

    def setImagesDimensions(self, width, height):
        self.redWidget.setFixedSize(width, height)
        self.yellowWidget.setFixedSize(width, height)
        self.greenWidget.setFixedSize(width, height)

    def setSlicesIntersectionVisibility(self, visible):
        self.compositeNodeRedView.SetSliceIntersectionVisibility(visible)
        self.compositeNodeYellowView.SetSliceIntersectionVisibility(visible)
        self.compositeNodeGreenView.SetSliceIntersectionVisibility(visible)

    def setSlicesPosition(self, yellowPosition, greenPosition, redPosition):
        self.nodeRedView.SetSliceOffset(redPosition)
        self.nodeYellowView.SetSliceOffset(yellowPosition)
        self.nodeGreenView.SetSliceOffset(greenPosition)

    def setImage(self, filePath):

        slicer.util.loadVolume(filePath)

        self.centerZ = self.nodeRedView.GetSliceOffset()
        self.centerX = self.nodeYellowView.GetSliceOffset()
        self.centerY = self.nodeGreenView.GetSliceOffset()

        self.defaultFieldOfRedView = self.nodeRedView.GetFieldOfView()
        self.defaultFieldOfYellowView = self.nodeYellowView.GetFieldOfView()
        self.defaultFieldOfGreenView = self.nodeGreenView.GetFieldOfView()

    def setWindowAndLevel(self, window, level):
        self.sliceLogic.SetBackgroundWindowLevel(window, level)

    def initializeViews(self):

        self.nodeRedView.SetFieldOfView(self.defaultFieldOfRedView[0], self.defaultFieldOfRedView[1], self.defaultFieldOfRedView[2])
        self.nodeYellowView.SetFieldOfView(self.defaultFieldOfYellowView[0], self.defaultFieldOfYellowView[1], self.defaultFieldOfYellowView[2])
        self.nodeGreenView.SetFieldOfView(self.defaultFieldOfGreenView[0], self.defaultFieldOfGreenView[1], self.defaultFieldOfGreenView[2])

        self.nodeRedView.SetXYZOrigin(0, 0, 0)
        self.nodeYellowView.SetXYZOrigin(0, 0, 0)
        self.nodeGreenView.SetXYZOrigin(0, 0, 0)

    def magnifyViews(self,R, x, y, z):

        Dx = self.centerX - x
        Dy = self.centerY - y
        Dz = self.centerZ - z

        # Zoom

        self.nodeRedView.SetFieldOfView(self.defaultFieldOfRedView[0]/R, self.defaultFieldOfRedView[1]/R, self.defaultFieldOfRedView[2]/R)
        self.nodeYellowView.SetFieldOfView(self.defaultFieldOfYellowView[0]/R, self.defaultFieldOfYellowView[1]/R, self.defaultFieldOfYellowView[2]/R)
        self.nodeGreenView.SetFieldOfView(self.defaultFieldOfGreenView[0]/R, self.defaultFieldOfGreenView[1]/R, self.defaultFieldOfGreenView[2]/R)

        # View position

        self.nodeRedView.SetXYZOrigin(Dx, -Dy, 0)
        self.nodeYellowView.SetXYZOrigin(Dy, -Dz, 0)
        self.nodeGreenView.SetXYZOrigin(Dx, -Dz, 0)

    def saveScreenshots(self, directoryPath, name):
        self.saveScreeshot(directoryPath, name, 'red')
        self.saveScreeshot(directoryPath, name, 'yellow')
        self.saveScreeshot(directoryPath, name, 'green')

    def saveScreeshot(self, directoryPath, name, view):

        slicer.app.processEvents()

        windowToImageFilter = vtk.vtkWindowToImageFilter()
        pngWriter = vtk.vtkPNGWriter()

        if view == 'red':
            input = self.redView.renderWindow()
            filePath = directoryPath + name + 'Red.png'

        elif view == 'yellow':
            input = self.yellowView.renderWindow()
            filePath = directoryPath + name + 'Yellow.png'

        elif view == 'green':
            input = self.greenView.renderWindow()
            filePath = directoryPath + name + 'Green.png'

        windowToImageFilter.SetInput(input)
        windowToImageFilter.Update()
        pngWriter.SetFileName(filePath)
        pngWriter.SetInputConnection(windowToImageFilter.GetOutputPort())
        pngWriter.Write()

# Functions definition

def createListFromListFile(inputsFilePath):
    inputsFile = open(inputsFilePath)
    inputsList = []

    for line in inputsFile:
      inputsList.append(line)

    inputsFile.close()

    inputsList = map(lambda s: s.strip(), inputsList) #clean the \n

    return inputsList

# Main

print("--------------------------------------------------------------------------------")
print("------------------ Landmarks PDF Generator - Images Generator ------------------")
print("--------------------------------------------------------------------------------")

# Test arguments

if len(sys.argv) < 9:

    print("Error: Not enough arguments")
    print("--------------------------------------------------------------------------------")
    print("Argument 1: Path to inputs directory")
    print("Argument 2: Path to file inputs")
    print("Argument 3: Image width [px]")
    print("Argument 4: Image height [px]")
    print("Argument 5: Image level")
    print("Argument 6: Image window")
    print("Argument 7: Zoom ratio")
    print("Argument 8: Increment [mm]")
    print("--------------------------------------------------------------------------------")
    quit()
else:

    inputsDirectoryPath = sys.argv[1]
    inputsFilePath = sys.argv[2]
    imageWidth = float(sys.argv[3])
    imageHeight = float(sys.argv[4])
    window = float(sys.argv[5])
    level = float(sys.argv[6])
    zoomRatio = float(sys.argv[7])
    increment = float(sys.argv[8])

    print("Path to inputs directory: {0}".format(inputsDirectoryPath))
    print("Path to file inputs: {0}".format(inputsFilePath))
    print("Image width [px]: {0}".format(imageWidth))
    print("Image height [px]: {0}".format(imageHeight))
    print("Image level: {0}".format(window))
    print("Image window: {0}".format(level))
    print("Zoom ratio: {0}".format(zoomRatio))
    print("Increment [mm]: {0}".format(increment))

# Algorithm

#Initialization

iG = imagesGenerator()

iG.setImagesDimensions(imageWidth, imageHeight)

print("--------------------------------------------------------------------------------")
print("Processing:")
print("--------------------------------------------------------------------------------")

# Create the inputs list

inputsCases = createListFromListFile(inputsFilePath)

# Process the inputs list

for inputCase in inputsCases:

    imageFilePath = inputsDirectoryPath + inputCase + "/" + inputCase + "_INPUT.nrrd"
    landmarksFilePath = inputsDirectoryPath + inputCase + "/" + inputCase + "_LANDMARKS.txt"
    outputDirectoryPath = inputsDirectoryPath + inputCase + "/LandmarksViewer/"

    print("Case number: {0}".format(inputCase))
    print("Image: {0}".format(imageFilePath))
    print("Landmarks: {0}".format(landmarksFilePath))
    print("Outputs path: {0}".format(outputDirectoryPath))
    print("................................................................................")

    # Create the landmarks list

    rawLandmarks = []
    landmarks = []

    rawLandmarks = createListFromListFile(landmarksFilePath)

    for rawLandmark in rawLandmarks:
        parts = rawLandmark.split(' ')
        if len(parts) == 5:
            landmarks.append([parts[0], round(float(parts[2]), 3), round(float(parts[3]), 3), round(float(parts[4]), 3)])

    # Create the directory

    if not os.path.exists(outputDirectoryPath):
        os.makedirs(outputDirectoryPath)

    # Process the landmarks list

    iG.setImage(imageFilePath)
    iG.setWindowAndLevel(window, level)

    boxSize = min(iG.defaultFieldOfYellowView[0]/zoomRatio, iG.defaultFieldOfGreenView[0]/zoomRatio, iG.defaultFieldOfRedView[0]/zoomRatio)
    boxSize /= 2
    iG.box.SetRadiusXYZ([boxSize, boxSize, boxSize])

    for landmark in landmarks:

        iG.setSlicesPosition(landmark[1], landmark[2], landmark[3])

        iG.initializeViews()
        iG.setSlicesIntersectionVisibility(1)
        iG.box.SetXYZ([landmark[1], landmark[2], landmark[3]])
        iG.box.SetDisplayVisibility(1)

        # Normal views

        iG.saveScreenshots(outputDirectoryPath, landmark[0])
        print("{0} view generated for (x, y, z) = ({1}, {2}, {3})".format(landmark[0], landmark[1], landmark[2], landmark[3]))

        iG.magnifyViews(zoomRatio, landmark[1], landmark[2], landmark[3])

        # Zoomed views

        iG.box.SetDisplayVisibility(0)

        name = landmark[0] + str(zoomRatio) + "+0"
        iG.saveScreenshots(outputDirectoryPath, name)
        print("{0} view generated for (x, y, z) = ({1}, {2}, {3})".format(name, landmark[1], landmark[2], landmark[3]))

        iG.setSlicesIntersectionVisibility(0)

        iG.setSlicesPosition(landmark[1] - increment, landmark[2] - increment, landmark[3] - increment)
        name = landmark[0] + str(zoomRatio) + "-" + str(increment)
        iG.saveScreenshots(outputDirectoryPath, name)
        print("{0} view generated for (x, y, z) = ({1}, {2}, {3})".format(name, landmark[1], landmark[2], landmark[3]))

        iG.setSlicesPosition(landmark[1] + increment, landmark[2] + increment, landmark[3] + increment)
        name = landmark[0] + str(zoomRatio) + "+" + str(increment)
        iG.saveScreenshots(outputDirectoryPath, name)
        print("{0} view generated for (x, y, z) = ({1}, {2}, {3})".format(name, landmark[1], landmark[2], landmark[3]))


    print("--------------------------------------------------------------------------------")

# Quit slicer

slicer.util.quit()
