"""
Video Steganography Routes for SecureStego

This module provides API endpoints for embedding and extracting
encrypted messages from videos using DCT-based steganography.

Endpoints:
- POST /api/video/embed - Embed encrypted message into video
- POST /api/video/extract - Extract encrypted message from video
- GET /api/video/download/{filename} - Download stego video
- GET /api/video/health - Health check endpoint
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.models import VideoEmbedResponse, VideoExtractResponse
from app.services.video_steganography_service import video_steganography_service
import time
import os
from app.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/video", tags=["video-steganography"])


@router.post("/embed", response_model=VideoEmbedResponse, status_code=status.HTTP_200_OK)
async def embed_message(
    video: UploadFile = File(..., description="Video file to embed message into"),
    encryptedMessage: str = Form(..., description="Base64 encoded encrypted message"),
    salt: str = Form(..., description="Base64 encoded salt for key derivation"),
    iv: str = Form(..., description="Base64 encoded IV for encryption"),
    algorithm: str = Form(default="AES-256-GCM", description="Encryption algorithm used"),
    kdf: str = Form(default="Argon2id", description="Key derivation function used"),
    frameSelectionStrategy: str = Form(default="fixed_interval", description="Frame selection strategy"),
    frameInterval: int = Form(default=10, description="Interval for fixed interval selection")
):
    """
    Embed an encrypted message into a video using DCT-based steganography.
    
    This endpoint:
    1. Accepts a video file (MP4, AVI, MOV)
    2. Accepts encrypted message, salt, and iv from encryption service
    3. Converts video to MP4 if needed
    4. Extracts frames and selects embedding frames
    5. Embeds encrypted message with metadata using DCT coefficients
    6. Rebuilds video with preserved audio
    7. Returns stego video information and statistics
    
    Args:
        video: Video file to embed message into
        encryptedMessage: Base64 encoded encrypted message
        salt: Base64 encoded salt for key derivation
        iv: Base64 encoded IV for encryption
        algorithm: Encryption algorithm used (default: AES-256-GCM)
        kdf: Key derivation function used (default: Argon2id)
        frameSelectionStrategy: Frame selection strategy (default: fixed_interval)
        frameInterval: Interval for fixed interval selection (default: 10)
        
    Returns:
        VideoEmbedResponse with stego video information and statistics
        
    Raises:
        HTTPException: If embedding fails or video capacity is insufficient
    """
    temp_video_path = None
    try:
        logger.info("Received video steganography embed request")
        start_time = time.time()
        
        # Validate file type
        allowed_extensions = ['.mp4', '.avi', '.mov']
        file_ext = os.path.splitext(video.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported video format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file to temporary location
        import tempfile
        temp_video_path = tempfile.NamedTemporaryFile(
            suffix=file_ext,
            delete=False
        )
        temp_video_path.write(await video.read())
        temp_video_path.close()
        
        logger.info(f"Video uploaded: {video.filename} ({file_ext})")
        
        # Perform embedding using video steganography service
        result = video_steganography_service.embed_message(
            video_path=temp_video_path.name,
            encrypted_data=encryptedMessage,
            salt=salt,
            iv=iv,
            algorithm=algorithm,
            kdf=kdf,
            frame_selection_strategy=frameSelectionStrategy,
            frame_interval=frameInterval
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message embedded successfully in {processing_time:.3f}s")
        
        # Prepare response
        response = VideoEmbedResponse(
            success=True,
            fileName=result['fileName'],
            originalFormat=result['originalFormat'],
            convertedFormat=result['convertedFormat'],
            statistics=result['statistics']
        )
        
        # Store stego video path for download endpoint
        response.stegoVideoPath = result['stegoVideoPath']
        
        return response
        
    except ValueError as e:
        logger.error(f"Video embed validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Video embed error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Video embedding failed. Please try again."
        )
    finally:
        # Cleanup temporary uploaded file
        if temp_video_path and os.path.exists(temp_video_path.name):
            try:
                os.remove(temp_video_path.name)
                logger.info(f"Cleaned up temporary file: {temp_video_path.name}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary file: {e}")


@router.post("/extract", response_model=VideoExtractResponse, status_code=status.HTTP_200_OK)
async def extract_message(
    video: UploadFile = File(..., description="Stego video file containing hidden message")
):
    """
    Extract an encrypted message from a stego video.
    
    This endpoint:
    1. Accepts a stego MP4 video file
    2. Extracts frames from video
    3. Extracts hidden data using DCT coefficients
    4. Deserializes payload to get encrypted message
    5. Returns encrypted message and statistics
    
    Args:
        video: Stego MP4 video file containing hidden message
        
    Returns:
        VideoExtractResponse with encrypted message and statistics
        
    Raises:
        HTTPException: If extraction fails or video is invalid
    """
    temp_video_path = None
    try:
        logger.info("Received video steganography extract request")
        start_time = time.time()
        
        # Validate file type (must be MP4)
        file_ext = os.path.splitext(video.filename)[1].lower()
        
        if file_ext != '.mp4':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid video format. Only MP4 files are supported for extraction."
            )
        
        # Save uploaded file to temporary location
        import tempfile
        temp_video_path = tempfile.NamedTemporaryFile(
            suffix='.mp4',
            delete=False
        )
        temp_video_path.write(await video.read())
        temp_video_path.close()
        
        logger.info(f"Stego video uploaded: {video.filename}")
        
        # Perform extraction using video steganography service
        result = video_steganography_service.extract_message(
            video_path=temp_video_path.name
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message extracted successfully in {processing_time:.3f}s")
        
        # Prepare response
        response = VideoExtractResponse(
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
        logger.error(f"Video extract validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Video extract error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Video extraction failed. Please check the video and try again."
        )
    finally:
        # Cleanup temporary uploaded file
        if temp_video_path and os.path.exists(temp_video_path.name):
            try:
                os.remove(temp_video_path.name)
                logger.info(f"Cleaned up temporary file: {temp_video_path.name}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary file: {e}")


@router.get("/download/{filename}", status_code=status.HTTP_200_OK)
async def download_stego_video(filename: str):
    """
    Download a stego video file.
    
    Args:
        filename: Name of the stego video file to download
        
    Returns:
        FileResponse with the stego video
        
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
                detail="Stego video not found. It may have expired."
            )
        
        logger.info(f"Downloading stego video: {filename}")
        
        return FileResponse(
            file_path,
            media_type="video/mp4",
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
    """Health check endpoint for video steganography service."""
    return {
        "status": "healthy",
        "service": "video-steganography",
        "method": "DCT-Based Block Steganography",
        "supportedFormats": ["MP4", "AVI", "MOV"],
        "outputFormat": "MP4",
        "frameSelectionStrategies": ["fixed_interval", "uniform", "password_derived"],
        "audioPreservation": True
    }
