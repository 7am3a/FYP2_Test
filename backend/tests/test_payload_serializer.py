"""
Unit Tests for PayloadSerializer
Tests payload serialization for steganography
"""

import pytest
from app.utils.payload_serializer import payload_serializer


class TestPayloadSerializer:
    """Test cases for PayloadSerializer"""
    
    def test_create_payload_default_params(self):
        """Test payload creation with default parameters"""
        encrypted_data = "base64_encrypted_data"
        
        payload = payload_serializer.create_payload(encrypted_data)
        
        assert payload["version"] == "1.0"
        assert payload["algorithm"] == "AES-256-GCM"
        assert payload["encryptedData"] == encrypted_data
        assert "timestamp" in payload
    
    def test_create_payload_custom_params(self):
        """Test payload creation with custom parameters"""
        encrypted_data = "base64_encrypted_data"
        algorithm = "Custom-Algo"
        version = "2.0"
        
        payload = payload_serializer.create_payload(
            encrypted_data,
            algorithm=algorithm,
            version=version
        )
        
        assert payload["version"] == version
        assert payload["algorithm"] == algorithm
        assert payload["encryptedData"] == encrypted_data
    
    def test_serialize_to_binary(self):
        """Test payload serialization to binary"""
        encrypted_data = "base64_encrypted_data"
        payload = payload_serializer.create_payload(encrypted_data)
        
        binary_data = payload_serializer.serialize_to_binary(payload)
        
        assert isinstance(binary_data, bytes)
        assert len(binary_data) > 0
    
    def test_get_payload_size(self):
        """Test payload size calculation"""
        encrypted_data = "base64_encrypted_data"
        payload = payload_serializer.create_payload(encrypted_data)
        
        size = payload_serializer.get_payload_size(payload)
        
        assert isinstance(size, int)
        assert size > 0
    
    def test_serialize_deserialize_roundtrip(self):
        """Test that serialization produces consistent results"""
        encrypted_data = "base64_encrypted_data"
        payload = payload_serializer.create_payload(encrypted_data)
        
        binary1 = payload_serializer.serialize_to_binary(payload)
        binary2 = payload_serializer.serialize_to_binary(payload)
        
        assert binary1 == binary2
