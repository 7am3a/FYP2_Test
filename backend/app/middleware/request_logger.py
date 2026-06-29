"""
Request Logger Middleware for SecureStego

Logs all incoming requests for audit trail.
"""

from fastapi import Request
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


async def request_logger_middleware(request: Request, call_next):
    """
    Log all incoming requests.
    """
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} - {response.status_code}")
    return response
