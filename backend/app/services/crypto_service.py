"""
Crypto Service for SecureStego
Implements Argon2id key derivation and AES-256-GCM encryption
"""

import os
import base64
import secrets
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Dict
from app.config import settings
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class CryptoService:
    """
    Service for password-based encryption using Argon2id and AES-256-GCM.
    
    Security Features:
    - Argon2id for key derivation (memory-hard, resistant to GPU/ASIC attacks)
    - AES-256-GCM for authenticated encryption
    - Random salt and IV generation for each operation
    - Recommended Argon2id parameters (OWASP guidelines)
    - Parameters loaded from configuration
    """
    
    # AES-256-GCM parameters
    AES_KEY_SIZE = 32         # 256 bits
    AES_IV_SIZE = 12          # 96 bits (recommended for GCM)
    
    def __init__(self):
        """Initialize the crypto service with Argon2id hasher."""
        # Load Argon2id parameters from settings
        self.argon2_time_cost = settings.argon2_time_cost
        self.argon2_memory_cost = settings.argon2_memory_cost
        self.argon2_parallelism = settings.argon2_parallelism
        self.argon2_hash_len = settings.argon2_hash_len
        self.argon2_salt_len = settings.argon2_salt_len
        
        self.ph = PasswordHasher(
            time_cost=self.argon2_time_cost,
            memory_cost=self.argon2_memory_cost,
            parallelism=self.argon2_parallelism,
            hash_len=self.argon2_hash_len,
            salt_len=self.argon2_salt_len,
            type=Type.ID  # Argon2id
        )
        logger.info(
            f"CryptoService initialized with Argon2id: "
            f"time_cost={self.argon2_time_cost}, "
            f"memory_cost={self.argon2_memory_cost} KiB, "
            f"parallelism={self.argon2_parallelism}"
        )
    
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive a 256-bit encryption key from password using Argon2id.
        
        Args:
            password: User password
            salt: Random salt bytes
            
        Returns:
            32-byte derived key for AES-256
        """
        # Argon2id automatically handles the salt internally
        # We need to use the raw hash output
        # Since PasswordHasher is designed for password hashing, we'll use a different approach
        
        # Use argon2-cffi directly for key derivation
        from argon2.low_level import hash_secret_raw, Type
        
        # Derive key using Argon2id
        key = hash_secret_raw(
            secret=password.encode('utf-8'),
            salt=salt,
            time_cost=self.argon2_time_cost,
            memory_cost=self.argon2_memory_cost,
            parallelism=self.argon2_parallelism,
            hash_len=self.AES_KEY_SIZE,
            type=Type.ID
        )
        
        return key
    
    def encrypt_message(self, message: str, password: str) -> Dict[str, str]:
        """
        Encrypt a message using Argon2id key derivation and AES-256-GCM.
        
        Args:
            message: Plaintext message to encrypt
            password: User password for key derivation
            
        Returns:
            Dictionary containing:
            - ciphertext: Base64 encoded encrypted data
            - salt: Base64 encoded salt
            - iv: Base64 encoded IV
            - algorithm: Encryption algorithm used
            - kdf: Key derivation function used
        """
        try:
            logger.info("Starting encryption process")
            
            # Generate random salt and IV
            salt = secrets.token_bytes(self.argon2_salt_len)
            iv = secrets.token_bytes(self.AES_IV_SIZE)
            
            # Derive encryption key using Argon2id
            key = self.derive_key(password, salt)
            
            # Encrypt message using AES-256-GCM
            aesgcm = AESGCM(key)
            plaintext = message.encode('utf-8')
            ciphertext = aesgcm.encrypt(iv, plaintext, None)
            
            # Encode to base64 for transmission
            result = {
                "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
                "salt": base64.b64encode(salt).decode('utf-8'),
                "iv": base64.b64encode(iv).decode('utf-8'),
                "algorithm": "AES-256-GCM",
                "kdf": "Argon2id"
            }
            
            logger.info("Encryption completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt_message(self, ciphertext: str, password: str, salt: str, iv: str) -> str:
        """
        Decrypt a message using Argon2id key derivation and AES-256-GCM.
        
        Args:
            ciphertext: Base64 encoded ciphertext
            password: User password for key derivation
            salt: Base64 encoded salt
            iv: Base64 encoded IV
            
        Returns:
            Decrypted plaintext message
            
        Raises:
            ValueError: If decryption fails (wrong password or corrupted data)
        """
        try:
            logger.info("Starting decryption process")
            
            # Decode from base64
            ciphertext_bytes = base64.b64decode(ciphertext)
            salt_bytes = base64.b64decode(salt)
            iv_bytes = base64.b64decode(iv)
            
            # Derive encryption key using Argon2id
            key = self.derive_key(password, salt_bytes)
            
            # Decrypt using AES-256-GCM
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(iv_bytes, ciphertext_bytes, None)
            
            # Decode to string
            message = plaintext.decode('utf-8')
            
            logger.info("Decryption completed successfully")
            return message
            
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise ValueError("Decryption failed. Check your password and try again.")
    
    def generate_salt(self) -> str:
        """
        Generate a random salt for key derivation.
        
        Returns:
            Base64 encoded salt
        """
        salt = secrets.token_bytes(self.argon2_salt_len)
        return base64.b64encode(salt).decode('utf-8')
    
    def generate_iv(self) -> str:
        """
        Generate a random IV for AES-GCM.
        
        Returns:
            Base64 encoded IV
        """
        iv = secrets.token_bytes(self.AES_IV_SIZE)
        return base64.b64encode(iv).decode('utf-8')


# Global crypto service instance
crypto_service = CryptoService()
