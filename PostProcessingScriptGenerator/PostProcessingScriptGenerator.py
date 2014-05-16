# General imports

import sys
import os
import shutil
import stat

# Paths definition

sys.path.insert(0, './Dependencies/')

# Functions imports

import fctOthers

# Main

os.system('clear')

print("--------------------------------------------------------------------------------")
print("----------------------- Post Processing Script Generator -----------------------")
print("--------------------------------------------------------------------------------")

# Test arguments

if len(sys.argv) < 6:

    print("Error: Not enough arguments")
    print("--------------------------------------------------------------------------------")
    print("Argument 1: Path to inputs directory. This directory contains one directory per scan to process.")
    print("Argument 2: Path (reduced) file inputs. Each line should have the name of a directory containing the input files.")
    print("Argument 3: Path to desired main shell file that runs all the processing.")
    print("Argument 4: Path to Matlab executable.")
    print("Argument 5: Path to AirwayProcessing code directory.")
    print("--------------------------------------------------------------------------------")
    quit()

else:

    inputsDirectoryPath = sys.argv[1]
    inputsFilePath = sys.argv[2]
    mainScriptFilePath = sys.argv[3]
    matlabExecPath = sys.argv[4]
    codeDirectoryPath = sys.argv[5]

    print("Path to inputs directory: {0}".format(inputsDirectoryPath))
    print("Path (reduced) file inputs: {0}".format(inputsFilePath))
    print("Path to main script file: {0}".format(mainScriptFilePath))
    print("Path to Matlab executable: {0}".format(matlabExecPath))
    print("Path to code directory: {0}".format(codeDirectoryPath))


# Create the inputs list

print("--------------------------------------------------------------------------------")
print("Processing:")
print("--------------------------------------------------------------------------------")

inputsList = fctOthers.createListFromListFile(inputsFilePath)

# Paths definition

centerLineExec = codeDirectoryPath + "centerline"
crossSectionExec = codeDirectoryPath + "crossSections/bin/computeAreaAndContourWithMeanNorm"
displayExec = codeDirectoryPath + "display"

# Permissions for scripts

scriptPermissions = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH

# Algorithm

mainScriptFile = open(mainScriptFilePath, 'w')

for inputTemp in inputsList:

    inputDirectoryPath = inputsDirectoryPath + inputTemp + "/"
    postProcessingDirectoryPath = inputDirectoryPath + "PostProcessing/"
    scriptFilePath = postProcessingDirectoryPath + "postProcessing.sh"

    if os.path.exists(postProcessingDirectoryPath):
        shutil.rmtree(postProcessingDirectoryPath)
    os.mkdir(postProcessingDirectoryPath)

    mainScriptFile.write(scriptFilePath + "\n")

    print("Case number: {0}".format(inputTemp))
    print("Input directory: {0}".format(inputDirectoryPath))
    print("Post processing directory: {0}".format(postProcessingDirectoryPath))
    print("Script generated: {0}".format(scriptFilePath))
    print("................................................................................")

    outputNRRDFilePath = inputDirectoryPath + inputTemp + "_OUTPUT.nrrd"
    outputVTKFilePath = inputDirectoryPath + inputTemp + "_OUTPUT.vtk"
    landmarksFilePath = inputDirectoryPath + inputTemp + "_LANDMARKS.txt"
    clippingsFilePath = inputDirectoryPath + inputTemp + "_CLIPPINGS.txt"

    scriptFile = open(scriptFilePath, 'w')

    # Center line

    clISDirectoryPath = postProcessingDirectoryPath + "IsoSurface" + inputTemp + "/"

    scriptFile.write("# Center line\n\n")

    scriptFile.write("rm -r {0}\n".format(clISDirectoryPath))
    scriptFile.write("mkdir {0}\n\n".format(clISDirectoryPath))

    scriptFile.write("{0} -wait -nodesktop -nosplash -nodisplay -r ".format(matlabExecPath))
    scriptFile.write("\"cd {0}; ".format(centerLineExec))
    scriptFile.write("generateCenterlineOfAirway(\'{0}\', \'{1}\', \'{2}\', {3}, \'{4}\', \'{5}\'); ".format(inputTemp, outputNRRDFilePath, clISDirectoryPath, 100, landmarksFilePath, clippingsFilePath))
    scriptFile.write("quit;\"\n\n")

    # Cross section

    csCDirectoryPath = postProcessingDirectoryPath + "Contour" + inputTemp + "/"
    csMANFilePath = clISDirectoryPath + inputTemp + "_MeanAndNormal.txt"
    csAFilePath = csCDirectoryPath + inputTemp + "_Area.txt"
    csPFilePath = csCDirectoryPath + inputTemp + "_Perimeter.txt"
    csCDirectoryPath2 = csCDirectoryPath + "contour/"

    scriptFile.write("# Cross section\n\n")

    scriptFile.write("rm -r {0}\n".format(csCDirectoryPath))
    scriptFile.write("mkdir {0}\n\n".format(csCDirectoryPath))

    scriptFile.write("{0} ".format(crossSectionExec))
    scriptFile.write("{0} ".format(outputVTKFilePath))
    scriptFile.write("{0} ".format(csMANFilePath))
    scriptFile.write("{0} ".format(clippingsFilePath))
    scriptFile.write("{0} ".format(csAFilePath))
    scriptFile.write("{0} ".format(csPFilePath))
    scriptFile.write("{0} \n\n".format(csCDirectoryPath2[:-1]))

    # Display

    dCDirectoryPath = postProcessingDirectoryPath + "Curves" + inputTemp + "/"
    dCCCDirectoryPath = dCDirectoryPath + "contour" + inputTemp + "_contours/"
    dNRCFilePath = clISDirectoryPath + inputTemp + "_NormReliableCheck.txt"
    dCDirectoryPath2 = dCDirectoryPath + "contour" + inputTemp + "/"
    dAEFilePath = dCDirectoryPath + inputTemp + "_AreaEllipse.txt"

    scriptFile.write("# Display\n\n")

    scriptFile.write("rm -r {0}\n".format(dCDirectoryPath))
    scriptFile.write("mkdir {0}\n\n".format(dCDirectoryPath))
    scriptFile.write("mkdir {0}\n\n".format(dCCCDirectoryPath))

    scriptFile.write("{0} -wait -nodesktop -nosplash -nodisplay -r ".format(matlabExecPath))
    scriptFile.write("\"cd {0}; ".format(displayExec))
    scriptFile.write("drawContourOfAirway(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\'); ".format(csMANFilePath, dNRCFilePath, csCDirectoryPath2[:-1], dCDirectoryPath2[:-1], dAEFilePath, landmarksFilePath))
    scriptFile.write("quit;\"\n\n")

    # Finish

    fLIOCFilePath = clISDirectoryPath + inputTemp + "_LandmarksIdOnCenterline.txt"
    fCALFilePath = dCDirectoryPath + inputTemp + "_CurveAndLandmarks.png"

    scriptFile.write("# Finish\n\n")

    scriptFile.write("{0} -wait -nodesktop -nosplash -nodisplay -r ".format(matlabExecPath))
    scriptFile.write("\"cd {0}; ".format(displayExec))
    scriptFile.write("drawLandmarksOnOneCurve(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\'); ".format(csMANFilePath, csAFilePath, csPFilePath, dAEFilePath, fLIOCFilePath, fCALFilePath, dCDirectoryPath))
    scriptFile.write("quit;\"\n\n")

    scriptFile.close()
    os.chmod(scriptFilePath, scriptPermissions)

# Quit

mainScriptFile.close()
os.chmod(mainScriptFilePath, scriptPermissions)

quit()
