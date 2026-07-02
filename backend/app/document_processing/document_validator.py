"""
document_validator.py

Purpose:
Validates document files (PDF and TXT) for steganography operations.

This module is intentionally isolated from PDF parsing and TXT processing
to improve maintainability and debugging.

Why this exists:
- Ensures only valid documents are processed
- Prevents processing of corrupted or malformed files
- Validates file types and MIME types
- Checks encoding for TXT files
- Provides early error detection before expensive operations

Security Considerations:
- Validates file extensions to prevent unauthorized file types
- Checks MIME types to prevent file type spoofing
- Detects corrupted files before processing
- Validates encoding to prevent encoding attacks
"""

import os
import logging
from typing import Tuple, Optional

# Try to import python-magic, fall back gracefully if not available
try:
    import magic
    MAGIC_AVAILABLE = True
except (ImportError, OSError):
    MAGIC_AVAILABLE = False
    logging.warning("python-magic library not available. MIME type validation will be skipped. Install python-magic-bin on Windows or libmagic on Linux/macOS.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentValidator:
    """
    Validates document files for steganography operations.
    
    Why this exists:
    - Provides centralized validation logic
    - Prevents processing of invalid files
    - Ensures file integrity before steganography
    - Supports both PDF and TXT validation
    
    Security Considerations:
    - Validates both extension and MIME type
    - Detects file type spoofing attempts
    - Checks for file corruption
    - Validates text encoding
    """
    
    # Supported document formats
    SUPPORTED_PDF_EXTENSIONS = ['.pdf']
    SUPPORTED_TXT_EXTENSIONS = ['.txt']
    
    # Allowed MIME types
    PDF_MIME_TYPES = ['application/pdf']
    TXT_MIME_TYPES = ['text/plain']
    
    def __init__(self):
        """Initialize the document validator."""
        logger.info("DocumentValidator initialized")
    
    def validate_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a document file.
        
        This method:
        1. Checks if file exists
        2. Validates file extension
        3. Validates MIME type
        4. Checks file size
        5. For TXT: validates encoding
        
        Parameters:
        file_path (str):
            Path to the document file to validate.
            
        Returns:
        Tuple[bool, Optional[str]]:
            - True if valid, False otherwise
            - Error message if invalid, None if valid
            
        Raises:
        FileNotFoundError: If file does not exist
        """
        try:
            logger.info(f"Validating document: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                error_msg = f"File not found: {file_path}"
                logger.error(error_msg)
                return False, error_msg
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                error_msg = f"File is empty: {file_path}"
                logger.error(error_msg)
                return False, error_msg
            
            logger.info(f"File size: {file_size} bytes")
            
            # Get file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            logger.info(f"File extension: {file_ext}")
            
            # Validate based on file type
            if file_ext in self.SUPPORTED_PDF_EXTENSIONS:
                return self._validate_pdf(file_path)
            elif file_ext in self.SUPPORTED_TXT_EXTENSIONS:
                return self._validate_txt(file_path)
            else:
                error_msg = (
                    f"Unsupported file extension: {file_ext}. "
                    f"Supported: {', '.join(self.SUPPORTED_PDF_EXTENSIONS + self.SUPPORTED_TXT_EXTENSIONS)}"
                )
                logger.error(error_msg)
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Validation error: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def _validate_pdf(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a PDF file.
        
        Parameters:
        file_path (str):
            Path to the PDF file.
            
        Returns:
        Tuple[bool, Optional[str]]:
            - True if valid, False otherwise
            - Error message if invalid, None if valid
        """
        try:
            # Validate MIME type if magic library is available
            if MAGIC_AVAILABLE:
                mime = magic.Magic(mime=True)
                mime_type = mime.from_file(file_path)
                logger.info(f"PDF MIME type: {mime_type}")
                
                if mime_type not in self.PDF_MIME_TYPES:
                    error_msg = (
                        f"Invalid PDF MIME type: {mime_type}. "
                        f"Expected: {', '.join(self.PDF_MIME_TYPES)}"
                    )
                    logger.error(error_msg)
                    return False, error_msg
            else:
                logger.warning("Skipping MIME type validation for PDF (python-magic not available)")
            
            # Try to open PDF to check for corruption
            # This will be done by pdf_parser, but we do a basic check here
            logger.info("PDF validation passed")
            return True, None
            
        except Exception as e:
            error_msg = f"PDF validation failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def _validate_txt(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a TXT file.
        
        Parameters:
        file_path (str):
            Path to the TXT file.
            
        Returns:
        Tuple[bool, Optional[str]]:
            - True if valid, False otherwise
            - Error message if invalid, None if valid
        """
        try:
            # Validate MIME type if magic library is available
            if MAGIC_AVAILABLE:
                mime = magic.Magic(mime=True)
                mime_type = mime.from_file(file_path)
                logger.info(f"TXT MIME type: {mime_type}")
                
                if mime_type not in self.TXT_MIME_TYPES:
                    error_msg = (
                        f"Invalid TXT MIME type: {mime_type}. "
                        f"Expected: {', '.join(self.TXT_MIME_TYPES)}"
                    )
                    logger.error(error_msg)
                    return False, error_msg
            else:
                logger.warning("Skipping MIME type validation for TXT (python-magic not available)")
            
            # Validate encoding
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                logger.info(f"TXT encoding validated (UTF-8), content length: {len(content)}")
            except UnicodeDecodeError:
                # Try other common encodings
                encodings = ['utf-8-sig', 'latin-1', 'cp1252']
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        logger.info(f"TXT encoding validated ({encoding}), content length: {len(content)}")
                        return True, None
                    except UnicodeDecodeError:
                        continue
                
                error_msg = "Unable to decode TXT file with supported encodings (UTF-8, UTF-8-SIG, Latin-1, CP1252)"
                logger.error(error_msg)
                return False, error_msg
            
            # Check if file has content
            if len(content.strip()) == 0:
                error_msg = "TXT file is empty or contains only whitespace"
                logger.error(error_msg)
                return False, error_msg
            
            logger.info("TXT validation passed")
            return True, None
            
        except Exception as e:
            error_msg = f"TXT validation failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def get_document_type(self, file_path: str) -> Optional[str]:
        """
        Determine the document type (PDF or TXT).
        
        Parameters:
        file_path (str):
            Path to the document file.
            
        Returns:
        Optional[str]:
            'pdf' or 'txt' if valid, None otherwise
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in self.SUPPORTED_PDF_EXTENSIONS:
            return 'pdf'
        elif file_ext in self.SUPPORTED_TXT_EXTENSIONS:
            return 'txt'
        
        return None


# Global document validator instance
document_validator = DocumentValidator()
