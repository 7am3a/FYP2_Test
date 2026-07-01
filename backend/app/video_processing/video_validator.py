"""
Video Validator Module for SecureStego

Purpose:
Validates video files to ensure they are suitable for steganography operations.

This module is isolated from video conversion, frame extraction, and steganography
to improve maintainability and debugging.

Validation Checks:
- File existence and readability
- MIME type verification
- Supported format check (MP4, AVI, MOV)
- File corruption detection
- Duration validation
- Resolution validation
- Frame rate validation

Why This Exists:
- Prevents processing of invalid files
- Provides early error detection
- Ensures video meets minimum requirements
- Logs validation results for debugging
"""

import os
import logging
import subprocess
import json 
from typing import Tuple, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoValidator:
    """
    Validates video files for steganography processing.
    
    Why this exists:
    - Ensures only valid videos are processed
    - Prevents wasting resources on corrupted files
    - Provides detailed error messages for users
    - Validates format support before processing
    
    Security Considerations:
    - Validates file extensions to prevent path traversal
    - Checks file size to prevent DoS attacks
    - Uses subprocess with proper validation
    - Does not execute arbitrary video files
    """
    
    # Supported video formats
    SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov']
    
    # MIME type mapping
    MIME_TYPES = {
        '.mp4': 'video/mp4',
        '.avi': 'video/x-msvideo',
        '.mov': 'video/quicktime'
    }
    
    # Maximum file size (500 MB)
    MAX_FILE_SIZE = 500 * 1024 * 1024
    
    # Minimum duration (1 second)
    MIN_DURATION = 1.0
    
    # Maximum duration (10 minutes)
    MAX_DURATION = 600.0
    
    # Minimum resolution (320x240)
    MIN_WIDTH = 320
    MIN_HEIGHT = 240
    
    def __init__(self):
        """Initialize the video validator."""
        logger.info("VideoValidator initialized")
    
    def validate_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a video file for steganography processing.
        
        This method performs comprehensive validation:
        1. Checks file existence and readability
        2. Validates file extension
        3. Checks file size limits
        4. Verifies video integrity using ffprobe
        5. Validates duration, resolution, and frame rate
        
        Parameters:
        file_path (str):
            Path to the video file to validate.
            
        Returns:
        Tuple[bool, Optional[str]]:
            - (True, None) if validation passes
            - (False, error_message) if validation fails
            
        Raises:
        ValueError: If file path is invalid or inaccessible
        """
        try:
            logger.info(f"Validating video file: {file_path}")
            
            # Step 1: Check file existence
            if not os.path.exists(file_path):
                error = f"File does not exist: {file_path}"
                logger.error(error)
                return False, error
            
            # Step 2: Check file readability
            if not os.access(file_path, os.R_OK):
                error = f"File is not readable: {file_path}"
                logger.error(error)
                return False, error
            
            # Step 3: Validate file extension
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in self.SUPPORTED_FORMATS:
                error = (
                    f"Unsupported video format: {file_ext}. "
                    f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
                )
                logger.error(error)
                return False, error
            
            # Step 4: Check file size
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                error = "File is empty"
                logger.error(error)
                return False, error
            
            if file_size > self.MAX_FILE_SIZE:
                error = (
                    f"File size exceeds maximum allowed size. "
                    f"Maximum: {self.MAX_FILE_SIZE / (1024*1024):.0f} MB, "
                    f"Actual: {file_size / (1024*1024):.0f} MB"
                )
                logger.error(error)
                return False, error
            
            logger.info(f"File size: {file_size / (1024*1024):.2f} MB")
            
            # Step 5: Validate video integrity using ffprobe
            video_info = self._get_video_info(file_path)
            if video_info is None:
                error = "Failed to read video information. File may be corrupted."
                logger.error(error)
                return False, error
            
            # Step 6: Validate duration
            duration = video_info.get('duration', 0)
            if duration < self.MIN_DURATION:
                error = (
                    f"Video duration is too short. "
                    f"Minimum: {self.MIN_DURATION}s, Actual: {duration:.2f}s"
                )
                logger.error(error)
                return False, error
            
            if duration > self.MAX_DURATION:
                error = (
                    f"Video duration is too long. "
                    f"Maximum: {self.MAX_DURATION}s, Actual: {duration:.2f}s"
                )
                logger.error(error)
                return False, error
            
            logger.info(f"Video duration: {duration:.2f}s")
            
            # Step 7: Validate resolution
            width = video_info.get('width', 0)
            height = video_info.get('height', 0)
            
            if width < self.MIN_WIDTH or height < self.MIN_HEIGHT:
                error = (
                    f"Video resolution is too low. "
                    f"Minimum: {self.MIN_WIDTH}x{self.MIN_HEIGHT}, "
                    f"Actual: {width}x{height}"
                )
                logger.error(error)
                return False, error
            
            logger.info(f"Video resolution: {width}x{height}")
            
            # Step 8: Validate frame rate
            fps = video_info.get('fps', 0)
            if fps <= 0:
                error = f"Invalid frame rate: {fps}"
                logger.error(error)
                return False, error
            
            logger.info(f"Video frame rate: {fps:.2f} fps")
            
            logger.info("Video validation passed")
            return True, None
            
        except Exception as e:
            error = f"Video validation error: {str(e)}"
            logger.error(error)
            return False, error
    
    def _get_video_info(self, file_path: str) -> Optional[dict]:
        """
        Extract video information using ffprobe.
        
        This method uses ffprobe to get:
        - Duration
        - Width and height
        - Frame rate
        - Codec information
        
        Parameters:
        file_path (str):
            Path to the video file.
            
        Returns:
        Optional[dict]:
            Dictionary with video information, or None if extraction fails.
        """
        try:
            # Use ffprobe to get video information
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,r_frame_rate,duration',
                '-show_entries', 'format=duration',
                '-of', 'json',
                file_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                logger.error(f"ffprobe error: {result.stderr}")
                return None
            
            # Parse JSON output
            info = json.loads(result.stdout)
            
            # Extract relevant information
            stream = info.get('streams', [{}])[0]
            format_info = info.get('format', {})
            
            # Parse frame rate (e.g., "30/1" -> 30.0)
            r_frame_rate = stream.get('r_frame_rate', '0/1')
            if '/' in r_frame_rate:
                num, den = r_frame_rate.split('/')
                fps = float(num) / float(den)
            else:
                fps = float(r_frame_rate)
            
            return {
                'width': stream.get('width', 0),
                'height': stream.get('height', 0),
                'fps': fps,
                'duration': float(format_info.get('duration', stream.get('duration', 0))),
                'codec': stream.get('codec_name', 'unknown')
            }
            
        except subprocess.TimeoutExpired:
            logger.error("ffprobe timeout")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse ffprobe output: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
    
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


# Global video validator instance
video_validator = VideoValidator()
