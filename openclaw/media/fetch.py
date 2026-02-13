"""Media fetching utilities

This module provides utilities for fetching media from various sources including:
- URL downloads
- Social media platforms
- Cloud storage
- Streaming services
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .constants import (
    DEFAULT_MAX_AUDIO_SIZE,
    DEFAULT_MAX_IMAGE_SIZE,
    DEFAULT_MAX_VIDEO_SIZE,
    get_media_category,
)

logger = logging.getLogger(__name__)


class MediaFetchError(Exception):
    """Media fetch error"""
    pass


async def fetch_from_url(
    url: str,
    output_path: Path | str | None = None,
    max_size: int | None = None,
    timeout: int = 60,
) -> tuple[bytes, str]:
    """
    Fetch media from URL
    
    Args:
        url: URL to fetch from
        output_path: Optional output path to save to
        max_size: Maximum file size in bytes
        timeout: Request timeout in seconds
        
    Returns:
        Tuple of (content_bytes, content_type)
        
    Raises:
        MediaFetchError: If fetch fails
    """
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                # Check status
                if response.status != 200:
                    raise MediaFetchError(f"HTTP {response.status}: {response.reason}")
                
                # Get content type
                content_type = response.headers.get("Content-Type", "application/octet-stream")
                
                # Check content length
                content_length = response.headers.get("Content-Length")
                if content_length and max_size:
                    if int(content_length) > max_size:
                        raise MediaFetchError(
                            f"File too large: {int(content_length)} bytes (max: {max_size})"
                        )
                
                # Read content
                content = await response.read()
                
                # Check actual size
                if max_size and len(content) > max_size:
                    raise MediaFetchError(
                        f"File too large: {len(content)} bytes (max: {max_size})"
                    )
                
                # Save to file if output path provided
                if output_path:
                    output_path = Path(output_path)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(content)
                    logger.info(f"Saved media to: {output_path}")
                
                logger.info(f"Fetched {len(content)} bytes from {url}")
                return content, content_type
                
    except aiohttp.ClientError as e:
        raise MediaFetchError(f"Network error: {e}")
    except Exception as e:
        logger.error(f"Failed to fetch media: {e}")
        raise MediaFetchError(f"Fetch failed: {e}")


async def fetch_image(
    url: str,
    output_path: Path | str | None = None,
    max_size: int = DEFAULT_MAX_IMAGE_SIZE,
) -> tuple[bytes, str]:
    """
    Fetch image from URL
    
    Args:
        url: Image URL
        output_path: Optional output path
        max_size: Maximum size in bytes
        
    Returns:
        Tuple of (image_bytes, content_type)
    """
    content, content_type = await fetch_from_url(url, output_path, max_size)
    
    # Validate it's an image
    if not content_type.startswith("image/"):
        raise MediaFetchError(f"Not an image: {content_type}")
    
    return content, content_type


async def fetch_video(
    url: str,
    output_path: Path | str | None = None,
    max_size: int = DEFAULT_MAX_VIDEO_SIZE,
) -> tuple[bytes, str]:
    """
    Fetch video from URL
    
    Args:
        url: Video URL
        output_path: Optional output path
        max_size: Maximum size in bytes
        
    Returns:
        Tuple of (video_bytes, content_type)
    """
    content, content_type = await fetch_from_url(url, output_path, max_size, timeout=300)
    
    # Validate it's a video
    if not content_type.startswith("video/"):
        raise MediaFetchError(f"Not a video: {content_type}")
    
    return content, content_type


async def fetch_audio(
    url: str,
    output_path: Path | str | None = None,
    max_size: int = DEFAULT_MAX_AUDIO_SIZE,
) -> tuple[bytes, str]:
    """
    Fetch audio from URL
    
    Args:
        url: Audio URL
        output_path: Optional output path
        max_size: Maximum size in bytes
        
    Returns:
        Tuple of (audio_bytes, content_type)
    """
    content, content_type = await fetch_from_url(url, output_path, max_size, timeout=180)
    
    # Validate it's audio
    if not content_type.startswith("audio/"):
        raise MediaFetchError(f"Not audio: {content_type}")
    
    return content, content_type


def get_youtube_video_info(url: str) -> dict[str, Any]:
    """
    Get video information from YouTube URL
    
    Args:
        url: YouTube URL
        
    Returns:
        Video information dictionary
        
    Raises:
        MediaFetchError: If extraction fails
    """
    try:
        import yt_dlp
        
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "view_count": info.get("view_count"),
                "thumbnail": info.get("thumbnail"),
                "description": info.get("description"),
            }
            
    except ImportError:
        raise MediaFetchError("yt-dlp not installed")
    except Exception as e:
        raise MediaFetchError(f"Failed to get video info: {e}")


async def download_youtube_video(
    url: str,
    output_path: Path | str,
    format_spec: str = "best",
) -> Path:
    """
    Download video from YouTube
    
    Args:
        url: YouTube URL
        output_path: Output file path
        format_spec: Format specification (best, worst, or specific format)
        
    Returns:
        Path to downloaded file
        
    Raises:
        MediaFetchError: If download fails
    """
    try:
        import yt_dlp
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        ydl_opts = {
            "format": format_spec,
            "outtmpl": str(output_path),
            "quiet": True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        logger.info(f"Downloaded YouTube video to: {output_path}")
        return output_path
        
    except ImportError:
        raise MediaFetchError("yt-dlp not installed")
    except Exception as e:
        raise MediaFetchError(f"Download failed: {e}")


def extract_media_url(text: str) -> list[str]:
    """
    Extract media URLs from text
    
    Args:
        text: Text to extract URLs from
        
    Returns:
        List of media URLs
    """
    import re
    
    # URL regex pattern
    url_pattern = r"https?://[^\s<>\"{}|\\^`\[\]]+"
    
    urls = re.findall(url_pattern, text)
    
    # Filter for media URLs (basic heuristic)
    media_urls = []
    for url in urls:
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Check if URL ends with media extension
        if any(path.endswith(f".{ext}") for ext in [
            "jpg", "jpeg", "png", "gif", "webp", "bmp",
            "mp4", "webm", "ogg", "mov", "avi",
            "mp3", "wav", "ogg", "m4a", "flac"
        ]):
            media_urls.append(url)
        
        # Check for common media hosting domains
        elif any(domain in parsed.netloc for domain in [
            "youtube.com", "youtu.be", "vimeo.com",
            "imgur.com", "instagram.com", "twitter.com",
            "soundcloud.com", "spotify.com"
        ]):
            media_urls.append(url)
    
    return media_urls


def is_youtube_url(url: str) -> bool:
    """
    Check if URL is a YouTube URL
    
    Args:
        url: URL to check
        
    Returns:
        True if YouTube URL
    """
    parsed = urlparse(url)
    return parsed.netloc in ["youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"]


def is_media_url(url: str) -> bool:
    """
    Check if URL is likely a direct media URL
    
    Args:
        url: URL to check
        
    Returns:
        True if likely media URL
    """
    parsed = urlparse(url)
    path = parsed.path.lower()
    
    # Check file extension
    media_extensions = [
        "jpg", "jpeg", "png", "gif", "webp", "bmp", "svg",
        "mp4", "webm", "ogg", "mov", "avi", "mkv",
        "mp3", "wav", "ogg", "m4a", "flac", "aac"
    ]
    
    return any(path.endswith(f".{ext}") for ext in media_extensions)
