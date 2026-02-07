"""
OpenAI provider implementation
"""

import json
import logging
import os
from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from openclaw.media import encode_image_to_base64

from .base import LLMMessage, LLMProvider, LLMResponse

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """
    OpenAI provider

    Supports:
    - GPT-4, GPT-4 Turbo
    - GPT-3.5 Turbo
    - o1, o1-mini, o1-preview
    - Any OpenAI-compatible API (via base_url)

    Example:
        # OpenAI
        provider = OpenAIProvider("gpt-4", api_key="...")

        # OpenAI-compatible (e.g., LM Studio, Ollama with OpenAI compat)
        provider = OpenAIProvider(
            "model-name",
            base_url="http://localhost:1234/v1"
        )
    """

    @property
    def provider_name(self) -> str:
        return "openai"

    def get_client(self) -> AsyncOpenAI:
        """Get OpenAI client"""
        if self._client is None:
            api_key = self.api_key or os.getenv("OPENAI_API_KEY", "not-needed")

            # Support custom base URL for OpenAI-compatible APIs
            kwargs = {"api_key": api_key}
            if self.base_url:
                kwargs["base_url"] = self.base_url

            self._client = AsyncOpenAI(**kwargs)

        return self._client

    async def stream(
        self,
        messages: list[LLMMessage],
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
        **kwargs,
    ) -> AsyncIterator[LLMResponse]:
        """Stream responses from OpenAI"""
        client = self.get_client()

        logger.info(f"📥 [Provider Received Tools]: Count={len(tools) if tools else 0}")

        # Convert messages to OpenAI format
        openai_messages = []
        for msg in messages:
            content_list = [{"type": "text", "text": msg.content}]

            # [NEW] Handle images in messages
            images = getattr(msg, "images", [])
            if images:
                for img_data in images:
                    # Assuming img_data is a URL or a Base64 string
                    logger.info(
                        f"Processing image for message: {img_data[:30]}..."
                    )  # Log the start of the image data
                    b64_image = await encode_image_to_base64(img_data)
                    content_list.append({"type": "image_url", "image_url": {"url": b64_image}})

            m_dict = {"role": msg.role, "content": content_list}

            if hasattr(msg, "name") and msg.name:
                m_dict["name"] = msg.name
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                m_dict["tool_calls"] = msg.tool_calls
            if hasattr(msg, "tool_call_id") and msg.tool_call_id:
                m_dict["tool_call_id"] = msg.tool_call_id

            openai_messages.append(m_dict)

        formatted_tools = []
        if tools:
            for t in tools:
                # First, check if it's already in the correct format (dict with "type")
                if isinstance(t, dict) and "type" in t:
                    formatted_tools.append(t)
                else:
                    # Try to format it as a function tool with name and description
                    try:
                        name = getattr(t, "name", "unnamed")
                        desc = getattr(t, "description", "")
                        formatted_tools.append(
                            {
                                "type": "function",
                                "function": {"name": name, "description": desc, "parameters": {}},
                            }
                        )
                    except Exception as e:
                        logger.error(f"Failed to format individual tool: {e}")
        # Debug logging
        api_payload = {
            "model": self.model,
            "messages": openai_messages,
            "tools": formatted_tools if formatted_tools else None,
            "stream": True,
            "max_tokens": max_tokens,
            **kwargs,
        }
        # logger.info("📤 [CRITICAL] FINAL JSON PAYLOAD SENT TO GEMINI:")
        # print(json.dumps(api_payload, indent=2, ensure_ascii=False))

        if len(openai_messages) >= 2:
            # logger.info("📨 [Last 2 Messages sent to Gemini]:")
            # print(json.dumps(openai_messages[-2:], indent=2, ensure_ascii=False))
            pass

        try:
            stream = await client.chat.completions.create(**api_payload)

            # Track tool calls
            tool_calls_buffer = {}

            async for chunk in stream:
                if not chunk.choices:
                    continue

                choice = chunk.choices[0]
                delta = choice.delta

                if hasattr(delta, "tool_calls") and delta.tool_calls:
                    logger.info(f"⚙️ [LLM Tool Call Delta]: {delta.tool_calls}")

                # Text content
                if delta.content:
                    yield LLMResponse(type="text_delta", content=delta.content)

                # Tool calls
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        idx = tool_call.index

                        # Initialize buffer for this tool call
                        if idx not in tool_calls_buffer:
                            tool_calls_buffer[idx] = {
                                "id": tool_call.id or f"call_{idx}",
                                "name": "",
                                "arguments": "",
                            }

                        # Accumulate function name
                        if tool_call.function and tool_call.function.name:
                            tool_calls_buffer[idx]["name"] = tool_call.function.name

                        # Accumulate arguments
                        if tool_call.function and tool_call.function.arguments:
                            tool_calls_buffer[idx]["arguments"] += tool_call.function.arguments

                # Check if done
                if choice.finish_reason:
                    # Emit tool calls if any
                    if tool_calls_buffer:

                        tool_calls = []
                        for tc in tool_calls_buffer.values():
                            try:
                                args = json.loads(tc["arguments"]) if tc["arguments"] else {}
                            except json.JSONDecodeError:
                                args = {}

                            tool_calls.append(
                                {"id": tc["id"], "name": tc["name"], "arguments": args}
                            )

                        yield LLMResponse(type="tool_call", content=None, tool_calls=tool_calls)

                    yield LLMResponse(type="done", content=None, finish_reason=choice.finish_reason)

        except Exception as e:
            logger.error(f"OpenAI streaming error: {e}")
            yield LLMResponse(type="error", content=str(e))
