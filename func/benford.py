"""Newcomb-Benford Law computations for first-significant-digit distributions."""

import numpy as np

DIGITS = np.arange(1, 10)
EXPECTED_FREQUENCIES = np.log10(1 + 1 / DIGITS)


def first_significant_digits(values):
    """Leading (first) significant digit of every nonzero value, as an int array."""
    values = np.abs(np.asarray(values, dtype=np.int64))
    values = values[values != 0]
    if values.size == 0:
        return values
    magnitude = np.floor(np.log10(values)).astype(np.int64)
    return values // (10 ** magnitude)


def digit_frequencies(values):
    """
    Observed first-digit relative frequencies, indexed by digit (frequencies[0] is
    digit 1, frequencies[8] is digit 9) so they line up positionally with
    EXPECTED_FREQUENCIES and with each other -- this ordering is load-bearing for
    every caller that zips the result against DIGITS.

    Returns None when at least one digit never occurs in the sample, since NBL
    conformity is undefined without observations across the full digit range.
    """
    first_digits = first_significant_digits(values)
    if first_digits.size == 0:
        return None
    counts = np.bincount(first_digits, minlength=10)[1:10]
    if np.any(counts == 0):
        return None
    return counts / first_digits.size
