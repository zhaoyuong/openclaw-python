#!/usr/bin/env python3
"""
Simple test runner for refactored components

This doesn't require pytest and can run directly with uv.
"""

import asyncio
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))


async def test_events():
    """Test unified event system"""
    print("Testing Event System...")

    from openclaw.events import Event, EventBus, EventType, reset_event_bus

    reset_event_bus()
    bus = EventBus()

    # Test 1: Basic pub/sub
    received = []

    async def handler(event):
        received.append(event.type.value)

    bus.subscribe(EventType.AGENT_TEXT, handler)

    await bus.publish(Event(type=EventType.AGENT_TEXT, source="test", data={"text": "Hello"}))

    assert len(received) == 1, f"Expected 1 event, got {len(received)}"
    print("  ✓ Basic pub/sub works")

    # Test 2: Multiple subscribers
    count = {"a": 0, "b": 0}

    async def handler_a(event):
        count["a"] += 1

    async def handler_b(event):
        count["b"] += 1

    bus.subscribe(EventType.CHANNEL_STARTED, handler_a)
    bus.subscribe(EventType.CHANNEL_STARTED, handler_b)

    await bus.publish(Event(type=EventType.CHANNEL_STARTED, source="test", data={}))

    assert count["a"] == 1 and count["b"] == 1
    print("  ✓ Multiple subscribers work")

    # Test 3: Event serialization
    event = Event(
        type=EventType.AGENT_TEXT, source="test", session_id="sess-1", data={"text": "Test"}
    )

    d = event.to_dict()
    assert d["type"] == "agent.text"
    assert d["session_id"] == "sess-1"
    print("  ✓ Event serialization works")

    print("✅ Event System: PASSED\n")


async def test_runtime_env():
    """Test RuntimeEnv abstraction"""
    print("Testing RuntimeEnv...")

    from openclaw.runtime_env import RuntimeEnv, RuntimeEnvManager

    # Test 1: Create RuntimeEnv
    env = RuntimeEnv(
        env_id="test", model="anthropic/claude-sonnet-4", workspace=Path("./test_workspace")
    )

    assert env.env_id == "test"
    assert env.model == "anthropic/claude-sonnet-4"
    print("  ✓ RuntimeEnv creation works")

    # Test 2: RuntimeEnvManager
    manager = RuntimeEnvManager()

    prod = manager.create_env("prod", "model-1")
    dev = manager.create_env("dev", "model-2")

    assert len(manager.list_envs()) == 2
    assert manager.get_env("prod") == prod
    assert manager.get_env("dev") == dev
    print("  ✓ RuntimeEnvManager works")

    # Test 3: Default environment
    assert manager.get_default_env() == prod  # First is default

    manager.set_default("dev")
    assert manager.get_default_env() == dev
    print("  ✓ Default environment works")

    print("✅ RuntimeEnv: PASSED\n")


async def test_config():
    """Test unified configuration"""
    print("Testing Unified Config...")

    from openclaw.config.unified import ConfigBuilder, OpenClawConfig

    # Test 1: Default config
    config = OpenClawConfig()
    assert config.version == "0.6.0"
    assert config.gateway.port == 8765
    print("  ✓ Default config works")

    # Test 2: Builder pattern
    config = (
        ConfigBuilder()
        .with_agent(model="test-model")
        .with_gateway(port=9000)
        .with_channel("telegram", enabled=True)
        .build()
    )

    assert config.gateway.port == 9000
    print("  ✓ ConfigBuilder works")

    # Test 3: Get enabled channels
    enabled = config.get_enabled_channels()
    assert "telegram" in enabled
    print("  ✓ Get enabled channels works")

    print("✅ Unified Config: PASSED\n")


async def test_gateway_api():
    """Test Gateway API registry"""
    print("Testing Gateway API...")

    from openclaw.gateway.api import ConnectMethod, get_method_registry

    # Test 1: Get registry
    registry = get_method_registry()
    assert registry.get_method_count() >= 5
    print(f"  ✓ Registry has {registry.get_method_count()} methods")

    # Test 2: Get method
    method = registry.get("connect")
    assert method is not None
    assert method.name == "connect"
    print("  ✓ Method lookup works")

    # Test 3: List by category
    connection_methods = registry.list_by_category("connection")
    assert "connect" in connection_methods
    assert "ping" in connection_methods
    print(f"  ✓ Category listing works ({len(connection_methods)} connection methods)")

    # Test 4: Generate docs
    docs = registry.generate_docs()
    assert docs["total_methods"] >= 5
    assert "connect" in docs["methods"]
    print("  ✓ Documentation generation works")

    print("✅ Gateway API: PASSED\n")


async def test_channel_lifecycle():
    """Test standardized channel lifecycle"""
    print("Testing Channel Lifecycle...")

    from openclaw.channels.base import ChannelPlugin, InboundMessage

    # Create test channel
    class TestChannel(ChannelPlugin):
        def __init__(self):
            super().__init__()
            self.id = "test"
            self.label = "Test"
            self.init_called = False
            self.start_called = False
            self.ready_called = False
            self.stop_called = False
            self.destroy_called = False

        async def on_init(self):
            self.init_called = True

        async def on_start(self, config):
            self.start_called = True

        async def on_ready(self):
            self.ready_called = True

        async def on_stop(self):
            self.stop_called = True

        async def on_destroy(self):
            self.destroy_called = True

        async def send_text(self, target, text, reply_to=None):
            return "msg-123"

    channel = TestChannel()

    # Test start lifecycle
    await channel.start({"test": "config"})

    assert channel.init_called, "on_init not called"
    assert channel.start_called, "on_start not called"
    assert channel.ready_called, "on_ready not called"
    assert channel.is_running(), "Channel should be running"
    print("  ✓ Start lifecycle works")

    # Test stop lifecycle
    await channel.stop()

    assert channel.stop_called, "on_stop not called"
    assert channel.destroy_called, "on_destroy not called"
    assert not channel.is_running(), "Channel should not be running"
    print("  ✓ Stop lifecycle works")

    print("✅ Channel Lifecycle: PASSED\n")


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 Running Refactoring Tests")
    print("=" * 60)
    print()

    try:
        await test_events()
        await test_runtime_env()
        await test_config()
        await test_gateway_api()
        await test_channel_lifecycle()

        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("Summary:")
        print("  ✓ Event System: All tests passed")
        print("  ✓ RuntimeEnv: All tests passed")
        print("  ✓ Unified Config: All tests passed")
        print("  ✓ Gateway API: All tests passed")
        print("  ✓ Channel Lifecycle: All tests passed")
        print()

        return 0

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
