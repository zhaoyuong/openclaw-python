"""Media processing constants

This module provides constants used across media processing modules including:
- Supported formats
- File size limits
- Quality presets
- MIME type mappings
"""
from __future__ import annotations

# Supported image formats
SUPPORTED_IMAGE_FORMATS = {
    "jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff", "tif", "svg", "ico"
}

# Supported video formats
SUPPORTED_VIDEO_FORMATS = {
    "mp4", "webm", "ogg", "mov", "avi", "mkv", "flv", "wmv", "m4v"
}

# Supported audio formats
SUPPORTED_AUDIO_FORMATS = {
    "mp3", "wav", "ogg", "opus", "m4a", "aac", "flac", "wma", "aiff", "ape"
}

# Supported document formats
SUPPORTED_DOCUMENT_FORMATS = {
    "pdf", "txt", "md", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "odt", "ods", "odp", "rtf"
}

# MIME type mappings
MIME_TYPE_MAP = {
    # Images
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
    "bmp": "image/bmp",
    "tiff": "image/tiff",
    "tif": "image/tiff",
    "svg": "image/svg+xml",
    "ico": "image/x-icon",
    
    # Videos
    "mp4": "video/mp4",
    "webm": "video/webm",
    "ogg": "video/ogg",
    "mov": "video/quicktime",
    "avi": "video/x-msvideo",
    "mkv": "video/x-matroska",
    "flv": "video/x-flv",
    "wmv": "video/x-ms-wmv",
    
    # Audio
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "ogg": "audio/ogg",
    "opus": "audio/opus",
    "m4a": "audio/mp4",
    "aac": "audio/aac",
    "flac": "audio/flac",
    "wma": "audio/x-ms-wma",
    
    # Documents
    "pdf": "application/pdf",
    "txt": "text/plain",
    "md": "text/markdown",
    "json": "application/json",
    "xml": "application/xml",
    "html": "text/html",
    "css": "text/css",
    "js": "application/javascript",
}

# File size limits (in bytes)
DEFAULT_MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB
DEFAULT_MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100 MB
DEFAULT_MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50 MB
DEFAULT_MAX_DOCUMENT_SIZE = 20 * 1024 * 1024  # 20 MB

# Image quality presets
IMAGE_QUALITY_PRESETS = {
    "low": 60,
    "medium": 80,
    "high": 90,
    "max": 95,
}

# Video quality presets (CRF values for x264/x265)
VIDEO_QUALITY_PRESETS = {
    "low": 28,
    "medium": 23,
    "high": 18,
    "max": 15,
}

# Audio bitrate presets
AUDIO_BITRATE_PRESETS = {
    "low": "64k",
    "medium": "128k",
    "high": "192k",
    "max": "320k",
}

# Image dimension limits
MAX_IMAGE_WIDTH = 10000
MAX_IMAGE_HEIGHT = 10000
MAX_IMAGE_PIXELS = 100_000_000  # 100 megapixels

# Thumbnail sizes
THUMBNAIL_SIZES = {
    "small": (128, 128),
    "medium": (256, 256),
    "large": (512, 512),
}

# Video resolution presets
VIDEO_RESOLUTIONS = {
    "240p": (426, 240),
    "360p": (640, 360),
    "480p": (854, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "1440p": (2560, 1440),
    "2160p": (3840, 2160),  # 4K
}

# Common framerates
VIDEO_FRAMERATES = [24, 25, 30, 50, 60]

# Audio sample rates
AUDIO_SAMPLE_RATES = [8000, 16000, 22050, 44100, 48000, 96000]

# Supported subtitle formats
SUPPORTED_SUBTITLE_FORMATS = {
    "srt", "vtt", "ass", "ssa", "sub"
}

# Media processing timeouts (seconds)
IMAGE_PROCESSING_TIMEOUT = 30
VIDEO_PROCESSING_TIMEOUT = 600
AUDIO_PROCESSING_TIMEOUT = 300

# Cache settings
MEDIA_CACHE_TTL = 3600  # 1 hour
MEDIA_CACHE_MAX_SIZE = 1024 * 1024 * 1024  # 1 GB


def get_mime_type(extension: str) -> str:
    """
    Get MIME type for file extension
    
    Args:
        extension: File extension (with or without dot)
        
    Returns:
        MIME type string
    """
    ext = extension.lstrip(".").lower()
    return MIME_TYPE_MAP.get(ext, "application/octet-stream")


def is_supported_format(filename: str, category: str | None = None) -> bool:
    """
    Check if file format is supported
    
    Args:
        filename: File name
        category: Category to check (image, video, audio, document) or None for all
        
    Returns:
        True if supported
    """
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    
    if category == "image":
        return ext in SUPPORTED_IMAGE_FORMATS
    elif category == "video":
        return ext in SUPPORTED_VIDEO_FORMATS
    elif category == "audio":
        return ext in SUPPORTED_AUDIO_FORMATS
    elif category == "document":
        return ext in SUPPORTED_DOCUMENT_FORMATS
    else:
        # Check all categories
        return (
            ext in SUPPORTED_IMAGE_FORMATS
            or ext in SUPPORTED_VIDEO_FORMATS
            or ext in SUPPORTED_AUDIO_FORMATS
            or ext in SUPPORTED_DOCUMENT_FORMATS
        )


def get_media_category(filename: str) -> str | None:
    """
    Get media category for file
    
    Args:
        filename: File name
        
    Returns:
        Category string or None
    """
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    
    if ext in SUPPORTED_IMAGE_FORMATS:
        return "image"
    elif ext in SUPPORTED_VIDEO_FORMATS:
        return "video"
    elif ext in SUPPORTED_AUDIO_FORMATS:
        return "audio"
    elif ext in SUPPORTED_DOCUMENT_FORMATS:
        return "document"
    
    return None
