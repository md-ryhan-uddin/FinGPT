"""Wikipedia search tool for retrieving company and market information."""

from typing import Annotated
import wikipedia
from langchain_core.tools import tool


@tool
def wikipedia_tool(
    query: Annotated[str, "The Wikipedia search to execute to find key summary information."],
) -> str:
    """Use this to search Wikipedia for factual information about companies, CEOs, and market context."""
    try:
        # Step 1: Search using query
        results = wikipedia.search(query)

        if not results:
            return "No results found on Wikipedia."

        # Step 2: Retrieve page title
        title = results[0]

        # Step 3: Fetch summary
        summary = wikipedia.summary(title, sentences=8, auto_suggest=False, redirect=True)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"

    return f"Successfully executed:\nWikipedia summary: {summary}"
