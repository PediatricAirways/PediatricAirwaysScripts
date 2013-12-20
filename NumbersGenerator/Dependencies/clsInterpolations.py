# Imports

import math
import numpy
from scipy import interpolate

from clsValues import values

# Global variables

# Class definition

class interpolations:

    # Constructors

    def __init__(self):

        self.interpolationPerimeterDistance = False
        self.interpolationAreaDistance = False
        self.interpolationHydraulicDiameterDistance = False

        self.interpolationPerimeterPosition = False
        self.interpolationAreaPosition = False
        self.interpolationHydraulicDiameterPosition = False

    def computeInterpolations(self, valuesList):

        self.interpolationPerimeterDistance = computeInterpolation(valuesList, "perimeter", "distance")
        self.interpolationAreaDistance = computeInterpolation(valuesList, "area", "distance")
        self.interpolationHydraulicDiameterDistance = computeInterpolation(valuesList, "hydraulicDiameter", "distance")

        self.interpolationPerimeterPosition = computeInterpolation(valuesList, "perimeter", "position")
        self.interpolationAreaPosition = computeInterpolation(valuesList, "area", "position")
        self.interpolationHydraulicDiameterPosition = computeInterpolation(valuesList, "hydraulicDiameter", "position")

    # Getters

    def getInterpolation(self, quantity, abscissa):

        if abscissa == "distance":
            if quantity == "perimeter":
                return self.interpolationPerimeterDistance
            elif quantity == "area":
                return self.interpolationAreaDistance
            elif quantity == "hydraulicDiameter":
                return self.interpolationHydraulicDiameterDistance

        elif abscissa == "position":
            if quantity == "perimeter":
                return self.interpolationPerimeterPosition
            elif quantity == "area":
                return self.interpolationAreaPosition
            elif quantity == "hydraulicDiameter":
                return self.interpolationHydraulicDiameterPosition

    def getInterpolatesValues(self, quantity, abscissa, XInterpolation):

        if abscissa == "distance":
            if quantity == "perimeter":
                return interpolate.splev(XInterpolation, self.interpolationPerimeterDistance)
            elif quantity == "area":
                return interpolate.splev(XInterpolation, self.interpolationAreaDistance)
            elif quantity == "hydraulicDiameter":
                return interpolate.splev(XInterpolation, self.interpolationHydraulicDiameterDistance)

        elif abscissa == "position":
            if quantity == "perimeter":
                return interpolate.splev(XInterpolation, self.interpolationPerimeterPosition)
            elif quantity == "area":
                return interpolate.splev(XInterpolation, self.interpolationAreaPosition)
            elif quantity == "hydraulicDiameter":
                return interpolate.splev(XInterpolation, self.interpolationHydraulicDiameterPosition)

def computeInterpolation(valuesList, quantity, abscissa):

    X = []
    Y = []

    # Get the values

    for valuesTemp in valuesList:
        X.append(valuesTemp.getAbscissa(abscissa))
        Y.append(valuesTemp.getQuantity(quantity))

    # Compute the values to interpolate (To avoid errors)

    linearInterpolation = interpolate.interp1d(X, Y)

    X2 = numpy.linspace(numpy.min(X), numpy.max(X), 400)
    Y2 = linearInterpolation(X2)

    # Compute smoothing

    amplitude = max(Y)
    smoothing = getSmoothing(amplitude)
    smoothedInterpolation = interpolate.splrep(X2, Y2, s = smoothing, k = 3)

    return smoothedInterpolation

def getSmoothing(amplitude):

    minS = 10

    sB = 12000.0
    dB = 375.0

    A = sB / pow(dB, 2)

    smoothing = A * pow(amplitude, 2)

    return max(smoothing, minS)