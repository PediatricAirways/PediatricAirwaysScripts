# General imports



# Class imports

from clsLandmarkParameters import landmarkParameters

# Function import



# Class definition

class case:

    # Constructors

    def __init__(self, number, type, gender, age, weight, airwayClass, surgery, measurementsFilePath, scoresFilePath):

        self.number = number #CT scan number
        self.type = type #CRL or SGS
        self.gender = gender
        self.age = age
        self.weight = weight
        self.airwayClass = airwayClass #Class of the CT scan
        self.surgery = surgery
        self.landmarksParameters = []

        self.createLandmarks(measurementsFilePath, scoresFilePath)

    def createLandmarks(self, measurementsFilePath, scoresFilePath):

        nbDecimals = 5

        # Measurements

        measurementsFile = open(measurementsFilePath)

        for lineTemp in measurementsFile:

            lineTemp = lineTemp.rstrip('\n')
            parts = lineTemp.split(" ")

            nameTemp = parts[0]
            perimeterTemp = round(float(parts[2]), nbDecimals)
            areaTemp = round(float(parts[3]), nbDecimals)
            hydraulicDiameterTemp = round(float(parts[4]), nbDecimals)

            landmarkParametersTemp = landmarkParameters(nameTemp, perimeterTemp, areaTemp, hydraulicDiameterTemp)

            self.landmarksParameters.append(landmarkParametersTemp)

        measurementsFile.close()

        # Scores

        scoresFile = open(scoresFilePath)

        for line in scoresFile:

            line = line.rstrip('\n')
            parts = line.split(" ")

            nameTemp = parts[0]
            perimeterTemp = round(float(parts[2]), nbDecimals)
            areaTemp = round(float(parts[3]), nbDecimals)
            hydraulicDiameterTemp = round(float(parts[4]), nbDecimals)

            landmarkParametersTemp = landmarkParameters(nameTemp, perimeterTemp, areaTemp, hydraulicDiameterTemp)

            self.landmarksParameters.append(landmarkParametersTemp)

        scoresFile.close()

    # Getters

    def getNumber(self):
        return self.number

    def getType(self):
        return self.type

    def getGender(self):
        return self.gender

    def getAge(self):
        return self.age

    def getWeight(self):
        return self.weight

    def getAirwayClasses(self):
        return self.airwayClass

    def getSurgery(self):
        return self.surgery

    def getLandmarksParameters(self):
        return self.landmarksParameters

    # Others

    def display(self):

        print("Number : {0}".format(self.getNumber()))
        print("Type : {0}".format(self.getType()))
        print("Gender : {0}".format(self.getGender()))
        print("Age : {0}".format(self.getAge()))
        print("Weight : {0}".format(self.getWeight()))
        print("Airway class : {0}".format(self.getAirwayClasses()))
        print("Surgery class : {0}".format(self.getSurgery()))

        print("................................................................................")

        for landmarkParameter in self.landmarksParameters:
            landmarkParameter.display()