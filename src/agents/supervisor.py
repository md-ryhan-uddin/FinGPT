"""Supervisor agent for orchestrating the multi-agent system."""

import logging
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from src.agents.research_agent import create_research_agent
from src.agents.quant_agent import create_quant_agent
from src.agents.viz_agent import create_viz_agent

logger = logging.getLogger(__name__)


# Define the supervisor routing function
class SupervisorState(MessagesState):
    next: str


def create_supervisor_node(llm: ChatOpenAI):
    """Create a supervisor node that routes to appropriate agents."""
    
    system_prompt = (
        "You are a portfolio manager supervising a team of financial analysts.\n\n"
        "Your team consists of:\n"
        "- **researcher**: Retrieves company information from Wikipedia and loads stock data from CSV files.\n"
        "- **quant_analyst**: Performs statistical analysis including returns, volatility, comparisons, and correlations.\n"
        "- **viz_specialist**: Creates charts and visualizations using Python code.\n\n"
        "INSTRUCTIONS:\n"
        "- Review the conversation and determine what work remains to be done.\n"
        "- If an agent has already completed the user's request, respond with 'FINISH'.\n"
        "- Otherwise, delegate to the appropriate agent: 'researcher', 'quant_analyst', or 'viz_specialist'.\n"
        "- For research tasks (company info, CEO, background), use 'researcher'.\n"
        "- For calculations (returns, volatility, comparisons, correlations), use 'quant_analyst'.\n"
        "- For charts and visualizations, use 'viz_specialist'.\n"
        "- Each task typically requires only ONE agent call - don't repeat calls unless necessary.\n"
        "- If you see tool execution results or analysis, that agent has completed its work - move to FINISH.\n"
        "- DO NOT loop back to the same agent if it has already provided results.\n"
        "- Respond with ONLY the agent name: 'researcher', 'quant_analyst', 'viz_specialist', or 'FINISH'."
    )
    
    def supervisor_node(state: SupervisorState):
        logger.info("[SUPERVISOR] Routing decision requested")
        logger.debug(f"[SUPERVISOR] Current state has {len(state['messages'])} messages")
        
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = llm.invoke(messages)
        next_agent = response.content.strip().lower()
        
        logger.info(f"[SUPERVISOR] Raw LLM response: '{next_agent}'")
        
        # Map agent names
        if "researcher" in next_agent:
            next_agent = "researcher"
        elif "quant" in next_agent:
            next_agent = "quant_analyst"
        elif "viz" in next_agent:
            next_agent = "viz_specialist"
        elif "finish" in next_agent:
            next_agent = "FINISH"
        else:
            next_agent = "FINISH"
        
        logger.info(f"[SUPERVISOR] Routing to: {next_agent}")
        return {"next": next_agent}
    
    return supervisor_node


def create_supervisor_graph(llm: ChatOpenAI):
    """
    Create the supervisor multi-agent system that orchestrates:
    - Research Agent: Gathers company info and stock data
    - Quant Analyst: Performs statistical analysis
    - Viz Specialist: Creates visualizations

    Args:
        llm: Language model to use for all agents

    Returns:
        Compiled supervisor graph with checkpointer
    """
    logger.info("[SUPERVISOR] Creating supervisor graph")
    
    # Create specialist agents
    research_agent = create_research_agent(llm)
    quant_agent = create_quant_agent(llm)
    viz_agent = create_viz_agent(llm)
    
    # Create supervisor node
    supervisor_node = create_supervisor_node(llm)
    
    # Wrap agents with logging to show when they're invoked
    def logged_research_agent(state):
        logger.info("🔍 [RESEARCH_AGENT] Invoked - Gathering company information and stock data...")
        result = research_agent.invoke(state)
        logger.info("✓ [RESEARCH_AGENT] Completed research task")
        return result
    
    def logged_quant_agent(state):
        logger.info("📊 [QUANT_AGENT] Invoked - Performing statistical analysis...")
        result = quant_agent.invoke(state)
        logger.info("✓ [QUANT_AGENT] Completed quantitative analysis")
        return result
    
    def logged_viz_agent(state):
        logger.info("📈 [VIZ_AGENT] Invoked - Creating visualizations...")
        result = viz_agent.invoke(state)
        logger.info("✓ [VIZ_AGENT] Completed visualization task")
        return result

    # Create checkpointer for conversation memory
    checkpointer = MemorySaver()
    
    # Build the graph
    workflow = StateGraph(SupervisorState)
    
    # Add nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", logged_research_agent)
    workflow.add_node("quant_analyst", logged_quant_agent)
    workflow.add_node("viz_specialist", logged_viz_agent)
    
    logger.info("[SUPERVISOR] Added 4 nodes: supervisor, researcher, quant_analyst, viz_specialist")
    
    # Add edges
    workflow.add_edge(START, "supervisor")
    
    # Conditional edges from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "researcher": "researcher",
            "quant_analyst": "quant_analyst",
            "viz_specialist": "viz_specialist",
            "FINISH": END
        }
    )
    
    # Agent edges back to supervisor
    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("quant_analyst", "supervisor")
    workflow.add_edge("viz_specialist", "supervisor")
    
    # Compile the graph
    graph = workflow.compile(checkpointer=checkpointer)

    logger.info("[SUPERVISOR] Supervisor graph compiled successfully with memory checkpointer")
    return graph
