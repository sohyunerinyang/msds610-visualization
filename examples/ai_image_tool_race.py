"""The AI Image-Gen Tool Race — demo of simple_eda on real adoption data.

Produces the two "favorite" charts:
  1. radial_bar — GitHub stars per tool (mindshare), leader in gold
  2. bubble     — reach vs momentum, bubble size = forks (a market map)

Titles come from the column names, so we rename columns to friendly labels
first (the library keeps a tiny, no-frills signature).

Run:  python examples/ai_image_tool_race.py
Refresh the data first with:  python scripts/fetch_ai_tools.py
"""

import matplotlib
matplotlib.use("Agg")  # save files without a display
import pandas as pd
import simple_eda as eda

df = pd.read_csv("data/ai_image_tools_2026-07.csv").rename(columns={
    "tool": "Tool",
    "stars": "GitHub stars",
    "stars_per_day": "Avg stars/day",
    "forks": "Forks",
})

# --- a quick look, the boring EDA way -----------------------------------------
print(eda.summarize(df))
print("numeric:", eda.numeric_columns(df))

# --- chart 1: the race, as a radial bar ---------------------------------------
eda.radial_bar(df, "Tool", "GitHub stars", highlight="ComfyUI").savefig(
    "examples/01_radial.png", dpi=140)  # no tight crop: keep the centered square

# --- chart 2: the market map (reach vs momentum, bubble size = forks) ----------
eda.bubble(df, "GitHub stars", "Avg stars/day", "Forks",
           label_col="Tool", highlight="ComfyUI").savefig(
    "examples/02_market_map.png", dpi=140, bbox_inches="tight")

print("saved examples/01_radial.png and examples/02_market_map.png")
