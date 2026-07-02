"""
Video Steganography Service for SecureStego

This service orchestrates the entire video steganography workflow, coordinating
between video processing, frame selection, DCT transformation, payload serialization,
and audio preservation.

Workflow:
Embed:
1. Validate video format
2. Convert to MP4
3. Extract audio track
4. Extract frames
5. Select embedding frames
6. Serialize payload
7. Embed using DCT
8. Rebuild video
9. Reattach audio
10. Return stego video

Extract:
1. Validate video is MP4
2. Extract frames
3. Extract using DCT
4. Deserialize payload
5. Return encrypted data
"""

import os
import time
import cv2
from typing import Dict, Optional
from app.utils.logging_config import get_logger
from app.video_processing.video_validator import video_validator
from app.video_processing.video_converter import video_converter
from app.video_processing.frame_extractor import frame_extractor
from app.video_processing.frame_rebuilder import frame_rebuilder
from app.video_processing.audio_handler import audio_handler
from app.steganography.video.frame_selector import frame_selector
from app.steganography.video.dct_embedder import dct_embedder
from app.steganography.video.dct_extractor import dct_extractor
from app.utils.payload_serializer import payload_serializer
from app.utils.payload_deserializer import payload_deserializer
from app.services.platform_verification_service import platform_verification_service
from app.verification.signature_exceptions import SignatureVerificationError

logger = get_logger(__name__)


class VideoSteganographyService:
    """
    High-level service for video steganography operations.
    
    Why this exists:
    - Orchestrates all video steganography components
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
        """Initialize the video steganography service."""
        logger.info("VideoSteganographyService initialized")
    
    def embed_message(
        self,
        video_path: str,
        encrypted_data: str,
        salt: str,
        iv: str,
        algorithm: str = "AES-256-GCM",
        kdf: str = "Argon2id",
        frame_selection_strategy: str = "fixed_interval",
        frame_interval: int = 10
    ) -> Dict:
        """
        Complete workflow to embed encrypted message into a video.
        
        This method:
        1. Validates video format
        2. Converts video to MP4
        3. Extracts audio track
        4. Extracts frames from video
        5. Selects frames for embedding
        6. Creates structured payload
        7. Embeds payload using DCT
        8. Rebuilds video from frames
        9. Reattaches audio track
        10. Returns stego video path and statistics
        
        Parameters:
        video_path (str):
            Path to the uploaded video file.
        encrypted_data (str):
            Base64-encoded encrypted message from encryption service.
        salt (str):
            Base64-encoded salt for key derivation.
        iv (str):
            Base64-encoded IV for encryption.
        algorithm (str):
            Encryption algorithm used (default: AES-256-GCM).
        frame_selection_strategy (str):
            Frame selection strategy (default: fixed_interval).
        frame_interval (int):
            Interval for fixed interval selection (default: 10).
            
        Returns:
        Dict: Dictionary containing:
            - stegoVideoPath: Path to generated stego video
            - fileName: Name of the stego video file
            - originalFormat: Original video format
            - statistics: Detailed embedding statistics
            
        Raises:
        ValueError: If video format is unsupported or capacity insufficient
        IOError: If video processing fails
        """
        start_time = time.time()
        temp_mp4_path = None
        temp_audio_path = None
        temp_frames_dir = None
        temp_video_no_audio = None
        
        try:
            logger.info(f"Starting video embed workflow for: {video_path}")
            
            # Step 1: Validate video
            logger.info("Step 1: Validating video")
            is_valid, validation_error = video_validator.validate_file(video_path)
            if not is_valid:
                raise ValueError(f"Video validation failed: {validation_error}")
            
            # Step 2: Convert to MP4
            logger.info("Step 2: Converting video to MP4")
            if not video_converter.is_supported_format(video_path):
                raise ValueError(
                    f"Unsupported video format. "
                    f"Supported: {', '.join(video_converter.SUPPORTED_FORMATS)}"
                )
            
            original_format = video_converter.get_video_format(video_path)
            temp_mp4_path, original_format = video_converter.convert_to_mp4(video_path)
            logger.info(f"Video converted: {original_format} -> MP4")
            
            # Step 3: Extract audio
            logger.info("Step 3: Extracting audio track")
            temp_audio_path = audio_handler.extract_audio(temp_mp4_path)
            if temp_audio_path:
                logger.info(f"Audio extracted: {temp_audio_path}")
            else:
                logger.info("Video has no audio track")
            
            # Step 4: Extract frames
            logger.info("Step 4: Extracting frames")
            frame_paths, frame_metadata = frame_extractor.extract_frames(
                temp_mp4_path,
                interval=1  # Extract all frames for selection
            )
            temp_frames_dir = frame_metadata['frameDirectory']
            total_frames = len(frame_paths)
            logger.info(f"Extracted {total_frames} frames")
            
            # Step 5: Create structured payload with embedded metadata
            logger.info("Step 5: Creating structured payload with embedded metadata")
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
            
            # Step 5.5: Inject platform signature
            logger.info("Step 5.5: Injecting platform signature")
            combined_payload, signature_info = platform_verification_service.prepare_payload_for_embedding(
                encrypted_payload_binary=payload_binary,
                media_type="video"
            )
            logger.info(
                f"Platform signature injected: signature_size={signature_info['signatureSize']} bytes, "
                f"combined_size={signature_info['combinedSize']} bytes"
            )
            
            # Step 6: Calculate frame capacity
            logger.info("Step 6: Calculating frame capacity")
            # Read first frame to get dimensions
            first_frame = cv2.imread(frame_paths[0])
            frame_height, frame_width = first_frame.shape[:2]
            
            frame_capacity = frame_selector.calculate_frame_capacity(
                frame_width,
                frame_height,
                coefficient_count=15,
                bits_per_coefficient=1
            )
            
            # Step 7: Select frames for embedding
            logger.info("Step 7: Selecting frames for embedding")
            selected_frame_indices, selection_metadata = frame_selector.select_frames(
                total_frames=total_frames,
                required_capacity=len(combined_payload),
                strategy=frame_selection_strategy,
                interval=frame_interval,
                frame_capacity=frame_capacity
            )
            
            logger.info(f"Selected {len(selected_frame_indices)} frames for embedding")
            
            # Step 8: Embed payload into selected frames
            logger.info("Step 8: Embedding payload into selected frames")
            modified_frame_paths = []
            total_bits_embedded = 0
            
            for frame_idx in selected_frame_indices:
                if frame_idx >= len(frame_paths):
                    break
                
                # Read frame
                frame = cv2.imread(frame_paths[frame_idx])
                
                # Embed payload (distribute across frames)
                # For simplicity, embed full payload in first frame
                # In production, distribute across multiple frames
                if frame_idx == selected_frame_indices[0]:
                    modified_frame, embed_stats = dct_embedder.embed(
                        frame,
                        combined_payload
                    )
                    # ==========================
                    # DEBUG STEP 1
                    # Verify DCT embed/extract
                    # ==========================

                    logger.info("========== DEBUG STEP 1 ==========")

                    recovered_payload, _ = dct_extractor.extract(modified_frame)

                    logger.info(f"Original payload size : {len(combined_payload)}")
                    logger.info(f"Recovered payload size: {len(recovered_payload)}")
                    logger.info(
                        f"First 32 bytes original : {combined_payload[:32].hex()}"
                    )

                    logger.info(
                        f"First 32 bytes recovered: {recovered_payload[:32].hex()}"
                    )

                    if combined_payload == recovered_payload:
                        logger.info("DEBUG RESULT: Payloads are IDENTICAL")

                    else:
                        logger.error("DEBUG RESULT: Payloads DIFFER")

                        mismatch_found = False

                        for i, (a, b) in enumerate(zip(combined_payload, recovered_payload)):
                            if a != b:
                                logger.error(
                                    f"FIRST DIFFERENCE at byte {i}: "
                                    f"original={a:02X} recovered={b:02X} "
                                    f"xor={(a ^ b):02X}"
                                )
                                mismatch_found = True
                                break

                        if not mismatch_found and len(combined_payload) != len(recovered_payload):
                            logger.error("Payload lengths differ.")
                    
                    total_bits_embedded = embed_stats['totalBitsEmbedded']
                else:
                    modified_frame = frame  # Keep other frames unchanged
                
                # Save modified frame
                cv2.imwrite(frame_paths[frame_idx], modified_frame)

                # ==========================
                # DEBUG STEP 2
                # Verify PNG save/load
                # ==========================

                logger.info("========== DEBUG STEP 2 ==========")

                saved_frame = cv2.imread(frame_paths[frame_idx])

                saved_payload, _ = dct_extractor.extract(saved_frame)

                logger.info(
                    f"Payload after PNG save identical: "
                    f"{saved_payload == combined_payload}"
                )

                if saved_payload != combined_payload:
                    for i, (a, b) in enumerate(zip(combined_payload, saved_payload)):
                        if a != b:
                            logger.error(
                                f"PNG mismatch at byte {i}: "
                                f"{a:02X} -> {b:02X}"
                            )
                            break

                modified_frame_paths.append(frame_paths[frame_idx])
            
            logger.info(f"Payload embedded: {total_bits_embedded} bits")
            
            # Step 9: Rebuild video from frames
            logger.info("Step 9: Rebuilding video from frames")
            
            
            temp_video_no_audio = frame_rebuilder.rebuild_video(
                frame_paths,
                fps=frame_metadata.get('fps', 30.0),
                original_video_path=temp_mp4_path
            )
            logger.info(f"Video rebuilt: {temp_video_no_audio}")
            
            # ==========================================
            # DEBUG STEP 3
            # Verify payload after rebuilt video
            # ==========================================

            logger.info("========== DEBUG STEP 3 ==========")

            import tempfile
            import subprocess

            debug_frame = os.path.join(
                tempfile.gettempdir(),
                "debug_first_frame.png"
            )

            subprocess.run([
                "ffmpeg",
                "-y",
                "-i", temp_video_no_audio,
                "-frames:v", "1",
                debug_frame
            ], stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

            rebuilt_frame = cv2.imread(debug_frame)

            rebuilt_payload, _ = dct_extractor.extract(rebuilt_frame)

            logger.info(
                f"Payload after rebuilt video identical: "
                f"{rebuilt_payload == combined_payload}"
            )

            if rebuilt_payload != combined_payload:

                logger.error("Payload changed after rebuild!")

                for i, (a, b) in enumerate(zip(combined_payload, rebuilt_payload)):
                    if a != b:
                        logger.error(
                            f"FIRST DIFFERENCE after rebuild "
                            f"byte={i} "
                            f"original={a:02X} "
                            f"recovered={b:02X} "
                            f"xor={(a ^ b):02X}"
                        )
                        break

            # Step 10: Reattach audio
            logger.info("Step 10: Reattaching audio")
            if temp_audio_path:
                stego_video_path = audio_handler.attach_audio(
                    temp_video_no_audio,
                    temp_audio_path
                )
            else:
                # No audio, use video as-is
                stego_video_path = temp_video_no_audio
            
            logger.info("========== DEBUG STEP 4 ==========")

            debug_frame = os.path.join(
                tempfile.gettempdir(),
                "debug_after_audio.png"
            )

            subprocess.run([
                "ffmpeg",
                "-y",
                "-i", stego_video_path,
                "-frames:v", "1",
                debug_frame
            ], stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

            frame = cv2.imread(debug_frame)

            payload_after_audio, _ = dct_extractor.extract(frame)

            logger.info(
                f"Payload after audio identical: "
                f"{payload_after_audio == combined_payload}"
            )

            if payload_after_audio != combined_payload:
                for i, (a, b) in enumerate(zip(combined_payload, payload_after_audio)):
                    if a != b:
                        logger.error(
                            f"Audio mismatch at byte {i}: "
                            f"{a:02X}->{b:02X}"
                        )
                        break

            # Generate final filename
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            final_filename = f"{base_name}_stego.mp4"
            final_path = os.path.join(os.path.dirname(stego_video_path), final_filename)
            os.rename(stego_video_path, final_path)
            
            # Cleanup temporary files
            self._cleanup_temp_files(
                temp_mp4_path,
                temp_audio_path,
                temp_frames_dir,
                temp_video_no_audio if temp_video_no_audio != final_path else None
            )
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare response
            response = {
                'stegoVideoPath': final_path,
                'fileName': final_filename,
                'originalFormat': original_format,
                'convertedFormat': 'MP4',
                'statistics': {
                    'videoWidth': frame_width,
                    'videoHeight': frame_height,
                    'totalFrames': total_frames,
                    'selectedFrames': len(selected_frame_indices),
                    'frameSelectionStrategy': frame_selection_strategy,
                    'frameInterval': frame_interval,
                    'payloadSize': payload_size,
                    'totalBitsEmbedded': total_bits_embedded,
                    'capacityRemaining': selection_metadata['capacityRemaining'],
                    'capacityUsedPercent': selection_metadata.get('capacityUsedPercent', 0),
                    'embeddingMethod': 'DCT-Based Block Steganography',
                    'audioPreserved': temp_audio_path is not None,
                    'processingTime': round(processing_time, 3),
                    # Development debug information
                    'debug': {
                        'originalFormat': original_format,
                        'convertedFormat': 'MP4',
                        'resolution': f"{frame_width}x{frame_height}",
                        'frameCount': total_frames,
                        'fps': frame_metadata.get('fps', 30.0),
                        'duration': frame_metadata.get('duration', 0),
                        'selectedFrames': selected_frame_indices[:10],  # First 10 for brevity
                        'dctBlocksUsed': (frame_width // 8) * (frame_height // 8) * len(selected_frame_indices),
                        'payloadSize': payload_size,
                        'capacityUsed': total_bits_embedded,
                        'capacityRemaining': selection_metadata['capacityRemaining'],
                        'audioPreserved': temp_audio_path is not None,
                        'processingTime': round(processing_time, 3),
                        'embeddingMethod': 'DCT-Based Block Steganography'
                    }
                }
            }
            
            logger.info(f"Video embed workflow completed in {processing_time:.3f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Video embed workflow error: {e}")
            # Cleanup on error
            self._cleanup_temp_files(
                temp_mp4_path,
                temp_audio_path,
                temp_frames_dir,
                temp_video_no_audio
            )
            raise
    
    def extract_message(self, video_path: str) -> Dict:
        """
        Complete workflow to extract encrypted message from a stego video.
        
        This method:
        1. Validates video is MP4
        2. Extracts frames from video
        3. Extracts payload using DCT
        4. Deserializes payload
        5. Returns encrypted data and statistics
        
        Parameters:
        video_path (str):
            Path to the stego MP4 video file.
            
        Returns:
        Dict: Dictionary containing:
            - encryptedData: Base64-encoded encrypted message
            - algorithm: Encryption algorithm used
            - version: Payload version
            - timestamp: Payload timestamp
            - statistics: Detailed extraction statistics
            
        Raises:
        ValueError: If video is invalid or contains no hidden data
        IOError: If video processing fails
        """
        start_time = time.time()
        temp_frames_dir = None
        
        try:
            logger.info(f"Starting video extract workflow for: {video_path}")
            
            # Step 1: Validate video
            logger.info("Step 1: Validating video")
            is_valid, validation_error = video_validator.validate_file(video_path)
            if not is_valid:
                raise ValueError(f"Video validation failed: {validation_error}")
            
            # Step 2: Extract frames
            logger.info("Step 2: Extracting frames")
            frame_paths, frame_metadata = frame_extractor.extract_frames(
                video_path,
                interval=1  # Extract all frames
            )
            temp_frames_dir = frame_metadata['frameDirectory']
            total_frames = len(frame_paths)
            logger.info(f"Extracted {total_frames} frames")
            
            # Step 3: Try to extract payload from frames
            logger.info("Step 3: Extracting payload from frames")
            combined_payload = None
            extract_stats = None
            
            # Try first few frames to find payload
            for frame_idx in range(min(20, total_frames)):
                frame = cv2.imread(frame_paths[frame_idx])
                
                try:
                    combined_payload, extract_stats = dct_extractor.extract(frame)
                    
                    if combined_payload and len(combined_payload) > 0:
                        logger.info(f"Payload found in frame {frame_idx}")
                        break
                except ValueError:
                    # No payload in this frame, try next
                    continue
            
            if combined_payload is None:
                raise ValueError(
                    "No hidden payload found in video. "
                    "The video may not contain steganographic data."
                )
            
            # Step 3.5: Verify platform signature
            logger.info("Step 3.5: Verifying platform signature")
            try:
                payload_binary, verification_result = platform_verification_service.extract_and_verify_signature(
                    combined_payload=combined_payload,
                    actual_media_type="video"
                )
                logger.info(f"Platform signature verified successfully")
                logger.info(f"Verification diagnostics: {verification_result['diagnostics']}")
            except SignatureVerificationError as e:
                logger.error(f"Platform signature verification failed: {e}")
                # Cleanup frames
                frame_extractor.cleanup_frames(frame_paths)
                # Return error response instead of raising
                processing_time = time.time() - start_time
                
                # Calculate capacity statistics even for error response
                frame_width = extract_stats['frameWidth'] if extract_stats else 0
                frame_height = extract_stats['frameHeight'] if extract_stats else 0
                total_bits_extracted = extract_stats['totalBitsExtracted'] if extract_stats else 0
                frame_capacity_bytes = frame_selector.calculate_frame_capacity(
                    frame_width,
                    frame_height,
                    coefficient_count=15,
                    bits_per_coefficient=1
                )
                total_capacity_bits = (frame_capacity_bytes * 8) * total_frames
                capacity_remaining = total_capacity_bits - total_bits_extracted
                capacity_used_percent = (total_bits_extracted / total_capacity_bits) * 100 if total_capacity_bits > 0 else 0
                
                return {
                    'success': False,
                    'error': e.message,
                    'errorType': type(e).__name__,
                    'statistics': {
                        'videoWidth': frame_width,
                        'videoHeight': frame_height,
                        'totalFrames': total_frames,
                        'selectedFrames': total_frames,
                        'frameSelectionStrategy': 'all_frames',
                        'frameInterval': 1,
                        'payloadSize': extract_stats['payloadSize'] if extract_stats else 0,
                        'totalBitsEmbedded': total_bits_extracted,
                        'capacityRemaining': capacity_remaining,
                        'capacityUsedPercent': round(capacity_used_percent, 2),
                        'embeddingMethod': 'DCT-Based Block Steganography',
                        'audioPreserved': False,
                        'processingTime': round(processing_time, 3)
                    }
                }
            
            # Step 4: Deserialize payload
            logger.info("Step 4: Deserializing payload")
            payload_dict = payload_deserializer.deserialize_from_binary(payload_binary)
            encrypted_data = payload_deserializer.extract_encrypted_data(payload_dict)

            # Get frame dimensions from extraction statistics
            frame_width = extract_stats['frameWidth']
            frame_height = extract_stats['frameHeight']
            
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
            
            # Cleanup frames
            frame_extractor.cleanup_frames(frame_paths)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Calculate capacity statistics for extraction
            total_bits_extracted = extract_stats['totalBitsExtracted']
            frame_capacity_bytes = frame_selector.calculate_frame_capacity(
                frame_width,
                frame_height,
                coefficient_count=15,
                bits_per_coefficient=1
            )
            total_capacity_bits = (frame_capacity_bytes * 8) * total_frames
            capacity_remaining = total_capacity_bits - total_bits_extracted
            capacity_used_percent = (total_bits_extracted / total_capacity_bits) * 100 if total_capacity_bits > 0 else 0
            
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
                    'videoWidth': extract_stats['frameWidth'],
                    'videoHeight': extract_stats['frameHeight'],
                    'totalFrames': total_frames,
                    'selectedFrames': total_frames,  # All frames used for extraction
                    'frameSelectionStrategy': 'all_frames',
                    'frameInterval': 1,
                    'payloadSize': extract_stats['payloadSize'],
                    'totalBitsEmbedded': total_bits_extracted,
                    'capacityRemaining': capacity_remaining,
                    'capacityUsedPercent': round(capacity_used_percent, 2),
                    'embeddingMethod': 'DCT-Based Block Steganography',
                    'audioPreserved': False,  # Extraction doesn't preserve audio info
                    'processingTime': round(processing_time, 3),
                    # Development debug information
                    'debug': {
                        'resolution': f"{extract_stats['frameWidth']}x{extract_stats['frameHeight']}",
                        'frameCount': total_frames,
                        'fps': frame_metadata.get('fps', 30.0),
                        'duration': frame_metadata.get('duration', 0),
                        'payloadSize': extract_stats['payloadSize'],
                        'bitsExtracted': extract_stats['totalBitsExtracted'],
                        'processingTime': round(processing_time, 3),
                        'extractionMethod': 'DCT-Based Block Steganography'
                    }
                }
            }
            
            logger.info(f"Video extract workflow completed in {processing_time:.3f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Video extract workflow error: {e}")
            # Cleanup on error
            if temp_frames_dir:
                frame_extractor._cleanup_temp_dir(temp_frames_dir)
            raise
    
    def cleanup_stego_file(self, file_path: str) -> None:
        """
        Clean up a stego video file after download.
        
        Parameters:
        file_path (str):
            Path to the stego video file to delete.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up stego file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup stego file {file_path}: {e}")
    
    def _cleanup_temp_files(
        self,
        mp4_path: Optional[str],
        audio_path: Optional[str],
        frames_dir: Optional[str],
        video_no_audio: Optional[str]
    ) -> None:
        """
        Clean up temporary files created during processing.
        
        Parameters:
        mp4_path (Optional[str]):
            Path to temporary MP4 file.
        audio_path (Optional[str]):
            Path to temporary audio file.
        frames_dir (Optional[str]):
            Path to temporary frames directory.
        video_no_audio (Optional[str]):
            Path to temporary video without audio.
        """
        if mp4_path:
            video_converter.cleanup_temp_file(mp4_path)
        
        if audio_path:
            audio_handler.cleanup_temp_file(audio_path)
        
        if frames_dir:
            frame_extractor._cleanup_temp_dir(frames_dir)
        
        if video_no_audio:
            frame_rebuilder.cleanup_temp_file(video_no_audio)


# Global video steganography service instance
video_steganography_service = VideoSteganographyService()
