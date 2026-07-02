"""
Document Steganography Routes for SecureStego

This module provides API endpoints for embedding and extracting
encrypted messages from documents (PDF and TXT) using hybrid dual-layer
steganography.

Endpoints:
- POST /api/document/embed - Embed encrypted message into document
- POST /api/document/extract - Extract encrypted message from document
- GET /api/document/download/{filename} - Download stego document
- GET /api/document/health - Health check endpoint
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.models.schemas import DocumentEmbedResponse, DocumentExtractResponse
from app.services.document_steganography_service import document_steganography_service
import time
import os
from app.utils.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/document", tags=["document_steganography"])


@router.post("/embed", response_model=DocumentEmbedResponse, status_code=status.HTTP_200_OK)
async def embed_message(
    document: UploadFile = File(..., description="Document file (PDF or TXT) to embed message into"),
    encryptedMessage: str = Form(..., description="Base64 encoded encrypted message"),
    algorithm: str = Form(default="AES-256-GCM", description="Encryption algorithm used"),
    textMethod: str = Form(default="invisible_character", description="Text embedding method"),
    useImages: bool = Form(default=True, description="Use image steganography for PDFs")
):
    """
    Embed an encrypted message into a document using hybrid dual-layer steganography.
    
    This endpoint:
    1. Accepts a document file (PDF or TXT)
    2. Accepts encrypted message from encryption service
    3. For TXT: Embeds using invisible characters or structure-based methods
    4. For PDF: Implements hybrid dual-layer embedding
       - Text content: Invisible character or structure-based
       - Embedded images: Edge-based LSB
    5. Returns stego document information and statistics
    
    Args:
        document: Document file to embed message into (PDF or TXT)
        encryptedMessage: Base64 encoded encrypted message
        algorithm: Encryption algorithm used (default: AES-256-GCM)
        textMethod: Text embedding method ('invisible_character' or 'structure')
        useImages: Whether to use image steganography for PDFs (default: True)
        
    Returns:
        DocumentEmbedResponse with stego document information and statistics
        
    Raises:
        HTTPException: If embedding fails or document capacity is insufficient
    """
    temp_document_path = None
    try:
        logger.info("Received document steganography embed request")
        start_time = time.time()
        
        # Validate file type
        allowed_extensions = ['.pdf', '.txt']
        file_ext = os.path.splitext(document.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported document format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file to temporary location
        import tempfile
        temp_document_path = tempfile.NamedTemporaryFile(
            suffix=file_ext,
            delete=False
        )
        temp_document_path.write(await document.read())
        temp_document_path.close()
        
        logger.info(f"Document uploaded: {document.filename} ({file_ext})")
        
        # Perform embedding using document steganography service
        result = document_steganography_service.embed_message(
            document_path=temp_document_path.name,
            encrypted_data=encryptedMessage,
            algorithm=algorithm,
            text_method=textMethod,
            use_images=useImages
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message embedded successfully in {processing_time:.3f}s")
        
        # Prepare response
        response = DocumentEmbedResponse(
            success=True,
            fileName=result['fileName'],
            documentType=result['documentType'],
            statistics=result['statistics']
        )
        
        # Store stego document path for download endpoint
        response.stegoDocumentPath = result['stegoDocumentPath']
        
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
        if temp_document_path and os.path.exists(temp_document_path.name):
            try:
                os.remove(temp_document_path.name)
                logger.info(f"Cleaned up temporary file: {temp_document_path.name}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary file: {e}")


@router.post("/extract", response_model=DocumentExtractResponse, status_code=status.HTTP_200_OK)
async def extract_message(
    document: UploadFile = File(..., description="Stego document file containing hidden message")
):
    """
    Extract an encrypted message from a stego document.
    
    This endpoint:
    1. Accepts a stego document file (PDF or TXT)
    2. For TXT: Extracts using invisible characters or structure-based methods
    3. For PDF: Implements hybrid dual-layer extraction
       - Extract from text
       - Extract from images
       - Combine payloads
    4. Deserializes payload to get encrypted message
    5. Returns encrypted message and statistics
    
    Args:
        document: Stego document file containing hidden message (PDF or TXT)
        
    Returns:
        DocumentExtractResponse with encrypted message and statistics
        
    Raises:
        HTTPException: If extraction fails or document is invalid
    """
    temp_document_path = None
    try:
        logger.info("Received document steganography extract request")
        start_time = time.time()
        
        # Validate file type
        allowed_extensions = ['.pdf', '.txt']
        file_ext = os.path.splitext(document.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported document format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file to temporary location
        import tempfile
        temp_document_path = tempfile.NamedTemporaryFile(
            suffix=file_ext,
            delete=False
        )
        temp_document_path.write(await document.read())
        temp_document_path.close()
        
        logger.info(f"Stego document uploaded: {document.filename}")
        
        # Perform extraction using document steganography service
        result = document_steganography_service.extract_message(
            document_path=temp_document_path.name
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Message extracted successfully in {processing_time:.3f}s")
        
        # Prepare response
        response = DocumentExtractResponse(
            success=True,
            encryptedData=result['encryptedData'],
            algorithm=result['algorithm'],
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
            detail="Extraction failed. Please check the document and try again."
        )
    finally:
        # Cleanup temporary uploaded file
        if temp_document_path and os.path.exists(temp_document_path.name):
            try:
                os.remove(temp_document_path.name)
                logger.info(f"Cleaned up temporary file: {temp_document_path.name}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary file: {e}")


@router.get("/download/{filename}", status_code=status.HTTP_200_OK)
async def download_stego_document(filename: str):
    """
    Download a stego document file.
    
    Args:
        filename: Name of the stego document file to download
        
    Returns:
        FileResponse with the stego document
        
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
                detail="Stego document not found. It may have expired."
            )
        
        logger.info(f"Downloading stego document: {filename}")
        
        # Determine media type based on extension
        if filename.endswith('.pdf'):
            media_type = "application/pdf"
        elif filename.endswith('.txt'):
            media_type = "text/plain"
        else:
            media_type = "application/octet-stream"
        
        return FileResponse(
            file_path,
            media_type=media_type,
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
    """Health check endpoint for document steganography service."""
    return {
        "status": "healthy",
        "service": "document_steganography",
        "method": "Hybrid Dual-Layer Document Steganography",
        "textMethods": ["invisible_character", "structure"],
        "imageMethod": "Edge-Based LSB",
        "supportedFormats": ["PDF", "TXT"],
        "outputFormats": {
            "PDF": "PDF",
            "TXT": "TXT"
        }
    }
