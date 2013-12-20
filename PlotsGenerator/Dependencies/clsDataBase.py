# General imports



# Class imports

from clsCase import case

# Function import



# Class definition

class dataBase:

    # Constructors

    def __init__(self, name, type, inputsDirectoryPath, inputsFilePath):

        self.name = name
        self.type = type
        self.cases = []

        self.createDataBase(type, inputsDirectoryPath, inputsFilePath)

    def createDataBase(self, type, inputsDirectoryPath, inputsFilePath):

        inputsFile = open(inputsFilePath)

        for lineTemp in inputsFile:

            lineTemp = lineTemp.rstrip('\n')
            parts = lineTemp.split(" ")

            nameTemp = parts[0]
            typeTemp = type
            genderTemp = parts[2]
            ageTemp = round(float(parts[3]), 0)
            weightTemp = round(float(parts[4]), 1)
            airwayClassTemp = parts[5]
            surgeryTemp = bool(int(parts[6]))
            measurementsFilePathTemp = inputsDirectoryPath + nameTemp + "/" + nameTemp + "_MEASUREMENTS.txt"
            scoresFilePathTemp = inputsDirectoryPath + nameTemp + "/" + nameTemp + "_SCORES.txt"

            caseTemp = case(nameTemp, typeTemp, genderTemp, ageTemp, weightTemp, airwayClassTemp, surgeryTemp, measurementsFilePathTemp, scoresFilePathTemp)

            self.cases.append(caseTemp)

    # Getters

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getCases(self):
        return self.cases

    # Others

    def getPatientsNumbers(self):
        return len(self.cases)

    def display(self):

        print("{0} : {1}".format(self.getName(), self.getType()))

        print("--------------------------------------------------------------------------------")

        for case in self.cases:
            case.display()
            print("--------------------------------------------------------------------------------")