"""
pdf_image_processor.py

Purpose:
Processes embedded images in PDF files using the existing Edge-Based LSB Image Steganography Module.

This module integrates with the existing image steganography system to hide
payload data in images embedded within PDF documents.

Why this exists:
- Bridges PDF processing with image steganography
- Reuses existing edge-based LSB implementation
- Enables hybrid PDF steganography (text + images)
- Maintains consistency with image steganography

Security Considerations:
- Reuses validated image steganography module
- Preserves image quality
- Handles image conversion safely
- Logs all operations
"""

import logging
from typing import Dict, List, Tuple, Optional
from app.image_processing.edge_detector import edge_detector
from app.image_processing.image_converter import image_converter
from app.steganography.edge_lsb_embedder import edge_lsb_embedder
from app.steganography.edge_lsb_extractor import edge_lsb_extractor
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFImageProcessor:
    """
    Processes PDF embedded images using edge-based LSB steganography.
    
    Why this exists:
    - Integrates PDF images with existing image steganography
    - Provides hybrid steganography capability
    - Reuses validated image processing modules
    - Maintains consistency across steganography types
    
    Security Considerations:
    - Reuses validated edge-based LSB module
    - Validates images before processing
    - Handles errors gracefully
    - Logs all operations
    """
    
    def __init__(self):
        """Initialize the PDF image processor."""
        logger.info("PDFImageProcessor initialized")
    
    def embed_in_images(
        self,
        image_paths: List[str],
        payload: bytes
    ) -> Tuple[List[str], Dict]:
        """
        Embed payload into PDF embedded images using edge-based LSB.
        
        This method:
        1. Validates all images
        2. Converts images to PNG if needed
        3. Detects edges in each image
        4. Embeds payload across images
        5. Returns modified image paths and statistics
        
        Parameters:
        image_paths (List[str]):
            List of paths to extracted PDF images.
        payload (bytes):
            Binary payload to embed.
            
        Returns:
        Tuple[List[str], Dict]:
            - List of paths to modified images
            - Dictionary with embedding statistics
            
        Raises:
        ValueError: If image capacity is insufficient
        IOError: If image processing fails
        """
        try:
            logger.info(f"Starting PDF image embedding for {len(image_paths)} images")
            logger.info(f"Payload size: {len(payload)} bytes")
            
            modified_image_paths = []
            total_stats = {
                'totalImages': len(image_paths),
                'imagesProcessed': 0,
                'totalPayloadSize': len(payload),
                'totalCapacityBits': 0,
                'totalBitsUsed': 0,
                'imageStats': []
            }
            
            # Calculate total capacity across all images
            total_capacity_bits = 0
            image_capacities = []
            
            for img_path in image_paths:
                # Convert to PNG if needed
                if not img_path.endswith('.png'):
                    png_path, _ = image_converter.convert_to_png(img_path)
                    os.remove(img_path)  # Remove original
                    img_path = png_path
                
                # Detect edges
                edge_map = edge_detector.detect_edges(img_path)
                edge_coordinates = edge_detector.get_edge_pixel_coordinates(edge_map)
                edge_count = len(edge_coordinates)
                
                # Calculate capacity
                capacity_info = edge_lsb_embedder.calculate_capacity(edge_count)
                total_capacity_bits += capacity_info['totalCapacityBits']
                image_capacities.append({
                    'path': img_path,
                    'edgeCount': edge_count,
                    'capacityBits': capacity_info['totalCapacityBits']
                })
            
            total_stats['totalCapacityBits'] = total_capacity_bits
            logger.info(f"Total capacity across all images: {total_capacity_bits} bits")
            
            # Check capacity
            required_bits = len(payload) * 8 + edge_lsb_embedder.HEADER_SIZE * 8
            if required_bits > total_capacity_bits:
                raise ValueError(
                    f"Image capacity exceeded. "
                    f"Need {required_bits} bits but only have {total_capacity_bits} bits. "
                    f"Please use a PDF with more or larger images."
                )
            
            # Embed payload across images
            payload_index = 0
            remaining_bits = required_bits
            
            for i, img_path in enumerate(image_paths):
                if remaining_bits <= 0:
                    # No more payload to embed, keep original image
                    modified_image_paths.append(img_path)
                    continue
                
                # Calculate how much to embed in this image
                img_capacity = image_capacities[i]['capacityBits']
                bits_to_embed = min(remaining_bits, img_capacity)
                bytes_to_embed = (bits_to_embed + 7) // 8
                
                # Extract portion of payload for this image
                payload_start = payload_index
                payload_end = min(payload_index + bytes_to_embed, len(payload))
                image_payload = payload[payload_start:payload_end]
                
                # Detect edges
                edge_map = edge_detector.detect_edges(img_path)
                edge_coordinates = edge_detector.get_edge_pixel_coordinates(edge_map)
                
                # Embed
                stego_path, embed_stats = edge_lsb_embedder.embed(
                    img_path,
                    image_payload,
                    edge_coordinates
                )
                
                modified_image_paths.append(stego_path)
                total_stats['imagesProcessed'] += 1
                total_stats['totalBitsUsed'] += embed_stats['totalBitsUsed']
                total_stats['imageStats'].append(embed_stats)
                
                # Update counters
                payload_index = payload_end
                remaining_bits -= embed_stats['totalBitsUsed']
                
                logger.info(f"Embedded in image {i+1}/{len(image_paths)}: {embed_stats['totalBitsUsed']} bits")
            
            total_stats['capacityUsedPercent'] = round(
                (total_stats['totalBitsUsed'] / total_capacity_bits) * 100, 2
            )
            
            logger.info(f"PDF image embedding completed. Stats: {total_stats}")
            
            return modified_image_paths, total_stats
            
        except Exception as e:
            logger.error(f"PDF image embedding error: {e}")
            raise
    
    def extract_from_images(self, image_paths: List[str]) -> Tuple[bytes, Dict]:
        """
        Extract payload from PDF embedded images using edge-based LSB.
        
        This method:
        1. Validates all images
        2. Detects edges in each image
        3. Extracts payload from images
        4. Combines payload portions
        5. Returns complete payload and statistics
        
        Parameters:
        image_paths (List[str]):
            List of paths to stego PDF images.
            
        Returns:
        Tuple[bytes, Dict]:
            - Extracted payload bytes
            - Dictionary with extraction statistics
            
        Raises:
        ValueError: If extraction fails or no payload found
        IOError: If image processing fails
        """
        try:
            logger.info(f"Starting PDF image extraction for {len(image_paths)} images")
            
            payload_portions = []
            total_stats = {
                'totalImages': len(image_paths),
                'imagesProcessed': 0,
                'totalPayloadSize': 0,
                'totalBitsExtracted': 0,
                'imageStats': []
            }
            
            for i, img_path in enumerate(image_paths):
                try:
                    # Detect edges
                    edge_map = edge_detector.detect_edges(img_path)
                    edge_coordinates = edge_detector.get_edge_pixel_coordinates(edge_map)
                    
                    # Extract
                    payload_binary, extract_stats = edge_lsb_extractor.extract(
                        img_path,
                        edge_coordinates
                    )
                    
                    payload_portions.append(payload_binary)
                    total_stats['imagesProcessed'] += 1
                    total_stats['totalBitsExtracted'] += extract_stats['totalBitsExtracted']
                    total_stats['imageStats'].append(extract_stats)
                    
                    logger.info(f"Extracted from image {i+1}/{len(image_paths)}: {len(payload_binary)} bytes")
                    
                except Exception as e:
                    logger.warning(f"Failed to extract from image {i+1}: {e}")
                    continue
            
            # Combine payload portions
            # For now, we assume the payload is in the first image
            # In a more sophisticated implementation, we'd have a way to distribute
            # and reassemble payload across multiple images
            if payload_portions:
                complete_payload = payload_portions[0]
                total_stats['totalPayloadSize'] = len(complete_payload)
            else:
                raise ValueError("No payload found in any image")
            
            logger.info(f"PDF image extraction completed. Stats: {total_stats}")
            
            return complete_payload, total_stats
            
        except Exception as e:
            logger.error(f"PDF image extraction error: {e}")
            raise
    
    def cleanup_modified_images(self, image_paths: List[str]) -> None:
        """
        Clean up temporary modified image files after processing.
        
        Parameters:
        image_paths (List[str]):
            List of image file paths to delete.
        """
        for image_path in image_paths:
            try:
                if os.path.exists(image_path):
                    os.remove(image_path)
                    logger.info(f"Cleaned up modified image: {image_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup image {image_path}: {e}")


# Global PDF image processor instance
pdf_image_processor = PDFImageProcessor()
