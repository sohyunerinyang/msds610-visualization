# simple-eda

A tiny pandas + matplotlib package for fast, good-looking exploratory data
analysis. A couple hundred lines, two dependencies, no dashboard — just plain
functions you can import and reuse on any DataFrame.

Its house style has one idea: **spend your one bright color on the number that
matters.** Marks are a muted green; the single key value (a median, a leader)
is gold, so the eye lands there first.

Demo project: **[The AI Image-Gen Tool Race](#the-ai-image-gen-tool-race)** —
tracking which generative-image tools are winning developer adoption.

## Install

```bash
pip install -e .          # editable, from a clone
```

## EDA functions

Each does one job, takes a DataFrame, and **returns a plain object** (dict,
list, or pandas Series). Nothing is printed; the DataFrame is never mutated.

| Function | Returns |
| --- | --- |
| `summarize(df)` | dict — shape, column names, dtypes |
| `missing(df)` | Series — null count per column, highest first |
| `numeric_columns(df)` | list — numeric column names |
| `categorical_columns(df)` | list — non-numeric column names |

## Chart functions

Each takes a DataFrame and **returns a matplotlib `Figure`** (never calls
`show`, never mutates). Save with `fig.savefig(...)` or show it in a notebook.

Two charts, both with small no-frills signatures (titles derive from the
column names — rename your columns to friendly labels for a nice title):

| Function | Chart |
| --- | --- |
| `radial_bar(df, label_col, value_col, highlight=None)` | circular bar chart; length + color = magnitude |
| `bubble(df, x, y, size_col, label_col=None, color_col=None, highlight=None)` | bubble "market map"; size + color add dimensions |

### Aesthetic choices

- **One accent color.** Everything is recessive green except the key value,
  which is gold. Green and gold differ in *both* hue and lightness, so the
  highlight survives colorblindness (lightness carries it when hue washes out).
- **Color carries meaning.** In `radial_bar`, color *and* length both encode
  magnitude (a light→dark green ramp); in `bubble`, size and an optional
  category color add dimensions without a second chart.
- **Centered & symmetric.** The plot sits in the middle of the figure with
  balanced margins; bubbles are sized large enough to read at a glance.
- **Recessive chrome, data first.** Off-white surface, hairline gridlines,
  muted labels, top/right spines removed.
- **Direct labels over legends.** Values sit on the marks — nothing to
  cross-reference (a legend appears only when color encodes a category).

See [`docs/DESIGN_RATIONALE.md`](docs/DESIGN_RATIONALE.md) for how the design
maps to McCandless's four lenses (Interestingness × Function × Form ×
Integrity). Source attribution lives in the README / video narration, since the
chart signatures stay minimal.

## The AI Image-Gen Tool Race

Which open-source generative-image tools are winning developer adoption? This
demo reads real GitHub data for eight tools and produces two charts:

```bash
python scripts/fetch_ai_tools.py      # refresh the data (live GitHub API)
python examples/ai_image_tool_race.py # redraw the charts into examples/
```

- **`examples/01_radial.png`** — a radial bar of GitHub stars per tool
  (mindshare); A1111 leads, ComfyUI in gold.
- **`examples/02_market_map.png`** — a bubble *market map*: installed base
  (stars) vs momentum (stars/day), bubble size = forks. ComfyUI leads the
  modern pack.

Data snapshot lives in `data/`; re-run the fetcher monthly to keep it current.

## Folder shape

```
msds610-visualization/
├── src/simple_eda/
│   ├── __init__.py
│   ├── core.py            # EDA helpers
│   └── plots.py           # chart functions + house style
├── data/                  # dated GitHub snapshots (CSV)
├── scripts/fetch_ai_tools.py   # live data refresher
├── examples/ai_image_tool_race.py
├── README.md
├── pyproject.toml
└── LICENSE
```

## Publishing (optional, for maintainers)

```bash
python -m pip install --upgrade build twine
python -m build                                   # dist/*.whl + *.tar.gz
python -m twine upload --repository testpypi dist/*   # TestPyPI first
python -m twine upload dist/*                          # then PyPI
```

**Use API tokens, not passwords.** When `twine` prompts: username `__token__`,
password the `pypi-...` token. **Never commit tokens** — keep them in
`~/.pypirc` (chmod 600) or `TWINE_USERNAME` / `TWINE_PASSWORD` env vars.
