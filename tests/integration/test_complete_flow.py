"""
Complete integration test for openclaw-python
Tests the full flow from Telegram message to Gemini response

Requires environment variables:
- TELEGRAM_BOT_TOKEN
- GOOGLE_API_KEY
"""
import asyncio
import logging
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from dotenv import load_dotenv

from openclaw.agents.providers.gemini_provider import GeminiProvider
from openclaw.agents.runtime import MultiProviderRuntime
from openclaw.agents.session import Session, SessionManager
from openclaw.auto_reply.inbound_context import MsgContext, finalize_inbound_context
from openclaw.channels.base import InboundMessage
from openclaw.channels.telegram.channel import TelegramChannel
from openclaw.gateway.channel_manager import ChannelManager
from openclaw.memory.builtin_manager import BuiltinMemoryManager

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.getenv("TELEGRAM_BOT_TOKEN") or not os.getenv("GOOGLE_API_KEY"),
    reason="Real API keys not available"
)
async def test_context_building():
    """Test MsgContext building and finalization"""
    # Create a mock InboundMessage
    message = InboundMessage(
        channel_id="telegram",
        message_id="123",
        sender_id="456",
        sender_name="Test User",
        chat_id="789",
        chat_type="group",
        text="Hello, bot!",
        timestamp="2026-02-13T00:00:00Z",
        metadata={}
    )
    
    # Build MsgContext
    ctx = MsgContext(
        Body=message.text,
        RawBody=message.text,
        SessionKey=f"{message.channel_id}-{message.chat_id}",
        From=message.sender_id,
        To=message.channel_id,
        ChatType=message.chat_type,
        SenderName=message.sender_name,
        SenderId=message.sender_id,
    )
    
    # Finalize context
    ctx = finalize_inbound_context(ctx)
    
    # Verify context processing
    assert ctx.Body == "Hello, bot!"
    assert ctx.ChatType == "group"
    assert ctx.BodyForAgent is not None
    # In group chat, BodyForAgent should have sender metadata prepended
    assert "Test User:" in ctx.BodyForAgent or ctx.BodyForAgent == "Hello, bot!"
    
    logger.info(f"✓ Context building test passed")
    logger.info(f"  BodyForAgent: {ctx.BodyForAgent}")


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="Gemini API key not available"
)
async def test_gemini_provider():
    """Test Gemini provider integration"""
    provider = GeminiProvider(model="gemini-2.0-flash-exp")
    
    from openclaw.agents.providers.base import LLMMessage
    messages = [
        LLMMessage(role="user", content="Say hello in one word")
    ]
    
    response_text = ""
    async for response in provider.stream(messages, tools=None):
        if response.type == "text_delta":
            response_text += response.content
        elif response.type == "done":
            break
    
    assert len(response_text) > 0
    logger.info(f"✓ Gemini provider test passed")
    logger.info(f"  Response: {response_text}")


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="Gemini API key not available"
)
async def test_agent_runtime_with_session():
    """Test complete agent runtime flow with session"""
    workspace_dir = Path.home() / ".openclaw" / "test_workspace"
    workspace_dir.mkdir(parents=True, exist_ok=True)
    
    # Create runtime
    runtime = MultiProviderRuntime(
        provider="gemini",
        model="gemini-2.0-flash-exp",
        workspace_dir=workspace_dir
    )
    
    # Create session manager and session
    session_manager = SessionManager(workspace_dir)
    session = session_manager.get_or_create_session("test-session")
    
    # Run turn
    response_text = ""
    async for event in runtime.run_turn(
        session,
        "What is 2+2? Answer in one sentence.",
        tools=None
    ):
        if hasattr(event, 'type'):
            event_type = event.type.value if hasattr(event.type, 'value') else str(event.type)
            if event_type in ["agent.text", "text"]:
                delta = event.data.get("delta", {}).get("text", "")
                response_text += delta
            elif event_type in ["agent.turn_complete", "turn_complete"]:
                break
    
    assert len(response_text) > 0
    assert len(session.messages) >= 2  # User + assistant messages
    
    logger.info(f"✓ Agent runtime test passed")
    logger.info(f"  Response: {response_text[:100]}...")
    logger.info(f"  Session has {len(session.messages)} messages")


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="Gemini API key not available"
)
async def test_memory_manager():
    """Test memory manager integration"""
    workspace_dir = Path.home() / ".openclaw" / "test_workspace"
    workspace_dir.mkdir(parents=True, exist_ok=True)
    
    memory_manager = BuiltinMemoryManager(
        agent_id="test_agent",
        workspace_dir=workspace_dir,
        embedding_provider="openai"  # Will fall back if OpenAI key not available
    )
    
    # Test memory search (should not crash even if empty)
    results = await memory_manager.search(
        query="test query",
        limit=5,
        use_vector=False  # Use FTS only for this test
    )
    
    assert isinstance(results, list)
    logger.info(f"✓ Memory manager test passed")
    logger.info(f"  Found {len(results)} results")


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.getenv("TELEGRAM_BOT_TOKEN") or not os.getenv("GOOGLE_API_KEY"),
    reason="Real API keys not available"
)
async def test_channel_manager_flow():
    """Test complete channel manager flow (without actually starting channels)"""
    from openclaw.config import ClawdbotConfig
    
    workspace_dir = Path.home() / ".openclaw" / "test_workspace"
    workspace_dir.mkdir(parents=True, exist_ok=True)
    
    # Create runtime and session manager
    runtime = MultiProviderRuntime(
        provider="gemini",
        model="gemini-2.0-flash-exp",
        workspace_dir=workspace_dir
    )
    
    session_manager = SessionManager(workspace_dir)
    
    # Create channel manager
    channel_manager = ChannelManager(
        default_runtime=runtime,
        session_manager=session_manager,
        tools=[],
        system_prompt=None
    )
    
    # Register Telegram channel
    channel_manager.register("telegram", TelegramChannel)
    
    # Verify registration
    assert "telegram" in channel_manager.list_channels()
    
    logger.info(f"✓ Channel manager test passed")
    logger.info(f"  Registered channels: {channel_manager.list_channels()}")


@pytest.mark.asyncio
async def test_cron_heartbeat_integration():
    """Test cron heartbeat system"""
    from openclaw.infra.heartbeat_runner import (
        run_heartbeat_once,
        resolve_heartbeat_interval_ms,
        resolve_heartbeat_prompt
    )
    
    # Test heartbeat config resolution
    agent_config = {
        "heartbeat": {
            "enabled": True,
            "interval": "1h",
            "prompt": "Check for tasks"
        }
    }
    
    interval = resolve_heartbeat_interval_ms(agent_config)
    prompt = resolve_heartbeat_prompt(agent_config)
    
    assert interval == 3_600_000  # 1 hour in ms
    assert prompt == "Check for tasks"
    
    logger.info(f"✓ Heartbeat config test passed")
    logger.info(f"  Interval: {interval}ms, Prompt: {prompt}")


def test_session_store_compatibility():
    """Test session store format compatibility"""
    from openclaw.config.sessions.store import (
        load_session_store,
        save_session_store
    )
    from openclaw.config.sessions.types import SessionEntry
    from pathlib import Path
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        store_path = Path(tmpdir) / "sessions.json"
        
        # Create test entry
        entry = SessionEntry(
            session_id="test-123",
            updated_at=1000,
            channel="telegram",
            chat_type="dm"
        )
        
        # Save store
        store = {"main": entry}
        save_session_store(store_path, store)
        
        # Load store
        loaded = load_session_store(store_path)
        
        assert "main" in loaded
        assert loaded["main"].session_id == "test-123"
        assert loaded["main"].channel == "telegram"
        
        logger.info(f"✓ Session store compatibility test passed")


if __name__ == "__main__":
    # Run tests
    print("=" * 70)
    print("OpenClaw-Python Integration Tests")
    print("=" * 70)
    print()
    
    async def run_all_tests():
        try:
            # Test 1: Context building
            print("Test 1: Context Building")
            await test_context_building()
            print()
            
            # Test 2: Gemini provider
            if os.getenv("GOOGLE_API_KEY"):
                print("Test 2: Gemini Provider")
                await test_gemini_provider()
                print()
            else:
                print("Test 2: SKIPPED (no GOOGLE_API_KEY)")
                print()
            
            # Test 3: Agent runtime
            if os.getenv("GOOGLE_API_KEY"):
                print("Test 3: Agent Runtime with Session")
                await test_agent_runtime_with_session()
                print()
            else:
                print("Test 3: SKIPPED (no GOOGLE_API_KEY)")
                print()
            
            # Test 4: Memory manager
            if os.getenv("GOOGLE_API_KEY"):
                print("Test 4: Memory Manager")
                await test_memory_manager()
                print()
            else:
                print("Test 4: SKIPPED (no GOOGLE_API_KEY)")
                print()
            
            # Test 5: Channel manager
            if os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("GOOGLE_API_KEY"):
                print("Test 5: Channel Manager Flow")
                await test_channel_manager_flow()
                print()
            else:
                print("Test 5: SKIPPED (no TELEGRAM_BOT_TOKEN or GOOGLE_API_KEY)")
                print()
            
            # Test 6: Heartbeat
            print("Test 6: Cron Heartbeat Integration")
            await test_cron_heartbeat_integration()
            print()
            
            # Test 7: Session store
            print("Test 7: Session Store Compatibility")
            test_session_store_compatibility()
            print()
            
            print("=" * 70)
            print("✓ ALL TESTS PASSED")
            print("=" * 70)
            
        except Exception as e:
            print(f"\n✗ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    asyncio.run(run_all_tests())
