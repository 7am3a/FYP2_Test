"""
Image Loader Module for SecureStego

This module handles loading image pixel data for steganography operations.

Why This Module Exists:
- Provides a clean interface for loading image pixel data
- Ensures images are loaded in the correct format for processing
- Handles both grayscale and color images consistently
- Provides pixel access methods for embedding/extraction
- Isolates image loading logic from steganography logic

Supported Operations:
- Load PNG images as numpy arrays
- Access individual pixels
- Access pixel channels (R, G, B)
- Get image metadata (dimensions, mode, etc.)
"""

import cv2
import numpy as np
import logging
from typing import Tuple, Optional, Dict
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageLoader:
    """
    Loads and provides access to image pixel data.
    
    Why this exists:
    - Encapsulates image loading logic
    - Provides consistent interface for pixel access
    - Handles different image formats (RGB, RGBA, grayscale)
    - Converts images to format suitable for steganography
    - Provides metadata for capacity calculations
    
    Security Considerations:
    - Validates image before loading
    - Ensures images are in correct format (BGR for OpenCV)
    - Handles errors gracefully without exposing internals
    - Logs all operations for audit trail
    """
    
    def __init__(self):
        """Initialize the image loader."""
        logger.info("ImageLoader initialized")
    
    def load_image(self, image_path: str) -> np.ndarray:
        """
        Load an image file as a numpy array.
        
        This method:
        1. Loads the image using OpenCV
        2. Preserves alpha channel if present (IMREAD_UNCHANGED)
        3. Returns the image array (BGR or BGRA format)
        
        Parameters:
        image_path (str):
            Path to the PNG image file.
            
        Returns:
        np.ndarray: Image array in BGR or BGRA format.
            
        Raises:
        IOError: If image cannot be loaded.
        """
        try:
            logger.info(f"Loading image: {image_path}")
            
            # Load image using OpenCV with IMREAD_UNCHANGED to preserve alpha channel
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            
            if image is None:
                raise IOError(f"Failed to load image: {image_path}")
            
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            logger.info(f"Image loaded: {width}x{height}, shape: {image.shape}, channels: {channels}")
            
            return image
            
        except Exception as e:
            logger.error(f"Image loading error: {e}")
            raise IOError(f"Failed to load image: {e}")
    
    def load_image_pil(self, image_path: str) -> Image.Image:
        """
        Load an image file using PIL.
        
        This is useful for metadata extraction and format conversion.
        
        Parameters:
        image_path (str):
            Path to the image file.
            
        Returns:
        Image.Image: PIL Image object.
            
        Raises:
        IOError: If image cannot be loaded.
        """
        try:
            logger.info(f"Loading image with PIL: {image_path}")
            
            image = Image.open(image_path)
            
            logger.info(f"PIL image loaded: {image.format}, {image.mode}, {image.size}")
            
            return image
            
        except Exception as e:
            logger.error(f"PIL image loading error: {e}")
            raise IOError(f"Failed to load image with PIL: {e}")
    
    def get_pixel(self, image: np.ndarray, row: int, col: int) -> np.ndarray:
        """
        Get a single pixel from the image.
        
        Parameters:
        image (np.ndarray):
            Image array.
        row (int):
            Row coordinate of the pixel.
        col (int):
            Column coordinate of the pixel.
            
        Returns:
        np.ndarray: Pixel values (BGR format for color images).
            
        Raises:
        IndexError: If coordinates are out of bounds.
        """
        try:
            pixel = image[row, col]
            return pixel
        except IndexError as e:
            logger.error(f"Pixel access out of bounds: row={row}, col={col}")
            raise IndexError(f"Pixel coordinates out of bounds: {e}")
    
    def set_pixel(self, image: np.ndarray, row: int, col: int, pixel: np.ndarray) -> None:
        """
        Set a single pixel in the image.
        
        Parameters:
        image (np.ndarray):
            Image array (modified in-place).
        row (int):
            Row coordinate of the pixel.
        col (int):
            Column coordinate of the pixel.
        pixel (np.ndarray):
            New pixel values (BGR format).
            
        Raises:
        IndexError: If coordinates are out of bounds.
        """
        try:
            image[row, col] = pixel
        except IndexError as e:
            logger.error(f"Pixel set out of bounds: row={row}, col={col}")
            raise IndexError(f"Pixel coordinates out of bounds: {e}")
    
    def get_channel(self, pixel: np.ndarray, channel: int) -> int:
        """
        Get a specific channel value from a pixel.
        
        Parameters:
        pixel (np.ndarray):
            Pixel values (BGR format).
        channel (int):
            Channel index (0=B, 1=G, 2=R).
            
        Returns:
        int: Channel value (0-255).
            
        Raises:
        IndexError: If channel index is invalid.
        """
        try:
            return pixel[channel]
        except IndexError as e:
            logger.error(f"Invalid channel index: {channel}")
            raise IndexError(f"Channel index out of bounds: {e}")
    
    def set_channel(self, pixel: np.ndarray, channel: int, value: int) -> None:
        """
        Set a specific channel value in a pixel.
        
        Parameters:
        pixel (np.ndarray):
            Pixel values (modified in-place).
        channel (int):
            Channel index (0=B, 1=G, 2=R).
        value (int):
            New channel value (0-255).
            
        Raises:
        IndexError: If channel index is invalid.
        ValueError: If value is out of range.
        """
        try:
            if value < 0 or value > 255:
                raise ValueError(f"Channel value out of range: {value}")
            pixel[channel] = value
        except IndexError as e:
            logger.error(f"Invalid channel index: {channel}")
            raise IndexError(f"Channel index out of bounds: {e}")
    
    def get_image_metadata(self, image_path: str) -> Dict:
        """
        Get comprehensive metadata about an image.
        
        Parameters:
        image_path (str):
            Path to the image file.
            
        Returns:
        Dict: Dictionary containing image metadata.
        """
        try:
            logger.info(f"Getting image metadata: {image_path}")
            
            # Load with OpenCV
            cv_image = cv2.imread(image_path)
            if cv_image is None:
                raise IOError(f"Failed to load image: {image_path}")
            
            height, width = cv_image.shape[:2]
            channels = cv_image.shape[2] if len(cv_image.shape) == 3 else 1
            
            # Load with PIL for additional info
            pil_image = Image.open(image_path)
            
            metadata = {
                'path': image_path,
                'width': width,
                'height': height,
                'channels': channels,
                'totalPixels': width * height,
                'format': pil_image.format,
                'mode': pil_image.mode,
                'sizeBytes': len(cv_image.tobytes()),
                'dtype': str(cv_image.dtype)
            }
            
            logger.info(f"Image metadata: {metadata}")
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error getting image metadata: {e}")
            raise
    
    def is_color_image(self, image: np.ndarray) -> bool:
        """
        Check if an image is color (not grayscale).
        
        Parameters:
        image (np.ndarray):
            Image array.
            
        Returns:
        bool: True if color image, False if grayscale.
        """
        return len(image.shape) == 3 and image.shape[2] == 3
    
    def is_grayscale_image(self, image: np.ndarray) -> bool:
        """
        Check if an image is grayscale.
        
        Parameters:
        image (np.ndarray):
            Image array.
            
        Returns:
        bool: True if grayscale image, False if color.
        """
        return len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1)
    
    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Convert a color image to grayscale.
        
        Parameters:
        image (np.ndarray):
            Color image array (BGR format).
            
        Returns:
        np.ndarray: Grayscale image array.
        """
        try:
            logger.info("Converting image to grayscale")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            logger.info(f"Grayscale conversion complete: {gray.shape}")
            return gray
        except Exception as e:
            logger.error(f"Grayscale conversion error: {e}")
            raise
    
    def convert_to_color(self, image: np.ndarray) -> np.ndarray:
        """
        Convert a grayscale image to color (BGR).
        
        Parameters:
        image (np.ndarray):
            Grayscale image array.
            
        Returns:
        np.ndarray: Color image array (BGR format).
        """
        try:
            logger.info("Converting image to color")
            color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            logger.info(f"Color conversion complete: {color.shape}")
            return color
        except Exception as e:
            logger.error(f"Color conversion error: {e}")
            raise


# Global image loader instance
image_loader = ImageLoader()
