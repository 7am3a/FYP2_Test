"""
Frame Extractor Module for SecureStego

Purpose:
Extracts frames from video files for DCT-based steganography processing.

This module is isolated from video conversion, frame reconstruction, and steganography
to improve maintainability and debugging.

Extraction Workflow:
1. Validate video file
2. Extract frames at specified interval
3. Save frames as images in temporary directory
4. Return frame paths and metadata

Why This Exists:
- Provides individual frames for DCT processing
- Allows selective frame processing
- Maintains frame order and timing
- Supports frame selection strategies

Security Considerations:
- Uses temporary directories for frame storage
- Validates frame extraction success
- Cleans up temporary frames on error
- Does not modify original video
"""

import os
import logging
import subprocess
import tempfile
from typing import List, Tuple, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FrameExtractor:
    """
    Extracts frames from video files.
    
    Why this exists:
    - Provides individual frames for DCT processing
    - Enables selective frame embedding
    - Maintains frame sequence information
    - Supports various extraction strategies
    
    Security Considerations:
    - Creates temporary directories for frames
    - Validates extracted frames
    - Cleans up temporary files
    - Does not modify original video
    """
    
    # Default frame extraction interval (extract every Nth frame)
    DEFAULT_INTERVAL = 1  # Extract all frames
    
    # Frame image format
    FRAME_FORMAT = 'png'
    
    # Frame filename pattern
    FRAME_PATTERN = 'frame_%06d.png'
    
    def __init__(self):
        """Initialize the frame extractor."""
        logger.info("FrameExtractor initialized")
    
    def extract_frames(
        self,
        video_path: str,
        interval: int = DEFAULT_INTERVAL,
        max_frames: Optional[int] = None
    ) -> Tuple[List[str], dict]:
        """
        Extract frames from a video file.
        
        This method:
        1. Creates a temporary directory for frames
        2. Uses FFmpeg to extract frames at specified interval
        3. Saves frames as PNG images
        4. Returns list of frame paths and metadata
        
        Parameters:
        video_path (str):
            Path to the video file.
        interval (int):
            Extract every Nth frame (default: 1, extract all frames).
        max_frames (int, optional):
            Maximum number of frames to extract (None = no limit).
            
        Returns:
        Tuple[List[str], dict]:
            - List of extracted frame file paths
            - Dictionary with extraction metadata (frame_count, fps, duration, etc.)
            
        Raises:
        ValueError: If extraction fails
        IOError: If file operations fail
        """
        try:
            logger.info(f"Extracting frames from: {video_path}")
            logger.info(f"Extraction interval: every {interval} frame(s)")
            
            # Create temporary directory for frames
            temp_dir = tempfile.mkdtemp(prefix='video_frames_')
            logger.info(f"Frame directory: {temp_dir}")
            
            # Build frame output pattern
            frame_pattern = os.path.join(temp_dir, self.FRAME_PATTERN)
            
            # Build FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'select=\'not(mod(n,{interval}))\'',  # Select every Nth frame
                '-vsync', '0',  # Preserve frame timestamps
                '-q:v', '2',  # High quality for PNG
                f'{frame_pattern}',
                '-y'  # Overwrite existing files
            ]
            
            # Add max_frames limit if specified
            if max_frames:
                cmd.insert(-1, '-vframes')
                cmd.insert(-1, str(max_frames))
            
            logger.info(f"Running FFmpeg frame extraction")
            
            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode != 0:
                error = f"Frame extraction failed: {result.stderr}"
                logger.error(error)
                # Cleanup on error
                self._cleanup_temp_dir(temp_dir)
                raise ValueError(error)
            
            # Get list of extracted frames
            frame_paths = sorted([
                os.path.join(temp_dir, f)
                for f in os.listdir(temp_dir)
                if f.endswith(f'.{self.FRAME_FORMAT}')
            ])
            
            frame_count = len(frame_paths)
            
            if frame_count == 0:
                error = "No frames were extracted"
                logger.error(error)
                self._cleanup_temp_dir(temp_dir)
                raise ValueError(error)
            
            logger.info(f"Extracted {frame_count} frames")
            
            # Get video metadata
            metadata = self._get_video_metadata(video_path)
            
            # Add extraction-specific metadata
            metadata.update({
                'extractedFrameCount': frame_count,
                'extractionInterval': interval,
                'frameDirectory': temp_dir,
                'frameFormat': self.FRAME_FORMAT
            })
            
            return frame_paths, metadata
            
        except subprocess.TimeoutExpired:
            error = "Frame extraction timed out"
            logger.error(error)
            raise ValueError(error)
        except Exception as e:
            logger.error(f"Frame extraction error: {e}")
            raise
    
    def extract_frame_range(
        self,
        video_path: str,
        start_frame: int,
        end_frame: int
    ) -> Tuple[List[str], dict]:
        """
        Extract a specific range of frames from a video.
        
        This method extracts frames from start_frame to end_frame (inclusive).
        
        Parameters:
        video_path (str):
            Path to the video file.
        start_frame (int):
            Starting frame number (0-indexed).
        end_frame (int):
            Ending frame number (0-indexed).
            
        Returns:
        Tuple[List[str], dict]:
            - List of extracted frame file paths
            - Dictionary with extraction metadata
        """
        try:
            logger.info(f"Extracting frames {start_frame} to {end_frame}")
            
            # Create temporary directory for frames
            temp_dir = tempfile.mkdtemp(prefix='video_frames_')
            frame_pattern = os.path.join(temp_dir, self.FRAME_PATTERN)
            
            # Build FFmpeg command for frame range
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'select=between(n\\,{start_frame}\\,{end_frame})',
                '-vsync', '0',
                '-frame_pts', '1',
                '-q:v', '2',
                f'{frame_pattern}',
                '-y'
            ]
            
            logger.info(f"Running FFmpeg frame range extraction")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode != 0:
                error = f"Frame range extraction failed: {result.stderr}"
                logger.error(error)
                self._cleanup_temp_dir(temp_dir)
                raise ValueError(error)
            
            # Get list of extracted frames
            frame_paths = sorted([
                os.path.join(temp_dir, f)
                for f in os.listdir(temp_dir)
                if f.endswith(f'.{self.FRAME_FORMAT}')
            ])
            
            frame_count = len(frame_paths)
            logger.info(f"Extracted {frame_count} frames in range")
            
            # Get video metadata
            metadata = self._get_video_metadata(video_path)
            metadata.update({
                'extractedFrameCount': frame_count,
                'startFrame': start_frame,
                'endFrame': end_frame,
                'frameDirectory': temp_dir,
                'frameFormat': self.FRAME_FORMAT
            })
            
            return frame_paths, metadata
            
        except Exception as e:
            logger.error(f"Frame range extraction error: {e}")
            raise
    
    def _get_video_metadata(self, video_path: str) -> dict:
        """
        Get video metadata using ffprobe.
        
        Parameters:
        video_path (str):
            Path to the video file.
            
        Returns:
        dict: Video metadata (fps, duration, total_frames, etc.).
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=r_frame_rate,duration,nb_read_frames',
                '-show_entries', 'format=duration',
                '-of', 'json',
                video_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                logger.warning(f"Could not get video metadata: {result.stderr}")
                return {}
            
            import json
            info = json.loads(result.stdout)
            
            stream = info.get('streams', [{}])[0]
            format_info = info.get('format', {})
            
            # Parse frame rate
            r_frame_rate = stream.get('r_frame_rate', '0/1')
            if '/' in r_frame_rate:
                num, den = r_frame_rate.split('/')
                fps = float(num) / float(den)
            else:
                fps = float(r_frame_rate)
            
            return {
                'fps': fps,
                'duration': float(format_info.get('duration', stream.get('duration', 0))),
                'totalFrames': int(stream.get('nb_read_frames', 0))
            }
            
        except Exception as e:
            logger.error(f"Error getting video metadata: {e}")
            return {}
    
    def _cleanup_temp_dir(self, dir_path: str) -> None:
        """
        Clean up a temporary directory containing frames.
        
        Parameters:
        dir_path (str):
            Path to the temporary directory to delete.
        """
        try:
            if os.path.exists(dir_path):
                import shutil
                shutil.rmtree(dir_path)
                logger.info(f"Cleaned up temporary directory: {dir_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temporary directory {dir_path}: {e}")
    
    def cleanup_frames(self, frame_paths: List[str]) -> None:
        """
        Clean up extracted frame files.
        
        Parameters:
        frame_paths (List[str]):
            List of frame file paths to delete.
        """
        try:
            for frame_path in frame_paths:
                if os.path.exists(frame_path):
                    os.remove(frame_path)
            
            # Try to remove the directory if it's empty
            if frame_paths:
                frame_dir = os.path.dirname(frame_paths[0])
                try:
                    os.rmdir(frame_dir)
                    logger.info(f"Cleaned up frame directory: {frame_dir}")
                except:
                    pass  # Directory not empty
            
            logger.info(f"Cleaned up {len(frame_paths)} frame files")
            
        except Exception as e:
            logger.warning(f"Failed to cleanup frames: {e}")


# Global frame extractor instance
frame_extractor = FrameExtractor()
