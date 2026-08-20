"""Rendering of Benford's Law results: distribution, deviation, comparison, and ranking."""

import math
import os
import string
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

import func.benford as benford
import func.style as style
import func.tester as tester


@dataclass
class BenfordResult:
    country: str
    frequencies: "np.ndarray"
    mad: float
    conformity: str
    sample_size: int


def compute_benford_result(country_name, death_variance):
    """
    Compute the first-digit distribution and NBL conformity stats for a
    country's death-variation series. Returns None when the sample doesn't
    contain every leading digit, matching the original tool's behaviour of
    silently skipping countries too sparse to test.
    """
    frequencies = benford.digit_frequencies(death_variance)
    if frequencies is None:
        return None

    sample_size = int(benford.first_significant_digits(death_variance).size)
    mad = tester.mean_absolute_deviation(frequencies)
    category = tester.mad_conformity_category(mad)
    return BenfordResult(country_name, frequencies, mad, category, sample_size)


def _draw_distribution_panel(ax, result):
    """Observed frequency bars vs. the expected Benford curve and its tolerance interval."""
    lower, upper = tester.tolerance_bounds(result.sample_size)

    ax.fill_between(benford.DIGITS, lower, upper, color=style.BAND, alpha=0.12, zorder=1)
    ax.bar(benford.DIGITS, result.frequencies, color=style.OBSERVED, width=0.55, zorder=3)
    ax.plot(
        benford.DIGITS, benford.EXPECTED_FREQUENCIES, color=style.EXPECTED,
        marker="o", markersize=4, lw=1.6, ls="--", zorder=4,
    )

    ax.set_xticks(benford.DIGITS)
    ax.set_ylabel("Frequency")
    style.percent_axis(ax)
    ax.set_axisbelow(True)
    ax.grid(axis="y", zorder=0)
    ax.set_title(result.country)
    style.conformity_badge(ax, result.mad, result.conformity, result.sample_size)


def _draw_deviation_panel(ax, result):
    """
    Observed-minus-expected deviation per digit (percentage points), with the
    95% tolerance interval re-centered on zero so bars that poke outside it
    are visually -- not just chromatically -- flagged as out of tolerance.
    """
    lower, upper = tester.tolerance_bounds(result.sample_size)
    expected = benford.EXPECTED_FREQUENCIES
    deviation = (np.asarray(result.frequencies) - expected) * 100
    lower_dev = (lower - expected) * 100
    upper_dev = (upper - expected) * 100

    ax.fill_between(benford.DIGITS, lower_dev, upper_dev, color=style.BAND, alpha=0.12, zorder=1)
    ax.axhline(0, color=style.MUTED, lw=0.9, zorder=2)

    colors = [
        style.OBSERVED if lo <= d <= hi else style.CONFORMITY_COLORS["Nonconformity"]
        for d, lo, hi in zip(deviation, lower_dev, upper_dev)
    ]
    ax.bar(benford.DIGITS, deviation, color=colors, width=0.55, zorder=3)

    ax.set_xticks(benford.DIGITS)
    ax.set_xlabel("Leading digit")
    ax.set_ylabel("Deviation (pp)")
    ax.set_axisbelow(True)
    ax.grid(axis="y", zorder=0)


def _distribution_legend_handles():
    return [
        Patch(facecolor=style.OBSERVED, label="Observed"),
        plt.Line2D([0], [0], color=style.EXPECTED, ls="--", marker="o", markersize=4, label="Benford's Law"),
        Patch(facecolor=style.BAND, alpha=0.25, label="95% tolerance interval (Z-test, Eq. 2-3)"),
    ]


def plot_single_country_figure(result):
    """
    Standalone two-panel figure for one country: the distribution comparison
    on top, and the signed deviation from Benford's Law (with the same
    tolerance interval re-centered on zero) below it -- so the reader can
    check both the overall shape and exactly where and how far it strays.
    """
    fig, (ax_dist, ax_dev) = plt.subplots(
        2, 1, figsize=(7, 5.6), height_ratios=[3, 1.3], sharex=True, layout="constrained",
    )
    _draw_distribution_panel(ax_dist, result)
    ax_dist.tick_params(labelbottom=False)
    _draw_deviation_panel(ax_dev, result)

    handles = _distribution_legend_handles() + [
        Patch(facecolor=style.CONFORMITY_COLORS["Nonconformity"], label="Digit outside tolerance"),
    ]
    fig.legend(handles=handles, loc="outside lower center", ncol=2, fontsize=8.5)
    return fig


def plot_comparison_grid(results, ncols=3):
    """Small-multiples grid: one distribution panel per country, shared y-axis."""
    n = len(results)
    ncols = min(ncols, n)
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(
        nrows, ncols, figsize=(4.3 * ncols, 3.6 * nrows), sharey=True, squeeze=False,
        layout="constrained",
    )
    flat_axes = axes.flatten()

    for ax, result in zip(flat_axes, results):
        _draw_distribution_panel(ax, result)

    for row in axes:
        for ax in row[1:]:
            ax.set_ylabel("")

    for ax in flat_axes[n:]:
        ax.axis("off")

    fig.legend(handles=_distribution_legend_handles(), loc="outside lower center", ncol=3, fontsize=9)
    return fig


def plot_ranking(country_mads, top_n=15):
    """
    Horizontal dot plot of the most- and least-conforming countries by MAD,
    with Nigrini's conformity zones shaded as vertical reference bands and
    each dot colored and directly labeled by its own category -- a ranked
    "who's on top" view, rather than a bare sorted list.
    """
    ordered = sorted(country_mads, key=lambda cm: cm[1])
    best, worst = ordered[:top_n], ordered[-top_n:]
    rows = best + [("", None)] + worst

    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(7.5, 0.3 * len(rows) + 1), layout="constrained")

    thresholds = [0.0] + [t for t, _ in tester.MAD_CONFORMITY_THRESHOLDS[:-1]]
    xmax = max(m for _, m in country_mads) * 1.08
    bounds = thresholds + [xmax]
    for (lo, hi), category in zip(zip(bounds, bounds[1:]), style.CONFORMITY_ORDER):
        ax.axvspan(lo, hi, color=style.CONFORMITY_COLORS[category], alpha=0.06, zorder=0)

    for yi, (country, mad) in zip(y, rows):
        if mad is None:
            continue
        color = style.CONFORMITY_COLORS[tester.mad_conformity_category(mad)]
        ax.hlines(yi, 0, mad, color=color, lw=1, alpha=0.45, zorder=2)
        ax.scatter([mad], [yi], color=color, s=42, zorder=3, edgecolor="white", linewidth=0.7)
        ax.annotate(
            f"{mad:.4f}", xy=(mad, yi), xytext=(6, 0), textcoords="offset points",
            va="center", fontsize=8.5, color=style.INK,
        )

    ax.set_yticks(y)
    ax.set_yticklabels([c for c, _ in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, xmax)
    ax.set_xlabel("Mean Absolute Deviation")
    ax.spines[["left"]].set_visible(False)
    ax.tick_params(left=False)
    ax.grid(axis="x", alpha=0.3)
    ax.set_axisbelow(True)

    handles = [Patch(facecolor=c, label=cat) for cat, c in style.CONFORMITY_COLORS.items()]
    ax.legend(handles=handles, loc="upper right", fontsize=8, title="Conformity", title_fontsize=8.5)
    return fig


def sanitize_filename(name):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return "".join(c for c in name if c in valid_chars).replace(" ", "_")


def save_figure(fig, name, directory="results", fmt="svg"):
    """Save a figure under `directory`, creating it if needed. Vector (SVG) by
    default so charts embedded in the README stay crisp at any zoom."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{sanitize_filename(name)}.{fmt}")
    fig.savefig(path, bbox_inches="tight")
    return path
