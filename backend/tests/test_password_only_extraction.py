"""
Unit Tests for Password-Only Extraction Workflow
Tests the complete workflow: encrypt -> embed -> extract -> password-only decrypt
"""

import pytest
import base64
from app.services.crypto_service import crypto_service
from app.utils.payload_serializer import payload_serializer
from app.utils.payload_deserializer import payload_deserializer


class TestPasswordOnlyExtraction:
    """Test cases for password-only extraction workflow"""
    
    def test_complete_workflow_password_only(self):
        """Test complete workflow: encrypt -> embed payload -> extract -> decrypt with password only"""
        message = "Secret message for password-only extraction"
        password = "secure_password_123"
        
        # Step 1: Encrypt message
        encrypt_result = crypto_service.encrypt_message(message, password)
        assert "ciphertext" in encrypt_result
        assert "salt" in encrypt_result
        assert "iv" in encrypt_result
        
        # Step 2: Create payload with embedded metadata (version 2.0)
        payload_dict = payload_serializer.create_payload(
            encrypted_data=encrypt_result["ciphertext"],
            salt=encrypt_result["salt"],
            iv=encrypt_result["iv"],
            algorithm=encrypt_result["algorithm"],
            kdf=encrypt_result["kdf"]
        )
        
        # Step 3: Serialize payload to binary (simulating embedding)
        payload_binary = payload_serializer.serialize_to_binary(payload_dict)
        
        # Step 4: Deserialize payload (simulating extraction)
        extracted_payload = payload_deserializer.deserialize_from_binary(payload_binary)
        
        # Step 5: Extract encryption metadata from payload
        extracted_ciphertext = payload_deserializer.extract_encrypted_data(extracted_payload)
        extracted_salt = payload_deserializer.extract_salt(extracted_payload)
        extracted_iv = payload_deserializer.extract_iv(extracted_payload)
        extracted_algorithm = payload_deserializer.extract_algorithm(extracted_payload)
        extracted_kdf = payload_deserializer.extract_kdf(extracted_payload)
        
        # Verify metadata was recovered
        assert extracted_ciphertext == encrypt_result["ciphertext"]
        assert extracted_salt == encrypt_result["salt"]
        assert extracted_iv == encrypt_result["iv"]
        assert extracted_algorithm == "AES-256-GCM"
        assert extracted_kdf == "Argon2id"
        
        # Step 6: Decrypt using ONLY the password and recovered metadata
        decrypted_message = crypto_service.decrypt_message(
            ciphertext=extracted_ciphertext,
            password=password,
            salt=extracted_salt,
            iv=extracted_iv
        )
        
        # Verify original message is recovered
        assert decrypted_message == message
    
    def test_payload_version_2_contains_metadata(self):
        """Test that payload version 2.0 contains salt and iv"""
        message = "Test message"
        password = "test_password"
        
        # Encrypt
        encrypt_result = crypto_service.encrypt_message(message, password)
        
        # Create version 2.0 payload
        payload_dict = payload_serializer.create_payload(
            encrypted_data=encrypt_result["ciphertext"],
            salt=encrypt_result["salt"],
            iv=encrypt_result["iv"],
            version="2.0"
        )
        
        # Verify payload contains all required fields
        assert payload_dict["version"] == "2.0"
        assert "salt" in payload_dict
        assert "iv" in payload_dict
        assert "encryptedData" in payload_dict
        assert "algorithm" in payload_dict
        assert "kdf" in payload_dict
        assert "timestamp" in payload_dict
    
    def test_payload_deserializer_recovers_metadata(self):
        """Test that payload deserializer can recover salt and iv from version 2.0 payload"""
        message = "Test message"
        password = "test_password"
        
        # Encrypt
        encrypt_result = crypto_service.encrypt_message(message, password)
        
        # Create and serialize payload
        payload_dict = payload_serializer.create_payload(
            encrypted_data=encrypt_result["ciphertext"],
            salt=encrypt_result["salt"],
            iv=encrypt_result["iv"],
            version="2.0"
        )
        payload_binary = payload_serializer.serialize_to_binary(payload_dict)
        
        # Deserialize
        extracted_payload = payload_deserializer.deserialize_from_binary(payload_binary)
        
        # Extract metadata
        salt = payload_deserializer.extract_salt(extracted_payload)
        iv = payload_deserializer.extract_iv(extracted_payload)
        
        # Verify metadata matches original
        assert salt == encrypt_result["salt"]
        assert iv == encrypt_result["iv"]
    
    def test_legacy_payload_version_1_no_metadata(self):
        """Test that legacy payload version 1.0 does not contain salt and iv"""
        # Create a version 1.0 payload (legacy format)
        payload_dict = {
            "version": "1.0",
            "algorithm": "AES-256-GCM",
            "timestamp": "2024-01-01T00:00:00Z",
            "encryptedData": base64.b64encode(b"test ciphertext").decode('utf-8')
        }
        
        # Serialize and deserialize
        payload_binary = payload_serializer.serialize_to_binary(payload_dict)
        extracted_payload = payload_deserializer.deserialize_from_binary(payload_binary)
        
        # Attempting to extract salt should raise ValueError
        with pytest.raises(ValueError, match="Legacy payload version 1.0 does not contain embedded salt"):
            payload_deserializer.extract_salt(extracted_payload)
        
        # Attempting to extract iv should raise ValueError
        with pytest.raises(ValueError, match="Legacy payload version 1.0 does not contain embedded IV"):
            payload_deserializer.extract_iv(extracted_payload)
    
    def test_wrong_password_fails_with_embedded_metadata(self):
        """Test that wrong password fails even with embedded metadata"""
        message = "Secret message"
        password = "correct_password"
        wrong_password = "wrong_password"
        
        # Encrypt
        encrypt_result = crypto_service.encrypt_message(message, password)
        
        # Create payload with embedded metadata
        payload_dict = payload_serializer.create_payload(
            encrypted_data=encrypt_result["ciphertext"],
            salt=encrypt_result["salt"],
            iv=encrypt_result["iv"]
        )
        payload_binary = payload_serializer.serialize_to_binary(payload_dict)
        
        # Deserialize and extract metadata
        extracted_payload = payload_deserializer.deserialize_from_binary(payload_binary)
        extracted_ciphertext = payload_deserializer.extract_encrypted_data(extracted_payload)
        extracted_salt = payload_deserializer.extract_salt(extracted_payload)
        extracted_iv = payload_deserializer.extract_iv(extracted_payload)
        
        # Attempt to decrypt with wrong password should fail
        with pytest.raises(ValueError):
            crypto_service.decrypt_message(
                ciphertext=extracted_ciphertext,
                password=wrong_password,
                salt=extracted_salt,
                iv=extracted_iv
            )
    
    def test_payload_integrity_validation(self):
        """Test that payload deserializer validates payload structure"""
        # Valid payload
        valid_payload = {
            "version": "2.0",
            "algorithm": "AES-256-GCM",
            "kdf": "Argon2id",
            "timestamp": "2024-01-01T00:00:00Z",
            "salt": base64.b64encode(b"salt").decode('utf-8'),
            "iv": base64.b64encode(b"iv").decode('utf-8'),
            "encryptedData": base64.b64encode(b"ciphertext").decode('utf-8')
        }
        
        # Should not raise exception
        payload_deserializer._validate_payload(valid_payload)
        
        # Invalid payload - missing required field
        invalid_payload = {
            "version": "2.0",
            "algorithm": "AES-256-GCM"
            # Missing required fields
        }
        
        with pytest.raises(ValueError, match="missing required field"):
            payload_deserializer._validate_payload(invalid_payload)
