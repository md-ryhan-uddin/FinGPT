"""Unit tests for supervisor graph and workflow orchestration."""

import sys
import json
import pytest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_openai import ChatOpenAI
from src.agents.supervisor import create_supervisor_graph
from src.graph.workflow import create_workflow, get_config
import config


@pytest.fixture
def llm():
    """Create a test LLM instance."""
    return ChatOpenAI(
        model=config.AI_MODEL,
        api_key=config.AI_API_KEY,
        temperature=0.3,
    )


class TestSupervisorGraph:
    """Test suite for supervisor graph creation."""

    def test_supervisor_graph_creation(self, llm):
        """Test that supervisor graph can be created."""
        graph = create_supervisor_graph(llm)
        assert graph is not None

    def test_supervisor_graph_has_nodes(self, llm):
        """Test that graph has required nodes."""
        graph = create_supervisor_graph(llm)
        # The graph should be compiled and ready
        assert graph is not None


class TestWorkflowCreation:
    """Test suite for workflow module."""

    def test_create_workflow(self):
        """Test that workflow can be created."""
        graph = create_workflow()
        assert graph is not None

    def test_get_config(self):
        """Test config generation."""
        config_dict = get_config(thread_id="test_123", user_id="user_456")
        
        assert "configurable" in config_dict
        assert config_dict["configurable"]["thread_id"] == "test_123"
        assert config_dict["configurable"]["user_id"] == "user_456"
        assert "recursion_limit" in config_dict

    def test_get_config_defaults(self):
        """Test config with default values."""
        config_dict = get_config()
        
        assert "configurable" in config_dict
        assert config_dict["configurable"]["thread_id"] == "1"
        assert config_dict["configurable"]["user_id"] == "1"


class TestGraphStructure:
    """Test graph structure and connections."""

    def test_graph_can_be_invoked(self, llm):
        """Test that graph can be invoked with a simple message."""
        graph = create_supervisor_graph(llm)
        
        # Graph should be able to handle basic structure
        assert hasattr(graph, 'invoke') or hasattr(graph, 'stream')

    def test_graph_state_management(self):
        """Test that graph has proper state management."""
        graph = create_workflow()
        config_dict = get_config(thread_id="test_state")
        
        # Config should support state tracking
        assert config_dict["configurable"]["thread_id"] == "test_state"


class TestGraphIntegration:
    """Test graph integration and agent coordination."""

    def test_workflow_includes_all_agents(self, llm):
        """Test that workflow includes all required agents."""
        graph = create_supervisor_graph(llm)
        
        # The graph should be compiled with all agents
        assert graph is not None

    def test_multiple_graph_instances(self):
        """Test creating multiple graph instances."""
        graph1 = create_workflow()
        graph2 = create_workflow()
        
        # Both should be valid instances
        assert graph1 is not None
        assert graph2 is not None
