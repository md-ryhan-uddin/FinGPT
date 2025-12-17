"""Wikipedia search tool for retrieving company and market information.

This tool now returns a structured JSON string with the following keys:
  - success: bool
  - query: the original query string passed to the tool
  - title: the Wikipedia page title selected (if any)
  - summary: the page summary (if success)
  - error: error message when success is false
  - candidates: list of candidate titles when a DisambiguationError occurs
"""

from typing import Annotated
import json
import logging
import wikipedia
from wikipedia import DisambiguationError, PageError

# Configure logger
logger = logging.getLogger(__name__)
from langchain_core.tools import tool


@tool
def wikipedia_tool(
    query: Annotated[str, "The Wikipedia search to execute to find key summary information."],
) -> str:
    """Use this to search Wikipedia for factual information about companies, CEOs, and market context.

    Returns a JSON string with structured fields so callers can parse results programmatically.
    """
    logger.info(f"[WIKIPEDIA_TOOL] Input: query='{query}'")
    
    result = {
        "success": False,
        "query": query,
        "title": None,
        "summary": None,
        "error": None,
        "candidates": None,
    }

    try:
        # Step 1: Search using query
        results = wikipedia.search(query)

        if not results:
            result["error"] = "No results found on Wikipedia."
            return json.dumps(result)

        # Step 2: Retrieve page title (top search result)
        title = results[0]
        result["title"] = title

        # Step 3: Fetch summary (handle disambiguation/page errors explicitly)
        try:
            summary = wikipedia.summary(title, sentences=8, auto_suggest=False, redirect=True)
            result["summary"] = summary
            result["success"] = True
            logger.info(f"[WIKIPEDIA_TOOL] Success: Retrieved summary for '{title}' ({len(summary)} chars)")
        except DisambiguationError as e:
            # Provide the list of candidate titles so the caller/agent can disambiguate
            result["candidates"] = getattr(e, "options", []) or list(e)
            result["error"] = "DisambiguationError: multiple possible pages returned."
            logger.warning(f"[WIKIPEDIA_TOOL] DisambiguationError: Found {len(result['candidates'])} candidates for '{title}'")
        except PageError as e:
            result["error"] = f"PageError: {repr(e)}"
            logger.warning(f"[WIKIPEDIA_TOOL] PageError for '{title}': {e}")

    except Exception as e:
        # Catch other exceptions (network, etc.) and return structured error
        result["error"] = repr(e)
        logger.error(f"[WIKIPEDIA_TOOL] Exception: {e}")

    logger.info(f"[WIKIPEDIA_TOOL] Output: success={result['success']}, error={result['error']}")
    return json.dumps(result)
