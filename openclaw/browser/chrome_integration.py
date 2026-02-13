"""Chrome browser integration and management

This module provides Chrome browser lifecycle management including:
- Browser process launching
- Profile management
- Extension loading
- Debugging port management
"""
from __future__ import annotations

import asyncio
import logging
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ChromeError(Exception):
    """Chrome integration error"""
    pass


class ChromeBrowser:
    """Chrome browser instance manager"""
    
    def __init__(
        self,
        profile_dir: Path | None = None,
        headless: bool = False,
        debugging_port: int = 9222,
        extensions: list[Path] | None = None,
        user_data_dir: Path | None = None,
    ):
        """
        Initialize Chrome browser instance
        
        Args:
            profile_dir: Chrome profile directory
            headless: Run in headless mode
            debugging_port: Remote debugging port
            extensions: List of extension directories to load
            user_data_dir: User data directory
        """
        self.profile_dir = profile_dir
        self.headless = headless
        self.debugging_port = debugging_port
        self.extensions = extensions or []
        self.user_data_dir = user_data_dir
        self.process: subprocess.Popen | None = None
        self._temp_profile: Path | None = None
    
    def get_chrome_path(self) -> str:
        """
        Get Chrome executable path for current platform
        
        Returns:
            Path to Chrome executable
            
        Raises:
            ChromeError: If Chrome not found
        """
        system = platform.system()
        
        if system == "Darwin":  # macOS
            paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
            ]
        elif system == "Linux":
            paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium",
            ]
        elif system == "Windows":
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
        else:
            raise ChromeError(f"Unsupported platform: {system}")
        
        for path in paths:
            if os.path.exists(path):
                return path
        
        raise ChromeError("Chrome not found. Please install Google Chrome.")
    
    def _get_chrome_args(self) -> list[str]:
        """
        Get Chrome command line arguments
        
        Returns:
            List of command line arguments
        """
        args = [
            f"--remote-debugging-port={self.debugging_port}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-breakpad",
            "--disable-client-side-phishing-detection",
            "--disable-component-extensions-with-background-pages",
            "--disable-default-apps",
            "--disable-dev-shm-usage",
            "--disable-extensions",
            "--disable-features=TranslateUI",
            "--disable-hang-monitor",
            "--disable-ipc-flooding-protection",
            "--disable-popup-blocking",
            "--disable-prompt-on-repost",
            "--disable-renderer-backgrounding",
            "--disable-sync",
            "--force-color-profile=srgb",
            "--metrics-recording-only",
            "--no-service-autorun",
            "--password-store=basic",
            "--use-mock-keychain",
        ]
        
        if self.headless:
            args.append("--headless=new")
        
        # User data directory
        if self.user_data_dir:
            args.append(f"--user-data-dir={self.user_data_dir}")
        elif self.profile_dir:
            args.append(f"--user-data-dir={self.profile_dir}")
        
        # Load extensions
        if self.extensions:
            extension_paths = ",".join(str(ext) for ext in self.extensions)
            args.append(f"--load-extension={extension_paths}")
            args.append("--disable-extensions-except=" + extension_paths)
        
        return args
    
    async def launch(self, url: str = "about:blank") -> None:
        """
        Launch Chrome browser
        
        Args:
            url: Initial URL to navigate to
            
        Raises:
            ChromeError: If launch fails
        """
        if self.process:
            raise ChromeError("Browser already running")
        
        try:
            chrome_path = self.get_chrome_path()
            args = [chrome_path] + self._get_chrome_args() + [url]
            
            logger.info(f"Launching Chrome: {' '.join(args)}")
            
            self.process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
            )
            
            # Wait for browser to be ready
            await asyncio.sleep(2)
            
            if self.process.poll() is not None:
                raise ChromeError("Browser process exited immediately")
            
            logger.info(f"Chrome launched on port {self.debugging_port}")
            
        except Exception as e:
            logger.error(f"Failed to launch Chrome: {e}")
            raise ChromeError(f"Launch failed: {e}")
    
    async def close(self) -> None:
        """Close Chrome browser"""
        if self.process:
            try:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait()
                
                logger.info("Chrome browser closed")
                
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
            
            finally:
                self.process = None
        
        # Clean up temporary profile
        if self._temp_profile and self._temp_profile.exists():
            try:
                shutil.rmtree(self._temp_profile)
                logger.info(f"Cleaned up temp profile: {self._temp_profile}")
            except Exception as e:
                logger.warning(f"Failed to clean up temp profile: {e}")
    
    def is_running(self) -> bool:
        """
        Check if browser is running
        
        Returns:
            True if running
        """
        return self.process is not None and self.process.poll() is None
    
    def get_ws_endpoint(self) -> str:
        """
        Get WebSocket endpoint for CDP
        
        Returns:
            WebSocket URL
        """
        return f"ws://localhost:{self.debugging_port}/devtools/browser"
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.launch()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()


async def get_chrome_version() -> str | None:
    """
    Get installed Chrome version
    
    Returns:
        Version string or None if not found
    """
    try:
        browser = ChromeBrowser()
        chrome_path = browser.get_chrome_path()
        
        result = subprocess.run(
            [chrome_path, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # Parse version from output (e.g., "Google Chrome 120.0.6099.109")
            version = result.stdout.strip().split()[-1]
            return version
        
    except Exception as e:
        logger.warning(f"Failed to get Chrome version: {e}")
    
    return None


async def is_chrome_installed() -> bool:
    """
    Check if Chrome is installed
    
    Returns:
        True if Chrome is installed
    """
    try:
        browser = ChromeBrowser()
        browser.get_chrome_path()
        return True
    except ChromeError:
        return False
