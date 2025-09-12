"""
Execution Agent responsible for tool execution using ReAct framework.
"""
from .base_agent import BaseAgent
from ..tools.tool_registry import ToolRegistry
from typing import Dict, Any, List
import re

class ExecutionAgent(BaseAgent):
    """Agent responsible for executing individual steps using the ReAct framework."""
    
    def __init__(self, api_key: str):
        """Initialize the Execution Agent."""
        super().__init__(api_key)
        self.agent_name = "Execution Agent"
        self.tool_registry = ToolRegistry()
    
    async def execute_step(self, step: str, context: str = "", available_tools: List[str] = None) -> Dict[str, Any]:
        """
        Execute a single step from the plan using ReAct (Reason + Act) framework.
        Returns the result of the step execution.
        """
        if available_tools is None:
            available_tools = list(self.tool_registry.get_available_tools().keys())
        
        tools_description = self._format_tools_description(available_tools)
        
        prompt = f"""
You are the Execution Agent in a Multi-Agent AI system. You use the ReAct (Reason + Act) framework to execute tasks step by step.

Current Step to Execute: {step}
Context: {context}

Available Tools:
{tools_description}

Instructions:
1. Follow the ReAct pattern: Thought → Action → Observation
2. Think about what you need to do for this step
3. Decide if you need to use a tool or if you can complete the step with reasoning alone
4. If using a tool, specify the tool name and parameters
5. Provide clear observations about the results

Use this exact format:

Thought: [Your reasoning about how to approach this step]

Action: [Either "use_tool" with tool name and parameters, or "reasoning_only" for steps that don't require tools]

Tool: [tool_name if using a tool, or "none" if reasoning only]
Parameters: [tool parameters as JSON if using a tool, or "none"]

Observation: [What you learned or accomplished from this step]

Result: [Clear summary of what was completed in this step]
"""

        try:
            response = await self._generate_content(prompt)
            return self._parse_execution_result(response, step)
        except Exception as e:
            return {
                "step": step,
                "success": False,
                "result": f"Error executing step: {str(e)}",
                "tool_used": None,
                "observation": f"Technical error: {str(e)}"
            }
    
    def _format_tools_description(self, available_tools: List[str]) -> str:
        """Format the available tools for the prompt."""
        tools_info = self.tool_registry.get_available_tools()
        description = ""
        
        for tool_name in available_tools:
            if tool_name in tools_info:
                tool_info = tools_info[tool_name]
                description += f"- {tool_name}: {tool_info.get('description', 'No description available')}\n"
        
        return description
    
    def _parse_execution_result(self, response: str, original_step: str) -> Dict[str, Any]:
        """Parse the execution response into structured data."""
        result = {
            "step": original_step,
            "success": True,
            "result": "",
            "tool_used": None,
            "observation": "",
            "thought": ""
        }
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("Thought:"):
                current_section = "thought"
                thought_text = line.split("Thought:", 1)[1].strip()
                if thought_text:
                    result["thought"] = thought_text
            
            elif line.startswith("Action:"):
                current_section = "action"
                # Action handling is implicit in the tool parsing
            
            elif line.startswith("Tool:"):
                tool_text = line.split("Tool:", 1)[1].strip()
                if tool_text.lower() != "none":
                    result["tool_used"] = tool_text
            
            elif line.startswith("Parameters:"):
                if result["tool_used"]:
                    params_text = line.split("Parameters:", 1)[1].strip()
                    if params_text.lower() != "none":
                        try:
                            # Try to execute the tool
                            import json
                            params = json.loads(params_text) if params_text.startswith('{') else {"query": params_text}
                            tool_result = self.tool_registry.execute_tool(result["tool_used"], params)
                            result["observation"] += f"Tool {result['tool_used']} executed: {tool_result}\n"
                        except Exception as e:
                            result["observation"] += f"Tool execution failed: {str(e)}\n"
            
            elif line.startswith("Observation:"):
                current_section = "observation"
                obs_text = line.split("Observation:", 1)[1].strip()
                if obs_text:
                    result["observation"] += obs_text + "\n"
            
            elif line.startswith("Result:"):
                current_section = "result"
                result_text = line.split("Result:", 1)[1].strip()
                if result_text:
                    result["result"] = result_text
            
            elif line and current_section:
                if current_section == "thought":
                    result["thought"] += " " + line
                elif current_section == "observation":
                    result["observation"] += line + "\n"
                elif current_section == "result":
                    result["result"] += " " + line
        
        # Ensure we have a result
        if not result["result"]:
            result["result"] = f"Completed step: {original_step}"
        
        # Clean up observation
        result["observation"] = result["observation"].strip()
        
        return result