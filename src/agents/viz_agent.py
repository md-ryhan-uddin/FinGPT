"""Visualization specialist agent for creating charts and graphs."""

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from src.tools import python_repl_tool


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
    viz_agent = create_react_agent(
        llm,
        tools=[python_repl_tool],
        prompt=(
            "You are a visualization specialist agent that creates charts and graphs.\n\n"
            "INSTRUCTIONS:\n"
            "- Create visualizations using python_repl_tool with matplotlib/pandas.\n"
            "- CSV files in data/ have these columns: Date, Close/Last, Volume, Open, High, Low\n"
            "- IMPORTANT: Use 'Close/Last' column (not 'Close'), or rename it first\n"
            "- Clean dollar signs: df['Close/Last'] = df['Close/Last'].str.replace('$','').astype(float)\n"
            "- Create ONE chart per request - don't retry if it works the first time.\n"
            "- Use plt.figure() to create charts. DO NOT use plt.show() or plt.savefig().\n"
            "- After creating the chart successfully, provide a brief description.\n"
            "- DO NOT try to print dataframes or debug - just create the chart."
        ),
        name="viz_specialist"
    )

    return viz_agent
