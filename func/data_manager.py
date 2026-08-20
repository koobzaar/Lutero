"""Death-count datasets for Newcomb-Benford Law analysis, backed by pandas."""

import pandas as pd

import func.data_loader as data_loader

# JHU used these as "Country/Region" values for isolated case clusters, not
# actual countries; left in, they'd produce nonsense Benford plots under --all.
NON_COUNTRY_ENTRIES = {
    "Diamond Princess",
    "MS Zaandam",
    "Summer Olympics 2020",
    "Winter Olympics 2022",
}


class JHUDeaths:
    """Cumulative COVID-19 deaths by country, from the JHU time-series CSV.

    Countries reported as multiple sub-national rows (e.g. Canada, Australia,
    China) are summed into a single country-level total; the original
    dict-indexing approach silently dropped these countries entirely and
    leaked their provinces into the country list instead.
    """

    def __init__(self, data_path):
        raw = data_loader.load_jhu(data_path)
        raw = raw[~raw["Country/Region"].isin(NON_COUNTRY_ENTRIES)]
        date_columns = raw.columns[4:]
        totals = raw.groupby("Country/Region")[date_columns].sum()
        self._daily_totals = totals.apply(pd.to_numeric, errors="coerce")

    def available_countries(self):
        return sorted(self._daily_totals.index)

    def death_variation(self, country):
        """Day-over-day change in cumulative deaths for a country."""
        if country not in self._daily_totals.index:
            raise KeyError(country)
        return self._daily_totals.loc[country].diff().dropna().astype(int).tolist()


def _positive_variation(series):
    values = pd.to_numeric(series, errors="coerce")
    return values[values >= 0].dropna().astype(int).tolist()


def cvi_death_variation(data_path):
    """Daily death variation reported by Brazil's press-vehicle consortium (CVI)."""
    df = data_loader.load_cvi(data_path)
    return _positive_variation(df["variacao_absoluta_sobre_o_dia_anterior"])


def brazil_ms_death_variation(data_path):
    """Daily death variation reported by Brazil's Ministry of Health, national total."""
    df = data_loader.load_brazil_ministerio_saude(data_path)
    df = df[df["regiao"] == "Brasil"]
    return _positive_variation(df["obitosNovos"])


def usa_death_variation(data_path):
    """Weekly death counts reported by the CDC for the United States."""
    df = data_loader.load_usa(data_path)
    return _positive_variation(df["Weekly Deaths"])
