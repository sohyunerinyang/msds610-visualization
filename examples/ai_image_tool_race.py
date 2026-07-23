"""The AI Image-Gen Tool Race — demo of simple_eda on real adoption data.

Reads the bundled GitHub snapshot and produces the two "favorite" charts:
  1. ranked_bar  — GitHub stars per tool (mindshare), leader in gold
  2. scatter     — installed base vs star velocity (a traction quadrant)

Run:  python examples/ai_image_tool_race.py
Refresh the data first with:  python scripts/fetch_ai_tools.py
"""

import matplotlib
matplotlib.use("Agg")  # save files without a display
import pandas as pd
import simple_eda as eda

df = pd.read_csv("data/ai_image_tools_2026-07.csv")

# --- a quick look, the boring EDA way -----------------------------------------
print(eda.summarize(df))
print("numeric:", eda.numeric_columns(df))

# --- chart 1: who has the mindshare -------------------------------------------
eda.ranked_bar(
    df, "tool", "stars",
    title="Who owns developer mindshare in AI image tools? (GitHub stars, Jul 2026)",
).savefig("examples/01_stars.png", dpi=140, bbox_inches="tight")

# --- chart 2: the traction quadrant -------------------------------------------
# x = installed base (total stars, log), y = momentum (stars/day since launch)
eda.scatter(
    df, "stars", "stars_per_day", label_col="tool", highlight="ComfyUI",
    logx=True,
    title="Traction quadrant: installed base vs momentum (ComfyUI leads the modern pack)",
).savefig("examples/02_traction.png", dpi=140, bbox_inches="tight")

print("saved examples/01_stars.png and examples/02_traction.png")
