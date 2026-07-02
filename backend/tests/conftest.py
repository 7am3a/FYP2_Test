"""
Pytest Configuration and Fixtures
"""

import pytest
import sys
import os

# Add backend app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configure logging for tests
from app.utils.logging_config import LoggingConfig

LoggingConfig.setup_logging()


@pytest.fixture
def sample_message():
    """Fixture for sample message"""
    return "Test secret message"


@pytest.fixture
def sample_password():
    """Fixture for sample password"""
    return "test_password_123"


@pytest.fixture
def sample_encrypted_data():
    """Fixture for sample encrypted data"""
    return "base64_encoded_encrypted_data_placeholder"
