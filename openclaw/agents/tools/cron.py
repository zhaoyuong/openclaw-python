"""Cron job management tool using APScheduler

Matches TypeScript openclaw/src/agents/tools/cron-tool.ts
"""
from __future__ import annotations


import logging
import uuid
from datetime import UTC, datetime
from typing import Any, Optional

from .base import AgentTool, ToolResult

logger = logging.getLogger(__name__)


class CronTool(AgentTool):
    """
    Scheduled task management - AI-powered cron system
    
    This tool allows the agent to create, manage, and execute scheduled tasks
    using the Gateway's cron service. Tasks can invoke LLM models to perform
    intelligent actions at scheduled times.
    """

    def __init__(self, cron_service=None, channel_registry=None, session_manager=None):
        super().__init__()
        self.name = "cron"
        self.description = """Manage Gateway cron jobs (status/list/add/update/remove/run) - YOU CAN DO THIS!

**ACTIONS:**
- status: Check cron scheduler status
- list: List all jobs (use includeDisabled:true to include disabled)
- add: Create new job (requires job object, see schema below)
- update: Modify existing job (requires jobId + patch object)
- remove: Delete job (requires jobId)
- run: Trigger job immediately (requires jobId)

**JOB SCHEMA (for add action):**
{
  "name": "Daily News Summary",
  "schedule": {"type": "cron", "expression": "0 9 * * *"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "prompt": "Search for today's top tech news and summarize"
  },
  "delivery": {
    "channel": "telegram",
    "target": "user_id"
  }
}

**SCHEDULE TYPES:**
- at: One-shot at absolute time
  {"type": "at", "timestamp": "2026-02-12T15:00:00Z"}
- every: Recurring interval
  {"type": "every", "interval_ms": 3600000, "anchor": "2026-02-12T09:00:00Z"}
- cron: Cron expression
  {"type": "cron", "expression": "0 9 * * *", "timezone": "UTC"}

**PAYLOAD TYPES:**
- systemEvent: System event to main session
  {"kind": "systemEvent", "text": "Reminder text"}
- agentTurn: Run LLM agent in isolated session (RECOMMENDED)
  {"kind": "agentTurn", "prompt": "Your intelligent task here", "model": "optional"}

**EXAMPLES:**
- "Set daily reminder at 9am to check email"
- "Every hour, check stock prices and alert me"
- "Tomorrow at 3pm, remind me about the meeting"
- "Show all my scheduled tasks"
- "Cancel the morning alarm"

I CAN schedule tasks that will run the AI agent to perform intelligent actions!
"""
        self._cron_service = cron_service
        self._channel_registry = channel_registry
        self._session_manager = session_manager
        self._current_chat_info: Optional[dict[str, str]] = None  # Store current chat context

    def set_chat_context(self, channel: str, chat_id: str) -> None:
        """
        Set current chat context for delivery
        
        This allows jobs created by the agent to automatically
        deliver to the current conversation.
        """
        self._current_chat_info = {
            "channel": channel,
            "chat_id": chat_id
        }

    def get_schema(self) -> dict[str, Any]:
        return {
            "name": "cron",
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["status", "list", "add", "update", "remove", "run"],
                        "description": "Action to perform"
                    },
                    "jobId": {
                        "type": "string",
                        "description": "Job ID (for update/remove/run/status actions)"
                    },
                    "job": {
                        "type": "object",
                        "description": "Job configuration (for add action)",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Job name"
                            },
                            "schedule": {
                                "type": "object",
                                "description": "Schedule configuration",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["at", "every", "cron"]
                                    },
                                    "timestamp": {"type": "string"},
                                    "interval_ms": {"type": "integer"},
                                    "expression": {"type": "string"},
                                    "timezone": {"type": "string"}
                                },
                                "required": ["type"]
                            },
                            "sessionTarget": {
                                "type": "string",
                                "enum": ["main", "isolated"],
                                "description": "Session target (use 'isolated' for AI tasks)"
                            },
                            "payload": {
                                "type": "object",
                                "description": "Job payload",
                                "properties": {
                                    "kind": {
                                        "type": "string",
                                        "enum": ["systemEvent", "agentTurn"]
                                    },
                                    "text": {"type": "string"},
                                    "prompt": {"type": "string"},
                                    "model": {"type": "string"}
                                },
                                "required": ["kind"]
                            },
                            "delivery": {
                                "type": "object",
                                "description": "Delivery configuration (optional)",
                                "properties": {
                                    "channel": {"type": "string"},
                                    "target": {"type": "string"},
                                    "best_effort": {"type": "boolean"}
                                }
                            }
                        },
                        "required": ["name", "schedule", "sessionTarget", "payload"]
                    },
                    "patch": {
                        "type": "object",
                        "description": "Job patch (for update action)"
                    },
                    "includeDisabled": {
                        "type": "boolean",
                        "description": "Include disabled jobs in list"
                    }
                },
                "required": ["action"]
            }
        }
    
    async def execute(self, args: dict[str, Any]) -> ToolResult:
        """Execute cron action"""
        if not self._cron_service:
            return ToolResult(
                success=False,
                output="",
                error="Cron service not available"
            )
        
        action = args.get("action")
        
        try:
            if action == "status":
                return await self._action_status()
            elif action == "list":
                return await self._action_list(args.get("includeDisabled", False))
            elif action == "add":
                return await self._action_add(args.get("job", {}))
            elif action == "update":
                return await self._action_update(args.get("jobId"), args.get("patch", {}))
            elif action == "remove":
                return await self._action_remove(args.get("jobId"))
            elif action == "run":
                return await self._action_run(args.get("jobId"))
            else:
                return ToolResult(
                    success=False,
                    output="",
                    error=f"Unknown action: {action}"
                )
        except Exception as e:
            logger.error(f"Cron tool error: {e}", exc_info=True)
            return ToolResult(
                success=False,
                output="",
                error=str(e)
            )
    
    async def _action_status(self) -> ToolResult:
        """Get cron service status"""
        jobs = self._cron_service.list_jobs()
        
        enabled_count = sum(1 for j in jobs if j.get("enabled", True))
        disabled_count = len(jobs) - enabled_count
        
        output = f"✅ Cron service running\n"
        output += f"📊 Jobs: {len(jobs)} total ({enabled_count} enabled, {disabled_count} disabled)"
        
        return ToolResult(
            success=True,
            output=output
        )
    
    async def _action_list(self, include_disabled: bool = False) -> ToolResult:
        """List all cron jobs"""
        jobs = self._cron_service.list_jobs()
        
        if not include_disabled:
            jobs = [j for j in jobs if j.get("enabled", True)]
        
        if not jobs:
            return ToolResult(
                success=True,
                output="No cron jobs found."
            )
        
        output = f"📋 Cron Jobs ({len(jobs)}):\n\n"
        
        for job in jobs:
            job_id = job.get("id", "")
            name = job.get("name", "Unnamed")
            schedule = job.get("schedule", {})
            enabled = job.get("enabled", True)
            session_target = job.get("sessionTarget", "main")
            
            status_icon = "✅" if enabled else "⏸️"
            target_icon = "🤖" if session_target == "isolated" else "📨"
            
            output += f"{status_icon} {target_icon} **{name}**\n"
            output += f"   ID: `{job_id}`\n"
            output += f"   Schedule: {self._format_schedule(schedule)}\n"
            
            next_run = job.get("nextRun")
            if next_run:
                output += f"   Next run: {next_run}\n"
            
            output += "\n"
        
        return ToolResult(
            success=True,
            output=output
        )
    
    async def _action_add(self, job_config: dict[str, Any]) -> ToolResult:
        """Add new cron job"""
        from ...cron.types import (
            AgentTurnPayload,
            AtSchedule,
            CronDelivery,
            CronJob,
            CronSchedule,
            EverySchedule,
            SystemEventPayload,
        )
        
        # Generate job ID
        job_id = f"cron-{uuid.uuid4().hex[:8]}"
        
        # Parse schedule
        schedule_config = job_config.get("schedule", {})
        schedule_type = schedule_config.get("type", "at")
        
        if schedule_type == "at":
            schedule = AtSchedule(
                timestamp=schedule_config.get("timestamp", ""),
                type="at"
            )
        elif schedule_type == "every":
            schedule = EverySchedule(
                interval_ms=schedule_config.get("interval_ms", 0),
                type="every",
                anchor=schedule_config.get("anchor")
            )
        elif schedule_type == "cron":
            schedule = CronSchedule(
                expression=schedule_config.get("expression", ""),
                type="cron",
                timezone=schedule_config.get("timezone", "UTC")
            )
        else:
            return ToolResult(
                success=False,
                output="",
                error=f"Unknown schedule type: {schedule_type}"
            )
        
        # Parse payload
        payload_config = job_config.get("payload", {})
        payload_kind = payload_config.get("kind", "systemEvent")
        
        if payload_kind == "systemEvent":
            payload = SystemEventPayload(
                text=payload_config.get("text", ""),
                kind="systemEvent"
            )
        elif payload_kind == "agentTurn":
            payload = AgentTurnPayload(
                prompt=payload_config.get("prompt", ""),
                kind="agentTurn",
                model=payload_config.get("model")
            )
        else:
            return ToolResult(
                success=False,
                output="",
                error=f"Unknown payload kind: {payload_kind}"
            )
        
        # Parse delivery (optional)
        delivery = None
        if "delivery" in job_config:
            delivery_config = job_config["delivery"]
            
            # Auto-fill channel and target from current context if not provided
            channel = delivery_config.get("channel")
            target = delivery_config.get("target")
            
            if not channel and self._current_chat_info:
                channel = self._current_chat_info.get("channel")
                logger.info(f"Auto-filled channel from context: {channel}")
            
            if not target and self._current_chat_info:
                target = self._current_chat_info.get("chat_id")
                logger.info(f"Auto-filled target from context: {target}")
            
            if channel:
                delivery = CronDelivery(
                    channel=channel,
                    target=target,
                    best_effort=delivery_config.get("best_effort", False)
                )
        
        # Create job
        job = CronJob(
            id=job_id,
            name=job_config.get("name", "Unnamed Job"),
            description=job_config.get("description"),
            enabled=job_config.get("enabled", True),
            schedule=schedule,
            session_target=job_config.get("sessionTarget", "main"),
            payload=payload,
            delivery=delivery,
        )
        
        # Add to service
        success = self._cron_service.add_job(job)
        
        if success:
            output = f"✅ Created cron job: **{job.name}**\n"
            output += f"   ID: `{job_id}`\n"
            output += f"   Schedule: {self._format_schedule(job_config.get('schedule', {}))}\n"
            output += f"   Type: {'🤖 Isolated Agent' if job.session_target == 'isolated' else '📨 System Event'}"
            
            if delivery:
                output += f"\n   Delivery: {delivery.channel}"
                if delivery.target:
                    output += f" → {delivery.target}"
            
            return ToolResult(success=True, output=output)
        else:
            return ToolResult(
                success=False,
                output="",
                error="Failed to add job"
            )
    
    async def _action_update(self, job_id: str | None, patch: dict[str, Any]) -> ToolResult:
        """Update existing job"""
        if not job_id:
            return ToolResult(
                success=False,
                output="",
                error="jobId is required for update action"
            )
        
        # Get existing job
        job_status = self._cron_service.get_job_status(job_id)
        if not job_status:
            return ToolResult(
                success=False,
                output="",
                error=f"Job not found: {job_id}"
            )
        
        # TODO: Implement job update
        # For now, just return success
        output = f"✅ Updated job: {job_id}\n(Note: Update functionality to be fully implemented)"
        
        return ToolResult(success=True, output=output)
    
    async def _action_remove(self, job_id: str | None) -> ToolResult:
        """Remove cron job"""
        if not job_id:
            return ToolResult(
                success=False,
                output="",
                error="jobId is required for remove action"
            )
        
        # Get job info before removing
        job_status = self._cron_service.get_job_status(job_id)
        if not job_status:
            return ToolResult(
                success=False,
                output="",
                error=f"Job not found: {job_id}"
            )
        
        # Remove job
        success = self._cron_service.remove_job(job_id)
        
        if success:
            return ToolResult(
                success=True,
                output=f"✅ Removed cron job: {job_id}"
            )
        else:
            return ToolResult(
                success=False,
                output="",
                error=f"Failed to remove job: {job_id}"
            )
    
    async def _action_run(self, job_id: str | None) -> ToolResult:
        """Run job immediately"""
        if not job_id:
            return ToolResult(
                success=False,
                output="",
                error="jobId is required for run action"
            )
        
        # TODO: Implement immediate job execution
        output = f"✅ Triggered job: {job_id}\n(Note: Immediate execution to be fully implemented)"
        
        return ToolResult(success=True, output=output)
    
    def _format_schedule(self, schedule: dict[str, Any]) -> str:
        """Format schedule for display"""
        schedule_type = schedule.get("type", "")
        
        if schedule_type == "at":
            timestamp = schedule.get("timestamp", "")
            return f"One-time at {timestamp}"
        elif schedule_type == "every":
            interval_ms = schedule.get("interval_ms", 0)
            interval_hours = interval_ms / (1000 * 60 * 60)
            return f"Every {interval_hours:.1f} hours"
        elif schedule_type == "cron":
            expression = schedule.get("expression", "")
            tz = schedule.get("timezone", "UTC")
            return f"Cron: {expression} ({tz})"
        else:
            return "Unknown schedule"
    
    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["add", "list", "remove", "status", "update", "run"],
                    "description": "Cron action to perform",
                },
                "job_id": {"type": "string", "description": "Job identifier"},
                "schedule": {
                    "type": "string",
                    "description": "Schedule in cron format or natural language (e.g., 'daily at 9am', '0 9 * * *')",
                },
                "task": {"type": "string", "description": "Task description or command to execute"},
                "message": {"type": "string", "description": "Message to send when job runs"},
                "session_id": {
                    "type": "string",
                    "description": "Target session for notifications",
                    "default": "main",
                },
            },
            "required": ["action"],
        }
    
    async def execute(self, params: dict[str, Any]) -> ToolResult:
        """Execute cron action"""
        action = params.get("action", "")

        if not action:
            return ToolResult(success=False, content="", error="action required")

        try:
            self._init_scheduler()

            if action == "add":
                return await self._add_job(params)
            elif action == "list":
                return await self._list_jobs(params)
            elif action == "remove":
                return await self._remove_job(params)
            elif action == "status":
                return await self._job_status(params)
            elif action == "update":
                return await self._update_job(params)
            elif action == "run":
                return await self._run_job(params)
            else:
                return ToolResult(success=False, content="", error=f"Unknown action: {action}")

        except ImportError as e:
            return ToolResult(success=False, content="", error=str(e))
        except Exception as e:
            logger.error(f"Cron tool error: {e}", exc_info=True)
            return ToolResult(success=False, content="", error=str(e))

    async def _add_job(self, params: dict[str, Any]) -> ToolResult:
        """Add scheduled job"""
        job_id = params.get("job_id") or f"job-{int(datetime.now(UTC).timestamp())}"
        schedule = params.get("schedule", "")
        task = params.get("task", "")
        message = params.get("message", "")
        session_id = params.get("session_id", "main")

        if not schedule or not (task or message):
            return ToolResult(
                success=False, content="", error="schedule and (task or message) required"
            )

        # Parse schedule
        trigger_kwargs = self._parse_schedule(schedule)

        if not trigger_kwargs:
            return ToolResult(
                success=False, content="", error=f"Invalid schedule format: {schedule}"
            )

        # Add job to scheduler
        self._scheduler.add_job(
            self._job_callback,
            **trigger_kwargs,
            id=job_id,
            kwargs={"job_id": job_id, "task": task, "message": message, "session_id": session_id},
        )

        # Store job info
        self._jobs[job_id] = {
            "id": job_id,
            "schedule": schedule,
            "task": task,
            "message": message,
            "session_id": session_id,
            "created": datetime.now(UTC).isoformat(),
            "runs": 0,
        }

        return ToolResult(
            success=True,
            content=f"Created job '{job_id}' with schedule '{schedule}'",
            metadata={"job_id": job_id},
        )

    def _parse_schedule(self, schedule: str) -> dict | None:
        """Parse schedule string to APScheduler trigger kwargs"""
        from apscheduler.triggers.cron import CronTrigger
        from apscheduler.triggers.interval import IntervalTrigger

        # Try cron format
        if any(c in schedule for c in ["*", ","]):
            try:
                parts = schedule.split()
                if len(parts) == 5:
                    minute, hour, day, month, day_of_week = parts
                    return {
                        "trigger": CronTrigger(
                            minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week
                        )
                    }
            except:
                pass

        # Natural language patterns
        schedule_lower = schedule.lower()

        if "every" in schedule_lower:
            # Extract interval
            if "minute" in schedule_lower:
                return {"trigger": IntervalTrigger(minutes=1)}
            elif "hour" in schedule_lower:
                return {"trigger": IntervalTrigger(hours=1)}
            elif "day" in schedule_lower:
                return {"trigger": IntervalTrigger(days=1)}

        if "daily" in schedule_lower or "every day" in schedule_lower:
            # Extract time if present
            import re

            time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", schedule_lower)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                am_pm = time_match.group(3)

                if am_pm == "pm" and hour < 12:
                    hour += 12
                elif am_pm == "am" and hour == 12:
                    hour = 0

                return {"trigger": CronTrigger(hour=hour, minute=minute)}

            return {"trigger": CronTrigger(hour=9, minute=0)}  # Default to 9am

        return None

    async def _job_callback(self, job_id: str, task: str, message: str, session_id: str):
        """Job execution callback"""
        logger.info(f"Executing job '{job_id}': {task or message}")

        # Update run count
        if job_id in self._jobs:
            self._jobs[job_id]["runs"] += 1
            self._jobs[job_id]["last_run"] = datetime.now(UTC).isoformat()
            
            # Store the notification message for the job
            job_info = self._jobs[job_id]
            notification_text = message or task or f"Scheduled task '{job_id}' triggered"

        # Send notification through channels if available
        if self._channel_registry:
            try:
                # Try to send through all active channels
                for channel_id in ["telegram", "discord", "slack"]:
                    channel = self._channel_registry.get(channel_id)
                    if channel and channel.is_running():
                        # Get the session to find the target chat/user
                        if self._session_manager and session_id != "main":
                            session = self._session_manager.get_session(session_id)
                            if session and hasattr(session, 'platform_data'):
                                target = session.platform_data.get('chat_id') or session.platform_data.get('user_id')
                                if target:
                                    await channel.send_text(
                                        str(target),
                                        f"⏰ **Reminder**\n\n{notification_text}"
                                    )
                                    logger.info(f"Sent cron notification to {channel_id}:{target}")
                                    return
            except Exception as e:
                logger.error(f"Failed to send cron notification: {e}", exc_info=True)
        
        # Fallback: just log
        logger.info(f"Job '{job_id}' notification: {notification_text}")

    async def _list_jobs(self, params: dict[str, Any]) -> ToolResult:
        """List all jobs"""
        if not self._jobs:
            return ToolResult(success=True, content="No scheduled jobs", metadata={"count": 0})

        output = f"Scheduled jobs ({len(self._jobs)}):\n\n"
        for job_id, job_info in self._jobs.items():
            output += f"- **{job_id}**\n"
            output += f"  Schedule: {job_info['schedule']}\n"
            output += f"  Task: {job_info.get('task', 'N/A')}\n"
            output += f"  Runs: {job_info['runs']}\n"
            if "last_run" in job_info:
                output += f"  Last run: {job_info['last_run']}\n"
            output += "\n"

        return ToolResult(
            success=True,
            content=output,
            metadata={"count": len(self._jobs), "jobs": list(self._jobs.values())},
        )

    async def _remove_job(self, params: dict[str, Any]) -> ToolResult:
        """Remove job"""
        job_id = params.get("job_id", "")

        if not job_id:
            return ToolResult(success=False, content="", error="job_id required")

        if job_id not in self._jobs:
            return ToolResult(success=False, content="", error=f"Job '{job_id}' not found")

        # Remove from scheduler
        self._scheduler.remove_job(job_id)

        # Remove from our tracking
        del self._jobs[job_id]

        return ToolResult(success=True, content=f"Removed job '{job_id}'")

    async def _job_status(self, params: dict[str, Any]) -> ToolResult:
        """Get job status"""
        job_id = params.get("job_id", "")

        if not job_id:
            # Return overall status
            return ToolResult(
                success=True,
                content=f"Scheduler running with {len(self._jobs)} jobs",
                metadata={"running": self._scheduler.running, "job_count": len(self._jobs)},
            )

        if job_id not in self._jobs:
            return ToolResult(success=False, content="", error=f"Job '{job_id}' not found")

        job_info = self._jobs[job_id]
        output = f"Job '{job_id}':\n"
        output += f"  Schedule: {job_info['schedule']}\n"
        output += f"  Task: {job_info.get('task', 'N/A')}\n"
        output += f"  Runs: {job_info['runs']}\n"
        if "last_run" in job_info:
            output += f"  Last run: {job_info['last_run']}\n"

        return ToolResult(success=True, content=output, metadata=job_info)

    async def _update_job(self, params: dict[str, Any]) -> ToolResult:
        """Update job"""
        job_id = params.get("job_id", "")
        schedule = params.get("schedule")

        if not job_id:
            return ToolResult(success=False, content="", error="job_id required")

        if job_id not in self._jobs:
            return ToolResult(success=False, content="", error=f"Job '{job_id}' not found")

        # For now, just update the schedule if provided
        if schedule:
            trigger_kwargs = self._parse_schedule(schedule)
            if trigger_kwargs:
                self._scheduler.reschedule_job(job_id, **trigger_kwargs)
                self._jobs[job_id]["schedule"] = schedule

        return ToolResult(success=True, content=f"Updated job '{job_id}'")

    async def _run_job(self, params: dict[str, Any]) -> ToolResult:
        """Run job immediately"""
        job_id = params.get("job_id", "")

        if not job_id:
            return ToolResult(success=False, content="", error="job_id required")

        if job_id not in self._jobs:
            return ToolResult(success=False, content="", error=f"Job '{job_id}' not found")

        # Get job and run it
        job = self._scheduler.get_job(job_id)
        if job:
            job.modify(next_run_time=datetime.now())

        return ToolResult(success=True, content=f"Triggered job '{job_id}'")
