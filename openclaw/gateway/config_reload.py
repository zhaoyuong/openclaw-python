"""Config hot reload system - aligned with TypeScript config-reload.ts"""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from openclaw.config.loader import load_config

logger = logging.getLogger(__name__)


class ConfigFileHandler(FileSystemEventHandler):
    """Handler for config file changes"""
    
    def __init__(self, config_path: Path, callback: Callable):
        self.config_path = config_path
        self.callback = callback
        self.debounce_task: Optional[asyncio.Task] = None
    
    def on_modified(self, event: FileModifiedEvent) -> None:
        """Handle file modification"""
        if event.src_path == str(self.config_path):
            # Debounce: wait 1 second before reloading
            if self.debounce_task:
                self.debounce_task.cancel()
            
            self.debounce_task = asyncio.create_task(self._debounced_reload())
    
    async def _debounced_reload(self) -> None:
        """Debounced reload"""
        await asyncio.sleep(1)
        await self.callback()


class ConfigReloader:
    """Config file watcher and hot reloader"""
    
    def __init__(self, config_path: Path, on_reload: Callable):
        self.config_path = config_path
        self.on_reload = on_reload
        self.observer: Optional[Observer] = None
        self.handler: Optional[ConfigFileHandler] = None
    
    async def start(self) -> None:
        """Start watching config file"""
        logger.info(f"Starting config file watcher: {self.config_path}")
        
        self.handler = ConfigFileHandler(self.config_path, self._handle_reload)
        self.observer = Observer()
        self.observer.schedule(self.handler, str(self.config_path.parent), recursive=False)
        self.observer.start()
        
        logger.info("Config reloader started")
    
    async def stop(self) -> None:
        """Stop watching"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        logger.info("Config reloader stopped")
    
    async def _handle_reload(self) -> None:
        """Handle config reload"""
        logger.info("Config file changed, reloading...")
        
        try:
            # Reload config
            new_config = load_config()
            
            # Call reload callback
            await self.on_reload(new_config)
            
            logger.info("✅ Config reloaded successfully")
        except Exception as e:
            logger.error(f"Failed to reload config: {e}")


async def start_config_reloader(config_path: Path, on_reload: Callable) -> ConfigReloader:
    """Start config file reloader
    
    Args:
        config_path: Path to config file
        on_reload: Async callback function(new_config)
        
    Returns:
        ConfigReloader instance
    """
    reloader = ConfigReloader(config_path, on_reload)
    await reloader.start()
    return reloader


__all__ = ["ConfigReloader", "start_config_reloader"]
