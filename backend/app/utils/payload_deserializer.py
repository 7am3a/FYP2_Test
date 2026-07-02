"""
Payload Deserializer Module for SecureStego

This module handles the deserialization of steganography payloads.
It extracts and validates structured payloads from binary data.

Why Deserialization is Separate:
- Follows Single Responsibility Principle
- Allows independent testing of deserialization logic
- Makes the codebase more maintainable
- Enables future extensions without modifying serializer

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

Legacy Payload Structure (Version 1.0):
{
    "version": "1.0",
    "algorithm": "AES-256-GCM",
    "timestamp": "ISO-8601 timestamp",
    "encryptedData": "base64 encoded encrypted message"
}
"""

import json
from typing import Dict, Any
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class PayloadDeserializer:
    """
    Deserializes steganography payloads from binary data.
    
    Why this exists:
    - Provides a dedicated interface for payload deserialization
    - Validates payload structure during extraction
    - Handles errors gracefully with clear messages
    - Enables version checking for backward compatibility
    - Automatically extracts encryption metadata for password-only decryption
    
    Security Considerations:
    - Validates all required fields are present
    - Checks version compatibility
    - Handles malformed JSON safely
    - Provides detailed error messages without exposing internals
    - Logs all deserialization attempts for audit trail
    """
    
    # Current supported payload versions
    SUPPORTED_VERSIONS = ["1.0", "2.0"]
    
    def __init__(self):
        """Initialize the payload deserializer."""
        logger.info("PayloadDeserializer initialized")
    
    def deserialize_from_binary(self, binary_data: bytes) -> Dict[str, Any]:
        """
        Convert binary data back to payload dictionary.
        
        This method:
        1. Decodes bytes to UTF-8 string
        2. Parses JSON string to dictionary
        3. Validates payload structure
        4. Checks version compatibility
        5. Returns validated payload dictionary
        
        Parameters:
        binary_data (bytes):
            Binary data extracted from image.
            
        Returns:
        Dict[str, Any]: Deserialized and validated payload dictionary.
            
        Raises:
        ValueError: If payload cannot be deserialized or is invalid.
        """
        try:
            logger.info("Deserializing payload from binary")
            logger.info(f"Binary data size: {len(binary_data)} bytes")
            
            # Decode from UTF-8 bytes
            json_string = binary_data.decode('utf-8')
            logger.info(f"Decoded to UTF-8: {len(json_string)} characters")
            
            # Parse JSON
            payload = json.loads(json_string)
            logger.info(f"JSON parsed successfully")
            
            # Validate payload structure
            self._validate_payload(payload)
            
            # Check version compatibility
            self._validate_version(payload.get('version'))
            
            logger.info(
                f"Payload deserialized successfully: "
                f"version={payload.get('version')}, "
                f"algorithm={payload.get('algorithm')}"
            )
            
            return payload
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise ValueError("Invalid payload format: not valid JSON")
        except UnicodeDecodeError as e:
            logger.error(f"Unicode decode error: {e}")
            raise ValueError("Invalid payload format: not valid UTF-8")
        except Exception as e:
            logger.error(f"Payload deserialization error: {e}")
            raise ValueError(f"Failed to deserialize payload: {e}")
    
    def _validate_payload(self, payload: Dict[str, Any]) -> None:
        """
        Validate the structure of a deserialized payload.
        
        This ensures all required fields are present and have correct types.
        Supports both version 1.0 (legacy) and 2.0 (current) payload structures.
        
        Parameters:
        payload (Dict[str, Any]):
            Payload dictionary to validate.
            
        Raises:
        ValueError: If payload is missing required fields or has invalid types.
        """
        version = payload.get('version', '1.0')
        
        # Base required fields for all versions
        required_fields = {
            'version': str,
            'algorithm': str,
            'timestamp': str,
            'encryptedData': str
        }
        
        # Additional required fields for version 2.0+
        if version == "2.0":
            required_fields.update({
                'kdf': str,
                'salt': str,
                'iv': str
            })
        
        for field, expected_type in required_fields.items():
            if field not in payload:
                raise ValueError(f"Invalid payload: missing required field '{field}'")
            
            if not isinstance(payload[field], expected_type):
                raise ValueError(
                    f"Invalid payload: field '{field}' must be {expected_type.__name__}, "
                    f"got {type(payload[field]).__name__}"
                )
        
        logger.info(f"Payload structure validation passed for version {version}")
    
    def _validate_version(self, version: str) -> None:
        """
        Validate the payload version is supported.
        
        Parameters:
        version (str):
            Payload version string.
            
        Raises:
        ValueError: If version is not supported.
        """
        if version not in self.SUPPORTED_VERSIONS:
            raise ValueError(
                f"Unsupported payload version: {version}. "
                f"Supported versions: {', '.join(self.SUPPORTED_VERSIONS)}"
            )
        
        logger.info(f"Version validation passed: {version}")
    
    def extract_encrypted_data(self, payload: Dict[str, Any]) -> str:
        """
        Extract the encrypted data from a validated payload.
        
        Parameters:
        payload (Dict[str, Any]):
            Deserialized and validated payload dictionary.
            
        Returns:
        str: Base64-encoded encrypted data.
        """
        encrypted_data = payload.get('encryptedData', '')
        logger.info(f"Extracted encrypted data: {len(encrypted_data)} characters")
        return encrypted_data
    
    def extract_algorithm(self, payload: Dict[str, Any]) -> str:
        """
        Extract the encryption algorithm from a validated payload.
        
        Parameters:
        payload (Dict[str, Any]):
            Deserialized and validated payload dictionary.
            
        Returns:
        str: Encryption algorithm name.
        """
        algorithm = payload.get('algorithm', '')
        logger.info(f"Extracted algorithm: {algorithm}")
        return algorithm
    
    def extract_version(self, payload: Dict[str, Any]) -> str:
        """
        Extract the payload version from a validated payload.
        
        Parameters:
        payload (Dict[str, Any]):
            Deserialized and validated payload dictionary.
            
        Returns:
        str: Payload version string.
        """
        version = payload.get('version', '')
        logger.info(f"Extracted version: {version}")
        return version
    
    def extract_timestamp(self, payload: Dict[str, Any]) -> str:
        """
        Extract the timestamp from a validated payload.
        
        Parameters:
        payload (Dict[str, Any]):
            Deserialized and validated payload dictionary.
            
        Returns:
        str: ISO-8601 timestamp string.
        """
        timestamp = payload.get('timestamp', '')
        logger.info(f"Extracted timestamp: {timestamp}")
        return timestamp
    
    def extract_salt(self, payload: Dict[str, Any]) -> str:
        """
        Extract the salt from a validated payload (version 2.0+).
        
        Parameters:
        payload (Dict[str, Any]):
            Deserialized and validated payload dictionary.
            
        Returns:
        str: Base64-encoded salt.
            
        Raises:
        ValueError: If salt is not present in payload (legacy version).
        """
        version = payload.get('version', '1.0')
        
        if version == "1.0":
            raise ValueError(
                "Legacy payload version 1.0 does not contain embedded salt. "
                "Please provide salt manually."
            )
        
        salt = payload.get('salt', '')
        logger.info(f"Extracted salt: {len(salt)} characters")
        return salt
    
    def extract_iv(self, payload: Dict[str, Any]) -> str:
        """
        Extract the IV from a validated payload (version 2.0+).
        
        Parameters:
        payload (Dict[str, Any]):
            Deserialized and validated payload dictionary.
            
        Returns:
        str: Base64-encoded IV.
            
        Raises:
        ValueError: If IV is not present in payload (legacy version).
        """
        version = payload.get('version', '1.0')
        
        if version == "1.0":
            raise ValueError(
                "Legacy payload version 1.0 does not contain embedded IV. "
                "Please provide IV manually."
            )
        
        iv = payload.get('iv', '')
        logger.info(f"Extracted IV: {len(iv)} characters")
        return iv
    
    def extract_kdf(self, payload: Dict[str, Any]) -> str:
        """
        Extract the key derivation function from a validated payload (version 2.0+).
        
        Parameters:
        payload (Dict[str, Any]):
            Deserialized and validated payload dictionary.
            
        Returns:
        str: Key derivation function name.
        """
        version = payload.get('version', '1.0')
        
        if version == "1.0":
            # Legacy version defaults to Argon2id
            return "Argon2id"
        
        kdf = payload.get('kdf', 'Argon2id')
        logger.info(f"Extracted KDF: {kdf}")
        return kdf
    
    def get_payload_summary(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a summary of the payload for logging/debugging.
        
        Parameters:
        payload (Dict[str, Any]):
            Deserialized payload dictionary.
            
        Returns:
        Dict[str, Any]: Summary of payload (without sensitive data).
        """
        summary = {
            'version': payload.get('version'),
            'algorithm': payload.get('algorithm'),
            'timestamp': payload.get('timestamp'),
            'encryptedDataLength': len(payload.get('encryptedData', ''))
        }
        
        logger.info(f"Payload summary: {summary}")
        return summary


# Global payload deserializer instance
payload_deserializer = PayloadDeserializer()
