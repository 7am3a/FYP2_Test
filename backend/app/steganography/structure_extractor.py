"""
structure_extractor.py

Purpose:
Extracts encrypted payload bits from document structure (whitespace, line endings, spacing).

This module is intentionally isolated from PDF processing and payload deserialization
to improve maintainability and debugging.

Why this exists:
- Implements structure-based extraction
- Decodes whitespace patterns
- Validates payload header
- Returns encrypted data

Security Considerations:
- Validates magic signature before extraction
- Handles corrupted payloads gracefully
- Provides error detection
- Logs all extraction operations
"""

import logging
from typing import Tuple, Dict, List
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StructureExtractor:
    """
    Extracts encrypted payload from document structure.
    
    Why this exists:
    - Implements structure-based extraction
    - Validates payload integrity
    - Handles various encoding methods
    - Provides reliable extraction
    
    Security Considerations:
    - Validates magic signature
    - Handles corrupted data
    - Provides error detection
    - Logs all operations
    """
    
    # Magic signature
    MAGIC_SIGNATURE = b'DSTG'
    
    # Payload header size in bytes
    HEADER_SIZE = 8
    
    def __init__(self):
        """Initialize the structure extractor."""
        logger.info("StructureExtractor initialized")
    
    def extract(self, text: str, method: str = "whitespace") -> Tuple[bytes, Dict]:
        """
        Extract payload from text using structure-based methods.
        
        This method:
        1. Applies structure-based decoding
        2. Converts to bit stream
        3. Validates magic signature
        4. Reads payload length
        5. Extracts payload data
        6. Returns payload and statistics
        
        Parameters:
        text (str):
            Text content with embedded payload.
        method (str):
            Extraction method ('whitespace', 'line_ending', 'spacing').
            
        Returns:
        Tuple[bytes, Dict]:
            - Extracted payload bytes
            - Dictionary with extraction statistics
            
        Raises:
        ValueError: If no payload found or payload is corrupted
        """
        try:
            logger.info(f"Starting structure-based extraction")
            logger.info(f"Text length: {len(text)} characters")
            logger.info(f"Method: {method}")
            
            # Extract bits based on method
            if method == "whitespace":
                bit_stream = self._extract_whitespace(text)
            elif method == "line_ending":
                bit_stream = self._extract_line_ending(text)
            elif method == "spacing":
                bit_stream = self._extract_spacing(text)
            else:
                raise ValueError(f"Unknown extraction method: {method}")
            
            logger.info(f"Bit stream length: {len(bit_stream)} bits")
            
            if len(bit_stream) == 0:
                raise ValueError("No structure patterns found in text. No hidden payload detected.")
            
            # Convert to bytes
            data_bytes = self._bits_to_bytes(bit_stream)
            logger.info(f"Data bytes length: {len(data_bytes)} bytes")
            
            # Validate and extract payload
            payload, payload_length = self._extract_payload_from_header(data_bytes)
            logger.info(f"Payload extracted: {len(payload)} bytes")
            
            # Calculate statistics
            stats = {
                'textLength': len(text),
                'totalBitsExtracted': len(bit_stream),
                'payloadSize': len(payload),
                'headerSize': self.HEADER_SIZE,
                'extractionMethod': f'Structure-Based ({method})'
            }
            
            logger.info(f"Extraction completed. Stats: {stats}")
            
            return payload, stats
            
        except Exception as e:
            logger.error(f"Structure-based extraction error: {e}")
            raise
    
    def _extract_whitespace(self, text: str) -> List[int]:
        """
        Extract bits using whitespace patterns.
        
        Method:
        - Single space = 0
        - Double space = 1
        
        Parameters:
        text (str):
            Text content.
            
        Returns:
        List[int]: List of extracted bits.
        """
        bits = []
        lines = text.split('\n')
        
        for line in lines:
            if line.endswith('  '):
                bits.append(1)
            elif line.endswith(' '):
                bits.append(0)
        
        return bits
    
    def _extract_line_ending(self, text: str) -> List[int]:
        """
        Extract bits using line ending patterns.
        
        Method:
        - \n = 0
        - \r\n = 1
        
        Parameters:
        text (str):
            Text content.
            
        Returns:
        List[int]: List of extracted bits.
        """
        bits = []
        
        # Check for \r\n patterns
        i = 0
        while i < len(text):
            if text[i] == '\r' and i + 1 < len(text) and text[i + 1] == '\n':
                bits.append(1)
                i += 2
            elif text[i] == '\n':
                bits.append(0)
                i += 1
            else:
                i += 1
        
        return bits
    
    def _extract_spacing(self, text: str) -> List[int]:
        """
        Extract bits using character spacing patterns.
        
        Method:
        - Normal space = 0
        - Non-breaking space = 1
        
        Parameters:
        text (str):
            Text content.
            
        Returns:
        List[int]: List of extracted bits.
        """
        bits = []
        
        for char in text:
            if char == '\u00A0':  # Non-breaking space
                bits.append(1)
            elif char == ' ':
                bits.append(0)
        
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


# Global structure extractor instance
structure_extractor = StructureExtractor()
