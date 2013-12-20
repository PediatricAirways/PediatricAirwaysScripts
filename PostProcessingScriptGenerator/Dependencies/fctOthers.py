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