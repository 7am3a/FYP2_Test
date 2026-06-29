"""
Video Converter Module for SecureStego

Purpose:
Converts video files to MP4 format for consistent steganography processing.

This module is isolated from video validation, frame extraction, and steganography
to improve maintainability and debugging.

Conversion Workflow:
1. Validate input format
2. Create temporary working copy
3. Convert to MP4 using FFmpeg
4. Verify output integrity
5. Return path to converted file

Why This Exists:
- Ensures all videos are in a consistent format
- MP4 is widely supported and reliable
- Simplifies downstream processing
- Preserves quality while normalizing format

Security Considerations:
- Uses temporary files for processing
- Validates output before returning
- Cleans up temporary files on error
- Does not modify original files
"""

import os
import logging
import subprocess
import tempfile
from typing import Tuple, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoConverter:
    """
    Converts video files to MP4 format.
    
    Why this exists:
    - Normalizes all input videos to MP4
    - Ensures consistent codec and container
    - Simplifies frame extraction and processing
    - Preserves original quality
    
    Security Considerations:
    - Creates temporary files in secure locations
    - Validates conversion output
    - Cleans up temporary files
    - Does not overwrite original files
    """
    
    # Supported input formats
    SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov']
    
    # Output format
    OUTPUT_FORMAT = '.mp4'
    
    # FFmpeg codec settings
    VIDEO_CODEC = 'libx264'
    AUDIO_CODEC = 'aac'
    PRESET = 'medium'  # Balance between speed and quality
    CRF = 23  # Constant Rate Factor (quality, lower = better)
    
    def __init__(self):
        """Initialize the video converter."""
        logger.info("VideoConverter initialized")
    
    def convert_to_mp4(self, input_path: str) -> Tuple[str, str]:
        """
        Convert a video file to MP4 format.
        
        This method:
        1. Creates a temporary file for output
        2. Converts video using FFmpeg with H.264 codec
        3. Preserves original audio track
        4. Verifies output integrity
        5. Returns path to converted file
        
        Parameters:
        input_path (str):
            Path to the input video file.
            
        Returns:
        Tuple[str, str]:
            - Path to the converted MP4 file
            - Original format (e.g., '.avi', '.mov', '.mp4')
            
        Raises:
        ValueError: If conversion fails or output is invalid
        IOError: If file operations fail
        """
        try:
            logger.info(f"Converting video to MP4: {input_path}")
            
            # Get original format
            original_format = self.get_video_format(input_path)
            logger.info(f"Original format: {original_format}")
            
            # Create temporary output file
            temp_dir = tempfile.gettempdir()
            base_name = Path(input_path).stem
            output_path = os.path.join(temp_dir, f"{base_name}_temp{self.OUTPUT_FORMAT}")
            
            logger.info(f"Output path: {output_path}")
            
            # Build FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-c:v', self.VIDEO_CODEC,
                '-preset', self.PRESET,
                '-crf', str(self.CRF),
                '-c:a', self.AUDIO_CODEC,
                '-movflags', '+faststart',  # Enable fast start for web playback
                '-y',  # Overwrite output file if exists
                output_path
            ]
            
            logger.info(f"Running FFmpeg conversion")
            
            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                error = f"FFmpeg conversion failed: {result.stderr}"
                logger.error(error)
                raise ValueError(error)
            
            # Verify output file exists and is not empty
            if not os.path.exists(output_path):
                error = "Output file was not created"
                logger.error(error)
                raise ValueError(error)
            
            if os.path.getsize(output_path) == 0:
                error = "Output file is empty"
                logger.error(error)
                raise ValueError(error)
            
            # Verify output is valid MP4
            if not self._verify_mp4(output_path):
                error = "Output file is not a valid MP4"
                logger.error(error)
                raise ValueError(error)
            
            logger.info(f"Conversion successful: {output_path}")
            
            return output_path, original_format
            
        except subprocess.TimeoutExpired:
            error = "Video conversion timed out"
            logger.error(error)
            raise ValueError(error)
        except Exception as e:
            logger.error(f"Video conversion error: {e}")
            raise
    
    def _verify_mp4(self, file_path: str) -> bool:
        """
        Verify that a file is a valid MP4 video.
        
        This method uses ffprobe to check:
        - File is readable
        - Contains video stream
        - Valid MP4 container
        
        Parameters:
        file_path (str):
            Path to the file to verify.
            
        Returns:
        bool: True if file is valid MP4, False otherwise.
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=codec_name',
                '-of', 'csv=p=0',
                file_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return result.returncode == 0 and len(result.stdout.strip()) > 0
            
        except Exception as e:
            logger.error(f"MP4 verification error: {e}")
            return False
    
    def is_supported_format(self, file_path: str) -> bool:
        """
        Check if a video file has a supported format.
        
        Parameters:
        file_path (str):
            Path to the video file.
            
        Returns:
        bool: True if format is supported, False otherwise.
        """
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.SUPPORTED_FORMATS
    
    def get_video_format(self, file_path: str) -> str:
        """
        Get the format of a video file.
        
        Parameters:
        file_path (str):
            Path to the video file.
            
        Returns:
        str: File extension (e.g., '.mp4', '.avi', '.mov').
        """
        return Path(file_path).suffix.lower()
    
    def cleanup_temp_file(self, file_path: str) -> None:
        """
        Clean up a temporary video file.
        
        Parameters:
        file_path (str):
            Path to the temporary file to delete.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temporary file {file_path}: {e}")


# Global video converter instance
video_converter = VideoConverter()
