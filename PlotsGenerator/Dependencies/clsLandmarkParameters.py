# General imports



# Class imports



# Function import



# Class definition

class landmarkParameters:

    # Constructors

    def __init__(self, name, perimeter, area, hydraulicDiameter):

        self.name = name
        self.perimeter = perimeter
        self.area = area
        self.hydraulicDiameter = hydraulicDiameter

    # Getters

    def getName(self):
        return self.name

    def getPerimeter(self):
        return self.perimeter

    def getArea(self):
        return self.area

    def getHydraulicDiameter(self):
        return self.hydraulicDiameter

    def getQuantity(self, quantity):
        if quantity == "perimeter":
            return self.getPerimeter()
        elif quantity == "area":
            return self.getArea()
        elif quantity == "hydraulicDiameter":
            return self.getHydraulicDiameter()
        else:
            return -1

    # Others

    def display(self):
        print("{0} : {1} {2} {3}".format(self.getName(), self.getPerimeter(), self.getArea(), self.getHydraulicDiameter()))