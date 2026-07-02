"""
Edge-Based LSB Extractor Module for SecureStego

This module implements the extraction logic for retrieving hidden data
from edge pixels of an image using Least Significant Bit (LSB) steganography.

Extraction Process:
1. Load stego PNG image pixels
2. Get edge pixel coordinates from edge detector
3. Extract payload length header from LSBs
4. Extract payload data from LSBs
5. Return extracted binary data
"""

import cv2
import numpy as np
import logging
from typing import Tuple
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EdgeLSBExtractor:
    """
    Extracts hidden payload from edge pixels using Edge-Based LSB steganography.
    
    Why this exists:
    - Implements the core extraction algorithm
    - Reads data only from edge pixels (matching embedder)
    - Handles payload length header for proper extraction
    - Validates extracted data integrity
    
    Security Considerations:
    - Extraction is deterministic (same image = same extracted data)
    - Only reads LSB of edge pixels
    - Validates payload length before extraction
    - Handles corrupted or invalid data gracefully
    """
    
    # Number of bits to extract per pixel (1 LSB per channel = 3 bits per pixel)
    BITS_PER_PIXEL = 3
    
    # Size of payload length header in bytes
    HEADER_SIZE = 4
    
    def __init__(self):
        """Initialize the edge LSB extractor."""
        logger.info("EdgeLSBExtractor initialized")
    
    def extract(
        self,
        image_path: str,
        edge_coordinates: list
    ) -> Tuple[bytes, dict]:
        """
        Extract payload from edge pixels of the stego image.
        
        This method:
        1. Loads the stego PNG image
        2. Extracts payload length header
        3. Extracts payload data based on length
        4. Returns extracted binary data
        
        Parameters:
        image_path (str):
            Path to the stego PNG image file.
        edge_coordinates (list):
            List of (row, col) tuples for edge pixels.
            
        Returns:
        Tuple[bytes, dict]:
            - Extracted binary payload data
            - Dictionary with extraction statistics
            
        Raises:
        ValueError: If image is corrupted or data cannot be extracted
        IOError: If image cannot be loaded
        """
        try:
            logger.info(f"Starting extraction process for: {image_path}")
            
            # Load stego image preserving alpha channel
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise IOError(f"Failed to load image: {image_path}")
            
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            has_alpha = channels == 4
            logger.info(f"Stego image loaded: {width}x{height}, channels: {channels}, has_alpha: {has_alpha}")
            
            # Extract all available bits from edge pixels (matching embedder behavior)
            max_possible_bits = len(edge_coordinates) * self.BITS_PER_PIXEL
            all_bits = self._extract_bits(image, edge_coordinates, max_possible_bits)
            
            # Extract header (payload length) from first 32 bits
            header_bits = all_bits[:self.HEADER_SIZE * 8]
            header_bytes = self._bits_to_bytes(header_bits)
            payload_length = struct.unpack('>I', header_bytes)[0]
            
            logger.info(f"Extracted payload length: {payload_length} bytes")
            
            # Validate payload length
            if payload_length <= 0 or payload_length > (len(edge_coordinates) * self.BITS_PER_PIXEL) // 8:
                raise ValueError(
                    f"Invalid payload length: {payload_length}. "
                    f"Image may be corrupted or not contain hidden data."
                )
            
            # Extract payload data from remaining bits (after header)
            payload_start_bit = self.HEADER_SIZE * 8
            payload_end_bit = payload_start_bit + (payload_length * 8)
            payload_bits = all_bits[payload_start_bit:payload_end_bit]
            payload = self._bits_to_bytes(payload_bits)
            
            logger.info(f"Extracted payload: {len(payload)} bytes")
            
            # Calculate statistics
            stats = {
                'imageWidth': width,
                'imageHeight': height,
                'totalPixels': width * height,
                'edgePixels': len(edge_coordinates),
                'payloadSize': len(payload),
                'headerSize': self.HEADER_SIZE,
                'totalBitsExtracted': (self.HEADER_SIZE + len(payload)) * 8
            }
            
            logger.info(f"Extraction completed successfully. Stats: {stats}")
            
            return payload, stats
            
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            raise
    
    def _extract_bits(
        self,
        image: np.ndarray,
        edge_coordinates: list,
        num_bits: int
    ) -> list:
        """
        Internal method to extract bits from image pixels.
        
        Parameters:
        image (np.ndarray):
            Image array (BGR or BGRA format).
        edge_coordinates (list):
            List of (row, col) tuples for edge pixels.
        num_bits (int):
            Number of bits to extract.
            
        Returns:
        list: List of extracted bits (0 or 1).
        """
        bits = []
        bit_index = 0
        
        for row, col in edge_coordinates:
            if bit_index >= num_bits:
                break
            
            # Get pixel (BGR or BGRA format)
            pixel = image[row, col]
            
            # Extract up to 3 bits (one per RGB channel)
            # Never read from alpha channel to match embedder behavior
            for channel in range(3):  # B, G, R (skip alpha if present)
                if bit_index >= num_bits:
                    break
                
                # Extract LSB
                bit = pixel[channel] & 1
                bits.append(bit)
                bit_index += 1
        
        logger.info(f"Extracted {len(bits)} bits from {len(edge_coordinates)} edge pixels")
        
        return bits
    
    def _bits_to_bytes(self, bits: list) -> bytes:
        """
        Convert list of bits to bytes.
        
        Parameters:
        bits (list):
            List of bits (0 or 1).
            
        Returns:
        bytes: Binary data.
        """
        # Ensure bits length is multiple of 8
        if len(bits) % 8 != 0:
            bits = bits[: (len(bits) // 8) * 8]
        
        bytes_data = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | bits[i + j]
            bytes_data.append(byte)
        
        return bytes(bytes_data)
    
    def validate_image(self, image_path: str) -> bool:
        """
        Validate that the image can be processed for extraction.
        
        Parameters:
        image_path (str):
            Path to the image file.
            
        Returns:
        bool: True if image is valid, False otherwise.
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Invalid image: {image_path}")
                return False
            
            # Check if image is PNG
            if not image_path.lower().endswith('.png'):
                logger.warning(f"Image is not PNG format: {image_path}")
                return False
            
            logger.info(f"Image validation passed: {image_path}")
            return True
            
        except Exception as e:
            logger.error(f"Image validation error: {e}")
            return False


# Global edge LSB extractor instance
edge_lsb_extractor = EdgeLSBExtractor()
