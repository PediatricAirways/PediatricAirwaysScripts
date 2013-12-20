# Imports



# Class definition

class weightedValues:

    # Constructors

    def __init__(self, weight, position, perimeter, area, hydraulicDiameter):
        self.weight = weight
        self.position = position
        self.perimeter = perimeter
        self.area = area
        self.hydraulicDiameter = hydraulicDiameter

    # Getter

    def getWeight(self):
        return self.weight

    def getPosition(self):
        return self.position

    def getPerimeter(self):
        return self.perimeter

    def getArea(self):
        return self.area

    def getHydraulicDiameter(self):
        return self.hydraulicDiameter

    def getQuantity(self, quantityName):
        if quantityName == "perimeter":
            return self.getPerimeter()
        elif quantityName == "area":
            return self.getArea()
        elif quantityName == "hydraulicDiameter":
            return self.getHydraulicDiameter()

    # Setters

    def setWeight(self, weight):
        self.weight = weight

    def setPosition(self, position):
        self.position = position

    def setDistance(self, distance):
        self.distance = distance

    def setPerimeter(self, perimeter):
        self.perimeter = perimeter

    def setArea(self, area):
        self.area = area

    def setHydraulicDiameter(self, hydraulicDiameter):
        self.hydraulicDiameter = hydraulicDiameter

    # Others

    def toString(self):

        nbDecimals = 5

        weight = self.getWeight()
        position = self.getPosition()
        perimeter = round(self.getPerimeter(), nbDecimals)
        area = round(self.getArea(), nbDecimals)
        hydraulicDiameter = round(self.getHydraulicDiameter(), nbDecimals)

        string = "{0} : {1} {2} {3} {4}".format(weight, position, perimeter, area, hydraulicDiameter)

        return string

    def display(self):
        print(self.toString())