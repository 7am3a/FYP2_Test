"""
structure_embedder.py

Purpose:
Embeds encrypted payload bits into document structure (whitespace, line endings, spacing).

This module is intentionally isolated from PDF processing and payload serialization
to improve maintainability and debugging.

Why this exists:
- Implements structure-based steganography
- Uses controlled whitespace patterns
- Preserves document layout
- Provides alternative embedding method

Security Considerations:
- Preserves visual appearance
- Uses subtle structure modifications
- Includes payload header
- Supports reliable extraction
"""

import logging
from typing import Tuple, Dict, List
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StructureEmbedder:
    """
    Embeds encrypted payload into document structure.
    
    Why this exists:
    - Implements structure-based embedding
    - Uses whitespace and spacing patterns
    - Preserves document appearance
    - Provides alternative to invisible characters
    
    Security Considerations:
    - Preserves visual layout
    - Uses subtle modifications
    - Includes payload header
    - Supports reliable extraction
    """
    
    # Payload header size in bytes
    HEADER_SIZE = 8
    
    def __init__(self):
        """Initialize the structure embedder."""
        logger.info("StructureEmbedder initialized")
    
    def embed(
        self,
        text: str,
        payload: bytes,
        method: str = "whitespace"
    ) -> Tuple[str, Dict]:
        """
        Embed payload into text using structure-based methods.
        
        This method:
        1. Prepares payload with header
        2. Converts payload to bit stream
        3. Applies structure-based encoding
        4. Returns modified text and statistics
        
        Parameters:
        text (str):
            Original text content.
        payload (bytes):
            Binary payload to embed.
        method (str):
            Embedding method ('whitespace', 'line_ending', 'spacing').
            
        Returns:
        Tuple[str, Dict]:
            - Modified text with embedded payload
            - Dictionary with embedding statistics
            
        Raises:
        ValueError: If text capacity is insufficient
        """
        try:
            logger.info(f"Starting structure-based embedding")
            logger.info(f"Original text length: {len(text)} characters")
            logger.info(f"Payload size: {len(payload)} bytes")
            logger.info(f"Method: {method}")
            
            # Calculate capacity
            capacity_info = self.calculate_capacity(text, method)
            required_bits = (len(payload) * 8) + (self.HEADER_SIZE * 8)
            available_bits = capacity_info['totalCapacityBits']
            
            logger.info(f"Capacity check: needed={required_bits} bits, available={available_bits} bits")
            
            if required_bits > available_bits:
                raise ValueError(
                    f"Text capacity exceeded. "
                    f"Need {required_bits} bits but only have {available_bits} bits. "
                    f"Please use a document with more content."
                )
            
            # Prepare payload with header
            payload_with_header = self._prepare_payload(payload)
            logger.info(f"Payload with header size: {len(payload_with_header)} bytes")
            
            # Convert to bit stream
            bit_stream = self._bytes_to_bits(payload_with_header)
            logger.info(f"Bit stream length: {len(bit_stream)} bits")
            
            # Embed based on method
            if method == "whitespace":
                stego_text = self._embed_whitespace(text, bit_stream)
            elif method == "line_ending":
                stego_text = self._embed_line_ending(text, bit_stream)
            elif method == "spacing":
                stego_text = self._embed_spacing(text, bit_stream)
            else:
                raise ValueError(f"Unknown embedding method: {method}")
            
            # Calculate statistics
            stats = {
                'originalLength': len(text),
                'stegoLength': len(stego_text),
                'payloadSize': len(payload),
                'headerSize': self.HEADER_SIZE,
                'totalBitsEmbedded': len(bit_stream),
                'capacityUsedPercent': round((len(bit_stream) / available_bits) * 100, 2),
                'embeddingMethod': f'Structure-Based ({method})'
            }
            
            logger.info(f"Embedding completed. Stats: {stats}")
            
            return stego_text, stats
            
        except Exception as e:
            logger.error(f"Structure-based embedding error: {e}")
            raise
    
    def _prepare_payload(self, payload: bytes) -> bytes:
        """
        Prepare payload with header for embedding.
        
        Header structure:
        - 4 bytes: MAGIC signature
        - 4 bytes: Payload length (big-endian)
        - N bytes: Payload data
        
        Parameters:
        payload (bytes):
            Original payload data.
            
        Returns:
        bytes: Payload with header.
        """
        # Magic signature: "DSTG" (Document SteGanography)
        magic = b'DSTG'
        
        # Payload length (4 bytes, big-endian)
        payload_length = struct.pack('>I', len(payload))
        
        # Combine: magic + length + payload
        payload_with_header = magic + payload_length + payload
        
        return payload_with_header
    
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
    
    def _embed_whitespace(self, text: str, bit_stream: List[int]) -> str:
        """
        Embed payload using whitespace patterns.
        
        Method:
        - Single space = 0
        - Double space = 1
        
        Parameters:
        text (str):
            Original text.
        bit_stream (List[int]):
            List of bits to embed.
            
        Returns:
        str: Text with embedded payload.
        """
        lines = text.split('\n')
        stego_lines = []
        bit_index = 0
        
        for line in lines:
            if bit_index >= len(bit_stream):
                stego_lines.append(line)
                continue
            
            # Check if line ends with space
            if line.endswith(' '):
                # Modify trailing spaces to encode bit
                bit = bit_stream[bit_index]
                if bit == 0:
                    # Single space
                    modified_line = line.rstrip() + ' '
                else:
                    # Double space
                    modified_line = line.rstrip() + '  '
                bit_index += 1
                stego_lines.append(modified_line)
            else:
                stego_lines.append(line)
        
        return '\n'.join(stego_lines)
    
    def _embed_line_ending(self, text: str, bit_stream: List[int]) -> str:
        """
        Embed payload using line ending patterns.
        
        Method:
        - \n = 0
        - \r\n = 1
        
        Parameters:
        text (str):
            Original text.
        bit_stream (List[int]):
            List of bits to embed.
            
        Returns:
        str: Text with embedded payload.
        """
        lines = text.split('\n')
        stego_lines = []
        bit_index = 0
        
        for i, line in enumerate(lines):
            if bit_index >= len(bit_stream):
                stego_lines.append(line)
                continue
            
            # If not last line, modify line ending
            if i < len(lines) - 1:
                bit = bit_stream[bit_index]
                if bit == 0:
                    # Use \n
                    stego_lines.append(line + '\n')
                else:
                    # Use \r\n
                    stego_lines.append(line + '\r\n')
                bit_index += 1
            else:
                stego_lines.append(line)
        
        return ''.join(stego_lines)
    
    def _embed_spacing(self, text: str, bit_stream: List[int]) -> str:
        """
        Embed payload using character spacing patterns.
        
        Method:
        - Normal space = 0
        - Non-breaking space = 1
        
        Parameters:
        text (str):
            Original text.
        bit_stream (List[int]):
            List of bits to embed.
            
        Returns:
        str: Text with embedded payload.
        """
        stego_text = []
        bit_index = 0
        
        for char in text:
            if char == ' ' and bit_index < len(bit_stream):
                bit = bit_stream[bit_index]
                if bit == 0:
                    # Normal space
                    stego_text.append(' ')
                else:
                    # Non-breaking space
                    stego_text.append('\u00A0')
                bit_index += 1
            else:
                stego_text.append(char)
        
        return ''.join(stego_text)
    
    def calculate_capacity(self, text: str, method: str) -> Dict:
        """
        Calculate steganography capacity of text for structure-based methods.
        
        Parameters:
        text (str):
            Text content.
        method (str):
            Embedding method.
            
        Returns:
        Dict: Capacity information.
        """
        if method == "whitespace":
            # Count lines ending with space
            lines = text.split('\n')
            valid_positions = sum(1 for line in lines if line.endswith(' '))
        elif method == "line_ending":
            # Count line endings
            valid_positions = text.count('\n')
        elif method == "spacing":
            # Count spaces
            valid_positions = text.count(' ')
        else:
            valid_positions = 0
        
        # Each position can hold 1 bit
        total_capacity_bits = valid_positions
        header_capacity_bits = self.HEADER_SIZE * 8
        data_capacity_bits = total_capacity_bits - header_capacity_bits
        data_capacity_bytes = data_capacity_bits // 8
        
        return {
            'validPositions': valid_positions,
            'totalCapacityBits': total_capacity_bits,
            'headerCapacityBits': header_capacity_bits,
            'dataCapacityBits': data_capacity_bits,
            'dataCapacityBytes': data_capacity_bytes
        }


# Global structure embedder instance
structure_embedder = StructureEmbedder()
