"""
Hook system integration with Cron service

Provides bridge for hooks to create cron jobs dynamically.
Aligned with TypeScript hook→cron integration.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..cron import CronService
    from ..cron.types import CronJob

logger = logging.getLogger(__name__)


async def create_cron_job_from_hook(
    hook_result: dict[str, Any],
    cron_service: 'CronService',
    delivery_config: dict[str, Any] | None = None,
) -> str:
    """
    Create a one-shot cron job from hook result
    
    TypeScript equivalent: dispatchAgentHook creates cron job
    
    This allows hooks to schedule delayed agent execution, for example:
    - Gmail hook receives email → schedules agent to process it
    - Calendar hook detects event → schedules reminder
    - Custom hook triggers → schedules agent action
    
    Args:
        hook_result: Hook execution result containing:
            - hook_name: Name of the hook
            - message: Message/prompt for agent
            - agent_id: Optional agent ID
            - model: Optional model override
            - thinking: Optional thinking level
            - timeout: Optional timeout
        cron_service: Cron service instance
        delivery_config: Optional delivery configuration
        
    Returns:
        Created job ID
    """
    from ..cron.types import CronJob, AtSchedule, AgentTurnPayload
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Extract hook info
    hook_name = hook_result.get("hook_name", "unknown")
    message = hook_result.get("message", "")
    agent_id = hook_result.get("agent_id")
    model = hook_result.get("model")
    thinking = hook_result.get("thinking")
    timeout = hook_result.get("timeout")
    
    if not message:
        raise ValueError("Hook result must include 'message' field")
    
    # Create one-shot schedule (run immediately)
    schedule = AtSchedule(
        timestamp=datetime.now(timezone.utc).isoformat(),
        type="at"
    )
    
    # Build delivery config if provided
    delivery = None
    if delivery_config:
        from ..cron.types import CronDelivery
        
        delivery = CronDelivery(
            mode=delivery_config.get("mode", "announce"),
            channel=delivery_config.get("channel", "last"),
            target=delivery_config.get("target"),
            best_effort=delivery_config.get("best_effort", False)
        )
    
    # Create agent turn payload
    payload = AgentTurnPayload(
        kind="agentTurn",
        message=message,
        model=model,
        thinking=thinking,
        timeout_seconds=timeout,
        delivery=delivery
    )
    
    # Create cron job
    job = CronJob(
        id=job_id,
        name=f"hook-{hook_name}",
        schedule=schedule,
        session_target="isolated",
        agent_id=agent_id,
        payload=payload,
        enabled=True,
        delete_after_run=True,  # One-shot job
        metadata={"source": "hook", "hook_name": hook_name}
    )
    
    # Add to cron service
    cron_service.add_job(job)
    
    logger.info(f"Created cron job {job_id} from hook '{hook_name}'")
    
    return job_id


async def create_delayed_cron_job(
    message: str,
    delay_seconds: int,
    cron_service: 'CronService',
    agent_id: str | None = None,
    delivery_config: dict[str, Any] | None = None,
    name: str | None = None,
) -> str:
    """
    Create a delayed cron job
    
    Useful for scheduling agent tasks with a delay, for example:
    - "Remind me in 1 hour"
    - "Check again in 30 minutes"
    
    Args:
        message: Message/prompt for agent
        delay_seconds: Delay in seconds before execution
        cron_service: Cron service instance
        agent_id: Optional agent ID
        delivery_config: Optional delivery configuration
        name: Optional job name
        
    Returns:
        Created job ID
    """
    from ..cron.types import CronJob, AtSchedule, AgentTurnPayload, CronDelivery
    from datetime import timedelta
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Calculate execution time
    run_at = datetime.now(timezone.utc) + timedelta(seconds=delay_seconds)
    
    # Create schedule
    schedule = AtSchedule(
        timestamp=run_at.isoformat(),
        type="at"
    )
    
    # Build delivery
    delivery = None
    if delivery_config:
        delivery = CronDelivery(
            mode=delivery_config.get("mode", "announce"),
            channel=delivery_config.get("channel", "last"),
            target=delivery_config.get("target"),
            best_effort=delivery_config.get("best_effort", False)
        )
    
    # Create payload
    payload = AgentTurnPayload(
        kind="agentTurn",
        message=message,
        delivery=delivery
    )
    
    # Create job
    job = CronJob(
        id=job_id,
        name=name or f"delayed-{delay_seconds}s",
        schedule=schedule,
        session_target="isolated",
        agent_id=agent_id,
        payload=payload,
        enabled=True,
        delete_after_run=True,
        metadata={"source": "delayed", "delay_seconds": delay_seconds}
    )
    
    # Add to service
    cron_service.add_job(job)
    
    logger.info(f"Created delayed cron job {job_id} (delay: {delay_seconds}s)")
    
    return job_id


async def create_recurring_cron_job(
    message: str,
    interval_ms: int,
    cron_service: 'CronService',
    agent_id: str | None = None,
    delivery_config: dict[str, Any] | None = None,
    name: str | None = None,
    max_runs: int | None = None,
) -> str:
    """
    Create a recurring cron job
    
    Useful for periodic agent tasks:
    - "Check email every 5 minutes"
    - "Generate daily report"
    
    Args:
        message: Message/prompt for agent
        interval_ms: Interval in milliseconds
        cron_service: Cron service instance
        agent_id: Optional agent ID
        delivery_config: Optional delivery configuration
        name: Optional job name
        max_runs: Optional maximum number of runs (auto-delete after)
        
    Returns:
        Created job ID
    """
    from ..cron.types import CronJob, EverySchedule, AgentTurnPayload, CronDelivery
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Create schedule
    schedule = EverySchedule(
        interval_ms=interval_ms,
        type="every"
    )
    
    # Build delivery
    delivery = None
    if delivery_config:
        delivery = CronDelivery(
            mode=delivery_config.get("mode", "announce"),
            channel=delivery_config.get("channel", "last"),
            target=delivery_config.get("target"),
            best_effort=delivery_config.get("best_effort", False)
        )
    
    # Create payload
    payload = AgentTurnPayload(
        kind="agentTurn",
        message=message,
        delivery=delivery
    )
    
    # Create job
    job = CronJob(
        id=job_id,
        name=name or f"recurring-{interval_ms}ms",
        schedule=schedule,
        session_target="isolated",
        agent_id=agent_id,
        payload=payload,
        enabled=True,
        delete_after_run=False,  # Recurring
        metadata={
            "source": "recurring",
            "interval_ms": interval_ms,
            "max_runs": max_runs,
            "run_count": 0
        }
    )
    
    # Add to service
    cron_service.add_job(job)
    
    logger.info(f"Created recurring cron job {job_id} (interval: {interval_ms}ms)")
    
    return job_id


def needs_cron_job(hook_result: dict[str, Any]) -> bool:
    """
    Check if hook result should create a cron job
    
    Args:
        hook_result: Hook execution result
        
    Returns:
        True if cron job should be created
    """
    # Check if result explicitly requests cron job
    if hook_result.get("create_cron_job"):
        return True
    
    # Check if result has delayed execution
    if hook_result.get("delay_seconds"):
        return True
    
    # Check if result is for asynchronous processing
    if hook_result.get("async_processing"):
        return True
    
    return False
