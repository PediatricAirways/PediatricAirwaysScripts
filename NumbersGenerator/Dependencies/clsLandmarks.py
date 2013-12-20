# Imports

from clsLandmark import landmark

# Class definition

class landmarks:

    # Constructors

    def __init__(self):

        self.landmarksList = []

    # Getters

    def getLandmarksList(self):
        return self.landmarksList

    def getLandmarkByName(self, landmarkName):

        for landmarkTemp in self.landmarksList:
            if landmarkTemp.getName() == landmarkName:
                return landmarkTemp

    # Others

    def addLandmark(self, landmark):
        self.landmarksList.append(landmark)

    # Others

    def display(self):

        for landmarkTemp in self.landmarksList:
            landmarkTemp.display()