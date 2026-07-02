"""
Centralized Exception Handling for SecureStego

This module provides custom exceptions for the application.
It ensures consistent error handling and error messages across all modules.

Benefits:
- Single source of truth for exception definitions
- Consistent error handling patterns
- Easy to add new exception types
- Structured error responses for APIs
"""

from typing import Optional, Dict, Any


class SecureStegoException(Exception):
    """
    Base exception for all SecureStego errors.
    
    Why this exists:
    - Provides a common base for all custom exceptions
    - Enables consistent error handling across the application
    - Allows for structured error responses
    - Facilitates error logging and monitoring
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """
        Initialize the exception.
        
        Parameters:
        message (str):
            Human-readable error message.
        details (Dict[str, Any], optional):
            Additional error details for debugging.
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary for API responses.
        
        Returns:
        Dict[str, Any]: Exception data as dictionary.
        """
        return {
            "error": self.message,
            "errorType": self.__class__.__name__,
            "details": self.details
        }


# Encryption Exceptions
class EncryptionError(SecureStegoException):
    """Base exception for encryption-related errors."""
    pass


class DecryptionError(SecureStegoException):
    """Base exception for decryption-related errors."""
    pass


class InvalidPasswordError(DecryptionError):
    """Raised when password is invalid or incorrect."""
    pass


class KeyDerivationError(EncryptionError):
    """Raised when key derivation fails."""
    pass


# Steganography Exceptions
class SteganographyError(SecureStegoException):
    """Base exception for steganography-related errors."""
    pass


class CapacityExceededError(SteganographyError):
    """Raised when payload exceeds media capacity."""
    pass


class InvalidMediaError(SteganographyError):
    """Raised when media file is invalid or unsupported."""
    pass


class EmbeddingError(SteganographyError):
    """Raised when embedding fails."""
    pass


class ExtractionError(SteganographyError):
    """Raised when extraction fails."""
    pass


class NoHiddenDataError(ExtractionError):
    """Raised when no hidden data is found in media."""
    pass


# Image Steganography Exceptions
class ImageSteganographyError(SteganographyError):
    """Base exception for image steganography errors."""
    pass


class ImageConversionError(ImageSteganographyError):
    """Raised when image conversion fails."""
    pass


class EdgeDetectionError(ImageSteganographyError):
    """Raised when edge detection fails."""
    pass


# Video Steganography Exceptions
class VideoSteganographyError(SteganographyError):
    """Base exception for video steganography errors."""
    pass


class VideoConversionError(VideoSteganographyError):
    """Raised when video conversion fails."""
    pass


class FrameExtractionError(VideoSteganographyError):
    """Raised when frame extraction fails."""
    pass


class AudioExtractionError(VideoSteganographyError):
    """Raised when audio extraction fails."""
    pass


# Audio Steganography Exceptions
class AudioSteganographyError(SteganographyError):
    """Base exception for audio steganography errors."""
    pass


class AudioConversionError(AudioSteganographyError):
    """Raised when audio conversion fails."""
    pass


class SampleSelectionError(AudioSteganographyError):
    """Raised when sample selection fails."""
    pass


# Document Steganography Exceptions
class DocumentSteganographyError(SteganographyError):
    """Base exception for document steganography errors."""
    pass


class PDFProcessingError(DocumentSteganographyError):
    """Raised when PDF processing fails."""
    pass


class TextEmbeddingError(DocumentSteganographyError):
    """Raised when text embedding fails."""
    pass


# Platform Verification Exceptions
class VerificationError(SecureStegoException):
    """Base exception for verification-related errors."""
    pass


class SignatureVerificationError(VerificationError):
    """Raised when signature verification fails."""
    pass


class MissingSignatureError(SignatureVerificationError):
    """Raised when signature is missing."""
    pass


class InvalidSignatureError(SignatureVerificationError):
    """Raised when signature format is invalid."""
    pass


class TamperedSignatureError(SignatureVerificationError):
    """Raised when signature has been tampered with."""
    pass


class VersionMismatchError(SignatureVerificationError):
    """Raised when signature version is not supported."""
    pass


class PlatformMismatchError(SignatureVerificationError):
    """Raised when platform identity does not match."""
    pass


class MediaTypeMismatchError(SignatureVerificationError):
    """Raised when media type does not match."""
    pass


# File Processing Exceptions
class FileProcessingError(SecureStegoException):
    """Base exception for file processing errors."""
    pass


class FileValidationError(FileProcessingError):
    """Raised when file validation fails."""
    pass


class FileSizeExceededError(FileValidationError):
    """Raised when file size exceeds limit."""
    pass


class UnsupportedFormatError(FileValidationError):
    """Raised when file format is not supported."""
    pass


# Validation Exceptions
class ValidationError(SecureStegoException):
    """Base exception for validation errors."""
    pass


class InvalidPayloadError(ValidationError):
    """Raised when payload is invalid."""
    pass


class InvalidParameterError(ValidationError):
    """Raised when parameter is invalid."""
    pass


# Configuration Exceptions
class ConfigurationError(SecureStegoException):
    """Base exception for configuration errors."""
    pass


class MissingConfigurationError(ConfigurationError):
    """Raised when required configuration is missing."""
    pass


class InvalidConfigurationError(ConfigurationError):
    """Raised when configuration is invalid."""
    pass
