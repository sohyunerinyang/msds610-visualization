"""simple_eda: pandas-based EDA helpers plus two styled matplotlib charts."""

from .core import summarize, missing, numeric_columns, categorical_columns
from .plots import radial_bar, bubble

__version__ = "0.1.0"
__all__ = [
    "summarize", "missing", "numeric_columns", "categorical_columns",
    "radial_bar", "bubble",
]
