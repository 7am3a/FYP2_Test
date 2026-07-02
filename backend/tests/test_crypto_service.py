"""
Unit Tests for CryptoService
Tests Argon2id key derivation and AES-256-GCM encryption
"""

import pytest
import base64
from app.services.crypto_service import crypto_service


class TestCryptoService:
    """Test cases for CryptoService"""
    
    def test_encrypt_message_success(self):
        """Test successful message encryption"""
        message = "Test message"
        password = "test_password"
        
        result = crypto_service.encrypt_message(message, password)
        
        assert "ciphertext" in result
        assert "salt" in result
        assert "iv" in result
        assert "algorithm" in result
        assert result["algorithm"] == "AES-256-GCM"
        assert result["kdf"] == "Argon2id"
        
        # Verify base64 encoding
        try:
            base64.b64decode(result["ciphertext"])
            base64.b64decode(result["salt"])
            base64.b64decode(result["iv"])
        except Exception:
            pytest.fail("Ciphertext, salt, or iv should be valid base64")
    
    def test_decrypt_message_success(self):
        """Test successful message decryption"""
        message = "Test message"
        password = "test_password"
        
        # Encrypt first
        encrypt_result = crypto_service.encrypt_message(message, password)
        
        # Decrypt
        decrypted = crypto_service.decrypt_message(
            ciphertext=encrypt_result["ciphertext"],
            password=password,
            salt=encrypt_result["salt"],
            iv=encrypt_result["iv"]
        )
        
        assert decrypted == message
    
    def test_decrypt_wrong_password(self):
        """Test decryption with wrong password raises ValueError"""
        message = "Test message"
        password = "test_password"
        wrong_password = "wrong_password"
        
        # Encrypt first
        encrypt_result = crypto_service.encrypt_message(message, password)
        
        # Try to decrypt with wrong password
        with pytest.raises(ValueError):
            crypto_service.decrypt_message(
                ciphertext=encrypt_result["ciphertext"],
                password=wrong_password,
                salt=encrypt_result["salt"],
                iv=encrypt_result["iv"]
            )
    
    def test_different_encryptions_different_ciphertexts(self):
        """Test that encrypting the same message twice produces different ciphertexts"""
        message = "Test message"
        password = "test_password"
        
        result1 = crypto_service.encrypt_message(message, password)
        result2 = crypto_service.encrypt_message(message, password)
        
        # Different IVs should produce different ciphertexts
        assert result1["ciphertext"] != result2["ciphertext"]
        assert result1["iv"] != result2["iv"]
        assert result1["salt"] != result2["salt"]
    
    def test_empty_message(self):
        """Test encryption of empty message"""
        message = ""
        password = "test_password"
        
        result = crypto_service.encrypt_message(message, password)
        assert "ciphertext" in result
    
    def test_long_message(self):
        """Test encryption of long message"""
        message = "A" * 10000  # 10KB message
        password = "test_password"
        
        result = crypto_service.encrypt_message(message, password)
        assert "ciphertext" in result
        
        # Verify decryption works
        decrypted = crypto_service.decrypt_message(
            ciphertext=result["ciphertext"],
            password=password,
            salt=result["salt"],
            iv=result["iv"]
        )
        assert decrypted == message
    
    def test_special_characters(self):
        """Test encryption of message with special characters"""
        message = "Test message with special chars: !@#$%^&*()_+-=[]{}|;':,.<>?"
        password = "test_password"
        
        result = crypto_service.encrypt_message(message, password)
        
        decrypted = crypto_service.decrypt_message(
            ciphertext=result["ciphertext"],
            password=password,
            salt=result["salt"],
            iv=result["iv"]
        )
        assert decrypted == message
