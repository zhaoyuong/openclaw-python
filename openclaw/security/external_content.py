"""External content validation and security

This module provides security validation for external content including:
- URL validation and sanitization
- Content type validation
- Malware scanning integration
- Safe content loading
"""
from __future__ import annotations

import logging
import mimetypes
import re
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ExternalContentError(Exception):
    """External content security error"""
    pass


class URLValidator:
    """URL validation and sanitization"""
    
    # Dangerous URL schemes
    BLOCKED_SCHEMES = {
        "file", "javascript", "data", "vbscript", "about"
    }
    
    # Suspicious patterns in URLs
    SUSPICIOUS_PATTERNS = [
        r"[<>\"']",  # HTML/script injection
        r"\.\./",  # Path traversal
        r"\\x[0-9a-f]{2}",  # Hex encoding
        r"%[0-9a-f]{2}",  # URL encoding (check for suspicious patterns)
    ]
    
    def __init__(self, allowed_domains: list[str] | None = None):
        """
        Initialize URL validator
        
        Args:
            allowed_domains: List of allowed domains (None = all allowed)
        """
        self.allowed_domains = allowed_domains
    
    def validate_url(self, url: str) -> bool:
        """
        Validate URL for security
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is safe
            
        Raises:
            ExternalContentError: If URL is unsafe
        """
        try:
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme.lower() in self.BLOCKED_SCHEMES:
                raise ExternalContentError(f"Blocked URL scheme: {parsed.scheme}")
            
            # Only allow http(s) and ftp
            if parsed.scheme.lower() not in ["http", "https", "ftp", "ftps"]:
                raise ExternalContentError(f"Unsupported URL scheme: {parsed.scheme}")
            
            # Check for suspicious patterns
            for pattern in self.SUSPICIOUS_PATTERNS:
                if re.search(pattern, url, re.IGNORECASE):
                    raise ExternalContentError(f"Suspicious pattern in URL: {pattern}")
            
            # Check domain whitelist
            if self.allowed_domains:
                domain = parsed.netloc.lower()
                if not any(allowed in domain for allowed in self.allowed_domains):
                    raise ExternalContentError(f"Domain not allowed: {domain}")
            
            return True
            
        except Exception as e:
            logger.error(f"URL validation failed: {e}")
            raise ExternalContentError(f"Invalid URL: {e}")
    
    def sanitize_url(self, url: str) -> str:
        """
        Sanitize URL by removing dangerous parts
        
        Args:
            url: URL to sanitize
            
        Returns:
            Sanitized URL
        """
        # Remove whitespace
        url = url.strip()
        
        # Parse and rebuild
        parsed = urlparse(url)
        
        # Force https if http
        scheme = "https" if parsed.scheme.lower() == "http" else parsed.scheme
        
        # Remove fragment (after #)
        return f"{scheme}://{parsed.netloc}{parsed.path}{'?' + parsed.query if parsed.query else ''}"
    
    def is_safe_redirect(self, original_url: str, redirect_url: str) -> bool:
        """
        Check if redirect is safe (same domain or allowed)
        
        Args:
            original_url: Original URL
            redirect_url: Redirect target URL
            
        Returns:
            True if redirect is safe
        """
        try:
            orig_parsed = urlparse(original_url)
            redir_parsed = urlparse(redirect_url)
            
            # Same domain is always safe
            if orig_parsed.netloc == redir_parsed.netloc:
                return True
            
            # Check if redirect domain is allowed
            if self.allowed_domains:
                return any(
                    allowed in redir_parsed.netloc.lower()
                    for allowed in self.allowed_domains
                )
            
            # Be conservative: disallow cross-domain redirects by default
            return False
            
        except Exception:
            return False


class ContentValidator:
    """Content type and format validation"""
    
    # Allowed content types for different categories
    ALLOWED_IMAGE_TYPES = {
        "image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"
    }
    
    ALLOWED_VIDEO_TYPES = {
        "video/mp4", "video/webm", "video/ogg"
    }
    
    ALLOWED_AUDIO_TYPES = {
        "audio/mpeg", "audio/wav", "audio/ogg", "audio/webm"
    }
    
    ALLOWED_DOCUMENT_TYPES = {
        "application/pdf", "text/plain", "text/markdown",
        "application/json", "application/xml"
    }
    
    # Dangerous file extensions
    BLOCKED_EXTENSIONS = {
        "exe", "dll", "so", "dylib", "bat", "cmd", "sh", "ps1",
        "vbs", "scr", "msi", "app", "deb", "rpm", "jar"
    }
    
    def __init__(self):
        """Initialize content validator"""
        pass
    
    def validate_content_type(
        self,
        content_type: str,
        allowed_categories: list[str] | None = None
    ) -> bool:
        """
        Validate content type
        
        Args:
            content_type: MIME type to validate
            allowed_categories: Allowed categories (image, video, audio, document)
            
        Returns:
            True if content type is allowed
            
        Raises:
            ExternalContentError: If content type is not allowed
        """
        content_type = content_type.lower().split(";")[0].strip()
        
        # Check against allowed categories
        if allowed_categories:
            allowed_types = set()
            if "image" in allowed_categories:
                allowed_types.update(self.ALLOWED_IMAGE_TYPES)
            if "video" in allowed_categories:
                allowed_types.update(self.ALLOWED_VIDEO_TYPES)
            if "audio" in allowed_categories:
                allowed_types.update(self.ALLOWED_AUDIO_TYPES)
            if "document" in allowed_categories:
                allowed_types.update(self.ALLOWED_DOCUMENT_TYPES)
            
            if content_type not in allowed_types:
                raise ExternalContentError(
                    f"Content type not allowed: {content_type}"
                )
        
        return True
    
    def validate_file_extension(self, filename: str) -> bool:
        """
        Validate file extension
        
        Args:
            filename: File name to validate
            
        Returns:
            True if extension is safe
            
        Raises:
            ExternalContentError: If extension is blocked
        """
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        
        if ext in self.BLOCKED_EXTENSIONS:
            raise ExternalContentError(f"Blocked file extension: {ext}")
        
        return True
    
    def validate_file_size(
        self,
        size_bytes: int,
        max_size_mb: int = 10
    ) -> bool:
        """
        Validate file size
        
        Args:
            size_bytes: File size in bytes
            max_size_mb: Maximum size in MB
            
        Returns:
            True if size is within limit
            
        Raises:
            ExternalContentError: If file is too large
        """
        max_bytes = max_size_mb * 1024 * 1024
        
        if size_bytes > max_bytes:
            raise ExternalContentError(
                f"File too large: {size_bytes / (1024 * 1024):.1f}MB "
                f"(max: {max_size_mb}MB)"
            )
        
        return True
    
    def detect_content_type(self, filename: str, content: bytes | None = None) -> str:
        """
        Detect content type from filename and content
        
        Args:
            filename: File name
            content: File content (for magic number detection)
            
        Returns:
            Detected MIME type
        """
        # Try filename extension first
        mime_type, _ = mimetypes.guess_type(filename)
        
        if mime_type:
            return mime_type
        
        # Try magic numbers if content provided
        if content and len(content) >= 4:
            # Check common magic numbers
            magic = content[:4]
            
            # PNG
            if magic == b'\x89PNG':
                return "image/png"
            # JPEG
            elif magic[:2] == b'\xff\xd8':
                return "image/jpeg"
            # GIF
            elif magic[:3] == b'GIF':
                return "image/gif"
            # PDF
            elif magic == b'%PDF':
                return "application/pdf"
            # ZIP
            elif magic[:2] == b'PK':
                return "application/zip"
        
        # Default to octet-stream
        return "application/octet-stream"


class ExternalContentLoader:
    """Safe external content loading"""
    
    def __init__(
        self,
        url_validator: URLValidator | None = None,
        content_validator: ContentValidator | None = None,
    ):
        """
        Initialize content loader
        
        Args:
            url_validator: URL validator
            content_validator: Content validator
        """
        self.url_validator = url_validator or URLValidator()
        self.content_validator = content_validator or ContentValidator()
    
    async def load_content(
        self,
        url: str,
        allowed_content_types: list[str] | None = None,
        max_size_mb: int = 10,
    ) -> tuple[bytes, str]:
        """
        Safely load external content
        
        Args:
            url: URL to load from
            allowed_content_types: Allowed content type categories
            max_size_mb: Maximum file size in MB
            
        Returns:
            Tuple of (content_bytes, content_type)
            
        Raises:
            ExternalContentError: If content is unsafe or loading fails
        """
        # Validate URL
        self.url_validator.validate_url(url)
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    # Check content type
                    content_type = response.headers.get("Content-Type", "application/octet-stream")
                    
                    if allowed_content_types:
                        self.content_validator.validate_content_type(
                            content_type,
                            allowed_content_types
                        )
                    
                    # Check content length
                    content_length = response.headers.get("Content-Length")
                    if content_length:
                        self.content_validator.validate_file_size(
                            int(content_length),
                            max_size_mb
                        )
                    
                    # Read content
                    content = await response.read()
                    
                    # Validate actual size
                    self.content_validator.validate_file_size(len(content), max_size_mb)
                    
                    logger.info(f"Loaded {len(content)} bytes from {url}")
                    return content, content_type
                    
        except Exception as e:
            logger.error(f"Failed to load content: {e}")
            raise ExternalContentError(f"Content loading failed: {e}")


# Convenience functions
def validate_url(url: str, allowed_domains: list[str] | None = None) -> bool:
    """
    Validate URL for security
    
    Args:
        url: URL to validate
        allowed_domains: Allowed domains
        
    Returns:
        True if URL is safe
    """
    validator = URLValidator(allowed_domains=allowed_domains)
    return validator.validate_url(url)


def sanitize_url(url: str) -> str:
    """
    Sanitize URL
    
    Args:
        url: URL to sanitize
        
    Returns:
        Sanitized URL
    """
    validator = URLValidator()
    return validator.sanitize_url(url)
