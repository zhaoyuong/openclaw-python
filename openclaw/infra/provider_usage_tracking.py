"""LLM provider usage tracking

This module tracks LLM API usage including:
- Token consumption
- API costs
- Request counts
- Error rates
- Performance metrics
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class UsageMetrics:
    """Usage metrics for an LLM call"""
    
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    duration_ms: int = 0
    success: bool = True
    error: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class AggregatedMetrics:
    """Aggregated usage metrics"""
    
    provider: str
    model: str | None = None
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    avg_duration_ms: float = 0.0
    error_rate: float = 0.0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class UsageTracker:
    """Track LLM provider usage"""
    
    # Approximate pricing (per 1M tokens) - update as needed
    PRICING = {
        "anthropic/claude-3-opus": {"input": 15.0, "output": 75.0},
        "anthropic/claude-3-sonnet": {"input": 3.0, "output": 15.0},
        "anthropic/claude-3-haiku": {"input": 0.25, "output": 1.25},
        "openai/gpt-4": {"input": 30.0, "output": 60.0},
        "openai/gpt-4-turbo": {"input": 10.0, "output": 30.0},
        "openai/gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
        "google/gemini-pro": {"input": 0.5, "output": 1.5},
        "google/gemini-3-pro": {"input": 1.25, "output": 5.0},
    }
    
    def __init__(self, storage_path: Path | None = None):
        """
        Initialize usage tracker
        
        Args:
            storage_path: Path to store usage logs (JSONL format)
        """
        self.storage_path = storage_path
        self.metrics: list[UsageMetrics] = []
        
        if self.storage_path:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    def estimate_cost(
        self,
        provider: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> float:
        """
        Estimate cost for API call
        
        Args:
            provider: Provider name
            model: Model name
            prompt_tokens: Prompt tokens
            completion_tokens: Completion tokens
            
        Returns:
            Estimated cost in USD
        """
        key = f"{provider}/{model}"
        
        if key not in self.PRICING:
            logger.warning(f"No pricing info for {key}, using default")
            return 0.0
        
        pricing = self.PRICING[key]
        input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]
        
        return input_cost + output_cost
    
    def track(
        self,
        provider: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        duration_ms: int,
        success: bool = True,
        error: str | None = None,
    ) -> UsageMetrics:
        """
        Track an API call
        
        Args:
            provider: Provider name
            model: Model name
            prompt_tokens: Prompt tokens
            completion_tokens: Completion tokens
            duration_ms: Duration in milliseconds
            success: Whether call succeeded
            error: Error message if failed
            
        Returns:
            Usage metrics
        """
        total_tokens = prompt_tokens + completion_tokens
        cost = self.estimate_cost(provider, model, prompt_tokens, completion_tokens)
        
        metrics = UsageMetrics(
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=cost,
            duration_ms=duration_ms,
            success=success,
            error=error,
        )
        
        self.metrics.append(metrics)
        
        # Log to file if storage path configured
        if self.storage_path:
            try:
                with open(self.storage_path, "a") as f:
                    f.write(json.dumps(metrics.to_dict()) + "\n")
            except Exception as e:
                logger.error(f"Failed to write usage log: {e}")
        
        logger.info(
            f"Tracked: {provider}/{model} - "
            f"{total_tokens} tokens, ${cost:.4f}, {duration_ms}ms"
        )
        
        return metrics
    
    def get_aggregated_metrics(
        self,
        provider: str | None = None,
        model: str | None = None,
    ) -> AggregatedMetrics:
        """
        Get aggregated metrics
        
        Args:
            provider: Filter by provider (None = all)
            model: Filter by model (None = all)
            
        Returns:
            Aggregated metrics
        """
        # Filter metrics
        filtered = self.metrics
        if provider:
            filtered = [m for m in filtered if m.provider == provider]
        if model:
            filtered = [m for m in filtered if m.model == model]
        
        if not filtered:
            return AggregatedMetrics(
                provider=provider or "all",
                model=model,
            )
        
        # Aggregate
        total_requests = len(filtered)
        successful = len([m for m in filtered if m.success])
        failed = total_requests - successful
        
        total_prompt = sum(m.prompt_tokens for m in filtered)
        total_completion = sum(m.completion_tokens for m in filtered)
        total_tokens = sum(m.total_tokens for m in filtered)
        total_cost = sum(m.cost_usd for m in filtered)
        
        avg_duration = sum(m.duration_ms for m in filtered) / total_requests if total_requests > 0 else 0
        error_rate = failed / total_requests if total_requests > 0 else 0
        
        return AggregatedMetrics(
            provider=provider or "all",
            model=model,
            total_requests=total_requests,
            successful_requests=successful,
            failed_requests=failed,
            total_prompt_tokens=total_prompt,
            total_completion_tokens=total_completion,
            total_tokens=total_tokens,
            total_cost_usd=total_cost,
            avg_duration_ms=avg_duration,
            error_rate=error_rate,
        )
    
    def get_recent_metrics(self, limit: int = 100) -> list[UsageMetrics]:
        """
        Get recent metrics
        
        Args:
            limit: Maximum number of metrics to return
            
        Returns:
            List of recent metrics
        """
        return self.metrics[-limit:]
    
    def clear_metrics(self) -> None:
        """Clear all metrics"""
        self.metrics.clear()
    
    def export_metrics(self, output_path: Path) -> None:
        """
        Export metrics to file
        
        Args:
            output_path: Output file path
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            for metric in self.metrics:
                f.write(json.dumps(metric.to_dict()) + "\n")
        
        logger.info(f"Exported {len(self.metrics)} metrics to {output_path}")
    
    def load_metrics(self, input_path: Path) -> None:
        """
        Load metrics from file
        
        Args:
            input_path: Input file path
        """
        if not input_path.exists():
            logger.warning(f"Metrics file not found: {input_path}")
            return
        
        count = 0
        with open(input_path, "r") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    metric = UsageMetrics(**data)
                    self.metrics.append(metric)
                    count += 1
                except json.JSONDecodeError:
                    continue
        
        logger.info(f"Loaded {count} metrics from {input_path}")
    
    def get_cost_summary(self) -> dict[str, Any]:
        """
        Get cost summary
        
        Returns:
            Cost summary dictionary
        """
        total_cost = sum(m.cost_usd for m in self.metrics)
        
        # Group by provider
        by_provider: dict[str, float] = {}
        for metric in self.metrics:
            if metric.provider not in by_provider:
                by_provider[metric.provider] = 0.0
            by_provider[metric.provider] += metric.cost_usd
        
        # Group by model
        by_model: dict[str, float] = {}
        for metric in self.metrics:
            key = f"{metric.provider}/{metric.model}"
            if key not in by_model:
                by_model[key] = 0.0
            by_model[key] += metric.cost_usd
        
        return {
            "total_cost_usd": total_cost,
            "total_requests": len(self.metrics),
            "by_provider": by_provider,
            "by_model": by_model,
        }


# Global usage tracker
_usage_tracker: UsageTracker | None = None


def get_usage_tracker(storage_path: Path | None = None) -> UsageTracker:
    """
    Get global usage tracker
    
    Args:
        storage_path: Storage path (only used on first call)
        
    Returns:
        Global usage tracker instance
    """
    global _usage_tracker
    
    if _usage_tracker is None:
        _usage_tracker = UsageTracker(storage_path=storage_path)
    
    return _usage_tracker
