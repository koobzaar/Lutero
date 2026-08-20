"""Generate Newcomb-Benford Law plots for COVID-19 death-reporting data."""

import argparse
import os

import matplotlib.pyplot as plt
from tqdm import tqdm

import config
import func.data_manager as data_manager
import func.plotter as plotter
import func.style as style

RESULTS_DIR = "results"
MAD_LOG = os.path.join(RESULTS_DIR, "mad.txt")


def _finish(fig, name, fmt="svg"):
    path = plotter.save_figure(fig, name, fmt=fmt)
    plt.close(fig)
    print(f"Saved {path}")


def plot_country(jhu, country):
    result = plotter.compute_benford_result(country, jhu.death_variation(country))
    if result is None:
        print(f"'{country}': sample doesn't cover all nine leading digits, skipped.")
        return None
    fig = plotter.plot_single_country_figure(result)
    _finish(fig, country)
    return result


def plot_dataset(name, death_variation):
    result = plotter.compute_benford_result(name, death_variation)
    if result is None:
        print(f"'{name}': sample doesn't cover all nine leading digits, skipped.")
        return None
    print(f"{name}: n={result.sample_size}, MAD={result.mad:.4f} ({result.conformity})")
    fig = plotter.plot_single_country_figure(result)
    _finish(fig, name)
    return result


def run_all_countries(jhu):
    countries = jhu.available_countries()
    os.makedirs(RESULTS_DIR, exist_ok=True)
    written = 0
    country_mads = []
    with open(MAD_LOG, "w", encoding="utf-8") as mad_log:
        for country in tqdm(countries, desc="Processing countries"):
            result = plot_country(jhu, country)
            if result is not None:
                mad_log.write(f"{country},{result.mad}\n")
                country_mads.append((country, result.mad))
                written += 1
    print(f"Wrote MAD values for {written}/{len(countries)} countries to {MAD_LOG}")

    ranking_fig = plotter.plot_ranking(country_mads)
    _finish(ranking_fig, "ranking")


def run_specific_countries(jhu, countries):
    available = jhu.available_countries()
    unknown = [c for c in countries if c not in available]
    if unknown:
        raise ValueError(
            f"Unknown countries: {', '.join(unknown)}. "
            f"Choose from: {', '.join(available)}"
        )

    results = [plotter.compute_benford_result(c, jhu.death_variation(c)) for c in countries]
    skipped = [c for c, r in zip(countries, results) if r is None]
    if skipped:
        print(f"Skipped (sample doesn't cover all nine leading digits): {', '.join(skipped)}")
    results = [r for r in results if r is not None]
    if not results:
        print("Nothing to plot.")
        return

    fig = plotter.plot_comparison_grid(results)
    name = "comparison_" + "_".join(countries)
    _finish(fig, name)


def main(args):
    style.apply()

    if args.all or args.specific_countries:
        jhu = data_manager.JHUDeaths(config.DATA_PATH)
        if args.all:
            run_all_countries(jhu)
        else:
            run_specific_countries(jhu, args.specific_countries)

    elif args.cvi:
        plot_dataset("CVI", data_manager.cvi_death_variation(config.CVI_DATA_PATH))

    elif args.bms:
        plot_dataset("Brasil (MS)", data_manager.brazil_ms_death_variation(config.BRAZIL_MS_DATA_PATH))

    elif args.usa:
        plot_dataset("USA", data_manager.usa_death_variation(config.USA_DATA_PATH))

    elif args.country:
        jhu = data_manager.JHUDeaths(config.DATA_PATH)
        if args.country not in jhu.available_countries():
            print(f"'{args.country}' is not available. Please choose from the following countries:")
            print(", ".join(jhu.available_countries()))
            return
        plot_country(jhu, args.country)

    else:
        print("Please provide a country or use --all, --cvi, --bms, --usa, or --specific-countries.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot Benford's Law for a country or all countries.")
    parser.add_argument("--country", type=str, help="The country to plot.")
    parser.add_argument("--all", action="store_true", help="Plot all available countries.")
    parser.add_argument("--cvi", action="store_true", help="Plot only the Brazilian CVI dataset.")
    parser.add_argument("--bms", action="store_true", help="Plot only the Brazilian Ministry of Health dataset.")
    parser.add_argument("--usa", action="store_true", help="Plot only the USA dataset.")
    parser.add_argument("--specific-countries", nargs="+", help="Plot a comparison grid for specific countries.")
    main(parser.parse_args())
