"""Security fix utilities

This module provides utilities for fixing common security issues including:
- Permission fixes
- Path sanitization
- Input validation helpers
- Security audit fixes
"""
from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SecurityFixError(Exception):
    """Security fix error"""
    pass


def fix_file_permissions(
    path: Path | str,
    mode: int = 0o600,
    recursive: bool = False
) -> bool:
    """
    Fix file permissions to secure defaults
    
    Args:
        path: Path to fix
        mode: Target mode (default: 0o600 for files, 0o700 for dirs)
        recursive: Fix recursively
        
    Returns:
        True if fixed successfully
    """
    try:
        path = Path(path)
        
        if not path.exists():
            logger.warning(f"Path does not exist: {path}")
            return False
        
        if path.is_dir():
            # Directories need execute permission
            dir_mode = mode | 0o100
            os.chmod(path, dir_mode)
            logger.info(f"Fixed directory permissions: {path} -> {oct(dir_mode)}")
            
            if recursive:
                for item in path.rglob("*"):
                    if item.is_dir():
                        os.chmod(item, dir_mode)
                    else:
                        os.chmod(item, mode)
        else:
            os.chmod(path, mode)
            logger.info(f"Fixed file permissions: {path} -> {oct(mode)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to fix permissions: {e}")
        return False


def sanitize_path(
    path: str,
    base_path: Path | str,
    allow_absolute: bool = False
) -> Path:
    """
    Sanitize path to prevent directory traversal
    
    Args:
        path: Path to sanitize
        base_path: Base directory path
        allow_absolute: Allow absolute paths
        
    Returns:
        Sanitized path
        
    Raises:
        SecurityFixError: If path is unsafe
    """
    try:
        base_path = Path(base_path).resolve()
        
        # Convert to Path
        user_path = Path(path)
        
        # Check for absolute path
        if user_path.is_absolute():
            if not allow_absolute:
                raise SecurityFixError("Absolute paths not allowed")
            resolved = user_path.resolve()
        else:
            # Resolve relative to base
            resolved = (base_path / user_path).resolve()
        
        # Check if resolved path is within base
        try:
            resolved.relative_to(base_path)
        except ValueError:
            raise SecurityFixError(
                f"Path traversal detected: {path} resolves outside {base_path}"
            )
        
        return resolved
        
    except Exception as e:
        logger.error(f"Path sanitization failed: {e}")
        raise SecurityFixError(f"Invalid path: {e}")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing dangerous characters
    
    Args:
        filename: Filename to sanitize
        
    Returns:
        Sanitized filename
    """
    # Remove path separators
    filename = filename.replace("/", "_").replace("\\", "_")
    
    # Remove null bytes
    filename = filename.replace("\x00", "")
    
    # Remove control characters
    filename = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip(". ")
    
    # Ensure not empty
    if not filename:
        filename = "unnamed"
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255 - len(ext)] + ext
    
    return filename


def sanitize_command(command: str, allowed_commands: list[str] | None = None) -> str:
    """
    Sanitize shell command
    
    Args:
        command: Command to sanitize
        allowed_commands: List of allowed commands
        
    Returns:
        Sanitized command
        
    Raises:
        SecurityFixError: If command is unsafe
    """
    # Check for command injection patterns
    dangerous_patterns = [
        r"[;&|]",  # Command chaining
        r"[\$`]",  # Command substitution
        r"\beval\b",  # Eval
        r"\bexec\b",  # Exec
        r">\s*/dev/",  # Device file redirect
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, command):
            raise SecurityFixError(f"Dangerous pattern in command: {pattern}")
    
    # Check allowed commands
    if allowed_commands:
        cmd_name = command.split()[0] if command else ""
        if cmd_name not in allowed_commands:
            raise SecurityFixError(f"Command not allowed: {cmd_name}")
    
    return command.strip()


def validate_email(email: str) -> bool:
    """
    Validate email address
    
    Args:
        email: Email to validate
        
    Returns:
        True if valid
    """
    # Basic email regex
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def sanitize_html(html: str) -> str:
    """
    Sanitize HTML by removing dangerous tags and attributes
    
    Args:
        html: HTML to sanitize
        
    Returns:
        Sanitized HTML
    """
    # Remove script tags
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove event handlers
    html = re.sub(r"\son\w+\s*=\s*[\"'][^\"']*[\"']", "", html, flags=re.IGNORECASE)
    
    # Remove javascript: urls
    html = re.sub(r"javascript:[^\"']*", "", html, flags=re.IGNORECASE)
    
    # Remove data: urls (potential XSS)
    html = re.sub(r"data:[^\"']*", "", html, flags=re.IGNORECASE)
    
    return html


def mask_sensitive_data(text: str, mask_char: str = "*") -> str:
    """
    Mask sensitive data in text (API keys, tokens, etc.)
    
    Args:
        text: Text to mask
        mask_char: Character to use for masking
        
    Returns:
        Masked text
    """
    # Mask API keys (format: sk-... or xxxxx-xxxxx...)
    text = re.sub(
        r"\b(sk-|pk-|API[_-]?KEY[_-]?)[a-zA-Z0-9]{20,}",
        lambda m: m.group(1) + mask_char * 20,
        text,
        flags=re.IGNORECASE
    )
    
    # Mask tokens (long alphanumeric strings)
    text = re.sub(
        r"\b[a-zA-Z0-9]{40,}\b",
        mask_char * 40,
        text
    )
    
    # Mask credit card numbers
    text = re.sub(
        r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        mask_char * 16,
        text
    )
    
    # Mask passwords in common formats
    text = re.sub(
        r"(password|passwd|pwd)[\s:=]+['\"]?([^'\"\\s]+)['\"]?",
        lambda m: m.group(1) + "=" + mask_char * 10,
        text,
        flags=re.IGNORECASE
    )
    
    return text


def check_sql_injection(query: str) -> bool:
    """
    Check for SQL injection patterns
    
    Args:
        query: Query string to check
        
    Returns:
        True if suspicious patterns found
    """
    suspicious_patterns = [
        r";\s*DROP\s+TABLE",
        r";\s*DELETE\s+FROM",
        r";\s*INSERT\s+INTO",
        r";\s*UPDATE\s+",
        r"UNION\s+SELECT",
        r"--",
        r"/\*",
        r"xp_cmdshell",
    ]
    
    query_upper = query.upper()
    
    for pattern in suspicious_patterns:
        if re.search(pattern, query_upper, re.IGNORECASE):
            logger.warning(f"Suspicious SQL pattern detected: {pattern}")
            return True
    
    return False


def generate_secure_token(length: int = 32) -> str:
    """
    Generate cryptographically secure random token
    
    Args:
        length: Token length
        
    Returns:
        Secure random token (hex string)
    """
    import secrets
    return secrets.token_hex(length // 2)


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt
    
    Args:
        password: Password to hash
        
    Returns:
        Hashed password
    """
    try:
        import bcrypt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    except ImportError:
        logger.error("bcrypt not installed, falling back to basic hash")
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify password against hash
    
    Args:
        password: Password to verify
        hashed: Hashed password
        
    Returns:
        True if password matches
    """
    try:
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except ImportError:
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed


def audit_security_issues(directory: Path | str) -> list[dict[str, Any]]:
    """
    Audit directory for common security issues
    
    Args:
        directory: Directory to audit
        
    Returns:
        List of security issues found
    """
    issues: list[dict[str, Any]] = []
    directory = Path(directory)
    
    if not directory.exists():
        return issues
    
    for path in directory.rglob("*"):
        if path.is_file():
            # Check file permissions
            stat = path.stat()
            mode = stat.st_mode & 0o777
            
            # Check for world-writable files
            if mode & 0o002:
                issues.append({
                    "type": "world_writable",
                    "path": str(path),
                    "mode": oct(mode),
                    "severity": "high"
                })
            
            # Check for world-readable sensitive files
            if mode & 0o004:
                if any(pattern in path.name.lower() for pattern in [
                    "secret", "password", "key", ".env", "credential"
                ]):
                    issues.append({
                        "type": "world_readable_sensitive",
                        "path": str(path),
                        "mode": oct(mode),
                        "severity": "high"
                    })
    
    return issues
