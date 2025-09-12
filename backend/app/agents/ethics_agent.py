"""
Ethics Agent responsible for ethical review using Constitutional AI principles.
"""
from .base_agent import BaseAgent
from ..tools.tool_registry import ToolRegistry
from typing import Dict, Any

class EthicsAgent(BaseAgent):
    """Agent responsible for ethical review and Constitutional AI principles."""
    
    def __init__(self, api_key: str):
        """Initialize the Ethics Agent."""
        super().__init__(api_key)
        self.agent_name = "Ethics & Safety Review Agent"
        self.tool_registry = ToolRegistry()
    
    async def review_plan_or_output(self, content: str, content_type: str = "plan") -> Dict[str, Any]:
        """
        Review a plan or output against constitutional AI principles.
        Returns approval status and any suggested revisions.
        """
        # Retrieve relevant constitutional principles
        constitution = self.tool_registry.execute_tool("constitution_retriever", {"query": content})
        
        prompt = f"""
You are the Ethics & Safety Review Agent in a Multi-Agent AI system. Your role is to review plans and outputs against Constitutional AI principles to ensure they are ethical, safe, and beneficial.

Content to review ({content_type}):
{content}

Constitutional Principles to Consider:
{constitution}

Your task:
1. Carefully analyze the content against the constitutional principles
2. Identify any potential ethical concerns, safety issues, or harmful implications
3. Determine if the content should be approved, revised, or rejected
4. If revisions are needed, provide specific, constructive suggestions

Consider these aspects:
- Does it respect human dignity and rights?
- Could it cause harm to individuals or groups?
- Does it promote fairness and avoid discrimination?
- Is it truthful and accurate?
- Does it respect privacy and confidentiality?
- Is it beneficial to users and society?

Provide your review in this format:

ETHICAL REVIEW ASSESSMENT:

Status: [APPROVED/NEEDS_REVISION/REJECTED]

Reasoning:
[Explain your assessment based on constitutional principles]

Concerns (if any):
[List specific ethical concerns or issues identified]

Suggestions for improvement (if applicable):
[Provide constructive suggestions for addressing concerns]

Final recommendation:
[Your final recommendation for how to proceed]
"""

        try:
            response = await self._generate_content(prompt)
            return self._parse_ethics_review(response)
        except Exception as e:
            return {
                "status": "error",
                "reasoning": f"Error during ethical review: {str(e)}",
                "concerns": ["Technical error during review"],
                "suggestions": ["Please try again with a different approach"],
                "approved": False
            }
    
    def _parse_ethics_review(self, response: str) -> Dict[str, Any]:
        """Parse the ethics review response into structured data."""
        result = {
            "status": "needs_revision",  # Default to cautious approach
            "reasoning": "",
            "concerns": [],
            "suggestions": [],
            "approved": False
        }
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if "Status:" in line:
                status_text = line.split("Status:", 1)[1].strip().upper()
                if "APPROVED" in status_text:
                    result["status"] = "approved"
                    result["approved"] = True
                elif "REJECTED" in status_text:
                    result["status"] = "rejected"
                    result["approved"] = False
                else:
                    result["status"] = "needs_revision"
                    result["approved"] = False
            
            elif "Reasoning:" in line:
                current_section = "reasoning"
                reasoning_text = line.split("Reasoning:", 1)[1].strip()
                if reasoning_text:
                    result["reasoning"] = reasoning_text
            
            elif "Concerns" in line and ":" in line:
                current_section = "concerns"
            
            elif "Suggestions" in line and ":" in line:
                current_section = "suggestions"
            
            elif "Final recommendation:" in line:
                current_section = "recommendation"
            
            elif line and current_section:
                if current_section == "reasoning" and not result["reasoning"]:
                    result["reasoning"] = line
                elif current_section == "reasoning":
                    result["reasoning"] += " " + line
                elif current_section == "concerns" and line.startswith(('-', '•', '*')):
                    result["concerns"].append(line.lstrip('-•* '))
                elif current_section == "suggestions" and line.startswith(('-', '•', '*')):
                    result["suggestions"].append(line.lstrip('-•* '))
        
        # Ensure we have some reasoning
        if not result["reasoning"]:
            result["reasoning"] = "Content reviewed against constitutional principles."
        
        return result