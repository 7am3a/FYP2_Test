"""
Video Processing Module for SecureStego

This module handles all video processing operations required for
video steganography, including validation, conversion, frame extraction,
frame reconstruction, and audio preservation.

Modules:
- video_validator: Validates video files
- video_converter: Converts videos to MP4 format
- frame_extractor: Extracts frames from videos
- frame_rebuilder: Rebuilds videos from frames
- audio_handler: Extracts and preserves audio tracks
"""

from app.video_processing.video_validator import video_validator
from app.video_processing.video_converter import video_converter
from app.video_processing.frame_extractor import frame_extractor
from app.video_processing.frame_rebuilder import frame_rebuilder
from app.video_processing.audio_handler import audio_handler

__all__ = [
    'video_validator',
    'video_converter',
    'frame_extractor',
    'frame_rebuilder',
    'audio_handler'
]
