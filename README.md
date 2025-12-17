# 📈 FinGPT - Multi-Agent Financial Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3.27-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.5.3-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-127%20Passing-brightgreen.svg)

> An intelligent multi-agent system leveraging LangGraph supervisor pattern for comprehensive financial analysis

## 🚀 **[Try Live Demo →](https://fin-gpt.streamlit.app/)**

---

## 🌟 Overview

**FinGPT** is a production-grade agentic AI system that orchestrates multiple specialized agents to deliver comprehensive financial intelligence. Built with LangChain/LangGraph, it demonstrates advanced multi-agent coordination, tool integration, and state management - perfect for showcasing AI/ML engineering capabilities.

### 🎯 Key Features

- 🤖 **Supervisor-Based Architecture** - 3 specialized agents coordinated by a portfolio manager supervisor
- 📊 **Automated Analysis** - Quantitative metrics, statistical analysis, and visualization generation
- 🔍 **Intelligent Research** - Integrated Wikipedia search and historical stock data retrieval
- 💬 **Conversational Interface** - Multi-turn conversations with context retention
- 🧠 **Reasoning Flow Viewer** - Real-time visibility into agent routing and tool usage (like ChatGPT's "View Analysis")
- 📈 **Professional Reports** - Comprehensive financial insights and actionable recommendations
- 📝 **Comprehensive Logging** - Full visibility into agent decisions and tool executions
- ✅ **100% Test Coverage** - 133 passing tests across all components

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│                  (Streamlit Chat UI)                         │
└────────────────────────┬─────────────────────────────────────┘
                         │ User Query
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                   SUPERVISOR AGENT                           │
│             (Portfolio Manager/Orchestrator)                 │
│                                                              │
│  • Analyzes user intent                                      │
│  • Routes to appropriate specialist                          │
│  • Synthesizes final response                                │
└───┬──────────────────┬──────────────────┬─────────────-──────┘
    │                  │                  │
    │ Delegate         │ Delegate         │ Delegate
    ▼                  ▼                  ▼
┌─────────┐    ┌──────────────┐    ┌────────────────┐
│RESEARCH │    │QUANT ANALYST │    │VIZ SPECIALIST  │
│ AGENT   │    │   AGENT      │    │    AGENT       │
└────┬────┘    └──────┬───────┘    └───────┬────────┘
     │                │                     │
     │ Tools:         │ Tools:              │ Tools:
     │ • Wikipedia    │ • Returns           │ • Python REPL
     │ • Stock Data   │ • Volatility        │ • Matplotlib
     │                │ • Compare           │ • Charts
     │                │ • Correlation       │
     ▼                ▼                     ▼
┌──────────────────────────────────────────────────────────────┐
│                   DATA & OUTPUT LAYER                        │
│  • CSV Files (Historical Stock Data)                         │
│  • Generated Charts (PNG)                                    │
│  • API Responses (Wikipedia)                                 │
└──────────────────────────────────────────────────────────────┘
     │                │                     │
     │ Results        │ Results             │ Results
     └────────────────┴─────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│              SUPERVISOR - FINAL SYNTHESIS                    │
│  • Aggregates specialist outputs                             │
│  • Generates coherent final response                         │
│  • Presents to user via UI                                   │
└──────────────────────────────────────────────────────────────┘
```

### Agent Roles & Responsibilities

```
┌──────────────────────────────────────────────────────────────┐
│  🎯 Portfolio Manager (Supervisor)                           │
│  ├─ Analyzes user query                                      │
│  ├─ Routes to appropriate specialist agent                   │
│  ├─ Synthesizes results from multiple agents                 │
│  └─ Delivers final recommendation                            │
└──────────────────────────────────────────────────────────────┘
                     │
    ┌────────────────┼────────────────────┐
    │                │                    │
    ▼                ▼                    ▼
┌────────────┐ ┌──────────────┐ ┌────────────────────┐
│ 🔍 Research│ │ 📊 Quant     │ │ 📈 Viz             │
│    Agent   │ │   Analyst    │ │   Specialist       │
└────────────┘ └──────────────┘ └────────────────────┘
    │                │                  │
    ▼                ▼                  ▼
┌────────────┐ ┌──────────────┐ ┌────────────────────┐
│ Wikipedia  │ │ Calculate    │ │ Matplotlib Charts  │
│ CSV Data   │ │ Analyze      │ │                    │
└────────────┘ └──────────────┘ └────────────────────┘
```

### Component Details

#### 1. **Portfolio Manager (Supervisor)** 🎯
- **Role**: Orchestrates workflow and delegates tasks
- **Intelligence**: Uses GPT-4o-mini to analyze queries and route to specialists
- **Features**:
  - Context-aware task delegation
  - Multi-agent coordination
  - Result synthesis
  - Conversation memory management

#### 2. **Research Agent** 🔍
- **Role**: Gathers factual information
- **Tools**:
  - `wikipedia_tool` - Searches Wikipedia for company/CEO information
  - `stock_data_tool` - Loads historical stock data from CSV files
- **Output**: JSON-structured data with company background and stock prices

#### 3. **Quantitative Analyst** 📊
- **Role**: Performs statistical analysis
- **Tools**:
  - `calculate_returns_tool` - Computes total and daily returns
  - `calculate_volatility_tool` - Analyzes price volatility
  - `compare_stocks_tool` - Side-by-side stock comparisons
  - `correlation_analysis_tool` - Correlation matrices
- **Output**: JSON-structured metrics and insights

#### 4. **Visualization Specialist** 📈
- **Role**: Creates charts and visualizations
- **Tools**:
  - `python_repl_tool` - Executes matplotlib code
- **Output**: PNG charts saved to `output/` directory

---

## 🚀 Quick Start

### Prerequisites

```bash
- Python 3.9 or higher
- OpenAI API key
- Git (for version control)
```

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/md-ryhan-uddin/FinGPT.git
cd FinGPT
```

**2. Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API key:
# AI_API_KEY=your_openai_api_key_here
```

**5. Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 💡 Usage Examples

### Example 1: CEO Research
**User**: "Who is Tesla's CEO?"

**System Flow**:
```
User Query → Supervisor → Research Agent → Wikipedia Tool
                                         ↓
                                    Elon Musk info
                                         ↓
                                    Supervisor → User
```

### Example 2: Stock Analysis
**User**: "Analyze Apple's stock performance over the last 30 days"

**System Flow**:
```
User Query → Supervisor → Research Agent → Stock Data Tool
                       → Quant Analyst → Returns + Volatility
                                         ↓
                                    Comprehensive Analysis
                                         ↓
                                    Supervisor → User
```

### Example 3: Comparative Visualization
**User**: "Compare AAPL vs MSFT performance and create a chart"

**System Flow**:
```
User Query → Supervisor → Quant Analyst → Compare Stocks
                       → Viz Specialist → Create Chart
                                         ↓
                                    Chart + Analysis
                                         ↓
                                    Supervisor → User
```

---

## 📁 Project Structure

```
FinGPT/
│
├── app.py                          # Streamlit application entry point
├── config.py                       # Configuration and environment variables
├── requirements.txt                # Python dependencies
│
├── src/                            # Source code
│   ├── agents/                     # Agent definitions
│   │   ├── research_agent.py       # Research specialist
│   │   ├── quant_agent.py          # Quantitative analyst
│   │   ├── viz_agent.py            # Visualization specialist
│   │   └── supervisor.py           # Supervisor orchestrator
│   │
│   ├── tools/                      # Tool implementations
│   │   ├── wikipedia_tool.py       # Wikipedia search
│   │   ├── stock_data_tool.py      # CSV data loader
│   │   ├── analysis_tools.py       # Statistical analysis
│   │   └── visualization_tools.py  # Chart generation
│   │
│   ├── graph/                      # LangGraph workflow
│   │   └── workflow.py             # Graph creation and config
│   │
│   └── utils/                      # Utilities
│       ├── constants.py            # Constants and mappings
│       └── data_loader.py          # Data loading helpers
│
├── data/                           # Stock price data (CSV)
│   ├── AAPL.csv
│   ├── AMZN.csv
│   ├── META.csv
│   ├── MSFT.csv
│   ├── NFLX.csv
│   └── TSLA.csv
│
├── tests/                          # Comprehensive test suite
│   ├── test_agents.py              # Agent tests
│   ├── test_analysis_tools.py      # Analysis tool tests
│   ├── test_data_tools.py          # Data tool tests
│   ├── test_e2e.py                 # End-to-end tests
│   ├── test_graph.py               # Graph structure tests
│   ├── test_tools.py               # General tool tests
│   ├── test_visualization_tools.py # Viz tool tests
│   ├── test_workflow.py            # Workflow tests
│   ├── smoke_test.py               # Quick smoke tests
│   └── run_tests.py                # Test runner
│
├── output/                         # Generated charts
└── assets/                         # Static assets
```

---

## 🧪 Testing

### Run All Tests
```bash
python tests/run_tests.py --mode=all
```

**Results**: ✅ 133/133 tests passing

### Run Individual Test Suites
```bash
# Agent tests
pytest tests/test_agents.py -v

# Tool tests
pytest tests/test_analysis_tools.py -v

# End-to-end tests
pytest tests/test_e2e.py -v

# Quick smoke test
python smoke_test.py
```

### Test Coverage
- **Agent Tests**: 8 tests - Agent creation, tool assignment, independence
- **Analysis Tools**: 22 tests - Returns, volatility, comparisons, correlations
- **Data Tools**: 21 tests - Stock data retrieval, Wikipedia search, error handling
- **Visualization Tools**: 18 tests - Chart creation, code execution, file management
- **Workflow Tests**: 22 tests - Graph structure, configuration, state management
- **E2E Tests**: 20 tests - Real user scenarios, error recovery, performance
- **Smoke Tests**: 6 tests - Quick validation of core functionality

---

## 📊 Logging & Debugging

### View Logs in Real-Time

When you run the app, comprehensive logs appear in your terminal:

```bash
streamlit run app.py
```

**Example Log Output**:
```
2025-12-17 12:43:49 - __main__ - INFO - [APP] Starting FinGPT application
2025-12-17 12:43:49 - src.graph.workflow - INFO - [WORKFLOW] Initializing multi-agent system
2025-12-17 12:43:49 - src.agents.supervisor - INFO - [SUPERVISOR] Creating supervisor graph
2025-12-17 12:43:49 - src.agents.research_agent - INFO - [RESEARCH_AGENT] Creating research agent
2025-12-17 12:43:49 - src.agents.quant_agent - INFO - [QUANT_AGENT] Creating quant agent
2025-12-17 12:43:49 - src.agents.viz_agent - INFO - [VIZ_AGENT] Creating viz agent
2025-12-17 12:43:50 - src.agents.supervisor - INFO - [SUPERVISOR] Routing to: researcher
2025-12-17 12:43:52 - src.tools.wikipedia_tool - INFO - [WIKIPEDIA_TOOL] Input: query='Apple CEO'
2025-12-17 12:43:54 - src.tools.wikipedia_tool - INFO - [WIKIPEDIA_TOOL] Success: Retrieved summary
2025-12-17 12:43:55 - src.agents.supervisor - INFO - [SUPERVISOR] Routing to: FINISH
```

**Log Components**:
- `[APP]` - Application-level events
- `[WORKFLOW]` - Graph initialization
- `[SUPERVISOR]` - Routing decisions
- `[RESEARCH_AGENT]` - Research operations
- `[QUANT_AGENT]` - Analysis operations
- `[VIZ_AGENT]` - Visualization operations
- `[WIKIPEDIA_TOOL]` - Wikipedia searches
- `[STOCK_DATA_TOOL]` - Data loading
- `[CALCULATE_*]` - Analysis calculations
- `[PYTHON_REPL]` - Code execution

---

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
# OpenAI API Configuration
AI_API_KEY=your_api_key_here
AI_MODEL=model-name

# Optional: Adjust LLM temperature (0.0-1.0)
# Lower = more focused, Higher = more creative
TEMPERATURE=0.3
```

### Available Stock Tickers
- **AAPL** - Apple Inc.
- **AMZN** - Amazon.com Inc.
- **META** - Meta Platforms Inc.
- **MSFT** - Microsoft Corporation
- **NFLX** - Netflix Inc.
- **TSLA** - Tesla Inc.

### Adding New Stocks
1. Place CSV file in `data/` directory (format: `TICKER.csv`)
2. CSV must have columns: Date, Close/Last, Volume, Open, High, Low
3. Update `src/utils/constants.py` with the new ticker

---



## 💡 Usage Examples

### Example Queries

```
"Who is Apple's CEO?"
→ Research agent retrieves Wikipedia information about Tim Cook

"Analyze Tesla's stock performance over the last month"
→ Research agent loads data → Quant agent calculates metrics → Supervisor synthesizes

"Compare Apple vs Microsoft returns over 90 days"
→ Quant agent performs comparative analysis with detailed metrics

"Show me a chart of Meta's stock price over the last quarter"
→ Research agent loads data → Viz specialist creates price chart

"Calculate volatility for Netflix and explain what it means"
→ Quant agent calculates volatility with interpretation

"Which tech stock has better risk-adjusted returns: AAPL or MSFT?"
→ Full multi-agent workflow with research, analysis, and recommendations
```


## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|----------|
| **LLM** | OpenAI GPT-4o-mini | Agent reasoning & responses |
| **Framework** | LangChain 0.3.27 | Tool abstraction & chains |
| **Orchestration** | LangGraph 0.5.3 | Multi-agent workflow |
| **UI** | Streamlit | Interactive web interface |
| **Data** | Pandas, NumPy | CSV processing & analysis |
| **Visualization** | Matplotlib | Chart generation |
| **Testing** | Pytest | 133 comprehensive tests |

---

## 👨‍💻 Author

**Md Ryhan Uddin**
- GitHub: [@md-ryhan-uddin](https://github.com/md-ryhan-uddin)

---

**⭐ Star this repo if you find it helpful!**
