"""Internationalization (i18n) support for OpenClaw"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Translation cache
_translations: dict[str, dict[str, Any]] = {}
_current_language: str = "en"

# Available languages
AVAILABLE_LANGUAGES = {
    "en": "English",
    "zh": "中文 (Chinese)",
}

DEFAULT_LANGUAGE = "en"


def load_translations(language: str) -> dict[str, Any]:
    """Load translations for a language"""
    global _translations
    
    if language in _translations:
        return _translations[language]
    
    # Find translation file
    i18n_dir = Path(__file__).parent
    translation_file = i18n_dir / f"{language}.json"
    
    if not translation_file.exists():
        logger.warning(f"Translation file not found for language: {language}")
        # Fall back to English
        if language != DEFAULT_LANGUAGE:
            return load_translations(DEFAULT_LANGUAGE)
        return {}
    
    try:
        with open(translation_file, "r", encoding="utf-8") as f:
            translations = json.load(f)
            _translations[language] = translations
            return translations
    except Exception as e:
        logger.error(f"Failed to load translations for {language}: {e}")
        return {}


def set_language(language: str) -> bool:
    """Set current language"""
    global _current_language
    
    if language not in AVAILABLE_LANGUAGES:
        logger.warning(f"Unsupported language: {language}")
        return False
    
    _current_language = language
    load_translations(language)
    return True


def get_language() -> str:
    """Get current language"""
    return _current_language


def t(key: str, language: Optional[str] = None, **kwargs) -> str:
    """Translate a key
    
    Args:
        key: Translation key (e.g., "commands.help.description")
        language: Language code (optional, uses current language if not specified)
        **kwargs: Variables to interpolate into the translation
        
    Returns:
        Translated string
    """
    lang = language or _current_language
    translations = load_translations(lang)
    
    # Navigate nested keys
    parts = key.split(".")
    value = translations
    
    for part in parts:
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            # Key not found, return the key itself
            logger.debug(f"Translation key not found: {key} (language: {lang})")
            return key
    
    # If value is still a dict, return the key
    if isinstance(value, dict):
        return key
    
    # Interpolate variables
    result = str(value)
    for k, v in kwargs.items():
        result = result.replace(f"{{{k}}}", str(v))
    
    return result


def get_all_translations(language: Optional[str] = None) -> dict[str, Any]:
    """Get all translations for a language"""
    lang = language or _current_language
    return load_translations(lang)


def detect_language_from_locale(locale: str) -> str:
    """Detect language from locale string
    
    Args:
        locale: Locale string (e.g., "en_US", "zh_CN", "en-US")
        
    Returns:
        Language code (e.g., "en", "zh")
    """
    # Normalize locale
    locale = locale.lower().replace("-", "_")
    
    # Extract language code
    if "_" in locale:
        lang_code = locale.split("_")[0]
    else:
        lang_code = locale
    
    # Check if supported
    if lang_code in AVAILABLE_LANGUAGES:
        return lang_code
    
    # Default to English
    return DEFAULT_LANGUAGE


# Initialize with default language
load_translations(DEFAULT_LANGUAGE)


__all__ = [
    "t",
    "set_language",
    "get_language",
    "get_all_translations",
    "detect_language_from_locale",
    "AVAILABLE_LANGUAGES",
    "DEFAULT_LANGUAGE",
]
