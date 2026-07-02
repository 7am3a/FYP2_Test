"""
Steganography Service for SecureStego

This service orchestrates the entire steganography workflow, coordinating
between image processing, edge detection, payload serialization, and
LSB embedding/extraction.

Workflow:
Embed:
1. Convert image to PNG
2. Detect edges
3. Serialize payload
4. Embed using edge-based LSB
5. Return stego image

Extract:
1. Validate image is PNG
2. Detect edges
3. Extract using edge-based LSB
4. Deserialize payload
5. Return encrypted data
"""

import os
import time
from typing import Dict, Tuple, Optional
from app.utils.logging_config import get_logger
from app.image_processing.image_converter import image_converter
from app.image_processing.edge_detector import edge_detector
from app.image_processing.image_validator import image_validator
from app.utils.payload_serializer import payload_serializer
from app.utils.payload_deserializer import payload_deserializer
from app.steganography.edge_lsb_embedder import edge_lsb_embedder
from app.steganography.edge_lsb_extractor import edge_lsb_extractor
from app.services.platform_verification_service import platform_verification_service
from app.verification.signature_exceptions import SignatureVerificationError

logger = get_logger(__name__)


class SteganographyService:
    """
    High-level service for image steganography operations.
    
    Why this exists:
    - Orchestrates all steganography components
    - Provides a clean API for the routes layer
    - Handles error cases and validation
    - Manages temporary file cleanup
    - Provides comprehensive statistics for debugging
    
    Security Considerations:
    - Validates all inputs before processing
    - Cleans up temporary files after use
    - Provides capacity checking before embedding
    - Logs all operations for audit trail
    - Handles errors gracefully without exposing internals
    """
    
    def __init__(self):
        """Initialize the steganography service."""
        logger.info("SteganographyService initialized")
    
    def embed_message(
        self,
        image_path: str,
        encrypted_data: str,
        salt: str,
        iv: str,
        algorithm: str = "AES-256-GCM",
        kdf: str = "Argon2id"
    ) -> Dict:
        """
        Complete workflow to embed encrypted message into an image.
        
        This method:
        1. Validates image format
        2. Converts image to PNG if needed
        3. Detects edge pixels
        4. Creates structured payload with embedded metadata
        5. Embeds payload into edge pixels
        6. Returns stego image path and statistics
        
        Parameters:
        image_path (str):
            Path to the uploaded image file.
        encrypted_data (str):
            Base64-encoded encrypted message from encryption service.
        salt (str):
            Base64-encoded salt for key derivation.
        iv (str):
            Base64-encoded IV for encryption.
        algorithm (str):
            Encryption algorithm used (default: AES-256-GCM).
        kdf (str):
            Key derivation function used (default: Argon2id).
            
        Returns:
        Dict: Dictionary containing:
            - stegoImagePath: Path to generated stego image
            - fileName: Name of the stego image file
            - originalFormat: Original image format
            - statistics: Detailed embedding statistics
            
        Raises:
        ValueError: If image format is unsupported or capacity insufficient
        IOError: If image processing fails
        """
        start_time = time.time()
        temp_png_path = None
        
        try:
            logger.info(f"Starting embed workflow for: {image_path}")
            
            # Log original image information
            original_file_size = os.path.getsize(image_path)
            logger.info(f"Original file size: {original_file_size} bytes")
            
            # Step 1: Validate image
            logger.info("Step 1: Validating image")
            is_valid, validation_error = image_validator.validate_file(image_path)
            if not is_valid:
                raise ValueError(f"Image validation failed: {validation_error}")
            
            # Step 2: Convert image to PNG
            logger.info("Step 2: Converting image to PNG")
            if not image_converter.is_supported_format(image_path):
                raise ValueError(
                    f"Unsupported image format. "
                    f"Supported: {', '.join(image_converter.SUPPORTED_FORMATS)}"
                )
            
            original_format = image_converter.get_image_format(image_path)
            
            # Convert to PNG (even if already PNG, to get temp file)
            temp_png_path, original_format = image_converter.convert_to_png(image_path)
            logger.info(f"Image converted: {original_format} -> PNG")
            
            # Step 3: Detect edges
            logger.info("Step 3: Detecting edges")
            # Use clear_lsb=True to make edge detection LSB-invariant for extraction
            edge_map = edge_detector.detect_edges(temp_png_path, clear_lsb=True)
            edge_coordinates = edge_detector.get_edge_pixel_coordinates(edge_map)
            edge_count = len(edge_coordinates)
            logger.info(f"Edge detection complete: {edge_count} edge pixels")
            
            # Step 4: Create structured payload with embedded metadata
            logger.info("Step 4: Creating structured payload with embedded metadata")
            payload_dict = payload_serializer.create_payload(
                encrypted_data=encrypted_data,
                salt=salt,
                iv=iv,
                algorithm=algorithm,
                kdf=kdf
            )
            payload_binary = payload_serializer.serialize_to_binary(payload_dict)
            payload_size = len(payload_binary)
            logger.info(f"Payload created: {payload_size} bytes")
            
            # Step 4.5: Inject platform signature
            logger.info("Step 4.5: Injecting platform signature")
            combined_payload, signature_info = platform_verification_service.prepare_payload_for_embedding(
                encrypted_payload_binary=payload_binary,
                media_type="image"
            )
            logger.info(
                f"Platform signature injected: signature_size={signature_info['signatureSize']} bytes, "
                f"combined_size={signature_info['combinedSize']} bytes"
            )
            
            # Step 5: Check capacity
            logger.info("Step 5: Checking capacity")
            capacity_info = edge_lsb_embedder.calculate_capacity(edge_count)
            required_bits = (len(combined_payload) * 8) + (edge_lsb_embedder.HEADER_SIZE * 8)
            available_bits = capacity_info['totalCapacityBits']
            
            if required_bits > available_bits:
                raise ValueError(
                    f"Image capacity exceeded. "
                    f"Need {required_bits} bits but only have {available_bits} bits. "
                    f"Please upload a larger image."
                )
            
            logger.info(
                f"Capacity check passed: {required_bits} bits needed, "
                f"{available_bits} bits available"
            )
            
            # Step 6: Embed payload
            logger.info("Step 6: Embedding payload")
            stego_path, embed_stats = edge_lsb_embedder.embed(
                temp_png_path,
                combined_payload,
                edge_coordinates
            )
            logger.info(f"Payload embedded: {stego_path}")
            
            # Step 7: Cleanup temporary PNG file
            image_converter.cleanup_temp_file(temp_png_path)
            
            # Log stego image file size
            stego_file_size = os.path.getsize(stego_path)
            logger.info(f"Stego file size: {stego_file_size} bytes")
            logger.info(f"File size ratio: {stego_file_size / original_file_size:.2f}x")
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare response
            response = {
                'stegoImagePath': stego_path,
                'fileName': os.path.basename(stego_path),
                'originalFormat': original_format,
                'convertedFormat': 'PNG',
                'statistics': {
                    'imageWidth': embed_stats['imageWidth'],
                    'imageHeight': embed_stats['imageHeight'],
                    'totalPixels': embed_stats['totalPixels'],
                    'edgePixels': embed_stats['edgePixels'],
                    'payloadSize': embed_stats['payloadSize'],
                    'headerSize': embed_stats['headerSize'],
                    'totalBitsUsed': embed_stats['totalBitsUsed'],
                    'capacityRemaining': embed_stats['capacityRemaining'],
                    'capacityUsedPercent': round(embed_stats['capacityUsedPercent'], 2),
                    'embeddingMethod': 'Edge-Based LSB',
                    'edgeDetectionMethod': 'Canny',
                    'processingTime': round(processing_time, 3),
                    'originalFileSize': original_file_size,
                    'stegoFileSize': stego_file_size,
                    'fileSizeRatio': round(stego_file_size / original_file_size, 2)
                }
            }
            
            logger.info(f"Embed workflow completed in {processing_time:.3f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Embed workflow error: {e}")
            # Cleanup on error
            if temp_png_path and os.path.exists(temp_png_path):
                image_converter.cleanup_temp_file(temp_png_path)
            raise
    
    def extract_message(self, image_path: str) -> Dict:
        """
        Complete workflow to extract encrypted message from a stego image.
        
        This method:
        1. Validates image is PNG
        2. Detects edges
        3. Extracts payload from edge pixels
        4. Deserializes payload
        5. Returns encrypted data and statistics
        
        Parameters:
        image_path (str):
            Path to the stego PNG image file.
            
        Returns:
        Dict: Dictionary containing:
            - encryptedData: Base64-encoded encrypted message
            - algorithm: Encryption algorithm used
            - version: Payload version
            - timestamp: Payload timestamp
            - statistics: Detailed extraction statistics
            
        Raises:
        ValueError: If image is invalid or contains no hidden data
        IOError: If image processing fails
        """
        start_time = time.time()
        
        try:
            logger.info(f"Starting extract workflow for: {image_path}")
            
            # Step 1: Validate image
            logger.info("Step 1: Validating image")
            if not edge_lsb_extractor.validate_image(image_path):
                raise ValueError(
                    "Invalid image. Must be a PNG file containing hidden data."
                )
            
            # Step 2: Detect edges
            logger.info("Step 2: Detecting edges")
            # Use clear_lsb=True to make edge detection LSB-invariant for extraction
            edge_map = edge_detector.detect_edges(image_path, clear_lsb=True)
            edge_coordinates = edge_detector.get_edge_pixel_coordinates(edge_map)
            edge_count = len(edge_coordinates)
            logger.info(f"Edge detection complete: {edge_count} edge pixels")
            
            # Step 3: Extract payload
            logger.info("Step 3: Extracting payload")
            combined_payload, extract_stats = edge_lsb_extractor.extract(
                image_path,
                edge_coordinates
            )
            logger.info(f"Combined payload extracted: {len(combined_payload)} bytes")
            
            # Step 3.5: Verify platform signature
            logger.info("Step 3.5: Verifying platform signature")
            try:
                payload_binary, verification_result = platform_verification_service.extract_and_verify_signature(
                    combined_payload=combined_payload,
                    actual_media_type="image"
                )
                logger.info(f"Platform signature verified successfully")
                logger.info(f"Verification diagnostics: {verification_result['diagnostics']}")
            except SignatureVerificationError as e:
                logger.error(f"Platform signature verification failed: {e}")
                # Return error response instead of raising
                processing_time = time.time() - start_time
                
                # Calculate capacity statistics even for error response
                total_bits_used = extract_stats['totalBitsExtracted']
                capacity_info = edge_lsb_embedder.calculate_capacity(edge_count)
                capacity_remaining = capacity_info['totalCapacityBits'] - total_bits_used
                capacity_used_percent = (total_bits_used / capacity_info['totalCapacityBits']) * 100 if capacity_info['totalCapacityBits'] > 0 else 0
                
                return {
                    'success': False,
                    'error': e.message,
                    'errorType': type(e).__name__,
                    'statistics': {
                        'imageWidth': extract_stats['imageWidth'],
                        'imageHeight': extract_stats['imageHeight'],
                        'totalPixels': extract_stats['totalPixels'],
                        'edgePixels': extract_stats['edgePixels'],
                        'payloadSize': extract_stats['payloadSize'],
                        'headerSize': extract_stats['headerSize'],
                        'totalBitsUsed': total_bits_used,
                        'capacityRemaining': capacity_remaining,
                        'capacityUsedPercent': round(capacity_used_percent, 2),
                        'embeddingMethod': 'Edge-Based LSB',
                        'edgeDetectionMethod': 'Canny',
                        'processingTime': round(processing_time, 3)
                    }
                }
            
            # Step 4: Deserialize payload
            logger.info("Step 4: Deserializing payload")
            payload_dict = payload_deserializer.deserialize_from_binary(payload_binary)
            encrypted_data = payload_deserializer.extract_encrypted_data(payload_dict)
            
            # Extract metadata for password-only decryption (version 2.0+)
            payload_version = payload_dict.get('version', '1.0')
            kdf = payload_deserializer.extract_kdf(payload_dict)
            
            # Try to extract salt and iv (will raise exception for legacy version 1.0)
            salt = None
            iv = None
            try:
                salt = payload_deserializer.extract_salt(payload_dict)
                iv = payload_deserializer.extract_iv(payload_dict)
                logger.info(f"Extracted encryption metadata from payload version {payload_version}")
            except ValueError as e:
                logger.warning(f"Could not extract encryption metadata: {e}")
                # This is expected for legacy version 1.0 payloads
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Calculate capacity statistics for extraction
            total_bits_used = extract_stats['totalBitsExtracted']
            capacity_info = edge_lsb_embedder.calculate_capacity(edge_count)
            capacity_remaining = capacity_info['totalCapacityBits'] - total_bits_used
            capacity_used_percent = (total_bits_used / capacity_info['totalCapacityBits']) * 100 if capacity_info['totalCapacityBits'] > 0 else 0
            
            # Prepare response
            response = {
                'encryptedData': encrypted_data,
                'algorithm': payload_dict.get('algorithm'),
                'kdf': kdf,
                'salt': salt,
                'iv': iv,
                'version': payload_version,
                'timestamp': payload_dict.get('timestamp'),
                'statistics': {
                    'imageWidth': extract_stats['imageWidth'],
                    'imageHeight': extract_stats['imageHeight'],
                    'totalPixels': extract_stats['totalPixels'],
                    'edgePixels': extract_stats['edgePixels'],
                    'payloadSize': extract_stats['payloadSize'],
                    'headerSize': extract_stats['headerSize'],
                    'totalBitsUsed': total_bits_used,
                    'capacityRemaining': capacity_remaining,
                    'capacityUsedPercent': round(capacity_used_percent, 2),
                    'embeddingMethod': 'Edge-Based LSB',
                    'edgeDetectionMethod': 'Canny',
                    'processingTime': round(processing_time, 3)
                }
            }
            
            logger.info(f"Extract workflow completed in {processing_time:.3f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Extract workflow error: {e}")
            raise
    
    def cleanup_stego_file(self, file_path: str) -> None:
        """
        Clean up a stego image file after download.
        
        Parameters:
        file_path (str):
            Path to the stego image file to delete.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up stego file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup stego file {file_path}: {e}")


# Global steganography service instance
steganography_service = SteganographyService()
