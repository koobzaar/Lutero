import argparse
import config
import func.csv_data_converter
import func.data_manager
import func.plotter
from tqdm import tqdm

def main(country=None, all_countries=False, cvi=False, bms=False, usa=False):
    # data = func.csv_data_converter.Converter(config.DATA_PATH)._load_data();
    # data_manager = func.data_manager.Data(data);
    # countries = data_manager.get_all_available_countries();
    if all_countries:
        data = func.csv_data_converter.Converter(config.DATA_PATH)._load_data();
        data_manager = func.data_manager.Data(data);
        countries = data_manager.get_all_available_countries();
        with tqdm(total=len(countries), desc='Processing countries') as pbar:
            for country in countries:
                death_variation = data_manager.get_death_variation(country);
                func.plotter.plot_benford_law(country, death_variation);
                pbar.update()
    elif cvi:
        cvi_data = func.csv_data_converter.Converter(config.CVI_DATA_PATH)._load_data();
        data_manager = func.data_manager.Data(cvi_data);
        death_variation = data_manager.get_death_variation_for_CVI(cvi_data);
        print(len(death_variation))
        benford_value = func.plotter.plot_benford_law("CVI", death_variation);

    elif bms:
        bms_data = func.csv_data_converter.Converter(config.BRAZIL_MS_DATA_PATH)._load_data();
        data_manager = func.data_manager.Data(bms_data);
        death_variation = data_manager.get_death_variation_for_BMS(bms_data);
        print(len(death_variation))
        benford_value = func.plotter.plot_benford_law("Brasil (OMS)", death_variation);
    elif usa:
        usa_data = func.csv_data_converter.Converter(config.USA_DATA_PATH)._load_data();
        data_manager = func.data_manager.Data(usa_data);
        death_variation = data_manager.get_death_variation_for_USA(usa_data);
        print(len(death_variation))
        benford_value = func.plotter.plot_benford_law("USA", death_variation);
    
    elif country:
        data = func.csv_data_converter.Converter(config.DATA_PATH)._load_data();
        data_manager = func.data_manager.Data(data);
        countries = data_manager.get_all_available_countries();
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
    parser.add_argument('--cvi', action='store_true', help='Calculate only CVI')
    parser.add_argument('--bms', action='store_true', help='Calculate only Brazil MS')
    parser.add_argument('--usa', action='store_true', help='Calculate only USA')
    args = parser.parse_args()
    print(args)
    main(args.country, args.all, args.cvi, args.bms, args.usa)