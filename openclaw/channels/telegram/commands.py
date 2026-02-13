"""Telegram command system

Manages command registration and routing for Telegram bots.
Matches TypeScript src/telegram/bot-native-commands.ts
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class CommandSpec:
    """Command specification"""
    name: str
    description: str
    args: List[Dict[str, Any]]
    scope: str  # "dm", "group", "all"
    native_name: Optional[str] = None


def list_native_commands(cfg: dict) -> List[CommandSpec]:
    """
    List native commands from auto-reply registry
    
    Matches TypeScript listNativeCommandSpecsForConfig()
    """
    try:
        from ...auto_reply.commands_registry_data import BUILT_IN_COMMANDS
        
        commands = []
        for cmd in BUILT_IN_COMMANDS:
            # Skip if explicitly disabled for Telegram
            if not cmd.get("telegram_enabled", True):
                continue
            
            commands.append(CommandSpec(
                name=cmd.get("native_name", cmd["key"]),
                description=cmd.get("description", ""),
                args=cmd.get("args", []),
                scope=cmd.get("scope", "all"),
                native_name=cmd.get("native_name"),
            ))
        
        logger.info(f"Loaded {len(commands)} native commands")
        return commands
    
    except ImportError:
        logger.warning("Auto-reply commands registry not found")
        # Return basic fallback commands
        return [
            CommandSpec(
                name="help",
                description="Show available commands",
                args=[],
                scope="all",
            ),
            CommandSpec(
                name="status",
                description="Show bot status",
                args=[],
                scope="all",
            ),
        ]


def get_plugin_commands() -> List[CommandSpec]:
    """
    Get plugin-provided commands
    
    Matches TypeScript getPluginCommandSpecs()
    """
    # TODO: Query plugin registry
    commands = []
    
    try:
        from ...plugins.loader import get_plugin_registry
        
        registry = get_plugin_registry()
        # Extract commands from plugins
        # for plugin in registry.get_all_plugins():
        #     if hasattr(plugin, 'commands'):
        #         commands.extend(plugin.commands)
    
    except Exception as e:
        logger.debug(f"Plugin commands not available: {e}")
    
    return commands


def resolve_custom_commands(cfg: dict, account_id: str) -> List[CommandSpec]:
    """
    Resolve custom commands from config
    
    Matches TypeScript resolveTelegramCustomCommands()
    """
    commands = []
    
    try:
        telegram_cfg = cfg.get("channels", {}).get("telegram", {})
        accounts = telegram_cfg.get("accounts", {})
        account = accounts.get(account_id, {})
        custom = account.get("customCommands", [])
        
        for cmd in custom:
            commands.append(CommandSpec(
                name=cmd["command"],
                description=cmd.get("description", "Custom command"),
                args=[],
                scope="all",
            ))
        
        logger.info(f"Loaded {len(commands)} custom commands for account {account_id}")
    
    except Exception as e:
        logger.warning(f"Failed to load custom commands: {e}")
    
    return commands


async def register_commands_with_telegram(bot, cfg: dict, account_id: str):
    """
    Register all commands with Telegram Bot API
    
    Calls bot.set_my_commands() with all available commands.
    Matches TypeScript bot.api.setMyCommands() logic.
    """
    # Gather all command types
    native = list_native_commands(cfg)
    plugins = get_plugin_commands()
    custom = resolve_custom_commands(cfg, account_id)
    
    all_commands = native + plugins + custom
    
    if not all_commands:
        logger.warning("No commands to register")
        return
    
    # Format for Telegram API
    bot_commands = [
        {"command": cmd.name, "description": cmd.description[:256]}  # Telegram limit
        for cmd in all_commands
    ]
    
    try:
        await bot.set_my_commands(bot_commands)
        logger.info(f"✅ Registered {len(bot_commands)} commands with Telegram")
    
    except Exception as e:
        logger.error(f"Failed to register commands: {e}")


def find_command_spec(command_name: str, commands: List[CommandSpec]) -> Optional[CommandSpec]:
    """Find command spec by name"""
    for cmd in commands:
        if cmd.name == command_name or cmd.native_name == command_name:
            return cmd
    return None
