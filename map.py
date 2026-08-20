"""World choropleth of Newcomb-Benford Law conformity (MAD) per country.

Run `python main.py --all` first to populate results/mad.txt.
"""

import argparse
import os

import geopandas
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import func.plotter as plotter
import func.style as style
import func.tester as tester

SHAPEFILE = "world_map/ne_110m_admin_0_countries.shp"
MAD_LOG = "results/mad.txt"
EQUAL_EARTH = "+proj=eqearth"  # equal-area: color intensity isn't confounded by high-latitude area inflation

# JHU's "Country/Region" labels that don't match Natural Earth's ADMIN field.
NAME_ALIASES = {
    "US": "United States of America",
    "Congo (Brazzaville)": "Republic of the Congo",
    "Congo (Kinshasa)": "Democratic Republic of the Congo",
    "Cote d'Ivoire": "Ivory Coast",
    "Burma": "Myanmar",
    "Taiwan*": "Taiwan",
    "Serbia": "Republic of Serbia",
    "Tanzania": "United Republic of Tanzania",
    "West Bank and Gaza": "Palestine",
    "Eswatini": "eSwatini",
}


def load_mad_values(mad_log=MAD_LOG):
    """Read the `country,mad` rows written by `main.py --all` into a {country: mad} dict."""
    if not os.path.exists(mad_log) or os.path.getsize(mad_log) == 0:
        raise FileNotFoundError(
            f"'{mad_log}' not found or empty. Run `python main.py --all` first "
            "to compute MAD for every country."
        )

    mad_by_country = {}
    with open(mad_log, "r", encoding="utf-8") as file:
        for line in file:
            country, mad = line.strip().split(",")
            mad_by_country[NAME_ALIASES.get(country, country)] = float(mad)
    return mad_by_country


def build_choropleth(mad_by_country):
    """
    Classify every country into one of Nigrini's four MAD conformity
    categories -- the same categories and colors used on every country's own
    chart -- rather than a continuous gradient with no interpretable
    threshold. Countries never tested (no data, not "zero deviation") get a
    hatched neutral fill via a dedicated legend entry, never a data color.
    """
    style.apply()
    world = geopandas.read_file(SHAPEFILE)
    world = world[world["ADMIN"] != "Antarctica"].to_crs(EQUAL_EARTH)

    world["mad"] = world["ADMIN"].map(mad_by_country)
    world["area"] = world.geometry.area
    tested = world["mad"].notna()
    world.loc[tested, "conformity"] = world.loc[tested, "mad"].apply(tester.mad_conformity_category)

    matched = set(world.loc[tested, "ADMIN"])
    missing = sorted(set(mad_by_country) - matched)
    if missing:
        print(f"{len(missing)} countries not found in the shapefile, skipped: {', '.join(missing)}")

    fig, ax = plt.subplots(figsize=(14, 7.6), layout="constrained")

    world.loc[~tested].plot(
        ax=ax, color="#f4f4f5", edgecolor="white", linewidth=0.4, hatch="///", zorder=1,
    )
    for category in style.CONFORMITY_ORDER:
        subset = world.loc[world["conformity"] == category]
        if len(subset):
            subset.plot(ax=ax, color=style.CONFORMITY_COLORS[category], edgecolor="white", linewidth=0.4, zorder=2)

    # Label only the physically largest countries -- the map's job is the spatial
    # pattern (where), not exact per-country reading (how much, precisely; that's
    # what the ranking chart is for). Labeling every tested country crowds small,
    # densely packed regions (the Balkans, Central America, the Caribbean).
    largest_tested = world.loc[tested].nlargest(16, "area")
    for _, row in largest_tested.iterrows():
        point = row.geometry.representative_point()
        ax.text(
            point.x, point.y, f"{row['mad']:.3f}", fontsize=6.5, color="white",
            ha="center", va="center", fontweight="bold", zorder=3,
        )

    handles = [Patch(facecolor=c, edgecolor="white", label=cat) for cat, c in style.CONFORMITY_COLORS.items()]
    handles.append(Patch(facecolor="#f4f4f5", edgecolor="0.6", hatch="///", label="Not tested"))
    ax.legend(
        handles=handles, loc="lower left", fontsize=9, frameon=False,
        title="Conformity (MAD)", title_fontsize=9.5,
    )

    ax.set_title("Newcomb-Benford Law conformity of COVID-19 death reporting, by country")
    ax.set_axis_off()
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mad-log", default=MAD_LOG, help="Path to the country,mad log file.")
    parser.add_argument("--out", default="results/world_map", help="Output path, without extension.")
    parser.add_argument("--fmt", default="svg", choices=["svg", "png"])
    args = parser.parse_args()

    mad_by_country = load_mad_values(args.mad_log)
    fig = build_choropleth(mad_by_country)
    directory, name = os.path.split(args.out)
    path = plotter.save_figure(fig, name, directory=directory or ".", fmt=args.fmt)
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
