# General imports



# Function definition

def displayList(list):
    for i in range(len(list)):
        print(list[i])


def createListFromListFile(inputsFilePath):
    inputsFile = open(inputsFilePath)
    inputsList = []

    for lineTemp in inputsFile:
        inputsList.append(lineTemp)

    inputsFile.close()

    inputsList = map(lambda s: s.strip(), inputsList)         #clean the \n
    inputsList = map(lambda s: s.split( ' ' )[0], inputsList) #take only first item
    inputsList = filter(lambda s : s[0] != '#', inputsList)   #skip comments

    return inputsList
