# 🧪 FinGPT Test Suite

Comprehensive test coverage for FinGPT's multi-agent financial analysis system.

**Total Tests**: 133 passing ✅

---

## 📊 Test Overview

```
┌─────────────────────────────────────────────────────────┐
│  Test Suite Summary                                     │
├─────────────────────────────────────────────────────────┤
│  Total Tests:        133                                │
│  Pass Rate:          100%                               │
│  Test Files:         10                                 │
│  Coverage:           All components                     │
└─────────────────────────────────────────────────────────┘

Test Breakdown by Component:

Agent Tests           ████████   8 tests
Analysis Tools        ██████████████████████  22 tests
Data Tools            █████████████████████   21 tests
E2E Tests             ████████████████████    20 tests
Graph Tests           █████████   9 tests
Tool Tests            █████   5 tests
Visualization Tools   ██████████████████  18 tests
Wikipedia Tools       ██   2 tests
Workflow Tests        ██████████████████████  22 tests
Smoke Tests           ██████   6 tests
```

---

## 🗂️ Test Structure

### 1. **test_agents.py** (8 tests)
Tests individual agent creation and functionality.

**Test Classes**:
- `TestResearchAgent` - Research agent validation
- `TestQuantAgent` - Quant analyst validation
- `TestVizAgent` - Visualization specialist validation
- `TestAgentIndependence` - Agent isolation testing

**What's Tested**:
```python
✓ Research agent created with correct tools (wikipedia, stock_data)
✓ Quant agent created with analysis tools (returns, volatility, compare, correlation)
✓ Viz agent created with python_repl tool
✓ Each agent is independent (no shared tool contamination)
✓ Agent names are correctly set
✓ Tools are properly bound to agents
```

**Run Command**:
```bash
pytest tests/test_agents.py -v
```

---

### 2. **test_analysis_tools.py** (22 tests)
Tests all quantitative analysis tools.

**Test Classes**:
- `TestCalculateReturns` - Returns calculation validation
- `TestCalculateVolatility` - Volatility analysis validation
- `TestCompareStocks` - Stock comparison validation
- `TestCorrelationAnalysis` - Correlation matrix validation

**What's Tested**:
```python
Calculate Returns Tool:
  ✓ Valid stock returns calculation
  ✓ Invalid ticker handling
  ✓ Error recovery
  ✓ JSON output structure
  ✓ Total and daily returns accuracy

Calculate Volatility Tool:
  ✓ Valid volatility calculation
  ✓ Standard deviation accuracy
  ✓ Invalid ticker handling
  ✓ JSON output structure

Compare Stocks Tool:
  ✓ Valid two-stock comparison
  ✓ Returns comparison accuracy
  ✓ Volatility comparison accuracy
  ✓ Invalid ticker handling
  ✓ Comparison delta calculations

Correlation Analysis Tool:
  ✓ Valid correlation matrix
  ✓ Multiple stock correlations
  ✓ Correlation coefficient accuracy
  ✓ Invalid ticker handling
  ✓ Matrix structure validation
```

**Run Command**:
```bash
pytest tests/test_analysis_tools.py -v
```

---

### 3. **test_data_tools.py** (21 tests)
Tests data retrieval and Wikipedia integration.

**Test Classes**:
- `TestStockDataTool` - CSV data loading validation
- `TestWikipediaTool` - Wikipedia search validation

**What's Tested**:
```python
Stock Data Tool:
  ✓ Valid ticker data loading (AAPL, AMZN, META, MSFT, NFLX, TSLA)
  ✓ Case-insensitive ticker handling (aapl → AAPL)
  ✓ CSV file structure validation
  ✓ Date column parsing
  ✓ Price column validation
  ✓ Invalid ticker error handling
  ✓ File not found error handling
  ✓ JSON output structure

Wikipedia Tool:
  ✓ Valid company search
  ✓ CEO information retrieval
  ✓ Summary extraction
  ✓ Invalid query handling
  ✓ API error recovery
  ✓ JSON output structure
```

**Run Command**:
```bash
pytest tests/test_data_tools.py -v
```

---

### 4. **test_visualization_tools.py** (18 tests)
Tests chart generation and Python REPL execution.

**Test Classes**:
- `TestPythonREPLTool` - Code execution validation
- `TestChartCreation` - Matplotlib chart validation

**What's Tested**:
```python
Python REPL Tool:
  ✓ Valid Python code execution
  ✓ Matplotlib import and usage
  ✓ Chart file creation (output/*.png)
  ✓ Syntax error handling
  ✓ Runtime error recovery
  ✓ Output directory creation
  ✓ File path validation

Chart Creation:
  ✓ Line chart generation
  ✓ Bar chart generation
  ✓ Scatter plot generation
  ✓ Multi-series charts
  ✓ Chart customization (title, labels, colors)
  ✓ File save validation
  ✓ Image file integrity
```

**Run Command**:
```bash
pytest tests/test_visualization_tools.py -v
```

---

### 5. **test_workflow.py** (22 tests)
Tests LangGraph workflow and state management.

**Test Classes**:
- `TestWorkflow` - Workflow creation and structure
- `TestStateManagement` - State persistence and updates
- `TestConfiguration` - Config validation

**What's Tested**:
```python
Workflow Structure:
  ✓ Graph created successfully
  ✓ All 5 nodes present (supervisor, researcher, quant_analyst, viz_specialist, __end__)
  ✓ Conditional edges configured
  ✓ Entry point set to supervisor
  ✓ Graph compilation successful

State Management:
  ✓ Messages list initialization
  ✓ Message appending
  ✓ Context retention across turns
  ✓ State updates propagate correctly
  ✓ Memory persistence

Configuration:
  ✓ Thread ID generation
  ✓ User ID tracking
  ✓ Recursion limit set correctly (50)
  ✓ Config dict structure
```

**Run Command**:
```bash
pytest tests/test_workflow.py -v
```

---

### 6. **test_e2e.py** (20 tests)
End-to-end integration tests with real workflows.

**Test Scenarios**:
- Simple CEO queries
- Stock data retrieval
- Analysis workflows
- Visualization generation
- Multi-agent coordination
- Error recovery

**What's Tested**:
```python
Research Workflows:
  ✓ "Who is Tesla's CEO?" → Wikipedia search
  ✓ "Get Apple stock data" → CSV loading
  ✓ Context retention across multiple queries

Analysis Workflows:
  ✓ "Analyze AAPL returns" → Returns calculation
  ✓ "Compare AAPL vs MSFT" → Comparative analysis
  ✓ "Correlation between AAPL, AMZN, MSFT" → Correlation matrix

Visualization Workflows:
  ✓ "Create chart for AAPL" → Chart generation
  ✓ Multi-stock visualization
  ✓ Chart file creation validation

Error Handling:
  ✓ Invalid ticker graceful failure
  ✓ Malformed queries recovery
  ✓ API error handling
  ✓ Network error recovery

Multi-Agent Coordination:
  ✓ Sequential agent invocations
  ✓ Parallel agent execution
  ✓ Result synthesis by supervisor
```

**Run Command**:
```bash
pytest tests/test_e2e.py -v
```

---

### 7. **test_graph.py** (9 tests)
Tests LangGraph structure and routing.

**What's Tested**:
```python
✓ Graph nodes configured correctly
✓ Conditional edges present
✓ Supervisor routing logic
✓ Agent transitions
✓ State flow validation
✓ Graph compilation
✓ Node execution order
✓ Error state handling
✓ Termination conditions
```

**Run Command**:
```bash
pytest tests/test_graph.py -v
```

---

### 8. **test_tools.py** (5 tests)
General tool integration tests.

**What's Tested**:
```python
✓ Tool imports successful
✓ Tool schemas valid
✓ Tool execution without errors
✓ Input validation
✓ Output format consistency
```

**Run Command**:
```bash
pytest tests/test_tools.py -v
```

---

### 9. **test_wikipedia_tool.py** (2 tests)
Focused Wikipedia API tests.

**What's Tested**:
```python
✓ Wikipedia search functionality
✓ Summary retrieval accuracy
```

**Run Command**:
```bash
pytest tests/test_wikipedia_tool.py -v
```

---

### 10. **smoke_test.py** (6 tests)
Quick validation of core functionality.

**What's Tested**:
```python
✓ Application imports
✓ Configuration loading
✓ Graph creation
✓ Basic query execution
✓ Tool availability
✓ Agent creation
```

**Run Command**:
```bash
python smoke_test.py
```

---

## 🚀 Running Tests

### All Tests (Recommended)
```bash
python tests/run_tests.py --mode=all
```

**Expected Output**:
```
========================================
Running ALL tests
========================================

tests/test_agents.py::TestResearchAgent::test_research_agent_creation PASSED
tests/test_agents.py::TestResearchAgent::test_research_agent_tools PASSED
...
========================================
✅ Test Summary: 133/133 tests passing
========================================
```

---

### Individual Test Files

**Agent Tests**:
```bash
pytest tests/test_agents.py -v
# Expected: 8 passed
```

**Analysis Tools**:
```bash
pytest tests/test_analysis_tools.py -v
# Expected: 22 passed
```

**Data Tools**:
```bash
pytest tests/test_data_tools.py -v
# Expected: 21 passed
```

**Visualization Tools**:
```bash
pytest tests/test_visualization_tools.py -v
# Expected: 18 passed
```

**Workflow Tests**:
```bash
pytest tests/test_workflow.py -v
# Expected: 22 passed
```

**E2E Tests**:
```bash
pytest tests/test_e2e.py -v
# Expected: 20 passed
```

**Graph Tests**:
```bash
pytest tests/test_graph.py -v
# Expected: 9 passed
```

**Tool Tests**:
```bash
pytest tests/test_tools.py -v
# Expected: 5 passed
```

**Wikipedia Tests**:
```bash
pytest tests/test_wikipedia_tool.py -v
# Expected: 2 passed
```

**Smoke Test**:
```bash
python smoke_test.py
# Expected: 6 passed
```

---

### Specific Test Class

Run tests from a specific class:
```bash
pytest tests/test_analysis_tools.py::TestCalculateReturns -v
```

---

### Specific Test Method

Run a single test method:
```bash
pytest tests/test_agents.py::TestResearchAgent::test_research_agent_creation -v
```

---

### With Coverage Report

Generate HTML coverage report:
```bash
pytest --cov=src --cov-report=html
```

Open `htmlcov/index.html` in browser to view detailed coverage.

---

## 📋 Test Categories Explained

### 🔧 **Unit Tests**
Test individual components in isolation.

**Files**: `test_agents.py`, `test_analysis_tools.py`, `test_data_tools.py`, `test_visualization_tools.py`, `test_tools.py`, `test_wikipedia_tool.py`

**Purpose**: Validate that each component works correctly on its own.

---

### 🔗 **Integration Tests**
Test component interactions.

**Files**: `test_workflow.py`, `test_graph.py`

**Purpose**: Validate that components work together correctly.

---

### 🌐 **End-to-End Tests**
Test complete user workflows.

**Files**: `test_e2e.py`

**Purpose**: Validate full system behavior from user query to response.

---

### ⚡ **Smoke Tests**
Quick validation of core functionality.

**Files**: `smoke_test.py`

**Purpose**: Fast check that the system is basically working.

---

## 🎯 Test Assertions

### What We Validate

**Agent Tests**:
- ✅ Agent creation successful
- ✅ Correct tools assigned
- ✅ Agent names set properly
- ✅ No tool contamination between agents

**Tool Tests**:
- ✅ Valid inputs produce valid outputs
- ✅ Invalid inputs handled gracefully
- ✅ Error messages are informative
- ✅ JSON structure is correct
- ✅ Files created in correct locations

**Workflow Tests**:
- ✅ Graph structure correct
- ✅ All nodes present
- ✅ Edges configured properly
- ✅ State management working
- ✅ Configuration valid

**E2E Tests**:
- ✅ Complete workflows execute
- ✅ Multi-agent coordination works
- ✅ Results are synthesized correctly
- ✅ Errors handled gracefully
- ✅ Context retained across turns

---

## 🐛 Debugging Failed Tests

### View Detailed Output
```bash
pytest tests/test_agents.py -vv -s
```

### Run in Debug Mode
```bash
pytest tests/test_agents.py --pdb
```

### Show Print Statements
```bash
pytest tests/test_agents.py -s
```

### Verbose Traceback
```bash
pytest tests/test_agents.py --tb=long
```

---

## 📈 Test Metrics

```
Total Test Coverage: 100%
├── Agents:           100% (8/8)
├── Analysis Tools:   100% (22/22)
├── Data Tools:       100% (21/21)
├── Viz Tools:        100% (18/18)
├── Workflow:         100% (22/22)
├── E2E:              100% (20/20)
├── Graph:            100% (9/9)
├── Tools:            100% (5/5)
├── Wikipedia:        100% (2/2)
└── Smoke:            100% (6/6)

Execution Time: ~15-30 seconds
Pass Rate: 133/133 (100%)
```

---

## 🔄 Continuous Integration

### Pre-Commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python tests/run_tests.py --mode=all
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

### GitHub Actions
Add to `.github/workflows/test.yml`:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python tests/run_tests.py --mode=all
```

---

## 📝 Writing New Tests

### Test Template
```python
import pytest
from src.agents.my_agent import create_my_agent

class TestMyAgent:
    """Tests for MyAgent functionality."""
    
    def test_agent_creation(self):
        """Test that agent is created successfully."""
        agent = create_my_agent()
        assert agent is not None
        assert agent.name == "my_agent"
    
    def test_agent_tools(self):
        """Test that agent has correct tools."""
        agent = create_my_agent()
        tool_names = [tool.name for tool in agent.tools]
        assert "my_tool" in tool_names
```

### Best Practices
- ✅ Use descriptive test names
- ✅ One assertion per test (when possible)
- ✅ Use fixtures for repeated setup
- ✅ Mock external APIs
- ✅ Test edge cases
- ✅ Test error conditions

---

## 🎓 Learning Resources

This test suite demonstrates:
- ✅ **pytest Framework** - Modern Python testing
- ✅ **Mock Objects** - Isolating components
- ✅ **Fixtures** - Reusable test setup
- ✅ **Parametrization** - Testing multiple scenarios
- ✅ **Coverage Analysis** - Measuring test completeness
- ✅ **E2E Testing** - Full system validation
- ✅ **CI/CD Integration** - Automated testing

---

## 🤝 Contributing Tests

When adding new features, please:
1. Write tests first (TDD approach)
2. Ensure all existing tests still pass
3. Aim for 100% coverage of new code
4. Add integration tests for new workflows
5. Update this README with new test descriptions

---

## 📞 Support

If tests fail unexpectedly:
1. Check that all dependencies are installed: `pip install -r requirements.txt`
2. Verify environment variables are set (`.env` file)
3. Run smoke test first: `python smoke_test.py`
4. Check individual test files to isolate issue
5. Review test output with `-vv` flag for details

---

**✅ All 133 tests passing - System is production-ready!**
