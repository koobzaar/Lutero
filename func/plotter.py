import matplotlib.pyplot as plt
import func.benford
import os
import re
import string
import func.tester
import numpy as np

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

def plot_data(digits, frequencies, expected_values, country_name, tolerance_area):
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
    lowerTolerance, higherTolerance = tolerance_area
    
    
    plt.plot(digits, higherTolerance, label='Tolerância',color="#8577ff", ls='dotted', alpha=0.5)
    plt.scatter(digits, higherTolerance, color='#8577ff', marker='x', s=10, linewidths=1)

   
    plt.plot(digits, frequencies, label={country_name}, color='#ff8577', alpha=0.9)
    plt.scatter(digits, frequencies, color='red', marker='x', s=10, linewidths=1)

    plt.plot(digits, expected_values, label='Benford', color='grey', ls='--')
    plt.scatter(digits, expected_values, color='grey', marker='x', s=10, linewidths=1)

   
    plt.plot(digits, lowerTolerance, label='Tolerância', color="#01a833", ls='dotted', alpha=0.5)
    plt.scatter(digits, lowerTolerance, color='#01a833', marker='x', s=10, linewidths=1)
    
    for i, digit in enumerate(digits):
        plt.vlines(x=digit, ymin=lowerTolerance[i], ymax=higherTolerance[i], colors='black', linestyles='solid', linewidth=0.5)
    
    plt.xlabel('Primeiro Dígito')
    plt.ylabel('Frequência')
    plt.title(f'Distribuição da Lei de Benford para {country_name}')
    plt.xticks(digits)
    valor_maximo = max(frequencies)
    ticks = np.arange(0, valor_maximo + 0.05, 0.05)
    plt.yticks(ticks)
    plt.grid(axis='y')

    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.13), ncol=5, frameon=False)

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

    # Generating the tolerance area
    upper, lower = func.tester.calculateAreaOfTolerance(death_variance)

    benford_data = calculate_benford_data(country_name, death_variance)

    if benford_data is None:
        return

    digits = list(range(1, 10))
    frequencies = benford_data
    expected_values = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

    plot_data(digits, frequencies, expected_values, country_name, tolerance_area=(upper, lower))
    save_plot(country_name)

    return benford_data