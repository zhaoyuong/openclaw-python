"""Non-interactive onboarding mode"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from openclaw.config.schema import ClawdbotConfig, GatewayConfig, AgentConfig
from openclaw.config.loader import save_config

logger = logging.getLogger(__name__)


async def run_non_interactive_onboarding(
    provider: str = "gemini",
    api_key: Optional[str] = None,
    gateway_port: int = 18789,
    gateway_bind: str = "loopback",
    gateway_auth: str = "token",
    gateway_token: Optional[str] = None,
    telegram_token: Optional[str] = None,
    workspace: Optional[Path] = None,
    accept_risk: bool = False
) -> dict:
    """Run non-interactive onboarding with CLI flags
    
    Args:
        provider: LLM provider (anthropic, openai, gemini, ollama)
        api_key: API key for provider
        gateway_port: Gateway port (default: 18789)
        gateway_bind: Gateway bind mode
        gateway_auth: Auth mode (token, password, none)
        gateway_token: Gateway token
        telegram_token: Telegram bot token
        workspace: Workspace directory
        accept_risk: Must be True for non-interactive mode
        
    Returns:
        Dict with setup result
    """
    if not accept_risk:
        logger.error("Non-interactive mode requires --accept-risk flag")
        return {
            "success": False,
            "error": "Risk not accepted. Use --accept-risk flag."
        }
    
    print("🤖 OpenClaw Non-Interactive Onboarding")
    print("=" * 60)
    
    # Create config
    config = ClawdbotConfig()
    
    # Configure agent
    if provider == "anthropic":
        model = "anthropic/claude-sonnet-4"
    elif provider == "openai":
        model = "openai/gpt-4"
    elif provider == "gemini":
        model = "google/gemini-2.0-flash-exp"
    elif provider == "ollama":
        model = "ollama/llama3"
    else:
        model = f"{provider}/default"
    
    config.agent = AgentConfig(model=model)
    
    # Configure gateway
    config.gateway = GatewayConfig(
        port=gateway_port,
        bind=gateway_bind,
        mode="local"
    )
    
    # Configure gateway auth
    if gateway_auth == "token":
        if not gateway_token:
            # Generate random token
            import secrets
            gateway_token = secrets.token_hex(24)
        config.gateway.auth = {"mode": "token", "token": gateway_token}
    elif gateway_auth == "password":
        config.gateway.auth = {"mode": "password"}
    
    # Configure channels
    if telegram_token:
        config.channels = {
            "telegram": {
                "enabled": True,
                "botToken": telegram_token,
                "dmPolicy": "pairing"
            }
        }
    
    # Save config
    try:
        save_config(config)
        print("✅ Configuration saved")
    except Exception as e:
        logger.error(f"Failed to save config: {e}")
        return {"success": False, "error": str(e)}
    
    # Mark onboarding complete
    if workspace:
        marker = workspace / ".openclaw" / "onboarding-complete"
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text('{"completed_at": "' + str(Path.ctime(marker)) + '"}')
    
    print("\n✅ Non-interactive onboarding complete!")
    print("\n🚀 Next steps:")
    print("   openclaw start              # Start gateway and channels")
    print("   openclaw tui                # Launch Terminal UI")
    print(f"   http://localhost:{gateway_port}/  # Open Web UI")
    
    return {
        "success": True,
        "config": {
            "provider": provider,
            "gateway_port": gateway_port,
            "gateway_bind": gateway_bind,
            "channels_configured": bool(telegram_token)
        }
    }


__all__ = ["run_non_interactive_onboarding"]
