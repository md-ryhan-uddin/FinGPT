"""Tools for FinGPT agents."""

from .wikipedia_tool import wikipedia_tool
from .stock_data_tool import stock_data_tool
from .visualization_tools import python_repl_tool
from .analysis_tools import (
    calculate_returns_tool,
    calculate_volatility_tool,
    compare_stocks_tool,
    correlation_analysis_tool,
)

__all__ = [
    "wikipedia_tool",
    "stock_data_tool",
    "python_repl_tool",
    "calculate_returns_tool",
    "calculate_volatility_tool",
    "compare_stocks_tool",
    "correlation_analysis_tool",
]
