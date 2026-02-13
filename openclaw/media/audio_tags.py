"""Audio metadata extraction

This module provides utilities for extracting metadata from audio files including:
- ID3 tags (MP3)
- Vorbis comments (OGG, FLAC)
- MP4 tags (M4A, AAC)
- Basic audio properties (duration, bitrate, sample rate)
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class AudioMetadata:
    """Audio file metadata"""
    
    # Basic properties
    duration_seconds: float | None = None
    bitrate: int | None = None
    sample_rate: int | None = None
    channels: int | None = None
    
    # Tags
    title: str | None = None
    artist: str | None = None
    album: str | None = None
    album_artist: str | None = None
    genre: str | None = None
    year: int | None = None
    track_number: int | None = None
    disc_number: int | None = None
    composer: str | None = None
    comment: str | None = None
    
    # Format
    format: str | None = None
    codec: str | None = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "duration_seconds": self.duration_seconds,
            "bitrate": self.bitrate,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "album_artist": self.album_artist,
            "genre": self.genre,
            "year": self.year,
            "track_number": self.track_number,
            "disc_number": self.disc_number,
            "composer": self.composer,
            "comment": self.comment,
            "format": self.format,
            "codec": self.codec,
        }


def extract_audio_metadata(file_path: Path | str) -> AudioMetadata:
    """
    Extract metadata from audio file
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Audio metadata
    """
    file_path = Path(file_path)
    metadata = AudioMetadata()
    
    try:
        # Try mutagen (best option)
        import mutagen
        
        audio = mutagen.File(file_path)
        
        if audio is None:
            logger.warning(f"Could not read audio file: {file_path}")
            return metadata
        
        # Extract basic properties
        info = audio.info
        metadata.duration_seconds = getattr(info, "length", None)
        metadata.bitrate = getattr(info, "bitrate", None)
        metadata.sample_rate = getattr(info, "sample_rate", None)
        metadata.channels = getattr(info, "channels", None)
        
        # Extract tags (handle different tag formats)
        tags = audio.tags
        
        if tags:
            # Try common tag fields
            metadata.title = _get_tag(tags, ["TIT2", "title", "\xa9nam"])
            metadata.artist = _get_tag(tags, ["TPE1", "artist", "\xa9ART"])
            metadata.album = _get_tag(tags, ["TALB", "album", "\xa9alb"])
            metadata.album_artist = _get_tag(tags, ["TPE2", "albumartist", "aART"])
            metadata.genre = _get_tag(tags, ["TCON", "genre", "\xa9gen"])
            metadata.comment = _get_tag(tags, ["COMM", "comment", "\xa9cmt"])
            metadata.composer = _get_tag(tags, ["TCOM", "composer", "\xa9wrt"])
            
            # Year
            year_str = _get_tag(tags, ["TDRC", "date", "\xa9day"])
            if year_str:
                try:
                    metadata.year = int(str(year_str)[:4])
                except (ValueError, TypeError):
                    pass
            
            # Track number
            track_str = _get_tag(tags, ["TRCK", "tracknumber", "trkn"])
            if track_str:
                try:
                    # Handle "1/12" format
                    metadata.track_number = int(str(track_str).split("/")[0])
                except (ValueError, TypeError):
                    pass
            
            # Disc number
            disc_str = _get_tag(tags, ["TPOS", "discnumber", "disk"])
            if disc_str:
                try:
                    metadata.disc_number = int(str(disc_str).split("/")[0])
                except (ValueError, TypeError):
                    pass
        
        # Format information
        metadata.format = file_path.suffix.lstrip(".")
        metadata.codec = type(audio).__name__
        
    except ImportError:
        logger.warning("mutagen not installed, metadata extraction limited")
        metadata.format = file_path.suffix.lstrip(".")
    
    except Exception as e:
        logger.error(f"Error extracting audio metadata: {e}")
    
    return metadata


def _get_tag(tags: Any, keys: list[str]) -> str | None:
    """
    Get tag value from multiple possible keys
    
    Args:
        tags: Tags object
        keys: List of possible key names
        
    Returns:
        Tag value or None
    """
    for key in keys:
        try:
            if key in tags:
                value = tags[key]
                # Handle different tag formats
                if hasattr(value, "text"):
                    # ID3 tags
                    return str(value.text[0]) if value.text else None
                elif isinstance(value, (list, tuple)):
                    # Vorbis comments
                    return str(value[0]) if value else None
                else:
                    return str(value)
        except (KeyError, IndexError, AttributeError):
            continue
    
    return None


def get_audio_duration(file_path: Path | str) -> float | None:
    """
    Get audio duration in seconds
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Duration in seconds or None
    """
    metadata = extract_audio_metadata(file_path)
    return metadata.duration_seconds


def format_duration(seconds: float) -> str:
    """
    Format duration as MM:SS or HH:MM:SS
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def is_audio_file(file_path: Path | str) -> bool:
    """
    Check if file is an audio file based on extension
    
    Args:
        file_path: Path to file
        
    Returns:
        True if audio file
    """
    audio_extensions = {
        ".mp3", ".m4a", ".aac", ".ogg", ".opus", ".flac",
        ".wav", ".wma", ".aiff", ".ape", ".wv"
    }
    
    return Path(file_path).suffix.lower() in audio_extensions
