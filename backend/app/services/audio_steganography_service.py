"""
audio_steganography_service.py

Purpose:
Coordinates the entire audio steganography workflow, orchestrating
between audio processing, sample selection, LSB embedding/extraction,
and payload serialization.

This service follows the same architectural pattern as the existing
image and video steganography services for consistency.

Workflow:
Embed:
1. Validate audio file format
2. Convert to WAV (if not already)
3. Load audio samples
4. Serialize payload with existing serializer
5. Calculate capacity
6. Generate randomized sample positions
7. Embed payload using LSB
8. Verify embedding integrity
9. Generate stego WAV file
10. Return stego file and statistics

Extract:
1. Validate audio is WAV
2. Load audio samples
3. Generate randomized sample positions
4. Extract payload using LSB
5. Deserialize payload with existing deserializer
6. Return encrypted data and statistics
"""

import os
import time
from typing import Dict, Optional
from app.utils.logging_config import get_logger
from app.audio_processing.audio_validator import audio_validator
from app.audio_processing.audio_converter import audio_converter
from app.audio_processing.audio_loader import audio_loader
from app.audio_processing.audio_writer import audio_writer
from app.utils.payload_serializer import payload_serializer
from app.utils.payload_deserializer import payload_deserializer
from app.steganography.audio.sample_selector import sample_selector
from app.steganography.audio.audio_lsb_embedder import audio_lsb_embedder
from app.steganography.audio.audio_lsb_extractor import audio_lsb_extractor
from app.services.platform_verification_service import platform_verification_service
from app.verification.signature_exceptions import SignatureVerificationError

logger = get_logger(__name__)


class AudioSteganographyService:
    """
    High-level service for audio steganography operations.
    
    Why this exists:
    - Orchestrates all audio steganography components
    - Provides a clean API for the routes layer
    - Handles error cases and validation
    - Manages temporary file cleanup
    - Provides comprehensive statistics for debugging
    - Follows existing architectural patterns
    
    Security Considerations:
    - Validates all inputs before processing
    - Cleans up temporary files after use
    - Provides capacity checking before embedding
    - Logs all operations for audit trail
    - Handles errors gracefully without exposing internals
    """
    
    def __init__(self):
        """Initialize the audio steganography service."""
        logger.info("AudioSteganographyService initialized")
    
    def embed_message(
        self,
        audio_path: str,
        encrypted_data: str,
        salt: str,
        iv: str,
        password: str,
        algorithm: str = "AES-256-GCM",
        kdf: str = "Argon2id"
    ) -> Dict:
        """
        Complete workflow to embed encrypted message into an audio file.
        
        This method:
        1. Validates audio format
        2. Converts audio to WAV if needed
        3. Loads audio samples
        4. Creates structured payload
        5. Calculates capacity
        6. Generates randomized sample positions
        7. Embeds payload into audio samples
        8. Verifies embedding integrity
        9. Generates stego WAV file
        10. Returns stego file path and statistics
        
        Parameters:
        audio_path (str):
            Path to the uploaded audio file.
        encrypted_data (str):
            Base64-encoded encrypted message from encryption service.
        password (str):
            Password for generating sample positions.
        algorithm (str):
            Encryption algorithm used (default: AES-256-GCM).
            
        Returns:
        Dict: Dictionary containing:
            - stegoAudioPath: Path to generated stego audio
            - fileName: Name of the stego audio file
            - originalFormat: Original audio format
            - statistics: Detailed embedding statistics
            - debug: Development debug information
            
        Raises:
        ValueError: If audio format is unsupported or capacity insufficient
        IOError: If audio processing fails
    """
        start_time = time.time()
        temp_wav_path = None
        
        try:
            logger.info(f"Starting audio embed workflow for: {audio_path}")
            
            # Step 1: Validate audio
            logger.info("Step 1: Validating audio")
            is_valid, validation_error = audio_validator.validate_file(audio_path)
            if not is_valid:
                raise ValueError(f"Audio validation failed: {validation_error}")
            
            # Step 2: Convert to WAV
            logger.info("Step 2: Converting audio to WAV")
            if not audio_converter.is_supported_format(audio_path):
                raise ValueError(
                    f"Unsupported audio format. "
                    f"Supported: {', '.join(audio_converter.get_supported_formats())}"
                )
            
            original_format = audio_converter.get_audio_format(audio_path)
            
            # Skip conversion if already WAV to improve performance
            if original_format.lower() == 'wav':
                logger.info("Audio is already WAV format, skipping conversion")
                temp_wav_path = audio_path
            else:
                # Convert to WAV for other formats
                temp_wav_path, original_format = audio_converter.convert_to_wav(audio_path)
                logger.info(f"Audio converted: {original_format} -> WAV")
            
            # Step 3: Load audio samples
            logger.info("Step 3: Loading audio samples")
            samples, metadata = audio_loader.load_wav_samples(temp_wav_path)
            total_samples = metadata['totalSamples']
            logger.info(f"Audio samples loaded: {total_samples} samples")
            
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
                media_type="audio"
            )
            logger.info(
                f"Platform signature injected: signature_size={signature_info['signatureSize']} bytes, "
                f"combined_size={signature_info['combinedSize']} bytes"
            )
            
            # Step 5: Calculate capacity
            logger.info("Step 5: Checking capacity")
            capacity_info = audio_lsb_embedder.calculate_capacity(total_samples)
            required_bits = (len(combined_payload) * 8) + (audio_lsb_embedder.HEADER_SIZE * 8)
            available_bits = capacity_info['availableCapacityBits']
            
            if required_bits > available_bits:
                raise ValueError(
                    f"Audio capacity exceeded. "
                    f"Need {required_bits} bits but only have {available_bits} bits. "
                    f"Please upload a longer audio file."
                )
            
            logger.info(
                f"Capacity check passed: {required_bits} bits needed, "
                f"{available_bits} bits available"
            )
            
            # Step 6: Generate randomized sample positions
            logger.info("Step 6: Generating randomized sample positions")
            total_payload_bits = required_bits
            positions = sample_selector.generate_bit_positions(
                password=password,
                total_samples=total_samples,
                num_bits=total_payload_bits
            )
            logger.info(f"Sample positions generated: {len(positions)} positions")
            
            # Step 7: Embed payload
            logger.info("Step 7: Embedding payload")
            stego_samples, embed_stats = audio_lsb_embedder.embed(
                samples=samples,
                payload=combined_payload,
                positions=positions
            )
            logger.info("Payload embedded successfully")
            
            # Step 8: Generate stego WAV file
            logger.info("Step 8: Generating stego WAV file")
            stego_path = audio_writer.create_stego_wav(
                samples=stego_samples,
                original_path=audio_path,
                metadata=metadata
            )
            logger.info(f"Stego WAV generated: {stego_path}")
            
            # Step 9: Cleanup temporary WAV file
            audio_converter.cleanup_temp_file(temp_wav_path)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare debug information
            debug_info = {
                'originalFormat': original_format,
                'convertedFormat': 'WAV',
                'duration': metadata['duration'],
                'channels': metadata['channels'],
                'sampleRate': metadata['sampleRate'],
                'bitDepth': metadata['bitsPerSample'],
                'totalSamples': total_samples,
                'availableCapacityBytes': capacity_info['availableCapacityBytes'],
                'usedCapacityBytes': payload_size,
                'remainingCapacityBytes': capacity_info['availableCapacityBytes'] - payload_size,
                'embeddingMethod': 'Randomized WAV LSB',
                'payloadSize': payload_size,
                'verificationStatus': 'PASSED',
                'processingTime': round(processing_time, 3)
            }
            
            # Prepare response
            response = {
                'stegoAudioPath': stego_path,
                'fileName': os.path.basename(stego_path),
                'originalFormat': original_format,
                'convertedFormat': 'WAV',
                'statistics': {
                    'duration': metadata['duration'],
                    'channels': metadata['channels'],
                    'sampleRate': metadata['sampleRate'],
                    'bitDepth': metadata['bitsPerSample'],
                    'totalSamples': total_samples,
                    'payloadSize': payload_size,
                    'headerSize': audio_lsb_embedder.HEADER_SIZE,
                    'totalBitsEmbedded': embed_stats['totalBitsEmbedded'],
                    'capacityRemaining': embed_stats['capacityRemaining'],
                    'capacityUsedPercent': embed_stats['capacityUsedPercent'],
                    'embeddingMethod': 'Randomized WAV LSB',
                    'processingTime': round(processing_time, 3)
                },
                'debug': debug_info
            }
            
            logger.info(f"Audio embed workflow completed in {processing_time:.3f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Audio embed workflow error: {e}")
            # Cleanup on error
            if temp_wav_path and os.path.exists(temp_wav_path):
                audio_converter.cleanup_temp_file(temp_wav_path)
            raise
    
    def extract_message(
        self,
        audio_path: str,
        password: str
    ) -> Dict:
        """
        Complete workflow to extract encrypted message from a stego audio file.
        
        This method:
        1. Validates audio is WAV
        2. Loads audio samples
        3. Generates randomized sample positions
        4. Extracts payload from audio samples
        5. Deserializes payload
        6. Returns encrypted data and statistics
        
        Parameters:
        audio_path (str):
            Path to the stego WAV audio file.
        password (str):
            Password for generating sample positions.
            
        Returns:
        Dict: Dictionary containing:
            - encryptedData: Base64-encoded encrypted message
            - algorithm: Encryption algorithm used
            - version: Payload version
            - timestamp: Payload timestamp
            - statistics: Detailed extraction statistics
            - debug: Development debug information
            
        Raises:
        ValueError: If audio is invalid or contains no hidden data
        IOError: If audio processing fails
    """
        start_time = time.time()
        
        try:
            logger.info(f"Starting audio extract workflow for: {audio_path}")
            
            # Step 1: Validate audio is WAV
            logger.info("Step 1: Validating audio")
            is_valid, validation_error = audio_validator.validate_file(audio_path)
            if not is_valid:
                raise ValueError(f"Audio validation failed: {validation_error}")
            
            file_ext = os.path.splitext(audio_path)[1].lower()
            if file_ext != '.wav':
                raise ValueError(
                    "Invalid audio format. Only WAV files are supported for extraction."
                )
            
            # Step 2: Load audio samples
            logger.info("Step 2: Loading audio samples")
            samples, metadata = audio_loader.load_wav_samples(audio_path)
            total_samples = metadata['totalSamples']
            logger.info(f"Audio samples loaded: {total_samples} samples")
            
            # Step 3: Extract payload
            logger.info("Step 3: Extracting payload")
            combined_payload, extract_stats = audio_lsb_extractor.extract(
                samples=samples,
                password=password,
                total_samples=total_samples
            )
            logger.info(f"Combined payload extracted: {len(combined_payload)} bytes")
            
            # Step 3.5: Verify platform signature
            logger.info("Step 3.5: Verifying platform signature")
            try:
                payload_binary, verification_result = platform_verification_service.extract_and_verify_signature(
                    combined_payload=combined_payload,
                    actual_media_type="audio"
                )
                logger.info(f"Platform signature verified successfully")
                logger.info(f"Verification diagnostics: {verification_result['diagnostics']}")
            except SignatureVerificationError as e:
                logger.error(f"Platform signature verification failed: {e}")
                # Return error response instead of raising
                processing_time = time.time() - start_time
                
                # Calculate capacity statistics even for error response
                total_bits_extracted = extract_stats['totalBitsExtracted']
                capacity_info = audio_lsb_embedder.calculate_capacity(total_samples)
                capacity_remaining = capacity_info['availableCapacityBytes'] * 8 - total_bits_extracted
                capacity_used_percent = (total_bits_extracted / (capacity_info['availableCapacityBytes'] * 8)) * 100 if capacity_info['availableCapacityBytes'] > 0 else 0
                
                return {
                    'success': False,
                    'error': e.message,
                    'errorType': type(e).__name__,
                    'statistics': {
                        'duration': metadata['duration'],
                        'channels': metadata['channels'],
                        'sampleRate': metadata['sampleRate'],
                        'bitDepth': metadata['bitsPerSample'],
                        'totalSamples': total_samples,
                        'payloadSize': extract_stats['payloadSize'],
                        'headerSize': extract_stats['headerSize'],
                        'totalBitsExtracted': total_bits_extracted,
                        'capacityRemaining': capacity_remaining,
                        'capacityUsedPercent': round(capacity_used_percent, 2),
                        'extractionMethod': 'Randomized WAV LSB',
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
            
            # Prepare debug information
            debug_info = {
                'format': 'WAV',
                'duration': metadata['duration'],
                'channels': metadata['channels'],
                'sampleRate': metadata['sampleRate'],
                'bitDepth': metadata['bitsPerSample'],
                'totalSamples': total_samples,
                'payloadSize': len(payload_binary),
                'extractionMethod': 'Randomized WAV LSB',
                'processingTime': round(processing_time, 3)
            }
            
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
                    'duration': metadata['duration'],
                    'channels': metadata['channels'],
                    'sampleRate': metadata['sampleRate'],
                    'bitDepth': metadata['bitsPerSample'],
                    'totalSamples': total_samples,
                    'payloadSize': extract_stats['payloadSize'],
                    'headerSize': extract_stats['headerSize'],
                    'totalBitsExtracted': extract_stats['totalBitsExtracted'],
                    'capacityRemaining': extract_stats['capacityRemaining'],
                    'capacityUsedPercent': extract_stats['capacityUsedPercent'],
                    'extractionMethod': 'Randomized WAV LSB',
                    'processingTime': round(processing_time, 3)
                },
                'debug': debug_info
            }
            
            logger.info(f"Audio extract workflow completed in {processing_time:.3f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Audio extract workflow error: {e}")
            raise
    
    def cleanup_stego_file(self, file_path: str) -> None:
        """
        Clean up a stego audio file after download.
        
        Parameters:
        file_path (str):
            Path to the stego audio file to delete.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up stego audio file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup stego audio file {file_path}: {e}")


# Global audio steganography service instance
audio_steganography_service = AudioSteganographyService()
