"""LangGraph workflow creation and initialization."""

import logging
from langchain_openai import ChatOpenAI
from src.agents.supervisor import create_supervisor_graph
import config

logger = logging.getLogger(__name__)


def create_workflow():
    """
    Create and compile the FinGPT multi-agent workflow.

    Returns:
        Compiled supervisor graph ready for execution
    """
    logger.info("[WORKFLOW] Initializing FinGPT multi-agent system...")
    
    # Initialize language model
    llm = ChatOpenAI(
        model=config.AI_MODEL,
        api_key=config.AI_API_KEY,
        temperature=0.3,
    )

    # Create supervisor graph with all agents
    logger.info("[WORKFLOW] Creating supervisor graph with 3 specialist agents...")
    graph = create_supervisor_graph(llm)
    
    logger.info("[WORKFLOW] Multi-agent system ready!")
    return graph


# Create the graph instance for import
graph = create_workflow()

# Thread configuration for conversations
def get_config(thread_id: str = "1", user_id: str = "1"):
    """
    Get configuration for graph execution.

    Args:
        thread_id: Conversation thread identifier
        user_id: User identifier

    Returns:
        Config dictionary for graph execution
    """
    return {
        "configurable": {
            "thread_id": thread_id,
            "user_id": user_id
        },
        "recursion_limit": 50  # Increased from default 25 to allow more agent interactions
    }
