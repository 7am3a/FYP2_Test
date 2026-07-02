"""
txt_handler.py

Purpose:
Handles TXT file processing for steganography operations.

This module is intentionally isolated from steganography embedding
to improve maintainability and debugging.

Why this exists:
- Provides TXT file reading and writing
- Analyzes text capacity for steganography
- Preserves text encoding and formatting
- Enables text-based steganography

Security Considerations:
- Validates text encoding
- Preserves original formatting
- Handles large text files safely
- Prevents encoding attacks
"""

import logging
from typing import Dict, Tuple
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TxtHandler:
    """
    Handles TXT file processing for steganography operations.
    
    Why this exists:
    - Provides centralized TXT processing logic
    - Analyzes text capacity
    - Preserves formatting
    - Supports multiple encodings
    
    Security Considerations:
    - Validates encoding before processing
    - Preserves original formatting
    - Handles large files safely
    - Logs all operations
    """
    
    SUPPORTED_ENCODINGS = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    def __init__(self):
        """Initialize the TXT handler."""
        logger.info("TxtHandler initialized")
    
    def read_txt(self, file_path: str) -> Tuple[str, str]:
        """
        Read content from a TXT file.
        
        This method:
        1. Detects file encoding
        2. Reads text content
        3. Returns content and encoding used
        
        Parameters:
        file_path (str):
            Path to the TXT file.
            
        Returns:
        Tuple[str, str]:
            - Text content
            - Encoding used
            
        Raises:
        ValueError: If file cannot be read with supported encodings
        IOError: If file cannot be accessed
        """
        try:
            logger.info(f"Reading TXT file: {file_path}")
            
            # Try different encodings
            for encoding in self.SUPPORTED_ENCODINGS:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    logger.info(f"TXT read successfully with encoding: {encoding}")
                    logger.info(f"Content length: {len(content)} characters")
                    return content, encoding
                except UnicodeDecodeError:
                    continue
            
            error_msg = f"Unable to decode TXT file with supported encodings: {self.SUPPORTED_ENCODINGS}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        except Exception as e:
            logger.error(f"TXT reading error: {e}")
            raise ValueError(f"Failed to read TXT file: {str(e)}")
    
    def write_txt(self, content: str, output_path: str, encoding: str = 'utf-8') -> None:
        """
        Write content to a TXT file.
        
        Parameters:
        content (str):
            Text content to write.
        output_path (str):
            Path to the output TXT file.
        encoding (str):
            Encoding to use (default: utf-8).
            
        Raises:
        IOError: If file cannot be written
        """
        try:
            logger.info(f"Writing TXT file: {output_path}")
            logger.info(f"Content length: {len(content)} characters")
            logger.info(f"Encoding: {encoding}")
            
            with open(output_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            logger.info("TXT file written successfully")
            
        except Exception as e:
            logger.error(f"TXT writing error: {e}")
            raise IOError(f"Failed to write TXT file: {str(e)}")
    
    def analyze_capacity(self, content: str) -> Dict:
        """
        Analyze the steganography capacity of text content.
        
        This method calculates:
        - Character count
        - Word count
        - Line count
        - Invisible character capacity
        - Structure-based capacity
        
        Parameters:
        content (str):
            Text content to analyze.
            
        Returns:
        Dict: Capacity information including various metrics.
        """
        try:
            logger.info("Analyzing text capacity")
            
            # Basic metrics
            char_count = len(content)
            word_count = len(content.split())
            line_count = len(content.splitlines())
            
            # Invisible character capacity
            # Each invisible character can hide 2 bits (4 different characters)
            # We estimate capacity based on word count (insert between words)
            invisible_char_capacity = word_count * 2  # 2 bits per word position
            invisible_char_capacity_bytes = invisible_char_capacity // 8
            
            # Structure-based capacity
            # We can use line endings, spacing patterns, etc.
            # Estimate based on line count
            structure_capacity = line_count * 4  # 4 bits per line
            structure_capacity_bytes = structure_capacity // 8
            
            # Total capacity
            total_capacity_bits = invisible_char_capacity + structure_capacity
            total_capacity_bytes = total_capacity_bits // 8
            
            result = {
                'charCount': char_count,
                'wordCount': word_count,
                'lineCount': line_count,
                'invisibleCharCapacityBits': invisible_char_capacity,
                'invisibleCharCapacityBytes': invisible_char_capacity_bytes,
                'structureCapacityBits': structure_capacity,
                'structureCapacityBytes': structure_capacity_bytes,
                'totalCapacityBits': total_capacity_bits,
                'totalCapacityBytes': total_capacity_bytes
            }
            
            logger.info(f"Capacity analysis completed: {result}")
            
            return result
            
        except Exception as e:
            logger.error(f"Capacity analysis error: {e}")
            raise ValueError(f"Failed to analyze capacity: {str(e)}")
    
    def get_text_statistics(self, content: str) -> Dict:
        """
        Get detailed statistics about text content.
        
        Parameters:
        content (str):
            Text content to analyze.
            
        Returns:
        Dict: Detailed text statistics.
        """
        try:
            logger.info("Getting text statistics")
            
            stats = {
                'length': len(content),
                'words': len(content.split()),
                'lines': len(content.splitlines()),
                'paragraphs': len([p for p in content.split('\n\n') if p.strip()]),
                'spaces': content.count(' '),
                'tabs': content.count('\t'),
                'newlines': content.count('\n'),
                'alphanumeric': sum(c.isalnum() for c in content),
                'punctuation': sum(not c.isalnum() and not c.isspace() for c in content)
            }
            
            logger.info(f"Text statistics: {stats}")
            
            return stats
            
        except Exception as e:
            logger.error(f"Statistics calculation error: {e}")
            raise ValueError(f"Failed to calculate statistics: {str(e)}")


# Global TXT handler instance
txt_handler = TxtHandler()
