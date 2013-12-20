# General imports



# Class imports



# Function import



# Class definition

class plotter:

    # Constructors

    def __init__(self, name):

        self.name = name
        self.plots = []

    # Getters

    def getName(self):
        return self.name

    def getPlots(self):
        return self.plots

    # Others

    def addPlot(self, plot):
        self.plots.append(plot)