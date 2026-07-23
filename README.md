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

| Function | Chart |
| --- | --- |
| `ranked_bar(df, label_col, value_col)` | horizontal ranked bar, leader in gold |
| `scatter(df, x, y, label_col=, highlight=)` | labeled scatter / traction quadrant |
| `histogram(df, column)` | distribution with the median bin in gold |
| `correlation_heatmap(df)` | diverging blue→gray→red heatmap |

### Aesthetic choices

- **One accent color.** Everything is recessive green except the key value,
  which is gold. Green and gold differ in *both* hue and lightness, so the
  highlight survives colorblindness (lightness carries it when hue washes out).
- **Recessive chrome, data first.** Off-white surface, hairline gridlines,
  muted labels, top/right spines removed.
- **Direct labels over legends.** Values sit on the marks — nothing to
  cross-reference.
- **Diverging = signed.** Correlations use blue↔red with a neutral-gray zero,
  locked to [-1, 1], because correlation has a sign and gray must mean "none."
- **Attribution = integrity.** Every chart takes a `source=` footer and honest
  metric labels. See [`docs/DESIGN_RATIONALE.md`](docs/DESIGN_RATIONALE.md) for
  how the whole design maps to McCandless's four lenses of good information
  design (Interestingness × Function × Form × Integrity).

## The AI Image-Gen Tool Race

Which open-source generative-image tools are winning developer adoption? This
demo reads real GitHub data for eight tools and produces two charts:

```bash
python scripts/fetch_ai_tools.py      # refresh the data (live GitHub API)
python examples/ai_image_tool_race.py # redraw the charts into examples/
```

- **`examples/01_stars.png`** — GitHub stars per tool (mindshare); A1111 leads.
- **`examples/02_traction.png`** — a *traction quadrant*: installed base (stars)
  vs momentum (stars/day since launch). ComfyUI leads the modern pack.

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
