"""
audio_writer.py

Purpose:
Generates WAV output files from modified audio samples.

This module is intentionally isolated from audio validation,
conversion, and steganography logic to improve maintainability.

Why Sample Writing is Separate:
- Provides a dedicated interface for writing WAV files
- Handles WAV file construction and sample encoding
- Enables independent testing of file generation
- Makes the codebase more maintainable
- Allows easy addition of new output features

Security Considerations:
- Validates sample data before writing
- Ensures proper WAV file structure
- Handles file I/O errors gracefully
- Logs all write operations for audit trail
"""

import os
import logging
import struct
import tempfile
from typing import Tuple
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioWriter:
    """
    Writes audio samples to WAV files.
    
    Why this exists:
    - Provides a dedicated interface for WAV file generation
    - Handles WAV header construction
    - Encodes samples to binary format
    - Manages output file creation
    - Provides writing statistics for debugging
    
    Responsibilities:
    - Write WAV files from sample arrays
    - Construct proper WAV headers
    - Encode samples to binary format
    - Validate output files
    - Manage temporary file lifecycle
    
    Dependencies:
    - numpy for array operations
    - struct for binary encoding
    """
    
    def __init__(self):
        """Initialize the audio writer."""
        logger.info("AudioWriter initialized")
    
    def write_wav_file(
        self,
        samples: np.ndarray,
        output_path: str,
        sample_rate: int = 44100,
        channels: int = 2,
        bits_per_sample: int = 16
    ) -> dict:
        """
        Write audio samples to a WAV file.
        
        This method:
        1. Validates sample data
        2. Constructs WAV header
        3. Encodes samples to binary
        4. Writes WAV file
        5. Validates output
        6. Returns statistics
        
        Parameters:
        samples (np.ndarray):
            Array of audio samples.
        output_path (str):
            Path for the output WAV file.
        sample_rate (int):
            Sample rate in Hz (default: 44100).
        channels (int):
            Number of channels (default: 2).
        bits_per_sample (int):
            Bits per sample (default: 16).
            
        Returns:
        dict: Dictionary containing write statistics.
            
        Raises:
        ValueError: If samples are invalid or writing fails
        IOError: If file cannot be written
    """
        try:
            logger.info(f"Writing WAV file: {output_path}")
            
            # Step 1: Validate samples
            self._validate_samples(samples, bits_per_sample)
            
            # Step 2: Calculate audio parameters
            byte_rate = sample_rate * channels * (bits_per_sample // 8)
            block_align = channels * (bits_per_sample // 8)
            
            # Step 3: Encode samples to bytes
            sample_data = self._encode_samples(samples, bits_per_sample)
            data_size = len(sample_data)
            
            # Step 4: Construct WAV header
            header = self._construct_wav_header(
                data_size,
                sample_rate,
                channels,
                bits_per_sample,
                byte_rate,
                block_align
            )
            
            # Step 5: Write WAV file
            with open(output_path, 'wb') as f:
                f.write(header)
                f.write(sample_data)
            
            # Step 6: Validate output
            if not os.path.exists(output_path):
                raise ValueError("Output file was not created")
            
            file_size = os.path.getsize(output_path)
            if file_size == 0:
                raise ValueError("Output file is empty")
            
            # Calculate duration
            duration = data_size / byte_rate
            total_samples = data_size // block_align
            
            statistics = {
                'outputPath': output_path,
                'fileSize': file_size,
                'sampleRate': sample_rate,
                'channels': channels,
                'bitsPerSample': bits_per_sample,
                'byteRate': byte_rate,
                'blockAlign': block_align,
                'dataSize': data_size,
                'duration': round(duration, 3),
                'totalSamples': total_samples,
                'samplesWritten': len(samples)
            }
            
            logger.info(f"WAV file written successfully: {statistics}")
            
            return statistics
            
        except Exception as e:
            logger.error(f"WAV writing error: {e}")
            raise
    
    def _validate_samples(self, samples: np.ndarray, bits_per_sample: int) -> None:
        """
        Validate audio samples before writing.
        
        This method checks:
        - Samples array is not empty
        - Sample values are within valid range
        - Data type is appropriate
        
        Parameters:
        samples (np.ndarray):
            Array of audio samples.
        bits_per_sample (int):
            Bits per sample for range validation.
            
        Raises:
        ValueError: If samples are invalid.
        """
        try:
            # Check samples array is not empty
            if len(samples) == 0:
                raise ValueError("Samples array is empty")
            
            # Check sample values are within range
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
    
    def _encode_samples(self, samples: np.ndarray, bits_per_sample: int) -> bytes:
        """
        Encode audio samples to binary format.
        
        This method converts numpy array samples to binary bytes
        in the appropriate format for WAV files.
        
        Parameters:
        samples (np.ndarray):
            Array of audio samples.
        bits_per_sample (int):
            Bits per sample for encoding.
            
        Returns:
        bytes: Binary encoded sample data.
            
        Raises:
        ValueError: If encoding fails.
        """
        try:
            # Convert samples to appropriate dtype
            if bits_per_sample == 16:
                # 16-bit signed little-endian
                samples_int16 = samples.astype(np.int16)
                return samples_int16.tobytes()
            elif bits_per_sample == 24:
                # 24-bit (convert from 32-bit)
                samples_int32 = samples.astype(np.int32)
                # Convert to 24-bit
                samples_24bit = samples_int32 & 0xFFFFFF
                # Pack as 3 bytes per sample
                sample_bytes = bytearray()
                for sample in samples_24bit:
                    sample_bytes.extend(sample.to_bytes(3, byteorder='little', signed=True))
                return bytes(sample_bytes)
            elif bits_per_sample == 32:
                # 32-bit signed little-endian
                samples_int32 = samples.astype(np.int32)
                return samples_int32.tobytes()
            else:
                raise ValueError(f"Unsupported bit depth: {bits_per_sample}")
                
        except Exception as e:
            logger.error(f"Sample encoding error: {e}")
            raise ValueError(f"Failed to encode samples: {str(e)}")
    
    def _construct_wav_header(
        self,
        data_size: int,
        sample_rate: int,
        channels: int,
        bits_per_sample: int,
        byte_rate: int,
        block_align: int
    ) -> bytes:
        """
        Construct WAV file header.
        
        This method creates a proper WAV header with all required
        chunks and metadata.
        
        Parameters:
        data_size (int):
            Size of the audio data in bytes.
        sample_rate (int):
            Sample rate in Hz.
        channels (int):
            Number of channels.
        bits_per_sample (int):
            Bits per sample.
        byte_rate (int):
            Byte rate (bytes per second).
        block_align (int):
            Block align (bytes per sample frame).
            
        Returns:
        bytes: WAV header as bytes.
        """
        try:
            # RIFF chunk
            riff = b'RIFF'
            file_size = 36 + data_size  # 36 for header, plus data
            file_size_bytes = struct.pack('<I', file_size)
            wave = b'WAVE'
            
            # fmt chunk
            fmt = b'fmt '
            fmt_chunk_size = struct.pack('<I', 16)  # PCM format chunk size
            audio_format = struct.pack('<H', 1)  # PCM
            channels_bytes = struct.pack('<H', channels)
            sample_rate_bytes = struct.pack('<I', sample_rate)
            byte_rate_bytes = struct.pack('<I', byte_rate)
            block_align_bytes = struct.pack('<H', block_align)
            bits_per_sample_bytes = struct.pack('<H', bits_per_sample)
            
            # data chunk
            data = b'data'
            data_size_bytes = struct.pack('<I', data_size)
            
            # Combine all parts
            header = (
                riff +
                file_size_bytes +
                wave +
                fmt +
                fmt_chunk_size +
                audio_format +
                channels_bytes +
                sample_rate_bytes +
                byte_rate_bytes +
                block_align_bytes +
                bits_per_sample_bytes +
                data +
                data_size_bytes
            )
            
            logger.info(f"WAV header constructed: {len(header)} bytes")
            
            return header
            
        except Exception as e:
            logger.error(f"Header construction error: {e}")
            raise ValueError(f"Failed to construct WAV header: {str(e)}")
    
    def create_stego_wav(
        self,
        samples: np.ndarray,
        original_path: str,
        metadata: dict = None
    ) -> str:
        """
        Create a stego WAV file with appropriate naming.
        
        This is a convenience method that creates a stego WAV file
        with "_stego" suffix in the filename.
        
        Parameters:
        samples (np.ndarray):
            Array of audio samples with embedded payload.
        original_path (str):
            Path to the original audio file.
        metadata (dict, optional):
            Audio metadata (sample rate, channels, etc.).
            
        Returns:
        str: Path to the created stego WAV file.
    """
        try:
            logger.info(f"Creating stego WAV from: {original_path}")
            
            # Get metadata if not provided
            if metadata is None:
                from .audio_loader import audio_loader
                metadata = audio_loader.get_audio_info(original_path)
            
            # Create output filename
            temp_dir = tempfile.gettempdir()
            base_name = os.path.splitext(os.path.basename(original_path))[0]
            stego_wav_path = os.path.join(temp_dir, f"{base_name}_stego.wav")
            
            # Ensure unique filename
            counter = 1
            while os.path.exists(stego_wav_path):
                stego_wav_path = os.path.join(temp_dir, f"{base_name}_stego_{counter}.wav")
                counter += 1
            
            # Write WAV file
            statistics = self.write_wav_file(
                samples=samples,
                output_path=stego_wav_path,
                sample_rate=metadata.get('sampleRate', 44100),
                channels=metadata.get('channels', 2),
                bits_per_sample=metadata.get('bitsPerSample', 16)
            )
            
            logger.info(f"Stego WAV created: {stego_wav_path}")
            
            return stego_wav_path
            
        except Exception as e:
            logger.error(f"Stego WAV creation error: {e}")
            raise
    
    def cleanup_file(self, file_path: str) -> None:
        """
        Clean up a WAV file.
        
        This method safely removes a WAV file with error handling.
        
        Parameters:
        file_path (str):
            Path to the file to remove.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up WAV file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup WAV file {file_path}: {e}")


# Global audio writer instance
audio_writer = AudioWriter()
