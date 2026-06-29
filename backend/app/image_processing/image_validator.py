"""
Image Validator Module for SecureStego

This module validates uploaded image files to ensure they meet the
requirements for steganography operations.

Why Validation is Important:
- Prevents processing of corrupted or invalid images
- Ensures only supported formats are accepted
- Detects malformed files that could cause errors
- Provides clear error messages for unsupported formats
- Improves security by rejecting potentially malicious files

Supported Formats:
- PNG (lossless, ideal for steganography)
- JPG/JPEG (will be converted to PNG)
- HEIC (will be converted to PNG)
"""

import os
import logging
from typing import Tuple, Optional
from PIL import Image, UnidentifiedImageError
import imghdr

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageValidator:
    """
    Validates image files for steganography operations.
    
    Why this exists:
    - Ensures only valid images are processed
    - Detects corrupted or malformed files early
    - Validates file extensions match actual content
    - Provides detailed error messages for debugging
    - Prevents security issues from malicious files
    
    Security Considerations:
    - Validates both file extension and actual file content
    - Detects file type spoofing (e.g., .exe renamed to .png)
    - Checks for corrupted image data
    - Validates image dimensions are reasonable
    - Rejects files that exceed size limits
    """
    
    # Supported file extensions
    SUPPORTED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.heic', '.heif']
    
    # Maximum allowed image dimensions (to prevent DoS)
    MAX_WIDTH = 10000
    MAX_HEIGHT = 10000
    
    # Maximum allowed file size in bytes (10 MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # Minimum allowed image dimensions
    MIN_WIDTH = 10
    MIN_HEIGHT = 10
    
    def __init__(self):
        """Initialize the.image validator."""
        logger.info("ImageValidator initialized")
    
    def validate_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Perform comprehensive validation on an image file.
        
        This method:
        1. Checks if file exists
        2. Validates file extension
        3. Validates file size
        4. Validates file is actually an image
        5. Validates image can be opened
        6. Validates image dimensions
        
        Parameters:
        file_path (str):
            Path to the image file to validate.
            
        Returns:
        Tuple[bool, Optional[str]]:
            - True if validation passes, False otherwise
            - Error message if validation fails, None otherwise
        """
        try:
            logger.info(f"Validating image file: {file_path}")
            
            # Check file exists
            if not os.path.exists(file_path):
                error_msg = f"File does not exist: {file_path}"
                logger.error(error_msg)
                return False, error_msg
            
            # Check file extension
            ext_valid, ext_error = self._validate_extension(file_path)
            if not ext_valid:
                return False, ext_error
            
            # Check file size
            size_valid, size_error = self._validate_file_size(file_path)
            if not size_valid:
                return False, size_error
            
            # Check file is actually an image
            image_valid, image_error = self._validate_image_content(file_path)
            if not image_valid:
                return False, image_error
            
            # Check image can be opened
            open_valid, open_error = self._validate_image_openable(file_path)
            if not open_valid:
                return False, open_error
            
            # Check image dimensions
            dim_valid, dim_error = self._validate_image_dimensions(file_path)
            if not dim_valid:
                return False, dim_error
            
            logger.info(f"Image validation passed: {file_path}")
            return True, None
            
        except Exception as e:
            error_msg = f"Unexpected validation error: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def _validate_extension(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate the file extension is supported.
        
        Parameters:
        file_path (str):
            Path to the image file.
            
        Returns:
        Tuple[bool, Optional[str]]:
            - True if extension is valid, False otherwise
            - Error message if invalid, None otherwise
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext not in self.SUPPORTED_EXTENSIONS:
            error_msg = (
                f"Unsupported file extension: {ext}. "
                f"Supported formats: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )
            logger.error(error_msg)
            return False, error_msg
        
        logger.info(f"Extension validation passed: {ext}")
        return True, None
    
    def _validate_file_size(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate the file size is within acceptable limits.
        
        Parameters:
        file_path (str):
            Path to the image file.
            
        Returns:
        Tuple[bool, Optional[str]]:
            - True if size is valid, False otherwise
            - Error message if invalid, None otherwise
        """
        file_size = os.path.getsize(file_path)
        
        if file_size == 0:
            error_msg = "File is empty"
            logger.error(error_msg)
            return False, error_msg
        
        if file_size > self.MAX_FILE_SIZE:
            error_msg = (
                f"File size exceeds maximum allowed size. "
                f"Size: {file_size} bytes, Maximum: {self.MAX_FILE_SIZE} bytes"
            )
            logger.error(error_msg)
            return False, error_msg
        
        logger.info(f"File size validation passed: {file_size} bytes")
        return True, None
    
    def _validate_image_content(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate the file actually contains image data.
        
        This uses imghdr to detect the actual file type,
        preventing file type spoofing attacks.
        
        Parameters:
        file_path (str):
            Path to the image file.
            
        Returns:
        Tuple[bool, Optional[str]]:
            - True if file contains valid image data, False otherwise
            - Error message if invalid, None otherwise
        """
        try:
            # Detect actual file type
            detected_type = imghdr.what(file_path)
            
            if detected_type is None:
                error_msg = "File does not contain valid image data"
                logger.error(error_msg)
                return False, error_msg
            
            # Map detected types to our supported types
            supported_types = ['png', 'jpeg', 'rgb', 'heic']
            if detected_type not in supported_types:
                error_msg = (
                    f"Detected image type '{detected_type}' is not supported. "
                    f"Supported types: {', '.join(supported_types)}"
                )
                logger.error(error_msg)
                return False, error_msg
            
            logger.info(f"Image content validation passed: {detected_type}")
            return True, None
            
        except Exception as e:
            error_msg = f"Error detecting image content: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def _validate_image_openable(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate the image can be opened by PIL.
        
        This ensures the image is not corrupted and can be processed.
        
        Parameters:
        file_path (str):
            Path to the image file.
            
        Returns:
        Tuple[bool, Optional[str]]:
            - True if image can be opened, False otherwise
            - Error message if invalid, None otherwise
        """
        try:
            with Image.open(file_path) as img:
                # Just opening is enough to validate
                img.verify()
            
            # Re-open after verify (verify closes the file)
            with Image.open(file_path) as img:
                pass
            
            logger.info(f"Image openable validation passed")
            return True, None
            
        except UnidentifiedImageError:
            error_msg = "File is not a valid or supported image format"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Error opening image: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def _validate_image_dimensions(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate the image dimensions are within acceptable limits.
        
        Parameters:
        file_path (str):
            Path to the image file.
            
        Returns:
        Tuple[bool, Optional[str]]:
            - True if dimensions are valid, False otherwise
            - Error message if invalid, None otherwise
        """
        try:
            with Image.open(file_path) as img:
                width, height = img.size
            
            if width < self.MIN_WIDTH or height < self.MIN_HEIGHT:
                error_msg = (
                    f"Image dimensions too small. "
                    f"Minimum: {self.MIN_WIDTH}x{self.MIN_HEIGHT}, "
                    f"Actual: {width}x{height}"
                )
                logger.error(error_msg)
                return False, error_msg
            
            if width > self.MAX_WIDTH or height > self.MAX_HEIGHT:
                error_msg = (
                    f"Image dimensions too large. "
                    f"Maximum: {self.MAX_WIDTH}x{self.MAX_HEIGHT}, "
                    f"Actual: {width}x{height}"
                )
                logger.error(error_msg)
                return False, error_msg
            
            logger.info(f"Image dimensions validation passed: {width}x{height}")
            return True, None
            
        except Exception as e:
            error_msg = f"Error validating image dimensions: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def get_file_info(self, file_path: str) -> dict:
        """
        Get detailed information about an image file.
        
        Parameters:
        file_path (str):
            Path to the image file.
            
        Returns:
        dict: Dictionary containing file information.
        """
        try:
            with Image.open(file_path) as img:
                info = {
                    'path': file_path,
                    'extension': os.path.splitext(file_path)[1].lower(),
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'fileSize': os.path.getsize(file_path),
                    'hasTransparency': img.mode in ('RGBA', 'LA', 'PA') or 'transparency' in img.info,
                    'bands': len(img.getbands()) if hasattr(img, 'getbands') else 0
                }
            
            logger.info(f"File info retrieved: {info}")
            return info
            
        except Exception as e:
            logger.error(f"Error getting file info: {e}")
            raise


# Global image validator instance
image_validator = ImageValidator()
