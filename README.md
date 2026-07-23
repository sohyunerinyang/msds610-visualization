# simple-eda

A tiny pandas-based exploratory data analysis package: a couple hundred lines,
one dependency (pandas), no CI/CD, no tests — just plain Python functions you
can import and use.

## Install

```bash
pip install simple-eda-syang120
```

## Usage

```python
import pandas as pd
import simple_eda as eda

df = pd.read_csv("data.csv")

eda.summarize(df)      # shape, dtypes, missing counts, uniques
eda.missing(df)        # which columns are missing data, and how much
eda.distribution(df, "some_column")   # value counts or describe() for one column
eda.correlations(df)   # correlation matrix for numeric columns
```

## Local development

```bash
git clone <this repo>
cd msds610-visualization
python -m pip install -e .
```

## Publishing (for maintainers)

```bash
python -m pip install --upgrade build twine
python -m build                                   # creates dist/*.whl and dist/*.tar.gz

python -m twine upload --repository testpypi dist/*   # TestPyPI first
pip install --index-url https://test.pypi.org/simple/ simple-eda-syang120

python -m twine upload dist/*                     # then real PyPI
pip install simple-eda-syang120
```
