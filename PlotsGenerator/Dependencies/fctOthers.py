# General imports

from matplotlib import pyplot

# Classes imports

from clsValue import value
from clsPlot import plot
from clsSubPlot import subPlot
from clsSerie import serie
from clsRegression import regression
from clsTTest import tTest

# Functions import



# Functions definition

def findValues(dataBase, quantity, abscissa, landmark, gender, surgery):

    values = []

    for caseTemp in dataBase.getCases():
        if caseTemp.getGender() == gender:
            if caseTemp.getSurgery() == surgery:
                for landmarkParametersTemp in caseTemp.getLandmarksParameters():
                    if landmarkParametersTemp.getName() == landmark:
                        if abscissa == "age":
                            valueTemp = value(caseTemp.getAge(), landmarkParametersTemp.getQuantity(quantity))
                            values.append(valueTemp)
                        elif abscissa == "weight":
                            valueTemp = value(caseTemp.getWeight(), landmarkParametersTemp.getQuantity(quantity))
                            values.append(valueTemp)

    return values

def generatePlot(name, quantity, abscissa, dataBaseCRL, dataBaseSGS, fileName):

    p = plot(name)
    p.addSubPlot(generateSubPlot(quantity, abscissa, "TVC", dataBaseCRL, dataBaseSGS))
    p.addSubPlot(generateSubPlot(quantity, abscissa, "Subglottic", dataBaseCRL, dataBaseSGS))
    p.addSubPlot(generateSubPlot(quantity, abscissa, "MidTrachea", dataBaseCRL, dataBaseSGS))

    p.setShareXScale(True)
    p.setShareYScale(True)
    p.save(fileName)

def generatePlot2(name, quantity, abscissa, dataBaseCRL, dataBaseSGS, fileName):

    p = plot(name)
    p.addSubPlot(generateSubPlot(quantity, abscissa, "Ratio", dataBaseCRL, dataBaseSGS))
    p.addSubPlot(generateSubPlot(quantity, abscissa, "RatioScore", dataBaseCRL, dataBaseSGS))
    p.addSubPlot(generateSubPlot(quantity, abscissa, "AtlasScore", dataBaseCRL, dataBaseSGS))

    p.setShareXScale(True)
    #p.setShareYScale(True)
    p.save(fileName)

def generateSubPlot(quantity, abscissa, landmark, dataBaseCRL, dataBaseSGS):

    s1 = serie("CRL M", quantity, abscissa, landmark, "CRL", "M", False, dataBaseCRL, dataBaseSGS)
    s2 = serie("CRL F", quantity, abscissa, landmark, "CRL", "F", False, dataBaseCRL, dataBaseSGS)

    s3 = serie("SGS M", quantity, abscissa, landmark, "SGS", "M", False, dataBaseCRL, dataBaseSGS)
    s4 = serie("SGS F", quantity, abscissa, landmark, "SGS", "F", False, dataBaseCRL, dataBaseSGS)
    s5 = serie("SGS M Surgery", quantity, abscissa, landmark, "SGS", "M", True, dataBaseCRL, dataBaseSGS)
    s6 = serie("SGS F Surgery", quantity, abscissa, landmark, "SGS", "F", True, dataBaseCRL, dataBaseSGS)

    r1 = regression("CRL", quantity, abscissa, "CRL")
    r1.addSerie(s1)
    r1.addSerie(s2)

    r2 = regression("SGS", quantity, abscissa, "SGS")
    r2.addSerie(s5)
    r2.addSerie(s6)

    tT = tTest()
    tT.addSerie(s1)
    tT.addSerie(s2)
    tT.addSerie(s5)
    tT.addSerie(s6)

    xLabelPart1 = abscissa.title()
    if abscissa == "age":
        xLabelPart2 = "(months)"
    elif abscissa == "weight":
        xLabelPart2 = "(kilograms)"
    else:
        xLabelPart2 = ""

    yLabelPart1 = quantity.title()
    if landmark == "TVC" or landmark == "Subglottic" or landmark == "MidTrachea":
        if quantity == "perimeter" or quantity == "hydraulicDiameter":
            yLabelPart2 = "(mm)"
        elif quantity == "area":
            yLabelPart2 = "(mm2)"
        else:
            yLabelPart2 = ""
    else:
        yLabelPart2 = ""

    sP = subPlot(landmark, [ xLabelPart1 + " " + xLabelPart2, yLabelPart1 + " " + yLabelPart2])
    sP.addSerie(s1)
    sP.addSerie(s2)
    sP.addSerie(s3)
    sP.addSerie(s4)
    sP.addSerie(s5)
    sP.addSerie(s6)
    sP.addRegression(r1)
    sP.addRegression(r2)
    sP.addTTest(tT)

    return sP