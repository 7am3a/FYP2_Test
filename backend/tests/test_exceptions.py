"""
Unit Tests for Custom Exceptions
Tests exception hierarchy and error handling
"""

import pytest
from app.utils.exceptions import (
    SecureStegoException,
    EncryptionError,
    DecryptionError,
    InvalidPasswordError,
    KeyDerivationError,
    SteganographyError,
    CapacityExceededError,
    InvalidMediaError,
    EmbeddingError,
    ExtractionError,
    NoHiddenDataError,
    VerificationError,
    SignatureVerificationError,
    FileProcessingError,
    FileValidationError,
    ValidationError
)


class TestExceptions:
    """Test cases for custom exceptions"""
    
    def test_base_exception(self):
        """Test base SecureStegoException"""
        exc = SecureStegoException("Test error")
        
        assert str(exc) == "Test error"
        assert exc.message == "Test error"
        assert exc.details == {}
    
    def test_base_exception_with_details(self):
        """Test base exception with details"""
        details = {"key": "value"}
        exc = SecureStegoException("Test error", details)
        
        assert exc.details == details
    
    def test_base_exception_to_dict(self):
        """Test exception to_dict method"""
        exc = SecureStegoException("Test error", {"key": "value"})
        
        result = exc.to_dict()
        
        assert result["error"] == "Test error"
        assert result["errorType"] == "SecureStegoException"
        assert result["details"] == {"key": "value"}
    
    def test_encryption_error_hierarchy(self):
        """Test encryption error hierarchy"""
        exc = EncryptionError("Encryption failed")
        
        assert isinstance(exc, SecureStegoException)
        assert isinstance(exc, EncryptionError)
    
    def test_decryption_error_hierarchy(self):
        """Test decryption error hierarchy"""
        exc = DecryptionError("Decryption failed")
        
        assert isinstance(exc, SecureStegoException)
        assert isinstance(exc, DecryptionError)
    
    def test_invalid_password_error_hierarchy(self):
        """Test invalid password error hierarchy"""
        exc = InvalidPasswordError("Wrong password")
        
        assert isinstance(exc, SecureStegoException)
        assert isinstance(exc, DecryptionError)
        assert isinstance(exc, InvalidPasswordError)
    
    def test_steganography_error_hierarchy(self):
        """Test steganography error hierarchy"""
        exc = SteganographyError("Steganography failed")
        
        assert isinstance(exc, SecureStegoException)
        assert isinstance(exc, SteganographyError)
    
    def test_capacity_exceeded_error_hierarchy(self):
        """Test capacity exceeded error hierarchy"""
        exc = CapacityExceededError("Payload too large")
        
        assert isinstance(exc, SecureStegoException)
        assert isinstance(exc, SteganographyError)
        assert isinstance(exc, CapacityExceededError)
    
    def test_verification_error_hierarchy(self):
        """Test verification error hierarchy"""
        exc = VerificationError("Verification failed")
        
        assert isinstance(exc, SecureStegoException)
        assert isinstance(exc, VerificationError)
    
    def test_signature_verification_error_hierarchy(self):
        """Test signature verification error hierarchy"""
        exc = SignatureVerificationError("Signature invalid")
        
        assert isinstance(exc, SecureStegoException)
        assert isinstance(exc, VerificationError)
        assert isinstance(exc, SignatureVerificationError)
    
    def test_file_processing_error_hierarchy(self):
        """Test file processing error hierarchy"""
        exc = FileProcessingError("File processing failed")
        
        assert isinstance(exc, SecureStegoException)
        assert isinstance(exc, FileProcessingError)
    
    def test_validation_error_hierarchy(self):
        """Test validation error hierarchy"""
        exc = ValidationError("Validation failed")
        
        assert isinstance(exc, SecureStegoException)
        assert isinstance(exc, ValidationError)
    
    def test_exception_catching(self):
        """Test catching exceptions by base class"""
        try:
            raise InvalidPasswordError("Wrong password")
        except DecryptionError:
            caught = True
        else:
            caught = False
        
        assert caught
    
    def test_exception_catching_specific(self):
        """Test catching exceptions by specific class"""
        try:
            raise InvalidPasswordError("Wrong password")
        except InvalidPasswordError:
            caught = True
        else:
            caught = False
        
        assert caught
