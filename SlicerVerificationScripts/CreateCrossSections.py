import glob
import os
import sys
import string
import vtk

##########################################################
def CreateCrossSectionPolyDataFromFile(file):
  
  with open(file, 'r') as f:
    read_data = f.read()

  tokens = string.split(read_data)

  numPts = int(tokens[0])
  numCells = int(tokens[1])

  print numPts, numCells

  newPoints = vtk.vtkPoints()
  newPoints.SetNumberOfPoints(numPts)

  offset = 2
  for ptId in xrange(numPts):
    x = float(tokens[ptId*3 + 0 + offset])
    y = float(tokens[ptId*3 + 1 + offset])
    z = float(tokens[ptId*3 + 2 + offset])
    newPoints.SetPoint(ptId, x, y, z)

  output = vtk.vtkPolyData()
  output.SetPoints(newPoints)
  output.Allocate(3*numCells)

  offset = 2 + 3*numPts
  triangle = vtk.vtkTriangle()
  pointIds = triangle.GetPointIds()
  pointIds.SetNumberOfIds(3)
  for cellId in xrange(numCells):
    for i in xrange(3):
      pointIds.SetId(i, int(tokens[cellId*3 + i + offset]))
    
    output.InsertNextCell(triangle.GetCellType(), pointIds)
    
  return output

##########################################################
def CreateCrossSections(files, outputAreas, outputGeometryFile):
  areaFile = open(outputAreas, 'w')

  appender = vtk.vtkAppendPolyData()
  mp = vtk.vtkMassProperties()
  for idx in range(len(files)):
    file = files[idx]
    polydata = CreateCrossSectionPolyDataFromFile(file)
    mp.SetInputData(polydata)
    mp.Update()
    areaFile.write(str(mp.GetSurfaceArea()))
    areaFile.write('\n')
    appender.AddInputData(polydata)
    
  writer = vtk.vtkXMLPolyDataWriter()
  writer.SetFileName(outputGeometryFile)
  writer.SetInputConnection(appender.GetOutputPort())
  writer.Update()

  areaFile.close()

##########################################################
if __name__ == "__main__":
  if len(sys.argv) < 4:
    print "Usage: %s <contour file name pattern> <output areas file> <output geometry file>" % (sys.argv[0],)
    sys.exit(-1)

  files = glob.glob(sys.argv[1])
  fileRoot = os.path.commonprefix(files)
  outputAreas = sys.argv[2]
  outputGeometryFile = sys.argv[3]
  CreateCrossSections(files, outputAreas, outputGeometryFile)