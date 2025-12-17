"""Comprehensive unit tests for analysis tools."""

import sys
import os
import json
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.analysis_tools import (
    calculate_returns_tool,
    calculate_volatility_tool,
    compare_stocks_tool,
    correlation_analysis_tool,
)


class TestCalculateReturnsTool:
    """Test suite for calculate_returns_tool."""

    def test_valid_returns_calculation(self):
        """Test returns calculation with valid ticker and period."""
        result = calculate_returns_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 30
        })
        data = json.loads(result)
        assert data["success"] is True
        assert "metrics" in data
        assert data["ticker"] == "AAPL"

    def test_different_time_periods(self):
        """Test returns across different time periods."""
        periods = [7, 30, 90]
        for period in periods:
            result = calculate_returns_tool.invoke({
                "company_ticker": "TSLA",
                "num_days": period
            })
            data = json.loads(result)
            assert data["success"] is True
            assert data["num_days"] == period

    def test_invalid_ticker(self):
        """Test with invalid ticker symbol."""
        result = calculate_returns_tool.invoke({
            "company_ticker": "INVALID",
            "num_days": 30
        })
        assert "not available" in result

    def test_insufficient_data(self):
        """Test with period exceeding available data."""
        result = calculate_returns_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 10000  # Unrealistic period
        })
        # Should still execute without error
        assert result is not None

    def test_all_available_tickers(self):
        """Test returns calculation for all tickers."""
        tickers = ["AAPL", "AMZN", "META", "MSFT", "NFLX", "TSLA"]
        for ticker in tickers:
            result = calculate_returns_tool.invoke({
                "company_ticker": ticker,
                "num_days": 30
            })
            data = json.loads(result)
            assert "success" in data


class TestCalculateVolatilityTool:
    """Test suite for calculate_volatility_tool."""

    def test_valid_volatility_calculation(self):
        """Test volatility calculation with valid inputs."""
        result = calculate_volatility_tool.invoke({
            "company_ticker": "NFLX",
            "num_days": 30
        })
        data = json.loads(result)
        assert data["success"] is True
        assert "metrics" in data

    def test_volatility_different_periods(self):
        """Test volatility across different time periods."""
        periods = [7, 30, 90, 180]
        for period in periods:
            result = calculate_volatility_tool.invoke({
                "company_ticker": "MSFT",
                "num_days": period
            })
            data = json.loads(result)
        assert data["success"] is True

    def test_volatility_invalid_ticker(self):
        """Test volatility with invalid ticker."""
        result = calculate_volatility_tool.invoke({
            "company_ticker": "XYZ123",
            "num_days": 30
        })
        assert "not available" in result

    def test_volatility_all_tickers(self):
        """Test volatility for all available tickers."""
        tickers = ["AAPL", "AMZN", "META", "MSFT", "NFLX", "TSLA"]
        for ticker in tickers:
            result = calculate_volatility_tool.invoke({
                "company_ticker": ticker,
                "num_days": 30
            })
            assert result is not None
            data = json.loads(result)
        assert "success" in data


class TestCompareStocksTool:
    """Test suite for compare_stocks_tool."""

    def test_valid_comparison(self):
        """Test comparing two valid stocks."""
        result = compare_stocks_tool.invoke({
            "ticker1": "AAPL",
            "ticker2": "MSFT",
            "num_days": 30
        })
        data = json.loads(result)
        assert data["success"] is True
        assert "winner" in data

    def test_comparison_different_pairs(self):
        """Test different stock pair comparisons."""
        pairs = [
            ("AAPL", "TSLA"),
            ("MSFT", "AMZN"),
            ("META", "NFLX"),
        ]
        for ticker1, ticker2 in pairs:
            result = compare_stocks_tool.invoke({
                "ticker1": ticker1,
                "ticker2": ticker2,
                "num_days": 30
            })
            data = json.loads(result)
            assert data["success"] is True

    def test_comparison_invalid_ticker(self):
        """Test comparison with one invalid ticker."""
        result = compare_stocks_tool.invoke({
            "ticker1": "AAPL",
            "ticker2": "INVALID",
            "num_days": 30
        })
        assert "not available" in result

    def test_comparison_same_ticker(self):
        """Test comparing a stock with itself."""
        result = compare_stocks_tool.invoke({
            "ticker1": "AAPL",
            "ticker2": "AAPL",
            "num_days": 30
        })
        # Should work but show identical results
        data = json.loads(result)
        assert data["success"] is True


class TestCorrelationAnalysisTool:
    """Test suite for correlation_analysis_tool."""

    def test_valid_correlation(self):
        """Test correlation analysis with valid tickers."""
        result = correlation_analysis_tool.invoke({
            "tickers_list": "AAPL,MSFT,TSLA",
            "num_days": 30
        })
        data = json.loads(result)
        assert data["success"] is True
        assert "AAPL" in result
        assert "MSFT" in result
        assert "TSLA" in result

    def test_correlation_two_stocks(self):
        """Test correlation with minimum number of stocks."""
        result = correlation_analysis_tool.invoke({
            "tickers_list": "AAPL,MSFT",
            "num_days": 30
        })
        data = json.loads(result)
        assert data["success"] is True

    def test_correlation_all_stocks(self):
        """Test correlation with all available stocks."""
        result = correlation_analysis_tool.invoke({
            "tickers_list": "AAPL,AMZN,META,MSFT,NFLX,TSLA",
            "num_days": 30
        })
        data = json.loads(result)
        assert data["success"] is True

    def test_correlation_single_ticker(self):
        """Test correlation with only one ticker (should fail)."""
        result = correlation_analysis_tool.invoke({
            "tickers_list": "AAPL",
            "num_days": 30
        })
        assert "at least 2" in result

    def test_correlation_invalid_ticker(self):
        """Test correlation with invalid ticker in list."""
        result = correlation_analysis_tool.invoke({
            "tickers_list": "AAPL,INVALID,MSFT",
            "num_days": 30
        })
        assert "not available" in result

    def test_correlation_different_periods(self):
        """Test correlation across different time periods."""
        periods = [7, 30, 90]
        for period in periods:
            result = correlation_analysis_tool.invoke({
                "tickers_list": "AAPL,MSFT",
                "num_days": period
            })
            data = json.loads(result)
        assert data["success"] is True


class TestDataIntegrity:
    """Test data file integrity and format."""

    def test_csv_files_exist(self):
        """Verify all expected CSV files exist."""
        tickers = ["AAPL", "AMZN", "META", "MSFT", "NFLX", "TSLA"]
        data_dir = Path(__file__).parent.parent / "data"
        
        for ticker in tickers:
            csv_file = data_dir / f"{ticker}.csv"
            assert csv_file.exists(), f"Missing data file: {ticker}.csv"

    def test_csv_format(self):
        """Test CSV files have correct format."""
        data_dir = Path(__file__).parent.parent / "data"
        csv_file = data_dir / "AAPL.csv"
        
        df = pd.read_csv(csv_file)
        
        # Check required columns exist
        required_columns = ["Date", "Close/Last", "Volume", "Open", "High", "Low"]
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"
        
        # Check data types
        assert not df.empty, "CSV file is empty"
        assert len(df) > 0, "No data rows in CSV"

    def test_data_consistency(self):
        """Test data consistency across all tickers."""
        tickers = ["AAPL", "AMZN", "META", "MSFT", "NFLX", "TSLA"]
        data_dir = Path(__file__).parent.parent / "data"
        
        for ticker in tickers:
            csv_file = data_dir / f"{ticker}.csv"
            df = pd.read_csv(csv_file)
            
            # Check we have data
            assert len(df) > 0, f"No data for {ticker}"
            
            # Check required columns
            assert "Close/Last" in df.columns, f"Missing Close/Last column in {ticker}"
            assert "Date" in df.columns, f"Missing Date column in {ticker}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
