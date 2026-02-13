"""i18n support for Telegram channel"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from openclaw.i18n import AVAILABLE_LANGUAGES, t, set_language, get_language

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


# Store user language preferences
_user_languages: dict[int, str] = {}


def get_user_language(user_id: int) -> str:
    """Get user's preferred language"""
    return _user_languages.get(user_id, "en")


def set_user_language(user_id: int, language: str) -> bool:
    """Set user's preferred language"""
    if language not in AVAILABLE_LANGUAGES:
        return False
    
    _user_languages[user_id] = language
    logger.info(f"User {user_id} language set to: {language}")
    return True


def t_user(key: str, user_id: int, **kwargs) -> str:
    """Translate for a specific user"""
    lang = get_user_language(user_id)
    return t(key, language=lang, **kwargs)


async def handle_lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /lang command for language switching"""
    if not update.effective_user or not update.message:
        return
    
    user_id = update.effective_user.id
    current_lang = get_user_language(user_id)
    
    # Create inline keyboard with language options
    keyboard = []
    for lang_code, lang_name in AVAILABLE_LANGUAGES.items():
        # Add checkmark for current language
        if lang_code == current_lang:
            button_text = f"✓ {lang_name}"
        else:
            button_text = lang_name
        
        keyboard.append([
            InlineKeyboardButton(
                button_text,
                callback_data=f"lang:{lang_code}"
            )
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send language selection message
    message_text = t_user("commands.lang.title", user_id) + "\n\n"
    message_text += t_user("commands.lang.current", user_id) + f" {AVAILABLE_LANGUAGES[current_lang]}\n"
    message_text += t_user("commands.lang.available", user_id)
    
    await update.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def handle_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language selection callback"""
    if not update.callback_query or not update.effective_user:
        return
    
    query = update.callback_query
    await query.answer()
    
    # Extract language code from callback data
    callback_data = query.data
    if not callback_data or not callback_data.startswith("lang:"):
        return
    
    lang_code = callback_data.split(":", 1)[1]
    user_id = update.effective_user.id
    
    # Set user language
    if set_user_language(user_id, lang_code):
        # Update the message
        success_message = t_user("commands.lang.switched", user_id, language=AVAILABLE_LANGUAGES[lang_code])
        
        await query.edit_message_text(
            success_message,
            parse_mode="Markdown"
        )
    else:
        # Invalid language
        error_message = t_user("commands.lang.invalid", user_id)
        await query.edit_message_text(
            error_message,
            parse_mode="Markdown"
        )


def register_lang_handlers(application) -> None:
    """Register language-related handlers with the Telegram application"""
    from telegram.ext import CommandHandler, CallbackQueryHandler
    
    # Register /lang command
    application.add_handler(CommandHandler("lang", handle_lang_command))
    
    # Register callback query handler for language selection
    application.add_handler(CallbackQueryHandler(
        handle_lang_callback,
        pattern="^lang:"
    ))
    
    logger.info("Language handlers registered")


__all__ = [
    "get_user_language",
    "set_user_language",
    "t_user",
    "handle_lang_command",
    "handle_lang_callback",
    "register_lang_handlers",
]
