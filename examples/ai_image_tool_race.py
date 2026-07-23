"""The AI Image-Gen Tool Race — demo of simple_eda on real adoption data.

Reads the bundled GitHub snapshot and produces the two "favorite" charts:
  1. radial_bar — GitHub stars per tool (mindshare), leader in gold
  2. bubble     — reach vs momentum, bubble size = forks (a market map)

Run:  python examples/ai_image_tool_race.py
Refresh the data first with:  python scripts/fetch_ai_tools.py
"""

import matplotlib
matplotlib.use("Agg")  # save files without a display
import pandas as pd
import simple_eda as eda

df = pd.read_csv("data/ai_image_tools_2026-07.csv")
SOURCE = "Source: GitHub API · snapshot 23 Jul 2026 · n=8 open-source tools"

# --- a quick look, the boring EDA way -----------------------------------------
print(eda.summarize(df))
print("numeric:", eda.numeric_columns(df))

# --- chart 1: the race, as a radial bar ---------------------------------------
eda.radial_bar(
    df, "tool", "stars", highlight="ComfyUI",
    title="The AI Image-Gen Tool Race",
    subtitle="GitHub stars by tool — ComfyUI, the modern leader, in gold",
    source=SOURCE,
).savefig("examples/01_radial.png", dpi=140, bbox_inches="tight")

# --- chart 2: the market map (reach vs momentum, size = forks) -----------------
eda.bubble(
    df, "stars", "stars_per_day", size_col="forks", label_col="tool",
    highlight="ComfyUI", logx=True,
    vline=df["stars"].median(), hline=df["stars_per_day"].median(),
    title="Market map: reach vs momentum",
    subtitle="Top-right = big AND fast-growing. Bubble size = forks (contributor pull).",
    xlabel="Installed base — GitHub stars",
    ylabel="Momentum — avg stars/day since launch",
    source=SOURCE + " · momentum is a LIFETIME average, not last-30-days",
).savefig("examples/02_market_map.png", dpi=140, bbox_inches="tight")

print("saved examples/01_radial.png and examples/02_market_map.png")
