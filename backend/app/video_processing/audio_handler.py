"""
Audio Handler Module for SecureStego

Purpose:
Extracts and preserves audio tracks from video files during steganography processing.

This module is isolated from video conversion, frame processing, and steganography
to improve maintainability and debugging.

Audio Workflow:
1. Extract audio track from original video
2. Save as temporary audio file
3. Reattach audio to processed video
4. Verify audio preservation

Why This Exists:
- Preserves original audio during video processing
- Ensures stego video has same audio as original
- Supports various audio codecs
- Maintains audio-video synchronization

Security Considerations:
- Uses temporary files for audio storage
- Validates audio extraction
- Cleans up temporary files
- Does not modify original audio
"""

import os
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioHandler:
    """
    Handles audio track extraction and preservation for video steganography.
    
    Why this exists:
    - Preserves original audio during video processing
    - Ensures stego video maintains audio quality
    - Supports various audio formats
    - Maintains audio-video synchronization
    
    Security Considerations:
    - Creates temporary files for audio
    - Validates audio extraction
    - Cleans up temporary files
    - Does not modify original audio
    """
    
    # Audio codec for extraction
    AUDIO_CODEC = 'aac'
    
    # Audio format
    AUDIO_FORMAT = 'aac'
    
    def __init__(self):
        """Initialize the audio handler."""
        logger.info("AudioHandler initialized")
    
    def extract_audio(self, video_path: str) -> Optional[str]:
        """
        Extract audio track from a video file.
        
        This method:
        1. Checks if video has audio track
        2. Extracts audio to temporary file
        3. Returns path to audio file
        4. Returns None if no audio track exists
        
        Parameters:
        video_path (str):
            Path to the video file.
            
        Returns:
        Optional[str]:
            Path to extracted audio file, or None if no audio track.
            
        Raises:
        ValueError: If audio extraction fails
        IOError: If file operations fail
        """
        try:
            logger.info(f"Extracting audio from: {video_path}")
            
            # Check if video has audio track
            if not self._has_audio_track(video_path):
                logger.info("Video has no audio track")
                return None
            
            # Create temporary audio file
            temp_dir = tempfile.gettempdir()
            base_name = Path(video_path).stem
            audio_path = os.path.join(temp_dir, f"{base_name}_audio.{self.AUDIO_FORMAT}")
            
            logger.info(f"Audio output path: {audio_path}")
            
            # Build FFmpeg command to extract audio
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vn',  # No video
                '-acodec', self.AUDIO_CODEC,
                '-y',  # Overwrite existing file
                audio_path
            ]
            
            logger.info(f"Running FFmpeg audio extraction")
            
            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                error = f"Audio extraction failed: {result.stderr}"
                logger.error(error)
                raise ValueError(error)
            
            # Verify audio file exists and is not empty
            if not os.path.exists(audio_path):
                error = "Audio file was not created"
                logger.error(error)
                raise ValueError(error)
            
            if os.path.getsize(audio_path) == 0:
                error = "Audio file is empty"
                logger.error(error)
                raise ValueError(error)
            
            logger.info(f"Audio extracted successfully: {audio_path}")
            
            return audio_path
            
        except subprocess.TimeoutExpired:
            error = "Audio extraction timed out"
            logger.error(error)
            raise ValueError(error)
        except Exception as e:
            logger.error(f"Audio extraction error: {e}")
            raise
    
    def attach_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: Optional[str] = None
    ) -> str:
        """
        Attach audio track to a video file.
        
        This method:
        1. Combines video and audio tracks
        2. Creates output video with audio
        3. Preserves synchronization
        4. Returns path to output video
        
        Parameters:
        video_path (str):
            Path to the video file (without audio).
        audio_path (str):
            Path to the audio file to attach.
        output_path (str, optional):
            Path for output video (if None, creates temp file).
            
        Returns:
        str: Path to the video file with audio attached.
            
        Raises:
        ValueError: If audio attachment fails
        IOError: If file operations fail
        """
        try:
            logger.info(f"Attaching audio to video: {video_path}")
            logger.info(f"Audio source: {audio_path}")
            
            # Validate input files
            if not os.path.exists(video_path):
                raise ValueError(f"Video file not found: {video_path}")
            
            if not os.path.exists(audio_path):
                raise ValueError(f"Audio file not found: {audio_path}")
            
            # Create output path if not provided
            if output_path is None:
                temp_dir = tempfile.gettempdir()
                base_name = Path(video_path).stem
                output_path = os.path.join(temp_dir, f"{base_name}_with_audio.mp4")
            
            logger.info(f"Output path: {output_path}")
            
            # Build FFmpeg command to attach audio
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',  # Copy video stream without re-encoding
                '-c:a', 'aac',  # Encode audio to AAC
                '-map', '0:v:0',  # Use video from first input
                '-map', '1:a:0',  # Use audio from second input
                '-shortest',  # Use shortest duration
                '-y',
                output_path
            ]
            
            logger.info(f"Running FFmpeg audio attachment")
            
            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                error = f"Audio attachment failed: {result.stderr}"
                logger.error(error)
                raise ValueError(error)
            
            # Verify output file exists and is not empty
            if not os.path.exists(output_path):
                error = "Output video file was not created"
                logger.error(error)
                raise ValueError(error)
            
            if os.path.getsize(output_path) == 0:
                error = "Output video file is empty"
                logger.error(error)
                raise ValueError(error)
            
            # Verify output has audio
            if not self._has_audio_track(output_path):
                error = "Output video does not have audio track"
                logger.error(error)
                raise ValueError(error)
            
            logger.info(f"Audio attached successfully: {output_path}")
            
            return output_path
            
        except subprocess.TimeoutExpired:
            error = "Audio attachment timed out"
            logger.error(error)
            raise ValueError(error)
        except Exception as e:
            logger.error(f"Audio attachment error: {e}")
            raise
    
    def _has_audio_track(self, video_path: str) -> bool:
        """
        Check if a video file has an audio track.
        
        Parameters:
        video_path (str):
            Path to the video file.
            
        Returns:
        bool: True if video has audio track, False otherwise.
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'a',
                '-show_entries', 'stream=codec_type',
                '-of', 'csv=p=0',
                video_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return result.returncode == 0 and 'audio' in result.stdout.lower()
            
        except Exception as e:
            logger.error(f"Error checking audio track: {e}")
            return False
    
    def cleanup_temp_file(self, file_path: str) -> None:
        """
        Clean up a temporary audio file.
        
        Parameters:
        file_path (str):
            Path to the temporary file to delete.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary audio file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temporary audio file {file_path}: {e}")


# Global audio handler instance
audio_handler = AudioHandler()
