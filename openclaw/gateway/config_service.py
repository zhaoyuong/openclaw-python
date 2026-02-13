"""
Configuration management service

Handles saving, loading, and applying Gateway configuration changes.
"""

import json
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ConfigService:
    """Manages configuration persistence and updates"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize config service
        
        Args:
            config_path: Path to config file (optional)
        """
        self.config_path = config_path
        self._current_config: Optional[dict] = None
    
    def load_config(self) -> dict:
        """
        Load configuration from file
        
        Returns:
            Configuration dictionary
        """
        if not self.config_path or not self.config_path.exists():
            logger.warning("No config file found, returning empty config")
            return {}
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            self._current_config = config
            return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def save_config(self, config: dict) -> bool:
        """
        Save configuration to file
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if successful
        """
        if not self.config_path:
            logger.warning("No config path set, cannot save")
            return False
        
        try:
            # Ensure parent directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write config
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            self._current_config = config
            logger.info(f"Saved configuration to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    def patch_config(self, patch: dict) -> dict:
        """
        Apply patch to configuration
        
        Args:
            patch: Dictionary of key-value pairs to update
            
        Returns:
            Updated configuration
        """
        if self._current_config is None:
            self._current_config = self.load_config()
        
        # Apply patch (simple merge for now)
        for key, value in patch.items():
            self._set_nested_value(self._current_config, key, value)
        
        # Save updated config
        self.save_config(self._current_config)
        
        return self._current_config
    
    def _set_nested_value(self, config: dict, key_path: str, value: Any):
        """
        Set nested configuration value using dot notation
        
        Args:
            config: Configuration dictionary
            key_path: Key path (e.g., "gateway.auth.token")
            value: Value to set
        """
        keys = key_path.split('.')
        current = config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def get_config_schema(self) -> dict:
        """
        Get configuration schema
        
        Returns:
            JSON schema for configuration
        """
        # Simplified schema - in production this should be comprehensive
        return {
            "type": "object",
            "properties": {
                "gateway": {
                    "type": "object",
                    "properties": {
                        "auth": {
                            "type": "object",
                            "properties": {
                                "mode": {"type": "string", "enum": ["token", "password"]},
                                "token": {"type": "string"},
                                "password": {"type": "string"}
                            }
                        },
                        "bindHost": {"type": "string"},
                        "bindPort": {"type": "integer"}
                    }
                },
                "agents": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "model": {"type": "string"},
                            "temperature": {"type": "number"},
                            "maxTokens": {"type": "integer"}
                        }
                    }
                }
            }
        }


# Global config service instance
_config_service: Optional[ConfigService] = None


def get_config_service() -> ConfigService:
    """Get global config service instance"""
    global _config_service
    if _config_service is None:
        _config_service = ConfigService()
    return _config_service


def set_config_service(service: ConfigService):
    """Set global config service instance"""
    global _config_service
    _config_service = service
