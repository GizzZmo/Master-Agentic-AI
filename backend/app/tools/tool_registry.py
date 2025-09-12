"""
Tool Registry for managing and executing available tools.
"""
from typing import Dict, Any, Callable
from .web_search import web_search
from .code_interpreter import code_interpreter
from .constitution_retriever import constitution_retriever

class ToolRegistry:
    """Registry for managing available tools and their execution."""
    
    def __init__(self):
        """Initialize the tool registry with available tools."""
        self._tools = {
            "web_search": {
                "function": web_search,
                "description": "Search the web for information on a given topic",
                "parameters": ["query"]
            },
            "code_interpreter": {
                "function": code_interpreter,
                "description": "Execute and interpret code snippets",
                "parameters": ["code", "language"]
            },
            "constitution_retriever": {
                "function": constitution_retriever,
                "description": "Retrieve relevant constitutional AI principles",
                "parameters": ["query"]
            }
        }
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of all available tools and their metadata."""
        return {name: {
            "description": tool_info["description"],
            "parameters": tool_info["parameters"]
        } for name, tool_info in self._tools.items()}
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a tool with the given parameters."""
        if tool_name not in self._tools:
            return f"Error: Tool '{tool_name}' not found. Available tools: {list(self._tools.keys())}"
        
        try:
            tool_function = self._tools[tool_name]["function"]
            return tool_function(**parameters)
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
    
    def register_tool(self, name: str, function: Callable, description: str, parameters: list):
        """Register a new tool with the registry."""
        self._tools[name] = {
            "function": function,
            "description": description,
            "parameters": parameters
        }
    
    def list_tools(self) -> str:
        """Get a formatted string listing all available tools."""
        output = "Available Tools:\n"
        for name, info in self._tools.items():
            output += f"- {name}: {info['description']}\n"
        return output