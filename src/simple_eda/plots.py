"""Plotting helpers.

Each function takes a DataFrame, applies one deliberate house style, and
*returns* a matplotlib ``Figure`` (it never calls ``show`` and never modifies
the DataFrame). The style is one cohesive system: an off-white surface,
recessive chrome (hairline grid, muted labels, no top/right spines), a single
colorblind-safe blue for one-series charts, and a blue-to-red diverging ramp
with a neutral-gray midpoint for signed values.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

# --- house palette (validated, colorblind-safe) -------------------------------
SURFACE = "#fcfcfb"   # soft off-white, easier on the eye than stark white
INK = "#0b0b0b"       # primary text
SECONDARY = "#52514e"  # axis titles
MUTED = "#898781"     # tick labels
GRID = "#e1e0d9"      # hairline gridlines
BASELINE = "#c3c2b7"  # the one axis line we keep
BLUE = "#2a78d6"      # single lead hue for one-series charts
# diverging poles for signed data: blue (low) <-> gray (zero) <-> red (high)
DIVERGING = mcolors.LinearSegmentedColormap.from_list(
    "eda_diverging", ["#256abf", "#f0efec", "#d03b3b"]
)


def _style(ax) -> None:
    """Apply the recessive house chrome to one axes: no clutter, data first."""
    ax.set_facecolor(SURFACE)
    ax.figure.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(BASELINE)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.title.set_color(INK)
    ax.xaxis.label.set_color(SECONDARY)
    ax.yaxis.label.set_color(SECONDARY)


def missing_plot(df: pd.DataFrame):
    """Horizontal bar chart of missing-value counts per column, highest on top."""
    counts = df.isna().sum().sort_values()
    counts = counts[counts > 0]

    fig, ax = plt.subplots(figsize=(7, max(2, 0.45 * len(counts) + 1)))
    _style(ax)

    if counts.empty:
        ax.text(0.5, 0.5, "No missing values", ha="center", va="center",
                color=MUTED, fontsize=12, transform=ax.transAxes)
        ax.set_xticks([])
        ax.set_yticks([])
        return fig

    ax.barh(counts.index, counts.values, color=BLUE, height=0.65)
    ax.xaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    # direct labels: the count sits right at the end of each bar
    for y, v in enumerate(counts.values):
        ax.text(v, y, f" {int(v)}", va="center", ha="left",
                color=SECONDARY, fontsize=9)
    ax.set_title("Missing values per column", loc="left", fontsize=13, pad=12)
    ax.set_xlabel("count")
    fig.tight_layout()
    return fig


def histogram(df: pd.DataFrame, column: str, bins: int = 20):
    """Distribution of one numeric column as a single-hue histogram."""
    series = df[column].dropna()

    fig, ax = plt.subplots(figsize=(7, 4))
    _style(ax)
    ax.hist(series, bins=bins, color=BLUE, edgecolor=SURFACE, linewidth=1)
    ax.yaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.set_title(f"Distribution of {column}", loc="left", fontsize=13, pad=12)
    ax.set_xlabel(column)
    ax.set_ylabel("frequency")
    fig.tight_layout()
    return fig


def correlation_heatmap(df: pd.DataFrame):
    """Heatmap of numeric-column correlations on a diverging blue-red ramp.

    Correlation is signed (-1 to +1), so the color has polarity: blue pulls one
    way, red the other, and a neutral gray marks zero. The scale is locked to
    [-1, 1] so gray always means "no correlation."
    """
    corr = df.select_dtypes(include="number").corr()
    n = len(corr)

    fig, ax = plt.subplots(figsize=(1 + 0.7 * n, 1 + 0.7 * n))
    ax.set_facecolor(SURFACE)
    fig.set_facecolor(SURFACE)
    im = ax.imshow(corr.values, cmap=DIVERGING, vmin=-1, vmax=1)

    ax.set_xticks(range(n), corr.columns, rotation=45, ha="right",
                  color=MUTED, fontsize=9)
    ax.set_yticks(range(n), corr.index, color=MUTED, fontsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)

    # direct value labels; ink flips to white where the cell is dark
    for i in range(n):
        for j in range(n):
            val = corr.values[i, j]
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8,
                    color=INK if abs(val) < 0.6 else SURFACE)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(colors=MUTED, length=0, labelsize=8)
    ax.set_title("Correlation", loc="left", fontsize=13, pad=12, color=INK)
    fig.tight_layout()
    return fig
