"""
Image Converter Module for SecureStego

This module handles image format conversion to ensure all steganography
operations are performed on PNG images, which support lossless compression
and are ideal for LSB steganography.

Supported Input Formats:
- PNG (no conversion needed)
- JPG/JPEG (converted to PNG)
- HEIC (converted to PNG)

Output Format:
- PNG (always)
"""

import os
import logging
from PIL import Image
from typing import Tuple, Optional
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageConverter:
    """
    Converts various image formats to PNG for steganography operations.
    
    Why this exists:
    - PNG uses lossless compression, preserving pixel values exactly
    - JPG/JPEG use lossy compression, which corrupts LSB data
    - HEIC is a modern format that needs conversion for compatibility
    - All steganography operations require consistent pixel access
    
    Security Considerations:
    - Conversion is done in-memory when possible
    - Temporary files are cleaned up after use
    - Original image quality is preserved during conversion
    """
    
    # Supported input formats
    SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.heic', '.heif']
    
    # Output format (always PNG)
    OUTPUT_FORMAT = 'PNG'
    
    def __init__(self):
        """Initialize the image converter."""
        logger.info("ImageConverter initialized")
    
    def is_supported_format(self, file_path: str) -> bool:
        """
        Check if the image format is supported for conversion.
        
        Parameters:
        file_path (str):
            Path to the image file.
            
        Returns:
        bool: True if format is supported, False otherwise.
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.SUPPORTED_FORMATS
    
    def get_image_format(self, file_path: str) -> str:
        """
        Get the image format from file extension.
        
        Parameters:
        file_path (str):
            Path to the image file.
            
        Returns:
        str: Image format (e.g., 'PNG', 'JPEG', 'HEIC').
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        format_map = {
            '.png': 'PNG',
            '.jpg': 'JPEG',
            '.jpeg': 'JPEG',
            '.heic': 'HEIC',
            '.heif': 'HEIC'
        }
        
        return format_map.get(ext, 'UNKNOWN')
    
    def convert_to_png(self, file_path: str) -> Tuple[str, str]:
        """
        Convert an image to PNG format.
        
        This method:
        1. Opens the image file
        2. Converts to PNG if needed
        3. Saves to a temporary file
        4. Returns path to the PNG file
        
        Parameters:
        file_path (str):
            Path to the input image file.
            
        Returns:
        Tuple[str, str]: 
            - Path to the converted PNG file
            - Original format of the image
            
        Raises:
        ValueError: If file format is not supported
        IOError: If image cannot be read or converted
        """
        try:
            logger.info(f"Converting image: {file_path}")
            
            # Check if format is supported
            if not self.is_supported_format(file_path):
                raise ValueError(
                    f"Unsupported image format. "
                    f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
                )
            
            # Get original format
            original_format = self.get_image_format(file_path)
            logger.info(f"Original format: {original_format}")
            
            # Open the image
            with Image.open(file_path) as img:
                original_mode = img.mode
                logger.info(f"Original image mode: {original_mode}")
                
                # Preserve RGBA mode for transparency
                # Only convert if mode is not RGB or RGBA
                if img.mode not in ('RGB', 'RGBA'):
                    # For modes like P, LA, etc., convert to RGBA to preserve transparency
                    if 'A' in img.mode or img.mode == 'P':
                        img = img.convert('RGBA')
                        logger.info(f"Converted image mode to RGBA to preserve transparency")
                    else:
                        img = img.convert('RGB')
                        logger.info(f"Converted image mode to RGB")
                
                # Create temporary file for PNG output
                temp_file = tempfile.NamedTemporaryFile(
                    suffix='.png',
                    delete=False
                )
                temp_path = temp_file.name
                temp_file.close()
                
                # Save as PNG with balanced compression (level 6 for better performance)
                img.save(temp_path, format=self.OUTPUT_FORMAT, compress_level=6)
                logger.info(f"Image converted to PNG with compression level 6: {temp_path}")
                
                return temp_path, original_format
                
        except Exception as e:
            logger.error(f"Image conversion error: {e}")
            raise IOError(f"Failed to convert image to PNG: {e}")
    
    def get_image_dimensions(self, file_path: str) -> Tuple[int, int]:
        """
        Get the dimensions of an image.
        
        Parameters:
        file_path (str):
            Path to the image file.
            
        Returns:
        Tuple[int, int]: Width and height of the image.
        """
        try:
            with Image.open(file_path) as img:
                return img.size
        except Exception as e:
            logger.error(f"Error getting image dimensions: {e}")
            raise IOError(f"Failed to get image dimensions: {e}")
    
    def cleanup_temp_file(self, file_path: str) -> None:
        """
        Clean up temporary files created during conversion.
        
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


# Global image converter instance
image_converter = ImageConverter()
