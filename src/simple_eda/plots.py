"""Two styled matplotlib charts plus a shared house style. Each takes a
DataFrame and returns a Figure (never shows, never mutates). Signatures are
kept small (the "design the smallest API" rule); color carries meaning and a
single gold accent marks the highlighted category. Titles derive from the
column names, so there are no title/label parameters to pass."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as pe
from matplotlib.ticker import FuncFormatter
import pandas as pd

SURFACE, INK, SECONDARY, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE = "#e1e0d9", "#c3c2b7"
GREEN, GOLD = "#1f6f54", "#f2a900"                       # recessive base + one accent
RAMP = mcolors.LinearSegmentedColormap.from_list("g", ["#cfe8dc", GREEN])  # magnitude
QUAL = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7", "#e34948", "#eda100"]   # categories


def _k(x, _p=None):
    a = abs(x)
    return f"{x/1e6:.0f}M" if a >= 1e6 else f"{x/1e3:.0f}k" if a >= 1e3 else f"{x:.0f}"


def _style(ax):
    ax.set_facecolor(SURFACE); ax.figure.set_facecolor(SURFACE); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(BASELINE)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)


def radial_bar(df, label_col, value_col, highlight=None):
    """Circular bar chart: bar length AND color both encode value; the
    highlighted category is gold. Centered and symmetric in the figure."""
    d = df[[label_col, value_col]].dropna().sort_values(value_col, ascending=False)
    labels = d[label_col].astype(str).tolist()
    values = d[value_col].to_numpy(float)
    n = len(values); vmax = values.max()
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    width = 2 * np.pi / n * 0.9
    colors = [GOLD if labels[i] == str(highlight) else RAMP(values[i] / vmax) for i in range(n)]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    fig.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
    ax.set_position([0.13, 0.13, 0.74, 0.74])           # centered square, equal margins
    ax.bar(ang, values, width=width, color=colors, edgecolor=SURFACE, linewidth=1.5)
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
    ax.set_ylim(-vmax * 0.5, vmax * 1.32)               # hollow center + room for a label ring
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines["polar"].set_visible(False); ax.grid(False)
    for i in range(n):                                  # labels on one outer ring (tidy, symmetric)
        deg = np.degrees(ang[i]); rot, ha = deg, "left"
        if 90 < deg < 270:
            rot, ha = deg + 180, "right"
        ax.text(ang[i], vmax * 1.12, f"{labels[i]}  {values[i]:,.0f}",
                rotation=rot, rotation_mode="anchor", ha=ha, va="center", fontsize=9,
                color=INK if labels[i] == str(highlight) else SECONDARY,
                weight="bold" if labels[i] == str(highlight) else "normal")
    if str(highlight) in labels:                        # headline the story in the hub
        hv = values[labels.index(str(highlight))]
        ax.text(0.5, 0.54, str(highlight), transform=ax.transAxes, ha="center",
                va="center", color=GOLD, fontsize=13, weight="bold")
        ax.text(0.5, 0.45, f"{hv:,.0f}", transform=ax.transAxes, ha="center",
                va="center", color=SECONDARY, fontsize=10)
    else:
        ax.text(0.5, 0.5, value_col, transform=ax.transAxes, ha="center",
                va="center", color=MUTED, fontsize=11)
    fig.suptitle(f"{value_col} by {label_col}", y=0.95, fontsize=15, weight="bold", color=INK)
    return fig


def bubble(df, x, y, size_col, label_col=None, color_col=None, highlight=None):
    """Bubble chart: bubble AREA = size_col; color = color_col category, or the
    gold accent for the highlighted label. Bubbles are large enough to read and
    the plot is centered with symmetric margins."""
    d = df.dropna(subset=[x, y, size_col]).copy()
    s = d[size_col].to_numpy(float)
    sizes = 800 + (s - s.min()) / (np.ptp(s) or 1) * (4600 - 800)   # never too small

    fig, ax = plt.subplots(figsize=(9, 7.5)); _style(ax)
    ax.axvline(d[x].median(), color=BASELINE, lw=1, ls=(0, (4, 4)), zorder=1)   # market-map
    ax.axhline(d[y].median(), color=BASELINE, lw=1, ls=(0, (4, 4)), zorder=1)   # 2x2 quadrants
    labels = d[label_col].astype(str) if label_col else pd.Series([""] * len(d), index=d.index)
    if color_col:
        cats = list(dict.fromkeys(d[color_col]))
        cmap = {c: QUAL[i % len(QUAL)] for i, c in enumerate(cats)}
        colors = [cmap[c] for c in d[color_col]]
    else:
        colors = [GOLD if lab == str(highlight) else GREEN for lab in labels]
    ax.scatter(d[x], d[y], s=sizes, c=colors, alpha=0.85, edgecolor=SURFACE, linewidth=1.5, zorder=3)
    halo = [pe.withStroke(linewidth=3, foreground=SURFACE)]   # keep labels legible on any fill
    for xi, yi, lab, sz in zip(d[x], d[y], labels, sizes):
        off = (sz / np.pi) ** 0.5 + 6                         # sit just above each bubble
        ax.annotate(lab, (xi, yi), xytext=(0, off), textcoords="offset points",
                    ha="center", va="bottom", fontsize=10, weight="bold",
                    color=INK, zorder=6, path_effects=halo)
    ax.grid(True, color=GRID, linewidth=1)
    ax.xaxis.set_major_formatter(FuncFormatter(_k)); ax.yaxis.set_major_formatter(FuncFormatter(_k))
    ax.margins(0.18)                                     # symmetric breathing room
    if color_col:
        for c in cats:
            ax.scatter([], [], c=cmap[c], s=120, edgecolor=SURFACE, label=str(c))
        ax.legend(frameon=False, fontsize=9, labelcolor=SECONDARY)
    ax.set_title(f"{y} vs {x}", loc="center", color=INK, fontsize=14, pad=12)
    ax.set_xlabel(x, color=SECONDARY); ax.set_ylabel(y, color=SECONDARY)
    fig.tight_layout(); return fig
