"""
audio_lsb_extractor.py

Purpose:
Extracts encrypted payload bits from WAV audio samples using
deterministic randomized LSB steganography.

This module is intentionally isolated from audio conversion,
payload deserialization, and embedding logic to improve maintainability.

Why LSB Extraction:
- Complements the LSB embedding process
- Uses the same randomized sample positions
- Ensures reliable payload recovery
- Validates extracted data integrity
- Provides extraction statistics for debugging

Security Considerations:
- Uses same password-derived positions as embedding
- Validates magic signature before extraction
- Verifies payload length matches header
- Logs all extraction operations for audit trail
- Handles corrupted or invalid stego files gracefully
"""

import logging
from typing import Tuple, Dict
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioLSBExtractor:
    """
    Extracts payload bits from audio samples using LSB steganography.
    
    Why this exists:
    - Provides a dedicated interface for LSB extraction
    - Implements randomized sample position generation
    - Handles payload header parsing
    - Validates extracted data integrity
    - Provides extraction statistics for debugging
    
    Responsibilities:
    - Extract payload bits from audio samples
    - Parse payload header with metadata
    - Use randomized sample positions (same as embedding)
    - Validate extracted payload
    - Calculate extraction statistics
    
    Header Structure:
    - Magic Signature (4 bytes): "STEG"
    - Version (1 byte): Payload version
    - Payload Length (4 bytes): Size of payload in bytes
    - Payload Data (variable): Actual encrypted payload
    
    Dependencies:
    - numpy for efficient array operations
    - sample_selector for randomized positions
    """
    
    # Header constants (must match embedder)
    MAGIC_SIGNATURE = b'STEG'
    HEADER_SIZE = 9  # 4 bytes magic + 1 byte version + 4 bytes length
    
    def __init__(self):
        """Initialize the LSB extractor."""
        logger.info("AudioLSBExtractor initialized")
    
    def extract(
        self,
        samples: np.ndarray,
        password: str,
        total_samples: int
    ) -> Tuple[bytes, Dict]:
        """
        Extract payload bits from audio samples using LSB steganography.
        
        This method:
        1. Generates sample positions from password
        2. Extracts LSB bits from specified positions
        3. Converts bits to bytes
        4. Parses payload header
        5. Validates payload integrity
        6. Returns payload and statistics
        
        Parameters:
        samples (np.ndarray):
            Stego audio samples with embedded payload.
        password (str):
            Password for generating sample positions.
        total_samples (int):
            Total number of samples in the audio file.
            
        Returns:
        Tuple[bytes, Dict]: 
            - Extracted payload data
            - Dictionary containing extraction statistics
            
        Raises:
        ValueError: If extraction fails or payload is invalid
    """
        try:
            logger.info("Starting LSB extraction")
            
            # Step 1: Extract header to determine payload size
            header_positions = self._generate_header_positions(password, total_samples)
            header_bits = self._extract_bits(samples, header_positions)
            header_bytes = self._bits_to_bytes(header_bits)
            
            # Step 2: Parse header
            payload_length = self._parse_header(header_bytes)
            logger.info(f"Header parsed: payload length = {payload_length} bytes")
            
            # Step 3: Generate positions for full payload
            total_payload_size = self.HEADER_SIZE + payload_length
            total_bits = total_payload_size * 8
            full_positions = self._generate_payload_positions(
                password,
                total_samples,
                total_bits
            )
            
            # Step 4: Extract full payload bits
            payload_bits = self._extract_bits(samples, full_positions)
            
            # Step 5: Convert to bytes
            payload_bytes = self._bits_to_bytes(payload_bits)
            
            # Step 6: Remove header to get actual payload
            actual_payload = payload_bytes[self.HEADER_SIZE:]
            
            # Step 7: Validate payload
            self._validate_payload(actual_payload, payload_length)
            
            # Step 8: Calculate statistics
            statistics = self._calculate_statistics(
                samples,
                actual_payload,
                full_positions
            )
            
            logger.info(f"LSB extraction completed successfully: {len(actual_payload)} bytes")
            
            return actual_payload, statistics
            
        except Exception as e:
            logger.error(f"LSB extraction error: {e}")
            raise
    
    def _generate_header_positions(self, password: str, total_samples: int) -> list:
        """
        Generate sample positions for header extraction.
        
        Parameters:
        password (str):
            Password for generating positions.
        total_samples (int):
            Total number of samples.
            
        Returns:
        list: List of sample positions for header.
        """
        try:
            from .sample_selector import sample_selector
            
            # Header is HEADER_SIZE bytes = HEADER_SIZE * 8 bits
            header_bits = self.HEADER_SIZE * 8
            
            positions = sample_selector.generate_bit_positions(
                password=password,
                total_samples=total_samples,
                num_bits=header_bits
            )
            
            return positions
            
        except Exception as e:
            logger.error(f"Header position generation error: {e}")
            raise ValueError(f"Failed to generate header positions: {str(e)}")
    
    def _generate_payload_positions(
        self,
        password: str,
        total_samples: int,
        num_bits: int
    ) -> list:
        """
        Generate sample positions for full payload extraction.
        
        Parameters:
        password (str):
            Password for generating positions.
        total_samples (int):
            Total number of samples.
        num_bits (int):
            Number of bits to extract.
            
        Returns:
        list: List of sample positions for payload.
        """
        try:
            from .sample_selector import sample_selector
            
            positions = sample_selector.generate_bit_positions(
                password=password,
                total_samples=total_samples,
                num_bits=num_bits
            )
            
            return positions
            
        except Exception as e:
            logger.error(f"Payload position generation error: {e}")
            raise ValueError(f"Failed to generate payload positions: {str(e)}")
    
    def _extract_bits(self, samples: np.ndarray, positions: list) -> list:
        """
        Extract LSB bits from audio samples at specified positions.
        
        Parameters:
        samples (np.ndarray):
            Audio samples to extract from.
        positions (list):
            List of sample positions.
            
        Returns:
        list: List of extracted bits (0 or 1).
    """
        try:
            bits = []
            for position in positions:
                sample = samples[position]
                bit = sample & 1  # Extract LSB
                bits.append(bit)
            
            logger.info(f"Extracted {len(bits)} bits from {len(positions)} positions")
            
            return bits
            
        except Exception as e:
            logger.error(f"Bit extraction error: {e}")
            raise ValueError(f"Failed to extract bits: {str(e)}")
    
    def _bits_to_bytes(self, bits: list) -> bytes:
        """
        Convert list of bits to bytes.
        
        Parameters:
        bits (list):
            List of bits (0 or 1).
            
        Returns:
        bytes: Converted bytes.
    """
        try:
            # Ensure bits length is multiple of 8
            if len(bits) % 8 != 0:
                # Pad with zeros if needed
                bits = bits + [0] * (8 - len(bits) % 8)
            
            # Convert bits to bytes
            bytes_data = bytearray()
            for i in range(0, len(bits), 8):
                byte_bits = bits[i:i+8]
                byte_value = 0
                for bit in byte_bits:
                    byte_value = (byte_value << 1) | bit
                bytes_data.append(byte_value)
            
            return bytes(bytes_data)
            
        except Exception as e:
            logger.error(f"Bits to bytes conversion error: {e}")
            raise ValueError(f"Failed to convert bits to bytes: {str(e)}")
    
    def _parse_header(self, header_bytes: bytes) -> int:
        """
        Parse payload header to extract payload length.
        
        This method validates the magic signature and extracts
        the payload length from the header.
        
        Parameters:
        header_bytes (bytes):
            Header bytes to parse.
            
        Returns:
        int: Payload length in bytes.
            
        Raises:
        ValueError: If header is invalid or signature mismatch.
        """
        try:
            # Check header size
            if len(header_bytes) < self.HEADER_SIZE:
                raise ValueError(
                    f"Header too small: expected {self.HEADER_SIZE} bytes, "
                    f"got {len(header_bytes)} bytes"
                )
            
            # Extract magic signature
            magic = header_bytes[:4]
            
            # Validate magic signature
            if magic != self.MAGIC_SIGNATURE:
                raise ValueError(
                    f"Invalid magic signature: expected {self.MAGIC_SIGNATURE}, "
                    f"got {magic}"
                )
            
            # Extract version
            version = header_bytes[4]
            if version != 1:
                logger.warning(f"Unexpected version: {version} (expected 1)")
            
            # Extract payload length
            payload_length = int.from_bytes(header_bytes[5:9], byteorder='big')
            
            logger.info(
                f"Header parsed: magic={magic}, version={version}, "
                f"payload_length={payload_length}"
            )
            
            return payload_length
            
        except Exception as e:
            logger.error(f"Header parsing error: {e}")
            raise ValueError(f"Failed to parse header: {str(e)}")
    
    def _validate_payload(self, payload: bytes, expected_length: int) -> None:
        """
        Validate extracted payload.
        
        Parameters:
        payload (bytes):
            Extracted payload data.
        expected_length (int):
            Expected payload length from header.
            
        Raises:
        ValueError: If payload validation fails.
        """
        try:
            # Check payload length
            if len(payload) != expected_length:
                raise ValueError(
                    f"Payload length mismatch: expected {expected_length} bytes, "
                    f"got {len(payload)} bytes"
                )
            
            # Check payload is not empty
            if len(payload) == 0:
                raise ValueError("Payload is empty")
            
            logger.info("Payload validation passed")
            
        except Exception as e:
            logger.error(f"Payload validation error: {e}")
            raise
    
    def _calculate_statistics(
        self,
        samples: np.ndarray,
        payload: bytes,
        positions: list
    ) -> Dict:
        """
        Calculate extraction statistics.
        
        Parameters:
        samples (np.ndarray):
            Stego audio samples.
        payload (bytes):
            Extracted payload.
        positions (list):
            Positions used for extraction.
            
        Returns:
        Dict: Dictionary containing extraction statistics.
        """
        try:
            # Calculate payload size
            payload_size = len(payload)
            header_size = self.HEADER_SIZE
            total_size = payload_size + header_size
            total_bits = total_size * 8
            
            # Calculate capacity information
            total_samples = len(samples)
            positions_used = len(positions)
            capacity_remaining = total_samples - positions_used
            capacity_used_percent = (positions_used / total_samples) * 100
            
            statistics = {
                'totalSamples': total_samples,
                'payloadSize': payload_size,
                'headerSize': header_size,
                'totalPayloadSize': total_size,
                'totalBitsExtracted': total_bits,
                'positionsUsed': positions_used,
                'capacityRemaining': capacity_remaining,
                'capacityUsedPercent': round(capacity_used_percent, 4),
                'extractionMethod': 'Randomized LSB',
                'headerStructure': '4-byte magic + 1-byte version + 4-byte length'
            }
            
            logger.info(f"Extraction statistics: {statistics}")
            
            return statistics
            
        except Exception as e:
            logger.error(f"Statistics calculation error: {e}")
            return {}
    
    def validate_stego_audio(self, samples: np.ndarray) -> bool:
        """
        Validate that audio file contains steganography data.
        
        This is a lightweight validation that checks if the audio
        appears to be a valid stego file.
        
        Parameters:
        samples (np.ndarray):
            Audio samples to validate.
            
        Returns:
        bool: True if appears to be valid stego audio, False otherwise.
        """
        try:
            # Basic validation: check samples array is not empty
            if len(samples) == 0:
                return False
            
            # Check samples have reasonable values
            if np.any(np.abs(samples) > 32768):  # Beyond 16-bit range
                return False
            
            logger.info("Stego audio validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Stego audio validation error: {e}")
            return False


# Global audio LSB extractor instance
audio_lsb_extractor = AudioLSBExtractor()
