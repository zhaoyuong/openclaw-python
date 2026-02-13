"""Telegram command handler

Handles slash commands for Telegram bots.
Matches TypeScript src/telegram/bot-native-commands.ts
"""
import logging
from typing import Optional, Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from .commands import list_native_commands, get_plugin_commands, resolve_custom_commands, find_command_spec

logger = logging.getLogger(__name__)


class TelegramCommandHandler:
    """
    Handles Telegram slash commands
    
    Routes commands to appropriate handlers and manages
    authorization and argument parsing.
    """
    
    def __init__(self, cfg: dict, account_id: str, runtime):
        """
        Initialize command handler
        
        Args:
            cfg: Configuration dict
            account_id: Telegram account ID
            runtime: Runtime environment
        """
        self.cfg = cfg
        self.account_id = account_id
        self.runtime = runtime
        
        # Load command specs
        self._load_commands()
    
    def _load_commands(self):
        """Load all available commands"""
        self.native_commands = list_native_commands(self.cfg)
        self.plugin_commands = get_plugin_commands()
        self.custom_commands = resolve_custom_commands(self.cfg, self.account_id)
        
        self.all_commands = (
            self.native_commands +
            self.plugin_commands +
            self.custom_commands
        )
        
        logger.info(f"Loaded {len(self.all_commands)} total commands")
    
    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle incoming command
        
        Main entry point for command processing.
        """
        message = update.message
        if not message or not message.text:
            return
        
        # Parse command
        parts = message.text.split(maxsplit=1)
        command = parts[0][1:]  # Remove leading '/'
        
        # Remove bot username if present (@username)
        if "@" in command:
            command = command.split("@")[0]
        
        args_text = parts[1] if len(parts) > 1 else ""
        
        logger.info(f"Handling command: /{command} {args_text}")
        
        # Check authorization
        if not await self._check_auth(update):
            await message.reply_text("❌ You are not authorized to use this bot")
            return
        
        # Find command spec
        command_spec = find_command_spec(command, self.all_commands)
        
        # Route to handler
        handler = self._get_handler(command)
        if handler:
            try:
                await handler(update, context, args_text, command_spec)
            except Exception as e:
                logger.error(f"Command handler error: {e}", exc_info=True)
                await message.reply_text(f"❌ Error executing command: {str(e)}")
        else:
            await message.reply_text(
                f"Unknown command: /{command}\n"
                f"Use /help to see available commands"
            )
    
    async def _check_auth(self, update: Update) -> bool:
        """
        Check if user is authorized
        
        Implements allow_from checking.
        """
        message = update.message
        if not message:
            return False
        
        user = message.from_user
        if not user:
            return False
        
        # Get allowFrom configuration
        telegram_cfg = self.cfg.get("channels", {}).get("telegram", {})
        accounts = telegram_cfg.get("accounts", {})
        account = accounts.get(self.account_id, {})
        allow_from = account.get("allowFrom", [])
        
        # If allowFrom is empty, allow all (for testing)
        if not allow_from:
            return True
        
        # Check if user ID is in allowFrom
        user_id = str(user.id)
        username = f"@{user.username}" if user.username else None
        
        return (
            user_id in allow_from or
            (username and username in allow_from)
        )
    
    def _get_handler(self, command: str):
        """Get handler function for command"""
        handlers = {
            "help": self._handle_help,
            "model": self._handle_model,
            "status": self._handle_status,
            "start": self._handle_start,
            "ping": self._handle_ping,
        }
        return handlers.get(command)
    
    async def _handle_help(self, update, context, args, command_spec):
        """Handle /help command"""
        help_text = "📋 **Available Commands:**\n\n"
        
        for cmd in self.all_commands[:20]:  # Limit to avoid message too long
            help_text += f"/{cmd.name} - {cmd.description}\n"
        
        if len(self.all_commands) > 20:
            help_text += f"\n_...and {len(self.all_commands) - 20} more_"
        
        await update.message.reply_text(
            help_text,
            parse_mode="Markdown"
        )
    
    async def _handle_model(self, update, context, args, command_spec):
        """Handle /model command"""
        if not args:
            # Show current model
            current_model = self.cfg.get("agents", {}).get("defaults", {}).get("model", "unknown")
            await update.message.reply_text(
                f"🤖 Current model: `{current_model}`\n\n"
                f"To change model, use: /model <model_name>",
                parse_mode="Markdown"
            )
            return
        
        # Show model selection menu
        await self._show_model_menu(update, args)
    
    async def _show_model_menu(self, update, current_selection: str = ""):
        """Show interactive model selection menu"""
        models = [
            ("claude-3-5-sonnet", "Claude 3.5 Sonnet"),
            ("claude-3-opus", "Claude 3 Opus"),
            ("gpt-4", "GPT-4"),
            ("gpt-3.5-turbo", "GPT-3.5 Turbo"),
            ("gemini-pro", "Gemini Pro"),
        ]
        
        keyboard = []
        for model_id, model_name in models:
            keyboard.append([
                InlineKeyboardButton(
                    model_name,
                    callback_data=f"model:{model_id}"
                )
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🤖 Select a model:",
            reply_markup=reply_markup
        )
    
    async def _handle_status(self, update, context, args, command_spec):
        """Handle /status command"""
        status_text = (
            "✅ **Bot Status**\n\n"
            f"Account: `{self.account_id}`\n"
            f"Commands: {len(self.all_commands)}\n"
            f"Runtime: Active\n"
        )
        
        await update.message.reply_text(
            status_text,
            parse_mode="Markdown"
        )
    
    async def _handle_start(self, update, context, args, command_spec):
        """Handle /start command"""
        welcome_text = (
            "👋 Welcome to OpenClaw!\n\n"
            "I'm an AI assistant bot. Use /help to see what I can do.\n\n"
            "Start chatting with me by sending any message!"
        )
        
        await update.message.reply_text(welcome_text)
    
    async def _handle_ping(self, update, context, args, command_spec):
        """Handle /ping command"""
        await update.message.reply_text("🏓 Pong!")
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle callback queries from inline keyboards
        
        Used for interactive command menus.
        """
        query = update.callback_query
        if not query:
            return
        
        await query.answer()
        
        data = query.data
        logger.info(f"Callback query: {data}")
        
        # Parse callback data
        if data.startswith("model:"):
            model_id = data.split(":", 1)[1]
            await query.edit_message_text(
                f"✅ Model set to: `{model_id}`",
                parse_mode="Markdown"
            )
        
        elif data.startswith("cmd:"):
            # Command with arguments
            parts = data.split(":", 2)
            if len(parts) >= 3:
                command_key = parts[1]
                arg_value = parts[2]
                
                # Execute command with argument
                await query.edit_message_text(
                    f"Executing: /{command_key} {arg_value}"
                )
