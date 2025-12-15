"""Utility functions for loading and processing stock data."""

import pandas as pd
from pathlib import Path
from typing import Optional


def load_stock_data(ticker: str, data_dir: str = "data") -> Optional[pd.DataFrame]:
    """
    Load stock data from CSV file.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        data_dir: Directory containing CSV files

    Returns:
        DataFrame with stock data or None if file not found
    """
    file_path = Path(data_dir) / f"{ticker}.csv"

    if not file_path.exists():
        return None

    df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
    return df


def get_available_tickers(data_dir: str = "data") -> list[str]:
    """
    Get list of available stock tickers from data directory.

    Args:
        data_dir: Directory containing CSV files

    Returns:
        List of available ticker symbols
    """
    data_path = Path(data_dir)
    csv_files = list(data_path.glob("*.csv"))
    tickers = [f.stem for f in csv_files]
    return sorted(tickers)
