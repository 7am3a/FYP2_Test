"""
Centralized Logging Configuration for SecureStego

This module provides a unified logging configuration for all modules.
It ensures consistent logging format, levels, and handlers across the application.

Benefits:
- Single source of truth for logging configuration
- Consistent log format across all modules
- Easy to modify logging behavior globally
- Supports structured logging for production
"""

import logging
import sys
from typing import Optional


class LoggingConfig:
    """
    Centralized logging configuration for SecureStego.
    
    Why this exists:
    - Eliminates duplicate logging.basicConfig() calls across modules
    - Ensures consistent log format throughout the application
    - Provides single point of control for logging behavior
    - Enables easy configuration changes
    
    Features:
    - Structured log format with timestamp, logger name, level, and message
    - Configurable log level
    - Console and file output support
    - Thread-safe configuration
    """
    
    # Default log format
    DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # Default log level
    DEFAULT_LEVEL = logging.INFO
    
    _configured = False
    
    @classmethod
    def setup_logging(
        cls,
        level: int = DEFAULT_LEVEL,
        log_format: str = DEFAULT_FORMAT,
        date_format: str = DEFAULT_DATE_FORMAT,
        log_file: Optional[str] = None
    ) -> None:
        """
        Configure logging for the entire application.
        
        This method should be called once at application startup.
        It configures the root logger and all child loggers.
        
        Parameters:
        level (int):
            Logging level (default: logging.INFO).
        log_format (str):
            Log message format string.
        date_format (str):
            Date format string for timestamps.
        log_file (str, optional):
            Optional file path to write logs to.
            
        Note:
            This method is idempotent - calling it multiple times has no effect.
        """
        if cls._configured:
            return
        
        # Configure root logger
        logging.basicConfig(
            level=level,
            format=log_format,
            datefmt=date_format,
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Add file handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(logging.Formatter(log_format, date_format))
            logging.getLogger().addHandler(file_handler)
        
        cls._configured = True
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get a logger instance with the specified name.
        
        Parameters:
        name (str):
            Name of the logger (typically __name__ of the calling module).
            
        Returns:
        logging.Logger: Configured logger instance.
        """
        return logging.getLogger(name)
    
    @classmethod
    def set_level(cls, level: int) -> None:
        """
        Change the logging level at runtime.
        
        Parameters:
        level (int):
            New logging level.
        """
        logging.getLogger().setLevel(level)
    
    @classmethod
    def is_configured(cls) -> bool:
        """
        Check if logging has been configured.
        
        Returns:
        bool: True if logging is configured, False otherwise.
        """
        return cls._configured


# Convenience function for getting loggers
def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    This is a convenience function that wraps LoggingConfig.get_logger().
    
    Parameters:
    name (str):
        Name of the logger.
        
    Returns:
    logging.Logger: Configured logger instance.
    """
    return LoggingConfig.get_logger(name)
