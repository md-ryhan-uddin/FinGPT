# 📈 FinGPT - Multi-Agent Financial Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3.27-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.5.3-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> An intelligent multi-agent system leveraging LangGraph supervisor pattern for comprehensive financial analysis

## 🌟 Overview

**FinGPT** is a production-grade agentic AI system that orchestrates multiple specialized agents to deliver comprehensive financial intelligence. Built with LangChain/LangGraph, it demonstrates advanced multi-agent coordination, tool integration, and state management - perfect for showcasing AI/ML engineering capabilities.

### Key Features

- 🤖 **Supervisor-Based Architecture** - 3 specialized agents coordinated by a portfolio manager supervisor
- 📊 **Automated Analysis** - Quantitative metrics, statistical analysis, and visualization generation
- 🔍 **Intelligent Research** - Integrated Wikipedia search and historical stock data retrieval
- 💬 **Conversational Interface** - Multi-turn conversations with context retention
- 📈 **Professional Reports** - Comprehensive financial insights and actionable recommendations

## 🏗️ Architecture

```
User Query → Portfolio Manager (Supervisor)
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
Research Agent  Quant Analyst  Viz Specialist
    │               │               │
Wikipedia       Returns         Charts &
Stock Data      Volatility      Visualizations
                Comparisons
    │               │               │
    └───────────────┴───────────────┘
                    ↓
            Synthesized Response
```

### Agent Roles

1. **Portfolio Manager (Supervisor)**
   - Orchestrates workflow and delegates tasks
   - Synthesizes insights from specialist agents
   - Provides final recommendations to users

2. **Research Agent**
   - Gathers company background from Wikipedia
   - Retrieves historical stock data from CSV
   - Provides factual context for analysis

3. **Quantitative Analyst**
   - Calculates returns and volatility metrics
   - Performs comparative stock analysis
   - Analyzes correlations between stocks

4. **Visualization Specialist**
   - Creates professional matplotlib charts
   - Generates comparative visualizations
   - Executes Python code for data exploration

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Git (for version control)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/md-ryhan-uddin/FinGPT.git
   cd FinGPT
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key:
   # AI_API_KEY=your_openai_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   Navigate to `http://localhost:8501`

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

### Available Stock Tickers

- **AAPL** - Apple Inc.
- **AMZN** - Amazon.com Inc.
- **META** - Meta Platforms Inc.
- **MSFT** - Microsoft Corporation
- **NFLX** - Netflix Inc.
- **TSLA** - Tesla Inc.

## 📁 Project Structure

```
FinGPT/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variable template
├── .gitignore                         # Git ignore rules
├── config.py                          # Configuration management
├── app.py                             # Main Streamlit application
│
├── src/
│   ├── agents/
│   │   ├── research_agent.py         # Wikipedia + stock data retrieval
│   │   ├── quant_agent.py            # Statistical analysis
│   │   ├── viz_agent.py              # Visualization creation
│   │   └── supervisor.py             # Supervisor orchestration
│   │
│   ├── tools/
│   │   ├── wikipedia_tool.py         # Wikipedia search tool
│   │   ├── stock_data_tool.py        # CSV data retrieval
│   │   ├── analysis_tools.py         # Quant analysis tools
│   │   └── visualization_tools.py    # Python REPL tool
│   │
│   ├── graph/
│   │   └── workflow.py               # LangGraph workflow
│   │
│   └── utils/
│       ├── constants.py              # Application constants
│       └── data_loader.py            # Data loading utilities
│
├── data/
│   └── *.csv                         # Historical stock data
│
└── tests/
    └── test_workflow.py              # Unit and integration tests
```

## 🛠️ Technical Highlights

### For Recruiters & Technical Reviewers

**Advanced Multi-Agent Orchestration**
- Supervisor pattern with dynamic task delegation
- State management across agent boundaries
- Conversation memory via LangGraph checkpointing

**Production-Quality Code**
- Modular architecture with clear separation of concerns
- Type hints and comprehensive docstrings
- Proper error handling and logging
- Environment-based configuration management

**LangGraph Expertise**
- Custom supervisor implementation using `langgraph-supervisor`
- InMemorySaver for multi-turn conversation context
- Proper tool integration with type annotations
- Agent handoff mechanisms

**Tool Engineering**
- 7 custom tools with proper LangChain annotations
- Tool chaining and data passing between agents
- Stateful tool execution (Python REPL)
- Robust error handling in tool implementations

**Real-World Application**
- Solves practical financial analysis problems
- Handles complex multi-step reasoning
- Produces actionable insights, not just chatbot responses

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 🔧 Development

### Adding New Tools

1. Create tool in `src/tools/` with `@tool` decorator
2. Add to appropriate agent in `src/agents/`
3. Update `src/tools/__init__.py` exports

### Adding New Agents

1. Create agent module in `src/agents/`
2. Use `create_react_agent()` from langgraph.prebuilt
3. Add to supervisor in `src/agents/supervisor.py`

## 📊 Tech Stack

- **Framework**: LangChain 0.3.27, LangGraph 0.5.3
- **LLM**: OpenAI GPT-4o-mini
- **UI**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Tools**: Wikipedia API, Python REPL

## 🎯 Future Enhancements

- [ ] Real-time market data integration (Alpha Vantage, Yahoo Finance)
- [ ] Advanced portfolio optimization algorithms
- [ ] ML-based price prediction models
- [ ] PDF report export functionality
- [ ] User authentication and personalized portfolios
- [ ] Deployment to Streamlit Cloud / Hugging Face Spaces
- [ ] Additional agent types (News Analyst, Risk Manager)
- [ ] Extended tool library (technical indicators, sentiment analysis)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Md. Ryhan Uddin**

- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- GitHub: [Your GitHub](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Built as a portfolio project demonstrating advanced agentic AI systems
- Inspired by DataCamp's LangChain/LangGraph course
- LangChain and LangGraph documentation and examples

## 📚 Learning Resources

This project demonstrates concepts from:
- Multi-agent system design
- LangGraph supervisor pattern
- Tool creation and integration
- State management in conversational AI
- Production-quality Python development

---

**⭐ If you find this project helpful, please consider giving it a star!**

Built with ❤️ using LangChain, LangGraph, and Streamlit
