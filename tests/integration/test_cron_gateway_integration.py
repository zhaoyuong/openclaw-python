"""
Integration tests for Cron service with Gateway
"""
import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

from openclaw.gateway.types import GatewayDeps, GatewayCronState


@pytest.fixture
def mock_config():
    """Mock gateway configuration"""
    return {
        "cron": {
            "enabled": True,
            "store": "~/.openclaw/cron/jobs.json"
        },
        "channels": {}
    }


@pytest.fixture
def mock_deps():
    """Mock gateway dependencies"""
    deps = Mock(spec=GatewayDeps)
    deps.provider = Mock()
    deps.tools = []
    deps.session_manager = Mock()
    deps.get_channel_manager = Mock(return_value=None)
    return deps


class TestCronBootstrap:
    """Test cron bootstrap with gateway"""
    
    @pytest.mark.asyncio
    async def test_build_gateway_cron_service(self, mock_config, mock_deps, tmp_path):
        """Test building cron service for gateway"""
        from openclaw.gateway.cron_bootstrap import build_gateway_cron_service
        
        # Override store path to temp
        mock_config["cron"]["store"] = str(tmp_path / "jobs.json")
        
        # Mock broadcast
        broadcast_calls = []
        
        def broadcast(event: str, payload: dict, opts: dict | None = None):
            broadcast_calls.append((event, payload, opts))
        
        # Build service
        state = await build_gateway_cron_service(
            config=mock_config,
            deps=mock_deps,
            broadcast=broadcast
        )
        
        # Verify state
        assert isinstance(state, GatewayCronState)
        assert state.cron is not None
        assert state.enabled is True
        assert state.store_path.exists() or state.store_path.parent.exists()
    
    @pytest.mark.asyncio
    async def test_cron_service_disabled(self, mock_config, mock_deps, tmp_path):
        """Test cron service when disabled"""
        from openclaw.gateway.cron_bootstrap import build_gateway_cron_service
        
        # Disable cron
        mock_config["cron"]["enabled"] = False
        mock_config["cron"]["store"] = str(tmp_path / "jobs.json")
        
        def broadcast(event: str, payload: dict, opts: dict | None = None):
            pass
        
        # Build service
        state = await build_gateway_cron_service(
            config=mock_config,
            deps=mock_deps,
            broadcast=broadcast
        )
        
        # Verify disabled
        assert state.enabled is False


class TestCronDelivery:
    """Test cron job delivery to channels"""
    
    @pytest.mark.asyncio
    async def test_delivery_with_channel_manager(self):
        """Test delivery uses lazy channel manager access"""
        from openclaw.cron.isolated_agent.delivery import deliver_result
        from openclaw.cron.types import CronJob, AtSchedule, AgentTurnPayload, CronDelivery
        from datetime import datetime, timezone
        
        # Mock channel manager
        mock_channel_manager = Mock()
        mock_channel = Mock()
        mock_channel.is_running = Mock(return_value=True)
        mock_channel.send_text = AsyncMock()
        mock_channel_manager.get_channel = Mock(return_value=mock_channel)
        
        # Create job with delivery
        job = CronJob(
            id="test",
            name="Test",
            schedule=AtSchedule(timestamp=datetime.now(timezone.utc).isoformat(), type="at"),
            session_target="isolated",
            payload=AgentTurnPayload(kind="agentTurn", message="Test"),
            enabled=True,
            delivery=CronDelivery(
                channel="telegram",
                target="123456789"
            )
        )
        
        result = {
            "success": True,
            "summary": "Test summary"
        }
        
        # Deliver
        success = await deliver_result(
            job=job,
            result=result,
            get_channel_manager=lambda: mock_channel_manager
        )
        
        # Verify delivery attempted
        assert success
        mock_channel.send_text.assert_called_once()


class TestCronBroadcast:
    """Test cron event broadcasting"""
    
    def test_broadcast_function_queuing(self):
        """Test broadcast queues events before WebSocket ready"""
        from openclaw.gateway.events import GatewayBroadcaster
        
        broadcaster = GatewayBroadcaster()
        
        # Broadcast without WebSocket server
        broadcaster.broadcast("test", {"data": "value"}, {"dropIfSlow": True})
        
        # Verify queued
        assert broadcaster.get_queue_size() == 1
    
    def test_broadcast_function_flushing(self):
        """Test broadcast flushes queue when WebSocket ready"""
        from openclaw.gateway.events import GatewayBroadcaster
        
        broadcaster = GatewayBroadcaster()
        
        # Queue events
        broadcaster.broadcast("event1", {"data": 1})
        broadcaster.broadcast("event2", {"data": 2})
        
        assert broadcaster.get_queue_size() == 2
        
        # Set WebSocket server
        mock_ws_server = Mock()
        mock_ws_server.broadcast = Mock()
        
        broadcaster.set_ws_server(mock_ws_server)
        
        # Verify flushed
        assert broadcaster.get_queue_size() == 0
        assert mock_ws_server.broadcast.call_count == 2


class TestHooksCronIntegration:
    """Test hooks creating cron jobs"""
    
    @pytest.mark.asyncio
    async def test_create_cron_job_from_hook(self, tmp_path):
        """Test hook creating cron job"""
        from openclaw.hooks.cron_bridge import create_cron_job_from_hook
        from openclaw.cron import CronService
        
        # Create cron service
        service = CronService(store_path=tmp_path / "jobs.json")
        
        # Hook result
        hook_result = {
            "hook_name": "test_hook",
            "message": "Process this task",
            "agent_id": "main"
        }
        
        # Create job from hook
        job_id = await create_cron_job_from_hook(
            hook_result=hook_result,
            cron_service=service
        )
        
        # Verify job created
        assert job_id in service.jobs
        assert service.jobs[job_id].name == "hook-test_hook"
        assert service.jobs[job_id].delete_after_run is True
    
    @pytest.mark.asyncio
    async def test_delayed_cron_job(self, tmp_path):
        """Test creating delayed cron job"""
        from openclaw.hooks.cron_bridge import create_delayed_cron_job
        from openclaw.cron import CronService
        
        # Create cron service
        service = CronService(store_path=tmp_path / "jobs.json")
        
        # Create delayed job
        job_id = await create_delayed_cron_job(
            message="Reminder: Check status",
            delay_seconds=300,  # 5 minutes
            cron_service=service,
            name="delayed-reminder"
        )
        
        # Verify job created
        assert job_id in service.jobs
        assert service.jobs[job_id].schedule.kind == "at"


@pytest.mark.skip(reason="Requires full bootstrap and WebSocket server")
class TestFullIntegration:
    """Full integration tests"""
    
    @pytest.mark.asyncio
    async def test_complete_cron_flow(self):
        """Test complete flow: bootstrap → job execution → delivery → broadcast"""
        # This would test:
        # 1. Gateway bootstrap with cron
        # 2. Add cron job via CLI or API
        # 3. Job executes on schedule
        # 4. Result delivered to channel
        # 5. Events broadcast to WebSocket clients
        pass
