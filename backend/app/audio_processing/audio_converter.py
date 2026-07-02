"""
audio_converter.py

Purpose:
Converts various audio formats (WAV, MP3, M4A, FLAC) to WAV format
for steganography processing.

This module is intentionally isolated from audio validation,
sample loading, and steganography logic to improve maintainability.

Why WAV Conversion is Mandatory:
- WAV is uncompressed, providing raw sample access
- All steganography operations require uncompressed audio
- WAV format is well-documented and reliable
- Ensures consistent processing regardless of input format
- Prevents quality loss from multiple compression cycles

Security Considerations:
- Validates input file before conversion
- Uses temporary files to prevent overwriting originals
- Cleans up temporary files after conversion
- Logs all conversion operations for audit trail
"""

import os
import logging
import tempfile
import subprocess
from typing import Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioConverter:
    """
    Converts audio files to WAV format for steganography.
    
    Why this exists:
    - Provides a dedicated interface for audio format conversion
    - Ensures all audio is in WAV format before steganography
    - Handles multiple input formats (WAV, MP3, M4A, FLAC)
    - Manages temporary file lifecycle
    - Provides conversion statistics for debugging
    
    Responsibilities:
    - Convert WAV, MP3, M4A, FLAC to WAV
    - Manage temporary file creation and cleanup
    - Validate conversion output
    - Provide conversion statistics
    - Handle conversion errors gracefully
    
    Dependencies:
    - Requires ffmpeg to be installed on the system
    - ffmpeg is the industry standard for audio conversion
    """
    
    # Supported input formats
    SUPPORTED_FORMATS = ['.wav', '.mp3', '.m4a', '.flac']
    
    # Output format (always WAV)
    OUTPUT_FORMAT = '.wav'
    
    # FFmpeg path (will be detected automatically)
    FFMPEG_PATH = None
    
    def __init__(self):
        """Initialize the audio converter and detect ffmpeg."""
        logger.info("AudioConverter initialized")
        self._detect_ffmpeg()
    
    def _detect_ffmpeg(self) -> None:
        """
        Detect if ffmpeg is available on the system.
        
        FFmpeg is required for audio conversion. This method checks
        if ffmpeg is in the system PATH.
        
        Note: If FFmpeg is not found, the converter will log a warning
        but will not raise an error. Audio conversion will fail at runtime
        if FFmpeg is not available.
        """
        try:
            # Try to run ffmpeg -version
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self.FFMPEG_PATH = 'ffmpeg'
                logger.info("FFmpeg detected successfully")
                # Log version
                version_line = result.stdout.split('\n')[0]
                logger.info(f"FFmpeg version: {version_line}")
            else:
                logger.warning("FFmpeg command returned non-zero exit code")
                self.FFMPEG_PATH = None
                
        except FileNotFoundError:
            logger.warning(
                "FFmpeg is not installed or not in system PATH. "
                "Audio conversion will not be available. "
                "Install FFmpeg from https://ffmpeg.org/download.html"
            )
            self.FFMPEG_PATH = None
        except subprocess.TimeoutExpired:
            logger.warning("FFmpeg command timed out")
            self.FFMPEG_PATH = None
        except Exception as e:
            logger.warning(f"Error detecting FFmpeg: {e}")
            self.FFMPEG_PATH = None
    
    def convert_to_wav(self, input_path: str) -> Tuple[str, str]:
        """
        Convert an audio file to WAV format.
        
        This method:
        1. Validates input file exists
        2. Creates a temporary WAV file
        3. Uses ffmpeg to convert the audio
        4. Validates the output file
        5. Returns the path to the WAV file and original format
        
        Parameters:
        input_path (str):
            Path to the input audio file.
            
        Returns:
        Tuple[str, str]: 
            - Path to the converted WAV file
            - Original file format (e.g., 'mp3', 'wav')
            
        Raises:
        ValueError: If input file is invalid or conversion fails
        RuntimeError: If ffmpeg is not available
        IOError: If file operations fail
        """
        try:
            logger.info(f"Converting audio to WAV: {input_path}")
            
            # Step 1: Validate input file
            if not os.path.exists(input_path):
                raise ValueError(f"Input file does not exist: {input_path}")
            
            if not os.access(input_path, os.R_OK):
                raise ValueError(f"Input file is not readable: {input_path}")
            
            # Step 2: Get original format
            original_format = os.path.splitext(input_path)[1].lower()
            original_format_name = original_format[1:]  # Remove dot
            
            # Step 3: Create temporary WAV file
            temp_dir = tempfile.gettempdir()
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            temp_wav_path = os.path.join(temp_dir, f"{base_name}_temp.wav")
            
            # Ensure unique filename
            counter = 1
            while os.path.exists(temp_wav_path):
                temp_wav_path = os.path.join(temp_dir, f"{base_name}_temp_{counter}.wav")
                counter += 1
            
            logger.info(f"Temporary WAV path: {temp_wav_path}")
            
            # Step 4: Perform conversion using ffmpeg
            self._runffmpeg_conversion(input_path, temp_wav_path)
            
            # Step 5: Validate output file
            if not os.path.exists(temp_wav_path):
                raise ValueError("Conversion failed: output file not created")
            
            if os.path.getsize(temp_wav_path) == 0:
                raise ValueError("Conversion failed: output file is empty")
            
            logger.info(
                f"Conversion successful: {original_format_name} -> WAV "
                f"({os.path.getsize(temp_wav_path)} bytes)"
            )
            
            return temp_wav_path, original_format_name
            
        except Exception as e:
            logger.error(f"Conversion error: {e}")
            raise
    
    def _runffmpeg_conversion(self, input_path: str, output_path: str) -> None:
        """
        Run ffmpeg conversion command.
        
        This method constructs and executes the ffmpeg command to convert
        the audio file to WAV format with PCM encoding.
        
        Parameters:
        input_path (str):
            Path to the input audio file.
        output_path (str):
            Path to the output WAV file.
            
        Raises:
        subprocess.CalledProcessError: If ffmpeg conversion fails.
        """
        try:
            # FFmpeg command for WAV conversion
            # -y: Overwrite output file if exists
            # -i: Input file
            # -acodec pcm_s16le: 16-bit little-endian PCM
            # -ar 44100: Sample rate 44.1 kHz (standard CD quality)
            # -ac 2: Stereo (better for steganography capacity)
            command = [
                self.FFMPEG_PATH,
                '-y',
                '-i', input_path,
                '-acodec', 'pcm_s16le',
                '-ar', '44100',
                '-ac', '2',
                output_path
            ]
            
            logger.info(f"Running FFmpeg: {' '.join(command)}")
            
            # Run ffmpeg
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                error_msg = f"FFmpeg conversion failed: {result.stderr}"
                logger.error(error_msg)
                raise subprocess.CalledProcessError(result.returncode, command, result.stderr)
            
            logger.info("FFmpeg conversion completed successfully")
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("FFmpeg conversion timed out after 5 minutes")
        except Exception as e:
            logger.error(f"FFmpeg execution error: {e}")
            raise
    
    def convert_to_stego_wav(self, input_path: str) -> str:
        """
        Convert audio to WAV with stego-specific naming.
        
        This is a convenience method that converts the audio and
        returns a path with "_stego" suffix for the final output.
        
        Parameters:
        input_path (str):
            Path to the input audio file.
            
        Returns:
        str: Path to the converted WAV file with stego naming.
        """
        try:
            logger.info(f"Converting to stego WAV: {input_path}")
            
            # Convert to WAV
            temp_wav_path, original_format = self.convert_to_wav(input_path)
            
            # Create stego-named file
            temp_dir = tempfile.gettempdir()
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            stego_wav_path = os.path.join(temp_dir, f"{base_name}_stego.wav")
            
            # Ensure unique filename
            counter = 1
            while os.path.exists(stego_wav_path):
                stego_wav_path = os.path.join(temp_dir, f"{base_name}_stego_{counter}.wav")
                counter += 1
            
            # Copy temp WAV to stego WAV
            import shutil
            shutil.copy2(temp_wav_path, stego_wav_path)
            
            # Clean up temp WAV
            self.cleanup_temp_file(temp_wav_path)
            
            logger.info(f"Stego WAV created: {stego_wav_path}")
            
            return stego_wav_path
            
        except Exception as e:
            logger.error(f"Stego WAV conversion error: {e}")
            raise
    
    def is_supported_format(self, file_path: str) -> bool:
        """
        Check if a file format is supported for conversion.
        
        Parameters:
        file_path (str):
            Path to the audio file.
            
        Returns:
        bool: True if format is supported, False otherwise.
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in self.SUPPORTED_FORMATS
    
    def get_audio_format(self, file_path: str) -> str:
        """
        Get the audio format of a file.
        
        Parameters:
        file_path (str):
            Path to the audio file.
            
        Returns:
        str: File format (e.g., 'mp3', 'wav').
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext[1:]  # Remove dot
    
    def get_supported_formats(self) -> list:
        """
        Get list of supported input formats.
        
        Returns:
        list: List of supported file extensions.
        """
        return self.SUPPORTED_FORMATS.copy()
    
    def cleanup_temp_file(self, file_path: str) -> None:
        """
        Clean up a temporary file.
        
        This method safely removes a temporary file with error handling.
        
        Parameters:
        file_path (str):
            Path to the temporary file to remove.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temporary file {file_path}: {e}")


# Global audio converter instance
audio_converter = AudioConverter()
