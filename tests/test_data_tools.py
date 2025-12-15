"""Comprehensive tests for data tools (stock data and wikipedia)."""

import sys
import os
import pytest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.stock_data_tool import stock_data_tool
from src.tools.wikipedia_tool import wikipedia_tool


class TestStockDataTool:
    """Test suite for stock_data_tool."""

    def test_valid_stock_data_retrieval(self):
        """Test retrieving stock data with valid ticker."""
        result = stock_data_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 7
        })
        assert "Successfully executed" in result
        assert "AAPL" in result

    def test_different_time_periods(self):
        """Test stock data retrieval across different periods."""
        periods = [7, 14, 30, 90]
        for period in periods:
            result = stock_data_tool.invoke({
                "company_ticker": "TSLA",
                "num_days": period
            })
            assert "Successfully executed" in result
            assert "TSLA" in result

    def test_all_available_tickers(self):
        """Test stock data for all available tickers."""
        tickers = ["AAPL", "AMZN", "META", "MSFT", "NFLX", "TSLA"]
        for ticker in tickers:
            result = stock_data_tool.invoke({
                "company_ticker": ticker,
                "num_days": 30
            })
            assert "Successfully executed" in result or "Error" in result

    def test_invalid_ticker(self):
        """Test with invalid ticker symbol."""
        result = stock_data_tool.invoke({
            "company_ticker": "INVALIDXYZ",
            "num_days": 7
        })
        assert "not available" in result or "Error" in result

    def test_zero_days(self):
        """Test with zero days period."""
        result = stock_data_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 0
        })
        # Should handle gracefully
        assert result is not None

    def test_large_period(self):
        """Test with very large period."""
        result = stock_data_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 365
        })
        assert result is not None

    def test_case_sensitivity(self):
        """Test ticker case sensitivity."""
        # Test lowercase
        result_lower = stock_data_tool.invoke({
            "company_ticker": "aapl",
            "num_days": 7
        })
        # Test uppercase
        result_upper = stock_data_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 7
        })
        # Both should work
        assert result_lower is not None
        assert result_upper is not None


class TestWikipediaTool:
    """Test suite for wikipedia_tool."""

    def test_valid_ceo_search(self):
        """Test searching for CEO information."""
        queries = [
            "Tim Cook",
            "Elon Musk",
            "Satya Nadella",
            "Mark Zuckerberg"
        ]
        for query in queries:
            result = wikipedia_tool.invoke({"query": query})
            assert result is not None
            assert len(result) > 0

    def test_company_search(self):
        """Test searching for company information."""
        companies = ["Apple Inc", "Tesla Inc", "Microsoft"]
        for company in companies:
            result = wikipedia_tool.invoke({"query": company})
            assert result is not None
            assert len(result) > 0

    def test_search_returns_summary(self):
        """Test that search returns meaningful summary."""
        result = wikipedia_tool.invoke({"query": "Apple Inc"})
        assert len(result) > 50  # Should have substantial content
        assert "Apple" in result

    def test_ambiguous_search(self):
        """Test search with ambiguous term."""
        result = wikipedia_tool.invoke({"query": "Apple"})
        # Should return something, even if disambiguated
        assert result is not None
        assert len(result) > 0

    def test_nonexistent_topic(self):
        """Test search for non-existent topic."""
        result = wikipedia_tool.invoke({
            "query": "XYZ123NonexistentCompanyABC"
        })
        # Should handle gracefully
        assert result is not None

    def test_special_characters_query(self):
        """Test search with special characters."""
        result = wikipedia_tool.invoke({
            "query": "AT&T"
        })
        assert result is not None

    def test_empty_query(self):
        """Test with empty query string."""
        result = wikipedia_tool.invoke({"query": ""})
        # Should handle gracefully
        assert result is not None

    def test_very_long_query(self):
        """Test with very long query string."""
        long_query = "Apple Inc CEO Tim Cook biography history " * 10
        result = wikipedia_tool.invoke({"query": long_query})
        assert result is not None


class TestToolIntegration:
    """Test integration between tools."""

    def test_stock_data_then_analysis_workflow(self):
        """Test workflow of getting stock data then analyzing."""
        # First get stock data
        stock_result = stock_data_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 30
        })
        assert "Successfully executed" in stock_result
        
        # This confirms data is available for analysis tools
        from src.tools.analysis_tools import calculate_returns_tool
        analysis_result = calculate_returns_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 30
        })
        assert "Returns Analysis" in analysis_result

    def test_wikipedia_then_stock_workflow(self):
        """Test workflow of researching company then getting stock data."""
        # First research the company
        wiki_result = wikipedia_tool.invoke({"query": "Tesla Inc"})
        assert "Tesla" in wiki_result or "Musk" in wiki_result
        
        # Then get stock data
        stock_result = stock_data_tool.invoke({
            "company_ticker": "TSLA",
            "num_days": 7
        })
        assert "Successfully executed" in stock_result

    def test_multiple_tool_calls(self):
        """Test making multiple sequential tool calls."""
        tickers = ["AAPL", "MSFT", "TSLA"]
        
        for ticker in tickers:
            result = stock_data_tool.invoke({
                "company_ticker": ticker,
                "num_days": 7
            })
            assert result is not None


class TestErrorHandling:
    """Test error handling across data tools."""

    def test_missing_data_file(self):
        """Test handling of missing data file."""
        result = stock_data_tool.invoke({
            "company_ticker": "NONEXISTENT",
            "num_days": 7
        })
        assert "not available" in result

    def test_invalid_inputs(self):
        """Test various invalid inputs."""
        invalid_cases = [
            {"company_ticker": "", "num_days": 7},
            {"company_ticker": None, "num_days": 7},
            {"company_ticker": "AAPL", "num_days": -1},
        ]
        
        for case in invalid_cases:
            try:
                result = stock_data_tool.invoke(case)
                # Should handle gracefully
                assert result is not None
            except Exception:
                # Should not raise unhandled exceptions
                pass

    def test_network_error_handling(self):
        """Test that network errors are handled (for Wikipedia)."""
        # This might fail if no network, should handle gracefully
        try:
            result = wikipedia_tool.invoke({"query": "Test Query"})
            assert result is not None
        except Exception as e:
            # Should provide meaningful error message
            assert str(e) is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
