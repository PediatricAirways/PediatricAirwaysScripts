class values:

    # Constructors

    def __init__(self, index, position, distance, perimeter, area, hydraulicDiameter, landmarkName):
        self.index = index
        self.position = position
        self.distance = distance
        self.perimeter = perimeter
        self.area = area
        self.hydraulicDiameter = hydraulicDiameter
        self.landmarkName = landmarkName

    # Getter

    def getIndex(self):
        return self.index

    def getPosition(self):
        return self.position

    def getDistance(self):
        return self.distance

    def getPerimeter(self):
        return self.perimeter

    def getArea(self):
        return self.area

    def getHydraulicDiameter(self):
        return self.hydraulicDiameter

    def getLandmarkName(self):
        return self.landmarkName

    def getAbscissa(self, abscissa):
        if abscissa == "position":
            return self.getPosition()
        elif abscissa == "distance":
            return self.getDistance()

    def getQuantity(self, quantityName):
        if quantityName == "perimeter":
            return self.getPerimeter()
        elif quantityName == "area":
            return self.getArea()
        elif quantityName == "hydraulicDiameter":
            return self.getHydraulicDiameter()

    # Setters

    def setIndex(self, index):
        self.index = index

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

    def setLandmarkName(self, landmarkName):
        self.landmarkName = landmarkName

    # Others

    def toString(self):

        nbDecimals = 5

        index = self.getIndex()
        position = round(self.getPosition(), nbDecimals)
        distance = round(self.getDistance(), nbDecimals)
        perimeter = round(self.getPerimeter(), nbDecimals)
        area = round(self.getArea(), nbDecimals)
        hydraulicDiameter = round(self.getHydraulicDiameter(), nbDecimals)
        landmarkName = self.getLandmarkName()

        string = "{0} : {1} {2} {3} {4} {5} {6}".format(index, position, distance, perimeter, area, hydraulicDiameter, landmarkName)

        return string

    def display(self):
        print(self.toString())