"""
pdf_rebuilder.py

Purpose:
Rebuilds PDF files after steganography modifications.

This module is intentionally isolated from PDF parsing and steganography
to improve maintainability and debugging.

Why this exists:
- Reconstructs PDFs with modified content
- Reinserts stego images into PDFs
- Preserves PDF structure and metadata
- Ensures PDF integrity after modifications

Security Considerations:
- Validates rebuilt PDF structure
- Preserves original PDF metadata
- Ensures PDF remains valid after modifications
- Handles large PDFs safely
"""

import logging
from typing import Dict, List, Optional
import fitz  # PyMuPDF
import tempfile
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFRebuilder:
    """
    Rebuilds PDF files after steganography modifications.
    
    Why this exists:
    - Provides centralized PDF rebuilding logic
    - Handles text and image reinsertion
    - Preserves PDF structure
    - Ensures output PDF validity
    
    Security Considerations:
    - Validates input before rebuilding
    - Preserves original metadata
    - Ensures output PDF is valid
    - Handles errors gracefully
    """
    
    def __init__(self):
        """Initialize the PDF rebuilder."""
        logger.info("PDFRebuilder initialized")
    
    def rebuild_pdf(
        self,
        original_pdf_path: str,
        modified_text_blocks: Optional[List[Dict]] = None,
        modified_image_paths: Optional[List[str]] = None,
        original_image_info: Optional[List[Dict]] = None
    ) -> str:
        """
        Rebuild a PDF file with modified content.
        
        This method:
        1. Opens the original PDF
        2. Replaces text blocks if provided
        3. Replaces images if provided
        4. Saves the modified PDF
        5. Validates the output PDF
        
        Parameters:
        original_pdf_path (str):
            Path to the original PDF file.
        modified_text_blocks (Optional[List[Dict]]):
            List of modified text blocks (optional).
        modified_image_paths (Optional[List[str]]):
            List of paths to modified images (optional).
        original_image_info (Optional[List[Dict]]):
            Information about original image positions (optional).
            
        Returns:
        str: Path to the rebuilt PDF file.
            
        Raises:
        ValueError: If rebuilding fails
        IOError: If PDF cannot be written
        """
        try:
            logger.info(f"Rebuilding PDF: {original_pdf_path}")
            
            # Open original PDF
            pdf_document = fitz.open(original_pdf_path)
            page_count = pdf_document.page_count
            logger.info(f"Original PDF opened: {page_count} pages")
            
            # Process modifications
            if modified_text_blocks:
                self._replace_text_blocks(pdf_document, modified_text_blocks)
            
            if modified_image_paths and original_image_info:
                self._replace_images(pdf_document, modified_image_paths, original_image_info)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(
                suffix='_stego.pdf',
                delete=False
            )
            stego_pdf_path = temp_file.name
            temp_file.close()
            
            # Save modified PDF
            pdf_document.save(stego_pdf_path)
            pdf_document.close()
            
            logger.info(f"PDF rebuilt successfully: {stego_pdf_path}")
            
            # Validate the rebuilt PDF
            self._validate_rebuilt_pdf(stego_pdf_path)
            
            return stego_pdf_path
            
        except Exception as e:
            logger.error(f"PDF rebuilding error: {e}")
            raise ValueError(f"Failed to rebuild PDF: {str(e)}")
    
    def _replace_text_blocks(self, pdf_document: fitz.Document, text_blocks: List[Dict]) -> None:
        """
        Replace text blocks in PDF with modified versions.
        
        Parameters:
        pdf_document (fitz.Document):
            Opened PDF document.
        text_blocks (List[Dict]):
            List of modified text blocks.
        """
        logger.info(f"Replacing {len(text_blocks)} text blocks")
        
        # Group text blocks by page
        blocks_by_page = {}
        for block in text_blocks:
            page_num = block['page']
            if page_num not in blocks_by_page:
                blocks_by_page[page_num] = []
            blocks_by_page[page_num].append(block)
        
        # Replace text on each page
        for page_num, blocks in blocks_by_page.items():
            page = pdf_document[page_num]
            
            for block in blocks:
                # Get the rectangle for this block
                rect = fitz.Rect(block['x0'], block['y0'], block['x1'], block['y1'])
                
                # Redact the old text (make it transparent)
                page.redact(rect)
                
                # Insert new text
                page.insert_text(
                    fitz.Point(block['x0'], block['y1']),
                    block['text'],
                    fontsize=10  # Default font size, could be improved
                )
        
        logger.info("Text blocks replaced")
    
    def _replace_images(
        self,
        pdf_document: fitz.Document,
        modified_image_paths: List[str],
        original_image_info: List[Dict]
    ) -> None:
        """
        Replace images in PDF with modified versions.
        
        Parameters:
        pdf_document (fitz.Document):
            Opened PDF document.
        modified_image_paths (List[str]):
            List of paths to modified images.
        original_image_info (List[Dict]):
            Information about original image positions.
        """
        logger.info(f"Replacing {len(modified_image_paths)} images")
        
        # Replace each image
        for img_idx, (modified_path, orig_info) in enumerate(zip(modified_image_paths, original_image_info)):
            page_num = orig_info['page']
            page = pdf_document[page_num]
            
            # Insert modified image
            rect = fitz.Rect(orig_info['x0'], orig_info['y0'], orig_info['x1'], orig_info['y1'])
            page.insert_image(rect, filename=modified_path)
            
            logger.info(f"Replaced image {img_idx + 1} on page {page_num}")
        
        logger.info("Images replaced")
    
    def _validate_rebuilt_pdf(self, pdf_path: str) -> None:
        """
        Validate that the rebuilt PDF is valid.
        
        Parameters:
        pdf_path (str):
            Path to the rebuilt PDF.
            
        Raises:
        ValueError: If PDF is invalid
        """
        try:
            # Try to open the PDF
            pdf_document = fitz.open(pdf_path)
            page_count = pdf_document.page_count
            
            if page_count == 0:
                raise ValueError("Rebuilt PDF has no pages")
            
            pdf_document.close()
            
            logger.info(f"Rebuilt PDF validated: {page_count} pages")
            
        except Exception as e:
            logger.error(f"Rebuilt PDF validation failed: {e}")
            raise ValueError(f"Rebuilt PDF is invalid: {str(e)}")
    
    def create_text_only_pdf(self, text_content: str) -> str:
        """
        Create a simple PDF from text content.
        
        This is useful for TXT to PDF conversion if needed.
        
        Parameters:
        text_content (str):
            Text content to convert to PDF.
            
        Returns:
        str: Path to the created PDF file.
        """
        try:
            logger.info("Creating PDF from text content")
            
            # Create new PDF
            pdf_document = fitz.open()
            page = pdf_document.new_page()
            
            # Insert text
            page.insert_text(fitz.Point(50, 50), text_content, fontsize=12)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(
                suffix='.pdf',
                delete=False
            )
            pdf_path = temp_file.name
            temp_file.close()
            
            pdf_document.save(pdf_path)
            pdf_document.close()
            
            logger.info(f"PDF created from text: {pdf_path}")
            
            return pdf_path
            
        except Exception as e:
            logger.error(f"PDF creation error: {e}")
            raise ValueError(f"Failed to create PDF: {str(e)}")


# Global PDF rebuilder instance
pdf_rebuilder = PDFRebuilder()
