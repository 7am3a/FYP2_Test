"""
invisible_character_embedder.py

Purpose:
Embeds encrypted payload bits into document text using randomized invisible Unicode characters.

This module is intentionally isolated from PDF processing and payload serialization
to improve maintainability and debugging.

Why this exists:
- Implements invisible character steganography
- Randomizes insertion points for security
- Preserves document readability
- Prevents easy detection

Security Considerations:
- Uses randomized placement to avoid patterns
- Preserves visual appearance
- Uses multiple invisible character types
- Includes payload header for extraction
"""

import logging
import random
from typing import Tuple, Dict, List
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvisibleCharacterEmbedder:
    """
    Embeds encrypted payload into text using invisible Unicode characters.
    
    Why this exists:
    - Implements randomized invisible character embedding
    - Provides secure hiding mechanism
    - Preserves text readability
    - Supports multiple document types
    
    Security Considerations:
    - Randomizes insertion points to avoid detection
    - Uses multiple invisible character types
    - Includes payload header for reliable extraction
    - Preserves document appearance
    """
    
    # Invisible Unicode characters for encoding
    # Each represents 2 bits (4 different characters)
    INVISIBLE_CHARS = {
        '00': '\u200B',  # Zero Width Space
        '01': '\u200C',  # Zero Width Non-Joiner
        '10': '\u200D',  # Zero Width Joiner
        '11': '\uFEFF'   # Zero Width No-Break Space (BOM)
    }
    
    # Reverse mapping for extraction
    CHAR_TO_BITS = {v: k for k, v in INVISIBLE_CHARS.items()}
    
    # Payload header size in bytes
    HEADER_SIZE = 8
    
    def __init__(self):
        """Initialize the invisible character embedder."""
        logger.info("InvisibleCharacterEmbedder initialized")
    
    def embed(
        self,
        text: str,
        payload: bytes,
        method: str = "randomized"
    ) -> Tuple[str, Dict]:
        """
        Embed payload into text using invisible characters.
        
        This method:
        1. Prepares payload with header
        2. Converts payload to bit stream
        3. Generates insertion positions
        4. Embeds invisible characters
        5. Returns modified text and statistics
        
        Parameters:
        text (str):
            Original text content.
        payload (bytes):
            Binary payload to embed.
        method (str):
            Embedding method ('randomized' or 'sequential').
            
        Returns:
        Tuple[str, Dict]:
            - Modified text with embedded payload
            - Dictionary with embedding statistics
            
        Raises:
        ValueError: If text capacity is insufficient
        """
        try:
            logger.info(f"Starting invisible character embedding")
            logger.info(f"Original text length: {len(text)} characters")
            logger.info(f"Payload size: {len(payload)} bytes")
            
            # Calculate capacity
            capacity_info = self.calculate_capacity(text)
            required_bits = (len(payload) * 8) + (self.HEADER_SIZE * 8)
            available_bits = capacity_info['totalCapacityBits']
            
            logger.info(f"Capacity check: needed={required_bits} bits, available={available_bits} bits")
            
            if required_bits > available_bits:
                raise ValueError(
                    f"Text capacity exceeded. "
                    f"Need {required_bits} bits but only have {available_bits} bits. "
                    f"Please use a document with more text content."
                )
            
            # Prepare payload with header
            payload_with_header = self._prepare_payload(payload)
            logger.info(f"Payload with header size: {len(payload_with_header)} bytes")
            
            # Convert to bit stream
            bit_stream = self._bytes_to_bits(payload_with_header)
            logger.info(f"Bit stream length: {len(bit_stream)} bits")
            
            # Generate insertion positions
            if method == "randomized":
                insertion_positions = self._generate_random_positions(text, len(bit_stream))
            else:
                insertion_positions = self._generate_sequential_positions(text, len(bit_stream))
            
            logger.info(f"Generated {len(insertion_positions)} insertion positions")
            
            # Embed invisible characters
            stego_text = self._embed_invisible_chars(text, bit_stream, insertion_positions)
            
            # Calculate statistics
            stats = {
                'originalLength': len(text),
                'stegoLength': len(stego_text),
                'payloadSize': len(payload),
                'headerSize': self.HEADER_SIZE,
                'totalBitsEmbedded': len(bit_stream),
                'invisibleCharsInserted': len(insertion_positions),
                'capacityUsedPercent': round((len(bit_stream) / available_bits) * 100, 2),
                'embeddingMethod': f'Invisible Character ({method})'
            }
            
            logger.info(f"Embedding completed. Stats: {stats}")
            
            return stego_text, stats
            
        except Exception as e:
            logger.error(f"Invisible character embedding error: {e}")
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
    
    def _generate_random_positions(self, text: str, num_bits: int) -> List[int]:
        """
        Generate randomized insertion positions.
        
        This method:
        1. Identifies valid insertion points (after words, spaces)
        2. Randomly selects positions
        3. Ensures positions are unique
        4. Returns sorted list of positions
        
        Parameters:
        text (str):
            Text content.
        num_bits (int):
            Number of bits to embed.
            
        Returns:
        List[int]: List of insertion positions (character indices).
        """
        # Find valid insertion points (after spaces, word boundaries)
        valid_positions = []
        for i, char in enumerate(text):
            if char.isspace() or char in '.,;:!?':
                valid_positions.append(i + 1)  # Insert after the character
        
        # If not enough positions, use all character positions
        if len(valid_positions) < num_bits:
            valid_positions = list(range(1, len(text)))
        
        # Randomly select positions
        num_chars_needed = (num_bits + 1) // 2  # 2 bits per character
        selected_positions = random.sample(valid_positions, min(num_chars_needed, len(valid_positions)))
        
        # Sort positions
        selected_positions.sort()
        
        return selected_positions
    
    def _generate_sequential_positions(self, text: str, num_bits: int) -> List[int]:
        """
        Generate sequential insertion positions.
        
        Parameters:
        text (str):
            Text content.
        num_bits (int):
            Number of bits to embed.
            
        Returns:
        List[int]: List of insertion positions (character indices).
        """
        # Insert after every N characters
        num_chars_needed = (num_bits + 1) // 2
        interval = max(1, len(text) // num_chars_needed)
        
        positions = []
        for i in range(num_chars_needed):
            pos = (i + 1) * interval
            if pos < len(text):
                positions.append(pos)
        
        return positions
    
    def _embed_invisible_chars(
        self,
        text: str,
        bit_stream: List[int],
        positions: List[int]
    ) -> str:
        """
        Embed invisible characters into text at specified positions.
        
        Parameters:
        text (str):
            Original text.
        bit_stream (List[int]):
            List of bits to embed.
        positions (List[int]):
            Insertion positions.
            
        Returns:
        str: Text with embedded invisible characters.
        """
        # Convert text to list for easier insertion
        text_list = list(text)
        
        # Insert invisible characters
        bit_index = 0
        offset = 0  # Offset to account for inserted characters
        
        for pos in positions:
            if bit_index + 1 >= len(bit_stream):
                break
            
            # Get 2 bits
            bit_pair = f"{bit_stream[bit_index]}{bit_stream[bit_index + 1]}"
            
            # Get corresponding invisible character
            invisible_char = self.INVISIBLE_CHARS.get(bit_pair, '\u200B')
            
            # Insert at position (with offset)
            actual_pos = pos + offset
            if actual_pos <= len(text_list):
                text_list.insert(actual_pos, invisible_char)
                offset += 1
            
            bit_index += 2
        
        # Join back to string
        stego_text = ''.join(text_list)
        
        return stego_text
    
    def calculate_capacity(self, text: str) -> Dict:
        """
        Calculate steganography capacity of text.
        
        Parameters:
        text (str):
            Text content.
            
        Returns:
        Dict: Capacity information.
        """
        # Count valid insertion points
        valid_positions = 0
        for char in text:
            if char.isspace() or char in '.,;:!?':
                valid_positions += 1
        
        # Each position can hold 2 bits
        total_capacity_bits = valid_positions * 2
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


# Global invisible character embedder instance
invisible_character_embedder = InvisibleCharacterEmbedder()
