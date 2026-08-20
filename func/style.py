"""Shared visual language for every chart in this project.

Academic register: neutral (not "finding") titles, mandatory labeled
uncertainty, and a colorblind-safe palette that survives grayscale.
Findings belong in the surrounding prose/caption, not baked into the chart.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Okabe & Ito (2008) -- the standard colorblind-safe categorical palette.
INK = "#1f2430"
MUTED = "#6b7280"
GRID = "#e5e7eb"
BACKGROUND = "#ffffff"

EXPECTED = "#595959"       # Benford reference curve: neutral, never a data color
OBSERVED = "#0072B2"       # Okabe-Ito blue: observed frequency bars
BAND = "#0072B2"           # tolerance-interval fill, same hue as OBSERVED

# Nigrini's four MAD conformity categories, in one fixed color per category,
# reused everywhere (country badges, ranking chart, world map) so the same
# color always means the same thing across the whole project.
CONFORMITY_COLORS = {
    "Close conformity": "#009E73",       # Okabe-Ito green
    "Acceptable conformity": "#0072B2",  # Okabe-Ito blue
    "Marginal conformity": "#E69F00",    # Okabe-Ito orange
    "Nonconformity": "#D55E00",          # Okabe-Ito vermillion
}
CONFORMITY_ORDER = list(CONFORMITY_COLORS)

FIGURE_DPI = 200


def apply():
    """Apply a shared, colorblind-safe academic-register theme to every chart."""
    plt.rcParams.update(
        {
            "figure.facecolor": BACKGROUND,
            "axes.facecolor": BACKGROUND,
            "savefig.facecolor": BACKGROUND,
            "savefig.dpi": FIGURE_DPI,
            "figure.dpi": 110,
            "font.family": "sans-serif",
            "font.size": 11,
            "text.color": INK,
            "axes.edgecolor": MUTED,
            "axes.labelcolor": INK,
            "axes.titlecolor": INK,
            "axes.titleweight": "bold",
            "axes.titlesize": 12.5,
            "axes.titlelocation": "left",
            "axes.labelsize": 10.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.9,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelsize": 9.5,
            "ytick.labelsize": 9.5,
            "grid.color": GRID,
            "grid.linewidth": 0.9,
            "legend.frameon": False,
            "legend.fontsize": 9.5,
        }
    )


def percent_axis(ax, decimals=0):
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=decimals))


def conformity_badge(ax, mad, category, sample_size):
    """Draw the MAD / conformity-category / sample-size badge used on every chart.

    Sample size is reported directly on the figure (academic convention) so
    the image is interpretable if it's ever seen apart from its caption.
    """
    color = CONFORMITY_COLORS.get(category, MUTED)
    ax.text(
        0.985,
        0.97,
        f"MAD {mad:.4f} — {category}\nn = {sample_size:,}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        color=color,
        bbox={
            "boxstyle": "round,pad=0.4",
            "facecolor": color + "1a",
            "edgecolor": color,
            "linewidth": 0.8,
        },
    )
