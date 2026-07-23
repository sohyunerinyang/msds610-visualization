"""Core EDA helpers: a handful of pandas-based functions for a first look at a dataframe."""

import pandas as pd


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """Print a quick overview of a dataframe and return a per-column summary table."""
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    print()

    summary = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "non_null": df.count(),
        "unique": df.nunique(),
        "missing": df.isna().sum(),
    })
    summary["missing_pct"] = (summary["missing"] / len(df) * 100).round(1)
    print(summary)
    return summary


def missing(df: pd.DataFrame) -> pd.DataFrame:
    """Return columns with missing values, sorted by how much is missing."""
    counts = df.isna().sum()
    counts = counts[counts > 0].sort_values(ascending=False)

    report = pd.DataFrame({
        "missing": counts,
        "missing_pct": (counts / len(df) * 100).round(1),
    })

    if report.empty:
        print("No missing values found.")
    else:
        print(report)
    return report


def distribution(df: pd.DataFrame, column: str) -> pd.Series:
    """Show value counts (categorical) or descriptive stats (numeric) for one column."""
    series = df[column]

    if pd.api.types.is_numeric_dtype(series):
        stats = series.describe()
        print(stats)
        return stats

    counts = series.value_counts(dropna=False)
    print(counts)
    return counts


def correlations(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """Return the correlation matrix for a dataframe's numeric columns."""
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        print("Need at least two numeric columns to compute correlations.")
        return pd.DataFrame()

    corr = numeric_df.corr(method=method)
    print(corr)
    return corr
