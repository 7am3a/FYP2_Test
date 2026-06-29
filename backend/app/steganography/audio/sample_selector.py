"""
sample_selector.py

Purpose:
Generates deterministic randomized sample positions for audio LSB steganography.

This module is intentionally isolated from embedding, extraction,
and audio processing logic to improve maintainability.

Why Randomized Sample Selection:
- Prevents predictable embedding patterns
- Enhances security against steganalysis
- Ensures same password generates same positions (deterministic)
- Distributes payload across entire audio file
- Minimizes audible distortion by spreading changes

Security Considerations:
- Uses password-derived key for deterministic randomness
- Prevents sequential embedding (easily detected)
- Ensures reliable extraction with same password
- Logs all selection operations for audit trail
"""

import hashlib
import logging
from typing import List
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SampleSelector:
    """
    Generates deterministic randomized sample positions for LSB embedding.
    
    Why this exists:
    - Provides a dedicated interface for sample selection
    - Implements password-derived deterministic randomness
    - Ensures same password always generates same positions
    - Prevents predictable sequential embedding
    - Enhances security against steganalysis
    
    Responsibilities:
    - Generate sample selection sequences from passwords
    - Ensure deterministic behavior (same password = same positions)
    - Distribute samples across audio file
    - Provide selection statistics for debugging
    
    Algorithm:
    - Hash password to generate seed
    - Use deterministic random number generator
    - Generate unique sample positions
    - Ensure positions are within audio bounds
    
    Dependencies:
    - hashlib for password hashing
    - numpy for efficient array operations
    """
    
    def __init__(self):
        """Initialize the sample selector."""
        logger.info("SampleSelector initialized")
    
    def generate_sample_positions(
        self,
        password: str,
        total_samples: int,
        num_positions: int,
        salt: str = ""
    ) -> List[int]:
        """
        Generate deterministic randomized sample positions.
        
        This method:
        1. Hashes the password with salt to create a seed
        2. Uses deterministic random number generator
        3. Generates unique sample positions
        4. Ensures positions are within audio bounds
        5. Returns sorted list of positions
        
        Parameters:
        password (str):
            User password for key derivation.
        total_samples (int):
            Total number of samples in the audio file.
        num_positions (int):
            Number of sample positions to generate.
        salt (str):
            Optional salt for additional security.
            
        Returns:
        List[int]: List of unique sample positions (sorted).
            
        Raises:
        ValueError: If parameters are invalid.
    """
        try:
            logger.info(
                f"Generating sample positions: total_samples={total_samples}, "
                f"num_positions={num_positions}"
            )
            
            # Step 1: Validate parameters
            if num_positions <= 0:
                raise ValueError("Number of positions must be positive")
            
            if total_samples <= 0:
                raise ValueError("Total samples must be positive")
            
            if num_positions > total_samples:
                raise ValueError(
                    f"Cannot select {num_positions} positions from {total_samples} samples"
                )
            
            # Step 2: Generate seed from password
            seed = self._generate_seed(password, salt)
            logger.info("Generated deterministic seed from password")
            
            # Step 3: Generate deterministic random positions
            positions = self._generate_positions_deterministic(
                seed,
                total_samples,
                num_positions
            )
            
            logger.info(f"Generated {len(positions)} unique sample positions")
            
            return positions
            
        except Exception as e:
            logger.error(f"Sample position generation error: {e}")
            raise
    
    def _generate_seed(self, password: str, salt: str) -> int:
        """
        Generate a numeric seed from password and salt.
        
        This method hashes the password and salt to create a
        deterministic seed for the random number generator.
        
        Parameters:
        password (str):
            User password.
        salt (str):
            Optional salt.
            
        Returns:
        int: Numeric seed for random number generator.
        """
        try:
            # Combine password and salt
            combined = password + salt
            
            # Hash using SHA-256
            hash_bytes = hashlib.sha256(combined.encode('utf-8')).digest()
            
            # Convert first 8 bytes to integer (64-bit seed)
            seed = int.from_bytes(hash_bytes[:8], byteorder='big') % (2**32)  # Limit to 32-bit for numpy
            
            return seed
            
        except Exception as e:
            logger.error(f"Seed generation error: {e}")
            raise ValueError(f"Failed to generate seed: {str(e)}")
    
    def _generate_positions_deterministic(
        self,
        seed: int,
        total_samples: int,
        num_positions: int
    ) -> List[int]:
        """
        Generate unique sample positions using deterministic randomness.
        
        This method uses a custom deterministic random number generator
        to ensure the same seed always produces the same sequence.
        
        Parameters:
        seed (int):
            Seed for random number generator.
        total_samples (int):
            Total number of samples available.
        num_positions (int):
            Number of positions to generate.
            
        Returns:
        List[int]: List of unique sample positions (sorted).
    """
        try:
            # Use numpy's random with fixed seed for determinism
            np.random.seed(seed)
            
            # Generate one deterministic permutation
            all_positions = np.arange(total_samples)

            np.random.shuffle(all_positions)

            # Keep the permutation order.
            # Do NOT sort.
            positions = all_positions[:num_positions].tolist()
            
            logger.info(
                f"Deterministic positions generated: "
                f"range=[{positions[0]}, {positions[-1]}]"
            )
            
            return positions
            
        except Exception as e:
            logger.error(f"Deterministic position generation error: {e}")
            raise ValueError(f"Failed to generate positions: {str(e)}")
    
    def generate_bit_positions(
        self,
        password: str,
        total_samples: int,
        num_bits: int,
        samples_per_bit: int = 1,
        salt: str = ""
    ) -> List[int]:
        """
        Generate sample positions for embedding a specific number of bits.
        
        This is a convenience method that calculates the number of
        sample positions needed based on bits to embed.
        
        Parameters:
        password (str):
            User password for key derivation.
        total_samples (int):
            Total number of samples in the audio file.
        num_bits (int):
            Number of bits to embed.
        samples_per_bit (int):
            Number of samples per bit (default: 1).
        salt (str):
            Optional salt for additional security.
            
        Returns:
        List[int]: List of unique sample positions (sorted).
    """
        try:
            # Calculate number of positions needed
            num_positions = num_bits * samples_per_bit
            
            # Generate positions
            positions = self.generate_sample_positions(
                password=password,
                total_samples=total_samples,
                num_positions=num_positions,
                salt=salt
            )
            
            return positions
            
        except Exception as e:
            logger.error(f"Bit position generation error: {e}")
            raise
    
    def validate_positions(
        self,
        positions: List[int],
        total_samples: int
    ) -> bool:
        """
        Validate that sample positions are within bounds.
        
        Parameters:
        positions (List[int]):
            List of sample positions.
        total_samples (int):
            Total number of samples.
            
        Returns:
        bool: True if positions are valid, False otherwise.
        """
        try:
            # Check positions are within bounds
            for pos in positions:
                if pos < 0 or pos >= total_samples:
                    logger.error(f"Invalid position: {pos} (total: {total_samples})")
                    return False
            
            # Check for duplicates
            if len(positions) != len(set(positions)):
                logger.error("Duplicate positions found")
                return False
            
            logger.info("Position validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Position validation error: {e}")
            return False


# Global sample selector instance
sample_selector = SampleSelector()
