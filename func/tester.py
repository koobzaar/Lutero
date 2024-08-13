import math

def benford_law_array():
    return [math.log10(1 + 1/i) for i in range(1, 10)]

def calulate_standard_deviations(day_by_day_variance):
    data_size = len(day_by_day_variance)
    arr_benford = benford_law_array()
    return [math.pow(((arr_benford[i] * (1 - arr_benford[i])) / data_size), 1/2) for i in range(9)]

def calculate_area_of_tolerance(day_by_day_variance):
    total_observations = len(day_by_day_variance
    )
    arr_benford = benford_law_array()
    standard_deviations = calulate_standard_deviations(day_by_day_variance)
    lower_bounds = [arr_benford[i] - (1.96 * standard_deviations[i] - 1/(2*total_observations)) for i in range(9)]
    upper_bounds = [arr_benford[i] + (1.96 * standard_deviations[i] + 1/(2*total_observations)) for i in range(9)]
    return lower_bounds, upper_bounds

def calculate_MAD(frequency):
    arr_benford = benford_law_array()
    data_size = len(frequency)
    mad = sum(abs(arr_benford[i] - frequency[i]) for i in range(9))
    return mad / data_size