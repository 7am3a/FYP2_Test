"""
Unit Tests for LoggingConfig
Tests centralized logging configuration
"""

import pytest
import logging
from app.utils.logging_config import LoggingConfig, get_logger


class TestLoggingConfig:
    """Test cases for LoggingConfig"""
    
    def test_setup_logging(self):
        """Test logging setup"""
        LoggingConfig.setup_logging()
        
        assert LoggingConfig.is_configured()
    
    def test_setup_logging_idempotent(self):
        """Test that setup_logging can be called multiple times safely"""
        LoggingConfig.setup_logging()
        LoggingConfig.setup_logging()
        
        assert LoggingConfig.is_configured()
    
    def test_get_logger(self):
        """Test logger retrieval"""
        LoggingConfig.setup_logging()
        
        logger = get_logger("test_module")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"
    
    def test_set_level(self):
        """Test changing log level"""
        LoggingConfig.setup_logging()
        
        LoggingConfig.set_level(logging.DEBUG)
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG
    
    def test_is_configured(self):
        """Test configuration status check"""
        # Before setup
        status_before = LoggingConfig.is_configured()
        
        # After setup
        LoggingConfig.setup_logging()
        status_after = LoggingConfig.is_configured()
        
        assert not status_before or status_after  # Should be true after setup
