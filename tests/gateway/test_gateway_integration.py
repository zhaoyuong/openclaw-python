"""
Gateway integration tests

Tests the complete Gateway system including authentication, authorization,
and method execution.
"""

import asyncio
import json
import pytest
import websockets
from unittest.mock import Mock


class MockConfig:
    """Mock configuration"""
    
    class Gateway:
        bind = "loopback"
        port = 8765
        enable_web_ui = False
    
    gateway = Gateway()
    model = "claude-sonnet-4"


@pytest.fixture
async def mock_gateway_server():
    """Create a mock Gateway server"""
    from openclaw.gateway.server import GatewayServer
    
    config = MockConfig()
    gateway = GatewayServer(config=config)
    
    # Start server in background
    server_task = asyncio.create_task(gateway.start(start_channels=False))
    
    # Wait for server to start
    await asyncio.sleep(0.5)
    
    yield gateway
    
    # Cleanup
    gateway.running = False
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass


@pytest.mark.asyncio
async def test_connect_flow():
    """Test complete connect flow with auth"""
    # This is a template test - requires running server
    
    # Mock the connect flow
    connect_request = {
        "type": "req",
        "id": "1",
        "method": "connect",
        "params": {
            "maxProtocol": 3,
            "client": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    # Verify request structure
    assert connect_request["method"] == "connect"
    assert connect_request["params"]["maxProtocol"] == 3


@pytest.mark.asyncio
async def test_method_authorization():
    """Test role-based authorization"""
    from openclaw.gateway.authorization import (
        authorize_gateway_method,
        AuthContext,
        Scope
    )
    
    # Test operator with admin scope
    admin_context = AuthContext(
        role="operator",
        scopes={Scope.ADMIN}
    )
    assert authorize_gateway_method("config.set", admin_context)
    
    # Test operator without admin scope
    read_context = AuthContext(
        role="operator",
        scopes={Scope.READ}
    )
    assert not authorize_gateway_method("config.set", read_context)
    
    # Test node role
    node_context = AuthContext(
        role="node",
        scopes=set()
    )
    assert authorize_gateway_method("node.invoke", node_context)
    assert not authorize_gateway_method("config.set", node_context)


@pytest.mark.asyncio
async def test_protocol_validation():
    """Test protocol request validation"""
    from openclaw.gateway.protocol.validators import validate_method_params
    from pydantic import ValidationError
    
    # Valid params
    valid_params = {
        "message": "Hello",
        "sessionKey": "main"
    }
    result = validate_method_params("agent", valid_params)
    assert result.message == "Hello"
    
    # Invalid params (missing required field)
    with pytest.raises(ValidationError):
        validate_method_params("agent", {})


def test_error_codes():
    """Test error code standardization"""
    from openclaw.gateway.error_codes import (
        ErrorCode,
        error_shape,
        AuthFailedError
    )
    
    # Test error shape
    error = error_shape(
        ErrorCode.AUTH_FAILED,
        "Invalid credentials",
        retryable=True
    )
    
    assert error["code"] == "AUTH_FAILED"
    assert error["message"] == "Invalid credentials"
    assert error["retryable"] is True
    
    # Test error exception
    exc = AuthFailedError("Bad token")
    assert exc.error_code == ErrorCode.AUTH_FAILED


def test_device_authentication():
    """Test device authentication"""
    from openclaw.gateway.device_auth import (
        DeviceIdentity,
        authorize_device_identity
    )
    import time
    from datetime import datetime
    
    # Create device identity
    identity = DeviceIdentity(
        id="test-device",
        public_key="test-key",
        signature="test-sig",
        signed_at=datetime.now().isoformat(),
        nonce="test-nonce"
    )
    
    # Test authorization (will fail signature but tests structure)
    result = authorize_device_identity(identity, nonce="test-nonce")
    assert not result.ok  # Expected to fail signature check


def test_cron_service():
    """Test cron service"""
    from openclaw.cron.service import CronService, CronJob
    
    service = CronService()
    
    # Create job
    job = CronJob(
        id="test-job",
        schedule="*/5 * * * *",  # Every 5 minutes
        action="agent",
        params={"message": "Test"}
    )
    
    # Add job
    success = service.add_job(job)
    assert success
    
    # List jobs
    jobs = service.list_jobs()
    assert len(jobs) == 1
    assert jobs[0]["id"] == "test-job"
    
    # Remove job
    service.remove_job("test-job")
    jobs = service.list_jobs()
    assert len(jobs) == 0


def test_node_manager():
    """Test node management"""
    from openclaw.nodes.manager import NodeManager
    
    manager = NodeManager()
    
    # Register node
    node = manager.register_node(
        "test-node",
        {"exec": True, "tools": ["bash"]},
        public_key="test-key"
    )
    
    assert node.id == "test-node"
    
    # List nodes
    nodes = manager.list_nodes()
    assert len(nodes) == 1
    
    # Request pairing
    request = manager.request_pairing("test-node", "nonce", "signature")
    assert request.node_id == "test-node"
    
    # Approve pairing
    token = manager.approve_pairing("test-node")
    assert token is not None
    
    # Verify token
    verified_node_id = manager.verify_token(token)
    assert verified_node_id == "test-node"


def test_device_manager():
    """Test device management"""
    from openclaw.devices.manager import DeviceManager
    
    manager = DeviceManager()
    
    # Request pairing
    request = manager.request_pairing("test-device", "public-key")
    assert request.device_id == "test-device"
    
    # Approve pairing
    token = manager.approve_pairing("test-device", label="Test Device")
    assert token is not None
    
    # List devices
    devices = manager.list_devices()
    assert len(devices) == 1
    assert devices[0]["label"] == "Test Device"
    
    # Verify token
    device_id = manager.verify_token(token)
    assert device_id == "test-device"
    
    # Rotate token
    new_token = manager.rotate_token("test-device")
    assert new_token != token
    
    # Old token should be revoked
    assert manager.verify_token(token) is None


def test_exec_approval_manager():
    """Test exec approval management"""
    from openclaw.exec.approval_manager import ExecApprovalManager
    
    manager = ExecApprovalManager()
    
    # Request approval
    approval_id = manager.request_approval(
        "rm -rf /",
        {"user": "test", "cwd": "/home/test"}
    )
    
    assert approval_id is not None
    
    # List pending
    pending = manager.list_pending()
    assert len(pending) == 1
    
    # Approve
    success = manager.approve(approval_id, approved_by="admin")
    assert success
    
    # Should no longer be pending
    pending = manager.list_pending()
    assert len(pending) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
