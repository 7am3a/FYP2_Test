"""
Payload Validator for SecureStego

Validates payload data for steganography operations.
"""

from typing import Tuple
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class PayloadValidator:
    """
    Validates payload data for steganography operations.
    
    Why this exists:
    - Centralizes payload validation logic
    - Ensures payload size limits are enforced
    - Validates payload structure before embedding
    """
    
    MAX_PAYLOAD_SIZE = 1000000  # 1MB
    
    @classmethod
    def validate_payload_size(cls, payload_size: int) -> Tuple[bool, str]:
        """
        Validate payload size.
        
        Parameters:
        payload_size (int): Size of the payload in bytes.
        
        Returns:
        Tuple[bool, str]: (is_valid, error_message)
        """
        if payload_size > cls.MAX_PAYLOAD_SIZE:
            return False, f"Payload size exceeds limit of {cls.MAX_PAYLOAD_SIZE} bytes"
        
        return True, ""
