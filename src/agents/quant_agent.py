"""Quantitative analyst agent for statistical analysis of stock data."""

import logging
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from src.tools import (
    calculate_returns_tool,
    calculate_volatility_tool,
    compare_stocks_tool,
    correlation_analysis_tool,
)

logger = logging.getLogger(__name__)


def create_quant_agent(llm: ChatOpenAI):
    """
    Create a quantitative analyst agent that can:
    - Calculate returns and volatility
    - Compare multiple stocks
    - Analyze correlations

    Args:
        llm: Language model to use for the agent

    Returns:
        Quantitative analyst agent instance
    """
    logger.info("[QUANT_AGENT] Creating quant agent with 4 analysis tools")
    
    quant_agent = create_react_agent(
        llm,
        tools=[
            calculate_returns_tool,
            calculate_volatility_tool,
            compare_stocks_tool,
            correlation_analysis_tool,
        ],
        prompt=(
            "You are a quantitative analyst agent specialized in statistical financial analysis.\n\n"
            "INSTRUCTIONS:\n"
            "- Perform quantitative analysis on stock data using the available tools.\n"
            "- Use the appropriate tool for the task: calculate_volatility_tool, calculate_returns_tool, "
            "compare_stocks_tool, or correlation_analysis_tool.\n"
            "- On success=true, extract the 'metrics' (or 'comparison'/'correlation_matrix') and format nicely.\n"
            "- On success=false, check the 'error' field and explain the issue in plain English.\n"
            "- For Netflix, use ticker 'NFLX'. For Apple use 'AAPL', Tesla use 'TSLA', etc.\n"
            "- Convert time periods: 1 month = 30 days, 1 week = 7 days, 90 days = 90 days.\n"
            "- After executing the tool, provide a brief summary of the results.\n"
            "- DO NOT make multiple tool calls unless explicitly needed.\n"
            "- Format output with clear headers, bullet points, and formatted numbers (e.g., 20.67%, $241.84).\n"
            "- Present results clearly and concisely in natural language ONLY."
        ),
        name="quant_analyst"
    )

    logger.info("[QUANT_AGENT] Quant agent created successfully")
    return quant_agent
