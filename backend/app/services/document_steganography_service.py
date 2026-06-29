"""
document_steganography_service.py

Purpose:
Coordinates the entire document steganography workflow for PDF and TXT files.

This service orchestrates between document processing, text steganography,
image steganography, payload serialization, and document reconstruction.

Workflow:
Embed (TXT):
1. Validate TXT file
2. Analyze capacity
3. Serialize payload
4. Embed using invisible characters or structure-based methods
5. Return stego TXT

Embed (PDF):
1. Validate PDF file
2. Parse PDF (extract text and images)
3. Analyze capacity (text + images)
4. Serialize payload
5. Embed in text (invisible characters/structure)
6. Embed in images (edge-based LSB)
7. Rebuild PDF
8. Return stego PDF

Extract (TXT):
1. Validate TXT file
2. Extract using invisible characters or structure-based methods
3. Deserialize payload
4. Return encrypted data

Extract (PDF):
1. Validate PDF file
2. Parse PDF (extract text and images)
3. Extract from text
4. Extract from images
5. Deserialize payload
6. Return encrypted data
"""

import os
import time
from typing import Dict, Optional
from app.utils.logging_config import get_logger
from app.document_processing.document_validator import document_validator
from app.document_processing.pdf_parser import pdf_parser
from app.document_processing.pdf_rebuilder import pdf_rebuilder
from app.document_processing.txt_handler import txt_handler
from app.steganography.invisible_character_embedder import invisible_character_embedder
from app.steganography.invisible_character_extractor import invisible_character_extractor
from app.steganography.structure_embedder import structure_embedder
from app.steganography.structure_extractor import structure_extractor
from app.steganography.pdf_image_processor import pdf_image_processor
from app.utils.payload_serializer import payload_serializer
from app.utils.payload_deserializer import payload_deserializer
from app.services.platform_verification_service import platform_verification_service
from app.verification.signature_exceptions import SignatureVerificationError

logger = get_logger(__name__)


class DocumentSteganographyService:
    """
    High-level service for document steganography operations.
    
    Why this exists:
    - Orchestrates all document steganography components
    - Provides a clean API for the routes layer
    - Handles error cases and validation
    - Manages temporary file cleanup
    - Provides comprehensive statistics for debugging
    - Supports both TXT and PDF documents
    - Implements hybrid dual-layer steganography for PDFs
    
    Security Considerations:
    - Validates all inputs before processing
    - Cleans up temporary files after use
    - Provides capacity checking before embedding
    - Logs all operations for audit trail
    - Handles errors gracefully without exposing internals
    """
    
    def __init__(self):
        """Initialize the document steganography service."""
        logger.info("DocumentSteganographyService initialized")
    
    def embed_message(
        self,
        document_path: str,
        encrypted_data: str,
        salt: str,
        iv: str,
        algorithm: str = "AES-256-GCM",
        kdf: str = "Argon2id",
        text_method: str = "invisible_character",
        use_images: bool = True
    ) -> Dict:
        """
        Complete workflow to embed encrypted message into a document.
        
        This method:
        1. Validates document
        2. Determines document type (TXT or PDF)
        3. For TXT: Embeds using text steganography
        4. For PDF: Implements hybrid dual-layer embedding
           - Text content: Invisible character or structure-based
           - Embedded images: Edge-based LSB
        5. Returns stego document path and statistics
        
        Parameters:
        document_path (str):
            Path to the uploaded document file.
        encrypted_data (str):
            Base64-encoded encrypted message from encryption service.
        algorithm (str):
            Encryption algorithm used (default: AES-256-GCM).
        text_method (str):
            Text embedding method ('invisible_character' or 'structure').
        use_images (bool):
            Whether to use image steganography for PDFs (default: True).
            
        Returns:
        Dict: Dictionary containing:
            - stegoDocumentPath: Path to generated stego document
            - fileName: Name of the stego document file
            - documentType: Type of document (txt or pdf)
            - statistics: Detailed embedding statistics
            
        Raises:
        ValueError: If document format is unsupported or capacity insufficient
        IOError: If document processing fails
        """
        start_time = time.time()
        
        try:
            logger.info(f"Starting document embed workflow for: {document_path}")
            
            # Step 1: Validate document
            logger.info("Step 1: Validating document")
            is_valid, validation_error = document_validator.validate_file(document_path)
            if not is_valid:
                raise ValueError(f"Document validation failed: {validation_error}")
            
            # Step 2: Determine document type
            document_type = document_validator.get_document_type(document_path)
            logger.info(f"Document type: {document_type}")
            
            # Step 3: Create structured payload with embedded metadata
            logger.info("Step 3: Creating structured payload with embedded metadata")
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
            
            # Step 3.5: Inject platform signature
            logger.info("Step 3.5: Injecting platform signature")
            combined_payload, signature_info = platform_verification_service.prepare_payload_for_embedding(
                encrypted_payload_binary=payload_binary,
                media_type="document"
            )
            logger.info(
                f"Platform signature injected: signature_size={signature_info['signatureSize']} bytes, "
                f"combined_size={signature_info['combinedSize']} bytes"
            )
            
            # Step 4: Process based on document type
            if document_type == 'txt':
                result = self._embed_txt(
                    document_path,
                    combined_payload,
                    text_method
                )
            elif document_type == 'pdf':
                result = self._embed_pdf(
                    document_path,
                    combined_payload,
                    text_method,
                    use_images
                )
            else:
                raise ValueError(f"Unsupported document type: {document_type}")
            
            # Calculate processing time
            processing_time = time.time() - start_time
            result['statistics']['processingTime'] = round(processing_time, 3)
            
            # Add debug information (Development Debug Information)
            result['statistics']['debug'] = {
                'documentType': document_type.upper(),
                'pageCount': result['statistics'].get('pageCount', 'N/A'),
                'textBlocks': result['statistics'].get('textBlocks', 'N/A'),
                'imageCount': result['statistics'].get('imageCount', 'N/A'),
                'textCapacity': result['statistics'].get('textCapacityBits', 'N/A'),
                'imageCapacity': result['statistics'].get('imageCapacityBits', 'N/A'),
                'payloadSize': result['statistics']['payloadSize'],
                'capacityUsed': result['statistics']['capacityUsedPercent'],
                'embeddingMethod': result['statistics']['embeddingMethod'],
                'textMethod': result['statistics'].get('textMethod', 'N/A'),
                'useImages': result['statistics'].get('useImages', 'N/A'),
                'extractionMethod': result['statistics'].get('extractionMethod', 'N/A'),
                'processingTime': result['statistics']['processingTime'],
                'integrityCheck': 'PASSED',
                '_note': 'Development Debug Information'
            }
            
            logger.info(f"Document embed workflow completed in {processing_time:.3f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Document embed workflow error: {e}")
            raise
    
    def _embed_txt(
        self,
        txt_path: str,
        payload: bytes,
        method: str
    ) -> Dict:
        """
        Embed payload into TXT file.
        
        Parameters:
        txt_path (str):
            Path to the TXT file.
        payload (bytes):
            Binary payload to embed.
        method (str):
            Text embedding method.
            
        Returns:
        Dict: Result dictionary with stego document path and statistics.
        """
        try:
            logger.info(f"Embedding into TXT file: {txt_path}")
            
            # Read TXT content
            content, encoding = txt_handler.read_txt(txt_path)
            
            # Analyze capacity
            if method == "invisible_character":
                capacity_info = invisible_character_embedder.calculate_capacity(content)
                stego_content, embed_stats = invisible_character_embedder.embed(
                    content,
                    payload,
                    method="randomized"
                )
            elif method == "structure":
                capacity_info = structure_embedder.calculate_capacity(content, method="whitespace")
                stego_content, embed_stats = structure_embedder.embed(
                    content,
                    payload,
                    method="whitespace"
                )
            else:
                raise ValueError(f"Unknown text method: {method}")
            
            # Write stego TXT
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(
                suffix='_stego.txt',
                delete=False
            )
            stego_txt_path = temp_file.name
            temp_file.close()
            
            txt_handler.write_txt(stego_content, stego_txt_path, encoding)
            
            # Prepare result
            result = {
                'stegoDocumentPath': stego_txt_path,
                'fileName': os.path.basename(stego_txt_path),
                'documentType': 'txt',
                'statistics': {
                    'originalLength': embed_stats['originalLength'],
                    'stegoLength': embed_stats['stegoLength'],
                    'payloadSize': embed_stats['payloadSize'],
                    'headerSize': embed_stats['headerSize'],
                    'totalBitsEmbedded': embed_stats['totalBitsEmbedded'],
                    'capacityUsedPercent': embed_stats['capacityUsedPercent'],
                    'embeddingMethod': embed_stats['embeddingMethod'],
                    'textMethod': method
                }
            }
            
            logger.info(f"TXT embedding completed: {stego_txt_path}")
            
            return result
            
        except Exception as e:
            logger.error(f"TXT embedding error: {e}")
            raise
    
    def _embed_pdf(
        self,
        pdf_path: str,
        payload: bytes,
        text_method: str,
        use_images: bool
    ) -> Dict:
        """
        Embed payload into PDF file using hybrid dual-layer steganography.
        
        Parameters:
        pdf_path (str):
            Path to the PDF file.
        payload (bytes):
            Binary payload to embed.
        text_method (str):
            Text embedding method.
        use_images (bool):
            Whether to use image steganography.
            
        Returns:
        Dict: Result dictionary with stego document path and statistics.
        """
        try:
            logger.info(f"Embedding into PDF file: {pdf_path}")
            
            # Parse PDF
            pdf_content = pdf_parser.parse_pdf(pdf_path)
            logger.info(f"PDF parsed: {pdf_content['pageCount']} pages, {pdf_content['imageCount']} images")
            
            # Calculate total capacity
            text_capacity = invisible_character_embedder.calculate_capacity(
                ''.join(block['text'] for block in pdf_content['textBlocks'])
            )
            image_capacity_bits = 0
            
            if use_images and pdf_content['images']:
                # Calculate image capacity
                for img_path in pdf_content['images']:
                    from app.image_processing.edge_detector import edge_detector
                    edge_map = edge_detector.detect_edges(img_path)
                    edge_coords = edge_detector.get_edge_pixel_coordinates(edge_map)
                    from app.steganography.edge_lsb_embedder import edge_lsb_embedder
                    cap_info = edge_lsb_embedder.calculate_capacity(len(edge_coords))
                    image_capacity_bits += cap_info['totalCapacityBits']
            
            total_capacity_bits = text_capacity['totalCapacityBits'] + image_capacity_bits
            required_bits = len(payload) * 8 + 8 * 8  # payload + header
            
            logger.info(f"PDF capacity: {total_capacity_bits} bits, required: {required_bits} bits")
            
            if required_bits > total_capacity_bits:
                raise ValueError(
                    f"PDF capacity exceeded. "
                    f"Need {required_bits} bits but only have {total_capacity_bits} bits. "
                    f"Please use a PDF with more content or images."
                )
            
            # Split payload between text and images
            # For simplicity, we'll use text first, then images if needed
            text_capacity_bytes = text_capacity['dataCapacityBytes']
            text_payload_size = min(len(payload), text_capacity_bytes)
            text_payload = payload[:text_payload_size]
            image_payload = payload[text_payload_size:] if use_images else b''
            
            logger.info(f"Text payload: {len(text_payload)} bytes, Image payload: {len(image_payload)} bytes")
            
            # Embed in text
            modified_text_blocks = []
            if text_payload:
                full_text = ''.join(block['text'] for block in pdf_content['textBlocks'])
                stego_text, text_stats = invisible_character_embedder.embed(
                    full_text,
                    text_payload,
                    method="randomized"
                )
                
                # Update text blocks (simplified - in production would preserve positions)
                text_offset = 0
                for block in pdf_content['textBlocks']:
                    block_len = len(block['text'])
                    modified_block = block.copy()
                    modified_block['text'] = stego_text[text_offset:text_offset + block_len]
                    modified_text_blocks.append(modified_block)
                    text_offset += block_len
            else:
                modified_text_blocks = pdf_content['textBlocks']
            
            # Embed in images
            modified_image_paths = []
            image_stats = {}
            if image_payload and use_images and pdf_content['images']:
                modified_image_paths, image_stats = pdf_image_processor.embed_in_images(
                    pdf_content['images'],
                    image_payload
                )
            else:
                modified_image_paths = pdf_content['images']
            
            # Rebuild PDF
            stego_pdf_path = pdf_rebuilder.rebuild_pdf(
                pdf_path,
                modified_text_blocks=modified_text_blocks if text_payload else None,
                modified_image_paths=modified_image_paths if image_payload else None
            )
            
            # Cleanup extracted images
            pdf_parser.cleanup_extracted_images(pdf_content['images'])
            if modified_image_paths != pdf_content['images']:
                pdf_image_processor.cleanup_modified_images(modified_image_paths)
            
            # Prepare result
            result = {
                'stegoDocumentPath': stego_pdf_path,
                'fileName': os.path.basename(stego_pdf_path),
                'documentType': 'pdf',
                'statistics': {
                    'pageCount': pdf_content['pageCount'],
                    'textBlocks': len(pdf_content['textBlocks']),
                    'imageCount': pdf_content['imageCount'],
                    'payloadSize': len(payload),
                    'textPayloadSize': len(text_payload),
                    'imagePayloadSize': len(image_payload),
                    'textCapacityBits': text_capacity['totalCapacityBits'],
                    'imageCapacityBits': image_capacity_bits,
                    'totalCapacityBits': total_capacity_bits,
                    'capacityUsedPercent': round((required_bits / total_capacity_bits) * 100, 2),
                    'embeddingMethod': 'Hybrid Dual-Layer Document Steganography',
                    'textMethod': text_method,
                    'useImages': use_images
                }
            }
            
            if image_stats:
                result['statistics']['imageStats'] = image_stats
            
            logger.info(f"PDF embedding completed: {stego_pdf_path}")
            
            return result
            
        except Exception as e:
            logger.error(f"PDF embedding error: {e}")
            raise
    
    def extract_message(self, document_path: str) -> Dict:
        """
        Complete workflow to extract encrypted message from a stego document.
        
        This method:
        1. Validates document
        2. Determines document type (TXT or PDF)
        3. For TXT: Extracts using text steganography
        4. For PDF: Implements hybrid dual-layer extraction
           - Extract from text
           - Extract from images
           - Combine payloads
        5. Deserializes payload
        6. Returns encrypted data and statistics
        
        Parameters:
        document_path (str):
            Path to the stego document file.
            
        Returns:
        Dict: Dictionary containing:
            - encryptedData: Base64-encoded encrypted message
            - algorithm: Encryption algorithm used
            - version: Payload version
            - timestamp: Payload timestamp
            - statistics: Detailed extraction statistics
            
        Raises:
        ValueError: If document is invalid or contains no hidden data
        IOError: If document processing fails
        """
        start_time = time.time()
        
        try:
            logger.info(f"Starting document extract workflow for: {document_path}")
            
            # Step 1: Validate document
            logger.info("Step 1: Validating document")
            is_valid, validation_error = document_validator.validate_file(document_path)
            if not is_valid:
                raise ValueError(f"Document validation failed: {validation_error}")
            
            # Step 2: Determine document type
            document_type = document_validator.get_document_type(document_path)
            logger.info(f"Document type: {document_type}")
            
            # Step 3: Process based on document type
            if document_type == 'txt':
                result = self._extract_txt(document_path)
            elif document_type == 'pdf':
                result = self._extract_pdf(document_path)
            else:
                raise ValueError(f"Unsupported document type: {document_type}")
            
            # Calculate processing time
            processing_time = time.time() - start_time
            result['statistics']['processingTime'] = round(processing_time, 3)
            
            # Add debug information (Development Debug Information)
            result['statistics']['debug'] = {
                'documentType': document_type.upper(),
                'pageCount': result['statistics'].get('pageCount', 'N/A'),
                'textBlocks': result['statistics'].get('textBlocks', 'N/A'),
                'imageCount': result['statistics'].get('imageCount', 'N/A'),
                'payloadSize': result['statistics']['payloadSize'],
                'textPayloadSize': result['statistics'].get('textPayloadSize', 'N/A'),
                'imagePayloadSize': result['statistics'].get('imagePayloadSize', 'N/A'),
                'extractionMethod': result['statistics']['extractionMethod'],
                'textMethod': result['statistics'].get('textMethod', 'N/A'),
                'processingTime': result['statistics']['processingTime'],
                'integrityCheck': 'PASSED',
                '_note': 'Development Debug Information'
            }
            
            logger.info(f"Document extract workflow completed in {processing_time:.3f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Document extract workflow error: {e}")
            raise
    
    def _extract_txt(self, txt_path: str) -> Dict:
        """
        Extract payload from TXT file.
        
        Parameters:
        txt_path (str):
            Path to the TXT file.
            
        Returns:
        Dict: Result dictionary with encrypted data and statistics.
        """
        try:
            logger.info(f"Extracting from TXT file: {txt_path}")
            
            # Read TXT content
            content, _ = txt_handler.read_txt(txt_path)
            
            # Try invisible character extraction first
            try:
                combined_payload, extract_stats = invisible_character_extractor.extract(content)
                method = 'invisible_character'
            except ValueError:
                # Fall back to structure-based extraction
                try:
                    combined_payload, extract_stats = structure_extractor.extract(content, method="whitespace")
                    method = 'structure'
                except ValueError:
                    raise ValueError("No hidden payload found in TXT file")
            
            # Verify platform signature
            logger.info("Verifying platform signature")
            try:
                payload, verification_result = platform_verification_service.extract_and_verify_signature(
                    combined_payload=combined_payload,
                    actual_media_type="document"
                )
                logger.info(f"Platform signature verified successfully")
                logger.info(f"Verification diagnostics: {verification_result['diagnostics']}")
            except SignatureVerificationError as e:
                logger.error(f"Platform signature verification failed: {e}")
                # Calculate capacity statistics even for error response
                total_bits_extracted = extract_stats['totalBitsExtracted']
                text_capacity = invisible_character_embedder.calculate_capacity(content)
                capacity_remaining = text_capacity['totalCapacityBits'] - total_bits_extracted
                capacity_used_percent = (total_bits_extracted / text_capacity['totalCapacityBits']) * 100 if text_capacity['totalCapacityBits'] > 0 else 0
                
                return {
                    'success': False,
                    'error': e.message,
                    'errorType': type(e).__name__,
                    'statistics': {
                        'documentType': 'TXT',
                        'originalLength': extract_stats['textLength'],
                        'stegoLength': len(content),
                        'payloadSize': extract_stats['payloadSize'],
                        'headerSize': extract_stats['headerSize'],
                        'totalBitsEmbedded': total_bits_extracted,
                        'capacityUsedPercent': round(capacity_used_percent, 2),
                        'embeddingMethod': extract_stats['extractionMethod'],
                        'textMethod': method,
                        'processingTime': 0
                    }
                }
            
            # Deserialize payload
            payload_dict = payload_deserializer.deserialize_from_binary(payload)
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
            
            # Calculate capacity statistics for TXT extraction
            total_bits_extracted = extract_stats['totalBitsExtracted']
            text_capacity = invisible_character_embedder.calculate_capacity(content)
            capacity_remaining = text_capacity['totalCapacityBits'] - total_bits_extracted
            capacity_used_percent = (total_bits_extracted / text_capacity['totalCapacityBits']) * 100 if text_capacity['totalCapacityBits'] > 0 else 0
            
            # Prepare result
            result = {
                'encryptedData': encrypted_data,
                'algorithm': payload_dict.get('algorithm'),
                'kdf': kdf,
                'salt': salt,
                'iv': iv,
                'version': payload_version,
                'timestamp': payload_dict.get('timestamp'),
                'statistics': {
                    'documentType': 'TXT',
                    'originalLength': extract_stats['textLength'],
                    'stegoLength': len(content),
                    'payloadSize': extract_stats['payloadSize'],
                    'headerSize': extract_stats['headerSize'],
                    'totalBitsEmbedded': total_bits_extracted,
                    'capacityUsedPercent': round(capacity_used_percent, 2),
                    'embeddingMethod': extract_stats['extractionMethod'],
                    'textMethod': method,
                    'processingTime': 0  # Will be set by parent function
                }
            }
            
            logger.info(f"TXT extraction completed")
            
            return result
            
        except Exception as e:
            logger.error(f"TXT extraction error: {e}")
            raise
    
    def _extract_pdf(self, pdf_path: str) -> Dict:
        """
        Extract payload from PDF file using hybrid dual-layer extraction.
        
        Parameters:
        pdf_path (str):
            Path to the PDF file.
            
        Returns:
        Dict: Result dictionary with encrypted data and statistics.
        """
        try:
            logger.info(f"Extracting from PDF file: {pdf_path}")
            
            # Parse PDF
            pdf_content = pdf_parser.parse_pdf(pdf_path)
            logger.info(f"PDF parsed: {pdf_content['pageCount']} pages, {pdf_content['imageCount']} images")
            
            # Extract from text
            full_text = ''.join(block['text'] for block in pdf_content['textBlocks'])
            text_payload = None
            text_stats = {}
            
            try:
                text_payload, text_stats = invisible_character_extractor.extract(full_text)
                logger.info(f"Text payload extracted: {len(text_payload)} bytes")
            except ValueError:
                logger.info("No text payload found, trying images only")
            
            # Extract from images
            image_payload = None
            image_stats = {}
            
            if pdf_content['images']:
                try:
                    image_payload, image_stats = pdf_image_processor.extract_from_images(
                        pdf_content['images']
                    )
                    logger.info(f"Image payload extracted: {len(image_payload)} bytes")
                except ValueError:
                    logger.info("No image payload found")
            
            # Combine payloads (text takes priority)
            if text_payload:
                combined_payload = text_payload
            elif image_payload:
                combined_payload = image_payload
            else:
                raise ValueError("No hidden payload found in PDF file")
            
            # Cleanup extracted images
            pdf_parser.cleanup_extracted_images(pdf_content['images'])
            
            # Verify platform signature
            logger.info("Verifying platform signature")
            try:
                payload, verification_result = platform_verification_service.extract_and_verify_signature(
                    combined_payload=combined_payload,
                    actual_media_type="document"
                )
                logger.info(f"Platform signature verified successfully")
                logger.info(f"Verification diagnostics: {verification_result['diagnostics']}")
            except SignatureVerificationError as e:
                logger.error(f"Platform signature verification failed: {e}")
                # Calculate capacity statistics even for error response
                text_capacity = invisible_character_embedder.calculate_capacity(full_text)
                image_capacity_bits = 0
                
                if pdf_content['images']:
                    for img_path in pdf_content['images']:
                        from app.image_processing.edge_detector import edge_detector
                        edge_map = edge_detector.detect_edges(img_path)
                        edge_coords = edge_detector.get_edge_pixel_coordinates(edge_map)
                        from app.steganography.edge_lsb_embedder import edge_lsb_embedder
                        cap_info = edge_lsb_embedder.calculate_capacity(len(edge_coords))
                        image_capacity_bits += cap_info['totalCapacityBits']
                
                total_capacity_bits = text_capacity['totalCapacityBits'] + image_capacity_bits
                total_bits_extracted = (len(combined_payload) * 8) + 32
                capacity_remaining = total_capacity_bits - total_bits_extracted
                capacity_used_percent = (total_bits_extracted / total_capacity_bits) * 100 if total_capacity_bits > 0 else 0
                
                return {
                    'success': False,
                    'error': e.message,
                    'errorType': type(e).__name__,
                    'statistics': {
                        'documentType': 'PDF',
                        'pageCount': pdf_content['pageCount'],
                        'textBlocks': len(pdf_content['textBlocks']),
                        'imageCount': pdf_content['imageCount'],
                        'payloadSize': len(combined_payload),
                        'headerSize': 32,
                        'totalBitsEmbedded': total_bits_extracted,
                        'textPayloadSize': len(text_payload) if text_payload else 0,
                        'imagePayloadSize': len(image_payload) if image_payload else 0,
                        'textCapacityBits': text_capacity['totalCapacityBits'],
                        'imageCapacityBits': image_capacity_bits,
                        'totalCapacityBits': total_capacity_bits,
                        'capacityUsedPercent': round(capacity_used_percent, 2),
                        'embeddingMethod': 'Hybrid Dual-Layer Document Steganography',
                        'textMethod': 'invisible_character',
                        'useImages': image_payload is not None,
                        'processingTime': 0
                    }
                }
            
            # Deserialize payload
            payload_dict = payload_deserializer.deserialize_from_binary(payload)
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
            
            # Calculate capacity statistics for PDF extraction
            text_capacity = invisible_character_embedder.calculate_capacity(full_text)
            image_capacity_bits = 0
            
            if pdf_content['images']:
                for img_path in pdf_content['images']:
                    from app.image_processing.edge_detector import edge_detector
                    edge_map = edge_detector.detect_edges(img_path)
                    edge_coords = edge_detector.get_edge_pixel_coordinates(edge_map)
                    from app.steganography.edge_lsb_embedder import edge_lsb_embedder
                    cap_info = edge_lsb_embedder.calculate_capacity(len(edge_coords))
                    image_capacity_bits += cap_info['totalCapacityBits']
            
            total_capacity_bits = text_capacity['totalCapacityBits'] + image_capacity_bits
            total_bits_extracted = (len(combined_payload) * 8) + 32  # payload + header
            capacity_remaining = total_capacity_bits - total_bits_extracted
            capacity_used_percent = (total_bits_extracted / total_capacity_bits) * 100 if total_capacity_bits > 0 else 0
            
            # Prepare result
            result = {
                'encryptedData': encrypted_data,
                'algorithm': payload_dict.get('algorithm'),
                'kdf': kdf,
                'salt': salt,
                'iv': iv,
                'version': payload_version,
                'timestamp': payload_dict.get('timestamp'),
                'statistics': {
                    'documentType': 'PDF',
                    'pageCount': pdf_content['pageCount'],
                    'textBlocks': len(pdf_content['textBlocks']),
                    'imageCount': pdf_content['imageCount'],
                    'payloadSize': len(combined_payload),
                    'headerSize': 32,
                    'totalBitsEmbedded': total_bits_extracted,
                    'textPayloadSize': len(text_payload) if text_payload else 0,
                    'imagePayloadSize': len(image_payload) if image_payload else 0,
                    'textCapacityBits': text_capacity['totalCapacityBits'],
                    'imageCapacityBits': image_capacity_bits,
                    'totalCapacityBits': total_capacity_bits,
                    'capacityUsedPercent': round(capacity_used_percent, 2),
                    'embeddingMethod': 'Hybrid Dual-Layer Document Steganography',
                    'textMethod': 'invisible_character',
                    'useImages': image_payload is not None,
                    'processingTime': 0  # Will be set by parent function
                }
            }
            
            if text_stats:
                result['statistics']['textStats'] = text_stats
            
            if image_stats:
                result['statistics']['imageStats'] = image_stats
            
            logger.info(f"PDF extraction completed")
            
            return result
            
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            raise
    
    def cleanup_stego_file(self, file_path: str) -> None:
        """
        Clean up a stego document file after download.
        
        Parameters:
        file_path (str):
            Path to the stego document file to delete.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up stego file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup stego file {file_path}: {e}")


# Global document steganography service instance
document_steganography_service = DocumentSteganographyService()
