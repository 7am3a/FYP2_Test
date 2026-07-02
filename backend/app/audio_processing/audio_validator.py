"""
audio_validator.py

Purpose:
Validates audio file format, MIME type, corruption, sample rate,
channel count, and duration for steganography operations.

This module is intentionally isolated from audio conversion,
sample loading, and steganography logic to improve maintainability.

Why Validation is Critical:
- Prevents processing of corrupted or unsupported files
- Ensures audio meets quality requirements for steganography
- Provides clear error messages for unsupported formats
- Protects against malicious file uploads
- Enables early rejection of files that cannot be processed

Security Considerations:
- Validates file signatures to prevent extension spoofing
- Checks for file corruption before processing
- Verifies audio meets minimum quality requirements
- Logs all validation attempts for audit trail
"""

import os
import logging
from typing import Tuple, Optional
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioValidator:
    """
    Validates audio files for steganography operations.
    
    Why this exists:
    - Provides a dedicated interface for audio validation
    - Ensures only supported formats are processed
    - Detects corrupted files early in the pipeline
    - Validates audio quality parameters
    - Provides detailed error messages for debugging
    
    Responsibilities:
    - Validate file format (WAV, MP3, M4A, FLAC)
    - Check file integrity and corruption
    - Verify audio parameters (sample rate, channels, bit depth)
    - Calculate audio duration
    - Provide validation reports
    """
    
    # Supported audio formats
    SUPPORTED_FORMATS = ['.wav', '.mp3', '.m4a', '.flac']
    
    # File signatures (magic bytes) for format validation
    FILE_SIGNATURES = {
        b'RIFF': '.wav',
        b'ID3': '.mp3',
        b'\xff\xfb': '.mp3',
        b'\xff\xfa': '.mp3',
        b'\xff\xf3': '.mp3',
        b'\xff\xf2': '.mp3',
        b'ftypM4A': '.m4a',
        b'fLaC': '.flac'
    }
    
    # Minimum quality requirements
    MIN_SAMPLE_RATE = 8000  # 8 kHz minimum
    MIN_BIT_DEPTH = 16  # 16-bit minimum
    MAX_CHANNELS = 2  # Stereo maximum for better capacity
    MIN_DURATION_SECONDS = 1.0  # Minimum 1 second
    
    def __init__(self):
        """Initialize the audio validator."""
        logger.info("AudioValidator initialized")
    
    def validate_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate an audio file for steganography processing.
        
        This method performs comprehensive validation:
        1. Checks file exists and is readable
        2. Validates file extension
        3. Verifies file signature (magic bytes)
        4. Checks file size
        5. Validates format-specific structure
        
        Parameters:
        file_path (str):
            Path to the audio file to validate.
            
        Returns:
        Tuple[bool, Optional[str]]: 
            - True, None if file is valid
            - False, error_message if file is invalid
            
        Raises:
        IOError: If file cannot be read
        """
        try:
            logger.info(f"Validating audio file: {file_path}")
            
            # Step 1: Check file exists
            if not os.path.exists(file_path):
                error_msg = f"File does not exist: {file_path}"
                logger.error(error_msg)
                return False, error_msg
            
            # Step 2: Check file is readable
            if not os.access(file_path, os.R_OK):
                error_msg = f"File is not readable: {file_path}"
                logger.error(error_msg)
                return False, error_msg
            
            # Step 3: Validate file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.SUPPORTED_FORMATS:
                error_msg = (
                    f"Unsupported audio format: {file_ext}. "
                    f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
                )
                logger.error(error_msg)
                return False, error_msg
            
            # Step 4: Check file size
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                error_msg = "File is empty"
                logger.error(error_msg)
                return False, error_msg
            
            if file_size < 100:  # Minimum reasonable size
                error_msg = f"File too small: {file_size} bytes"
                logger.error(error_msg)
                return False, error_msg
            
            # Step 5: Validate file signature
            signature_error = self._validate_file_signature(file_path, file_ext)
            if signature_error:
                logger.error(signature_error)
                return False, signature_error
            
            # Step 6: Format-specific validation
            format_error = self._validate_format_specific(file_path, file_ext)
            if format_error:
                logger.error(format_error)
                return False, format_error
            
            logger.info(f"Audio file validation passed: {file_path}")
            return True, None
            
        except Exception as e:
            error_msg = f"Validation error: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def _validate_file_signature(self, file_path: str, expected_ext: str) -> Optional[str]:
        """
        Validate file signature (magic bytes) to prevent extension spoofing.
        
        This reads the first few bytes of the file and checks if they match
        the expected signature for the file extension.
        
        Parameters:
        file_path (str):
            Path to the audio file.
        expected_ext (str):
            Expected file extension.
            
        Returns:
        Optional[str]: Error message if signature is invalid, None otherwise.
        """
        try:
            with open(file_path, 'rb') as f:
                # Read first 12 bytes for signature detection
                header = f.read(12)
            
            # Check if header matches any known signature
            detected_format = None
            for signature, format_ext in self.FILE_SIGNATURES.items():
                if header.startswith(signature):
                    detected_format = format_ext
                    break
            
            # WAV files have RIFF at start
            if expected_ext == '.wav':
                if not header.startswith(b'RIFF'):
                    return "Invalid WAV file: missing RIFF header"
                # Check for WAVE format
                if len(header) >= 12 and header[8:12] != b'WAVE':
                    return "Invalid WAV file: missing WAVE identifier"
            
            # MP3 files can have various signatures
            elif expected_ext == '.mp3':
                if detected_format != '.mp3':
                    return "Invalid MP3 file: signature mismatch"
            
            # M4A files
            elif expected_ext == '.m4a':
                if not header.startswith(b'ftyp'):
                    return "Invalid M4A file: missing ftyp header"
                if b'M4A' not in header:
                    return "Invalid M4A file: missing M4A identifier"
            
            # FLAC files
            elif expected_ext == '.flac':
                if not header.startswith(b'fLaC'):
                    return "Invalid FLAC file: missing fLaC signature"
            
            return None
            
        except Exception as e:
            return f"Signature validation error: {str(e)}"
    
    def _validate_format_specific(self, file_path: str, file_ext: str) -> Optional[str]:
        """
        Perform format-specific validation checks.
        
        For WAV files, this validates the WAV header structure.
        For other formats, it performs basic sanity checks.
        
        Parameters:
        file_path (str):
            Path to the audio file.
        file_ext (str):
            File extension.
            
        Returns:
        Optional[str]: Error message if validation fails, None otherwise.
        """
        try:
            if file_ext == '.wav':
                return self._validate_wav_structure(file_path)
            else:
                # For non-WAV formats, we'll do basic validation
                # Full validation will happen during conversion
                return None
                
        except Exception as e:
            return f"Format-specific validation error: {str(e)}"
    
    def _validate_wav_structure(self, file_path: str) -> Optional[str]:
        """
        Validate WAV file structure and header.
        
        This checks:
        - RIFF header
        - WAVE format identifier
        - fmt chunk
        - data chunk
        - Audio parameters (sample rate, channels, bit depth)
        
        Parameters:
        file_path (str):
            Path to the WAV file.
            
        Returns:
        Optional[str]: Error message if structure is invalid, None otherwise.
        """
        try:
            with open(file_path, 'rb') as f:
                # Read RIFF header
                riff_header = f.read(12)
                if len(riff_header) < 12:
                    return "Invalid WAV: file too small for header"
                
                if riff_header[:4] != b'RIFF':
                    return "Invalid WAV: missing RIFF header"
                
                if riff_header[8:12] != b'WAVE':
                    return "Invalid WAV: missing WAVE identifier"
                
                # Read fmt chunk
                fmt_chunk_id = f.read(4)
                if fmt_chunk_id != b'fmt ':
                    return "Invalid WAV: missing fmt chunk"
                
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
                    # Skip non-data chunks
                    chunk_size = struct.unpack('<I', f.read(4))[0]
                    f.read(chunk_size)
                    data_chunk_id = f.read(4)
                
                if data_chunk_id != b'data':
                    return "Invalid WAV: missing data chunk"
                
                # Validate audio parameters
                if audio_format != 1:  # PCM
                    return f"Invalid WAV: unsupported audio format {audio_format}. Only PCM is supported."
                
                if channels not in [1, 2]:
                    return f"Invalid WAV: unsupported channel count {channels}. Only mono and stereo are supported."
                
                if sample_rate < self.MIN_SAMPLE_RATE:
                    return f"Invalid WAV: sample rate {sample_rate} below minimum {self.MIN_SAMPLE_RATE}"
                
                if bits_per_sample < self.MIN_BIT_DEPTH:
                    return f"Invalid WAV: bit depth {bits_per_sample} below minimum {self.MIN_BIT_DEPTH}"
                
                logger.info(
                    f"WAV structure valid: {channels} channels, "
                    f"{sample_rate} Hz, {bits_per_sample}-bit"
                )
                
                return None
                
        except struct.error as e:
            return f"Invalid WAV: header parsing error - {str(e)}"
        except Exception as e:
            return f"WAV validation error: {str(e)}"
    
    def get_audio_info(self, file_path: str) -> dict:
        """
        Extract audio file information.
        
        This method returns detailed information about the audio file
        including format, duration, sample rate, channels, etc.
        
        Parameters:
        file_path (str):
            Path to the audio file.
            
        Returns:
        dict: Dictionary containing audio information.
            
        Raises:
        ValueError: If file cannot be parsed.
        """
        try:
            logger.info(f"Extracting audio info: {file_path}")
            
            file_ext = os.path.splitext(file_path)[1].lower()
            file_size = os.path.getsize(file_path)
            
            info = {
                'filePath': file_path,
                'fileExtension': file_ext,
                'fileSize': file_size,
                'format': file_ext[1:].upper()
            }
            
            # For WAV files, extract detailed info from header
            if file_ext == '.wav':
                wav_info = self._extract_wav_info(file_path)
                info.update(wav_info)
            
            logger.info(f"Audio info extracted: {info}")
            return info
            
        except Exception as e:
            logger.error(f"Audio info extraction error: {e}")
            raise ValueError(f"Failed to extract audio info: {str(e)}")
    
    def _extract_wav_info(self, file_path: str) -> dict:
        """
        Extract detailed WAV file information from header.
        
        Parameters:
        file_path (str):
            Path to the WAV file.
            
        Returns:
        dict: Dictionary containing WAV-specific information.
        """
        try:
            with open(file_path, 'rb') as f:
                # Skip RIFF header
                f.read(12)
                
                # Read fmt chunk
                f.read(4)  # fmt chunk ID
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
                
                # Look for data chunk to get size
                data_chunk_id = f.read(4)
                while data_chunk_id != b'data' and data_chunk_id:
                    chunk_size = struct.unpack('<I', f.read(4))[0]
                    f.read(chunk_size)
                    data_chunk_id = f.read(4)
                
                data_size = struct.unpack('<I', f.read(4))[0]
                
                # Calculate duration
                duration = data_size / byte_rate
                
                # Calculate total samples
                total_samples = data_size // block_align
                
                return {
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
                
        except Exception as e:
            logger.error(f"WAV info extraction error: {e}")
            raise ValueError(f"Failed to extract WAV info: {str(e)}")
    
    def is_supported_format(self, file_path: str) -> bool:
        """
        Check if a file format is supported.
        
        Parameters:
        file_path (str):
            Path to the audio file.
            
        Returns:
        bool: True if format is supported, False otherwise.
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in self.SUPPORTED_FORMATS
    
    def get_supported_formats(self) -> list:
        """
        Get list of supported audio formats.
        
        Returns:
        list: List of supported file extensions.
        """
        return self.SUPPORTED_FORMATS.copy()


# Global audio validator instance
audio_validator = AudioValidator()
