"""simple_eda: pandas-based EDA helpers plus styled matplotlib charts."""

from .core import summarize, missing, numeric_columns, categorical_columns
from .plots import histogram, ranked_bar, scatter, correlation_heatmap

__version__ = "0.3.0"
__all__ = [
    "summarize", "missing", "numeric_columns", "categorical_columns",
    "histogram", "ranked_bar", "scatter", "correlation_heatmap",
]
