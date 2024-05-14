import matplotlib.pyplot as plt
import func.benford
import os
import re
import string

def calculate_benford_data(country_name, death_variance):
    """
    Calculate the Benford's Law distribution for a given country.

    Args:
        country_name (str): The country name.
        death_variance (list): The death variance data.

    Returns:
        list: The Benford's Law data.
    """
    data = func.benford.CountryData(country_name, death_variance)
    benford_data = data.calculate_benford_law()

    if len(benford_data) != 9:
        print(f"Os dados de Benford para {country_name} não têm o tamanho esperado. Ignorando este país.")
        return None

    return benford_data

def plot_data(digits, frequencies, expected_values, country_name):
    """
    Plot the Benford's Law distribution.

    Args:
        digits (list): The digits.
        frequencies (list): The frequencies.
        expected_values (list): The expected values.
        country_name (str): The country name.

    Returns:
        None
    """
    plt.plot(digits, frequencies, label='Real Data')
    plt.plot(digits, expected_values, label='Expected Values', color='grey')
    plt.fill_between(digits, [i - 0.1 * i for i in expected_values], [i + 0.1 * i for i in expected_values], color='grey', alpha=0.2)

    plt.xlabel('Primeiro Dígito')
    plt.ylabel('Frequência')
    plt.title(f'Distribuição da Lei de Benford para {country_name}')
    plt.xticks(digits)
    plt.yticks([i/10 for i in range(0, 11)])

    plt.legend()

def sanitize_filename(filename):
    """
    Sanitize the filename by removing invalid characters.

    Args:
        filename (str): The filename.

    Returns:
        str: The sanitized filename.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_filename = ''.join(c for c in filename if c in valid_chars)
    sanitized_filename = sanitized_filename.replace(' ','_') # I don't like spaces in filenames.
    return sanitized_filename

def save_plot(country_name):
    """
    Save the plot as a PNG file.

    Args:
        country_name (str): The country name.

    Returns:
        None
    """
    if not os.path.exists('results'):
        os.makedirs('results')

    # Sanitize the country name to be a valid filename
    sanitized_country_name = sanitize_filename(country_name)

    plt.savefig(f'results/{sanitized_country_name}_benford_law.png')
    plt.clf()

def plot_benford_law(country_name, death_variance):
    """
    Plots the Benford's Law distribution for a given country and saves it as a PNG file.

    Args:
        country_name (str): The country name.
        death_variance (list): The death variance data.

    Returns:
        None
    """
    benford_data = calculate_benford_data(country_name, death_variance)

    if benford_data is None:
        return

    digits = list(range(1, 10))
    frequencies = benford_data
    expected_values = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

    plot_data(digits, frequencies, expected_values, country_name)
    save_plot(country_name)

    return benford_data