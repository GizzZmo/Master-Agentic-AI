"""
Agent Manager for handling agent lifecycle and coordination.
"""
from .base_agent import BaseAgent
from .master_orchestrator import MasterAgentOrchestrator
from .planning_agent import PlanningAgent
from .execution_agent import ExecutionAgent
from .ethics_agent import EthicsAgent

class AgentManager:
    """Manages the lifecycle and coordination of all agents."""
    
    def __init__(self, api_key: str):
        """Initialize the agent manager with API key."""
        self.api_key = api_key
        self._agents = {}
    
    def get_agent(self, agent_type: str) -> BaseAgent:
        """Get or create an agent instance."""
        if agent_type not in self._agents:
            self._agents[agent_type] = self._create_agent(agent_type)
        return self._agents[agent_type]
    
    def _create_agent(self, agent_type: str) -> BaseAgent:
        """Create a new agent instance based on type."""
        agent_classes = {
            'orchestrator': MasterAgentOrchestrator,
            'planning': PlanningAgent,
            'execution': ExecutionAgent,
            'ethics': EthicsAgent
        }
        
        agent_class = agent_classes.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return agent_class(self.api_key)
    
    def update_api_key(self, new_api_key: str):
        """Update API key for all agents."""
        self.api_key = new_api_key
        # Clear existing agents so they'll be recreated with new API key
        self._agents.clear()