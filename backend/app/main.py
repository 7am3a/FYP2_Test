from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.routes import encryption_router, steganography_router, video_steganography_router, document_steganography_router, audio_steganography_router
from app.utils.logging_config import LoggingConfig, get_logger

# Configure centralized logging
LoggingConfig.setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    This replaces the deprecated @app.on_event decorators.
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"API prefix: {settings.api_prefix}")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="SecureStego Backend API - Secure steganography platform with Argon2id encryption",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(encryption_router, prefix=settings.api_prefix)
app.include_router(steganography_router, prefix=settings.api_prefix)
app.include_router(video_steganography_router, prefix=settings.api_prefix)
app.include_router(document_steganography_router, prefix=settings.api_prefix)
app.include_router(audio_steganography_router, prefix=settings.api_prefix)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "endpoints": {
            "docs": "/api/docs",
            "health": "/health",
            "encryption": {
                "health": f"{settings.api_prefix}/encryption/health",
                "encrypt": f"{settings.api_prefix}/encryption/encrypt",
                "decrypt": f"{settings.api_prefix}/encryption/decrypt"
            },
            "steganography": {
                "health": f"{settings.api_prefix}/steganography/health",
                "embed": f"{settings.api_prefix}/steganography/embed",
                "extract": f"{settings.api_prefix}/steganography/extract"
            },
            "video_steganography": {
                "health": f"{settings.api_prefix}/video/health",
                "embed": f"{settings.api_prefix}/video/embed",
                "extract": f"{settings.api_prefix}/video/extract",
                "download": f"{settings.api_prefix}/video/download/{{filename}}"
            },
            "document_steganography": {
                "health": f"{settings.api_prefix}/document/health",
                "embed": f"{settings.api_prefix}/document/embed",
                "extract": f"{settings.api_prefix}/document/extract",
                "download": f"{settings.api_prefix}/document/download/{{filename}}"
            },
            "audio_steganography": {
                "health": f"{settings.api_prefix}/audio/health",
                "embed": f"{settings.api_prefix}/audio/embed",
                "extract": f"{settings.api_prefix}/audio/extract",
                "download": f"{settings.api_prefix}/audio/download/{{filename}}"
            }
        }
    }


@app.get("/health", tags=["health"])
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }
