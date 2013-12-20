# General imports



# Class imports

import fctOthers

# Function import



# Class definition

class serie:

    # Constructors

    def __init__(self, name, quantity, abscissa, landmark, type, gender, surgery, dataBaseCRL, dataBaseSGS):

        self.name = name
        self.quantity = quantity
        self.abscissa = abscissa
        self.landmark = landmark
        self.type = type
        self.gender = gender
        self.surgery = surgery
        self.values = []

        self.createSerie(quantity, abscissa, landmark, type, gender, surgery, dataBaseCRL, dataBaseSGS)

    def createSerie(self, quantity, abscissa, landmark, type, gender, surgery, dataBaseCRL, dataBaseSGS):

        # Select the database

        if type == "CRL":
            dataBase = dataBaseCRL
        elif type == "SGS":
            dataBase = dataBaseSGS

        # Find values

        self.values = fctOthers.findValues(dataBase, quantity, abscissa, landmark, gender, surgery)

    # Getters

    def getName(self):
        return self.name

    def getQuantity(self):
        return self.quantity

    def getAbscissa(self):
        return self.abscissa

    def getLandmarks(self):
        return self.landmark

    def getType(self):
        return self.type

    def getGender(self):
        return self.gender

    def getSurgery(self):
        return self.surgery

    def getValues(self):
        return self.values

    # Others

    def getBounds(self):

        xMin = +1 * float("Inf")
        xMax = -1 * float("Inf")

        yMin = +1 * float("Inf")
        yMax = -1 * float("Inf")

        for valueTemp in self.getValues():
            xMin = min(xMin, valueTemp.getX())
            xMax = max(xMax, valueTemp.getX())
            yMin = min(yMin, valueTemp.getY())
            yMax = max(yMax, valueTemp.getY())

        return [[xMin, xMax], [yMin, yMax]]