"""
Platform Verification Service for SecureStego

Purpose:
This service provides a unified interface for platform signature operations
across all media types (image, video, audio, document). It orchestrates
signature generation, injection, extraction, and validation.

Responsibilities:
- Generate platform signatures for embedding
- Inject signatures into payloads before steganography
- Extract signatures from payloads during extraction
- Validate signatures before allowing extraction
- Provide unified verification interface for all media types
- Handle verification failures with appropriate error responses
- Provide detailed diagnostics for debugging

Workflow:
Embedding:
1. Generate platform signature for media type
2. Combine signature with encrypted payload
3. Return combined payload for steganography embedding

Extraction:
1. Extract combined payload from media
2. Separate platform signature from encrypted payload
3. Verify platform signature
4. If valid, return encrypted payload for decryption
5. If invalid, reject file and stop extraction

Security Considerations:
- Platform secret key loaded from environment variables
- HMAC-SHA256 provides cryptographic integrity
- Verification happens only on backend
- Rejects files without valid signatures
- Rejects files with tampered signatures
- Logs all verification attempts for audit trail
"""

import time
from typing import Dict, Any, Optional, Tuple
from app.utils.logging_config import get_logger
from app.verification.platform_signature import platform_signature
from app.verification.signature_validator import signature_validator
from app.verification.signature_constants import SUPPORTED_MEDIA_TYPES
from app.verification.signature_exceptions import (
    SignatureVerificationError,
    MissingSignatureError,
    InvalidSignatureError,
    TamperedSignatureError,
    VersionMismatchError,
    PlatformMismatchError,
    MediaTypeMismatchError
)

logger = get_logger(__name__)


class PlatformVerificationService:
    """
    Unified service for platform signature operations.
    
    Why this exists:
    - Provides a single interface for all signature operations
    - Ensures consistent signature handling across media types
    - Coordinates signature generation, injection, extraction, validation
    - Simplifies integration with steganography services
    - Provides comprehensive error handling and diagnostics
    
    Security Considerations:
    - All verification happens on backend only
    - Platform secret key never exposed to frontend
    - Rejects files without valid signatures
    - Rejects files with tampered signatures
    - Logs all operations for security monitoring
    - Provides detailed diagnostics for debugging
    """
    
    def __init__(self):
        """
        Initialize the platform verification service.
        """
        logger.info("PlatformVerificationService initialized")
    
    def prepare_payload_for_embedding(
        self,
        encrypted_payload_binary: bytes,
        media_type: str
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Prepare payload for embedding by adding platform signature.
        
        This method:
        1. Generates platform signature for the media type
        2. Serializes signature to binary
        3. Combines signature with encrypted payload
        4. Returns combined payload and signature info
        
        The combined payload format is:
        [signature_length (4 bytes)][signature_binary][encrypted_payload_binary]
        
        Parameters:
        encrypted_payload_binary (bytes):
            Binary encrypted payload from encryption service.
        media_type (str):
            Type of media (image, video, audio, document).
            
        Returns:
        Tuple[bytes, Dict[str, Any]]: 
            - Combined binary payload (signature + encrypted payload)
            - Signature information dictionary
            
        Raises:
        ValueError: If media type is not supported or signature generation fails.
        """
        start_time = time.time()
        
        try:
            logger.info(f"Preparing payload for embedding: media_type={media_type}")
            
            # Validate media type
            if media_type not in SUPPORTED_MEDIA_TYPES:
                raise ValueError(
                    f"Unsupported media type: {media_type}. "
                    f"Supported: {', '.join(SUPPORTED_MEDIA_TYPES)}"
                )
            
            # Generate platform signature
            # Include payload data in HMAC to bind signature to this specific payload
            logger.info("Generating platform signature")
            signature_dict = platform_signature.generate_signature(
                media_type=media_type,
                payload_data=encrypted_payload_binary
            )
            
            # Serialize signature to binary
            signature_binary = platform_signature.serialize_signature(signature_dict)
            signature_size = len(signature_binary)
            
            logger.info(f"Platform signature generated: {signature_size} bytes")
            
            # Create combined payload
            # Format: [signature_length (4 bytes, big-endian)][signature][encrypted_payload]
            signature_length_bytes = signature_size.to_bytes(4, byteorder='big')
            
            combined_payload = signature_length_bytes + signature_binary + encrypted_payload_binary
            
            # Prepare signature info for response
            signature_info = {
                "signatureSize": signature_size,
                "payloadSize": len(encrypted_payload_binary),
                "combinedSize": len(combined_payload),
                "platformName": signature_dict["platform"],
                "signatureVersion": signature_dict["version"],
                "mediaType": signature_dict["mediaType"],
                "createdAt": signature_dict["createdAt"]
            }
            
            processing_time = time.time() - start_time
            logger.info(
                f"Payload prepared for embedding in {processing_time:.3f}s: "
                f"combined_size={len(combined_payload)} bytes"
            )
            
            return combined_payload, signature_info
            
        except Exception as e:
            logger.error(f"Payload preparation error: {e}")
            raise
    
    def extract_and_verify_signature(
        self,
        combined_payload: bytes,
        actual_media_type: str
    ) -> Tuple[bytes, Dict[str, Any]]:
        """
        Extract and verify platform signature from combined payload.
        
        This method:
        1. Extracts signature length from first 4 bytes
        2. Extracts signature binary
        3. Extracts encrypted payload binary
        4. Verifies platform signature
        5. Returns encrypted payload and verification result
        
        Parameters:
        combined_payload (bytes):
            Combined payload extracted from media (signature + encrypted payload).
        actual_media_type (str):
            Actual media type of the file being verified.
            
        Returns:
        Tuple[bytes, Dict[str, Any]]:
            - Encrypted payload binary (if verification successful)
            - Verification result dictionary with diagnostics
            
        Raises:
        MissingSignatureError: If signature is not present.
        InvalidSignatureError: If signature format is invalid.
        TamperedSignatureError: If HMAC verification fails.
        VersionMismatchError: If signature version is not supported.
        PlatformMismatchError: If platform identity does not match.
        MediaTypeMismatchError: If media type does not match.
        """
        start_time = time.time()
        
        try:
            logger.info(f"Extracting and verifying signature: media_type={actual_media_type}")
            
            # Validate combined payload size
            if len(combined_payload) < 4:
                raise MissingSignatureError(
                    "Combined payload too small to contain signature"
                )
            
            # Extract signature length (first 4 bytes, big-endian)
            signature_length = int.from_bytes(combined_payload[:4], byteorder='big')
            
            logger.info(f"Signature length: {signature_length} bytes")
            
            # Validate signature length
            if signature_length <= 0 or signature_length > len(combined_payload) - 4:
                raise InvalidSignatureError(
                    f"Invalid signature length: {signature_length}"
                )
            
            # Extract signature binary
            signature_binary = combined_payload[4:4 + signature_length]
            
            # Extract encrypted payload binary
            encrypted_payload = combined_payload[4 + signature_length:]
            
            logger.info(
                f"Extracted: signature={len(signature_binary)} bytes, "
                f"payload={len(encrypted_payload)} bytes"
            )
            
            # Verify platform signature
            logger.info("Verifying platform signature")
            verification_result = signature_validator.verify_from_binary(
                signature_binary=signature_binary,
                actual_media_type=actual_media_type,
                payload_data=encrypted_payload
            )
            
            processing_time = time.time() - start_time
            verification_result["diagnostics"]["extractionTime"] = round(processing_time, 3)
            
            logger.info(
                f"Signature verification completed in {processing_time:.3f}s: "
                f"valid={verification_result['valid']}"
            )
            
            # Return encrypted payload and verification result
            return encrypted_payload, verification_result
            
        except (MissingSignatureError, InvalidSignatureError, TamperedSignatureError,
                VersionMismatchError, PlatformMismatchError, MediaTypeMismatchError) as e:
            # Re-raise verification errors
            logger.error(f"Signature verification failed: {e}")
            if e.details:
                logger.error(f"Details: {e.details}")
            raise
        except Exception as e:
            logger.error(f"Signature extraction error: {e}")
            raise InvalidSignatureError(f"Failed to extract signature: {e}")
    
    def verify_file_before_extraction(
        self,
        combined_payload: bytes,
        actual_media_type: str
    ) -> Dict[str, Any]:
        """
        Verify file before allowing extraction.
        
        This is a convenience method that:
        1. Extracts and verifies signature
        2. Returns verification result only (no payload)
        3. Used for pre-extraction validation checks
        
        Parameters:
        combined_payload (bytes):
            Combined payload extracted from media.
        actual_media_type (str):
            Actual media type of the file being verified.
            
        Returns:
        Dict[str, Any]: Verification result with diagnostics.
            
        Raises:
        SignatureVerificationError: If verification fails.
        """
        try:
            logger.info("Verifying file before extraction")
            
            # Extract and verify signature
            encrypted_payload, verification_result = self.extract_and_verify_signature(
                combined_payload,
                actual_media_type
            )
            
            # Return verification result
            return verification_result
            
        except SignatureVerificationError as e:
            # Log and re-raise
            logger.error(f"File verification failed: {e}")
            raise
    
    def get_error_response(self, error: SignatureVerificationError) -> Dict[str, Any]:
        """
        Generate standardized error response for verification failures.
        
        Parameters:
        error (SignatureVerificationError):
            The verification error that occurred.
            
        Returns:
        Dict[str, Any]: Standardized error response.
        """
        logger.info(f"Generating error response for: {type(error).__name__}")
        
        response = {
            "success": False,
            "error": error.message,
            "errorType": type(error).__name__
        }
        
        # Add diagnostics if available
        if hasattr(error, 'details') and error.details:
            logger.info(f"Error details: {error.details}")
            # Details are logged but not exposed to frontend for security
        
        return response
    
    def get_verification_diagnostics(
        self,
        verification_result: Dict[str, Any]
    ) -> str:
        """
        Format verification diagnostics for display.
        
        Parameters:
        verification_result (Dict[str, Any]):
            Verification result from verify_signature.
            
        Returns:
        str: Formatted diagnostics string.
        """
        return signature_validator.get_diagnostics_display(
            verification_result.get("diagnostics", {})
        )


# Global platform verification service instance
platform_verification_service = PlatformVerificationService()
