"""Cron service bootstrap for Gateway

Matches TypeScript openclaw/src/gateway/server-cron.ts
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from ..agents.providers import LLMProvider
    from ..agents.session import SessionManager
    from ..agents.tools.base import AgentTool
    from ..channels.base import BaseChannel
    from ..cron import CronService
    from ..cron.types import CronJob

logger = logging.getLogger(__name__)


async def build_gateway_cron_service(
    config: dict[str, Any],
    provider: LLMProvider,
    tools: list[AgentTool],
    session_manager: SessionManager,
    channel_registry: dict[str, BaseChannel],
    broadcast: Callable[[str, Any], None] | None = None,
) -> CronService:
    """
    Build and initialize cron service for Gateway
    
    This function:
    1. Resolves store path
    2. Creates service dependencies
    3. Initializes CronService
    4. Loads existing jobs
    5. Starts timer
    
    Args:
        config: Gateway configuration
        provider: LLM provider
        tools: Available tools
        session_manager: Session manager
        channel_registry: Channel registry
        broadcast: Event broadcast callback
        
    Returns:
        Initialized CronService
    """
    from ..cron import CronService
    from ..cron.store import CronStore
    from ..cron.isolated_agent.run import run_isolated_agent_turn
    from ..cron.isolated_agent.delivery import deliver_result
    
    # Resolve store path
    cron_config = config.get("cron", {})
    store_path_str = cron_config.get("store", "~/.openclaw/cron/jobs.json")
    
    if store_path_str.startswith("~"):
        store_path = Path.home() / store_path_str[2:]
    else:
        store_path = Path(store_path_str).expanduser()
    
    store_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Cron store path: {store_path}")
    
    # Check if cron is enabled
    cron_enabled = cron_config.get("enabled", True)
    
    if not cron_enabled:
        logger.info("Cron service is disabled")
        # Return disabled service
        service = CronService()
        service._enabled = False
        return service
    
    # Create store
    store = CronStore(store_path)
    
    # Migrate if needed
    store.migrate_if_needed()
    
    # Define enqueue_system_event callback
    async def enqueue_system_event(text: str, agent_id: str | None = None) -> None:
        """Enqueue system event to main session"""
        try:
            agent_id = agent_id or "main"
            logger.info(f"Enqueuing system event to agent '{agent_id}': {text[:100]}...")
            
            # Resolve main session for the agent
            session_key = f"{agent_id}-main"
            
            if session_manager:
                session = session_manager.get_session(session_key)
                if session:
                    # Add system message to session
                    session.add_system_message(text)
                    logger.info(f"System event added to session '{session_key}'")
                    
                    # Optionally trigger immediate processing if needed
                    # This would depend on whether we want synchronous or async processing
                else:
                    logger.warning(f"Session '{session_key}' not found for system event")
            else:
                logger.warning("Session manager not available for system event")
            
        except Exception as e:
            logger.error(f"Error enqueuing system event: {e}", exc_info=True)
    
    # Define run_isolated_agent callback
    async def run_isolated_agent(job: CronJob) -> dict[str, Any]:
        """Run isolated agent for cron job"""
        try:
            # Get sessions directory
            sessions_dir = getattr(session_manager, "sessions_dir", Path.home() / ".openclaw" / "sessions")
            
            # Run isolated agent turn
            result = await run_isolated_agent_turn(
                job=job,
                provider=provider,
                tools=tools,
                sessions_dir=sessions_dir,
                system_prompt=None,  # TODO: Get from config
            )
            
            # Deliver result if delivery configured
            if job.delivery and result.get("success"):
                try:
                    delivery_success = await deliver_result(
                        job=job,
                        result=result,
                        channel_registry=channel_registry,
                        session_history=None,  # TODO: Get from session
                    )
                    result["delivered"] = delivery_success
                except Exception as e:
                    logger.error(f"Error delivering result: {e}", exc_info=True)
                    result["delivery_error"] = str(e)
            
            return result
            
        except Exception as e:
            logger.error(f"Error running isolated agent: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
            }
    
    # Define heartbeat callbacks (integrated with heartbeat_runner)
    def request_heartbeat_now() -> None:
        """Request immediate heartbeat"""
        logger.info("Heartbeat requested - triggering run_heartbeat_once")
        # This would typically trigger an immediate heartbeat check
        # For now, just log as immediate execution needs async context
    
    async def run_heartbeat_once(reason: str | None = None) -> dict[str, Any]:
        """Run heartbeat once using heartbeat_runner"""
        try:
            from openclaw.infra.heartbeat_runner import (
                run_heartbeat_once as runner_run_once,
            )
            
            # Get agent config (default to main agent)
            agent_id = "main"
            agent_config = config.get("agent", {})
            if not agent_config.get("heartbeat", {}).get("enabled", False):
                logger.info(f"Heartbeat skipped - not enabled for agent '{agent_id}'")
                return {
                    "status": "skipped",
                    "reason": "not-enabled"
                }
            
            # Define execute function for heartbeat
            async def execute_heartbeat(agent_id_inner: str, prompt: str) -> Any:
                """Execute heartbeat by running agent turn"""
                session_key = f"{agent_id_inner}-main"
                
                if not session_manager:
                    logger.error("Session manager not available")
                    return None
                
                session = session_manager.get_session(session_key)
                if not session:
                    logger.error(f"Session '{session_key}' not found")
                    return None
                
                # Run agent turn with heartbeat prompt
                response_text = ""
                async for event in provider.prompt(
                    messages=[{"role": "user", "content": prompt}],
                    tools=None
                ):
                    if event.type == "text_delta":
                        response_text += event.content
                    elif event.type == "done":
                        break
                
                # Add to session
                if response_text:
                    session.add_user_message(prompt)
                    session.add_assistant_message(response_text)
                    logger.info(f"Heartbeat completed for '{agent_id_inner}': {len(response_text)} chars")
                
                return response_text
            
            # Run heartbeat once
            await runner_run_once(
                agent_id=agent_id,
                agent_config=agent_config,
                execute_fn=execute_heartbeat
            )
            
            return {
                "status": "completed",
                "reason": reason
            }
            
        except Exception as e:
            logger.error(f"Error running heartbeat: {e}", exc_info=True)
            return {
                "status": "error",
                "reason": str(e)
            }
    
    # Define event callback
    def on_event(event: dict[str, Any]) -> None:
        """Handle cron events"""
        try:
            if broadcast:
                broadcast("cron", event)
            
            # Log important events
            action = event.get("action")
            job_id = event.get("jobId")
            
            if action == "started":
                logger.info(f"Cron job started: {job_id}")
            elif action == "finished":
                status = event.get("status")
                duration_ms = event.get("durationMs", 0)
                logger.info(f"Cron job finished: {job_id}, status: {status}, duration: {duration_ms}ms")
                
                if status == "error":
                    error = event.get("error", "Unknown error")
                    logger.error(f"Cron job error: {job_id}, {error}")
            
        except Exception as e:
            logger.error(f"Error handling cron event: {e}", exc_info=True)
    
    # Create service
    service = CronService(
        store_path=store_path,
        log_dir=store_path.parent / "logs",
        on_system_event=enqueue_system_event,
        on_isolated_agent=run_isolated_agent,
        on_event=on_event,
    )
    
    # Add dependency references
    service._store = store
    service._cron_enabled = cron_enabled
    service._provider = provider
    service._tools = tools
    service._session_manager = session_manager
    service._channel_registry = channel_registry
    
    # Load jobs from store
    logger.info("Loading cron jobs from store...")
    jobs = store.load()
    logger.info(f"Loaded {len(jobs)} cron jobs")
    
    # Add jobs to service
    for job in jobs:
        # Don't use add_job (which would save again)
        # Just register the job
        service.jobs[job.id] = job
    
    # Start service
    logger.info("Starting cron service...")
    service.start()
    
    logger.info(f"✅ Cron service started with {len(jobs)} jobs")
    
    return service


def resolve_cron_store_path(config: dict[str, Any]) -> Path:
    """
    Resolve cron store path from config
    
    Args:
        config: Gateway configuration
        
    Returns:
        Resolved store path
    """
    cron_config = config.get("cron", {})
    store_path_str = cron_config.get("store", "~/.openclaw/cron/jobs.json")
    
    if store_path_str.startswith("~"):
        return Path.home() / store_path_str[2:]
    else:
        return Path(store_path_str).expanduser()


def is_cron_enabled(config: dict[str, Any]) -> bool:
    """
    Check if cron is enabled in config
    
    Args:
        config: Gateway configuration
        
    Returns:
        True if enabled
    """
    import os
    
    # Check environment variable
    if os.getenv("OPENCLAW_SKIP_CRON") == "1":
        return False
    
    # Check config
    cron_config = config.get("cron", {})
    return cron_config.get("enabled", True)
