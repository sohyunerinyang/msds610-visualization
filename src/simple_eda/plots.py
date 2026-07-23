"""Styled matplotlib charts. Each takes a DataFrame and returns a Figure
(never shows, never mutates). One idea: spend the single gold accent on the
value that matters; everything else recedes. title / subtitle / source= follow
McCandless's lenses (interestingness, function, form, integrity)."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter
import pandas as pd

SURFACE, INK, SECONDARY, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE = "#e1e0d9", "#c3c2b7"
GREEN, GOLD = "#1f6f54", "#f2a900"   # recessive base + the one accent (school colors)
# green/gold differ in hue AND lightness, so the accent survives colorblindness.
DIVERGING = mcolors.LinearSegmentedColormap.from_list("d", ["#256abf", "#f0efec", "#d03b3b"])


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


def histogram(df, column, bins=24, highlight="median", title=None, subtitle=None,
              xlabel=None, source=None):
    """Distribution of one numeric column; the median's bin is marked in gold."""
    s = df[column].dropna()
    fig, ax = plt.subplots(figsize=(9, 5)); _style(ax)
    counts, edges, bars = ax.hist(s, bins=bins, color=GREEN, edgecolor=SURFACE, linewidth=1.2)
    ax.yaxis.grid(True, color=GRID, linewidth=1)
    ax.xaxis.set_major_formatter(FuncFormatter(_k))
    m = {"median": s.median(), "mean": s.mean()}.get(highlight, highlight)
    if m is not None:
        i = int(np.clip(np.digitize(m, edges) - 1, 0, len(bars) - 1))
        bars[i].set_facecolor(GOLD)
        lbl = (highlight if isinstance(highlight, str) else "value").upper()
        ax.text(bars[i].get_x() + bars[i].get_width() / 2, counts[i] / 2,
                f"{lbl} {m:,.0f}", rotation=90, ha="center", va="center",
                color=INK, fontsize=10, weight="bold")
    _frame(fig, ax, title or f"Distribution of {column}", subtitle, source)
    ax.set_xlabel(xlabel or column, color=SECONDARY); ax.set_ylabel("frequency", color=SECONDARY)
    fig.tight_layout(); return fig


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
    pad = max(values) * 0.01
    for y, v in enumerate(values):
        ax.text(v + pad, y, f"{v:,.0f}", va="center", color=SECONDARY, fontsize=9)
    ax.margins(x=0.13)
    _frame(fig, ax, title or f"{value_col} by {label_col}", subtitle, source)
    ax.set_xlabel(xlabel or value_col, color=SECONDARY)
    fig.tight_layout(); return fig


def scatter(df, x, y, label_col=None, highlight=None, logx=False, title=None,
            subtitle=None, xlabel=None, ylabel=None, vline=None, hline=None, source=None):
    """Scatter / traction quadrant; highlight= (a label) is drawn in gold.
    Pass vline/hline (e.g. medians) to split the plane into quadrants."""
    d = df.dropna(subset=[x, y])
    fig, ax = plt.subplots(figsize=(9.5, 6.2)); _style(ax)
    if vline is not None: ax.axvline(vline, color=BASELINE, lw=1, ls=(0, (4, 4)))
    if hline is not None: ax.axhline(hline, color=BASELINE, lw=1, ls=(0, (4, 4)))
    hi = (d[label_col] == highlight) if (label_col and highlight) else pd.Series(False, index=d.index)
    ax.scatter(d.loc[~hi, x], d.loc[~hi, y], s=130, color=GREEN, edgecolor=SURFACE, linewidth=1.5, zorder=3)
    if hi.any():
        ax.scatter(d.loc[hi, x], d.loc[hi, y], s=240, color=GOLD, edgecolor=SURFACE, linewidth=1.5, zorder=4)
    if label_col:
        for _, r in d.iterrows():
            k = r[label_col] == highlight
            ax.annotate(str(r[label_col]), (r[x], r[y]), xytext=(10, 7),
                        textcoords="offset points", color=INK if k else SECONDARY,
                        fontsize=9, weight="bold" if k else "normal", zorder=5)
    if logx: ax.set_xscale("log")
    ax.grid(True, color=GRID, linewidth=1)
    ax.yaxis.set_major_formatter(FuncFormatter(_k))
    if not logx: ax.xaxis.set_major_formatter(FuncFormatter(_k))
    ax.margins(0.14)
    _frame(fig, ax, title or f"{y} vs {x}", subtitle, source)
    ax.set_xlabel((xlabel or x) + (" (log scale)" if logx else ""), color=SECONDARY)
    ax.set_ylabel(ylabel or y, color=SECONDARY)
    fig.tight_layout(); return fig


def correlation_heatmap(df, title=None, source=None):
    """Numeric correlations on a diverging blue-gray-red ramp, locked to [-1, 1]."""
    c = df.select_dtypes(include="number").corr(); n = len(c)
    fig, ax = plt.subplots(figsize=(1 + 0.75 * n, 1 + 0.75 * n))
    ax.set_facecolor(SURFACE); fig.set_facecolor(SURFACE)
    im = ax.imshow(c.values, cmap=DIVERGING, vmin=-1, vmax=1)
    ax.set_xticks(range(n), c.columns, rotation=45, ha="right", color=MUTED, fontsize=9)
    ax.set_yticks(range(n), c.index, color=MUTED, fontsize=9)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0)
    for i in range(n):
        for j in range(n):
            v = c.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8,
                    color=INK if abs(v) < 0.6 else SURFACE)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.outline.set_visible(False); cb.ax.tick_params(colors=MUTED, length=0, labelsize=8)
    ax.set_title(title or "Correlation", loc="left", color=INK, fontsize=14, pad=12)
    if source: fig.text(0.01, 0.005, source, color=MUTED, fontsize=8)
    fig.tight_layout(); return fig
