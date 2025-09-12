"""
Pydantic models for request and response validation.
"""
from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    response: str
    agent_status: Optional[str] = None
    is_final: bool = True

class ApiKeyRequest(BaseModel):
    api_key: str