import argparse
import config
import func.csv_data_converter
import func.data_manager
import func.plotter

from func.conversor import get_data_from_csv

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def load_data(path):
    return get_data_from_csv(path)

def process_country(data_manager, country, plot_func, *args):
    death_variation = data_manager.get_death_variation(country)
    plot_func(country, death_variation, *args)

def plot_benford(country, death_variation):
    return func.plotter.plot_benford_law(country, death_variation)

def process_specific_case(data_path, country_name, variation_func):
    data = load_data(data_path)
    data_manager = func.data_manager.Data(data)
    death_variation = variation_func(data_manager, data)
    print(len(death_variation))
    plot_benford(country_name, death_variation)

def main(country=None, all_countries=False, cvi=False, bms=False, usa=False, specific_countries_list=None):
    if all_countries or specific_countries_list:
        data = load_data(config.DATA_PATH)
        data_manager = func.data_manager.Data(data)
        countries = data_manager.get_all_available_countries()
        
        if all_countries:
            with tqdm(total=len(countries), desc='Processing countries') as pbar:
                for country in countries:
                    process_country(data_manager, country, plot_benford)
                    pbar.update()
        
        elif specific_countries_list:
            for country in specific_countries_list:
                if country not in countries:
                    raise ValueError(f"'{country}' is not available. Please choose from the following countries: {', '.join(countries)}")
            
            cmap = plt.get_cmap('inferno')
            color = cmap(np.linspace(0.2, 0.9, len(specific_countries_list)))
            current_color_index = 0
            with tqdm(total=len(specific_countries_list), desc='Processing countries') as pbar:
                for country in specific_countries_list:
                    process_country(data_manager, country, func.plotter.plot_multiple_data, color[current_color_index])
                    current_color_index += 1
                    pbar.update()
                
                expected_values = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
                digits = list(range(1, 10))
                plt.plot(digits, expected_values, label='Benford', color='black', ls='--')
                plt.scatter(digits, expected_values, color='black', marker='x', s=10, linewidths=1)
                ticks = np.arange(0, 0.5 + 0.05, 0.05)
                plt.yticks(ticks)
                plt.grid(axis='y')
                ax = plt.subplot(111)
                box = ax.get_position()
                ax.set_position([box.x0, box.y0 + box.height * 0.05, box.width, box.height])
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=5, frameon=False)
                plt.show()
                
    
    elif cvi:
        data = load_data(config.CVI_DATA_PATH)
        data_manager = func.data_manager.Data(data)
        death_variation = data_manager.get_death_variation_for_CVI(data)
        print(len(death_variation))
        plot_benford("CVI", death_variation)
    
    elif bms:
        data = load_data(config.BRAZIL_MS_DATA_PATH)
        data_manager = func.data_manager.Data(data)
        death_variation = data_manager.get_death_variation_for_BMS(data)
        print(len(death_variation))
        plot_benford("Brasil (OMS)", death_variation)
    
    elif usa:
        data = func.csv_data_converter.Converter(config.USA_DATA_PATH)._load_data()
        data_manager = func.data_manager.Data(data)
        death_variation = data_manager.get_death_variation_for_USA(data)
        print(len(death_variation))
        plot_benford("USA", death_variation)
    
    elif country:
        data = load_data(config.DATA_PATH)
        data_manager = func.data_manager.Data(data)
        countries = data_manager.get_all_available_countries()
        if country not in countries:
            print(f"'{country}' is not available. Please choose from the following countries:")
            print(', '.join(countries))
            return
        death_variation = data_manager.get_death_variation(country)
        print(f"Death variation for {country}: {death_variation}")
        benford_value = plot_benford(country, death_variation)
        print(f"Benford value for {country}: {benford_value}")
    else:
        print("Please provide a country or use the --all option.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot Benford Law for a country or all countries.')
    parser.add_argument('--country', type=str, help='The country to plot.')
    parser.add_argument('--all', action='store_true', help='If set, plots for all available countries.')
    parser.add_argument('--cvi', action='store_true', help='Calculate only CVI')
    parser.add_argument('--bms', action='store_true', help='Calculate only Brazil MS')
    parser.add_argument('--usa', action='store_true', help='Calculate only USA')
    parser.add_argument('--specific-countries', nargs='+', help='Calculate only specific countries')
    args = parser.parse_args()
    print(args)
    main(args.country, args.all, args.cvi, args.bms, args.usa, args.specific_countries)