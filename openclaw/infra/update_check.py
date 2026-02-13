"""Update checking functionality

This module provides functionality to check for updates from a remote source.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class VersionInfo:
    """Version information"""
    
    version: str
    release_date: str | None = None
    release_notes: str | None = None
    download_url: str | None = None
    breaking_changes: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "version": self.version,
            "release_date": self.release_date,
            "release_notes": self.release_notes,
            "download_url": self.download_url,
            "breaking_changes": self.breaking_changes,
        }


class UpdateChecker:
    """Check for software updates"""
    
    def __init__(
        self,
        current_version: str,
        update_url: str | None = None,
    ):
        """
        Initialize update checker
        
        Args:
            current_version: Current version string
            update_url: URL to check for updates
        """
        self.current_version = current_version
        self.update_url = update_url
    
    async def check_for_updates(self) -> VersionInfo | None:
        """
        Check for available updates
        
        Returns:
            Latest version info or None if no updates
        """
        if not self.update_url:
            logger.info("No update URL configured")
            return None
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.update_url,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status != 200:
                        logger.warning(f"Update check failed: HTTP {response.status}")
                        return None
                    
                    data = await response.json()
                    
                    latest_version = data.get("version")
                    if not latest_version:
                        logger.warning("No version in update response")
                        return None
                    
                    # Compare versions
                    if self._compare_versions(latest_version, self.current_version) > 0:
                        return VersionInfo(
                            version=latest_version,
                            release_date=data.get("release_date"),
                            release_notes=data.get("release_notes"),
                            download_url=data.get("download_url"),
                            breaking_changes=data.get("breaking_changes", False),
                        )
                    
                    logger.info(f"Current version {self.current_version} is up to date")
                    return None
        
        except Exception as e:
            logger.error(f"Update check failed: {e}")
            return None
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """
        Compare two version strings
        
        Args:
            v1: First version
            v2: Second version
            
        Returns:
            1 if v1 > v2, -1 if v1 < v2, 0 if equal
        """
        try:
            # Parse semantic versions (e.g., "1.2.3")
            parts1 = [int(x) for x in v1.split(".")]
            parts2 = [int(x) for x in v2.split(".")]
            
            # Pad to same length
            max_len = max(len(parts1), len(parts2))
            parts1.extend([0] * (max_len - len(parts1)))
            parts2.extend([0] * (max_len - len(parts2)))
            
            # Compare
            for p1, p2 in zip(parts1, parts2):
                if p1 > p2:
                    return 1
                elif p1 < p2:
                    return -1
            
            return 0
        
        except Exception:
            # Fallback to string comparison
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
            return 0
