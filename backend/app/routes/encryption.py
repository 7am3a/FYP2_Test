from fastapi import APIRouter, HTTPException, status
from app.models import EncryptRequest, EncryptResponse, DecryptRequest, DecryptResponse, ExtractDecryptRequest
from app.services.crypto_service import crypto_service
import time
from app.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/encryption", tags=["encryption"])


@router.post("/encrypt", response_model=EncryptResponse, status_code=status.HTTP_200_OK)
async def encrypt_message(request: EncryptRequest):
    """
    Encrypt a message using Argon2id key derivation and AES-256-GCM.
    
    This endpoint receives a plaintext message and password, then performs
    server-side encryption using Argon2id for key derivation and AES-256-GCM.
    
    Args:
        request: EncryptRequest containing message and password
        
    Returns:
        EncryptResponse with ciphertext, salt, iv, algorithm, and kdf
        
    Raises:
        HTTPException: If encryption fails
    """
    try:
        logger.info("Received encryption request")
        start_time = time.time()
        
        # Perform encryption using crypto service
        result = crypto_service.encrypt_message(
            message=request.message,
            password=request.password
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message encrypted successfully in {processing_time:.3f}s")
        
        return EncryptResponse(
            success=True,
            ciphertext=result["ciphertext"],
            salt=result["salt"],
            iv=result["iv"],
            algorithm=result["algorithm"],
            kdf=result["kdf"]
        )
        
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Encryption failed. Please try again."
        )


@router.post("/decrypt", response_model=DecryptResponse, status_code=status.HTTP_200_OK)
async def decrypt_message(request: DecryptRequest):
    """
    Decrypt a message using Argon2id key derivation and AES-256-GCM.
    
    This endpoint receives ciphertext, password, salt, and iv, then performs
    decryption using Argon2id for key derivation and AES-256-GCM.
    
    Args:
        request: DecryptRequest containing ciphertext, password, salt, and iv
        
    Returns:
        DecryptResponse with decrypted message
        
    Raises:
        HTTPException: If decryption fails
    """
    try:
        logger.info("Received decryption request")
        start_time = time.time()
        
        # Perform decryption using crypto service
        message = crypto_service.decrypt_message(
            ciphertext=request.ciphertext,
            password=request.password,
            salt=request.salt,
            iv=request.iv
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message decrypted successfully in {processing_time:.3f}s")
        
        return DecryptResponse(
            success=True,
            message=message
        )
        
    except ValueError as e:
        logger.error(f"Decryption validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Decryption failed. Please check your password and try again."
        )


@router.post("/decrypt-extracted", response_model=DecryptResponse, status_code=status.HTTP_200_OK)
async def decrypt_extracted_message(request: ExtractDecryptRequest):
    """
    Decrypt an extracted message using Argon2id key derivation and AES-256-GCM.
    
    This endpoint receives encrypted data with embedded metadata (salt, iv) from 
    the extraction process and performs password-only decryption.
    
    This is the recommended workflow for end-to-end extraction:
    1. Extract payload from media (returns encryptedData + salt + iv)
    2. Decrypt using only the password (salt and iv are auto-recovered)
    
    Args:
        request: ExtractDecryptRequest containing encryptedData, password, salt, and iv
        
    Returns:
        DecryptResponse with decrypted message
        
    Raises:
        HTTPException: If decryption fails
    """
    try:
        logger.info("Received extracted message decryption request")
        start_time = time.time()
        
        # Perform decryption using crypto service
        message = crypto_service.decrypt_message(
            ciphertext=request.encryptedData,
            password=request.password,
            salt=request.salt,
            iv=request.iv
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Extracted message decrypted successfully in {processing_time:.3f}s")
        
        return DecryptResponse(
            success=True,
            message=message
        )
        
    except ValueError as e:
        logger.error(f"Decryption validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Decryption failed. Please check your password and try again."
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint for encryption service."""
    return {
        "status": "healthy",
        "service": "encryption",
        "algorithm": "AES-256-GCM",
        "keyDerivation": "Argon2id"
    }
