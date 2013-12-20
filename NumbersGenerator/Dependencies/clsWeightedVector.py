# Imports

import math

from clsWeightedValues import weightedValues

# Class definition

class weightedVector:

    # Constructors

    def __init__(self, atlasType, value, sigma, position, dataBase):

        self.position = position
        self.atlasType = atlasType
        self.weightedValuesList = []

        if atlasType == "age":
            self.age = value
            self.weight = False

        elif atlasType == "weight":
            self.age = False
            self.weight = value

        # Create weighted values list

        for caseTemp in dataBase.getCases():

            # Weight

            if atlasType == "age":
                weightTemp = getWeight(caseTemp.getAge(), self.age, sigma)
            elif atlasType == "weight":
                weightTemp = getWeight(caseTemp.getWeight(), self.weight, sigma)

            # Position

            positionTemp = position

            # Values

            perimeterTemp = caseTemp.getGeometry().getInterpolations().getInterpolatesValues("perimeter", "position", positionTemp)
            areaTemp = caseTemp.getGeometry().getInterpolations().getInterpolatesValues("area", "position", positionTemp)
            hydraulicDiameterTemp = caseTemp.getGeometry().getInterpolations().getInterpolatesValues("hydraulicDiameter", "position", positionTemp)

            weightedValuesTemp = weightedValues(weightTemp, positionTemp, perimeterTemp, areaTemp, hydraulicDiameterTemp)

            self.weightedValuesList.append(weightedValuesTemp)

        # Normalize them

        weightsSum = 0

        for weightedValuesTemp in self.weightedValuesList:
            weightsSum += weightedValuesTemp.getWeight()

        for weightedValuesTemp in self.weightedValuesList:
            weightedValuesTemp.setWeight(weightedValuesTemp.getWeight() / weightsSum)

    # Getters

    def getPosition(self):
        return self.position

    def getWeight(self):
        return self.weight

    def getAge(self):
        return self.age

    def getWeightedValuesList(self):
        return self.weightedValuesList

    # Others

    def sortByQuantity(self, quantity):
        self.weightedValuesList.sort(key = lambda weightedValues: weightedValues.getQuantity(quantity))

    def getQuantityForPercentile(self, quantity, percentile):

        percentile /= 100.0

        # Sort the array by quantity

        self.sortByQuantity(quantity)

        # Compute the value

        weightsSum = 0
        i = 0

        while weightsSum <= percentile: #or 1 - weightsSum >= percentile:
            weightsSum += self.weightedValuesList[i].getWeight()
            i += 1

        return self.weightedValuesList[i - 1].getQuantity(quantity)

    def display(self):
        for weightedValuesTemp in self.weightedValuesList:
            weightedValuesTemp.display()

# Functions definition

def getWeight(caseValue, value, sigma):
    return math.exp(-0.5 * pow((caseValue - value) / sigma, 2))