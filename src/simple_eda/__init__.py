"""simple_eda: pandas-based EDA helpers plus a few styled matplotlib charts."""

from .core import summarize, missing, numeric_columns, categorical_columns
from .plots import missing_plot, histogram, correlation_heatmap

__version__ = "0.2.0"
__all__ = [
    "summarize",
    "missing",
    "numeric_columns",
    "categorical_columns",
    "missing_plot",
    "histogram",
    "correlation_heatmap",
]
