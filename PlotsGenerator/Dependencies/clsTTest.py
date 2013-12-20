# General imports

from scipy import stats

# Class imports



# Function import



# Class definition

class tTest:

    # Constructor

    def __init__(self):

        self.seriesCRL = []
        self.seriesSGS = []

        self.pValue = False

    # Getters

    def getSeries(self, type):
        if type == "CRL":
            return self.seriesCRL
        elif type == "SGS":
            return self.seriesSGS

    def getPValue(self):
        if self.pValue == False:
            self.computePValue()
        return self.pValue

    # Others

    def addSerie(self, serie):
        if serie.getType() == "CRL":
            self.seriesCRL.append(serie)
        elif serie.getType() == "SGS":
            self.seriesSGS.append(serie)

    def computePValue(self):

        YCRL = []
        YSGS = []

        # Get the values

        for serieTemp in self.seriesCRL:
            for valueTemp in serieTemp.getValues():
                YCRL.append(valueTemp.getY())

        for serieTemp in self.seriesSGS:
            for valueTemp in serieTemp.getValues():
                YSGS.append(valueTemp.getY())

        # Compute the P-Value

        self.pValue = stats.ttest_ind(YCRL, YSGS)[1]