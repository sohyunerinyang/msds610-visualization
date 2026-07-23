# simple-eda

A tiny pandas-based exploratory data analysis package. A couple hundred lines,
one dependency (pandas), no CI/CD, no tests — just plain Python functions you
can import and use.

No web app. No dashboard. Just useful, installable, importable.

## The functions

Each one does a single job, takes a DataFrame, and **returns a plain object**
(a dict, a list, or a pandas Series). Nothing is printed and your DataFrame is
never changed in place.

| Function | Returns |
| --- | --- |
| `summarize(df)` | dict — shape, column names, dtypes |
| `missing(df)` | Series — null count per column, highest first |
| `numeric_columns(df)` | list — names of the numeric columns |
| `categorical_columns(df)` | list — names of the non-numeric columns |

## Usage

```python
import pandas as pd
import simple_eda as eda

df = pd.read_csv("data.csv")

eda.summarize(df)            # {'rows': ..., 'columns': ..., 'column_names': [...], 'dtypes': {...}}
eda.missing(df)              # pandas Series of null counts
eda.numeric_columns(df)      # ['age', 'price', ...]
eda.categorical_columns(df)  # ['city', 'category', ...]
```

## Folder shape

```
msds610-visualization/
├── src/
│   └── simple_eda/
│       ├── __init__.py
│       └── core.py
├── README.md
├── pyproject.toml
└── LICENSE
```

## Local development (editable install)

```bash
git clone <this repo>
cd msds610-visualization
python -m pip install -e .
```

Editable mode means your source edits take effect immediately — no reinstall
needed.

## Publishing (for maintainers)

Build a wheel and a source distribution:

```bash
python -m pip install --upgrade build twine
python -m build          # creates dist/*.whl and dist/*.tar.gz
```

Upload to **TestPyPI** first, then install from it to confirm it works:

```bash
python -m twine upload --repository testpypi dist/*
python -m pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ simple-eda-syang120
```

Then upload to the real **PyPI**:

```bash
python -m twine upload dist/*
python -m pip install simple-eda-syang120
```

### Authentication — use API tokens, not passwords

Create a token at <https://test.pypi.org/manage/account/token/> (and
<https://pypi.org/manage/account/token/> for PyPI). When `twine` prompts:

- username: `__token__`
- password: the token (starts with `pypi-...`)

**Never commit tokens or secrets.** Keep them out of the repo — put them in
`~/.pypirc` (chmod 600) or the `TWINE_USERNAME` / `TWINE_PASSWORD` environment
variables instead.
