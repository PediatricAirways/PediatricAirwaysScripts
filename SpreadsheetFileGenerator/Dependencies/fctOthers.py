# General imports

# Functions definition

def createListFromListFile(inputsFilePath):
    inputsFile = open(inputsFilePath)
    inputsList = []

    for lineTemp in inputsFile:
        inputsList.append(lineTemp)

    inputsFile.close()

    inputsList = map(lambda s: s.strip(), inputsList) #clean the \n

    return inputsList

def transformLine(line):

    parts = line.split(" ")
    parts = map(lambda s: s.strip(), parts) #clean the \n

    string = parts[2] + "\t" + parts[3] + "\t" + parts[4]

    return string