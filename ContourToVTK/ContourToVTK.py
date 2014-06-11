import sys

if len(sys.argv) < 3:
    print "Usage:", sys.argv[0], "<input contour file> <output VTK file>"
    quit()
else:
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

print "Processing file '{0}'".format(inputFileName)

points = []
with open(inputFileName, 'r') as contourFile:
    lines = contourFile.readlines()
    totalPoints = lines[0].split(' ')[0]
    for line in lines[1:]:
        tokens = line.split(' ')
        if (len(tokens) < 3):
            continue
        points.append((float(tokens[0]), float(tokens[1]), float(tokens[2])))
        print points[-1]

# Now write out ASCII legacy VTK file
with open(outputFileName, 'w') as vtkFile:
    vtkFile.write("# vtk DataFile Version 3.0\n")
    vtkFile.write("ContourToPoints.py output\n")
    vtkFile.write("ASCII\n")
    vtkFile.write("DATASET POLYDATA\n")
    vtkFile.write("POINTS {0} float\n".format(len(points)))
    for pt in points:
        vtkFile.write("{0} {1} {2}\n".format(pt[0], pt[1], pt[2]))
    vtkFile.write("POLYGONS {0} {1}\n".format(len(points), 2*len(points)))
    for (i, pt) in zip(range(len(points)), points):
        vtkFile.write("1 {0}\n".format(i))
