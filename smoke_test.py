#!/usr/bin/env python3
"""Quick smoke test for FinGPT fixes."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


def test_stock_data():
    """Test stock data tool."""
    from src.tools.stock_data_tool import stock_data_tool
    result = stock_data_tool.invoke({"company_ticker": "AAPL", "num_days": 7})
    assert "Successfully executed" in result
    print("✅ Stock data tool works")


def test_analysis():
    """Test analysis tool."""
    from src.tools.analysis_tools import calculate_returns_tool
    result = calculate_returns_tool.invoke({"company_ticker": "TSLA", "num_days": 30})
    assert "Returns Analysis" in result
    print("✅ Analysis tool works")


def test_wikipedia():
    """Test Wikipedia tool."""
    from src.tools.wikipedia_tool import wikipedia_tool
    result = wikipedia_tool.invoke({"query": "Tim Cook"})
    assert len(result) > 0
    print("✅ Wikipedia tool works")


def test_visualization():
    """Test visualization tool."""
    from src.tools.visualization_tools import python_repl_tool
    code = """
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('data/AAPL.csv')
df['Close'] = df['Close/Last'].str.replace('$', '').astype(float)
fig = plt.figure()
plt.plot(df['Date'].head(10), df['Close'].head(10))
plt.title('Test Chart')
"""
    result = python_repl_tool.invoke({"code": code})
    # Success if either no error or chart created
    success = "Error" not in result or "Chart" in result
    assert success, f"Visualization failed: {result}"
    print("✅ Visualization tool works")


def test_data_files():
    """Test that all required data files exist."""
    import os
    tickers = ["AAPL", "AMZN", "META", "MSFT", "NFLX", "TSLA"]
    for ticker in tickers:
        assert os.path.exists(f"data/{ticker}.csv"), f"Missing {ticker}.csv"
    print("✅ All data files present")


def test_imports():
    """Test that all modules can be imported."""
    try:
        from src.tools import (
            wikipedia_tool,
            stock_data_tool,
            calculate_returns_tool,
            calculate_volatility_tool,
            compare_stocks_tool,
            correlation_analysis_tool,
            python_repl_tool,
        )
        from src.agents.supervisor import create_supervisor_graph
        from src.agents.research_agent import create_research_agent
        from src.agents.quant_agent import create_quant_agent
        from src.agents.viz_agent import create_viz_agent
        from src.graph.workflow import get_config
        print("✅ All imports successful")
    except Exception as e:
        raise AssertionError(f"Import failed: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🧪 Running FinGPT Smoke Tests...")
    print("=" * 70 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("Data Files", test_data_files),
        ("Stock Data", test_stock_data),
        ("Analysis", test_analysis),
        ("Wikipedia", test_wikipedia),
        ("Visualization", test_visualization),
    ]
    
    failed = []
    
    for name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            failed.append(name)
    
    print("\n" + "=" * 70)
    if not failed:
        print("✅ ALL SMOKE TESTS PASSED!")
        print("=" * 70 + "\n")
        sys.exit(0)
    else:
        print(f"❌ {len(failed)} TEST(S) FAILED: {', '.join(failed)}")
        print("=" * 70 + "\n")
        sys.exit(1)
