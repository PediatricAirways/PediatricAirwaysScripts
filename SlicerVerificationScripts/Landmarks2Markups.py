# This script converts a landmarks file in the format
#
# Landmark name 1 : <x> <y> <z>
# Landmark name 2 : <x> <y> <z>
#
# to a Slicer markups fiducial (.fcsv) file.

import string
import sys

##########################################################
def Landmarks2Markups(inputFile, outputFile):
  with open(inputFile, 'r') as f:
    read_data = f.read()

  tokens = read_data.splitlines()

  # Start writing landmarks file in Slicer format
  markupsFile = open(outputFile, 'w')
  markupsHeader = """# Markups fiducial file version = 4.3
# CoordinateSystem = 0
# columns = id,x,y,z,ow,ox,oy,oz,vis,sel,lock,label,desc,associatedNodeID"""
  markupsFile.write(markupsHeader)
  markupsFile.write('\n')

  # Fiducial node counter
  nodeCounter = 0
  for t in tokens:
    # Split by : token
    namePosition = t.split(':')
    if (len(namePosition) >= 2):
      name = string.strip(namePosition[0])
      xyz = string.strip(namePosition[1]).split() 
      #print name, xyz[0], xyz[1], xyz[2]
      if (len(xyz) >= 3):
        markupsFile.write('vtkMRMLMarkupsFiducialNode_%d,%s,%s,%s,0,0,0,1,1,1,0,%s,,vtkMRMLScalarVolumeNode2\n' % (nodeCounter, xyz[0], xyz[1], xyz[2], name))
        nodeCounter = nodeCounter + 1

  markupsFile.close()

##########################################################
if __name__ == "__main__":
  if (len(sys.argv) < 3):
    print "Usage:", sys.argv[0], "<landmarks file> <output FCSV file>"
    sys.exit(-1)

  # Parse the scan number from the landmarks file
  scanID = string.split(sys.argv[1], '_')
  print "scanID:", scanID
  
  inputFile = sys.argv[1]
  outputFile = sys.argv[2]

  Landmarks2Markups(inputFile, outputFile)