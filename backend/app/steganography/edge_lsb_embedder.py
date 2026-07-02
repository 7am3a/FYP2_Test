"""
Edge-Based LSB Embedder Module for SecureStego

This module implements the embedding logic for hiding encrypted data
inside edge pixels of an image using Least Significant Bit (LSB) steganography.

Why Edge-Based LSB:
- Edge regions are less sensitive to visual changes
- Hiding data only in edges reduces perceptible distortion
- Improves resistance against simple steganalysis
- Better preserves image quality compared to sequential LSB

Embedding Process:
1. Load PNG image pixels
2. Get edge pixel coordinates from edge detector
3. Convert payload to binary
4. Embed bits into LSB of edge pixels (RGB channels)
5. Save modified image as stego image
"""

import cv2
import numpy as np
import logging
from typing import Tuple, Dict
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EdgeLSBEmbedder:
    """
    Embeds encrypted payload into edge pixels using Edge-Based LSB steganography.
    
    Why this exists:
    - Implements the core embedding algorithm
    - Ensures data is hidden only in edge pixels
    - Preserves image quality by avoiding smooth regions
    - Provides capacity checking before embedding
    
    Security Considerations:
    - Only modifies LSB of edge pixels (minimal visual impact)
    - Embeds data across all RGB channels for capacity
    - Includes payload length header for extraction
    - Uses deterministic edge selection (same image = same locations)
    """
    
    # Number of bits to hide per pixel (1 LSB per channel = 3 bits per pixel)
    BITS_PER_PIXEL = 3
    
    # Size of payload length header in bytes (4 bytes = 32 bits = max 4GB payload)
    HEADER_SIZE = 4
    
    def __init__(self):
        """Initialize the edge LSB embedder."""
        logger.info("EdgeLSBEmbedder initialized")
    
    def embed(
        self,
        image_path: str,
        payload: bytes,
        edge_coordinates: list
    ) -> Tuple[str, Dict]:
        """
        Embed payload into edge pixels of the image.
        
        This method:
        1. Loads the PNG image
        2. Calculates required capacity
        3. Checks if image has sufficient edge pixels
        4. Embeds payload length header
        5. Embeds payload data into edge pixels
        6. Saves stego image
        
        Parameters:
        image_path (str):
            Path to the PNG image file.
        payload (bytes):
            Binary payload data to embed.
        edge_coordinates (list):
            List of (row, col) tuples for edge pixels.
            
        Returns:
        Tuple[str, Dict]:
            - Path to the generated stego image
            - Dictionary with embedding statistics
            
        Raises:
        ValueError: If image capacity is insufficient
        IOError: If image cannot be processed
        """
        try:
            logger.info(f"Starting embedding process for: {image_path}")
            
            # Load image preserving alpha channel
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise IOError(f"Failed to load image: {image_path}")
            
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            has_alpha = channels == 4
            logger.info(f"Image loaded: {width}x{height}, channels: {channels}, has_alpha: {has_alpha}")
            
            # Calculate required capacity
            payload_size_bits = len(payload) * 8
            header_size_bits = self.HEADER_SIZE * 8
            total_bits_needed = payload_size_bits + header_size_bits
            
            # Calculate available capacity
            available_pixels = len(edge_coordinates)
            available_capacity_bits = available_pixels * self.BITS_PER_PIXEL
            
            logger.info(
                f"Capacity check: needed={total_bits_needed} bits, "
                f"available={available_capacity_bits} bits"
            )
            
            # Check capacity
            if total_bits_needed > available_capacity_bits:
                raise ValueError(
                    f"Image capacity exceeded. "
                    f"Need {total_bits_needed} bits but only have {available_capacity_bits} bits. "
                    f"Please upload a larger image."
                )
            
            # Embed payload
            stego_image = self._embed_data(
                image,
                payload,
                edge_coordinates,
                has_alpha
            )
            
            # Save stego image with balanced compression
            import tempfile
            import os
            
            temp_file = tempfile.NamedTemporaryFile(
                suffix='_stego.png',
                delete=False
            )
            stego_path = temp_file.name
            temp_file.close()
            
            # Save with PNG compression level 6 for better performance
            cv2.imwrite(stego_path, stego_image, [cv2.IMWRITE_PNG_COMPRESSION, 6])
            logger.info(f"Stego image saved with compression level 6: {stego_path}")
            
            # Calculate statistics
            stats = {
                'imageWidth': width,
                'imageHeight': height,
                'totalPixels': width * height,
                'edgePixels': available_pixels,
                'payloadSize': len(payload),
                'headerSize': self.HEADER_SIZE,
                'totalBitsUsed': total_bits_needed,
                'capacityRemaining': available_capacity_bits - total_bits_needed,
                'capacityUsedPercent': (total_bits_needed / available_capacity_bits) * 100
            }
            
            logger.info(f"Embedding completed successfully. Stats: {stats}")
            
            return stego_path, stats
            
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            raise
    
    def _embed_data(
        self,
        image: np.ndarray,
        payload: bytes,
        edge_coordinates: list,
        has_alpha: bool = False
    ) -> np.ndarray:
        """
        Internal method to embed data into image pixels.
        
        Parameters:
        image (np.ndarray):
            Image array (BGR or BGRA format).
        payload (bytes):
            Binary payload data to embed.
        edge_coordinates (list):
            List of (row, col) tuples for edge pixels.
        has_alpha (bool):
            Whether the image has an alpha channel.
            
        Returns:
        np.ndarray: Modified image array with embedded data.
        """
        # Create a copy to avoid modifying original
        stego_image = image.copy()
        
        # Prepare data: header (payload length) + payload
        payload_length = len(payload)
        header = struct.pack('>I', payload_length)  # 4-byte big-endian
        data_to_embed = header + payload
        
        # Convert to bit stream
        bit_stream = self._bytes_to_bits(data_to_embed)
        
        # Embed bits into edge pixels
        bit_index = 0
        
        for row, col in edge_coordinates:
            if bit_index >= len(bit_stream):
                break
            
            # Get pixel (BGR or BGRA format)
            pixel = stego_image[row, col]
            
            # Embed up to 3 bits (one per RGB channel)
            # Never modify the alpha channel to preserve transparency
            for channel in range(3):  # B, G, R (skip alpha if present)
                if bit_index >= len(bit_stream):
                    break
                
                # Clear LSB and set to our bit
                pixel[channel] = (pixel[channel] & 0xFE) | bit_stream[bit_index]
                bit_index += 1
            
            # Update pixel in image
            stego_image[row, col] = pixel
        
        logger.info(f"Embedded {bit_index} bits into {len(edge_coordinates)} edge pixels (alpha preserved: {has_alpha})")
        
        return stego_image
    
    def _bytes_to_bits(self, data: bytes) -> list:
        """
        Convert bytes to list of bits.
        
        Parameters:
        data (bytes):
            Binary data.
            
        Returns:
        list: List of bits (0 or 1).
        """
        bits = []
        for byte in data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        return bits
    
    def calculate_capacity(self, edge_pixel_count: int) -> Dict:
        """
        Calculate steganography capacity based on edge pixel count.
        
        Parameters:
        edge_pixel_count (int):
            Number of edge pixels in the image.
            
        Returns:
        Dict: Capacity information including total, used, and remaining.
        """
        total_capacity_bits = edge_pixel_count * self.BITS_PER_PIXEL
        header_capacity_bits = self.HEADER_SIZE * 8
        data_capacity_bits = total_capacity_bits - header_capacity_bits
        data_capacity_bytes = data_capacity_bits // 8
        
        return {
            'totalCapacityBits': total_capacity_bits,
            'headerCapacityBits': header_capacity_bits,
            'dataCapacityBits': data_capacity_bits,
            'dataCapacityBytes': data_capacity_bytes
        }


# Global edge LSB embedder instance
edge_lsb_embedder = EdgeLSBEmbedder()
