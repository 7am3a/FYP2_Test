"""
DCT Embedder Module for SecureStego

Purpose:
Embeds encrypted payload bits into selected DCT coefficients of video frames.

This module is isolated from frame extraction, video conversion, and payload serialization
to improve maintainability and debugging.

Embedding Workflow:
1. Receive frame and payload binary
2. Convert frame to YCbCr
3. Extract luminance channel
4. Split into 8x8 blocks
5. Apply DCT to each block
6. Modify mid-frequency coefficients
7. Apply inverse DCT
8. Reconstruct frame
9. Return modified frame and statistics

Embedding Strategy:
- Use mid-frequency DCT coefficients
- Modify least significant bit of coefficient
- Avoid DC coefficient (0,0)
- Avoid very high frequencies (unstable)
- Preserve visual quality

Why This Exists:
- Provides frequency-domain embedding
- Improves robustness to compression
- Better imperceptibility than spatial methods
- Standard approach in video steganography

Security Considerations:
- Minimal coefficient modification (LSB only)
- Preserves statistical properties
- Does not introduce detectable patterns
- Deterministic embedding for reproducible extraction
"""

import numpy as np
import logging
from typing import Tuple, List
from app.steganography.video.dct_transform import dct_transform

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DCTEmbedder:
    """
    Embeds payload bits into DCT coefficients of video frames.
    
    Why this exists:
    - Provides frequency-domain embedding
    - Improves robustness and imperceptibility
    - Uses standard DCT-based approach
    - Enables high-capacity embedding
    
    Security Considerations:
    - Minimal coefficient modification
    - Preserves statistical properties
    - Deterministic embedding
    - No detectable artifacts
    """
    
    # Header size in bytes (for payload metadata)
    HEADER_SIZE = 32  # 256 bits for header
    
    # Bits per coefficient (LSB only)
    BITS_PER_COEFFICIENT = 1
    
    
    def __init__(self):
        """Initialize the DCT embedder."""
        logger.info("DCTEmbedder initialized")
    
    def embed(
        self,
        frame: np.ndarray,
        payload_binary: bytes,
        coefficient_positions: List[Tuple[int, int]] = None
    ) -> Tuple[np.ndarray, dict]:
        """
        Embed payload bits into a video frame using DCT coefficients.
        
        This method:
        1. Converts frame to YCbCr color space
        2. Extracts luminance channel
        3. Splits into 8x8 blocks
        4. Applies DCT to each block
        5. Embeds payload bits into mid-frequency coefficients
        6. Applies inverse DCT
        7. Reconstructs frame
        8. Returns modified frame and statistics
        
        Parameters:
        frame (np.ndarray):
            RGB frame (H x W x 3).
        payload_binary (bytes):
            Binary payload to embed.
        coefficient_positions (List[Tuple[int, int]], optional):
            List of (row, col) positions to use in each block.
            If None, uses default mid-frequency positions.
            
        Returns:
        Tuple[np.ndarray, dict]:
            - Modified RGB frame (H x W x 3)
            - Dictionary with embedding statistics
            
        Raises:
        ValueError: If payload exceeds frame capacity
        """
        try:
            logger.info(f"Embedding {len(payload_binary)} bytes into frame")
            
            # Get coefficient positions if not provided
            if coefficient_positions is None:
                coefficient_positions = dct_transform.get_mid_frequency_coefficients(
                    np.zeros((8, 8))
                )
            
            # Calculate capacity
            capacity_info = self.calculate_capacity(frame.shape, coefficient_positions)
            required_bits = (len(payload_binary) * 8) + (self.HEADER_SIZE * 8)
            
            if required_bits > capacity_info['totalCapacityBits']:
                raise ValueError(
                    f"Frame capacity exceeded. "
                    f"Need {required_bits} bits but only have {capacity_info['totalCapacityBits']} bits."
                )
            
            logger.info(
                f"Capacity check passed: {required_bits} bits needed, "
                f"{capacity_info['totalCapacityBits']} bits available"
            )
            
            # Step 1: Convert to YCbCr
            ycbcr_frame = dct_transform.frame_to_ycbcr(frame)
            
            # Step 2: Extract luminance
            luminance = dct_transform.extract_luminance(ycbcr_frame)
            
            # Step 3: Split into blocks
            blocks = dct_transform.split_into_blocks(luminance)
            
            # Step 4: Create payload with header
            payload_with_header = self._create_payload_with_header(payload_binary)
            
            # Step 5: Convert payload to bit stream
            bit_stream = self._bytes_to_bits(payload_with_header)
            
            # Step 6: Embed bits into DCT coefficients
            modified_blocks = []
            bit_idx = 0
            
            for block in blocks:
                if bit_idx >= len(bit_stream):
                    # No more bits to embed, keep original block
                    modified_blocks.append(block)
                    continue
                
                # Apply DCT
                dct_block = dct_transform.apply_dct(block)
                
                for pos in coefficient_positions:

                    if bit_idx >= len(bit_stream):
                        break

                    row, col = pos
                    logger.debug(
                        f"EMBED ({row},{col}) value={dct_block[row,col]:.2f} bit={bit_stream[bit_idx]}"
                    )

                    coefficient = dct_block[row, col]
                    

                    dct_block[row, col] = self._modify_coefficient_lsb(
                        coefficient,
                        bit_stream[bit_idx]
                    )
                    logger.info(
                        f"EMBED ({row},{col}) before={coefficient:.2f} after={dct_block[row,col]:.2f}"
                    )

                    bit_idx += 1
                
                # Apply inverse DCT
                modified_block = dct_transform.apply_inverse_dct(dct_block)
                modified_blocks.append(modified_block)
            
            # Step 7: Reconstruct luminance
            modified_luminance = dct_transform.reconstruct_from_blocks(
                modified_blocks,
                luminance.shape
            )
            
            # Step 8: Set luminance in YCbCr frame
            modified_ycbcr = dct_transform.set_luminance(ycbcr_frame, modified_luminance)
            
            # Step 9: Convert back to RGB
            modified_frame = dct_transform.ycbcr_to_frame(modified_ycbcr)
            
            # Calculate statistics
            stats = {
                'frameWidth': frame.shape[1],
                'frameHeight': frame.shape[0],
                'totalBlocks': len(blocks),
                'payloadSize': len(payload_binary),
                'headerSize': self.HEADER_SIZE,
                'totalBitsEmbedded': bit_idx,
                'bitsPerCoefficient': self.BITS_PER_COEFFICIENT,
                'coefficientsUsed': len(coefficient_positions),
                'capacityRemaining': capacity_info['totalCapacityBits'] - bit_idx,
                'capacityUsedPercent': round((bit_idx / capacity_info['totalCapacityBits']) * 100, 2)
            }
            
            
            
            return modified_frame, stats
            
        except Exception as e:
            logger.error(f"DCT embedding error: {e}")
            raise
    
    def _create_payload_with_header(self, payload_binary: bytes) -> bytes:
        """
        Create payload with header containing length information.
        
        Header structure (32 bytes):
        - Magic signature (8 bytes): "VIDSTEGO"
        - Payload length (4 bytes): uint32
        - Reserved (20 bytes): for future use
        
        Parameters:
        payload_binary (bytes):
            Original payload.
            
        Returns:
        bytes: Payload with header prepended.
        """
        try:
            # Magic signature
            magic = b'VIDSTEGO'
            
            # Payload length as uint32 (4 bytes)
            payload_length = len(payload_binary).to_bytes(4, byteorder='big')
            
            # Reserved space (20 bytes)
            reserved = b'\x00' * 20
            
            # Combine header
            header = magic + payload_length + reserved
            
            # Return header + payload
            return header + payload_binary
            
        except Exception as e:
            logger.error(f"Header creation error: {e}")
            raise
    
    def _bytes_to_bits(self, data: bytes) -> List[int]:
        """
        Convert bytes to list of bits.
        
        Parameters:
        data (bytes):
            Binary data.
            
        Returns:
        List[int]: List of bits (0 or 1).
        """
        bits = []
        for byte in data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        return bits
    
    QIM_DELTA = 32.0


    def _modify_coefficient_lsb(self, coefficient: float, bit: int) -> float:
        """
        Embed one bit using Quantization Index Modulation (QIM)
        instead of coefficient LSB.
        """

        delta = self.QIM_DELTA

        if bit == 0:
            return round(coefficient / delta) * delta

        else:
            return round((coefficient - delta / 2) / delta) * delta + delta / 2
    
    
    def calculate_capacity(
        self,
        frame_shape: Tuple[int, int, int],
        coefficient_positions: List[Tuple[int, int]]
    ) -> dict:
        """
        Calculate embedding capacity of a frame.
        
        Parameters:
        frame_shape (Tuple[int, int, int]):
            Frame shape (H, W, C).
        coefficient_positions (List[Tuple[int, int]]):
            List of coefficient positions to use.
            
        Returns:
        dict: Capacity information.
        """
        try:
            height, width = frame_shape[:2]
            
            # Calculate number of blocks
            blocks_per_row = (width + 7) // 8
            blocks_per_col = (height + 7) // 8
            total_blocks = blocks_per_row * blocks_per_col
            
            # Calculate total capacity
            bits_per_block = len(coefficient_positions) * self.BITS_PER_COEFFICIENT
            total_bits = total_blocks * bits_per_block
            total_bytes = total_bits // 8
            
            return {
                'totalBlocks': total_blocks,
                'coefficientsPerBlock': len(coefficient_positions),
                'bitsPerBlock': bits_per_block,
                'totalCapacityBits': total_bits,
                'totalCapacityBytes': total_bytes,
                'headerSizeBits': self.HEADER_SIZE * 8,
                'headerSizeBytes': self.HEADER_SIZE,
                'availablePayloadBits': total_bits - (self.HEADER_SIZE * 8),
                'availablePayloadBytes': total_bytes - self.HEADER_SIZE
            }
            
        except Exception as e:
            logger.error(f"Capacity calculation error: {e}")
            raise


# Global DCT embedder instance
dct_embedder = DCTEmbedder()
