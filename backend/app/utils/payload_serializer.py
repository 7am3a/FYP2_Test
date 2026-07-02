"""
Payload Serializer Module for SecureStego

This module handles the serialization of steganography payloads.
It creates a structured payload format that includes metadata alongside the encrypted data.

Why Structured Payload:
- Allows versioning for future compatibility
- Includes encryption algorithm information
- Stores timestamp for audit trail
- Enables validation during extraction
- Facilitates future extensions (video, audio steganography)
- Embeds all encryption metadata for password-only extraction

Payload Structure (Version 2.0):
{
    "version": "2.0",
    "algorithm": "AES-256-GCM",
    "kdf": "Argon2id",
    "timestamp": "ISO-8601 timestamp",
    "salt": "base64 encoded salt",
    "iv": "base64 encoded IV",
    "encryptedData": "base64 encoded encrypted message"
}

Note: Deserialization is handled by payload_deserializer.py
"""

import json
from datetime import datetime
from typing import Dict, Any
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class PayloadSerializer:
    """
    Serializes steganography payloads for embedding.
    
    Why this exists:
    - Provides a consistent payload format for embedding
    - Includes metadata for validation and debugging
    - Enables version control for future changes
    - Facilitates extraction with proper validation
    - Embeds all encryption metadata for password-only extraction
    
    Security Considerations:
    - Payload is JSON-encoded for easy parsing
    - Encrypted data is base64-encoded for binary safety
    - Salt and IV are embedded in payload for automatic recovery
    - Timestamp provides audit trail
    - Version field enables backward compatibility
    """
    
    # Current payload version
    PAYLOAD_VERSION = "2.0"
    
    # Default encryption algorithm
    DEFAULT_ALGORITHM = "AES-256-GCM"
    
    # Default key derivation function
    DEFAULT_KDF = "Argon2id"
    
    def __init__(self):
        """Initialize the payload serializer."""
        logger.info("PayloadSerializer initialized")
    
    def create_payload(
        self,
        encrypted_data: str,
        salt: str,
        iv: str,
        algorithm: str = None,
        kdf: str = None,
        version: str = None
    ) -> Dict[str, Any]:
        """
        Create a structured payload for embedding.
        
        This method:
        1. Creates a dictionary with metadata
        2. Includes version, algorithm, kdf, timestamp
        3. Embeds salt and iv for automatic recovery
        4. Adds the encrypted data
        5. Returns the structured payload
        
        Parameters:
        encrypted_data (str):
            Base64-encoded encrypted message from encryption service.
        salt (str):
            Base64-encoded salt for key derivation.
        iv (str):
            Base64-encoded IV for encryption.
        algorithm (str, optional):
            Encryption algorithm used (default: AES-256-GCM).
        kdf (str, optional):
            Key derivation function used (default: Argon2id).
        version (str, optional):
            Payload version (default: current version).
            
        Returns:
        Dict[str, Any]: Structured payload dictionary.
        """
        try:
            logger.info("Creating structured payload with embedded metadata")
            
            payload = {
                "version": version or self.PAYLOAD_VERSION,
                "algorithm": algorithm or self.DEFAULT_ALGORITHM,
                "kdf": kdf or self.DEFAULT_KDF,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "salt": salt,
                "iv": iv,
                "encryptedData": encrypted_data
            }
            
            logger.info(
                f"Payload created: version={payload['version']}, "
                f"algorithm={payload['algorithm']}, "
                f"kdf={payload['kdf']}"
            )
            
            return payload
            
        except Exception as e:
            logger.error(f"Payload creation error: {e}")
            raise
    
    def serialize_to_binary(self, payload: Dict[str, Any]) -> bytes:
        """
        Convert payload dictionary to binary format for embedding.
        
        This method:
        1. Converts dictionary to JSON string
        2. Encodes JSON string to UTF-8 bytes
        3. Returns binary data ready for embedding
        
        Parameters:
        payload (Dict[str, Any]):
            Structured payload dictionary.
            
        Returns:
        bytes: Binary representation of payload.
            
        Raises:
        ValueError: If payload cannot be serialized.
        """
        try:
            logger.info("Serializing payload to binary")
            
            # Convert to JSON string
            json_string = json.dumps(payload, separators=(',', ':'))
            
            # Encode to UTF-8 bytes
            binary_data = json_string.encode('utf-8')
            
            logger.info(f"Payload serialized: {len(binary_data)} bytes")
            
            return binary_data
            
        except Exception as e:
            logger.error(f"Payload serialization error: {e}")
            raise ValueError(f"Failed to serialize payload: {e}")
    
    def get_payload_size(self, payload: Dict[str, Any]) -> int:
        """
        Calculate the binary size of a payload.
        
        Parameters:
        payload (Dict[str, Any]):
            Payload dictionary.
            
        Returns:
        int: Size in bytes when serialized.
        """
        binary_data = self.serialize_to_binary(payload)
        return len(binary_data)


# Global payload serializer instance
payload_serializer = PayloadSerializer()
