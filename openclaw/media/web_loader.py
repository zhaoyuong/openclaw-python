"""Web media loading and optimization

Loads media from URLs or local files with automatic optimization.
Matches TypeScript src/web/media.ts
"""
import aiohttp
import io
import logging
import mimetypes
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


async def load_web_media(
    media_url: str,
    max_bytes: Optional[int] = None,
    ssrf_policy: str = "default"
) -> Dict[str, Any]:
    """
    Load media from URL or local path
    
    Matches TypeScript loadWebMedia()
    
    Args:
        media_url: URL or local file path
        max_bytes: Maximum size in bytes
        ssrf_policy: SSRF protection policy
        
    Returns:
        Dict with data, mime_type, size
    """
    # Check if local file
    if not media_url.startswith(("http://", "https://")):
        return await _load_local_media(media_url, max_bytes)
    
    # Validate URL (basic SSRF protection)
    if ssrf_policy != "disabled":
        if not _is_safe_url(media_url):
            raise ValueError(f"Unsafe URL blocked by SSRF policy: {media_url}")
    
    # Download from URL
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(media_url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status != 200:
                    raise ValueError(f"Failed to load media: HTTP {resp.status}")
                
                content = await resp.read()
                content_type = resp.headers.get("Content-Type", "")
                
                # Check size limit
                if max_bytes and len(content) > max_bytes:
                    # Try to optimize if image
                    if content_type.startswith("image/"):
                        logger.info(f"Optimizing image: {len(content)} -> max {max_bytes} bytes")
                        content = await optimize_image(content, max_bytes, content_type)
                    else:
                        raise ValueError(f"Media too large: {len(content)} > {max_bytes}")
                
                return {
                    "data": content,
                    "mime_type": content_type,
                    "size": len(content),
                    "url": media_url,
                }
    
    except aiohttp.ClientError as e:
        raise ValueError(f"Failed to download media: {e}")


async def _load_local_media(
    file_path: str,
    max_bytes: Optional[int] = None
) -> Dict[str, Any]:
    """Load media from local file"""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get MIME type
    mime_type, _ = mimetypes.guess_type(str(path))
    if not mime_type:
        mime_type = "application/octet-stream"
    
    # Read file
    content = path.read_bytes()
    
    # Check size limit
    if max_bytes and len(content) > max_bytes:
        if mime_type.startswith("image/"):
            content = await optimize_image(content, max_bytes, mime_type)
        else:
            raise ValueError(f"File too large: {len(content)} > {max_bytes}")
    
    return {
        "data": content,
        "mime_type": mime_type,
        "size": len(content),
        "path": str(path),
    }


async def optimize_image(data: bytes, max_bytes: int, mime_type: str) -> bytes:
    """
    Optimize image to reduce size
    
    Matches TypeScript image optimization logic
    
    Args:
        data: Image data
        max_bytes: Target size
        mime_type: Original MIME type
        
    Returns:
        Optimized image data
    """
    try:
        from PIL import Image
        
        img = Image.open(io.BytesIO(data))
        original_format = img.format or "JPEG"
        
        # Convert HEIC to JPEG
        if mime_type == "image/heic":
            original_format = "JPEG"
        
        # Resize if too large
        max_dimension = 2000
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            logger.info(f"Resized image to {new_size}")
        
        # Try progressive quality reduction
        for quality in [85, 70, 60, 50, 40]:
            output = io.BytesIO()
            
            # Save with quality
            save_kwargs = {
                "format": original_format,
                "quality": quality,
                "optimize": True,
            }
            
            # Handle PNG with transparency
            if original_format == "PNG" and img.mode in ("RGBA", "LA"):
                save_kwargs["compress_level"] = 9
                save_kwargs.pop("quality")
            elif img.mode not in ("RGB", "L"):
                # Convert to RGB for JPEG
                if original_format == "JPEG":
                    img = img.convert("RGB")
            
            img.save(output, **save_kwargs)
            result = output.getvalue()
            
            logger.info(f"Compressed to {len(result)} bytes (quality={quality})")
            
            if len(result) <= max_bytes:
                return result
        
        # If still too large, return best effort
        logger.warning(f"Could not optimize image below {max_bytes} bytes")
        return result
    
    except ImportError:
        logger.error("PIL not available for image optimization")
        raise ValueError("Image optimization not available (install Pillow)")
    except Exception as e:
        logger.error(f"Image optimization failed: {e}")
        raise ValueError(f"Failed to optimize image: {e}")


def _is_safe_url(url: str) -> bool:
    """
    Basic SSRF protection
    
    Blocks localhost, private IPs, etc.
    """
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    hostname = parsed.hostname
    
    if not hostname:
        return False
    
    # Block localhost
    if hostname in ("localhost", "127.0.0.1", "::1"):
        return False
    
    # Block private IPs (basic check)
    if hostname.startswith(("10.", "172.", "192.168.")):
        return False
    
    # Block internal domains
    if hostname.endswith(".local") or hostname.endswith(".internal"):
        return False
    
    return True


def detect_media_type(data: bytes, mime_type: str) -> str:
    """
    Detect media type from content
    
    Returns: "image", "video", "audio", "document"
    """
    if mime_type.startswith("image/"):
        return "image"
    elif mime_type.startswith("video/"):
        return "video"
    elif mime_type.startswith("audio/"):
        return "audio"
    else:
        return "document"


def is_gif(mime_type: str, filename: str = "") -> bool:
    """Check if media is a GIF"""
    return (
        mime_type == "image/gif" or
        filename.lower().endswith(".gif")
    )
