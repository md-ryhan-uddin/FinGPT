"""Test script for FinGPT tools."""

import sys
sys.path.insert(0, '/home/ryhan/Downloads/workspace/FinGPT')

from src.tools.stock_data_tool import stock_data_tool
from src.tools.analysis_tools import calculate_returns_tool, calculate_volatility_tool, compare_stocks_tool
from src.tools.wikipedia_tool import wikipedia_tool


def test_wikipedia_tool():
    """Test Wikipedia search."""
    print("\n=== Testing Wikipedia Tool ===")
    result = wikipedia_tool.invoke({"query": "Tim Cook"})
    print(f"✓ Wikipedia tool works: {result[:100]}...")
    assert "Tim" in result or "Cook" in result


def test_stock_data_tool():
    """Test stock data retrieval."""
    print("\n=== Testing Stock Data Tool ===")
    result = stock_data_tool.invoke({"company_ticker": "AAPL", "num_days": 7})
    print(f"✓ Stock data tool works: {result[:150]}...")
    assert "Successfully executed" in result
    assert "AAPL" in result


def test_calculate_returns():
    """Test returns calculation."""
    print("\n=== Testing Calculate Returns Tool ===")
    result = calculate_returns_tool.invoke({"company_ticker": "TSLA", "num_days": 30})
    print(result)
    assert "Returns Analysis" in result or "Error" not in result
    print("✓ Returns calculation works!")


def test_calculate_volatility():
    """Test volatility calculation."""
    print("\n=== Testing Calculate Volatility Tool ===")
    result = calculate_volatility_tool.invoke({"company_ticker": "NFLX", "num_days": 30})
    print(result)
    assert "Volatility Analysis" in result or "Error" not in result
    print("✓ Volatility calculation works!")


def test_compare_stocks():
    """Test stock comparison."""
    print("\n=== Testing Compare Stocks Tool ===")
    result = compare_stocks_tool.invoke({"ticker1": "AAPL", "ticker2": "MSFT", "num_days": 30})
    print(result)
    assert "Comparative Analysis" in result
    print("✓ Stock comparison works!")


if __name__ == "__main__":
    print("🧪 Running FinGPT Tool Tests...\n")

    try:
        test_wikipedia_tool()
        test_stock_data_tool()
        test_calculate_returns()
        test_calculate_volatility()
        test_compare_stocks()

        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
