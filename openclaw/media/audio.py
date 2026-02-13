"""Audio processing utilities

This module provides audio processing capabilities including:
- Audio format conversion
- Audio trimming and splitting
- Volume adjustment
- Audio analysis
"""
from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class AudioProcessingError(Exception):
    """Audio processing error"""
    pass


class AudioProcessor:
    """Audio processing operations using ffmpeg"""
    
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        """
        Initialize audio processor
        
        Args:
            ffmpeg_path: Path to ffmpeg executable
        """
        self.ffmpeg_path = ffmpeg_path
    
    def check_ffmpeg(self) -> bool:
        """
        Check if ffmpeg is available
        
        Returns:
            True if ffmpeg is available
        """
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def convert_audio(
        self,
        input_path: Path | str,
        output_path: Path | str,
        output_format: str | None = None,
        bitrate: str = "128k",
        sample_rate: int | None = None,
    ) -> bool:
        """
        Convert audio to different format
        
        Args:
            input_path: Input audio file
            output_path: Output audio file
            output_format: Output format (mp3, aac, opus, flac, wav)
            bitrate: Audio bitrate (e.g., "128k", "192k")
            sample_rate: Sample rate in Hz (e.g., 44100, 48000)
            
        Returns:
            True if successful
            
        Raises:
            AudioProcessingError: If conversion fails
        """
        if not self.check_ffmpeg():
            raise AudioProcessingError("ffmpeg not available")
        
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        # Determine output format
        if output_format is None:
            output_format = output_path.suffix.lstrip(".")
        
        # Build ffmpeg command
        cmd = [
            self.ffmpeg_path,
            "-i", str(input_path),
            "-b:a", bitrate,
        ]
        
        if sample_rate:
            cmd.extend(["-ar", str(sample_rate)])
        
        # Format-specific options
        if output_format == "mp3":
            cmd.extend(["-codec:a", "libmp3lame"])
        elif output_format == "aac":
            cmd.extend(["-codec:a", "aac"])
        elif output_format == "opus":
            cmd.extend(["-codec:a", "libopus"])
        elif output_format == "flac":
            cmd.extend(["-codec:a", "flac"])
        elif output_format == "wav":
            cmd.extend(["-codec:a", "pcm_s16le"])
        
        cmd.extend(["-y", str(output_path)])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise AudioProcessingError(
                    f"ffmpeg error: {result.stderr.decode('utf-8', errors='ignore')}"
                )
            
            logger.info(f"Converted audio: {input_path} -> {output_path}")
            return True
            
        except subprocess.TimeoutExpired:
            raise AudioProcessingError("Audio conversion timeout")
        except Exception as e:
            raise AudioProcessingError(f"Conversion failed: {e}")
    
    def trim_audio(
        self,
        input_path: Path | str,
        output_path: Path | str,
        start_time: float,
        duration: float | None = None,
        end_time: float | None = None,
    ) -> bool:
        """
        Trim audio file
        
        Args:
            input_path: Input audio file
            output_path: Output audio file
            start_time: Start time in seconds
            duration: Duration in seconds (mutually exclusive with end_time)
            end_time: End time in seconds (mutually exclusive with duration)
            
        Returns:
            True if successful
            
        Raises:
            AudioProcessingError: If trimming fails
        """
        if not self.check_ffmpeg():
            raise AudioProcessingError("ffmpeg not available")
        
        if duration is None and end_time is None:
            raise AudioProcessingError("Either duration or end_time must be specified")
        
        if duration is not None and end_time is not None:
            raise AudioProcessingError("Cannot specify both duration and end_time")
        
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        cmd = [
            self.ffmpeg_path,
            "-i", str(input_path),
            "-ss", str(start_time),
        ]
        
        if duration is not None:
            cmd.extend(["-t", str(duration)])
        else:
            cmd.extend(["-to", str(end_time)])
        
        cmd.extend(["-codec", "copy", "-y", str(output_path)])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise AudioProcessingError(
                    f"ffmpeg error: {result.stderr.decode('utf-8', errors='ignore')}"
                )
            
            logger.info(f"Trimmed audio: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            raise AudioProcessingError(f"Trimming failed: {e}")
    
    def adjust_volume(
        self,
        input_path: Path | str,
        output_path: Path | str,
        volume_db: float,
    ) -> bool:
        """
        Adjust audio volume
        
        Args:
            input_path: Input audio file
            output_path: Output audio file
            volume_db: Volume adjustment in dB (positive = louder, negative = quieter)
            
        Returns:
            True if successful
            
        Raises:
            AudioProcessingError: If adjustment fails
        """
        if not self.check_ffmpeg():
            raise AudioProcessingError("ffmpeg not available")
        
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        cmd = [
            self.ffmpeg_path,
            "-i", str(input_path),
            "-filter:a", f"volume={volume_db}dB",
            "-y", str(output_path)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise AudioProcessingError(
                    f"ffmpeg error: {result.stderr.decode('utf-8', errors='ignore')}"
                )
            
            logger.info(f"Adjusted volume: {input_path} -> {output_path} ({volume_db}dB)")
            return True
            
        except Exception as e:
            raise AudioProcessingError(f"Volume adjustment failed: {e}")
    
    def extract_audio_from_video(
        self,
        input_path: Path | str,
        output_path: Path | str,
        audio_format: str = "mp3",
        bitrate: str = "192k",
    ) -> bool:
        """
        Extract audio track from video file
        
        Args:
            input_path: Input video file
            output_path: Output audio file
            audio_format: Output audio format
            bitrate: Audio bitrate
            
        Returns:
            True if successful
            
        Raises:
            AudioProcessingError: If extraction fails
        """
        if not self.check_ffmpeg():
            raise AudioProcessingError("ffmpeg not available")
        
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        cmd = [
            self.ffmpeg_path,
            "-i", str(input_path),
            "-vn",  # No video
            "-b:a", bitrate,
            "-y", str(output_path)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=600
            )
            
            if result.returncode != 0:
                raise AudioProcessingError(
                    f"ffmpeg error: {result.stderr.decode('utf-8', errors='ignore')}"
                )
            
            logger.info(f"Extracted audio: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            raise AudioProcessingError(f"Audio extraction failed: {e}")
    
    def concatenate_audio(
        self,
        input_paths: list[Path | str],
        output_path: Path | str,
    ) -> bool:
        """
        Concatenate multiple audio files
        
        Args:
            input_paths: List of input audio files
            output_path: Output audio file
            
        Returns:
            True if successful
            
        Raises:
            AudioProcessingError: If concatenation fails
        """
        if not self.check_ffmpeg():
            raise AudioProcessingError("ffmpeg not available")
        
        if len(input_paths) < 2:
            raise AudioProcessingError("At least 2 input files required")
        
        output_path = Path(output_path)
        
        # Create concat file list
        concat_file = output_path.parent / "concat_list.txt"
        with open(concat_file, "w") as f:
            for input_path in input_paths:
                f.write(f"file '{Path(input_path).absolute()}'\n")
        
        cmd = [
            self.ffmpeg_path,
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            "-y", str(output_path)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=600
            )
            
            # Clean up concat file
            concat_file.unlink()
            
            if result.returncode != 0:
                raise AudioProcessingError(
                    f"ffmpeg error: {result.stderr.decode('utf-8', errors='ignore')}"
                )
            
            logger.info(f"Concatenated {len(input_paths)} audio files -> {output_path}")
            return True
            
        except Exception as e:
            # Clean up on error
            if concat_file.exists():
                concat_file.unlink()
            raise AudioProcessingError(f"Concatenation failed: {e}")


# Convenience functions
_default_processor: AudioProcessor | None = None


def get_audio_processor() -> AudioProcessor:
    """Get default audio processor instance"""
    global _default_processor
    if _default_processor is None:
        _default_processor = AudioProcessor()
    return _default_processor


def convert_audio(input_path: Path | str, output_path: Path | str, **kwargs) -> bool:
    """Convert audio file"""
    return get_audio_processor().convert_audio(input_path, output_path, **kwargs)


def trim_audio(input_path: Path | str, output_path: Path | str, **kwargs) -> bool:
    """Trim audio file"""
    return get_audio_processor().trim_audio(input_path, output_path, **kwargs)
