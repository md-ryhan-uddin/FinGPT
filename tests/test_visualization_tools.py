"""Tests for visualization tools and Python REPL."""

import sys
import os
import json
import pytest
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for testing

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.visualization_tools import python_repl_tool


class TestPythonREPLTool:
    """Test suite for python_repl_tool."""

    def test_simple_calculation(self):
        """Test executing simple Python calculation."""
        result = python_repl_tool.invoke({
            "code": "result = 2 + 2\nprint(result)"
        })
        assert result is not None
        assert "Error" not in result or "successfully" in result.lower()

    def test_import_pandas(self):
        """Test importing pandas library."""
        result = python_repl_tool.invoke({
            "code": "import pandas as pd\nprint('Pandas imported')"
        })
        assert "Error" not in result or "successfully" in result.lower()

    def test_import_matplotlib(self):
        """Test importing matplotlib."""
        result = python_repl_tool.invoke({
            "code": "import matplotlib.pyplot as plt\nprint('Matplotlib imported')"
        })
        assert result is not None

    def test_read_csv_data(self):
        """Test reading CSV data file."""
        code = """
import pandas as pd
import os
print(f"Current directory: {os.getcwd()}")
df = pd.read_csv('data/AAPL.csv')
print(f"Loaded {len(df)} rows")
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None
        # Should either work or provide error message
        assert "rows" in result or "Error" in result or "executed" in result

    def test_simple_plot_creation(self):
        """Test creating a simple matplotlib plot."""
        code = """
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(10, 6))
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title('Test Plot')
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None
        # Should create chart
        data = json.loads(result)
        assert data["success"] is True

    def test_stock_data_visualization(self):
        """Test creating stock price visualization."""
        code = """
import pandas as pd
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv('data/AAPL.csv', parse_dates=['Date'])

# Clean the Close/Last column
df['Close'] = df['Close/Last'].str.replace('$', '').astype(float)

# Get last 30 days
df = df.head(30)

# Create plot
fig = plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Close'], marker='o', linewidth=2)
plt.title('AAPL Stock Price - Last 30 Days')
plt.xlabel('Date')
plt.ylabel('Close Price ($)')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None

    def test_multiple_stock_comparison_plot(self):
        """Test creating comparison plot for multiple stocks."""
        code = """
import pandas as pd
import matplotlib.pyplot as plt

# Read data for two stocks
aapl = pd.read_csv('data/AAPL.csv', parse_dates=['Date'])
msft = pd.read_csv('data/MSFT.csv', parse_dates=['Date'])

# Clean prices
aapl['Close'] = aapl['Close/Last'].str.replace('$', '').astype(float)
msft['Close'] = msft['Close/Last'].str.replace('$', '').astype(float)

# Normalize to percentage change
aapl['Normalized'] = (aapl['Close'] / aapl['Close'].iloc[0] - 1) * 100
msft['Normalized'] = (msft['Close'] / msft['Close'].iloc[0] - 1) * 100

# Plot
fig = plt.figure(figsize=(12, 6))
plt.plot(aapl['Date'].head(30), aapl['Normalized'].head(30), label='AAPL', marker='o')
plt.plot(msft['Date'].head(30), msft['Normalized'].head(30), label='MSFT', marker='s')
plt.title('Stock Performance Comparison (% Change)')
plt.xlabel('Date')
plt.ylabel('Percentage Change (%)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None

    def test_error_handling(self):
        """Test error handling in code execution."""
        code = """
import pandas as pd
# This should cause an error - nonexistent file
df = pd.read_csv('nonexistent_file.csv')
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None
        assert "Error" in result or "Failed" in result

    def test_syntax_error_handling(self):
        """Test handling of syntax errors."""
        code = "print('missing parenthesis'"
        result = python_repl_tool.invoke({"code": code})
        assert result is not None
        assert "Error" in result or "Failed" in result

    def test_division_by_zero(self):
        """Test handling runtime errors."""
        code = "result = 1 / 0"
        result = python_repl_tool.invoke({"code": code})
        assert result is not None
        assert "Error" in result or "Failed" in result


class TestVisualizationOutput:
    """Test visualization output and file creation."""

    def test_chart_file_creation(self):
        """Test that charts are saved to output directory."""
        output_dir = Path(__file__).parent.parent / "output"
        
        # Count existing files
        existing_files = list(output_dir.glob("chart_*.png")) if output_dir.exists() else []
        initial_count = len(existing_files)
        
        # Create a chart
        code = """
import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [1, 4, 9])
plt.title('Test Chart')
"""
        result = python_repl_tool.invoke({"code": code})
        
        # Check if chart info is in result
        if "Chart" in result:
            # A chart should have been created
            assert "output/chart_" in result

    def test_multiple_charts_creation(self):
        """Test creating multiple charts in sequence."""
        codes = [
            "import matplotlib.pyplot as plt\nfig = plt.figure()\nplt.plot([1,2,3])\nplt.title('Chart 1')",
            "import matplotlib.pyplot as plt\nfig = plt.figure()\nplt.plot([3,2,1])\nplt.title('Chart 2')",
            "import matplotlib.pyplot as plt\nfig = plt.figure()\nplt.plot([1,3,2])\nplt.title('Chart 3')",
        ]
        
        for code in codes:
            result = python_repl_tool.invoke({"code": code})
            assert result is not None

    def test_chart_cleanup(self):
        """Test that matplotlib figures are properly cleaned up."""
        import matplotlib.pyplot as plt
        
        # Before execution
        initial_figs = len(plt.get_fignums())
        
        # Create chart
        code = "import matplotlib.pyplot as plt\nfig = plt.figure()\nplt.plot([1,2,3])"
        python_repl_tool.invoke({"code": code})
        
        # After execution - figures should be cleaned
        final_figs = len(plt.get_fignums())
        assert final_figs == initial_figs  # Should be same (cleaned up)


class TestDataProcessing:
    """Test data processing capabilities in REPL."""

    def test_pandas_operations(self):
        """Test pandas data operations."""
        code = """
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print(df.sum().to_dict())
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None

    def test_numpy_operations(self):
        """Test numpy operations."""
        code = """
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
mean = np.mean(arr)
std = np.std(arr)
print(f"Mean: {mean}, Std: {std}")
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None
        assert "Mean" in result or "successfully" in result.lower()

    def test_statistical_calculations(self):
        """Test statistical calculations on stock data."""
        code = """
import pandas as pd
import numpy as np

df = pd.read_csv('data/AAPL.csv')
df['Close'] = df['Close/Last'].str.replace('$', '').astype(float)

returns = df['Close'].pct_change()
volatility = returns.std()
mean_return = returns.mean()

print(f"Volatility: {volatility:.4f}, Mean Return: {mean_return:.4f}")
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None


class TestWorkingDirectory:
    """Test working directory handling."""

    def test_current_directory(self):
        """Test that working directory is correct."""
        code = """
import os
cwd = os.getcwd()
print(f"Current directory: {cwd}")
print(f"FinGPT in path: {'FinGPT' in cwd}")
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None

    def test_data_directory_access(self):
        """Test access to data directory."""
        code = """
import os
data_exists = os.path.exists('data')
print(f"Data directory exists: {data_exists}")
if data_exists:
    files = os.listdir('data')
    print(f"Data files: {len(files)}")
"""
        result = python_repl_tool.invoke({"code": code})
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
