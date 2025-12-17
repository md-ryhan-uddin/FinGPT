"""Visualization specialist agent for creating charts and graphs."""

import logging
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from src.tools import python_repl_tool

logger = logging.getLogger(__name__)


def create_viz_agent(llm: ChatOpenAI):
    """
    Create a visualization specialist agent that can:
    - Generate matplotlib/seaborn charts
    - Create comparative visualizations
    - Execute Python code for data analysis

    Args:
        llm: Language model to use for the agent

    Returns:
        Visualization specialist agent instance
    """
    logger.info("[VIZ_AGENT] Creating visualization agent with python_repl_tool")
    
    viz_agent = create_react_agent(
        llm,
        tools=[python_repl_tool],
        prompt=(
            "You are a visualization specialist agent that creates charts and graphs.\n\n"
            "INSTRUCTIONS:\n"
            "- Create visualizations using python_repl_tool with matplotlib/pandas.\n"
            "- On success=true, extract chart file paths from the 'charts' field internally.\n"
            "- Present chart paths to the user in markdown format: ![Chart](path).\n"
            "- Use load_stock_dataframe('TICKER', days) to load and clean data (case-insensitive tickers).\n"
            "- The helper function returns a DataFrame with 'Date' and 'Close' columns ready to use.\n"
            "- Create ONE chart per request - don't retry if it works the first time.\n"
            "- Use plt.figure() to create charts. DO NOT use plt.show() or plt.savefig().\n"
            "- After creating the chart successfully, provide a brief description in natural language only.\n\n"
            "EXAMPLE CODE FOR STOCK PRICE CHART:\n"
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "df = load_stock_dataframe('META', 90)  # Load 90 days of data\n"
            "plt.figure(figsize=(10, 6))\n"
            "plt.plot(df['Date'], df['Close'], linewidth=2)\n"
            "plt.title('META Stock Price - 90 Days')\n"
            "plt.xlabel('Date')\n"
            "plt.ylabel('Price (USD)')\n"
            "plt.grid(True, alpha=0.3)\n"
            "plt.xticks(rotation=45)\n"
            "plt.tight_layout()\n"
            "```\n\n"
            "IMPORTANT: The tool automatically saves figures - you don't need to call savefig()!"
        ),
        name="viz_specialist"
    )

    logger.info("[VIZ_AGENT] Visualization agent created successfully")
    return viz_agent
