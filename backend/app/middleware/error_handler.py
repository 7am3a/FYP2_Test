"""
Error Handler Middleware for SecureStego

Provides centralized error handling for all API requests.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.utils.exceptions import SecureStegoException
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """
    Global error handler middleware.
    
    Catches all exceptions and returns consistent error responses.
    """
    try:
        response = await call_next(request)
        return response
    except SecureStegoException as e:
        logger.error(f"SecureStegoException: {e.message}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": e.message, "errorType": type(e).__name__}
        )
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error", "errorType": "InternalServerError"}
        )
