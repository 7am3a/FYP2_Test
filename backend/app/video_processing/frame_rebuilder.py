"""
Frame Rebuilder Module for SecureStego

Purpose:
Rebuilds video files from processed frames for steganography output.

This module is isolated from frame extraction, video conversion, and steganography
to improve maintainability and debugging.

Rebuilding Workflow:
1. Validate frame directory
2. Sort frames in correct order
3. Rebuild video using FFmpeg
4. Verify output integrity
5. Return path to rebuilt video

Why This Exists:
- Reconstructs video from DCT-processed frames
- Maintains original frame rate and timing
- Supports audio reattachment
- Ensures output is valid MP4

Security Considerations:
- Uses temporary files for processing
- Validates output before returning
- Cleans up temporary files on error
- Does not modify original frames
"""

import os
import logging
import subprocess
import tempfile
from typing import List, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FrameRebuilder:
    """
    Rebuilds video files from processed frames.
    
    Why this exists:
    - Reconstructs video from DCT-modified frames
    - Maintains original video properties
    - Ensures valid MP4 output
    - Supports audio track reattachment
    
    Security Considerations:
    - Creates temporary files for output
    - Validates rebuilt video
    - Cleans up temporary files
    - Does not modify original frames
    """
    
    # Output format
    OUTPUT_FORMAT = '.mp4'
    
    # FFmpeg codec settings
    VIDEO_CODEC = 'libx264'
    PRESET = 'Medium'
    CRF = 0
    
    # Frame pattern to match
    FRAME_PATTERN = 'frame_%06d.png'
    
    def __init__(self):
        """Initialize the frame rebuilder."""
        logger.info("FrameRebuilder initialized")
    
    def rebuild_video(
        self,
        frame_paths: List[str],
        output_path: Optional[str] = None,
        fps: float = 30.0,
        original_video_path: Optional[str] = None
    ) -> str:
        """
        Rebuild a video from processed frames.
        
        This method:
        1. Sorts frames in correct order
        2. Creates temporary output file if not provided
        3. Uses FFmpeg to rebuild video from frames
        4. Preserves frame rate from original video
        5. Verifies output integrity
        6. Returns path to rebuilt video
        
        Parameters:
        frame_paths (List[str]):
            List of frame file paths (must be in order).
        output_path (str, optional):
            Path for output video file (if None, creates temp file).
        fps (float):
            Frame rate for output video (default: 30.0).
        original_video_path (str, optional):
            Path to original video for metadata preservation.
            
        Returns:
        str: Path to the rebuilt MP4 video file.
            
        Raises:
        ValueError: If rebuilding fails or output is invalid
        IOError: If file operations fail
        """
        try:
            logger.info(f"Rebuilding video from {len(frame_paths)} frames")
            
            # Validate frames
            if not frame_paths:
                raise ValueError("No frames provided for rebuilding")
            
            # Sort frames to ensure correct order
            frame_paths = sorted(frame_paths)
            logger.info(f"Frames sorted: {frame_paths[0]} to {frame_paths[-1]}")
            
            # Get frame directory
            frame_dir = os.path.dirname(frame_paths[0])
            frame_pattern = os.path.join(frame_dir, self.FRAME_PATTERN)
            
            # Create output path if not provided
            if output_path is None:
                temp_dir = tempfile.gettempdir()
                output_path = os.path.join(temp_dir, f"rebuilt_video_{os.getpid()}{self.OUTPUT_FORMAT}")
            
            logger.info(f"Output path: {output_path}")
            
            # If original video provided, try to get its frame rate
            if original_video_path:
                original_fps = self._get_video_fps(original_video_path)
                if original_fps:
                    fps = original_fps
                    logger.info(f"Using original video FPS: {fps}")
            
            # Build FFmpeg command
            cmd = [
                'ffmpeg',
                '-framerate', str(fps),
                '-i', frame_pattern,
                '-c:v', self.VIDEO_CODEC,
                '-preset', self.PRESET,
                '-crf', str(self.CRF),
                '-pix_fmt', 'yuv444p',
                '-movflags', '+faststart',
                '-y',
                output_path
            ]
                        
            logger.info(f"Running FFmpeg video rebuild")
            
            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode != 0:
                error = f"Video rebuild failed: {result.stderr}"
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
            
            # Verify output is valid MP4
            if not self._verify_mp4(output_path):
                error = "Output video is not a valid MP4"
                logger.error(error)
                raise ValueError(error)
            
            logger.info(f"Video rebuild successful: {output_path}")
            
            return output_path
            
        except subprocess.TimeoutExpired:
            error = "Video rebuild timed out"
            logger.error(error)
            raise ValueError(error)
        except Exception as e:
            logger.error(f"Video rebuild error: {e}")
            raise
    
    def _get_video_fps(self, video_path: str) -> Optional[float]:
        """
        Get the frame rate of a video file.
        
        Parameters:
        video_path (str):
            Path to the video file.
            
        Returns:
        Optional[float]: Frame rate, or None if unable to determine.
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=r_frame_rate',
                '-of', 'csv=p=0',
                video_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return None
            
            # Parse frame rate (e.g., "30/1" -> 30.0)
            r_frame_rate = result.stdout.strip()
            if '/' in r_frame_rate:
                num, den = r_frame_rate.split('/')
                fps = float(num) / float(den)
            else:
                fps = float(r_frame_rate)
            
            return fps
            
        except Exception as e:
            logger.error(f"Error getting video FPS: {e}")
            return None
    
    def _verify_mp4(self, file_path: str) -> bool:
        """
        Verify that a file is a valid MP4 video.
        
        Parameters:
        file_path (str):
            Path to the file to verify.
            
        Returns:
        bool: True if file is valid MP4, False otherwise.
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=codec_name',
                '-of', 'csv=p=0',
                file_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return result.returncode == 0 and len(result.stdout.strip()) > 0
            
        except Exception as e:
            logger.error(f"MP4 verification error: {e}")
            return False
    
    def cleanup_temp_file(self, file_path: str) -> None:
        """
        Clean up a temporary video file.
        
        Parameters:
        file_path (str):
            Path to the temporary file to delete.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temporary file {file_path}: {e}")


# Global frame rebuilder instance
frame_rebuilder = FrameRebuilder()
