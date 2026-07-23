"""Core EDA helpers.

Each function does one job, takes a DataFrame, and *returns* a plain object
(dict, list, or pandas Series) — nothing is printed and the DataFrame is never
modified in place.
"""

import pandas as pd


def summarize(df: pd.DataFrame) -> dict:
    """Return the dataframe's shape, column names, and dtypes as a plain dict."""
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
    }


def missing(df: pd.DataFrame) -> pd.Series:
    """Return the number of missing values per column, highest first."""
    return df.isna().sum().sort_values(ascending=False)


def numeric_columns(df: pd.DataFrame) -> list:
    """Return the names of the numeric columns."""
    return list(df.select_dtypes(include="number").columns)


def categorical_columns(df: pd.DataFrame) -> list:
    """Return the names of the non-numeric (categorical / object) columns."""
    return list(df.select_dtypes(exclude="number").columns)
