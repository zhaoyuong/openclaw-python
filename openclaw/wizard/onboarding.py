"""Onboarding wizard

First-run onboarding experience for new users.
Matches TypeScript openclaw/src/wizard/onboarding.ts
"""
from __future__ import annotations

import json
import logging
import secrets
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..config.loader import load_config, save_config
from ..config.schema import ClawdbotConfig, AgentConfig, GatewayConfig, ChannelsConfig
from .auth import configure_auth, check_env_api_key
from .config import configure_telegram_enhanced, configure_discord_enhanced, configure_agent

logger = logging.getLogger(__name__)


async def run_onboarding_wizard(config: Optional[dict] = None, workspace_dir: Optional[Path] = None) -> dict:
    """
    Run onboarding wizard
    
    Guides new users through initial setup:
    - Risk confirmation
    - Mode selection (QuickStart/Advanced)
    - API key configuration
    - Model selection
    - Gateway configuration
    - Channel setup
    
    Args:
        config: Existing Gateway configuration (optional)
        workspace_dir: Workspace directory (optional)
        
    Returns:
        Dict with wizard results
    """
    logger.info("Starting onboarding wizard")
    
    print("\n" + "=" * 80)
    print("🚀 Welcome to OpenClaw Onboarding!")
    print("=" * 80)
    print("\nThis wizard will help you set up OpenClaw for the first time.")
    print("You can exit anytime with Ctrl+C")
    
    # Step 1: Risk confirmation
    if not _confirm_risks():
        return {"completed": False, "skipped": True, "reason": "User declined"}
    
    # Step 2: Mode selection
    mode = _select_mode()
    
    # Step 3: Load or create config
    try:
        existing_config = load_config()
        print("\n✓ Found existing configuration")
        
        if mode == "quickstart":
            print("QuickStart mode: Using existing configuration as base")
            claw_config = existing_config
        else:
            action = _prompt_config_action()
            if action == "reset":
                print("Creating fresh configuration...")
                claw_config = ClawdbotConfig()
            elif action == "modify":
                print("Modifying existing configuration...")
                claw_config = existing_config
            else:  # keep
                print("Keeping existing configuration...")
                return {"completed": True, "skipped": False, "kept_existing": True}
    except Exception as e:
        logger.info(f"No existing config: {e}")
        print("\nCreating new configuration...")
        claw_config = ClawdbotConfig()
    
    # Step 4: Provider configuration
    provider_config = await _configure_provider(mode)
    if provider_config:
        # Update agent config with provider
        if not claw_config.agent:
            claw_config.agent = AgentConfig()
        claw_config.agent.model = provider_config.get("model", "claude-sonnet-4")
        # Store auth in environment variables (handled by configure_auth)
    
    # Step 5: Agent configuration
    if mode == "advanced":
        agent_config = await _configure_agent_settings()
        if agent_config:
            if not claw_config.agent:
                claw_config.agent = AgentConfig()
            claw_config.agent.workspace = agent_config.get("workspace", "./workspace")
    
    # Step 6: Gateway configuration
    gateway_config = await _configure_gateway(mode)
    if gateway_config:
        if not claw_config.gateway:
            claw_config.gateway = GatewayConfig()
        claw_config.gateway.port = gateway_config.get("port", 18789)
        claw_config.gateway.bind = gateway_config.get("bind", "loopback")
        if "auth_token" in gateway_config:
            claw_config.gateway.auth_token = gateway_config["auth_token"]
        if "auth_password" in gateway_config:
            claw_config.gateway.auth_password = gateway_config["auth_password"]
    
    # Step 7: Channels configuration
    channels_config = await _configure_channels(mode)
    if channels_config:
        if not claw_config.channels:
            claw_config.channels = ChannelsConfig()
        if "telegram" in channels_config:
            claw_config.channels.telegram = channels_config["telegram"]
        if "discord" in channels_config:
            claw_config.channels.discord = channels_config["discord"]
    
    # Step 8: Save configuration
    print("\n" + "-" * 80)
    print("Configuration Summary:")
    print("-" * 80)
    print(f"Provider: {provider_config.get('provider', 'Not configured')}")
    print(f"Model: {claw_config.agent.model if claw_config.agent else 'Default'}")
    print(f"Gateway Port: {claw_config.gateway.port if claw_config.gateway else 18789}")
    print(f"Gateway Bind: {claw_config.gateway.bind if claw_config.gateway else 'loopback'}")
    if channels_config:
        if "telegram" in channels_config:
            print("✓ Telegram configured")
        if "discord" in channels_config:
            print("✓ Discord configured")
    print("-" * 80)
    
    save_choice = input("\nSave this configuration? [Y/n]: ").strip().lower()
    if save_choice == "n":
        print("Configuration not saved. Exiting...")
        return {"completed": False, "skipped": True, "reason": "User chose not to save"}
    
    try:
        save_config(claw_config)
        print("✓ Configuration saved!")
    except Exception as e:
        logger.error(f"Failed to save config: {e}")
        print(f"✗ Error saving configuration: {e}")
        return {"completed": False, "error": str(e)}
    
    # Step 9: Mark onboarding complete
    if workspace_dir:
        mark_onboarding_complete(workspace_dir)
    else:
        mark_onboarding_complete(Path.home() / ".openclaw")
    
    # Step 10: Display next steps
    print("\n" + "=" * 80)
    print("🎉 Onboarding Complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Start the Gateway:")
    print("     $ openclaw gateway start")
    print("\n  2. Connect a channel (if configured):")
    if "telegram" in (channels_config or {}):
        print("     - Open Telegram and message your bot")
    if "discord" in (channels_config or {}):
        print("     - Invite your Discord bot to a server")
    print("\n  3. Or use the CLI:")
    print("     $ openclaw chat \"Hello!\"")
    print("\n" + "=" * 80 + "\n")
    
    logger.info("Onboarding wizard complete")
    
    return {
        "completed": True,
        "skipped": False,
        "mode": mode,
        "provider": provider_config.get("provider") if provider_config else None,
    }


def _confirm_risks() -> bool:
    """Confirm user understands risks"""
    print("\n" + "-" * 80)
    print("⚠️  Important: Security & Risks")
    print("-" * 80)
    print("""
OpenClaw is an AI agent that can:
  • Execute commands on your system
  • Read and modify files
  • Make network requests
  • Use your API keys

Please ensure:
  ✓ You trust the codebase
  ✓ You understand the permissions granted
  ✓ You review agent actions carefully
  ✓ You keep your API keys secure

This is experimental software. Use at your own risk.
""")
    
    confirm = input("Do you understand and accept these risks? [y/N]: ").strip().lower()
    return confirm == "y"


def _select_mode() -> str:
    """Select onboarding mode"""
    print("\n" + "-" * 80)
    print("Onboarding Mode")
    print("-" * 80)
    print("\nChoose your setup mode:")
    print("  1. QuickStart  - Fast setup with recommended settings (5 min)")
    print("  2. Advanced    - Customize everything (15 min)")
    
    choice = input("\nSelect mode [1]: ").strip()
    
    if choice == "2":
        print("\n✓ Advanced mode selected")
        return "advanced"
    else:
        print("\n✓ QuickStart mode selected")
        return "quickstart"


def _prompt_config_action() -> str:
    """Prompt for action on existing config"""
    print("\nWhat would you like to do with existing configuration?")
    print("  1. Keep    - Use existing configuration")
    print("  2. Modify  - Update specific settings")
    print("  3. Reset   - Start fresh")
    
    choice = input("\nSelect action [2]: ").strip()
    
    if choice == "1":
        return "keep"
    elif choice == "3":
        return "reset"
    else:
        return "modify"


async def _configure_provider(mode: str) -> Optional[dict]:
    """Configure LLM provider"""
    print("\n" + "-" * 80)
    print("Provider Configuration")
    print("-" * 80)
    
    if mode == "quickstart":
        # QuickStart: Check environment variables first
        providers = ["anthropic", "openai", "gemini"]
        for provider in providers:
            if check_env_api_key(provider):
                print(f"\n✓ Found {provider.title()} API key in environment")
                use_it = input(f"Use {provider.title()}? [Y/n]: ").strip().lower()
                if use_it != "n":
                    return {
                        "provider": provider,
                        "model": "claude-sonnet-4" if provider == "anthropic" else f"{provider}-default",
                    }
    
    # Prompt for provider
    print("\nSelect your LLM provider:")
    print("  1. Anthropic (Claude)  - Recommended")
    print("  2. OpenAI (GPT-4)")
    print("  3. Google (Gemini)")
    print("  4. Ollama (Local)")
    
    choice = input("\nSelect provider [1]: ").strip()
    
    provider_map = {
        "1": "anthropic",
        "2": "openai",
        "3": "gemini",
        "4": "ollama",
    }
    provider = provider_map.get(choice, "anthropic")
    
    # Configure auth (skips if Ollama)
    if provider != "ollama":
        try:
            auth_result = configure_auth(provider)
            print(f"\n✓ {provider.title()} configured")
        except Exception as e:
            print(f"\n✗ Failed to configure {provider}: {e}")
            return None
    
    # Select model
    model_map = {
        "anthropic": "claude-sonnet-4",
        "openai": "gpt-4",
        "gemini": "gemini-pro",
        "ollama": "llama2",
    }
    model = model_map.get(provider, "claude-sonnet-4")
    
    return {"provider": provider, "model": model}


async def _configure_agent_settings() -> Optional[dict]:
    """Configure agent settings"""
    print("\n" + "-" * 80)
    print("Agent Settings")
    print("-" * 80)
    
    return await configure_agent()


async def _configure_gateway(mode: str) -> Optional[dict]:
    """Configure Gateway settings"""
    print("\n" + "-" * 80)
    print("Gateway Configuration")
    print("-" * 80)
    
    config = {}
    
    # Port
    if mode == "quickstart":
        config["port"] = 18789
        print(f"\nUsing default port: {config['port']}")
    else:
        port_input = input("\nGateway port [18789]: ").strip()
        config["port"] = int(port_input) if port_input else 18789
    
    # Bind mode
    if mode == "quickstart":
        config["bind"] = "loopback"
        print("Using loopback mode (local access only)")
    else:
        print("\nBind mode:")
        print("  1. loopback  - Local access only (recommended)")
        print("  2. lan       - LAN access")
        print("  3. auto      - Auto-detect")
        
        bind_choice = input("\nSelect bind mode [1]: ").strip()
        bind_map = {"1": "loopback", "2": "lan", "3": "auto"}
        config["bind"] = bind_map.get(bind_choice, "loopback")
    
    # Authentication
    if mode == "quickstart":
        # Generate token
        config["auth_token"] = secrets.token_urlsafe(32)
        print("\n✓ Generated authentication token")
    else:
        print("\nAuthentication:")
        print("  1. Token     - Random token (recommended)")
        print("  2. Password  - Custom password")
        print("  3. None      - No authentication (local only)")
        
        auth_choice = input("\nSelect auth mode [1]: ").strip()
        
        if auth_choice == "2":
            password = input("Enter password: ").strip()
            if password:
                config["auth_password"] = password
        elif auth_choice == "3":
            print("⚠️  Warning: No authentication - use only for local development")
        else:
            config["auth_token"] = secrets.token_urlsafe(32)
            print("✓ Generated authentication token")
    
    return config


async def _configure_channels(mode: str) -> Optional[dict]:
    """Configure channels"""
    print("\n" + "-" * 80)
    print("Channels Configuration")
    print("-" * 80)
    
    if mode == "quickstart":
        setup_channels = input("\nConfigure channels now? [y/N]: ").strip().lower()
        if setup_channels != "y":
            print("Skipping channels. You can configure them later with:")
            print("  $ openclaw configure channels")
            return None
    
    channels_config = {}
    
    print("\nWhich channels would you like to configure?")
    print("  1. Telegram")
    print("  2. Discord")
    print("  3. Skip")
    
    choice = input("\nSelect channel [3]: ").strip()
    
    if choice == "1":
        print("\n" + "~" * 60)
        print("Configuring Telegram")
        print("~" * 60)
        telegram_config = configure_telegram_enhanced()
        if telegram_config:
            channels_config["telegram"] = telegram_config
    elif choice == "2":
        print("\n" + "~" * 60)
        print("Configuring Discord")
        print("~" * 60)
        discord_config = configure_discord_enhanced()
        if discord_config:
            channels_config["discord"] = discord_config
    
    return channels_config if channels_config else None


def mark_onboarding_complete(workspace_dir: Path) -> None:
    """Mark onboarding as complete"""
    marker_file = workspace_dir / ".openclaw" / "onboarding-complete"
    marker_file.parent.mkdir(parents=True, exist_ok=True)
    
    marker_data = {
        "completed_at": datetime.now().isoformat(),
        "version": "0.6.0",
    }
    
    marker_file.write_text(json.dumps(marker_data, indent=2))
    logger.info(f"Onboarding marked complete: {marker_file}")


def is_first_run(workspace_dir: Path) -> bool:
    """
    Check if this is the first run
    
    Args:
        workspace_dir: Workspace directory
        
    Returns:
        True if first run
    """
    marker_file = workspace_dir / ".openclaw" / "onboarding-complete"
    return not marker_file.exists()
