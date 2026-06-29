"""
Base Repository for SecureStego

Provides a base class for all repositories with common CRUD operations.
"""

from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class BaseRepository(ABC):
    """
    Abstract base repository class.
    
    Why this exists:
    - Provides a common interface for all repositories
    - Ensures consistent data access patterns
    - Facilitates testing with mock implementations
    - Enables future database integration without changing business logic
    """
    
    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record."""
        pass
    
    @abstractmethod
    async def read(self, id: str) -> Optional[Dict[str, Any]]:
        """Read a record by ID."""
        pass
    
    @abstractmethod
    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record by ID."""
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete a record by ID."""
        pass
