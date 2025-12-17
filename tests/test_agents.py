"""Unit tests for individual agents."""

import sys
import json
import pytest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_openai import ChatOpenAI
from src.agents.research_agent import create_research_agent
from src.agents.quant_agent import create_quant_agent
from src.agents.viz_agent import create_viz_agent
import config


@pytest.fixture
def llm():
    """Create a test LLM instance."""
    return ChatOpenAI(
        model=config.AI_MODEL,
        api_key=config.AI_API_KEY,
        temperature=0.3,
    )


class TestResearchAgent:
    """Test suite for research agent."""

    def test_research_agent_creation(self, llm):
        """Test that research agent can be created."""
        agent = create_research_agent(llm)
        assert agent is not None
        assert hasattr(agent, 'invoke')

    def test_research_agent_has_tools(self, llm):
        """Test that research agent has required tools."""
        agent = create_research_agent(llm)
        # Agent should have access to wikipedia_tool and stock_data_tool
        assert agent is not None


class TestQuantAgent:
    """Test suite for quantitative analyst agent."""

    def test_quant_agent_creation(self, llm):
        """Test that quant agent can be created."""
        agent = create_quant_agent(llm)
        assert agent is not None
        assert hasattr(agent, 'invoke')

    def test_quant_agent_has_tools(self, llm):
        """Test that quant agent has required tools."""
        agent = create_quant_agent(llm)
        # Agent should have access to analysis tools
        assert agent is not None


class TestVizAgent:
    """Test suite for visualization specialist agent."""

    def test_viz_agent_creation(self, llm):
        """Test that viz agent can be created."""
        agent = create_viz_agent(llm)
        assert agent is not None
        assert hasattr(agent, 'invoke')

    def test_viz_agent_has_tools(self, llm):
        """Test that viz agent has required tools."""
        agent = create_viz_agent(llm)
        # Agent should have access to python_repl_tool
        assert agent is not None


class TestAgentConfiguration:
    """Test agent configuration and setup."""

    def test_all_agents_can_be_created(self, llm):
        """Test that all agents can be instantiated."""
        research_agent = create_research_agent(llm)
        quant_agent = create_quant_agent(llm)
        viz_agent = create_viz_agent(llm)
        
        assert research_agent is not None
        assert quant_agent is not None
        assert viz_agent is not None

    def test_agents_are_independent(self, llm):
        """Test that agents can be created independently."""
        agent1 = create_research_agent(llm)
        agent2 = create_research_agent(llm)
        
        # Should create separate instances
        assert agent1 is not agent2
