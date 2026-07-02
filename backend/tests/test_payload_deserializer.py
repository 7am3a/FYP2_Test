"""
Unit Tests for PayloadDeserializer
Tests payload deserialization from steganography
"""

import pytest
from app.utils.payload_deserializer import payload_deserializer
from app.utils.payload_serializer import payload_serializer


class TestPayloadDeserializer:
    """Test cases for PayloadDeserializer"""
    
    def test_deserialize_from_binary_success(self):
        """Test successful payload deserialization"""
        encrypted_data = "base64_encrypted_data"
        payload = payload_serializer.create_payload(encrypted_data)
        binary_data = payload_serializer.serialize_to_binary(payload)
        
        deserialized = payload_deserializer.deserialize_from_binary(binary_data)
        
        assert deserialized["version"] == payload["version"]
        assert deserialized["algorithm"] == payload["algorithm"]
        assert deserialized["encryptedData"] == payload["encryptedData"]
        assert "timestamp" in deserialized
    
    def test_deserialize_invalid_json(self):
        """Test deserialization of invalid JSON raises ValueError"""
        invalid_binary = b"not valid json"
        
        with pytest.raises(ValueError, match="Invalid payload format"):
            payload_deserializer.deserialize_from_binary(invalid_binary)
    
    def test_deserialize_invalid_utf8(self):
        """Test deserialization of invalid UTF-8 raises ValueError"""
        invalid_binary = b"\xff\xfe\xfd"
        
        with pytest.raises(ValueError, match="Invalid payload format"):
            payload_deserializer.deserialize_from_binary(invalid_binary)
    
    def test_deserialize_missing_field(self):
        """Test deserialization of payload with missing field raises ValueError"""
        incomplete_payload = {"version": "1.0", "algorithm": "AES-256-GCM"}
        import json
        binary_data = json.dumps(incomplete_payload).encode('utf-8')
        
        with pytest.raises(ValueError, match="Invalid payload"):
            payload_deserializer.deserialize_from_binary(binary_data)
    
    def test_deserialize_invalid_field_type(self):
        """Test deserialization of payload with invalid field type raises ValueError"""
        invalid_payload = {
            "version": "1.0",
            "algorithm": 123,  # Should be string
            "timestamp": "2024-01-15T10:30:00Z",
            "encryptedData": "base64_data"
        }
        import json
        binary_data = json.dumps(invalid_payload).encode('utf-8')
        
        with pytest.raises(ValueError, match="Invalid payload"):
            payload_deserializer.deserialize_from_binary(binary_data)
    
    def test_deserialize_unsupported_version(self):
        """Test deserialization of unsupported version raises ValueError"""
        payload = {
            "version": "99.0",  # Unsupported version
            "algorithm": "AES-256-GCM",
            "timestamp": "2024-01-15T10:30:00Z",
            "encryptedData": "base64_data"
        }
        import json
        binary_data = json.dumps(payload).encode('utf-8')
        
        with pytest.raises(ValueError, match="Unsupported payload version"):
            payload_deserializer.deserialize_from_binary(binary_data)
    
    def test_extract_encrypted_data(self):
        """Test extraction of encrypted data from payload"""
        encrypted_data = "base64_encrypted_data"
        payload = payload_serializer.create_payload(encrypted_data)
        
        extracted = payload_deserializer.extract_encrypted_data(payload)
        
        assert extracted == encrypted_data
    
    def test_extract_algorithm(self):
        """Test extraction of algorithm from payload"""
        payload = payload_serializer.create_payload("base64_data")
        
        algorithm = payload_deserializer.extract_algorithm(payload)
        
        assert algorithm == "AES-256-GCM"
    
    def test_extract_version(self):
        """Test extraction of version from payload"""
        payload = payload_serializer.create_payload("base64_data")
        
        version = payload_deserializer.extract_version(payload)
        
        assert version == "1.0"
    
    def test_extract_timestamp(self):
        """Test extraction of timestamp from payload"""
        payload = payload_serializer.create_payload("base64_data")
        
        timestamp = payload_deserializer.extract_timestamp(payload)
        
        assert isinstance(timestamp, str)
        assert len(timestamp) > 0
    
    def test_get_payload_summary(self):
        """Test payload summary generation"""
        encrypted_data = "base64_encrypted_data"
        payload = payload_serializer.create_payload(encrypted_data)
        
        summary = payload_deserializer.get_payload_summary(payload)
        
        assert "version" in summary
        assert "algorithm" in summary
        assert "timestamp" in summary
        assert "encryptedDataLength" in summary
        assert "encryptedData" not in summary  # Should not expose sensitive data
