"""
Vector Engine provider implementation (OpenAI-compatible)
We find it hard to use openai directly due to data privacy concerns, so we
implement a provider that hardcodes the base_url to Vector Engine's API endpoint.
"""

import logging

from .openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)


class VectorEngineProvider(OpenAIProvider):
    """
    Vector Engine Provider

    Hardcodes the base_url to ensure requests never leak to OpenAI's official servers.
    """

    def __init__(
        self, model: str, api_key: str | None = None, base_url: str | None = None, **kwargs
    ):
        # Hardcode the base_url for Vector Engine
        base_url = base_url or "https://api.vectorengine.ai/v1"
        super().__init__(model=model, api_key=api_key, base_url=base_url, **kwargs)

    @property
    def provider_name(self) -> str:
        return "vectorengine"
