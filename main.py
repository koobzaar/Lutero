import argparse
import config
import func.csv_data_converter
import func.data_manager
import func.plotter
from tqdm import tqdm

def main(country=None, all_countries=False):
    data = func.csv_data_converter.Converter(config.DATA_PATH).get_data_coverted();
    data_manager = func.data_manager.Data(data);
    countries = data_manager.get_all_available_countries();
    print(f"Available countries: {', '.join(countries)}")
    if all_countries:
        with tqdm(total=len(countries), desc='Processing countries') as pbar:
            for country in countries:
                death_variation = data_manager.get_death_variation(country);
                func.plotter.plot_benford_law(country, death_variation);
                pbar.update()
    elif country:
        if country not in countries:
            print(f"'{country}' is not available. Please choose from the following countries:")
            print(', '.join(countries))
            return
        death_variation = data_manager.get_death_variation(country);
        print(f"Death variation for {country}: {death_variation}")
        benford_value = func.plotter.plot_benford_law(country, death_variation);
        print(f"Benford value for {country}: {benford_value}")
    else:
        print("Please provide a country or use the --all option.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot Benford Law for a country or all countries.')
    parser.add_argument('--country', type=str, help='The country to plot.')
    parser.add_argument('--all', action='store_true', help='If set, plots for all available countries.')
    args = parser.parse_args()
    main(args.country, args.all)