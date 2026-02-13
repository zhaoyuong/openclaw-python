"""Tests for Channel Plugin Normalization

Test normalize plugins for different channels.
"""

import pytest
from openclaw.channels.plugins.normalize import (
    normalize_telegram_target,
    looks_like_telegram_target,
    normalize_discord_target,
    looks_like_discord_target,
    normalize_signal_target,
    looks_like_signal_target,
)


class TestTelegramNormalize:
    """Test Telegram message normalization"""
    
    def test_normalize_username(self):
        """Test normalizing @username"""
        assert normalize_telegram_target("@username") == "telegram:@username"
    
    def test_normalize_with_prefix(self):
        """Test normalizing with telegram: prefix"""
        assert normalize_telegram_target("telegram:@username") == "telegram:@username"
        assert normalize_telegram_target("tg:@username") == "telegram:@username"
    
    def test_normalize_tme_url(self):
        """Test normalizing t.me URLs"""
        assert normalize_telegram_target("https://t.me/username") == "telegram:@username"
        assert normalize_telegram_target("t.me/username") == "telegram:@username"
    
    def test_normalize_empty(self):
        """Test normalizing empty string"""
        assert normalize_telegram_target("") is None
        assert normalize_telegram_target("  ") is None
    
    def test_looks_like_telegram(self):
        """Test Telegram ID detection"""
        assert looks_like_telegram_target("@username") is True
        assert looks_like_telegram_target("telegram:123456") is True
        assert looks_like_telegram_target("-1001234567890") is True
        assert looks_like_telegram_target("random text") is False


class TestDiscordNormalize:
    """Test Discord message normalization"""
    
    def test_normalize_snowflake(self):
        """Test normalizing Discord snowflake ID"""
        result = normalize_discord_target("123456789012345678")
        assert result == "discord:123456789012345678"
    
    def test_normalize_with_prefix(self):
        """Test normalizing with discord: prefix"""
        result = normalize_discord_target("discord:123456")
        assert result == "discord:123456"
    
    def test_looks_like_discord(self):
        """Test Discord ID detection"""
        assert looks_like_discord_target("discord:123456") is True
        assert looks_like_discord_target("12345678901234567") is True
        assert looks_like_discord_target("@username") is False


class TestSignalNormalize:
    """Test Signal message normalization"""
    
    def test_normalize_phone(self):
        """Test normalizing phone number"""
        result = normalize_signal_target("+1234567890")
        assert result == "signal:+1234567890"
    
    def test_normalize_with_prefix(self):
        """Test normalizing with signal: prefix"""
        result = normalize_signal_target("signal:+1234567890")
        assert result == "signal:+1234567890"
    
    def test_looks_like_signal(self):
        """Test Signal ID detection"""
        assert looks_like_signal_target("signal:+123456") is True
        assert looks_like_signal_target("+1234567890") is True
        assert looks_like_signal_target("random") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
