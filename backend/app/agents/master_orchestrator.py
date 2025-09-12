"""
Master Agent Orchestrator - The Super Agent that coordinates all other agents.
"""
from .base_agent import BaseAgent
from .planning_agent import PlanningAgent
from .execution_agent import ExecutionAgent
from .ethics_agent import EthicsAgent
from typing import Dict, Any, List, AsyncGenerator
import asyncio

class MasterAgentOrchestrator(BaseAgent):
    """
    The Master Orchestrator Agent coordinates all other agents in the system.
    This is the 'Super Agent' that manages the entire multi-agent workflow.
    """
    
    def __init__(self, api_key: str):
        """Initialize the Master Orchestrator with all sub-agents."""
        super().__init__(api_key)
        self.agent_name = "Master Agent Orchestrator"
        
        # Initialize sub-agents
        self.planning_agent = PlanningAgent(api_key)
        self.execution_agent = ExecutionAgent(api_key)
        self.ethics_agent = EthicsAgent(api_key)
        
        # Conversation history
        self.conversation_history = []
    
    async def handle_message(self, message: str, history: List[Dict] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Handle a user message through the complete multi-agent workflow.
        Yields status updates and final response.
        """
        self.conversation_history = history or []
        
        try:
            # Step 1: Orchestrator thinking
            yield {
                "type": "status",
                "agent": "Master Orchestrator",
                "message": "Analyzing request and coordinating agent workflow...",
                "is_final": False
            }
            
            # Step 2: Planning phase
            yield {
                "type": "status", 
                "agent": "Planning Agent",
                "message": "Creating detailed step-by-step plan...",
                "is_final": False
            }
            
            plan = await self.planning_agent.plan_task(
                goal=message,
                context="User request in multi-agent system",
                conversation_history=self.conversation_history
            )
            
            # Step 3: Ethics review of the plan
            yield {
                "type": "status",
                "agent": "Ethics & Safety Review Agent", 
                "message": "Reviewing plan for ethical compliance...",
                "is_final": False
            }
            
            ethics_review = await self.ethics_agent.review_plan_or_output(
                content="\n".join(plan),
                content_type="plan"
            )
            
            # Handle ethics review results
            if not ethics_review["approved"]:
                if ethics_review["status"] == "rejected":
                    yield {
                        "type": "response",
                        "agent": "Ethics & Safety Review Agent",
                        "message": f"I cannot fulfill this request due to ethical concerns: {ethics_review['reasoning']}",
                        "is_final": True
                    }
                    return
                else:
                    # Try to revise the plan
                    yield {
                        "type": "status",
                        "agent": "Planning Agent",
                        "message": "Revising plan based on ethical feedback...",
                        "is_final": False
                    }
                    
                    revised_context = f"Original request: {message}\nEthical concerns: {'; '.join(ethics_review['concerns'])}\nSuggestions: {'; '.join(ethics_review['suggestions'])}"
                    plan = await self.planning_agent.plan_task(
                        goal="Revise the approach to address ethical concerns while still being helpful",
                        context=revised_context,
                        conversation_history=self.conversation_history
                    )
            
            # Step 4: Execute the plan
            execution_results = []
            
            for i, step in enumerate(plan, 1):
                yield {
                    "type": "status",
                    "agent": "Execution Agent",
                    "message": f"Executing step {i}/{len(plan)}: {step[:50]}...",
                    "is_final": False
                }
                
                # Build context from previous steps
                context = self._build_execution_context(execution_results)
                
                step_result = await self.execution_agent.execute_step(
                    step=step,
                    context=context
                )
                
                execution_results.append(step_result)
                
                # Brief pause between steps for better UX
                await asyncio.sleep(0.5)
            
            # Step 5: Synthesize final response
            yield {
                "type": "status",
                "agent": "Master Orchestrator",
                "message": "Synthesizing final response...",
                "is_final": False
            }
            
            final_response = await self._synthesize_response(
                original_message=message,
                plan=plan,
                execution_results=execution_results,
                ethics_review=ethics_review
            )
            
            # Step 6: Final ethics check on the response
            final_ethics_review = await self.ethics_agent.review_plan_or_output(
                content=final_response,
                content_type="response"
            )
            
            if not final_ethics_review["approved"]:
                final_response = f"I've prepared a response, but upon final review, I need to modify it for ethical compliance. {final_ethics_review['reasoning']}"
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": final_response})
            
            # Final response
            yield {
                "type": "response",
                "agent": "Master Orchestrator",
                "message": final_response,
                "is_final": True,
                "metadata": {
                    "plan_steps": len(plan),
                    "executed_steps": len(execution_results),
                    "ethics_approved": final_ethics_review["approved"]
                }
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "agent": "Master Orchestrator",
                "message": f"An error occurred while processing your request: {str(e)}",
                "is_final": True
            }
    
    def _build_execution_context(self, previous_results: List[Dict]) -> str:
        """Build context string from previous execution results."""
        if not previous_results:
            return ""
        
        context = "Previous steps completed:\n"
        for i, result in enumerate(previous_results, 1):
            context += f"{i}. {result['result']}\n"
        
        return context
    
    async def _synthesize_response(self, original_message: str, plan: List[str], 
                                   execution_results: List[Dict], ethics_review: Dict) -> str:
        """Synthesize a final response based on all the work done."""
        
        # Collect all execution results
        completed_work = []
        for result in execution_results:
            if result["success"]:
                completed_work.append(result["result"])
        
        history_context = self._format_conversation_history(self.conversation_history)
        
        prompt = f"""
You are the Master Agent Orchestrator synthesizing a final response after coordinating multiple specialized agents.

Original User Request: {original_message}

Plan that was created:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(plan))}

Work completed by Execution Agent:
{chr(10).join(f"- {work}" for work in completed_work)}

Ethics Review Status: {"Approved" if ethics_review["approved"] else "Required revisions"}

{history_context}

Your task:
1. Synthesize all the work done into a coherent, helpful response
2. Address the original user request directly
3. Be natural and conversational, not overly technical
4. Don't mention the internal agent workflow unless relevant
5. Focus on providing value to the user

Create a clear, helpful response that directly addresses the user's request:
"""

        try:
            response = await self._generate_content(prompt)
            return response.strip()
        except Exception as e:
            return f"I've completed the analysis and work on your request. Here's what I found: {'; '.join(completed_work) if completed_work else 'I encountered some technical difficulties but did my best to address your request.'}"