# FinGPT Test Suite Documentation

## Overview

This directory contains comprehensive tests for the FinGPT multi-agent financial intelligence platform. The test suite covers all components including tools, agents, workflow, and end-to-end scenarios.

## Test Files

### 1. `test_analysis_tools.py`
Tests for quantitative analysis tools including:
- **Calculate Returns Tool**: Returns calculation, different time periods, invalid tickers
- **Calculate Volatility Tool**: Volatility metrics, annualized calculations
- **Compare Stocks Tool**: Stock comparisons, multiple pairs
- **Correlation Analysis Tool**: Correlation matrices, multiple stocks
- **Data Integrity**: CSV file validation, format checking

**Key Test Classes:**
- `TestCalculateReturnsTool`: 10+ tests for returns calculation
- `TestCalculateVolatilityTool`: 8+ tests for volatility analysis
- `TestCompareStocksTool`: 7+ tests for stock comparison
- `TestCorrelationAnalysisTool`: 8+ tests for correlation analysis
- `TestDataIntegrity`: CSV file validation tests

### 2. `test_data_tools.py`
Tests for data retrieval and research tools:
- **Stock Data Tool**: Data loading, time periods, error handling
- **Wikipedia Tool**: CEO searches, company information, edge cases
- **Tool Integration**: Workflow testing between tools
- **Error Handling**: Missing files, invalid inputs, network errors

**Key Test Classes:**
- `TestStockDataTool`: 10+ tests for stock data retrieval
- `TestWikipediaTool`: 10+ tests for Wikipedia searches
- `TestToolIntegration`: 5+ integration tests
- `TestErrorHandling`: 5+ error handling tests

### 3. `test_visualization_tools.py`
Tests for visualization and Python REPL tool:
- **Python REPL Tool**: Code execution, library imports, error handling
- **Chart Creation**: Matplotlib plots, stock visualizations
- **File Management**: Output directory, chart saving
- **Working Directory**: Path handling, data access

**Key Test Classes:**
- `TestPythonREPLTool`: 12+ tests for code execution
- `TestVisualizationOutput`: 5+ tests for chart creation
- `TestDataProcessing`: 5+ tests for pandas/numpy operations
- `TestWorkingDirectory`: Directory and path tests

### 4. `test_workflow.py`
Tests for multi-agent workflow and orchestration:
- **Agent Creation**: All agent initialization
- **Workflow Configuration**: Config management, memory
- **Agent Tools**: Tool availability and accessibility
- **State Management**: Conversation state, memory saver
- **Graph Structure**: Node connections, edges

**Key Test Classes:**
- `TestAgentCreation`: 4+ tests for agent initialization
- `TestWorkflowConfiguration`: 5+ tests for config
- `TestAgentTools`: 5+ tests for tool setup
- `TestStateManagement`: State and memory tests
- `TestGraphStructure`: Graph validation tests
- `TestErrorHandling`: Error recovery tests
- `TestConstants`: Configuration constant tests
- `TestDataLoader`: Data loading utility tests

### 5. `test_e2e.py`
End-to-end tests simulating real user scenarios:
- **User Scenarios**: Complete user interaction workflows
- **Error Recovery**: Typos, invalid inputs, edge cases
- **Data Consistency**: Multiple queries, all tickers
- **Performance**: Response time, sequential calls
- **Output Format**: Response structure validation

**Key Test Classes:**
- `TestUserScenarios`: 6+ realistic user scenarios
- `TestErrorRecovery`: 3+ error handling scenarios
- `TestDataConsistency`: 2+ consistency tests
- `TestPerformance`: 2+ performance tests
- `TestEdgeCases`: 5+ edge case tests
- `TestOutputFormat`: 3+ output validation tests

### 6. `test_tools.py`
Basic smoke tests for quick validation (legacy):
- Quick tool functionality checks
- Basic integration verification

## Running Tests

### Run All Tests
```bash
cd /home/ryhan/Downloads/workspace/FinGPT
python tests/run_tests.py --mode all
```

### Run Quick Tests
```bash
python tests/run_tests.py --mode quick
```

### Run Integration Tests Only
```bash
python tests/run_tests.py --mode integration
```

### Run Tool Tests Only
```bash
python tests/run_tests.py --mode tools
```

### Run Specific Test File
```bash
pytest tests/test_analysis_tools.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_analysis_tools.py::TestCalculateReturnsTool -v
```

### Run Specific Test Method
```bash
pytest tests/test_analysis_tools.py::TestCalculateReturnsTool::test_valid_returns_calculation -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

## Test Statistics

**Total Test Files**: 6
**Total Test Classes**: 30+
**Total Test Cases**: 150+

### Coverage by Component:
- **Analysis Tools**: 40+ tests
- **Data Tools**: 35+ tests  
- **Visualization Tools**: 25+ tests
- **Workflow/Agents**: 30+ tests
- **End-to-End**: 20+ tests

## Test Requirements

Required packages (already in `requirements.txt`):
- pytest
- pandas
- numpy
- matplotlib
- langchain ecosystem
- streamlit (for app tests)

## Test Data

Tests use CSV files in the `data/` directory:
- AAPL.csv
- AMZN.csv
- META.csv
- MSFT.csv
- NFLX.csv
- TSLA.csv

All test data files must have the following columns:
- Date
- Close/Last
- Volume
- Open
- High
- Low

## Environment Setup

For tests requiring API access (workflow tests):
```bash
export AI_API_KEY="your-openai-api-key"
```

Most tests work without API keys by testing local tool functionality.

## Test Patterns

### 1. Valid Input Tests
Test normal operation with valid inputs:
```python
def test_valid_calculation(self):
    result = tool.invoke({"param": "value"})
    assert "Expected" in result
```

### 2. Invalid Input Tests
Test error handling with invalid inputs:
```python
def test_invalid_ticker(self):
    result = tool.invoke({"ticker": "INVALID"})
    assert "not available" in result
```

### 3. Edge Case Tests
Test boundary conditions:
```python
def test_zero_days(self):
    result = tool.invoke({"days": 0})
    assert result is not None
```

### 4. Integration Tests
Test multiple components together:
```python
def test_workflow(self):
    result1 = tool1.invoke({...})
    result2 = tool2.invoke({...})
    assert both_work
```

## Continuous Integration

Add to CI/CD pipeline:
```yaml
test:
  script:
    - pip install -r requirements.txt
    - python tests/run_tests.py --mode all
```

## Troubleshooting

### Tests Fail with "FileNotFoundError"
- Ensure you're running tests from FinGPT root directory
- Check that `data/` directory exists with CSV files

### Tests Fail with "API Key Error"
- Some workflow tests need API key set
- Use mock/test API key for unit tests
- Skip integration tests if no API key available

### Import Errors
- Ensure all requirements are installed: `pip install -r requirements.txt`
- Check Python path includes project root

### Visualization Tests Fail
- Ensure matplotlib backend is set correctly (Agg for headless)
- Check `output/` directory permissions

## Contributing

When adding new features:
1. Write tests first (TDD)
2. Ensure >80% code coverage
3. Test both success and failure cases
4. Add edge case tests
5. Update this documentation

## Test Maintenance

- Review and update tests when APIs change
- Add new test cases for bug fixes
- Keep test data up to date
- Monitor test execution time
- Remove obsolete tests

## Contact

For questions about tests:
- Review test file docstrings
- Check inline comments
- See main README.md for project context
