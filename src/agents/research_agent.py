"""Research agent for gathering company information and stock data."""

import logging
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from src.tools import wikipedia_tool, stock_data_tool

logger = logging.getLogger(__name__)


def create_research_agent(llm: ChatOpenAI):
    """
    Create a research agent that can:
    - Search Wikipedia for company background and CEO information
    - Retrieve stock data from CSV files

    Args:
        llm: Language model to use for the agent

    Returns:
        Research agent instance
    """
    logger.info("[RESEARCH_AGENT] Creating research agent with wikipedia_tool and stock_data_tool")
    
    research_agent = create_react_agent(
        llm,
        tools=[wikipedia_tool, stock_data_tool],
        prompt=(
            "You are a research agent specialized in financial information gathering.\n\n"
            "INSTRUCTIONS:\n"
            "- Use wikipedia_tool to search for company information like CEO, founding, background.\n"
            "  * On success=true, extract the 'summary' field and present it naturally.\n"
            "  * On DisambiguationError, use the 'candidates' list to choose or ask for clarification.\n"
            "- Use stock_data_tool to retrieve historical stock price data.\n"
            "  * On success=true, present the 'data' field (which is a markdown table).\n"
            "- Convert company names to ticker symbols: Apple=AAPL, Tesla=TSLA, Microsoft=MSFT, "
            "Amazon=AMZN, Netflix=NFLX, Meta=META.\n"
            "- Convert time periods: 1 month = 30 days, 1 week = 7 days.\n"
            "- After using tools, provide a clear summary of the findings.\n"
            "- DO NOT perform calculations or create visualizations."
        ),
        name="researcher"
    )

    logger.info("[RESEARCH_AGENT] Research agent created successfully")
    return research_agent
