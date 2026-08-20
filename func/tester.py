"""Statistical tests for comparing an observed digit distribution against NBL."""

import numpy as np

import func.benford as benford

# Nigrini's MAD conformity thresholds for the first-digit test (Drake & Nigrini, 2000).
MAD_CONFORMITY_THRESHOLDS = (
    (0.006, "Close conformity"),
    (0.012, "Acceptable conformity"),
    (0.015, "Marginal conformity"),
    (float("inf"), "Nonconformity"),
)


def standard_deviations(sample_size):
    p = benford.EXPECTED_FREQUENCIES
    return np.sqrt(p * (1 - p) / sample_size)


def tolerance_bounds(sample_size):
    """
    95% (Z=1.96) tolerance bounds around the expected Benford frequencies, per
    digit, exactly as specified in the paper's Equations 2-3 (after
    Henselmann et al., 2012): the continuity correction 1/(2n) is subtracted
    on the lower bound and added on the upper bound, which makes the band
    asymmetric rather than uniformly widened. Kept as published rather than
    "corrected" to the symmetric textbook form -- flagged separately for the
    authors to confirm against their source.
    """
    p = benford.EXPECTED_FREQUENCIES
    std = standard_deviations(sample_size)
    continuity = 1 / (2 * sample_size)
    lower = p - (1.96 * std - continuity)
    upper = p + (1.96 * std + continuity)
    return lower, upper


def mean_absolute_deviation(observed_frequencies):
    """Mean absolute deviation between observed and expected digit frequencies."""
    return float(np.mean(np.abs(benford.EXPECTED_FREQUENCIES - observed_frequencies)))


def mad_conformity_category(mad):
    """Label an MAD value using Nigrini's first-digit conformity thresholds."""
    for threshold, label in MAD_CONFORMITY_THRESHOLDS:
        if mad < threshold:
            return label
    return MAD_CONFORMITY_THRESHOLDS[-1][1]
