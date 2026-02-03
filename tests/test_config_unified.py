"""Unit tests for unified configuration system"""

import pytest
import json
from pathlib import Path
from openclaw.config.unified import (
    OpenClawConfig,
    ConfigBuilder,
    AgentConfig,
    GatewayConfig,
    ChannelsConfig,
    SingleChannelConfig,
)


class TestOpenClawConfig:
    """Test OpenClawConfig"""
    
    def test_create_default_config(self):
        """Test creating default config"""
        config = OpenClawConfig()
        
        assert config.version == "0.6.0"
        assert config.agent is not None
        assert config.gateway is not None
        assert config.channels is not None
    
    def test_create_with_params(self):
        """Test creating config with parameters"""
        config = OpenClawConfig(
            agent={"model": "anthropic/claude-opus-4"},
            gateway={"port": 9000}
        )
        
        assert config.gateway.port == 9000
    
    def test_from_dict(self):
        """Test creating from dictionary"""
        data = {
            "agent": {"model": "anthropic/claude-sonnet-4"},
            "gateway": {"port": 8765},
            "channels": {
                "telegram": {"enabled": True}
            }
        }
        
        config = OpenClawConfig.from_dict(data)
        assert config.gateway.port == 8765
        assert config.channels.telegram.enabled is True
    
    def test_to_dict(self):
        """Test serialization"""
        config = OpenClawConfig(
            gateway={"port": 8765}
        )
        
        d = config.to_dict()
        assert isinstance(d, dict)
        assert d["gateway"]["port"] == 8765
    
    def test_get_enabled_channels(self):
        """Test getting enabled channels"""
        config = OpenClawConfig(
            channels={
                "telegram": {"enabled": True},
                "discord": {"enabled": False},
                "slack": {"enabled": True}
            }
        )
        
        enabled = config.get_enabled_channels()
        assert "telegram" in enabled
        assert "slack" in enabled
        assert "discord" not in enabled


class TestConfigBuilder:
    """Test ConfigBuilder"""
    
    def test_builder_pattern(self):
        """Test fluent builder API"""
        config = (ConfigBuilder()
            .with_agent(model="anthropic/claude-opus-4")
            .with_gateway(port=8765)
            .build())
        
        assert config.gateway.port == 8765
    
    def test_builder_with_channel(self):
        """Test adding channels via builder"""
        config = (ConfigBuilder()
            .with_channel("telegram", enabled=True, config={"bot_token": "test"})
            .with_channel("discord", enabled=False)
            .build())
        
        assert config.channels.telegram.enabled is True
        assert config.channels.discord.enabled is False
    
    def test_builder_chaining(self):
        """Test method chaining"""
        builder = ConfigBuilder()
        
        result = builder.with_agent(model="test-model")
        assert result is builder  # Should return self for chaining
        
        result = result.with_gateway(port=9000)
        assert result is builder


class TestAgentConfig:
    """Test AgentConfig"""
    
    def test_default_agent_config(self):
        """Test default values"""
        config = AgentConfig()
        
        assert config.workspace == "~/.openclaw/workspace"
        assert config.tools_profile == "full"
    
    def test_agent_with_model_string(self):
        """Test agent config with model string"""
        config = AgentConfig(model="anthropic/claude-sonnet-4")
        # Should parse string to AgentModelConfig
        assert config.model is not None


class TestGatewayConfig:
    """Test GatewayConfig"""
    
    def test_default_gateway_config(self):
        """Test default values"""
        config = GatewayConfig()
        
        assert config.port == 8765
        assert config.bind == "loopback"
        assert config.auto_start_channels is True
    
    def test_host_property(self):
        """Test host property"""
        config1 = GatewayConfig(bind="loopback")
        assert config1.host == "127.0.0.1"
        
        config2 = GatewayConfig(bind="all")
        assert config2.host == "0.0.0.0"


class TestChannelsConfig:
    """Test ChannelsConfig"""
    
    def test_default_channels_config(self):
        """Test default values"""
        config = ChannelsConfig()
        
        assert config.auto_start_all is False
        assert config.max_concurrent == 10
    
    def test_get_enabled(self):
        """Test getting enabled channels"""
        config = ChannelsConfig(
            telegram=SingleChannelConfig(enabled=True),
            discord=SingleChannelConfig(enabled=False)
        )
        
        enabled = config.get_enabled()
        assert "telegram" in enabled
        assert "discord" not in enabled
    
    def test_iterate_channels(self):
        """Test iterating over channels"""
        config = ChannelsConfig(
            telegram=SingleChannelConfig(enabled=True),
            discord=SingleChannelConfig(enabled=True)
        )
        
        channels = list(config)
        channel_names = [name for name, _ in channels]
        
        assert "telegram" in channel_names
        assert "discord" in channel_names
