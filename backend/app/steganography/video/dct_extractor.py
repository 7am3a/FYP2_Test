"""
DCT Extractor Module for SecureStego

Purpose:
Recovers encrypted payload bits from DCT coefficients of video frames.

This module is isolated from frame selection, video conversion, and payload deserialization
to improve maintainability and debugging.

Extraction Workflow:
1. Receive frame
2. Convert frame to YCbCr
3. Extract luminance channel
4. Split into 8x8 blocks
5. Apply DCT to each block
6. Extract bits from mid-frequency coefficients
7. Reconstruct payload from bit stream
8. Validate header
9. Return payload binary and statistics

Extraction Strategy:
- Read LSB of selected coefficients
- Use same coefficient positions as embedding
- Validate magic signature
- Read payload length from header
- Extract exact payload size

Why This Exists:
- Provides frequency-domain extraction
- Complements DCT embedder
- Ensures reproducible extraction
- Validates payload integrity

Security Considerations:
- Validates header before extraction
- Reads exact payload size (no guessing)
- Handles corrupted data gracefully
- Does not expose internal state
"""

import numpy as np
import logging
from typing import Tuple, List
from app.steganography.video.dct_transform import dct_transform

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DCTExtractor:
    """
    Extracts payload bits from DCT coefficients of video frames.
    
    Why this exists:
    - Recovers hidden data from DCT coefficients
    - Validates payload integrity
    - Ensures reproducible extraction
    - Handles errors gracefully
    
    Security Considerations:
    - Validates header before extraction
    - Reads exact payload size
    - Handles corrupted data
    - Does not expose internals
    """
    
    # Header size in bytes
    HEADER_SIZE = 32
    
    # Magic signature
    MAGIC_SIGNATURE = b'VIDSTEGO'
    
    # Bits per coefficient
    BITS_PER_COEFFICIENT = 1
    QIM_DELTA = 32.0
    
    def __init__(self):
        """Initialize the DCT extractor."""
        logger.info("DCTExtractor initialized")
    
    def extract(
        self,
        frame: np.ndarray,
        coefficient_positions: List[Tuple[int, int]] = None
    ) -> Tuple[bytes, dict]:
        """
        Extract payload bits from a video frame using DCT coefficients.
        
        This method:
        1. Converts frame to YCbCr color space
        2. Extracts luminance channel
        3. Splits into 8x8 blocks
        4. Applies DCT to each block
        5. Extracts bits from mid-frequency coefficients
        6. Reconstructs payload from bit stream
        7. Validates header
        8. Returns payload binary and statistics
        
        Parameters:
        frame (np.ndarray):
            RGB frame (H x W x 3).
        coefficient_positions (List[Tuple[int, int]], optional):
            List of (row, col) positions to use in each block.
            If None, uses default mid-frequency positions.
            
        Returns:
        Tuple[bytes, dict]:
            - Extracted payload binary
            - Dictionary with extraction statistics
            
        Raises:
        ValueError: If header validation fails or no payload found
        """
        try:
            logger.info("Extracting payload from frame")
            
            # Get coefficient positions if not provided
            if coefficient_positions is None:
                coefficient_positions = dct_transform.get_mid_frequency_coefficients(
                    np.zeros((8, 8))
                )
            
            # Step 1: Convert to YCbCr
            ycbcr_frame = dct_transform.frame_to_ycbcr(frame)
            
            # Step 2: Extract luminance
            luminance = dct_transform.extract_luminance(ycbcr_frame)
            
            # Step 3: Split into blocks
            blocks = dct_transform.split_into_blocks(luminance)
            
            # Step 4: Extract bits from DCT coefficients
            bit_stream = []
            
            for block in blocks:
                # Apply DCT
                dct_block = dct_transform.apply_dct(block)
                
                # Extract bits from selected coefficients
                for pos in coefficient_positions:
                    row, col = pos
                    
                    bit = self._extract_coefficient_lsb(dct_block[row, col])
                    bit_stream.append(bit)
            
            # Step 5: Convert bit stream to bytes
            extracted_bytes = self._bits_to_bytes(bit_stream)
            
            # Step 6: Validate and extract header
            if len(extracted_bytes) < self.HEADER_SIZE:
                raise ValueError(
                    f"Extracted data too short for header. "
                    f"Need {self.HEADER_SIZE} bytes, got {len(extracted_bytes)}"
                )
            
            header = extracted_bytes[:self.HEADER_SIZE]
            payload_length = self._parse_header(header)
            
            # Step 7: Extract payload
            payload_start = self.HEADER_SIZE
            payload_end = payload_start + payload_length
            
            if len(extracted_bytes) < payload_end:
                raise ValueError(
                    f"Extracted data too short for payload. "
                    f"Need {payload_end} bytes, got {len(extracted_bytes)}"
                )
            
            payload_binary = extracted_bytes[payload_start:payload_end]
            
            # Calculate statistics
            stats = {
                'frameWidth': frame.shape[1],
                'frameHeight': frame.shape[0],
                'totalBlocks': len(blocks),
                'totalBitsExtracted': len(bit_stream),
                'headerSize': self.HEADER_SIZE,
                'payloadSize': len(payload_binary),
                'coefficientsUsed': len(coefficient_positions),
                'bitsPerCoefficient': self.BITS_PER_COEFFICIENT
            }
            
            logger.info(f"Extracted {len(payload_binary)} bytes from frame")
            
            return payload_binary, stats
            
        except Exception as e:
            logger.error(f"DCT extraction error: {e}")
            raise
    
    def _parse_header(self, header: bytes) -> int:
        """
        Parse header to get payload length.
        
        Header structure (32 bytes):
        - Magic signature (8 bytes): "VIDSTEGO"
        - Payload length (4 bytes): uint32
        - Reserved (20 bytes): for future use
        
        Parameters:
        header (bytes):
            Header bytes.
            
        Returns:
        int: Payload length in bytes.
            
        Raises:
        ValueError: If magic signature is invalid.
        """
        try:
            # Extract magic signature
            magic = header[:8]
            
            # Validate magic signature
            if magic != self.MAGIC_SIGNATURE:
                raise ValueError(
                    f"Invalid magic signature. "
                    f"Expected {self.MAGIC_SIGNATURE}, got {magic}"
                )
            
            # Extract payload length (bytes 8-11)
            payload_length = int.from_bytes(header[8:12], byteorder='big')
            
            logger.info(f"Header validated, payload length: {payload_length} bytes")
            
            return payload_length
            
        except Exception as e:
            logger.error(f"Header parsing error: {e}")
            raise
    
    

    def _extract_coefficient_lsb(self, coefficient: float) -> int:
        """
        Recover one bit embedded using Quantization Index Modulation.
        """

        delta = self.QIM_DELTA

        q = round(coefficient / (delta / 2))

        return int(q % 2)
    
    def _bits_to_bytes(self, bits: List[int]) -> bytes:
        """
        Convert list of bits to bytes.
        
        Parameters:
        bits (List[int]):
            List of bits (0 or 1).
            
        Returns:
        bytes: Binary data.
        """
        try:
            # Pad bits to complete bytes if necessary
            padding = (8 - len(bits) % 8) % 8
            bits = bits + [0] * padding
            
            # Convert to bytes
            bytes_list = []
            for i in range(0, len(bits), 8):
                byte = 0
                for j in range(8):
                    byte = (byte << 1) | bits[i + j]
                bytes_list.append(byte)
            
            return bytes(bytes_list)
            
        except Exception as e:
            logger.error(f"Bits to bytes conversion error: {e}")
            raise
    
    def validate_frame(self, frame: np.ndarray) -> bool:
        """
        Validate that a frame is suitable for extraction.
        
        Parameters:
        frame (np.ndarray):
            RGB frame to validate.
            
        Returns:
        bool: True if frame is valid, False otherwise.
        """
        try:
            # Check frame dimensions
            if len(frame.shape) != 3:
                logger.error("Invalid frame dimensions")
                return False
            
            if frame.shape[2] != 3:
                logger.error("Frame must have 3 channels")
                return False
            
            # Check frame size
            if frame.shape[0] < 8 or frame.shape[1] < 8:
                logger.error("Frame too small for DCT processing")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Frame validation error: {e}")
            return False


# Global DCT extractor instance
dct_extractor = DCTExtractor()
