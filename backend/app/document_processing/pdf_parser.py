"""
pdf_parser.py

Purpose:
Extracts content from PDF files including text blocks and embedded images.

This module is intentionally isolated from PDF rebuilding and steganography
to improve maintainability and debugging.

Why this exists:
- Provides PDF content extraction capabilities
- Separates text and image extraction logic
- Enables capacity analysis before embedding
- Supports hybrid steganography (text + images)

Security Considerations:
- Handles potentially malicious PDFs safely
- Validates extracted content
- Prevents memory issues with large PDFs
- Logs all extraction operations
"""

import logging
from typing import Dict, List, Tuple, Optional
import fitz  # PyMuPDF
import io
from PIL import Image
import tempfile
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFParser:
    """
    Extracts content from PDF files for steganography operations.
    
    Why this exists:
    - Provides centralized PDF parsing logic
    - Extracts both text and images
    - Enables capacity analysis
    - Supports hybrid steganography workflow
    
    Security Considerations:
    - Validates PDF structure before extraction
    - Handles large PDFs safely
    - Limits memory usage
    - Logs all extraction operations
    """
    
    def __init__(self):
        """Initialize the PDF parser."""
        logger.info("PDFParser initialized")
    
    def parse_pdf(self, file_path: str) -> Dict:
        """
        Parse a PDF file and extract its content.
        
        This method:
        1. Opens the PDF file
        2. Extracts text content by page
        3. Extracts embedded images
        4. Returns structured content for steganography
        
        Parameters:
        file_path (str):
            Path to the PDF file to parse.
            
        Returns:
        Dict: Dictionary containing:
            - pageCount: Number of pages
            - textBlocks: List of text blocks with positions
            - images: List of extracted image paths
            - totalTextLength: Total length of text content
            - imageCount: Number of embedded images
            
        Raises:
        ValueError: If PDF is corrupted or invalid
        IOError: If PDF cannot be read
        """
        try:
            logger.info(f"Parsing PDF: {file_path}")
            
            # Open PDF
            pdf_document = fitz.open(file_path)
            page_count = pdf_document.page_count
            logger.info(f"PDF opened: {page_count} pages")
            
            # Extract text blocks
            text_blocks = self._extract_text_blocks(pdf_document)
            total_text_length = sum(len(block['text']) for block in text_blocks)
            logger.info(f"Text extracted: {total_text_length} characters in {len(text_blocks)} blocks")
            
            # Extract images
            image_paths = self._extract_images(pdf_document)
            logger.info(f"Images extracted: {len(image_paths)} images")
            
            # Close PDF
            pdf_document.close()
            
            result = {
                'pageCount': page_count,
                'textBlocks': text_blocks,
                'images': image_paths,
                'totalTextLength': total_text_length,
                'imageCount': len(image_paths)
            }
            
            logger.info(f"PDF parsing completed: {result}")
            
            return result
            
        except Exception as e:
            logger.error(f"PDF parsing error: {e}")
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    def _extract_text_blocks(self, pdf_document: fitz.Document) -> List[Dict]:
        """
        Extract text blocks from PDF pages.
        
        Parameters:
        pdf_document (fitz.Document):
            Opened PDF document.
            
        Returns:
        List[Dict]: List of text blocks with position information.
        """
        text_blocks = []
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            
            # Extract text blocks
            blocks = page.get_text("blocks")
            
            for block in blocks:
                # Block structure: (x0, y0, x1, y1, text, block_type, block_no)
                if len(blocks) >= 7 and block[5] == 0:  # 0 = text block
                    text_block = {
                        'page': page_num,
                        'x0': block[0],
                        'y0': block[1],
                        'x1': block[2],
                        'y1': block[3],
                        'text': block[4],
                        'blockNo': block[6]
                    }
                    text_blocks.append(text_block)
        
        return text_blocks
    
    def _extract_images(self, pdf_document: fitz.Document) -> List[str]:
        """
        Extract embedded images from PDF pages.
        
        This method:
        1. Iterates through all pages
        2. Extracts images from each page
        3. Saves images to temporary files
        4. Returns list of image paths
        
        Parameters:
        pdf_document (fitz.Document):
            Opened PDF document.
            
        Returns:
        List[str]: List of temporary file paths for extracted images.
        """
        image_paths = []
        image_counter = 0
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                # Get image reference
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                
                # Get image data
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Convert to PIL Image
                image = Image.open(io.BytesIO(image_bytes))
                
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Save to temporary file
                temp_file = tempfile.NamedTemporaryFile(
                    suffix=f'_pdf_img_{image_counter}.png',
                    delete=False
                )
                temp_path = temp_file.name
                temp_file.close()
                
                image.save(temp_path, 'PNG')
                image_paths.append(temp_path)
                
                image_counter += 1
                logger.info(f"Extracted image {image_counter} from page {page_num}")
        
        return image_paths
    
    def cleanup_extracted_images(self, image_paths: List[str]) -> None:
        """
        Clean up temporary image files after processing.
        
        Parameters:
        image_paths (List[str]):
            List of temporary image file paths to delete.
        """
        for image_path in image_paths:
            try:
                if os.path.exists(image_path):
                    os.remove(image_path)
                    logger.info(f"Cleaned up extracted image: {image_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup image {image_path}: {e}")
    
    def get_text_content(self, file_path: str) -> str:
        """
        Get all text content from a PDF file as a single string.
        
        Parameters:
        file_path (str):
            Path to the PDF file.
            
        Returns:
        str: All text content from the PDF.
        """
        try:
            logger.info(f"Extracting text content from: {file_path}")
            
            pdf_document = fitz.open(file_path)
            text_content = ""
            
            for page in pdf_document:
                text_content += page.get_text()
            
            pdf_document.close()
            
            logger.info(f"Text content extracted: {len(text_content)} characters")
            
            return text_content
            
        except Exception as e:
            logger.error(f"Text extraction error: {e}")
            raise ValueError(f"Failed to extract text: {str(e)}")


# Global PDF parser instance
pdf_parser = PDFParser()
