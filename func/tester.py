import math
def benfordLawArray():
    benfordLaw = []
    for i in range(1, 10):
        benfordLaw.append(math.log10(1 + 1/i))
    return benfordLaw

def calculateStandardDeviations(day_by_day_variance):
    sizeOfData = len(day_by_day_variance)
    arrBenford = benfordLawArray()
    standardDeviations = []
    for i in range(0, 9):
        standardDeviations.append(math.sqrt((arrBenford[i]*(1-arrBenford[i]))/sizeOfData))
    return standardDeviations

def calculateAreaOfTolerance(day_by_day_variance):
    arrBenford = benfordLawArray()
    standardDeviations = calculateStandardDeviations(day_by_day_variance)
    lowerBounds = []
    for i in range(0, 9):
        lowerBounds.append(arrBenford[i] - 1.96 * standardDeviations[i])

    upperBounds = []
    for i in range(0, 9):
        upperBounds.append(arrBenford[i] + 1.96 * standardDeviations[i])

    return lowerBounds, upperBounds


