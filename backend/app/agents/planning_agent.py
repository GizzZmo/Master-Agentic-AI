"""
Planning Agent responsible for task decomposition and planning using Chain-of-Thought reasoning.
"""
from .base_agent import BaseAgent
from typing import List, Dict, Any

class PlanningAgent(BaseAgent):
    """Agent responsible for breaking down complex tasks into step-by-step plans."""
    
    def __init__(self, api_key: str):
        """Initialize the Planning Agent."""
        super().__init__(api_key)
        self.agent_name = "Planning Agent"
    
    async def plan_task(self, goal: str, context: str = "", conversation_history: List[Dict] = None) -> List[str]:
        """
        Create a detailed step-by-step plan for achieving the given goal.
        Uses Chain-of-Thought reasoning to break down complex tasks.
        """
        history_context = self._format_conversation_history(conversation_history or [])
        
        prompt = f"""
You are the Planning Agent in a Multi-Agent AI system. Your role is to break down complex goals into clear, actionable steps using Chain-of-Thought reasoning.

Goal to plan for: {goal}

Additional Context: {context}
{history_context}

Instructions:
1. Think step by step about how to achieve this goal
2. Break it down into 3-7 logical, sequential steps
3. Each step should be clear and actionable
4. Consider what information or tools might be needed for each step
5. Ensure the plan is comprehensive but not overly complex

Think through this carefully:

Step-by-step reasoning:
- What is the main objective?
- What information do I need to gather first?
- What are the key components of this task?
- What logical sequence should I follow?
- What potential challenges might arise?

Now provide a numbered list of steps in this format:
1. [First step with clear action]
2. [Second step with clear action]
3. [Continue with remaining steps...]

Plan:
"""

        try:
            response = await self._generate_content(prompt)
            return self._parse_plan(response)
        except Exception as e:
            return [f"Error creating plan: {str(e)}"]
    
    def _parse_plan(self, response: str) -> List[str]:
        """Parse the AI response into a list of plan steps."""
        lines = response.split('\n')
        steps = []
        
        for line in lines:
            line = line.strip()
            # Look for numbered steps
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Clean up the step text
                step = line
                # Remove numbering and clean up
                if '. ' in step:
                    step = step.split('. ', 1)[1] if len(step.split('. ', 1)) > 1 else step
                elif '- ' in step:
                    step = step.replace('- ', '', 1)
                elif '• ' in step:
                    step = step.replace('• ', '', 1)
                
                if step.strip():
                    steps.append(step.strip())
        
        # If no numbered steps found, try to extract from the response
        if not steps:
            # Look for the "Plan:" section
            plan_section = False
            for line in lines:
                if "Plan:" in line:
                    plan_section = True
                    continue
                if plan_section and line.strip():
                    steps.append(line.strip())
        
        # Ensure we have at least one step
        if not steps:
            steps = ["Analyze the request and determine the appropriate response"]
        
        return steps[:7]  # Limit to 7 steps maximum