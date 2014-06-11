import sys
import csv
import math
import os
from os import listdir
from os.path import isdir, isfile, join
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

if len(sys.argv) < 4:
    print "Usage:", sys.argv[0], "<input directory> <subject CSV> <output CSV file>"
    quit()
else:
    inputDirectory = sys.argv[1]
    subjectCSV     = sys.argv[2]
    outputCSVFile  = sys.argv[3]

print("Processing directory '{0}'".format(inputDirectory))

# Load the subject CSV file
ID2ages = {}
with open(subjectCSV, 'rb') as subjectFile:
    csvreader = csv.reader(subjectFile)
    for row in csvreader:
        try:
            ID2ages[row[0]] = row[1]
        except:
            pass

# Create list of all directories in the input directory
directories = [ d for d in listdir(inputDirectory) if isdir(join(inputDirectory, d))]
directories.sort()

age = []
maxRadii = []
closestLandmarkHistogram = {}


outputFile = open(outputCSVFile, 'w')
outputFile.write('"ID","Age","Cross-sectional Area"\n')
for ID in directories:
    postProcessingFileName = join(inputDirectory, ID, "PostProcessing", "IsoSurface" + ID,
                                  ID + "_LandmarksIdOnCenterline.txt")

    if (not isfile(postProcessingFileName)):
        continue

    print "Processing file:", postProcessingFileName

    # Read in the landmark ID file. We really need the third line.
    f = open(postProcessingFileName)
    lines = f.readlines()
    f.close()

    landmarkIndices = {}
    landmarkIndices["NasalSpine"]                   = int(lines[1])
    landmarkIndices["PosteriorInferiorVomerCorner"] = int(lines[2])
    landmarkIndices["EpiglottisTip"]                = int(lines[3])
    landmarkIndices["TVC"]                          = int(lines[4])
    landmarkIndices["Subglottic"]                   = int(lines[5])
    landmarkIndices["TracheaCarina"]                = int(lines[6])

    # Now open up the cross-sectional area measurement
    xaFile = join(inputDirectory, ID, "PostProcessing", "Contour" + ID,
                  ID + "_Area.txt")
    f = open(xaFile)
    lines = f.readlines()
    f.close()
    xa = map(float, lines[landmarkIndices["PosteriorInferiorVomerCorner"]:-1])

    # Find maximum
    maxXA = max(xa)
    maxXAIndex = xa.index(maxXA) + landmarkIndices["PosteriorInferiorVomerCorner"]

    distanceToLandmarks = map(lambda key: (key, math.fabs(maxXAIndex - landmarkIndices[key])), landmarkIndices.keys())
    distanceToLandmarks.sort(key=lambda x: x[1])
    closestLandmark = distanceToLandmarks[0][0]
    try:
        closestLandmarkHistogram[closestLandmark] = closestLandmarkHistogram[closestLandmark] + 1
    except:
        closestLandmarkHistogram[closestLandmark] = 1

    try:
        outputFile.write(ID + ",{0},{1}\n".format(ID2ages[ID],maxXA))
        age.append(ID2ages[ID])
        maxRadii.append(math.sqrt(maxXA/math.pi))
    except:
        # Skip
        pass

outputFile.close()

fig = Figure()
canvas = FigureCanvas(fig)
axes = fig.add_subplot(111)

xLabel = "Age"
yLabel = "Maximum Radius Below Choanae"
axes.set_xlabel(xLabel + " (months)")
axes.set_ylabel(yLabel + " (mm)")

title = '{0} vs. {1}'.format(yLabel, xLabel)
axes.set_title(title)

axes.plot(age, maxRadii, 'b.', markersize=10)

fig.savefig('MaxRadiusVsAge.png')

for key in closestLandmarkHistogram:
    print "Count of max airway closest to {0}: {1}".format(key, closestLandmarkHistogram[key])
