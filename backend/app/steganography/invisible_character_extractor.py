"""
invisible_character_extractor.py

Purpose:
Extracts encrypted payload bits from document text using invisible Unicode characters.

This module is intentionally isolated from PDF processing and payload deserialization
to improve maintainability and debugging.

Why this exists:
- Implements invisible character extraction
- Locates and decodes hidden payload
- Validates payload header
- Returns encrypted data

Security Considerations:
- Validates magic signature before extraction
- Handles corrupted payloads gracefully
- Provides error detection
- Logs all extraction operations
"""

import logging
from typing import Tuple, Dict, List, Optional
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvisibleCharacterExtractor:
    """
    Extracts encrypted payload from text using invisible Unicode characters.
    
    Why this exists:
    - Implements invisible character extraction
    - Validates payload integrity
    - Handles various document types
    - Provides reliable extraction
    
    Security Considerations:
    - Validates magic signature
    - Handles corrupted data
    - Provides error detection
    - Logs all operations
    """
    
    # Invisible Unicode characters for decoding
    CHAR_TO_BITS = {
        '\u200B': '00',  # Zero Width Space
        '\u200C': '01',  # Zero Width Non-Joiner
        '\u200D': '10',  # Zero Width Joiner
        '\uFEFF': '11'   # Zero Width No-Break Space (BOM)
    }
    
    # Magic signature
    MAGIC_SIGNATURE = b'DSTG'
    
    # Payload header size in bytes
    HEADER_SIZE = 8
    
    def __init__(self):
        """Initialize the invisible character extractor."""
        logger.info("InvisibleCharacterExtractor initialized")
    
    def extract(self, text: str) -> Tuple[bytes, Dict]:
        """
        Extract payload from text using invisible characters.
        
        This method:
        1. Scans text for invisible characters
        2. Converts characters to bit stream
        3. Validates magic signature
        4. Reads payload length
        5. Extracts payload data
        6. Returns payload and statistics
        
        Parameters:
        text (str):
            Text content with embedded payload.
            
        Returns:
        Tuple[bytes, Dict]:
            - Extracted payload bytes
            - Dictionary with extraction statistics
            
        Raises:
        ValueError: If no payload found or payload is corrupted
        """
        try:
            logger.info(f"Starting invisible character extraction")
            logger.info(f"Text length: {len(text)} characters")
            
            # Extract invisible characters
            invisible_chars = self._extract_invisible_chars(text)
            logger.info(f"Found {len(invisible_chars)} invisible characters")
            
            if len(invisible_chars) == 0:
                raise ValueError("No invisible characters found in text. No hidden payload detected.")
            
            # Convert to bit stream
            bit_stream = self._chars_to_bits(invisible_chars)
            logger.info(f"Bit stream length: {len(bit_stream)} bits")
            
            # Convert to bytes
            data_bytes = self._bits_to_bytes(bit_stream)
            logger.info(f"Data bytes length: {len(data_bytes)} bytes")
            
            # Validate and extract payload
            payload, payload_length = self._extract_payload_from_header(data_bytes)
            logger.info(f"Payload extracted: {len(payload)} bytes")
            
            # Calculate statistics
            stats = {
                'textLength': len(text),
                'invisibleCharsFound': len(invisible_chars),
                'totalBitsExtracted': len(bit_stream),
                'payloadSize': len(payload),
                'headerSize': self.HEADER_SIZE,
                'extractionMethod': 'Invisible Character'
            }
            
            logger.info(f"Extraction completed. Stats: {stats}")
            
            return payload, stats
            
        except Exception as e:
            logger.error(f"Invisible character extraction error: {e}")
            raise
    
    def _extract_invisible_chars(self, text: str) -> List[str]:
        """
        Extract all invisible characters from text.
        
        Parameters:
        text (str):
            Text content.
            
        Returns:
        List[str]: List of invisible characters found.
        """
        invisible_chars = []
        
        for char in text:
            if char in self.CHAR_TO_BITS:
                invisible_chars.append(char)
        
        return invisible_chars
    
    def _chars_to_bits(self, chars: List[str]) -> List[int]:
        """
        Convert invisible characters to bit stream.
        
        Parameters:
        chars (List[str]):
            List of invisible characters.
            
        Returns:
        List[int]: List of bits (0 or 1).
        """
        bits = []
        
        for char in chars:
            bit_pair = self.CHAR_TO_BITS.get(char, '00')
            bits.append(int(bit_pair[0]))
            bits.append(int(bit_pair[1]))
        
        return bits
    
    def _bits_to_bytes(self, bits: List[int]) -> bytes:
        """
        Convert bit stream to bytes.
        
        Parameters:
        bits (List[int]):
            List of bits (0 or 1).
            
        Returns:
        bytes: Binary data.
        """
        # Pad bits to complete bytes
        padding = (8 - len(bits) % 8) % 8
        bits.extend([0] * padding)
        
        # Convert to bytes
        data_bytes = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | bits[i + j]
            data_bytes.append(byte)
        
        return bytes(data_bytes)
    
    def _extract_payload_from_header(self, data: bytes) -> Tuple[bytes, int]:
        """
        Extract payload from data with header.
        
        Header structure:
        - 4 bytes: MAGIC signature
        - 4 bytes: Payload length (big-endian)
        - N bytes: Payload data
        
        Parameters:
        data (bytes):
            Data with header.
            
        Returns:
        Tuple[bytes, int]:
            - Extracted payload
            - Payload length
            
        Raises:
        ValueError: If header is invalid or corrupted
        """
        # Check minimum size
        if len(data) < self.HEADER_SIZE:
            raise ValueError(
                f"Data too short for header. "
                f"Need {self.HEADER_SIZE} bytes but only have {len(data)} bytes."
            )
        
        # Extract magic signature
        magic = data[:4]
        
        # Validate magic signature
        if magic != self.MAGIC_SIGNATURE:
            raise ValueError(
                f"Invalid magic signature. "
                f"Expected {self.MAGIC_SIGNATURE} but got {magic}. "
                f"This may not be a valid stego document."
            )
        
        logger.info("Magic signature validated")
        
        # Extract payload length
        payload_length = struct.unpack('>I', data[4:8])[0]
        logger.info(f"Payload length from header: {payload_length} bytes")
        
        # Check if data contains full payload
        total_needed = self.HEADER_SIZE + payload_length
        if len(data) < total_needed:
            raise ValueError(
                f"Incomplete payload. "
                f"Need {total_needed} bytes but only have {len(data)} bytes."
            )
        
        # Extract payload
        payload = data[8:8 + payload_length]
        
        return payload, payload_length


# Global invisible character extractor instance
invisible_character_extractor = InvisibleCharacterExtractor()
