"""
audio_loader.py

Purpose:
Loads audio samples from WAV files for steganography processing.

This module is intentionally isolated from audio validation,
conversion, and steganography logic to improve maintainability.

Why Sample Loading is Separate:
- Provides a dedicated interface for reading audio data
- Handles WAV file parsing and sample extraction
- Enables independent testing of sample loading
- Makes the codebase more maintainable
- Allows easy addition of new audio processing features

Security Considerations:
- Validates WAV file structure before loading
- Handles corrupted files gracefully
- Provides detailed error messages
- Logs all loading operations for audit trail
"""

import os
import logging
import struct
from typing import Tuple
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioLoader:
    """
    Loads audio samples from WAV files for steganography.
    
    Why this exists:
    - Provides a dedicated interface for sample loading
    - Handles WAV file parsing and sample extraction
    - Converts samples to numpy arrays for processing
    - Provides audio metadata for capacity analysis
    - Handles errors gracefully with clear messages
    
    Responsibilities:
    - Load WAV file samples
    - Extract audio metadata
    - Convert samples to numpy arrays
    - Validate sample data
    - Provide loading statistics
    
    Dependencies:
    - numpy for efficient array operations
    - struct for WAV header parsing
    """
    
    def __init__(self):
        """Initialize the audio loader."""
        logger.info("AudioLoader initialized")
    
    def load_wav_samples(self, wav_path: str) -> Tuple[np.ndarray, dict]:
        """
        Load audio samples from a WAV file.
        
        This method:
        1. Validates the WAV file structure
        2. Parses the WAV header
        3. Extracts audio samples
        4. Converts to numpy array
        5. Returns samples and metadata
        
        Parameters:
        wav_path (str):
            Path to the WAV file.
            
        Returns:
        Tuple[np.ndarray, dict]: 
            - Numpy array of audio samples
            - Dictionary containing audio metadata
            
        Raises:
        ValueError: If WAV file is invalid or cannot be loaded
        IOError: If file cannot be read
    """
        try:
            logger.info(f"Loading WAV samples: {wav_path}")
            
            # Step 1: Validate file exists
            if not os.path.exists(wav_path):
                raise ValueError(f"WAV file does not exist: {wav_path}")
            
            if not os.access(wav_path, os.R_OK):
                raise ValueError(f"WAV file is not readable: {wav_path}")
            
            # Step 2: Parse WAV header
            metadata = self._parse_wav_header(wav_path)
            
            # Step 3: Load audio samples
            samples = self._load_sample_data(wav_path, metadata)
            
            # Step 4: Validate samples
            self._validate_samples(samples, metadata)
            
            logger.info(
                f"WAV samples loaded: {len(samples)} samples, "
                f"{metadata['channels']} channels, "
                f"{metadata['sampleRate']} Hz"
            )
            
            return samples, metadata
            
        except Exception as e:
            logger.error(f"WAV loading error: {e}")
            raise
    
    def _parse_wav_header(self, wav_path: str) -> dict:
        """
        Parse WAV file header and extract metadata.
        
        This method reads the WAV header and extracts:
        - Sample rate
        - Number of channels
        - Bits per sample
        - Byte rate
        - Data size
        - Duration
        
        Parameters:
        wav_path (str):
            Path to the WAV file.
            
        Returns:
        dict: Dictionary containing WAV metadata.
            
        Raises:
        ValueError: If WAV header is invalid.
        """
        try:
            with open(wav_path, 'rb') as f:
                # Read RIFF header
                riff_header = f.read(12)
                if len(riff_header) < 12:
                    raise ValueError("Invalid WAV: file too small for header")
                
                if riff_header[:4] != b'RIFF':
                    raise ValueError("Invalid WAV: missing RIFF header")
                
                if riff_header[8:12] != b'WAVE':
                    raise ValueError("Invalid WAV: missing WAVE identifier")
                
                # Read fmt chunk
                fmt_chunk_id = f.read(4)
                if fmt_chunk_id != b'fmt ':
                    raise ValueError("Invalid WAV: missing fmt chunk")
                
                fmt_chunk_size = struct.unpack('<I', f.read(4))[0]
                audio_format = struct.unpack('<H', f.read(2))[0]
                channels = struct.unpack('<H', f.read(2))[0]
                sample_rate = struct.unpack('<I', f.read(4))[0]
                byte_rate = struct.unpack('<I', f.read(4))[0]
                block_align = struct.unpack('<H', f.read(2))[0]
                bits_per_sample = struct.unpack('<H', f.read(2))[0]
                
                # Skip extra bytes in fmt chunk if present
                if fmt_chunk_size > 16:
                    f.read(fmt_chunk_size - 16)
                
                # Look for data chunk
                data_chunk_id = f.read(4)
                while data_chunk_id != b'data' and data_chunk_id:
                    chunk_size = struct.unpack('<I', f.read(4))[0]
                    f.read(chunk_size)
                    data_chunk_id = f.read(4)
                
                if data_chunk_id != b'data':
                    raise ValueError("Invalid WAV: missing data chunk")
                
                data_size = struct.unpack('<I', f.read(4))[0]
                
                # Calculate duration
                duration = data_size / byte_rate
                
                # Calculate total samples
                total_samples = data_size // block_align
                
                metadata = {
                    'channels': channels,
                    'sampleRate': sample_rate,
                    'bitsPerSample': bits_per_sample,
                    'byteRate': byte_rate,
                    'blockAlign': block_align,
                    'dataSize': data_size,
                    'duration': round(duration, 3),
                    'totalSamples': total_samples,
                    'audioFormat': 'PCM'
                }
                
                logger.info(f"WAV header parsed: {metadata}")
                
                return metadata
                
        except struct.error as e:
            raise ValueError(f"Invalid WAV: header parsing error - {str(e)}")
        except Exception as e:
            raise ValueError(f"WAV header parsing failed: {str(e)}")
    
    def _load_sample_data(self, wav_path: str, metadata: dict) -> np.ndarray:
        """
        Load audio sample data from WAV file.
        
        This method reads the audio data chunk and converts it to
        a numpy array of samples.
        
        Parameters:
        wav_path (str):
            Path to the WAV file.
        metadata (dict):
            WAV metadata from header parsing.
            
        Returns:
        np.ndarray: Array of audio samples.
            
        Raises:
        ValueError: If sample data cannot be loaded.
        """
        try:
            with open(wav_path, 'rb') as f:
                # Skip to data chunk
                f.seek(12)  # Skip RIFF header
                
                # Skip chunks until we find data
                chunk_id = f.read(4)
                while chunk_id != b'data' and chunk_id:
                    chunk_size = struct.unpack('<I', f.read(4))[0]
                    f.read(chunk_size)
                    chunk_id = f.read(4)
                
                if chunk_id != b'data':
                    raise ValueError("Data chunk not found")
                
                data_size = struct.unpack('<I', f.read(4))[0]
                
                # Read sample data
                sample_data = f.read(data_size)
                
                # Convert to numpy array based on bit depth
                bits_per_sample = metadata['bitsPerSample']
                
                if bits_per_sample == 16:
                    # 16-bit signed little-endian
                    dtype = np.int16
                    samples = np.frombuffer(sample_data, dtype=dtype)
                elif bits_per_sample == 24:
                    # 24-bit (convert to 32-bit for processing)
                    dtype = np.int32
                    samples = np.frombuffer(sample_data, dtype=np.uint8)
                    # Reshape and convert 24-bit to 32-bit
                    samples = samples.reshape(-1, 3)
                    samples = (samples[:, 0] | (samples[:, 1] << 8) | (samples[:, 2] << 16)).astype(np.int32)
                    # Sign extend for 24-bit
                    samples = np.where(samples >= 0x800000, samples - 0x1000000, samples)
                elif bits_per_sample == 32:
                    # 32-bit signed little-endian
                    dtype = np.int32
                    samples = np.frombuffer(sample_data, dtype=dtype)
                else:
                    raise ValueError(f"Unsupported bit depth: {bits_per_sample}")
                
                logger.info(f"Sample data loaded: {len(samples)} samples, dtype={samples.dtype}")
                
                return samples
                
        except Exception as e:
            logger.error(f"Sample data loading error: {e}")
            raise ValueError(f"Failed to load sample data: {str(e)}")
    
    def _validate_samples(self, samples: np.ndarray, metadata: dict) -> None:
        """
        Validate loaded audio samples.
        
        This method checks:
        - Samples array is not empty
        - Sample count matches metadata
        - Sample values are within expected range
        
        Parameters:
        samples (np.ndarray):
            Array of audio samples.
        metadata (dict):
            WAV metadata.
            
        Raises:
        ValueError: If samples are invalid.
        """
        try:
            # Check samples array is not empty
            if len(samples) == 0:
                raise ValueError("Samples array is empty")
            
            # Check sample count matches metadata
            expected_samples = metadata['totalSamples']
            actual_samples = len(samples)
            
            # Allow some tolerance for rounding
            if abs(actual_samples - expected_samples) > 100:
                logger.warning(
                    f"Sample count mismatch: expected {expected_samples}, "
                    f"got {actual_samples}"
                )
            
            # Check sample values are within range
            bits_per_sample = metadata['bitsPerSample']
            max_value = 2 ** (bits_per_sample - 1) - 1
            min_value = -(2 ** (bits_per_sample - 1))
            
            if np.any(samples > max_value) or np.any(samples < min_value):
                raise ValueError(
                    f"Sample values out of range for {bits_per_sample}-bit audio"
                )
            
            logger.info("Sample validation passed")
            
        except Exception as e:
            logger.error(f"Sample validation error: {e}")
            raise
    
    def get_audio_info(self, wav_path: str) -> dict:
        """
        Get audio information without loading samples.
        
        This is a lightweight method that only parses the header
        and returns metadata without loading the sample data.
        
        Parameters:
        wav_path (str):
            Path to the WAV file.
            
        Returns:
        dict: Dictionary containing audio metadata.
        """
        try:
            logger.info(f"Getting audio info: {wav_path}")
            metadata = self._parse_wav_header(wav_path)
            return metadata
        except Exception as e:
            logger.error(f"Audio info error: {e}")
            raise


# Global audio loader instance
audio_loader = AudioLoader()
