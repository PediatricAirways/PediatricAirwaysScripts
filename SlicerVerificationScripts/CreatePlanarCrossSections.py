# Generates cross section polygons and cross section outlines.
import glob
import os
import sys
import string
import vtk

##########################################################
def CreatePlanarCrossSectionPolyDataFromFile(file):

  with open(file, 'r') as f:
    read_data = f.read()

  tokens = string.split(read_data)

  offset = 2
  
  planeAppender = vtk.vtkAppendPolyData()
  outlineAppender = vtk.vtkAppendPolyData()

  # Iterate over separate pieces in the file
  while True:
    if (offset >= len(tokens)):
      break
    pointsInPiece = int(tokens[offset])
    
    newPoints = vtk.vtkPoints()
    newPoints.SetNumberOfPoints(pointsInPiece)
    
    for ptId in xrange(pointsInPiece):
      x = float(tokens[ptId*3 + 0 + offset + 1])
      y = float(tokens[ptId*3 + 1 + offset + 1])
      z = float(tokens[ptId*3 + 2 + offset + 1])
      newPoints.SetPoint(ptId, x, y, z)
    
    offset = offset + 3*pointsInPiece + 1
    
    polygon = vtk.vtkPolyData()
    polygon.SetPoints(newPoints)
    polygon.Allocate(pointsInPiece)
    polygon.InsertNextCell(vtk.VTK_POLYGON, pointsInPiece, range(pointsInPiece))

    triFilter = vtk.vtkTriangleFilter()
    triFilter.SetInputData(polygon)
   
    planeAppender.AddInputConnection(triFilter.GetOutputPort())
    
    outline = vtk.vtkPolyData()
    outline.SetPoints(newPoints)
    outline.Allocate(pointsInPiece)
    outline.InsertNextCell(vtk.VTK_POLY_LINE, pointsInPiece, range(pointsInPiece))
    outlineAppender.AddInputData(outline)
    
  planeAppender.Update()
  outlineAppender.Update()

  return (planeAppender.GetOutput(), outlineAppender.GetOutput())

##########################################################
def CreateCrossSections(files, outputAreas, outputGeometryFile, outputOutlineFile):
  areaFile = open(outputAreas, 'w')

  planeAppender = vtk.vtkAppendPolyData()
  outlineAppender = vtk.vtkAppendPolyData()
  for idx in range(len(files)):
    print 'Processing contour %d' % idx
    file = files[idx]
    (plane, outline) = CreatePlanarCrossSectionPolyDataFromFile(file)
    areaFile.write(str(ComputePolyDataArea(plane)))
    areaFile.write('\n')
    planeAppender.AddInputData(plane)
    outlineAppender.AddInputData(outline)
    
  planeWriter = vtk.vtkXMLPolyDataWriter()
  planeWriter.SetFileName(outputGeometryFile)
  planeWriter.SetInputConnection(planeAppender.GetOutputPort())
  planeWriter.Update()
  
  outlineWriter = vtk.vtkXMLPolyDataWriter()
  outlineWriter.SetFileName(outputOutlineFile)
  outlineWriter.SetInputConnection(outlineAppender.GetOutputPort())
  outlineWriter.Update()

  areaFile.close()

##########################################################
def ComputePolyDataArea(polydata):
  totalArea = 0.0
  numPolys = polydata.GetNumberOfPolys()
  for id in range(numPolys):
    cell = polydata.GetCell(id)
    cellArea = cell.ComputeArea()
    totalArea = totalArea + cellArea

  return totalArea

##########################################################
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Usage: %s <contour file name pattern> <output areas file> <output geometry file> <output outline file>" % (sys.argv[0],)
    sys.exit(-1)

  files = glob.glob(sys.argv[1])
  fileRoot = os.path.commonprefix(files)
  outputAreas = sys.argv[2]
  outputGeometryFile = sys.argv[3]
  outputOutlineFile = sys.argv[4]
  CreateCrossSections(files, outputAreas, outputGeometryFile, outputOutlineFile)
