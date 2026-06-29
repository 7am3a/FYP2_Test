"""
Audio Steganography Module for SecureStego

This module handles audio steganography operations including
sample selection, LSB embedding, and LSB extraction.

Why Separate Audio Steganography:
- Follows Single Responsibility Principle
- Isolates audio-specific steganography logic
- Enables independent testing of steganography algorithms
- Makes the codebase more maintainable and extensible
- Allows easy addition of new audio steganography methods

Modules:
- sample_selector: Generates deterministic randomized sample positions
- audio_lsb_embedder: Embeds payload bits into audio samples
- audio_lsb_extractor: Extracts payload bits from audio samples
"""

from .sample_selector import sample_selector
from .audio_lsb_embedder import audio_lsb_embedder
from .audio_lsb_extractor import audio_lsb_extractor

__all__ = [
    "sample_selector",
    "audio_lsb_embedder",
    "audio_lsb_extractor"
]
