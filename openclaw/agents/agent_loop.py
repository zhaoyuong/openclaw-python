"""Agent loop implementation matching pi-mono's agent-loop.ts

This module implements the core agent execution loop with:
- Streaming LLM responses
- Tool call extraction and execution
- Steering support (interrupting messages)
- Event emission for all steps
- Message conversion and context transformation hooks
"""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any, Literal

from .abort import AbortController, AbortError, AbortSignal
from .events import (
    AgentEndEvent,
    AgentEvent,
    AgentStartEvent,
    EventEmitter,
    MessageEndEvent,
    MessageStartEvent,
    MessageUpdateEvent,
    TextDeltaEvent,
    ThinkingDeltaEvent,
    ThinkingEndEvent,
    ThinkingStartEvent,
    ToolCallEndEvent,
    ToolCallStartEvent,
    ToolExecutionEndEvent,
    ToolExecutionStartEvent,
    ToolExecutionUpdateEvent,
    TurnEndEvent,
    TurnStartEvent,
)
from .providers import LLMMessage, LLMProvider
from .tools.base import AgentTool, ToolResult

logger = logging.getLogger(__name__)


@dataclass
class AgentMessage:
    """
    Agent message type that supports custom messages and filtering.
    
    This is the internal message format before conversion to LLMMessage.
    Allows for:
    - Custom message types that can be filtered out
    - System messages that may need special handling
    - Metadata and annotations
    """
    role: str
    content: Any
    images: list[str] | None = None
    tool_calls: list[dict] | None = None
    tool_call_id: str | None = None
    custom: bool = False  # Custom messages can be filtered during conversion
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentOptions:
    """
    Configuration options for agent execution.
    
    Matches TypeScript AgentOptions interface.
    """
    stream_fn: Callable[..., AsyncIterator[Any]] | None = None
    session_id: str | None = None
    get_api_key: Callable[[str], Awaitable[str | None]] | None = None
    thinking_budgets: dict[str, int] | None = None
    convert_to_llm: Callable[[list[AgentMessage]], list[LLMMessage]] | None = None
    transform_context: Callable[[list[LLMMessage]], list[LLMMessage]] | None = None
    steering_mode: Literal["all", "one-at-a-time"] = "one-at-a-time"
    follow_up_mode: Literal["all", "one-at-a-time"] = "one-at-a-time"


def default_convert_to_llm(messages: list[AgentMessage]) -> list[LLMMessage]:
    """
    Default message conversion from AgentMessage to LLMMessage.
    
    Filters out custom messages and converts to provider-compatible format.
    Matches TypeScript convertToLlm behavior.
    
    Args:
        messages: List of AgentMessage objects
        
    Returns:
        List of LLMMessage objects ready for provider
    """
    llm_messages: list[LLMMessage] = []
    
    for msg in messages:
        # Skip custom messages (they're for internal use only)
        if msg.custom:
            continue
        
        # Convert to LLMMessage
        llm_msg = LLMMessage(
            role=msg.role,
            content=msg.content,
            images=msg.images
        )
        
        # Preserve tool-related fields
        if msg.tool_calls:
            llm_msg.tool_calls = msg.tool_calls
        if msg.tool_call_id:
            llm_msg.tool_call_id = msg.tool_call_id
        
        llm_messages.append(llm_msg)
    
    return llm_messages


def default_transform_context(messages: list[LLMMessage]) -> list[LLMMessage]:
    """
    Default context transformation for context window management.
    
    Can be overridden to implement:
    - Context pruning (remove old messages)
    - External context injection
    - Message summarization
    
    Matches TypeScript transformContext behavior.
    
    Args:
        messages: List of LLMMessage objects
        
    Returns:
        Transformed list of messages
    """
    # Default: return messages as-is
    # Override this in AgentOptions to implement custom context management
    return messages


class AgentState:
    """Agent execution state with enhanced tracking"""
    
    def __init__(self):
        self.messages: list[AgentMessage] = []
        self.model: str = "google/gemini-3-pro-preview"
        self.tools: list[AgentTool] = []
        self.thinking_level: str = "off"
        self.steering_queue: list[str] = []
        self.followup_queue: list[str] = []
        self.turn_number: int = 0
        
        # Enhanced state tracking (matching TypeScript)
        self.is_streaming: bool = False
        self.stream_message: AgentMessage | None = None
        self.pending_tool_calls: list[dict[str, Any]] = []
        self.session_id: str | None = None
        
        # Abort control
        self.abort_controller: AbortController = AbortController()
    
    @property
    def signal(self) -> AbortSignal:
        """Get abort signal"""
        return self.abort_controller.signal


class AgentLoop:
    """Core agent execution loop with enhanced configuration"""
    
    def __init__(
        self,
        provider: LLMProvider,
        tools: list[AgentTool],
        event_emitter: EventEmitter | None = None,
        options: AgentOptions | None = None,
    ):
        self.provider = provider
        self.tools = {tool.name: tool for tool in tools}
        self.event_emitter = event_emitter or EventEmitter()
        self.options = options or AgentOptions()
        self.state = AgentState()
        
        # Set session ID if provided
        if self.options.session_id:
            self.state.session_id = self.options.session_id
    
    async def agent_loop(
        self,
        prompts: list[str],
        system_prompt: str | None = None,
        model: str | None = None,
    ) -> list[AgentMessage]:
        """
        Start agent loop with new prompts
        
        Args:
            prompts: User messages to process
            system_prompt: Optional system prompt
            model: Optional model override
            
        Returns:
            Final message list
        """
        # Initialize state
        self.state.messages = []
        self.state.turn_number = 0
        self.state.is_streaming = False
        self.state.stream_message = None
        self.state.pending_tool_calls = []
        
        if model:
            self.state.model = model
        
        # Add system prompt if provided
        if system_prompt:
            self.state.messages.append(AgentMessage(
                role="system",
                content=system_prompt
            ))
        
        # Add user prompts
        for prompt in prompts:
            self.state.messages.append(AgentMessage(
                role="user",
                content=prompt
            ))
        
        # Emit agent start
        await self.event_emitter.emit(AgentStartEvent(model=self.state.model))
        
        try:
            # Run main loop
            await self.run_loop()
            
            # Emit agent end
            await self.event_emitter.emit(AgentEndEvent(reason="completed"))
            
            return self.state.messages
            
        except Exception as e:
            logger.error(f"Agent loop error: {e}", exc_info=True)
            await self.event_emitter.emit(AgentEndEvent(reason="error"))
            raise
    
    async def agent_loop_continue(self) -> list[AgentMessage]:
        """
        Continue agent loop from existing state
        
        Returns:
            Final message list
        """
        try:
            await self.run_loop()
            return self.state.messages
        except Exception as e:
            logger.error(f"Agent loop continue error: {e}", exc_info=True)
            raise
    
    async def run_loop(self) -> None:
        """Main execution loop with mode support"""
        
        while True:
            # Check for abort signal
            try:
                self.state.signal.throw_if_aborted()
            except AbortError:
                logger.info("Agent loop aborted")
                break
            
            # Check for steering messages (interrupts)
            if self.state.steering_queue:
                # Process steering based on mode
                if self.options.steering_mode == "all":
                    # Process all steering messages at once
                    while self.state.steering_queue:
                        steering_msg = self.state.steering_queue.pop(0)
                        self.state.messages.append(AgentMessage(
                            role="user",
                            content=steering_msg
                        ))
                    logger.info("Processing all steering messages")
                else:
                    # One at a time (default)
                    steering_msg = self.state.steering_queue.pop(0)
                    self.state.messages.append(AgentMessage(
                        role="user",
                        content=steering_msg
                    ))
                    logger.info("Processing steering message")
                continue
            
            # Increment turn
            self.state.turn_number += 1
            
            # Emit turn start
            await self.event_emitter.emit(TurnStartEvent(
                turn_number=self.state.turn_number
            ))
            
            # Stream assistant response
            assistant_message, tool_calls = await self.stream_assistant_response()
            
            # Add assistant message to context
            self.state.messages.append(assistant_message)
            
            # Clear streaming state
            self.state.is_streaming = False
            self.state.stream_message = None
            
            # Emit turn end
            await self.event_emitter.emit(TurnEndEvent(
                turn_number=self.state.turn_number,
                has_tool_calls=len(tool_calls) > 0
            ))
            
            # If no tool calls, we're done
            if not tool_calls:
                break
            
            # Store pending tool calls
            self.state.pending_tool_calls = tool_calls
            
            # Execute tool calls
            await self.execute_tool_calls(tool_calls)
            
            # Clear pending tool calls
            self.state.pending_tool_calls = []
            
            # Check for follow-up messages
            if self.state.followup_queue:
                # Process follow-up based on mode
                if self.options.follow_up_mode == "all":
                    # Process all follow-up messages at once
                    while self.state.followup_queue:
                        followup_msg = self.state.followup_queue.pop(0)
                        self.state.messages.append(AgentMessage(
                            role="user",
                            content=followup_msg
                        ))
                else:
                    # One at a time (default)
                    followup_msg = self.state.followup_queue.pop(0)
                    self.state.messages.append(AgentMessage(
                        role="user",
                        content=followup_msg
                    ))
    
    async def stream_assistant_response(self) -> tuple[AgentMessage, list[dict[str, Any]]]:
        """
        Stream assistant response from LLM with conversion hooks
        
        Returns:
            Tuple of (assistant_message, tool_calls)
        """
        # Emit message start
        message_id = str(uuid.uuid4())
        await self.event_emitter.emit(MessageStartEvent(
            role="assistant",
            message_id=message_id
        ))
        
        # Set streaming state
        self.state.is_streaming = True
        self.state.stream_message = AgentMessage(role="assistant", content="")
        
        # Accumulate response
        content_parts: list[str] = []
        thinking_parts: list[str] = []
        tool_calls: list[dict[str, Any]] = []
        current_tool_call: dict[str, Any] | None = None
        in_thinking = False
        
        try:
            # Convert messages using conversion hook
            convert_fn = self.options.convert_to_llm or default_convert_to_llm
            llm_messages = convert_fn(self.state.messages)
            
            # Transform context using transformation hook
            transform_fn = self.options.transform_context or default_transform_context
            llm_messages = transform_fn(llm_messages)
            
            # Stream from provider
            async for response in self.provider.stream(
                messages=llm_messages,
                model=self.state.model,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.get_schema()
                        }
                    }
                    for tool in self.tools.values()
                ]
            ):
                # Handle LLMResponse objects from providers
                event_type = response.type
                
                if event_type == "thinking_start":
                    in_thinking = True
                    await self.event_emitter.emit(ThinkingStartEvent())
                
                elif event_type == "thinking_delta":
                    delta = str(response.content)
                    thinking_parts.append(delta)
                    await self.event_emitter.emit(ThinkingDeltaEvent(delta=delta))
                
                elif event_type == "thinking_end":
                    in_thinking = False
                    await self.event_emitter.emit(ThinkingEndEvent(
                        thinking="".join(thinking_parts)
                    ))
                
                elif event_type == "text_delta":
                    delta = str(response.content)
                    content_parts.append(delta)
                    await self.event_emitter.emit(TextDeltaEvent(delta=delta))
                    
                    # Update stream message
                    self.state.stream_message.content = "".join(content_parts)
                    
                    # Also emit message update
                    await self.event_emitter.emit(MessageUpdateEvent(
                        role="assistant",
                        content="".join(content_parts)
                    ))
                
                elif event_type == "tool_call":
                    # Handle tool calls from response
                    if response.tool_calls:
                        for tc in response.tool_calls:
                            tool_call_id = tc.get("id") or str(uuid.uuid4())
                            tool_name = tc.get("name", "")
                            params = tc.get("arguments", {})
                            
                            # Emit tool call events
                            await self.event_emitter.emit(ToolCallStartEvent(
                                tool_call_id=tool_call_id,
                                tool_name=tool_name
                            ))
                            
                            await self.event_emitter.emit(ToolCallEndEvent(
                                tool_call_id=tool_call_id,
                                tool_name=tool_name,
                                params=params
                            ))
                            
                            tool_calls.append({
                                "id": tool_call_id,
                                "name": tool_name,
                                "params": params
                            })
                
                elif event_type == "done":
                    break
        
        except Exception as e:
            logger.error(f"Error streaming response: {e}", exc_info=True)
            raise
        
        # Build final message
        content = "".join(content_parts)
        
        assistant_message = AgentMessage(
            role="assistant",
            content=content
        )
        
        # Add tool calls if any
        if tool_calls:
            assistant_message.tool_calls = tool_calls
        
        # Emit message end
        await self.event_emitter.emit(MessageEndEvent(
            role="assistant",
            content=content,
            message_id=message_id
        ))
        
        return assistant_message, tool_calls
    
    async def execute_tool_calls(self, tool_calls: list[dict[str, Any]]) -> None:
        """
        Execute tool calls sequentially with progress tracking
        
        Args:
            tool_calls: List of tool calls to execute
        """
        for tool_call in tool_calls:
            # Check for steering before each tool
            if self.state.steering_queue:
                logger.info("Steering detected, stopping tool execution")
                break
            
            tool_call_id = tool_call["id"]
            tool_name = tool_call["name"]
            params = tool_call.get("params", {})
            
            # Create progress callback for this tool execution
            async def progress_callback(current: int, total: int, message: str = ""):
                """Progress callback for long-running tools"""
                await self.event_emitter.emit(ToolExecutionUpdateEvent(
                    tool_call_id=tool_call_id,
                    tool_name=tool_name,
                    progress=current / total if total > 0 else 0,
                    message=message
                ))
            
            # Emit tool execution start
            await self.event_emitter.emit(ToolExecutionStartEvent(
                tool_name=tool_name,
                tool_call_id=tool_call_id,
                params=params
            ))
            
            try:
                # Get tool
                tool = self.tools.get(tool_name)
                if not tool:
                    error_msg = f"Tool '{tool_name}' not found"
                    logger.error(error_msg)
                    
                    # Emit error
                    await self.event_emitter.emit(ToolExecutionEndEvent(
                        tool_call_id=tool_call_id,
                        success=False,
                        error=error_msg
                    ))
                    
                    # Add error result to messages
                    self.state.messages.append(AgentMessage(
                        role="toolResult",
                        tool_call_id=tool_call_id,
                        content=f"Error: {error_msg}"
                    ))
                    continue
                
                # Execute tool with progress callback if supported
                if hasattr(tool, 'execute_with_progress'):
                    result: ToolResult = await tool.execute_with_progress(params, progress_callback)
                else:
                    result: ToolResult = await tool.execute(params)
                
                # Emit tool execution end
                await self.event_emitter.emit(ToolExecutionEndEvent(
                    tool_call_id=tool_call_id,
                    success=result.success,
                    result=result.content if result.success else None,
                    error=result.error if not result.success else None
                ))
                
                # Add result to messages
                result_content = result.content if result.success else f"Error: {result.error}"
                self.state.messages.append(AgentMessage(
                    role="toolResult",
                    tool_call_id=tool_call_id,
                    content=result_content
                ))
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Tool execution error: {e}", exc_info=True)
                
                # Emit error
                await self.event_emitter.emit(ToolExecutionEndEvent(
                    tool_call_id=tool_call_id,
                    success=False,
                    error=error_msg
                ))
                
                # Add error result
                self.state.messages.append(AgentMessage(
                    role="toolResult",
                    tool_call_id=tool_call_id,
                    content=f"Error: {error_msg}"
                ))
    
    def steer(self, message: str) -> None:
        """
        Add steering message (interrupts current execution)
        
        Args:
            message: Steering message to add
        """
        self.state.steering_queue.append(message)
    
    def followup(self, message: str) -> None:
        """
        Add follow-up message (queued after current turn)
        
        Args:
            message: Follow-up message to add
        """
        self.state.followup_queue.append(message)
    
    def abort(self, reason: Exception | None = None) -> None:
        """
        Abort agent loop with optional reason
        
        Args:
            reason: Optional exception describing abort reason
        """
        self.state.abort_controller.abort(reason)
