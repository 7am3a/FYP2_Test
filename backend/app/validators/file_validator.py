"""
File Validator for SecureStego

Validates uploaded files for steganography operations.
"""

from typing import Tuple
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class FileValidator:
    """
    Validates file uploads for steganography operations.
    
    Why this exists:
    - Centralizes file validation logic
    - Ensures consistent validation across all endpoints
    - Provides clear error messages for invalid files
    - Supports future extension with additional validation rules
    """
    
    ALLOWED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.heic', '.heif']
    ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov']
    ALLOWED_AUDIO_EXTENSIONS = ['.wav', '.mp3', '.m4a', '.flac']
    ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.txt']
    
    MAX_FILE_SIZE_MB = 100
    MAX_IMAGE_SIZE_MB = 50
    MAX_VIDEO_SIZE_MB = 500
    MAX_AUDIO_SIZE_MB = 100
    MAX_DOCUMENT_SIZE_MB = 50
    
    @classmethod
    def validate_image_file(cls, filename: str, size: int) -> Tuple[bool, str]:
        """
        Validate an image file.
        
        Parameters:
        filename (str): Name of the file.
        size (int): Size of the file in bytes.
        
        Returns:
        Tuple[bool, str]: (is_valid, error_message)
        """
        ext = filename.lower().split('.')[-1]
        if f'.{ext}' not in cls.ALLOWED_IMAGE_EXTENSIONS:
            return False, f"Unsupported image format. Allowed: {', '.join(cls.ALLOWED_IMAGE_EXTENSIONS)}"
        
        size_mb = size / (1024 * 1024)
        if size_mb > cls.MAX_IMAGE_SIZE_MB:
            return False, f"Image size exceeds limit of {cls.MAX_IMAGE_SIZE_MB}MB"
        
        return True, ""
    
    @classmethod
    def validate_video_file(cls, filename: str, size: int) -> Tuple[bool, str]:
        """Validate a video file."""
        ext = filename.lower().split('.')[-1]
        if f'.{ext}' not in cls.ALLOWED_VIDEO_EXTENSIONS:
            return False, f"Unsupported video format. Allowed: {', '.join(cls.ALLOWED_VIDEO_EXTENSIONS)}"
        
        size_mb = size / (1024 * 1024)
        if size_mb > cls.MAX_VIDEO_SIZE_MB:
            return False, f"Video size exceeds limit of {cls.MAX_VIDEO_SIZE_MB}MB"
        
        return True, ""
