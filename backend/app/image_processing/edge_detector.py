"""
Edge Detector Module for SecureStego

This module implements Canny edge detection to identify edge pixels
in images for use in edge-based LSB steganography.

Why Edge-Based Steganography:
- Edge regions are less sensitive to visual changes
- Hiding data in edges reduces perceptible distortion
- Improves resistance against simple steganalysis
- Better preserves image quality compared to sequential LSB

Algorithm: Canny Edge Detection
- Multi-stage algorithm for optimal edge detection
- Reduces noise while preserving edges
- Provides accurate edge localization
"""

import cv2
import numpy as np
import logging
from typing import Tuple, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EdgeDetector:
    """
    Detects edge pixels in images using Canny edge detection.
    
    Why this exists:
    - Edge-based LSB steganography requires identifying edge pixels
    - Canny provides the most accurate edge detection
    - Edge pixels are ideal embedding locations due to low visual sensitivity
    - Improves steganography security and image quality
    
    Security Considerations:
    - Edge detection parameters are tuned for balance between sensitivity and noise
    - Edge maps are generated per-image (no pre-computation)
    - Edge detection is deterministic (same image = same edges)
    """
    
    # Canny edge detection parameters
    # These values are tuned for good edge detection on typical images
    # Higher thresholds make edge detection more robust to LSB modifications
    CANNY_THRESHOLD1 = 100  # Lower threshold for edge linking (increased for robustness)
    CANNY_THRESHOLD2 = 200  # Upper threshold for strong edges (increased for robustness)
    CANNY_APERTURE_SIZE = 3  # Sobel operator aperture size
    
    def __init__(self, threshold1: int = None, threshold2: int = None):
        """
        Initialize the edge detector with optional custom thresholds.
        
        Parameters:
        threshold1 (int, optional):
            Lower threshold for Canny edge detection.
        threshold2 (int, optional):
            Upper threshold for Canny edge detection.
        """
        self.threshold1 = threshold1 or self.CANNY_THRESHOLD1
        self.threshold2 = threshold2 or self.CANNY_THRESHOLD2
        logger.info(
            f"EdgeDetector initialized with thresholds: "
            f"{self.threshold1}, {self.threshold2}"
        )
    
    def detect_edges(self, image_path: str, clear_lsb: bool = False) -> np.ndarray:
        """
        Detect edges in an image using Canny edge detection.
        
        This method:
        1. Loads the image preserving alpha channel
        2. Optionally clears LSBs to make edge detection LSB-invariant
        3. Converts to grayscale for edge detection
        4. Applies Gaussian blur to reduce noise
        5. Runs Canny edge detection
        6. Returns binary edge map
        
        Parameters:
        image_path (str):
            Path to the PNG image file.
        clear_lsb (bool):
            If True, clears LSBs before edge detection for LSB-invariance.
            This is useful for extraction to match embedding edge detection.
            
        Returns:
        np.ndarray: Binary edge map (255 for edges, 0 for non-edges).
            
        Raises:
        IOError: If image cannot be loaded
        """
        try:
            logger.info(f"Detecting edges in: {image_path} (clear_lsb={clear_lsb})")
            
            # Load image preserving alpha channel
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            
            if image is None:
                raise IOError(f"Failed to load image: {image_path}")
            
            # Clear LSBs if requested (for LSB-invariant edge detection)
            if clear_lsb and len(image.shape) == 3:
                # Clear LSB of each channel to make edge detection invariant to LSB modifications
                # Use in-place operation to avoid unnecessary copy
                for channel in range(min(3, image.shape[2])):  # Only clear RGB channels, not alpha
                    image[:, :, channel] = image[:, :, channel] & 0xFE
                logger.info("Cleared LSBs for LSB-invariant edge detection")
            
            # Convert to grayscale for edge detection
            # If image has alpha channel, use only RGB channels
            if len(image.shape) == 3 and image.shape[2] == 4:
                # BGRA image - use only BGR channels for edge detection
                image_bgr = image[:, :, :3]
                gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
                logger.info("Edge detection on BGRA image (using BGR channels)")
            elif len(image.shape) == 3 and image.shape[2] == 3:
                # BGR image
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                logger.info("Edge detection on BGR image")
            else:
                # Already grayscale
                gray = image
                logger.info("Edge detection on grayscale image")
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply Canny edge detection
            edges = cv2.Canny(
                blurred,
                self.threshold1,
                self.threshold2,
                apertureSize=self.CANNY_APERTURE_SIZE
            )
            
            logger.info(f"Edge detection completed. Edge pixels: {np.sum(edges > 0)}")
            
            return edges
            
        except Exception as e:
            logger.error(f"Edge detection error: {e}")
            raise IOError(f"Failed to detect edges: {e}")
    
    def get_edge_pixel_coordinates(self, edge_map: np.ndarray) -> List[Tuple[int, int]]:
        """
        Get the coordinates of all edge pixels from the edge map.
        
        Parameters:
        edge_map (np.ndarray):
            Binary edge map from detect_edges().
            
        Returns:
        List[Tuple[int, int]]: List of (row, col) coordinates of edge pixels.
        """
        # Find all pixels where edge value is 255
        edge_pixels = np.where(edge_map == 255)
        
        # Convert to list of (row, col) tuples
        coordinates = list(zip(edge_pixels[0], edge_pixels[1]))
        
        logger.info(f"Found {len(coordinates)} edge pixels")
        
        return coordinates
    
    def get_edge_pixel_count(self, edge_map: np.ndarray) -> int:
        """
        Get the total number of edge pixels in the edge map.
        
        Parameters:
        edge_map (np.ndarray):
            Binary edge map from detect_edges().
            
        Returns:
        int: Number of edge pixels.
        """
        return np.sum(edge_map > 0)
    
    def calculate_capacity(self, edge_map: np.ndarray, bits_per_pixel: int = 1) -> int:
        """
        Calculate the steganography capacity based on edge pixels.
        
        Parameters:
        edge_map (np.ndarray):
            Binary edge map from detect_edges().
        bits_per_pixel (int):
            Number of bits to hide per edge pixel (default: 1 for LSB).
            
        Returns:
        int: Total capacity in bits.
        """
        edge_count = self.get_edge_pixel_count(edge_map)
        capacity_bits = edge_count * bits_per_pixel
        capacity_bytes = capacity_bits // 8
        
        logger.info(
            f"Capacity calculation: {edge_count} edge pixels × "
            f"{bits_per_pixel} bits = {capacity_bits} bits ({capacity_bytes} bytes)"
        )
        
        return capacity_bits
    
    def is_edge_pixel(self, edge_map: np.ndarray, row: int, col: int) -> bool:
        """
        Check if a specific pixel is an edge pixel.
        
        Parameters:
        edge_map (np.ndarray):
            Binary edge map from detect_edges().
        row (int):
            Row coordinate of the pixel.
        col (int):
            Column coordinate of the pixel.
            
        Returns:
        bool: True if pixel is an edge, False otherwise.
        """
        return edge_map[row, col] == 255


# Global edge detector instance
edge_detector = EdgeDetector()
