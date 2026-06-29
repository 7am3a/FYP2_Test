"""
Steganography Routes for SecureStego

This module provides API endpoints for embedding and extracting
encrypted messages from images using edge-based LSB steganography.

Endpoints:
- POST /api/steganography/embed - Embed encrypted message into image
- POST /api/steganography/extract - Extract encrypted message from image
- GET /api/steganography/health - Health check endpoint
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.models import EmbedResponse, ExtractResponse
from app.services.steganography_service import steganography_service
import time
import os
from app.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/steganography", tags=["steganography"])


@router.post("/embed", response_model=EmbedResponse, status_code=status.HTTP_200_OK)
async def embed_message(
    image: UploadFile = File(..., description="Image file to embed message into"),
    encryptedMessage: str = Form(..., description="Base64 encoded encrypted message"),
    salt: str = Form(..., description="Base64 encoded salt for key derivation"),
    iv: str = Form(..., description="Base64 encoded IV for encryption"),
    algorithm: str = Form(default="AES-256-GCM", description="Encryption algorithm used"),
    kdf: str = Form(default="Argon2id", description="Key derivation function used")
):
    """
    Embed an encrypted message into an image using edge-based LSB steganography.
    
    This endpoint:
    1. Accepts an image file (PNG, JPG, JPEG, HEIC)
    2. Accepts encrypted message, salt, and iv from encryption service
    3. Converts image to PNG if needed
    4. Detects edge pixels using Canny edge detection
    5. Embeds encrypted message with metadata into edge pixels
    6. Returns stego image information and statistics
    
    Args:
        image: Image file to embed message into
        encryptedMessage: Base64 encoded encrypted message
        salt: Base64 encoded salt for key derivation
        iv: Base64 encoded IV for encryption
        algorithm: Encryption algorithm used (default: AES-256-GCM)
        kdf: Key derivation function used (default: Argon2id)
        
    Returns:
        EmbedResponse with stego image information and statistics
        
    Raises:
        HTTPException: If embedding fails or image capacity is insufficient
    """
    temp_image_path = None
    try:
        logger.info("Received steganography embed request")
        start_time = time.time()
        
        # Validate file type
        allowed_extensions = ['.png', '.jpg', '.jpeg', '.heic', '.heif']
        file_ext = os.path.splitext(image.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported image format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file to temporary location
        import tempfile
        temp_image_path = tempfile.NamedTemporaryFile(
            suffix=file_ext,
            delete=False
        )
        temp_image_path.write(await image.read())
        temp_image_path.close()
        
        logger.info(f"Image uploaded: {image.filename} ({file_ext})")
        
        # Perform embedding using steganography service
        result = steganography_service.embed_message(
            image_path=temp_image_path.name,
            encrypted_data=encryptedMessage,
            salt=salt,
            iv=iv,
            algorithm=algorithm,
            kdf=kdf
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message embedded successfully in {processing_time:.3f}s")
        
        # Prepare response
        response = EmbedResponse(
            success=True,
            fileName=result['fileName'],
            originalFormat=result['originalFormat'],
            convertedFormat=result['convertedFormat'],
            statistics=result['statistics']
        )
        
        # Store stego image path for download endpoint
        # In production, you'd use a proper file storage system
        response.stegoImagePath = result['stegoImagePath']
        
        return response
        
    except ValueError as e:
        logger.error(f"Embed validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Embed error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Embedding failed. Please try again."
        )
    finally:
        # Cleanup temporary uploaded file
        if temp_image_path and os.path.exists(temp_image_path.name):
            try:
                os.remove(temp_image_path.name)
                logger.info(f"Cleaned up temporary file: {temp_image_path.name}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary file: {e}")


@router.post("/extract", response_model=ExtractResponse, status_code=status.HTTP_200_OK)
async def extract_message(
    image: UploadFile = File(..., description="Stego image file containing hidden message")
):
    """
    Extract an encrypted message from a stego image.
    
    This endpoint:
    1. Accepts a stego PNG image file
    2. Detects edge pixels using Canny edge detection
    3. Extracts hidden data from edge pixels
    4. Deserializes payload to get encrypted message and metadata
    5. Automatically recovers salt and iv from payload (version 2.0+)
    6. Returns encrypted message, metadata, and statistics
    
    Args:
        image: Stego PNG image file containing hidden message
        
    Returns:
        ExtractResponse with encrypted message, metadata, and statistics
        
    Raises:
        HTTPException: If extraction fails or image is invalid
    """
    temp_image_path = None
    try:
        logger.info("Received steganography extract request")
        start_time = time.time()
        
        # Validate file type (must be PNG)
        file_ext = os.path.splitext(image.filename)[1].lower()
        
        if file_ext != '.png':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image format. Only PNG files are supported for extraction."
            )
        
        # Save uploaded file to temporary location
        import tempfile
        temp_image_path = tempfile.NamedTemporaryFile(
            suffix='.png',
            delete=False
        )
        temp_image_path.write(await image.read())
        temp_image_path.close()
        
        logger.info(f"Stego image uploaded: {image.filename}")
        
        # Perform extraction using steganography service
        result = steganography_service.extract_message(
            image_path=temp_image_path.name
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message extracted successfully in {processing_time:.3f}s")
        
        # Prepare response
        response = ExtractResponse(
            success=True,
            encryptedData=result['encryptedData'],
            algorithm=result['algorithm'],
            kdf=result.get('kdf', 'Argon2id'),
            salt=result.get('salt'),
            iv=result.get('iv'),
            version=result['version'],
            timestamp=result['timestamp'],
            statistics=result['statistics']
        )
        
        return response
        
    except ValueError as e:
        logger.error(f"Extract validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Extract error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Extraction failed. Please check the image and try again."
        )
    finally:
        # Cleanup temporary uploaded file
        if temp_image_path and os.path.exists(temp_image_path.name):
            try:
                os.remove(temp_image_path.name)
                logger.info(f"Cleaned up temporary file: {temp_image_path.name}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary file: {e}")


@router.get("/download/{filename}", status_code=status.HTTP_200_OK)
async def download_stego_image(filename: str):
    """
    Download a stego image file.
    
    Args:
        filename: Name of the stego image file to download
        
    Returns:
        FileResponse with the stego image
        
    Raises:
        HTTPException: If file not found
    """
    try:
        # In production, you'd use a proper file storage system
        # For now, we assume files are in temp directory
        import tempfile
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stego image not found. It may have expired."
            )
        
        logger.info(f"Downloading stego image: {filename}")
        
        return FileResponse(
            file_path,
            media_type="image/png",
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Download failed. Please try again."
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint for steganography service."""
    return {
        "status": "healthy",
        "service": "steganography",
        "method": "Edge-Based LSB",
        "edgeDetection": "Canny",
        "supportedFormats": ["PNG", "JPG", "JPEG", "HEIC"],
        "outputFormat": "PNG"
    }
