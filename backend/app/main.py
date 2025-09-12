"""
FastAPI main application for Master Agentic AI.
Provides API endpoints for chat functionality and serves the React frontend.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import json
import os
from typing import AsyncGenerator

from .models import ChatRequest, ChatResponse, ApiKeyRequest
from .agents.master_orchestrator import MasterAgentOrchestrator
from . import config

# Create FastAPI application
app = FastAPI(
    title="Master Agentic AI",
    description="A sophisticated Multi-Agent System (MAS) implementing Constitutional AI principles",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/set-api-key")
async def set_api_key(request: ApiKeyRequest):
    """Set the Gemini API key for the session."""
    try:
        config.set_api_key(request.api_key)
        return {"status": "success", "message": "API key set successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set API key: {str(e)}")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that processes user messages through the multi-agent system.
    Returns a streaming response with agent status updates and final response.
    """
    try:
        # Validate that we have an API key
        api_key = config.get_api_key()
        if not api_key:
            raise HTTPException(
                status_code=400, 
                detail="Gemini API key not configured. Please set your API key first."
            )
        
        # Initialize the Master Orchestrator
        orchestrator = MasterAgentOrchestrator(api_key)
        
        async def generate_response() -> AsyncGenerator[str, None]:
            """Generate streaming response from the agent system."""
            try:
                async for response in orchestrator.handle_message(
                    message=request.message,
                    history=request.conversation_history
                ):
                    # Convert response to JSON and yield
                    json_response = json.dumps(response) + "\n"
                    yield json_response
                    
            except Exception as e:
                # Send error response
                error_response = {
                    "type": "error",
                    "agent": "System",
                    "message": f"An error occurred: {str(e)}",
                    "is_final": True
                }
                yield json.dumps(error_response) + "\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="application/x-ndjson",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Master Agentic AI",
        "version": "1.0.0"
    }

@app.get("/api/status")
async def api_status():
    """API status endpoint with configuration info."""
    return {
        "api_key_configured": bool(config.get_api_key()),
        "agents_available": ["orchestrator", "planning", "execution", "ethics"],
        "tools_available": ["web_search", "code_interpreter", "constitution_retriever"]
    }

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return HTTPException(
        status_code=422,
        detail=f"Request validation error: {str(exc)}"
    )

@app.exception_handler(ValidationError)
async def pydantic_exception_handler(request, exc):
    return HTTPException(
        status_code=422,
        detail=f"Data validation error: {str(exc)}"
    )

# Serve static files (React frontend)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the React frontend."""
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        else:
            return {"message": "Frontend not built. Please build the React frontend first."}
else:
    @app.get("/")
    async def root():
        """Root endpoint when static files are not available."""
        return {
            "message": "Master Agentic AI API",
            "documentation": "/docs",
            "status": "Frontend not available - please build the React frontend"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)