import matplotlib.pyplot as plt
import os
import re
import string
import func.tester
import numpy as np

import func.benford as benford

from collections import Counter

def plot_data(digits, frequencies, expected_values, country_name, tolerance_area, sizeAmostra):
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
    mad = func.tester.calculateMAD(frequencies)
    
    if not os.path.exists('results'):
        os.makedirs('results')
    with open('results/mad.txt', 'a') as file:
        file.write(f"{country_name},{mad}\n")

    if(higherTolerance is not None):
        plt.plot(digits, higherTolerance, label='Tolerância Superior',color="#8577ff", ls='dotted', alpha=0.5)
        plt.scatter(digits, higherTolerance, color='#8577ff', marker='x', s=10, linewidths=1)

   
    plt.plot(digits, frequencies, label=country_name, color='#ff8577', alpha=0.9)
    plt.scatter(digits, frequencies, color='red', marker='x', s=10, linewidths=1)

    plt.plot(digits, expected_values, label='Benford', color='grey', ls='--')
    plt.scatter(digits, expected_values, color='grey', marker='x', s=10, linewidths=1)

    if(lowerTolerance is not None):
        plt.plot(digits, lowerTolerance, label='Tolerância Inferior', color="#01a833", ls='dotted', alpha=0.5)
        plt.scatter(digits, lowerTolerance, color='#01a833', marker='x', s=10, linewidths=1)
    
    for i, digit in enumerate(digits):
        plt.vlines(x=digit, ymin=lowerTolerance[i], ymax=higherTolerance[i], colors='black', linestyles='solid', linewidth=0.5)
    
    plt.xlabel('Primeiro Dígito')
    plt.ylabel('Frequência')
    plt.title(f'MAD: {mad:.4f} Tamanho da Amostra: {sizeAmostra}')
    plt.xticks(digits)
    valor_maximo = max(frequencies)
    ticks = np.arange(0, valor_maximo + 0.05, 0.05)
    plt.yticks(ticks)
    plt.grid(axis='y')

    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
    ncol = 3 if len(country_name) > 4 else 5
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.11), ncol=ncol, frameon=False)

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
    benford_data = benford.caculate_first_digit_distribution(death_variance)

    if benford_data is None:
        return

    digits = list(range(1, 10))
    frequencies = benford_data
    expected_values = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
    plot_data(digits, frequencies, expected_values, country_name, tolerance_area=(upper, lower), sizeAmostra=len(death_variance))
    save_plot(country_name)

    return benford_data

def plot_multiple_data(country_name, death_variance, color):
    """
    Plots the Benford's Law distribution for multiple countries and saves them as PNG files.

    Args:
        countries (list): The countries.
        death_variances (list): The death variance data.

    Returns:
        None
    """
    benford_data = benford.caculate_first_digit_distribution(death_variance)
    if benford_data is None:
        return
    frequencies = benford_data
    digits = list(range(1, 10))
    expected_values = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
    plot_multiple_data_in_graph(digits, frequencies, expected_values, country_name, color)
    
def generate_random_visible_hex_color():
    """
    Generate a random visible hex color.

    Returns:
        str: The hex color.
    """
    r = lambda: np.random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())

def plot_multiple_data_in_graph(digits, frequencies, expected_values, country_name, current_color):
   
    plt.plot(digits, frequencies, label=country_name, color=current_color, alpha=0.8)
    plt.scatter(digits, frequencies, color=current_color, marker='x', s=10, linewidths=1)
    plt.xlabel('Primeiro Dígito')
    plt.ylabel('Frequência')
    
    