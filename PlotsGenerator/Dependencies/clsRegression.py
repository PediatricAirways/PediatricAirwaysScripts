# General imports

import numpy
from scipy import stats

# Class imports



# Function import



# Class definition

class regression:

    # Constructor

    def __init__(self, name, quantity, abscissa, type):

        self.name = name
        self.quantity = quantity
        self.abscissa = abscissa
        self.type = type
        self.series = []
        self.a = -1
        self.b = -1
        self.r2 = -1

    # Getters

    def getName(self):
        return self.name

    def getQuantity(self):
        return self.quantity

    def getAbscissa(self):
        return self.abscissa

    def getType(self):
        return self.type

    def getSeries(self):
        return self.series

    def getParameters(self):
        return [self.a, self.b, self.r2]

    # Others

    def addSerie(self, serie):

        if serie.getQuantity() == self.getQuantity():
            if serie.getAbscissa() == self.getAbscissa():
                if serie.getType() == self.getType():
                    self.series.append(serie)
                    self.computeParameters()

    def computeParameters(self):

        X = []
        Y = []

        # Get all the values

        for serieTemp in self.getSeries():
            for valueTemp in serieTemp.getValues():
                X.append(valueTemp.getX())
                Y.append(valueTemp.getY())

        # Transform the values

        X = numpy.array(X)
        Y = numpy.array(Y)

        # Compute parameters

        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)

        self.a = slope
        self.b = intercept
        self.r2 = pow(r_value, 2)