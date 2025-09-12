"""
Base Agent class that provides common functionality for all agents.
"""
import google.generativeai as genai
from typing import Optional

class BaseAgent:
    """Base class for all agents in the Master Agentic AI system."""
    
    def __init__(self, api_key: str):
        """Initialize the base agent with API key."""
        self.api_key = api_key
        self._configure_genai()
    
    def _configure_genai(self):
        """Configure the Google Generative AI client."""
        if self.api_key:
            genai.configure(api_key=self.api_key)
    
    def _get_gemini_model(self, model_name: str = "gemini-pro"):
        """Get a configured Gemini model instance."""
        return genai.GenerativeModel(model_name)
    
    async def _generate_content(self, prompt: str, model_name: str = "gemini-pro") -> str:
        """Generate content using the Gemini model."""
        try:
            model = self._get_gemini_model(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def _format_conversation_history(self, history: list) -> str:
        """Format conversation history for context."""
        if not history:
            return ""
        
        formatted = "\nConversation History:\n"
        for entry in history[-5:]:  # Keep last 5 exchanges
            role = entry.get('role', 'unknown')
            content = entry.get('content', '')
            formatted += f"{role.capitalize()}: {content}\n"
        
        return formatted