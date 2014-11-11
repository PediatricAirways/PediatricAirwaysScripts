# This script runs through the post-processing results of pediatric airway
# scans and generates planar cross sections and cross section outlines for
# a scan.
#
# Usage: vtkpython.exe CreateSlicerFiles.py template.mrml data_directory output_directory
# where template.mrml is a template Slicer file with the text XXXX where the
# scan ID should go, the data_directory is the directory where the scan data
# and post-processing results should go, and output_directory is where all the
# generated files should go.

# Creates Slicer MRML and FCSV files for pediatric airways data
from Landmarks2Markups import *
from FindReplaceInFile import *
from CreatePlanarCrossSections import *

import os
import sys

if (len(sys.argv) < 4):
  print "Usage:", sys.argv[0], "<reference mrml file> <input directory> <output directory>"
  sys.exit(-1)

referenceMRMLFile = sys.argv[1]
inputDirectory    = sys.argv[2]
outputDirectory   = sys.argv[3]

inputDirList = os.listdir(inputDirectory)

for inputDir in inputDirList:
  scanID = os.path.split(inputDir)[1]
  
  print 'Processing directory %s' % scanID

  # Convert landmarks
  landmarksFile = '%s\\%s\\%s_LANDMARKS.txt' % (inputDirectory, scanID, scanID)
  if os.path.isfile(landmarksFile):
    markupsFile = '%s\\%s_Landmarks.fcsv' % (outputDirectory, scanID)
    Landmarks2Markups(landmarksFile, markupsFile)
  else:
    print 'No file named "%s" found' % (landmarksFile, )
    continue

  # Convert contours into polygonal data
  files = glob.glob('%s\\%s\\PostProcessing\\Contour%s\\contour???.txt' % (inputDirectory, scanID, scanID))
  fileRoot = os.path.commonprefix(files)
  outputAreas = '%s\\%s_Areas.txt' % (outputDirectory, scanID)
  outputGeometryFile = '%s\\%s_CrossSections.vtp' % (outputDirectory, scanID)
  outputOutlineFile = '%s\\%s_CrossSectionOutlines.vtp' % (outputDirectory, scanID)
  CreateCrossSections(files, outputAreas, outputGeometryFile, outputOutlineFile)

  # Create MRML file from template
  mrmlFile = '%s\\%s.mrml' % (outputDirectory, scanID)
  FindReplaceInFile(referenceMRMLFile, 'XXXX', scanID, mrmlFile)