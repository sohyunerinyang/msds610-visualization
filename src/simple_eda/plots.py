"""Styled matplotlib charts. Each takes a DataFrame and returns a Figure
(never shows, never mutates). One idea: color carries meaning and the single
gold accent marks the value that matters. title / subtitle / source= follow
McCandless's lenses (interestingness, function, form, integrity)."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter
import pandas as pd

SURFACE, INK, SECONDARY, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE = "#e1e0d9", "#c3c2b7"
GREEN, GOLD = "#1f6f54", "#f2a900"   # recessive base + the one accent (school colors)
RAMP = mcolors.LinearSegmentedColormap.from_list("g", ["#cfe8dc", GREEN])  # magnitude
# a small colorblind-safe qualitative set for category coloring (blue/orange/aqua/violet/red)
QUAL = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7", "#e34948", "#eda100"]


def _k(x, _p=None):
    a = abs(x)
    return f"{x/1e6:.0f}M" if a >= 1e6 else f"{x/1e3:.0f}k" if a >= 1e3 else f"{x:.0f}"


def _style(ax):
    ax.set_facecolor(SURFACE); ax.figure.set_facecolor(SURFACE); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(BASELINE)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)


def _frame(fig, ax, title, subtitle=None, source=None):
    """Title + optional takeaway subtitle + optional source footer (integrity)."""
    ax.set_title(title, loc="left", color=INK, fontsize=14, pad=26 if subtitle else 12)
    if subtitle:
        ax.annotate(subtitle, (0, 1), (0, 8), "axes fraction", "offset points",
                    ha="left", va="bottom", color=SECONDARY, fontsize=10)
    if source:
        fig.text(0.01, 0.005, source, color=MUTED, fontsize=8)


def ranked_bar(df, label_col, value_col, top=None, title=None, subtitle=None,
               xlabel=None, source=None):
    """Horizontal ranked bar; the #1 value is gold, the rest recede."""
    d = df[[label_col, value_col]].dropna().sort_values(value_col)
    if top: d = d.tail(top)
    labels, values = d[label_col].astype(str).tolist(), d[value_col].tolist()
    colors = [GREEN] * len(values); colors[-1] = GOLD
    fig, ax = plt.subplots(figsize=(9, max(2.5, 0.5 * len(values) + 1.2))); _style(ax)
    ax.barh(labels, values, color=colors, height=0.68)
    ax.xaxis.grid(True, color=GRID, linewidth=1)
    ax.xaxis.set_major_formatter(FuncFormatter(_k))
    for y, v in enumerate(values):
        ax.text(v + max(values) * 0.01, y, f"{v:,.0f}", va="center", color=SECONDARY, fontsize=9)
    ax.margins(x=0.13)
    _frame(fig, ax, title or f"{value_col} by {label_col}", subtitle, source)
    ax.set_xlabel(xlabel or value_col, color=SECONDARY)
    fig.tight_layout(); return fig


def radial_bar(df, label_col, value_col, highlight=None, title=None,
               subtitle=None, source=None):
    """Circular bar chart: one bar per category, length AND color = magnitude.
    A narrative, high-impact take on a ranking. The gold bar is `highlight`."""
    d = df[[label_col, value_col]].dropna().sort_values(value_col, ascending=False)
    labels, values = d[label_col].astype(str).tolist(), d[value_col].to_numpy(float)
    n = len(values); vmax = values.max()
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    width = 2 * np.pi / n * 0.9
    colors = [GOLD if labels[i] == highlight else RAMP(values[i] / vmax) for i in range(n)]

    fig, ax = plt.subplots(figsize=(8.5, 8.5), subplot_kw={"projection": "polar"})
    fig.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
    ax.bar(ang, values, width=width, color=colors, edgecolor=SURFACE, linewidth=1.5, zorder=3)
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
    ax.set_ylim(-vmax * 0.45, vmax * 1.02)  # hollow center
    ax.set_xticks([]); ax.set_yticks([]); ax.spines["polar"].set_visible(False); ax.grid(False)
    for i in range(n):
        deg = np.degrees(ang[i]); rot = deg
        align = "left"
        if 90 < deg < 270:
            rot = deg + 180; align = "right"
        ax.text(ang[i], values[i] + vmax * 0.04, f"{labels[i]}  {values[i]:,.0f}",
                rotation=rot, rotation_mode="anchor", ha=align, va="center",
                fontsize=8.5, color=INK if labels[i] == highlight else SECONDARY,
                weight="bold" if labels[i] == highlight else "normal")
    if title:
        fig.text(0.5, 0.94, title, ha="center", color=INK, fontsize=15, weight="bold")
    if subtitle:
        fig.text(0.5, 0.905, subtitle, ha="center", color=SECONDARY, fontsize=10)
    if source:
        fig.text(0.01, 0.01, source, color=MUTED, fontsize=8)
    return fig


def bubble(df, x, y, size_col, label_col=None, color_col=None, highlight=None,
           logx=False, vline=None, hline=None, title=None, subtitle=None,
           xlabel=None, ylabel=None, source=None, size_range=(80, 2000)):
    """Bubble "market map": x vs y, bubble area = size_col, color = color_col
    (a category) or the gold accent for `highlight`. Reusable for any data."""
    d = df.dropna(subset=[x, y, size_col]).copy()
    s = d[size_col].to_numpy(float)
    sizes = size_range[0] + (s - s.min()) / (np.ptp(s) or 1) * (size_range[1] - size_range[0])

    fig, ax = plt.subplots(figsize=(10, 6.5)); _style(ax)
    if vline is not None: ax.axvline(vline, color=BASELINE, lw=1, ls=(0, (4, 4)))
    if hline is not None: ax.axhline(hline, color=BASELINE, lw=1, ls=(0, (4, 4)))

    if color_col:
        cats = list(dict.fromkeys(d[color_col]))
        cmap = {c: QUAL[i % len(QUAL)] for i, c in enumerate(cats)}
        colors = [cmap[c] for c in d[color_col]]
    else:
        colors = [GOLD if (label_col and r == highlight) else GREEN
                  for r in (d[label_col] if label_col else [None] * len(d))]
    ax.scatter(d[x], d[y], s=sizes, c=colors, alpha=0.82,
               edgecolor=SURFACE, linewidth=1.5, zorder=3)
    if label_col:
        for _, r in d.iterrows():
            ax.annotate(str(r[label_col]), (r[x], r[y]), xytext=(0, 0),
                        textcoords="offset points", ha="center", va="center",
                        fontsize=8, color=INK, zorder=5)
    if logx: ax.set_xscale("log")
    ax.grid(True, color=GRID, linewidth=1)
    ax.yaxis.set_major_formatter(FuncFormatter(_k))
    if not logx: ax.xaxis.set_major_formatter(FuncFormatter(_k))
    ax.margins(0.16)
    if color_col:  # a legend only when color encodes a category
        for c in cats:
            ax.scatter([], [], c=cmap[c], s=90, edgecolor=SURFACE, label=str(c))
        ax.legend(frameon=False, fontsize=9, labelcolor=SECONDARY, loc="best")
    _frame(fig, ax, title or f"{y} vs {x}", subtitle, source)
    ax.set_xlabel((xlabel or x) + (" (log scale)" if logx else ""), color=SECONDARY)
    ax.set_ylabel(ylabel or y, color=SECONDARY)
    fig.tight_layout(); return fig
