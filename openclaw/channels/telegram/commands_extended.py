"""Extended Telegram commands - aligned with TypeScript openclaw"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

if TYPE_CHECKING:
    from telegram.ext import Application

from openclaw.i18n import t
from .i18n_support import t_user

logger = logging.getLogger(__name__)


async def handle_commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show paginated command list - /commands"""
    if not update.effective_user or not update.message:
        return
    
    user_id = update.effective_user.id
    
    # Get all commands (this would come from registry)
    commands = [
        ("/start", t_user("commands.start.description", user_id)),
        ("/help", t_user("commands.help.description", user_id)),
        ("/new", t_user("commands.new.description", user_id)),
        ("/status", t_user("commands.status.description", user_id)),
        ("/model", t_user("commands.model.description", user_id)),
        ("/lang", t_user("commands.lang.description", user_id)),
        ("/commands", t_user("commands.commands.description", user_id)),
        ("/context", t_user("commands.context.description", user_id)),
        ("/compact", t_user("commands.compact.description", user_id)),
        ("/stop", t_user("commands.stop.description", user_id)),
        ("/think", t_user("commands.think.description", user_id)),
        ("/verbose", t_user("commands.verbose.description", user_id)),
        ("/reasoning", t_user("commands.reasoning.description", user_id)),
        ("/usage", t_user("commands.usage.description", user_id)),
        ("/config", t_user("commands.config.description", user_id)),
        ("/debug", t_user("commands.debug.description", user_id)),
    ]
    
    # Pagination
    page = int(context.args[0]) if context.args and context.args[0].isdigit() else 0
    per_page = 8
    total_pages = (len(commands) + per_page - 1) // per_page
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, len(commands))
    page_commands = commands[start_idx:end_idx]
    
    # Build message
    title = t_user("commands.commands.title", user_id, page=page+1, total=total_pages)
    message_text = f"{title}\n\n"
    
    for cmd, desc in page_commands:
        message_text += f"{cmd} - {desc}\n"
    
    # Build navigation keyboard
    keyboard = []
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(
            t_user("commands.commands.prev", user_id),
            callback_data=f"commands_page:{page-1}"
        ))
    if end_idx < len(commands):
        nav_row.append(InlineKeyboardButton(
            t_user("commands.commands.next", user_id),
            callback_data=f"commands_page:{page+1}"
        ))
    
    if nav_row:
        keyboard.append(nav_row)
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    
    await update.message.reply_text(
        message_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def handle_context_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Explain context management - /context"""
    if not update.effective_user or not update.message:
        return
    
    user_id = update.effective_user.id
    
    message_text = t_user("commands.context.title", user_id) + "\n\n"
    message_text += t_user("commands.context.explanation", user_id)
    
    await update.message.reply_text(
        message_text,
        parse_mode="Markdown"
    )


async def handle_compact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Compact session context - /compact"""
    if not update.effective_user or not update.message:
        return
    
    user_id = update.effective_user.id
    
    # Send starting message
    await update.message.reply_text(
        t_user("commands.compact.started", user_id),
        parse_mode="Markdown"
    )
    
    # TODO: Actually compact session via runtime
    # For now, mock response
    await update.message.reply_text(
        t_user("commands.compact.success", user_id, tokens="1500"),
        parse_mode="Markdown"
    )


async def handle_stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop current agent run - /stop"""
    if not update.effective_user or not update.message:
        return
    
    user_id = update.effective_user.id
    
    # TODO: Actually stop via runtime
    # For now, send success message
    await update.message.reply_text(
        t_user("commands.stop.success", user_id),
        parse_mode="Markdown"
    )


async def handle_verbose_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Toggle verbose mode - /verbose"""
    if not update.effective_user or not update.message:
        return
    
    user_id = update.effective_user.id
    
    # Parse argument
    arg = context.args[0].lower() if context.args else "toggle"
    
    if arg in ["on", "true", "1"]:
        message = t_user("commands.verbose.enabled", user_id)
        # TODO: Actually set verbose mode
    elif arg in ["off", "false", "0"]:
        message = t_user("commands.verbose.disabled", user_id)
        # TODO: Actually disable verbose mode
    else:
        # Toggle
        message = t_user("commands.verbose.enabled", user_id)
    
    await update.message.reply_text(message, parse_mode="Markdown")


async def handle_reasoning_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Toggle reasoning visibility - /reasoning"""
    if not update.effective_user or not update.message:
        return
    
    user_id = update.effective_user.id
    
    arg = context.args[0].lower() if context.args else "on"
    
    if arg == "stream":
        message = t_user("commands.reasoning.stream", user_id)
    elif arg in ["on", "true"]:
        message = t_user("commands.reasoning.enabled", user_id)
    else:
        message = t_user("commands.reasoning.disabled", user_id)
    
    await update.message.reply_text(message, parse_mode="Markdown")


async def handle_usage_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show usage statistics - /usage"""
    if not update.effective_user or not update.message:
        return
    
    user_id = update.effective_user.id
    
    arg = context.args[0].lower() if context.args else "full"
    
    if arg == "off":
        message = t_user("commands.usage.mode_set", user_id, mode="off")
    elif arg == "tokens":
        message = t_user("commands.usage.mode_set", user_id, mode="tokens")
    elif arg == "cost":
        message = t_user("commands.usage.mode_set", user_id, mode="cost")
    else:
        # Show current usage
        title = t_user("commands.usage.title", user_id)
        tokens_label = t_user("commands.usage.tokens", user_id)
        cost_label = t_user("commands.usage.cost", user_id)
        
        message = f"{title}\n\n"
        message += f"{tokens_label} 15,234\n"
        message += f"{cost_label} $0.45"
    
    await update.message.reply_text(message, parse_mode="Markdown")


async def handle_callback_pagination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle commands pagination callback"""
    if not update.callback_query or not update.effective_user:
        return
    
    query = update.callback_query
    await query.answer()
    
    if not query.data or not query.data.startswith("commands_page:"):
        return
    
    page = int(query.data.split(":", 1)[1])
    user_id = update.effective_user.id
    
    # Get commands (same as handle_commands_command)
    commands = [
        ("/start", t_user("commands.start.description", user_id)),
        ("/help", t_user("commands.help.description", user_id)),
        ("/new", t_user("commands.new.description", user_id)),
        ("/status", t_user("commands.status.description", user_id)),
        ("/model", t_user("commands.model.description", user_id)),
        ("/lang", t_user("commands.lang.description", user_id)),
        ("/commands", t_user("commands.commands.description", user_id)),
        ("/context", t_user("commands.context.description", user_id)),
        ("/compact", t_user("commands.compact.description", user_id)),
        ("/stop", t_user("commands.stop.description", user_id)),
        ("/think", t_user("commands.think.description", user_id)),
        ("/verbose", t_user("commands.verbose.description", user_id)),
        ("/reasoning", t_user("commands.reasoning.description", user_id)),
        ("/usage", t_user("commands.usage.description", user_id)),
        ("/config", t_user("commands.config.description", user_id)),
        ("/debug", t_user("commands.debug.description", user_id)),
    ]
    
    per_page = 8
    total_pages = (len(commands) + per_page - 1) // per_page
    
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, len(commands))
    page_commands = commands[start_idx:end_idx]
    
    # Build message
    title = t_user("commands.commands.title", user_id, page=page+1, total=total_pages)
    message_text = f"{title}\n\n"
    
    for cmd, desc in page_commands:
        message_text += f"{cmd} - {desc}\n"
    
    # Build navigation keyboard
    keyboard = []
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(
            t_user("commands.commands.prev", user_id),
            callback_data=f"commands_page:{page-1}"
        ))
    if end_idx < len(commands):
        nav_row.append(InlineKeyboardButton(
            t_user("commands.commands.next", user_id),
            callback_data=f"commands_page:{page+1}"
        ))
    
    if nav_row:
        keyboard.append(nav_row)
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    
    await query.edit_message_text(
        message_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


def register_extended_commands(application: Application) -> None:
    """Register all extended commands"""
    
    # Register command handlers
    application.add_handler(CommandHandler("commands", handle_commands_command))
    application.add_handler(CommandHandler("context", handle_context_command))
    application.add_handler(CommandHandler("compact", handle_compact_command))
    application.add_handler(CommandHandler("stop", handle_stop_command))
    application.add_handler(CommandHandler("verbose", handle_verbose_command))
    application.add_handler(CommandHandler("reasoning", handle_reasoning_command))
    application.add_handler(CommandHandler("usage", handle_usage_command))
    
    # Register callback handlers
    application.add_handler(CallbackQueryHandler(
        handle_callback_pagination,
        pattern="^commands_page:"
    ))
    
    logger.info("Extended Telegram commands registered")


__all__ = [
    "register_extended_commands",
    "handle_commands_command",
    "handle_context_command",
    "handle_compact_command",
    "handle_stop_command",
    "handle_verbose_command",
    "handle_reasoning_command",
    "handle_usage_command",
]
