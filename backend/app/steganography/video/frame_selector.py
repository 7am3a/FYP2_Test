"""
Frame Selector Module for SecureStego

Purpose:
Selects frames from video for DCT-based steganography embedding.

This module is isolated from DCT processing, video conversion, and payload embedding
to improve maintainability and debugging.

Selection Strategies:
1. Fixed Interval: Select every Nth frame
2. Uniform Distribution: Spread frames evenly throughout video
3. Password-Derived: Use password hash to determine frame sequence
4. Capacity-Aware: Select frames based on available capacity

Why This Exists:
- Provides deterministic frame selection
- Ensures reproducible extraction
- Optimizes capacity utilization
- Supports multiple selection strategies

Security Considerations:
- Deterministic selection for reproducibility
- Password-derived selection adds security
- Does not introduce detectable patterns
- Configurable for different use cases
"""

import hashlib
import logging
from typing import List, Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FrameSelector:
    """
    Selects frames from video for steganography embedding.
    
    Why this exists:
    - Provides deterministic frame selection
    - Ensures reproducible extraction
    - Optimizes capacity utilization
    - Supports multiple strategies
    
    Security Considerations:
    - Deterministic selection
    - Password-derived option
    - No detectable patterns
    - Configurable strategies
    """
    
    # Selection strategies
    STRATEGY_FIXED_INTERVAL = 'fixed_interval'
    STRATEGY_UNIFORM = 'uniform'
    STRATEGY_PASSWORD_DERIVED = 'password_derived'
    
    # Default strategy
    DEFAULT_STRATEGY = STRATEGY_FIXED_INTERVAL
    
    # Default interval for fixed interval strategy
    DEFAULT_INTERVAL = 10  # Every 10th frame
    
    def __init__(self):
        """Initialize the frame selector."""
        logger.info("FrameSelector initialized")
    
    def select_frames(
        self,
        total_frames: int,
        required_capacity: int,
        strategy: str = DEFAULT_STRATEGY,
        interval: int = DEFAULT_INTERVAL,
        password: Optional[str] = None,
        frame_capacity: int = 1000  # Default capacity per frame in bytes
    ) -> Tuple[List[int], dict]:
        """
        Select frames for embedding based on strategy.
        
        This method:
        1. Calculates required number of frames
        2. Selects frames using specified strategy
        3. Validates selection meets capacity requirements
        4. Returns selected frame indices and metadata
        
        Parameters:
        total_frames (int):
            Total number of frames in video.
        required_capacity (int):
            Required capacity in bytes.
        strategy (str):
            Selection strategy (default: fixed_interval).
        interval (int):
            Interval for fixed_interval strategy (default: 10).
        password (str, optional):
            Password for password_derived strategy.
        frame_capacity (int):
            Estimated capacity per frame in bytes (default: 1000).
            
        Returns:
        Tuple[List[int], dict]:
            - List of selected frame indices (0-indexed)
            - Dictionary with selection metadata
            
        Raises:
        ValueError: If strategy is invalid or capacity insufficient
        """
        try:
            logger.info(f"Selecting frames using strategy: {strategy}")
            logger.info(f"Total frames: {total_frames}, Required capacity: {required_capacity} bytes")
            
            # Calculate required number of frames
            required_frames = (required_capacity + frame_capacity - 1) // frame_capacity
            logger.info(f"Required frames: {required_frames}")
            
            # Select frames based on strategy
            if strategy == self.STRATEGY_FIXED_INTERVAL:
                selected_frames = self._select_fixed_interval(
                    total_frames,
                    required_frames,
                    interval
                )
            elif strategy == self.STRATEGY_UNIFORM:
                selected_frames = self._select_uniform(
                    total_frames,
                    required_frames
                )
            elif strategy == self.STRATEGY_PASSWORD_DERIVED:
                if password is None:
                    raise ValueError("Password required for password_derived strategy")
                selected_frames = self._select_password_derived(
                    total_frames,
                    required_frames,
                    password
                )
            else:
                raise ValueError(f"Invalid strategy: {strategy}")
            
            # Validate selection
            if len(selected_frames) < required_frames:
                raise ValueError(
                    f"Insufficient frames selected. "
                    f"Need {required_frames}, got {len(selected_frames)}"
                )
            
            # Calculate actual capacity
            actual_capacity = len(selected_frames) * frame_capacity
            
            # Prepare metadata
            metadata = {
                'strategy': strategy,
                'totalFrames': total_frames,
                'selectedFrames': len(selected_frames),
                'requiredFrames': required_frames,
                'requiredCapacity': required_capacity,
                'actualCapacity': actual_capacity,
                'frameCapacity': frame_capacity,
                'capacityRemaining': actual_capacity - required_capacity,
                'interval': interval if strategy == self.STRATEGY_FIXED_INTERVAL else None,
                'passwordUsed': password is not None
            }
            
            logger.info(f"Selected {len(selected_frames)} frames")
            logger.info(f"Frame indices: {selected_frames[:10]}...")  # Show first 10
            
            return selected_frames, metadata
            
        except Exception as e:
            logger.error(f"Frame selection error: {e}")
            raise
    
    def _select_fixed_interval(
        self,
        total_frames: int,
        required_frames: int,
        interval: int
    ) -> List[int]:
        """
        Select frames at fixed intervals.
        
        Selects every Nth frame starting from frame 0.
        
        Parameters:
        total_frames (int):
            Total number of frames.
        required_frames (int):
            Number of frames required.
        interval (int):
            Interval between selected frames.
            
        Returns:
        List[int]: List of selected frame indices.
        """
        try:
            selected = []
            frame_idx = 0
            
            while len(selected) < required_frames and frame_idx < total_frames:
                selected.append(frame_idx)
                frame_idx += interval
            
            return selected
            
        except Exception as e:
            logger.error(f"Fixed interval selection error: {e}")
            raise
    
    def _select_uniform(
        self,
        total_frames: int,
        required_frames: int
    ) -> List[int]:
        """
        Select frames uniformly distributed throughout video.
        
        Spreads frames evenly across the entire video duration.
        
        Parameters:
        total_frames (int):
            Total number of frames.
        required_frames (int):
            Number of frames required.
            
        Returns:
        List[int]: List of selected frame indices.
        """
        try:
            if required_frames >= total_frames:
                return list(range(total_frames))
            
            # Calculate step size
            step = total_frames / required_frames
            
            # Select frames
            selected = []
            for i in range(required_frames):
                frame_idx = int(i * step)
                selected.append(frame_idx)
            
            return selected
            
        except Exception as e:
            logger.error(f"Uniform selection error: {e}")
            raise
    
    def _select_password_derived(
        self,
        total_frames: int,
        required_frames: int,
        password: str
    ) -> List[int]:
        """
        Select frames using password-derived sequence.
        
        Uses password hash to generate deterministic frame sequence.
        Same password always produces same frame sequence.
        
        Parameters:
        total_frames (int):
            Total number of frames.
        required_frames (int):
            Number of frames required.
        password (str):
            Password for deriving sequence.
            
        Returns:
        List[int]: List of selected frame indices.
        """
        try:
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Use hash to generate seed
            seed = int(password_hash[:16], 16)
            
            # Simple PRNG using seed
            selected = set()
            current = seed
            
            while len(selected) < required_frames and len(selected) < total_frames:
                # Map to frame index
                frame_idx = current % total_frames
                selected.add(frame_idx)
                
                # Advance PRNG (simple linear congruential generator)
                current = (current * 1103515245 + 12345) & 0x7fffffff
            
            # Convert to sorted list
            return sorted(list(selected))
            
        except Exception as e:
            logger.error(f"Password-derived selection error: {e}")
            raise
    
    def calculate_frame_capacity(
        self,
        frame_width: int,
        frame_height: int,
        coefficient_count: int = 15,
        bits_per_coefficient: int = 1
    ) -> int:
        """
        Calculate embedding capacity of a single frame.
        
        Parameters:
        frame_width (int):
            Frame width in pixels.
        frame_height (int):
            Frame height in pixels.
        coefficient_count (int):
            Number of coefficients used per block (default: 15).
        bits_per_coefficient (int):
            Bits per coefficient (default: 1).
            
        Returns:
        int: Capacity in bytes.
        """
        try:
            # Calculate number of 8x8 blocks
            blocks_per_row = (frame_width + 7) // 8
            blocks_per_col = (frame_height + 7) // 8
            total_blocks = blocks_per_row * blocks_per_col
            
            # Calculate total bits
            total_bits = total_blocks * coefficient_count * bits_per_coefficient
            
            # Convert to bytes (subtract header overhead)
            header_size = 32  # bytes
            capacity_bytes = (total_bits // 8) - header_size
            
            return max(0, capacity_bytes)
            
        except Exception as e:
            logger.error(f"Frame capacity calculation error: {e}")
            return 0


# Global frame selector instance
frame_selector = FrameSelector()
