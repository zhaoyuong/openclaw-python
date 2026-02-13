"""
OpenAI-compatible HTTP endpoint

Provides OpenAI API compatibility for chat completions.
"""

import asyncio
import json
import logging
import time
from typing import Any, AsyncGenerator, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    """Chat message"""
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    """OpenAI chat completion request"""
    model: str
    messages: list[ChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    stream: bool = False


class OpenAICompatibleEndpoint:
    """
    OpenAI-compatible HTTP endpoint
    
    Provides /v1/chat/completions endpoint that mimics OpenAI API.
    """
    
    def __init__(self, agent_runtime: Any = None):
        """
        Initialize endpoint
        
        Args:
            agent_runtime: AgentRuntime for executing requests
        """
        self.app = FastAPI(title="OpenClaw OpenAI API")
        self.agent_runtime = agent_runtime
        
        # Register routes
        self.app.post("/v1/chat/completions")(self.chat_completions)
        self.app.get("/v1/models")(self.list_models)
    
    async def chat_completions(self, request: ChatCompletionRequest):
        """
        Chat completions endpoint
        
        Args:
            request: Chat completion request
            
        Returns:
            Chat completion response
        """
        if not self.agent_runtime:
            raise HTTPException(status_code=503, detail="Agent runtime not available")
        
        # Extract last user message
        user_messages = [m for m in request.messages if m.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message found")
        
        last_message = user_messages[-1].content
        
        # Stream response
        if request.stream:
            return StreamingResponse(
                self._stream_completion(last_message, request),
                media_type="text/event-stream"
            )
        
        # Non-streaming response
        try:
            # TODO: Integrate with actual agent runtime
            # For now, return a stub response
            response_text = f"[Response to: {last_message[:50]}...]"
            
            return {
                "id": f"chatcmpl-{int(time.time() * 1000)}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response_text
                        },
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
            }
        except Exception as e:
            logger.error(f"Error in chat completion: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _stream_completion(
        self,
        message: str,
        request: ChatCompletionRequest
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completion chunks
        
        Args:
            message: User message
            request: Request params
            
        Yields:
            SSE-formatted chunks
        """
        # TODO: Integrate with actual streaming agent runtime
        # For now, simulate streaming
        
        response_text = f"[Streaming response to: {message[:50]}...]"
        
        # Send chunks
        for i, char in enumerate(response_text):
            chunk = {
                "id": f"chatcmpl-{int(time.time() * 1000)}",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": char},
                        "finish_reason": None
                    }
                ]
            }
            
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.01)  # Simulate delay
        
        # Send done
        yield "data: [DONE]\n\n"
    
    async def list_models(self):
        """
        List available models
        
        Returns:
            Models list
        """
        return {
            "object": "list",
            "data": [
                {
                    "id": "claude-sonnet-4",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "anthropic"
                }
            ]
        }
