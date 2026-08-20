"""Pandas-based CSV loaders, one per raw dataset shape used in this project."""

import glob

import pandas as pd


def _read_all(data_path, **read_csv_kwargs):
    files = sorted(glob.glob(f"{data_path}/*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {data_path}")
    return pd.concat((pd.read_csv(f, **read_csv_kwargs) for f in files), ignore_index=True)


def load_jhu(data_path):
    """JHU global time series: wide CSV(s), one column per date.

    A handful of rows in the raw export contain an unquoted comma inside a
    province name (e.g. "Bonaire, Sint Eustatius and Saba"), which shifts
    every field after it. Such rows are dropped with a warning rather than
    silently misread.
    """
    return _read_all(data_path, on_bad_lines="warn", engine="python")


def load_cvi(data_path):
    """Brazilian Consortium of Press Vehicles daily death counts."""
    return _read_all(data_path)


def load_brazil_ministerio_saude(data_path):
    """Brazilian Ministry of Health COVID-19 panel, semicolon-delimited."""
    return _read_all(data_path, delimiter=";")


def load_usa(data_path):
    """CDC weekly deaths export, which carries a two-line preamble before the header."""
    return _read_all(data_path, skiprows=2)
