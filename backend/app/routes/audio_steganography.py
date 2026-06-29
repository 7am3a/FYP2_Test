"""
Audio Steganography Routes for SecureStego

This module provides API endpoints for embedding and extracting
encrypted messages from audio files using randomized LSB steganography.

Endpoints:
- POST /api/audio/embed - Embed encrypted message into audio
- POST /api/audio/extract - Extract encrypted message from audio
- GET /api/audio/download/{filename} - Download stego audio file
- GET /api/audio/health - Health check endpoint
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.models import AudioEmbedResponse, AudioExtractResponse
from app.services.audio_steganography_service import audio_steganography_service
import time
import os
from app.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/audio", tags=["audio_steganography"])


@router.post("/embed", response_model=AudioEmbedResponse, status_code=status.HTTP_200_OK)
async def embed_message(
    audio: UploadFile = File(..., description="Audio file to embed message into"),
    encryptedMessage: str = Form(..., description="Base64 encoded encrypted message"),
    salt: str = Form(..., description="Base64 encoded salt for key derivation"),
    iv: str = Form(..., description="Base64 encoded IV for encryption"),
    password: str = Form(..., description="Password for sample position generation"),
    algorithm: str = Form(default="AES-256-GCM", description="Encryption algorithm used"),
    kdf: str = Form(default="Argon2id", description="Key derivation function used")
):
    """
    Embed an encrypted message into an audio file using randomized LSB steganography.
    
    This endpoint:
    1. Accepts an audio file (WAV, MP3, M4A, FLAC)
    2. Accepts encrypted message, salt, and iv from encryption service
    3. Accepts password for randomized sample selection
    4. Converts audio to WAV if needed
    5. Generates randomized sample positions from password
    6. Embeds encrypted message with metadata into audio samples using LSB
    7. Returns stego audio information and statistics
    
    Args:
        audio: Audio file to embed message into
        encryptedMessage: Base64 encoded encrypted message
        salt: Base64 encoded salt for key derivation
        iv: Base64 encoded IV for encryption
        password: Password for generating sample positions
        algorithm: Encryption algorithm used (default: AES-256-GCM)
        kdf: Key derivation function used (default: Argon2id)
        
    Returns:
        AudioEmbedResponse with stego audio information and statistics
        
    Raises:
        HTTPException: If embedding fails or audio capacity is insufficient
    """
    temp_audio_path = None
    try:
        logger.info("Received audio steganography embed request")
        start_time = time.time()
        
        # Validate file type
        allowed_extensions = ['.wav', '.mp3', '.m4a', '.flac']
        file_ext = os.path.splitext(audio.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported audio format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file to temporary location
        import tempfile
        temp_audio_path = tempfile.NamedTemporaryFile(
            suffix=file_ext,
            delete=False
        )
        temp_audio_path.write(await audio.read())
        temp_audio_path.close()
        
        logger.info(f"Audio uploaded: {audio.filename} ({file_ext})")
        
        # Perform embedding using audio steganography service
        result = audio_steganography_service.embed_message(
            audio_path=temp_audio_path.name,
            encrypted_data=encryptedMessage,
            salt=salt,
            iv=iv,
            password=password,
            algorithm=algorithm,
            kdf=kdf
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message embedded successfully in {processing_time:.3f}s")
        
        # Prepare response
        response = AudioEmbedResponse(
            success=True,
            fileName=result['fileName'],
            originalFormat=result['originalFormat'],
            convertedFormat=result['convertedFormat'],
            statistics=result['statistics'],
            debug=result.get('debug')
        )
        
        # Store stego audio path for download endpoint
        # In production, you'd use a proper file storage system
        response.stegoAudioPath = result['stegoAudioPath']
        
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
        if temp_audio_path and os.path.exists(temp_audio_path.name):
            try:
                os.remove(temp_audio_path.name)
                logger.info(f"Cleaned up temporary file: {temp_audio_path.name}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary file: {e}")


@router.post("/extract", response_model=AudioExtractResponse, status_code=status.HTTP_200_OK)
async def extract_message(
    audio: UploadFile = File(..., description="Stego audio file containing hidden message"),
    password: str = Form(..., description="Password for sample position generation")
):
    """
    Extract an encrypted message from a stego audio file.
    
    This endpoint:
    1. Accepts a stego WAV audio file
    2. Accepts password for sample position generation
    3. Generates randomized sample positions from password
    4. Extracts hidden data from audio samples using LSB
    5. Deserializes payload to get encrypted message
    6. Returns encrypted message and statistics
    
    Args:
        audio: Stego WAV audio file containing hidden message
        password: Password for generating sample positions
        
    Returns:
        AudioExtractResponse with encrypted message and statistics
        
    Raises:
        HTTPException: If extraction fails or audio is invalid
    """
    temp_audio_path = None
    try:
        logger.info("Received audio steganography extract request")
        start_time = time.time()
        
        # Validate file type (must be WAV)
        file_ext = os.path.splitext(audio.filename)[1].lower()
        
        if file_ext != '.wav':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid audio format. Only WAV files are supported for extraction."
            )
        
        # Save uploaded file to temporary location
        import tempfile
        temp_audio_path = tempfile.NamedTemporaryFile(
            suffix='.wav',
            delete=False
        )
        temp_audio_path.write(await audio.read())
        temp_audio_path.close()
        
        logger.info(f"Stego audio uploaded: {audio.filename}")
        
        # Perform extraction using audio steganography service
        result = audio_steganography_service.extract_message(
            audio_path=temp_audio_path.name,
            password=password
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message extracted successfully in {processing_time:.3f}s")
        
        # Prepare response
        response = AudioExtractResponse(
            success=True,
            encryptedData=result['encryptedData'],
            algorithm=result['algorithm'],
            kdf=result['kdf'],
            salt=result['salt'],
            iv=result['iv'],
            version=result['version'],
            timestamp=result['timestamp'],
            statistics=result['statistics'],
            debug=result.get('debug')
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
            detail="Extraction failed. Please check the audio file and try again."
        )
    finally:
        # Cleanup temporary uploaded file
        if temp_audio_path and os.path.exists(temp_audio_path.name):
            try:
                os.remove(temp_audio_path.name)
                logger.info(f"Cleaned up temporary file: {temp_audio_path.name}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary file: {e}")


@router.get("/download/{filename}", status_code=status.HTTP_200_OK)
async def download_stego_audio(filename: str):
    """
    Download a stego audio file.
    
    Args:
        filename: Name of the stego audio file to download
        
    Returns:
        FileResponse with the stego audio
        
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
                detail="Stego audio not found. It may have expired."
            )
        
        logger.info(f"Downloading stego audio: {filename}")
        
        return FileResponse(
            file_path,
            media_type="audio/wav",
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
    """Health check endpoint for audio steganography service."""
    return {
        "status": "healthy",
        "service": "audio_steganography",
        "method": "Randomized WAV LSB",
        "supportedFormats": ["WAV", "MP3", "M4A", "FLAC"],
        "outputFormat": "WAV",
        "embeddingMethod": "Randomized LSB",
        "sampleSelection": "Password-Derived Deterministic Random"
    }
