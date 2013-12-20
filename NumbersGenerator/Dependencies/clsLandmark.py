# Imports



# Class definition

class landmark:

    # Constructors

    def __init__(self, name, position, distance):
        self.name = name
        self.position = position
        self.distance = distance

    # Getters

    def getName(self):
        return self.name

    def getAbscissa(self, abscissa):
        if abscissa == "position":
            return self.position
        elif abscissa == "distance":
            return self.distance

    # Others

    def display(self):
        print("{0} : {1} {2}".format(self.name, self.position, self.distance))