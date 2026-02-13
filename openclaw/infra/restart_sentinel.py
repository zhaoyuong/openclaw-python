"""Restart detection and sentinel file management

This module provides restart detection functionality to help agents
persist state across restarts and detect when a restart has occurred.
"""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class RestartSentinel:
    """Restart detection using sentinel files"""
    
    def __init__(self, sentinel_path: Path | str):
        """
        Initialize restart sentinel
        
        Args:
            sentinel_path: Path to sentinel file
        """
        self.sentinel_path = Path(sentinel_path)
        self.sentinel_path.parent.mkdir(parents=True, exist_ok=True)
        self._process_id = os.getpid()
        self._start_time = time.time()
    
    def create_sentinel(self, data: dict[str, Any] | None = None) -> None:
        """
        Create sentinel file
        
        Args:
            data: Optional data to store in sentinel
        """
        import json
        
        sentinel_data = {
            "pid": self._process_id,
            "start_time": self._start_time,
            "timestamp": time.time(),
        }
        
        if data:
            sentinel_data.update(data)
        
        try:
            with open(self.sentinel_path, "w") as f:
                json.dump(sentinel_data, f, indent=2)
            
            logger.info(f"Created sentinel file: {self.sentinel_path}")
        
        except Exception as e:
            logger.error(f"Failed to create sentinel: {e}")
    
    def check_restart(self) -> bool:
        """
        Check if this is a restart
        
        Returns:
            True if restarted (sentinel exists and is from previous run)
        """
        if not self.sentinel_path.exists():
            return False
        
        try:
            import json
            
            with open(self.sentinel_path, "r") as f:
                data = json.load(f)
            
            # Check if PID is different
            old_pid = data.get("pid")
            if old_pid and old_pid != self._process_id:
                logger.info(f"Restart detected: old PID {old_pid}, new PID {self._process_id}")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Failed to check sentinel: {e}")
            return False
    
    def get_previous_data(self) -> dict[str, Any] | None:
        """
        Get data from previous run
        
        Returns:
            Previous run data or None
        """
        if not self.sentinel_path.exists():
            return None
        
        try:
            import json
            
            with open(self.sentinel_path, "r") as f:
                return json.load(f)
        
        except Exception as e:
            logger.error(f"Failed to read sentinel: {e}")
            return None
    
    def remove_sentinel(self) -> None:
        """Remove sentinel file"""
        try:
            if self.sentinel_path.exists():
                self.sentinel_path.unlink()
                logger.info(f"Removed sentinel file: {self.sentinel_path}")
        
        except Exception as e:
            logger.error(f"Failed to remove sentinel: {e}")
    
    def update_sentinel(self, data: dict[str, Any]) -> None:
        """
        Update sentinel with new data
        
        Args:
            data: Data to update
        """
        try:
            import json
            
            # Read existing data
            existing_data = {}
            if self.sentinel_path.exists():
                with open(self.sentinel_path, "r") as f:
                    existing_data = json.load(f)
            
            # Update
            existing_data.update(data)
            existing_data["last_update"] = time.time()
            
            # Write back
            with open(self.sentinel_path, "w") as f:
                json.dump(existing_data, f, indent=2)
        
        except Exception as e:
            logger.error(f"Failed to update sentinel: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        self.create_sentinel()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.remove_sentinel()


def detect_restart(sentinel_path: Path | str) -> bool:
    """
    Convenience function to detect restart
    
    Args:
        sentinel_path: Path to sentinel file
        
    Returns:
        True if restarted
    """
    sentinel = RestartSentinel(sentinel_path)
    return sentinel.check_restart()
