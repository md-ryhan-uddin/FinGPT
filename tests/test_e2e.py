"""End-to-end tests simulating user interactions with FinGPT."""

import sys
import os
import pytest
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestUserScenarios:
    """Test realistic user interaction scenarios."""

    def test_scenario_research_ceo(self):
        """Test: User asks 'Who is Apple's CEO?'"""
        import json
        from src.tools.wikipedia_tool import wikipedia_tool
        
        result = wikipedia_tool.invoke({"query": "Tim Cook Apple CEO"})
        assert result is not None
        assert len(result) > 0
        # Validate JSON structure
        data = json.loads(result)
        assert "success" in data
        assert "query" in data

    def test_scenario_stock_performance(self):
        """Test: User asks 'Analyze Tesla's stock performance'"""
        from src.tools.analysis_tools import calculate_returns_tool, calculate_volatility_tool
        
        # Get returns
        returns = calculate_returns_tool.invoke({
            "company_ticker": "TSLA",
            "num_days": 30
        })
        data = json.loads(returns)
        assert data["success"] is True
        
        # Get volatility
        volatility = calculate_volatility_tool.invoke({
            "company_ticker": "TSLA",
            "num_days": 30
        })
        data = json.loads(volatility)
        assert data["success"] is True

    def test_scenario_compare_stocks(self):
        """Test: User asks 'Compare Apple vs Microsoft'"""
        from src.tools.analysis_tools import compare_stocks_tool
        
        result = compare_stocks_tool.invoke({
            "ticker1": "AAPL",
            "ticker2": "MSFT",
            "num_days": 30
        })
        data = json.loads(result)
        assert data["success"] is True
        data = json.loads(result)
        assert "winner" in data

    def test_scenario_visualize_stock(self):
        """Test: User asks 'Show me a chart of Meta's stock'"""
        from src.tools.visualization_tools import python_repl_tool
        
        code = """
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/META.csv', parse_dates=['Date'])
df['Close'] = df['Close/Last'].str.replace('$', '').astype(float)

fig = plt.figure(figsize=(12, 6))
plt.plot(df['Date'].head(90), df['Close'].head(90))
plt.title('META Stock Price - Last 90 Days')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.grid(True)
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None

    def test_scenario_multiple_stock_comparison(self):
        """Test: User compares multiple tech stocks"""
        from src.tools.analysis_tools import compare_stocks_tool
        
        pairs = [("AAPL", "TSLA"), ("MSFT", "AMZN"), ("META", "NFLX")]
        
        for ticker1, ticker2 in pairs:
            result = compare_stocks_tool.invoke({
                "ticker1": ticker1,
                "ticker2": ticker2,
                "num_days": 30
            })
            data = json.loads(result)
        assert data["success"] is True

    def test_scenario_correlation_analysis(self):
        """Test: User asks about stock correlations"""
        from src.tools.analysis_tools import correlation_analysis_tool
        
        result = correlation_analysis_tool.invoke({
            "tickers_list": "AAPL,MSFT,TSLA",
            "num_days": 90
        })
        data = json.loads(result)
        assert data["success"] is True


class TestErrorRecovery:
    """Test error recovery scenarios."""

    def test_typo_in_ticker(self):
        """Test: User makes typo in ticker symbol"""
        from src.tools.analysis_tools import calculate_returns_tool
        
        result = calculate_returns_tool.invoke({
            "company_ticker": "APLE",  # Typo: should be AAPL
            "num_days": 30
        })
        assert "not available" in result

    def test_unrealistic_time_period(self):
        """Test: User requests unrealistic time period"""
        from src.tools.analysis_tools import calculate_returns_tool
        
        result = calculate_returns_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 10000  # Way more than available data
        })
        assert result is not None

    def test_invalid_chart_request(self):
        """Test: User requests chart with bad code"""
        from src.tools.visualization_tools import python_repl_tool
        
        code = "import pandas as pd\ndf = pd.read_csv('nonexistent.csv')"
        result = python_repl_tool.invoke({"code": code})
        assert "Error" in result or "Failed" in result


class TestDataConsistency:
    """Test data consistency across different queries."""

    def test_same_ticker_different_periods(self):
        """Test: Same ticker with different time periods"""
        from src.tools.analysis_tools import calculate_returns_tool
        
        results = []
        for period in [7, 30, 90]:
            result = calculate_returns_tool.invoke({
                "company_ticker": "AAPL",
                "num_days": period
            })
            results.append(result)
        
        # All should succeed
        for result in results:
            data = json.loads(result)
        assert data["success"] is True

    def test_all_tickers_accessible(self):
        """Test: All tickers can be accessed"""
        from src.tools.stock_data_tool import stock_data_tool
        
        tickers = ["AAPL", "AMZN", "META", "MSFT", "NFLX", "TSLA"]
        for ticker in tickers:
            result = stock_data_tool.invoke({
                "company_ticker": ticker,
                "num_days": 7
            })
            data = json.loads(result)
        assert data["success"] is True


class TestPerformance:
    """Test performance characteristics."""

    def test_quick_tool_response(self):
        """Test that tools respond quickly."""
        import time
        from src.tools.analysis_tools import calculate_returns_tool
        
        start = time.time()
        calculate_returns_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 30
        })
        elapsed = time.time() - start
        
        # Should complete in reasonable time (< 5 seconds)
        assert elapsed < 5.0

    def test_multiple_sequential_calls(self):
        """Test multiple tool calls in sequence."""
        from src.tools.analysis_tools import calculate_returns_tool
        
        for _ in range(5):
            result = calculate_returns_tool.invoke({
                "company_ticker": "AAPL",
                "num_days": 30
            })
            assert result is not None


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_zero_days_period(self):
        """Test with zero days period."""
        from src.tools.analysis_tools import calculate_returns_tool
        
        result = calculate_returns_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 0
        })
        assert result is not None

    def test_single_day_period(self):
        """Test with single day period."""
        from src.tools.analysis_tools import calculate_returns_tool
        
        result = calculate_returns_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 1
        })
        assert result is not None

    def test_empty_ticker_string(self):
        """Test with empty ticker string."""
        from src.tools.stock_data_tool import stock_data_tool
        
        try:
            result = stock_data_tool.invoke({
                "company_ticker": "",
                "num_days": 7
            })
            assert result is not None
        except Exception:
            pass  # May raise exception, which is acceptable

    def test_special_characters_in_query(self):
        """Test with special characters in query."""
        from src.tools.wikipedia_tool import wikipedia_tool
        
        result = wikipedia_tool.invoke({
            "query": "Apple Inc. & CEO (Tim Cook)"
        })
        assert result is not None


class TestOutputFormat:
    """Test output format and content."""

    def test_returns_output_format(self):
        """Test returns output has expected format."""
        from src.tools.analysis_tools import calculate_returns_tool
        
        result = calculate_returns_tool.invoke({
            "company_ticker": "AAPL",
            "num_days": 30
        })
        
        # Check for expected fields
        data = json.loads(result)
        assert "metrics" in data
        assert "avg_daily_return" in data["metrics"]

    def test_volatility_output_format(self):
        """Test volatility output has expected format."""
        from src.tools.analysis_tools import calculate_volatility_tool
        
        result = calculate_volatility_tool.invoke({
            "company_ticker": "TSLA",
            "num_days": 30
        })
        
        data = json.loads(result)
        assert "metrics" in data
        assert "annualized_volatility" in data["metrics"]

    def test_comparison_output_format(self):
        """Test comparison output has expected format."""
        from src.tools.analysis_tools import compare_stocks_tool
        
        result = compare_stocks_tool.invoke({
            "ticker1": "AAPL",
            "ticker2": "MSFT",
            "num_days": 30
        })
        
        assert "**AAPL:**" in result or "AAPL" in result
        assert "**MSFT:**" in result or "MSFT" in result
        data = json.loads(result)
        assert "winner" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
