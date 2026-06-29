"""
Application State for SecureStego

Manages application-wide state and configuration.
"""

from typing import Dict, Any
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class AppState:
    """
    Manages application state.
    
    Why this exists:
    - Provides a centralized location for application state
    - Enables state management across modules
    - Facilitates testing with mock state
    - Supports future features like caching and rate limiting
    """
    
    _instance = None
    _state: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from state."""
        return self._state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in state."""
        self._state[key] = value
    
    def delete(self, key: str) -> None:
        """Delete a value from state."""
        if key in self._state:
            del self._state[key]
    
    def clear(self) -> None:
        """Clear all state."""
        self._state.clear()


# Global app state instance
app_state = AppState()
