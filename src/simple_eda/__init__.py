"""simple_eda: a handful of pandas-based exploratory data analysis helpers."""

from .core import summarize, missing, numeric_columns, categorical_columns

__version__ = "0.1.0"
__all__ = ["summarize", "missing", "numeric_columns", "categorical_columns"]
