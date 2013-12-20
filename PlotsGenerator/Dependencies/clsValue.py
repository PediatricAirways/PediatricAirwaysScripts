# General imports



# Class imports



# Function import



# Class definition

class value:

    # Constructor

    def __init__(self, x, y):

        self.x = x
        self.y = y

    # Getters

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    # Others

    def display(self):
        print("[{0}, {1}]".format(self.getX(), self.getY()))