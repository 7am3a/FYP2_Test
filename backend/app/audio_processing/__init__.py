"""
Audio Processing Module for SecureStego

This module handles all audio file operations including validation,
conversion to WAV format, sample loading, and WAV file generation.

Why Separate Audio Processing:
- Follows Single Responsibility Principle
- Isolates audio format handling from steganography logic
- Enables independent testing of audio operations
- Makes the codebase more maintainable and extensible
- Allows easy addition of new audio formats in the future

Modules:
- audio_validator: Validates audio file format and integrity
- audio_converter: Converts various audio formats to WAV
- audio_loader: Loads audio samples for processing
- audio_writer: Generates WAV output files
"""

from .audio_validator import audio_validator
from .audio_converter import audio_converter
from .audio_loader import audio_loader
from .audio_writer import audio_writer

__all__ = [
    "audio_validator",
    "audio_converter",
    "audio_loader",
    "audio_writer"
]
