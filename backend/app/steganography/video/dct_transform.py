"""
DCT Transform Module for SecureStego

Purpose:
Performs Discrete Cosine Transform (DCT) and inverse DCT on image blocks
for frequency-domain steganography.

This module is isolated from frame selection, payload embedding, and video processing
to improve maintainability and debugging.

DCT Theory:
- DCT converts spatial domain to frequency domain
- Low frequencies represent overall image structure
- High frequencies represent fine details
- Mid frequencies are ideal for embedding (less visible, more robust)

Transform Workflow:
1. Convert frame to YCbCr color space
2. Extract luminance (Y) channel
3. Split into 8x8 blocks
4. Apply 2D DCT to each block
5. Modify selected coefficients
6. Apply inverse 2D DCT
7. Reconstruct luminance channel
8. Convert back to RGB

Why This Exists:
- Provides frequency-domain transformation
- Enables robust embedding in mid-frequency coefficients
- Improves imperceptibility compared to spatial methods
- Standard approach in JPEG and video compression

Security Considerations:
- Uses standard DCT algorithm (no custom implementations)
- Does not introduce artifacts that could reveal steganography
- Preserves image quality within acceptable limits
- Deterministic transformation for reproducible extraction
"""

import numpy as np
import cv2
import logging
from typing import Tuple, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DCTTransform:
    """
    Performs DCT and inverse DCT transformations on image blocks.
    
    Why this exists:
    - Converts spatial data to frequency domain
    - Enables embedding in mid-frequency coefficients
    - Improves robustness and imperceptibility
    - Standard approach in steganography
    
    Security Considerations:
    - Uses OpenCV's DCT implementation (trusted library)
    - Deterministic transformation
    - Does not introduce detectable artifacts
    - Preserves image quality
    """
    
    # Block size for DCT (standard JPEG block size)
    BLOCK_SIZE = 8
    
    # DCT coefficient positions to avoid
    # DC coefficient (0,0) - avoid modifying
    # Very high frequencies - avoid for robustness
    
    def __init__(self):
        """Initialize the DCT transform."""
        logger.info("DCTTransform initialized")
    
    def apply_dct(self, block: np.ndarray) -> np.ndarray:
        """
        Apply 2D DCT to an 8x8 block.
        
        This method:
        1. Converts block to float32
        2. Applies 2D DCT using OpenCV
        3. Returns frequency-domain coefficients
        
        Parameters:
        block (np.ndarray):
            8x8 pixel block (spatial domain).
            
        Returns:
        np.ndarray:
            8x8 DCT coefficients (frequency domain).
        """
        try:
            # Convert to float32 for DCT
            block_float = np.float32(block)
            
            # Apply 2D DCT
            dct_block = cv2.dct(block_float)
            
            return dct_block
            
        except Exception as e:
            logger.error(f"DCT application error: {e}")
            raise
    
    def apply_inverse_dct(self, dct_block: np.ndarray) -> np.ndarray:
        """
        Apply inverse 2D DCT to reconstruct spatial block.
        
        This method:
        1. Takes frequency-domain coefficients
        2. Applies inverse 2D DCT
        3. Returns spatial-domain block
        
        Parameters:
        dct_block (np.ndarray):
            8x8 DCT coefficients (frequency domain).
            
        Returns:
        np.ndarray:
            8x8 pixel block (spatial domain).
        """
        try:
            # Apply inverse 2D DCT
            reconstructed_block = cv2.idct(dct_block)
            
            # Clip values to valid range [0, 255]
            reconstructed_block = np.clip(reconstructed_block, 0, 255)
            
            # Convert back to uint8
            reconstructed_block = np.uint8(reconstructed_block)
            
            return reconstructed_block
            
        except Exception as e:
            logger.error(f"Inverse DCT application error: {e}")
            raise
    
    def frame_to_ycbcr(self, frame: np.ndarray) -> np.ndarray:
        """
        Convert RGB frame to YCbCr color space.
        
        This method:
        1. Takes RGB frame
        2. Converts to YCbCr
        3. Returns YCbCr frame
        
        Parameters:
        frame (np.ndarray):
            RGB frame (H x W x 3).
            
        Returns:
        np.ndarray:
            YCbCr frame (H x W x 3).
        """
        try:
            # OpenCV reads images as BGR
            ycbcr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
            return ycbcr_frame
            
        except Exception as e:
            logger.error(f"RGB to YCbCr conversion error: {e}")
            raise
    
    def ycbcr_to_frame(self, ycbcr_frame: np.ndarray) -> np.ndarray:
        """
        Convert YCbCr frame back to RGB color space.
        
        Parameters:
        ycbcr_frame (np.ndarray):
            YCbCr frame (H x W x 3).
            
        Returns:
        np.ndarray:
            RGB frame (H x W x 3).
        """
        try:
            # Convert back to OpenCV's BGR format
            bgr_frame = cv2.cvtColor(ycbcr_frame, cv2.COLOR_YCrCb2BGR)
            return bgr_frame
            
        except Exception as e:
            logger.error(f"YCbCr to RGB conversion error: {e}")
            raise
    
    def extract_luminance(self, ycbcr_frame: np.ndarray) -> np.ndarray:
        """
        Extract luminance (Y) channel from YCbCr frame.
        
        Parameters:
        ycbcr_frame (np.ndarray):
            YCbCr frame (H x W x 3).
            
        Returns:
        np.ndarray:
            Luminance channel (H x W).
        """
        try:
            # Y channel is at index 0 in OpenCV YCrCb
            luminance = ycbcr_frame[:, :, 0]
            return luminance
            
        except Exception as e:
            logger.error(f"Luminance extraction error: {e}")
            raise
    
    def set_luminance(self, ycbcr_frame: np.ndarray, luminance: np.ndarray) -> np.ndarray:
        """
        Set luminance (Y) channel in YCbCr frame.
        
        Parameters:
        ycbcr_frame (np.ndarray):
            Original YCbCr frame (H x W x 3).
        luminance (np.ndarray):
            New luminance channel (H x W).
            
        Returns:
        np.ndarray:
            YCbCr frame with updated luminance (H x W x 3).
        """
        try:
            # Create copy to avoid modifying original
            updated_frame = ycbcr_frame.copy()
            
            # Set Y channel
            updated_frame[:, :, 0] = luminance
            
            return updated_frame
            
        except Exception as e:
            logger.error(f"Luminance setting error: {e}")
            raise
    
    def split_into_blocks(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Split an image into 8x8 blocks.
        
        This method:
        1. Pads image if dimensions not divisible by 8
        2. Splits into 8x8 blocks
        3. Returns list of blocks
        
        Parameters:
        image (np.ndarray):
            Image to split (H x W).
            
        Returns:
        List[np.ndarray]:
            List of 8x8 blocks.
        """
        try:
            height, width = image.shape
            
            # Pad image if necessary
            pad_height = (8 - height % 8) % 8
            pad_width = (8 - width % 8) % 8
            
            if pad_height > 0 or pad_width > 0:
                image = np.pad(image, ((0, pad_height), (0, pad_width)), mode='constant')
            
            # Split into blocks
            blocks = []
            for y in range(0, image.shape[0], 8):
                for x in range(0, image.shape[1], 8):
                    block = image[y:y+8, x:x+8]
                    blocks.append(block)
            
            return blocks
            
        except Exception as e:
            logger.error(f"Block splitting error: {e}")
            raise
    
    def reconstruct_from_blocks(self, blocks: List[np.ndarray], original_shape: Tuple[int, int]) -> np.ndarray:
        """
        Reconstruct an image from 8x8 blocks.
        
        This method:
        1. Takes list of 8x8 blocks
        2. Reassembles them into image
        3. Crops to original shape if padded
        
        Parameters:
        blocks (List[np.ndarray]):
            List of 8x8 blocks.
        original_shape (Tuple[int, int]):
            Original image shape (H, W) for cropping.
            
        Returns:
        np.ndarray:
            Reconstructed image (H x W).
        """
        try:
            original_height, original_width = original_shape
            
            # Calculate padded dimensions
            blocks_per_row = (original_width + 7) // 8
            blocks_per_col = (original_height + 7) // 8
            
            # Create empty image
            padded_height = blocks_per_col * 8
            padded_width = blocks_per_row * 8
            reconstructed = np.zeros((padded_height, padded_width), dtype=np.uint8)
            
            # Reassemble blocks
            block_idx = 0
            for y in range(0, padded_height, 8):
                for x in range(0, padded_width, 8):
                    if block_idx < len(blocks):
                        reconstructed[y:y+8, x:x+8] = blocks[block_idx]
                        block_idx += 1
            
            # Crop to original size
            reconstructed = reconstructed[:original_height, :original_width]
            
            return reconstructed
            
        except Exception as e:
            logger.error(f"Block reconstruction error: {e}")
            raise
    
    def get_mid_frequency_coefficients(self, dct_block: np.ndarray) -> List[Tuple[int, int]]:
        """
        Get positions of mid-frequency coefficients in DCT block.
        
        This method:
        1. Identifies mid-frequency coefficient positions
        2. Avoids DC coefficient (0,0)
        3. Avoids very high frequencies
        4. Returns list of (row, col) positions
        
        Parameters:
        dct_block (np.ndarray):
            8x8 DCT block.
            
        Returns:
        List[Tuple[int, int]]:
            List of mid-frequency coefficient positions.
        """
        try:
            # Zig-zag pattern for frequency ordering
            # Lower indices = lower frequencies
            zigzag_order = [
                (0, 0),  # DC - skip
                (0, 1), (1, 0),  # Low - skip
                (2, 0), (1, 1), (0, 2),  # Low-mid
                (0, 3), (1, 2), (2, 1), (3, 0),  # Mid
                (4, 0), (3, 1), (2, 2), (1, 3), (0, 4),  # Mid
                (0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0),  # Mid-high
                (6, 0), (5, 1), (4, 2), (3, 3), (2, 4), (1, 5), (0, 6),  # High
                (0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0),  # Very high
                (7, 1), (6, 2), (5, 3), (4, 4), (3, 5), (2, 6), (1, 7),  # Very high
                (2, 7), (3, 6), (4, 5), (5, 4), (6, 3), (7, 2),  # Very high
                (7, 3), (6, 4), (5, 5), (4, 6), (3, 7),  # Very high
                (4, 7), (5, 6), (6, 5), (7, 4),  # Very high
                (7, 5), (6, 6), (5, 7),  # Very high
                (6, 7), (7, 6),  # Very high
                (7, 7)  # Very high
            ]
            
            # Select mid-frequency coefficients (indices 6-20)
            # Skip DC (0) and very low frequencies (1-2)
            # Skip very high frequencies (after index 20)
            mid_freq_positions = zigzag_order[6:15]
            
            return mid_freq_positions
            
        except Exception as e:
            logger.error(f"Mid-frequency coefficient selection error: {e}")
            raise


# Global DCT transform instance
dct_transform = DCTTransform()
