import math
def benford_law_array():
    benfordLaw = []
    for i in range(1, 10):
        benfordLaw.append(math.log10(1 + 1/i))
    return benfordLaw

def calulate_standard_deviations(day_by_day_variance):
    sizeOfData = len(day_by_day_variance)
    arrBenford = benford_law_array()
    standardDeviations = []
    for i in range(0, 9):
        standardDeviations.append(math.sqrt((arrBenford[i]*(1-arrBenford[i]))/sizeOfData))
    return standardDeviations

def calculateAreaOfTolerance(day_by_day_variance):
    arrBenford = benford_law_array()
    standardDeviations = calulate_standard_deviations(day_by_day_variance)
    lowerBounds = []
    for i in range(0, 9):
        lowerBounds.append(arrBenford[i] - 1.96 * standardDeviations[i])

    upperBounds = []
    for i in range(0, 9):
        upperBounds.append(arrBenford[i] + 1.96 * standardDeviations[i])

    return lowerBounds, upperBounds

def calculateMAD(frequency):
    arrBenford = benford_law_array()
    sizeOfData = len(frequency)
    print(sizeOfData)
    mad = 0
    for i in range(0, 9):
        mad += abs(arrBenford[i] - frequency[i])
    return mad/sizeOfData

