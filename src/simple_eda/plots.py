"""Plotting helpers.

Each function takes a DataFrame, applies one deliberate house style, and
*returns* a matplotlib ``Figure`` (it never calls ``show`` and never modifies
the DataFrame).

Design goals follow McCandless's four lenses for good information design:
  - Form         one recessive base color, one gold accent on the key value;
                 hairline chrome, direct labels, "k" number formatting.
  - Function     human-readable titles/axes, subtitles that state the takeaway.
  - Integrity    every chart carries an optional source/date footer, so the
                 numbers are attributable.
  - Interestingness  the caller supplies the question (title) and the "so what"
                 (subtitle); the accent color answers it at a glance.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter
import pandas as pd

# --- house palette ------------------------------------------------------------
SURFACE = "#fcfcfb"    # soft off-white, easier on the eye than stark white
INK = "#0b0b0b"        # primary text
SECONDARY = "#52514e"  # axis titles / value labels
MUTED = "#898781"      # tick labels / source footer
GRID = "#e1e0d9"       # hairline gridlines
BASELINE = "#c3c2b7"   # the one axis line we keep
GREEN = "#1f6f54"      # recessive base mark (school green)
GOLD = "#f2a900"       # the one accent, reserved for the key value (school gold)
# green and gold differ strongly in BOTH hue and lightness, so the highlight
# survives colorblindness (lightness carries it when hue washes out).
DIVERGING = mcolors.LinearSegmentedColormap.from_list(
    "eda_diverging", ["#256abf", "#f0efec", "#d03b3b"]
)


def _thousands(x, _pos=None):
    """Axis tick formatter: 25000 -> '25k', 1500000 -> '2M'."""
    ax = abs(x)
    if ax >= 1_000_000:
        return f"{x / 1_000_000:.0f}M"
    if ax >= 1_000:
        return f"{x / 1_000:.0f}k"
    return f"{x:.0f}"


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


def _titles(ax, title, subtitle):
    """Left-aligned title with an optional subtitle (the takeaway) beneath it."""
    ax.set_title(title, loc="left", fontsize=14, pad=26 if subtitle else 12)
    if subtitle:
        ax.annotate(subtitle, xy=(0, 1), xytext=(0, 8), xycoords="axes fraction",
                    textcoords="offset points", ha="left", va="bottom",
                    color=SECONDARY, fontsize=10)


def _footer(fig, source):
    """Muted source/date line at the bottom-left — attribution = integrity."""
    if source:
        fig.text(0.01, 0.005, source, ha="left", va="bottom",
                 color=MUTED, fontsize=8)


def missing_plot(df: pd.DataFrame, source=None):
    """Horizontal bar of missing-value counts per column, highest on top."""
    counts = df.isna().sum().sort_values()
    counts = counts[counts > 0]

    fig, ax = plt.subplots(figsize=(7, max(2, 0.45 * len(counts) + 1)))
    _style(ax)
    if counts.empty:
        ax.text(0.5, 0.5, "No missing values", ha="center", va="center",
                color=MUTED, fontsize=12, transform=ax.transAxes)
        ax.set_xticks([]); ax.set_yticks([])
        return fig

    ax.barh(counts.index, counts.values, color=GREEN, height=0.65)
    ax.xaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for y, v in enumerate(counts.values):
        ax.text(v, y, f" {int(v)}", va="center", ha="left",
                color=SECONDARY, fontsize=9)
    ax.set_title("Missing values per column", loc="left", fontsize=13, pad=12)
    ax.set_xlabel("count")
    _footer(fig, source)
    fig.tight_layout()
    return fig


def histogram(df: pd.DataFrame, column: str, bins: int = 24, highlight="median",
              title=None, subtitle=None, xlabel=None, source=None):
    """Distribution of one numeric column, with the median's bin marked in gold.

    ``highlight`` may be ``"median"``, ``"mean"``, a number, or ``None``.
    """
    series = df[column].dropna()

    fig, ax = plt.subplots(figsize=(9, 5))
    _style(ax)
    counts, edges, patches = ax.hist(series, bins=bins, color=GREEN,
                                     edgecolor=SURFACE, linewidth=1.2)
    ax.yaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(FuncFormatter(_thousands))

    marker = {"median": series.median(), "mean": series.mean()}.get(highlight,
                                                                     highlight)
    if marker is not None:
        idx = int(np.clip(np.digitize(marker, edges) - 1, 0, len(patches) - 1))
        patches[idx].set_facecolor(GOLD)
        label = (highlight if isinstance(highlight, str) else "value").upper()
        ax.text(patches[idx].get_x() + patches[idx].get_width() / 2,
                counts[idx] / 2, f"{label} {marker:,.0f}", rotation=90,
                ha="center", va="center", color=INK, fontsize=10, weight="bold")

    _titles(ax, title or f"Distribution of {column}", subtitle)
    ax.set_xlabel(xlabel or column)
    ax.set_ylabel("frequency")
    _footer(fig, source)
    fig.tight_layout()
    return fig


def ranked_bar(df: pd.DataFrame, label_col: str, value_col: str, top=None,
               title=None, subtitle=None, xlabel=None, source=None):
    """Horizontal ranked bar; the #1 value is accented in gold, rest recessive."""
    data = df[[label_col, value_col]].dropna().sort_values(value_col)
    if top:
        data = data.tail(top)
    labels = data[label_col].astype(str).tolist()
    values = data[value_col].tolist()
    colors = [GREEN] * len(values)
    colors[-1] = GOLD  # last (largest, top of chart) is the leader

    fig, ax = plt.subplots(figsize=(9, max(2.5, 0.5 * len(values) + 1.2)))
    _style(ax)
    ax.barh(labels, values, color=colors, height=0.68)
    ax.xaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(FuncFormatter(_thousands))
    pad = max(values) * 0.01
    for y, v in enumerate(values):
        ax.text(v + pad, y, f"{v:,.0f}", va="center", ha="left",
                color=SECONDARY, fontsize=9)
    ax.margins(x=0.13)
    _titles(ax, title or f"{value_col} by {label_col}", subtitle)
    ax.set_xlabel(xlabel or value_col)
    _footer(fig, source)
    fig.tight_layout()
    return fig


def scatter(df: pd.DataFrame, x: str, y: str, label_col=None, highlight=None,
            logx=False, title=None, subtitle=None, xlabel=None, ylabel=None,
            vline=None, hline=None, source=None):
    """Scatter of two numeric columns; ``highlight`` (a label) is drawn in gold.

    Handy as a "traction quadrant": installed base on x, growth on y. Pass
    ``vline`` / ``hline`` (e.g. the medians) to split the plane into quadrants.
    """
    data = df.dropna(subset=[x, y])
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    _style(ax)

    # quadrant reference lines (drawn first, so they sit behind the marks)
    if vline is not None:
        ax.axvline(vline, color=BASELINE, linewidth=1, linestyle=(0, (4, 4)))
    if hline is not None:
        ax.axhline(hline, color=BASELINE, linewidth=1, linestyle=(0, (4, 4)))

    hi_mask = (data[label_col] == highlight) if (label_col and highlight) \
        else pd.Series(False, index=data.index)
    ax.scatter(data.loc[~hi_mask, x], data.loc[~hi_mask, y], s=130,
               color=GREEN, edgecolor=SURFACE, linewidth=1.5, zorder=3)
    if hi_mask.any():
        ax.scatter(data.loc[hi_mask, x], data.loc[hi_mask, y], s=240,
                   color=GOLD, edgecolor=SURFACE, linewidth=1.5, zorder=4)

    if label_col:
        for _, r in data.iterrows():
            is_hi = r[label_col] == highlight
            ax.annotate(str(r[label_col]), (r[x], r[y]),
                        xytext=(10, 7), textcoords="offset points",
                        color=INK if is_hi else SECONDARY, fontsize=9,
                        weight="bold" if is_hi else "normal", zorder=5)

    if logx:
        ax.set_xscale("log")
    ax.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(FuncFormatter(_thousands))
    if not logx:
        ax.xaxis.set_major_formatter(FuncFormatter(_thousands))
    ax.margins(0.14)
    _titles(ax, title or f"{y} vs {x}", subtitle)
    ax.set_xlabel((xlabel or x) + (" (log scale)" if logx else ""))
    ax.set_ylabel(ylabel or y)
    _footer(fig, source)
    fig.tight_layout()
    return fig


def correlation_heatmap(df: pd.DataFrame, title=None, source=None):
    """Heatmap of numeric correlations on a diverging blue-red ramp.

    Correlation is signed (-1 to +1), so the color has polarity: blue pulls one
    way, red the other, and neutral gray marks zero. The scale is locked to
    [-1, 1] so gray always means "no correlation."
    """
    corr = df.select_dtypes(include="number").corr()
    n = len(corr)

    fig, ax = plt.subplots(figsize=(1 + 0.75 * n, 1 + 0.75 * n))
    ax.set_facecolor(SURFACE)
    fig.set_facecolor(SURFACE)
    im = ax.imshow(corr.values, cmap=DIVERGING, vmin=-1, vmax=1)

    ax.set_xticks(range(n), corr.columns, rotation=45, ha="right",
                  color=MUTED, fontsize=9)
    ax.set_yticks(range(n), corr.index, color=MUTED, fontsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)
    for i in range(n):
        for j in range(n):
            val = corr.values[i, j]
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8,
                    color=INK if abs(val) < 0.6 else SURFACE)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(colors=MUTED, length=0, labelsize=8)
    ax.set_title(title or "Correlation", loc="left", fontsize=14, pad=12,
                 color=INK)
    _footer(fig, source)
    fig.tight_layout()
    return fig
