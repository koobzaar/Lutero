from collections import Counter

def reduce_data_to_first_digit(dataset):
    return [int(str(abs(number))[0]) for number in dataset if number != 0]

def count_digit_appearance(reduced_dataset):
    return Counter(reduced_dataset)

def all_digits_are_present(benford_data_for_a_country):
    return len(set(benford_data_for_a_country)) == 9

def calculate_benford_distribution_for_data(amount_of_each_digit, dataset_size):
    return [count / dataset_size for digit, count in amount_of_each_digit.items()]

def caculate_first_digit_distribution(dataset):
    """
    Calculate the Benford's Law distribution for a given country.

    Args:
        dataset (list): The death variance data.

    Returns:
        list: The Benford's Law data.
    """
    reduced_dataset = reduce_data_to_first_digit(dataset)

    amount_of_each_digit = count_digit_appearance(reduced_dataset)

    dataset_size = len(reduced_dataset)

    benford_data = calculate_benford_distribution_for_data(amount_of_each_digit, dataset_size)

    if not all_digits_are_present(amount_of_each_digit):
        return None
    else:
        return benford_data