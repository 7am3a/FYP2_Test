"""
audio_lsb_embedder.py

Purpose:
Embeds encrypted payload bits into WAV audio samples using
deterministic randomized LSB steganography.

This module is intentionally isolated from audio conversion,
payload serialization, and extraction logic to improve maintainability.

Why LSB Embedding:
- Least Significant Bit modification is minimally audible
- Provides sufficient capacity for text messages
- Well-understood steganography technique
- Can be made secure through randomization
- Preserves audio quality effectively

Security Considerations:
- Uses randomized sample positions (not sequential)
- Password-derived positions prevent detection
- Embeds structured payload with header
- Performs integrity verification after embedding
- Logs all embedding operations for audit trail
"""

import logging
from typing import Tuple, Dict
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioLSBEmbedder:
    """
    Embeds payload bits into audio samples using LSB steganography.
    
    Why this exists:
    - Provides a dedicated interface for LSB embedding
    - Implements randomized sample selection
    - Handles payload header construction
    - Performs integrity verification
    - Provides embedding statistics for debugging
    
    Responsibilities:
    - Embed payload bits into audio samples
    - Construct payload header with metadata
    - Use randomized sample positions
    - Verify embedding integrity
    - Calculate capacity and statistics
    
    Header Structure:
    - Magic Signature (4 bytes): "STEG"
    - Version (1 byte): Payload version
    - Payload Length (4 bytes): Size of payload in bytes
    - Payload Data (variable): Actual encrypted payload
    
    Dependencies:
    - numpy for efficient array operations
    - sample_selector for randomized positions
    """
    
    # Header constants
    MAGIC_SIGNATURE = b'STEG'
    HEADER_SIZE = 9  # 4 bytes magic + 1 byte version + 4 bytes length
    
    def __init__(self):
        """Initialize the LSB embedder."""
        logger.info("AudioLSBEmbedder initialized")
    
    def embed(
        self,
        samples: np.ndarray,
        payload: bytes,
        positions: list
    ) -> Tuple[np.ndarray, Dict]:
        """
        Embed payload bits into audio samples using LSB steganography.
        
        This method:
        1. Constructs payload header
        2. Combines header with payload
        3. Converts to binary bit stream
        4. Embeds bits at randomized positions
        5. Verifies embedding integrity
        6. Returns modified samples and statistics
        
        Parameters:
        samples (np.ndarray):
            Original audio samples.
        payload (bytes):
            Encrypted payload data to embed.
        positions (list):
            List of sample positions for embedding.
            
        Returns:
        Tuple[np.ndarray, Dict]: 
            - Modified audio samples with embedded payload
            - Dictionary containing embedding statistics
            
        Raises:
        ValueError: If embedding fails or capacity insufficient
    """
        try:
            logger.info(f"Starting LSB embedding: {len(payload)} bytes payload")
            
            # Step 1: Construct full payload with header
            full_payload = self._construct_payload(payload)
            logger.info(f"Full payload size: {len(full_payload)} bytes")
            
            # Step 2: Convert to bit stream
            bit_stream = self._bytes_to_bits(full_payload)
            logger.info(f"Bit stream length: {len(bit_stream)} bits")
            
            # Step 3: Validate capacity
            if len(bit_stream) > len(positions):
                raise ValueError(
                    f"Insufficient capacity: need {len(bit_stream)} bits, "
                    f"have {len(positions)} positions"
                )
            
            # Step 4: Create copy of samples to avoid modifying original
            stego_samples = samples.copy()
            
            # Step 5: Embed bits at randomized positions
            self._embed_bits(stego_samples, bit_stream, positions)
            
            # Step 6: Verify embedding
            verification_passed = self._verify_embedding(
                stego_samples,
                bit_stream,
                positions
            )
            
            if not verification_passed:
                raise ValueError("Embedding verification failed")
            
            # Step 7: Calculate statistics
            statistics = self._calculate_statistics(
                samples,
                stego_samples,
                payload,
                positions
            )
            
            logger.info(f"LSB embedding completed successfully")
            
            return stego_samples, statistics
            
        except Exception as e:
            logger.error(f"LSB embedding error: {e}")
            raise
    
    def _construct_payload(self, payload: bytes) -> bytes:
        """
        Construct full payload with header.
        
        This method adds a header to the payload containing:
        - Magic signature for identification
        - Version for compatibility
        - Payload length for extraction
        
        Parameters:
        payload (bytes):
            Raw payload data.
            
        Returns:
        bytes: Full payload with header.
        """
        try:
            # Calculate payload length
            payload_length = len(payload)
            
            # Construct header
            header = (
                self.MAGIC_SIGNATURE +
                bytes([1]) +  # Version 1
                payload_length.to_bytes(4, byteorder='big')
            )
            
            # Combine header and payload
            full_payload = header + payload
            
            logger.info(
                f"Payload constructed: header={len(header)} bytes, "
                f"data={payload_length} bytes, total={len(full_payload)} bytes"
            )
            
            return full_payload
            
        except Exception as e:
            logger.error(f"Payload construction error: {e}")
            raise ValueError(f"Failed to construct payload: {str(e)}")
    
    def _bytes_to_bits(self, data: bytes) -> list:
        """
        Convert bytes to list of bits.
        
        Parameters:
        data (bytes):
            Data to convert.
            
        Returns:
        list: List of bits (0 or 1).
        """
        try:
            bits = []
            for byte in data:
                # Convert each byte to 8 bits
                for i in range(8):
                    bits.append((byte >> (7 - i)) & 1)
            
            return bits
            
        except Exception as e:
            logger.error(f"Bytes to bits conversion error: {e}")
            raise ValueError(f"Failed to convert bytes to bits: {str(e)}")
    
    def _embed_bits(
        self,
        samples: np.ndarray,
        bit_stream: list,
        positions: list
    ) -> None:
        """
        Embed bits into audio samples at specified positions.
        
        This method modifies the LSB of each sample at the
        specified positions to embed the bit stream.
        
        Parameters:
        samples (np.ndarray):
            Audio samples to modify (modified in-place).
        bit_stream (list):
            List of bits to embed.
        positions (list):
            List of sample positions for embedding.
    """
        try:
            # Embed each bit at its corresponding position
            for i, bit in enumerate(bit_stream):
                position = positions[i]
                
                # Get current sample value
                sample = samples[position]
                
                # Clear the LSB (set to 0)
                sample_cleared = sample & ~1
                
                # Set LSB to the bit value
                sample_modified = sample_cleared | bit
                
                # Update sample
                samples[position] = sample_modified
            
            logger.info(f"Embedded {len(bit_stream)} bits into {len(positions)} positions")
            
        except Exception as e:
            logger.error(f"Bit embedding error: {e}")
            raise ValueError(f"Failed to embed bits: {str(e)}")
    
    def _verify_embedding(
        self,
        samples: np.ndarray,
        bit_stream: list,
        positions: list
    ) -> bool:
        """
        Verify that bits were embedded correctly.
        
        This method extracts the bits from the embedded positions
        and compares them with the original bit stream.
        
        Parameters:
        samples (np.ndarray):
            Modified audio samples.
        bit_stream (list):
            Original bit stream that was embedded.
        positions (list):
            Positions where bits were embedded.
            
        Returns:
        bool: True if verification passed, False otherwise.
        """
        try:
            # Extract bits from embedded positions
            extracted_bits = []
            for i in range(len(bit_stream)):
                position = positions[i]
                sample = samples[position]
                bit = sample & 1  # Extract LSB
                extracted_bits.append(bit)
            
            # Compare with original
            if extracted_bits == bit_stream:
                logger.info("Embedding verification passed")
                return True
            else:
                logger.error("Embedding verification failed: bits mismatch")
                return False
                
        except Exception as e:
            logger.error(f"Embedding verification error: {e}")
            return False
    
    def _calculate_statistics(
        self,
        original_samples: np.ndarray,
        stego_samples: np.ndarray,
        payload: bytes,
        positions: list
    ) -> Dict:
        """
        Calculate embedding statistics.
        
        Parameters:
        original_samples (np.ndarray):
            Original audio samples.
        stego_samples (np.ndarray):
            Modified audio samples.
        payload (bytes):
            Embedded payload.
        positions (list):
            Positions used for embedding.
            
        Returns:
        Dict: Dictionary containing embedding statistics.
        """
        try:
            # Calculate payload size
            payload_size = len(payload)
            header_size = self.HEADER_SIZE
            total_size = payload_size + header_size
            total_bits = total_size * 8
            
            # Calculate capacity used
            total_samples = len(original_samples)
            capacity_used = len(positions)
            capacity_remaining = total_samples - capacity_used
            capacity_used_percent = (capacity_used / total_samples) * 100
            
            # Calculate distortion (SNR approximation)
            diff = stego_samples - original_samples
            distortion = np.sum(np.abs(diff))
            max_possible_distortion = len(positions)  # Each bit changes at most 1
            distortion_percent = (distortion / max_possible_distortion) * 100 if max_possible_distortion > 0 else 0
            
            statistics = {
                'totalSamples': total_samples,
                'payloadSize': payload_size,
                'headerSize': header_size,
                'totalPayloadSize': total_size,
                'totalBitsEmbedded': total_bits,
                'positionsUsed': len(positions),
                'capacityRemaining': capacity_remaining,
                'capacityUsedPercent': round(capacity_used_percent, 4),
                'distortion': round(distortion, 2),
                'distortionPercent': round(distortion_percent, 4),
                'embeddingMethod': 'Randomized LSB',
                'headerStructure': '4-byte magic + 1-byte version + 4-byte length'
            }
            
            logger.info(f"Embedding statistics: {statistics}")
            
            return statistics
            
        except Exception as e:
            logger.error(f"Statistics calculation error: {e}")
            return {}
    
    def calculate_capacity(self, total_samples: int) -> Dict:
        """
        Calculate embedding capacity for audio file.
        
        Parameters:
        total_samples (int):
            Total number of audio samples.
            
        Returns:
        Dict: Dictionary containing capacity information.
        """
        try:
            # Each sample can hold 1 bit
            total_capacity_bits = total_samples
            
            # Reserve space for header
            header_bits = self.HEADER_SIZE * 8
            available_capacity_bits = total_capacity_bits - header_bits
            available_capacity_bytes = available_capacity_bits // 8
            
            capacity_info = {
                'totalSamples': total_samples,
                'totalCapacityBits': total_capacity_bits,
                'headerSizeBits': header_bits,
                'headerSizeBytes': self.HEADER_SIZE,
                'availableCapacityBits': available_capacity_bits,
                'availableCapacityBytes': available_capacity_bytes
            }
            
            logger.info(f"Capacity calculated: {capacity_info}")
            
            return capacity_info
            
        except Exception as e:
            logger.error(f"Capacity calculation error: {e}")
            raise ValueError(f"Failed to calculate capacity: {str(e)}")


# Global audio LSB embedder instance
audio_lsb_embedder = AudioLSBEmbedder()
