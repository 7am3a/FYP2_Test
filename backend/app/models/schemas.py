from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class EncryptRequest(BaseModel):
    """Request schema for encryption endpoint."""
    
    message: str = Field(
        ...,
        description="Plaintext message to encrypt",
        min_length=1
    )
    password: str = Field(
        ...,
        description="User password for key derivation",
        min_length=1
    )


class EncryptResponse(BaseModel):
    """Response schema for encryption endpoint."""
    
    success: bool = Field(default=True)
    ciphertext: str = Field(
        ...,
        description="Base64 encoded ciphertext"
    )
    salt: str = Field(
        ...,
        description="Base64 encoded salt"
    )
    iv: str = Field(
        ...,
        description="Base64 encoded IV"
    )
    algorithm: str = Field(default="AES-256-GCM")
    kdf: str = Field(default="Argon2id")


class DecryptRequest(BaseModel):
    """Request schema for decryption endpoint."""
    
    ciphertext: str = Field(
        ...,
        description="Base64 encoded ciphertext",
        min_length=1
    )
    password: str = Field(
        ...,
        description="User password for key derivation",
        min_length=1
    )
    salt: str = Field(
        ...,
        description="Base64 encoded salt",
        min_length=1
    )
    iv: str = Field(
        ...,
        description="Base64 encoded IV",
        min_length=1
    )


class ExtractDecryptRequest(BaseModel):
    """Request schema for password-only decryption after extraction."""
    
    encryptedData: str = Field(
        ...,
        description="Base64 encoded encrypted message from extraction",
        min_length=1
    )
    password: str = Field(
        ...,
        description="User password for key derivation",
        min_length=1
    )
    salt: str = Field(
        ...,
        description="Base64 encoded salt from extraction",
        min_length=1
    )
    iv: str = Field(
        ...,
        description="Base64 encoded IV from extraction",
        min_length=1
    )


class DecryptResponse(BaseModel):
    """Response schema for decryption endpoint."""
    
    success: bool = Field(default=True)
    message: str = Field(
        ...,
        description="Decrypted plaintext message"
    )


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    detail: str
    status: str = "error"


class SteganographyStatistics(BaseModel):
    """Statistics for steganography operations."""
    
    imageWidth: int = Field(..., description="Image width in pixels")
    imageHeight: int = Field(..., description="Image height in pixels")
    totalPixels: int = Field(..., description="Total number of pixels")
    edgePixels: int = Field(..., description="Number of edge pixels detected")
    payloadSize: int = Field(..., description="Payload size in bytes")
    headerSize: int = Field(..., description="Header size in bytes")
    totalBitsUsed: int = Field(..., description="Total bits used for embedding")
    capacityRemaining: int = Field(..., description="Remaining capacity in bits")
    capacityUsedPercent: float = Field(..., description="Percentage of capacity used")
    embeddingMethod: str = Field(default="Edge-Based LSB", description="Steganography method used")
    edgeDetectionMethod: str = Field(default="Canny", description="Edge detection method used")
    processingTime: float = Field(..., description="Processing time in seconds")


class EmbedResponse(BaseModel):
    success: bool = Field(default=True)
    fileName: str = Field(..., description="Name of the stego image file")
    originalFormat: str = Field(..., description="Original image format")
    convertedFormat: str = Field(default="PNG", description="Converted image format")
    statistics: SteganographyStatistics = Field(..., description="Embedding statistics")
    stegoImagePath: Optional[str] = Field(default=None, description="Path to stego image for download")  # ADD THIS

# class EmbedResponse(BaseModel):
#     """Response schema for steganography embed endpoint."""
    
#     success: bool = Field(default=True)
#     fileName: str = Field(..., description="Name of the stego image file")
#     originalFormat: str = Field(..., description="Original image format")
#     convertedFormat: str = Field(default="PNG", description="Converted image format")
#     statistics: SteganographyStatistics = Field(..., description="Embedding statistics")


class ExtractResponse(BaseModel):
    """Response schema for steganography extract endpoint."""
    
    success: bool = Field(default=True)
    encryptedData: str = Field(..., description="Base64 encoded encrypted message")
    algorithm: str = Field(default="AES-256-GCM", description="Encryption algorithm used")
    kdf: str = Field(default="Argon2id", description="Key derivation function used")
    salt: Optional[str] = Field(None, description="Base64 encoded salt (embedded in payload version 2.0+)")
    iv: Optional[str] = Field(None, description="Base64 encoded IV (embedded in payload version 2.0+)")
    version: str = Field(..., description="Payload version")
    timestamp: str = Field(..., description="Payload timestamp")
    statistics: SteganographyStatistics = Field(..., description="Extraction statistics")


class VideoSteganographyStatistics(BaseModel):
    """Statistics for video steganography operations."""
    
    videoWidth: int = Field(..., description="Video width in pixels")
    videoHeight: int = Field(..., description="Video height in pixels")
    totalFrames: int = Field(..., description="Total number of frames in video")
    selectedFrames: int = Field(..., description="Number of frames selected for embedding")
    frameSelectionStrategy: str = Field(..., description="Frame selection strategy used")
    frameInterval: int = Field(..., description="Interval for fixed interval selection")
    payloadSize: int = Field(..., description="Payload size in bytes")
    totalBitsEmbedded: int = Field(..., description="Total bits embedded")
    capacityRemaining: int = Field(..., description="Remaining capacity in bytes")
    capacityUsedPercent: float = Field(..., description="Percentage of capacity used")
    embeddingMethod: str = Field(default="DCT-Based Block Steganography", description="Steganography method used")
    audioPreserved: bool = Field(..., description="Whether audio track was preserved")
    processingTime: float = Field(..., description="Processing time in seconds")
    debug: Optional[Dict[str, Any]] = Field(None, description="Development debug information")


class VideoEmbedResponse(BaseModel):
    """Response schema for video steganography embed endpoint."""
    
    success: bool = Field(default=True)
    fileName: str = Field(..., description="Name of the stego video file")
    originalFormat: str = Field(..., description="Original video format")
    convertedFormat: str = Field(default="MP4", description="Converted video format")
    statistics: VideoSteganographyStatistics = Field(..., description="Embedding statistics")
    
    # Internal field for file path (not included in response)
    stegoVideoPath: Optional[str] = Field(None, exclude=True)


class VideoExtractResponse(BaseModel):
    """Response schema for video steganography extract endpoint."""
    
    success: bool = Field(default=True)
    encryptedData: str = Field(..., description="Base64 encoded encrypted message")
    algorithm: str = Field(default="AES-256-GCM", description="Encryption algorithm used")
    kdf: str = Field(default="Argon2id", description="Key derivation function used")
    salt: Optional[str] = Field(None, description="Base64 encoded salt (embedded in payload version 2.0+)")
    iv: Optional[str] = Field(None, description="Base64 encoded IV (embedded in payload version 2.0+)")
    version: str = Field(..., description="Payload version")
    timestamp: str = Field(..., description="Payload timestamp")
    statistics: VideoSteganographyStatistics = Field(..., description="Extraction statistics")


class DocumentSteganographyStatistics(BaseModel):
    """Statistics for document steganography operations."""
    
    documentType: str = Field(..., description="Type of document (txt or pdf)")
    pageCount: Optional[int] = Field(None, description="Number of pages (PDF only)")
    textBlocks: Optional[int] = Field(None, description="Number of text blocks (PDF only)")
    imageCount: Optional[int] = Field(None, description="Number of embedded images (PDF only)")
    originalLength: Optional[int] = Field(None, description="Original text length (TXT only)")
    stegoLength: Optional[int] = Field(None, description="Stego text length (TXT only)")
    payloadSize: int = Field(..., description="Payload size in bytes")
    headerSize: int = Field(..., description="Header size in bytes")
    totalBitsEmbedded: Optional[int] = Field(None, description="Total bits used for embedding")
    textPayloadSize: Optional[int] = Field(None, description="Text payload size in bytes (PDF only)")
    imagePayloadSize: Optional[int] = Field(None, description="Image payload size in bytes (PDF only)")
    textCapacityBits: Optional[int] = Field(None, description="Text capacity in bits (PDF only)")
    imageCapacityBits: Optional[int] = Field(None, description="Image capacity in bits (PDF only)")
    totalCapacityBits: Optional[int] = Field(None, description="Total capacity in bits (PDF only)")
    capacityUsedPercent: float = Field(..., description="Percentage of capacity used")
    embeddingMethod: str = Field(default="Hybrid Dual-Layer Document Steganography", description="Steganography method used")
    textMethod: Optional[str] = Field(None, description="Text embedding method used")
    useImages: Optional[bool] = Field(None, description="Whether image steganography was used (PDF only)")
    processingTime: float = Field(..., description="Processing time in seconds")
    debug: Optional[Dict[str, Any]] = Field(None, description="Development debug information")


class DocumentEmbedResponse(BaseModel):
    """Response schema for document steganography embed endpoint."""
    
    success: bool = Field(default=True)
    fileName: str = Field(..., description="Name of the stego document file")
    documentType: str = Field(..., description="Type of document (txt or pdf)")
    statistics: DocumentSteganographyStatistics = Field(..., description="Embedding statistics")
    
    # Internal field for file path (not included in response)
    stegoDocumentPath: Optional[str] = Field(None, exclude=True)


class DocumentExtractResponse(BaseModel):
    """Response schema for document steganography extract endpoint."""
    
    success: bool = Field(default=True)
    encryptedData: str = Field(..., description="Base64 encoded encrypted message")
    algorithm: str = Field(default="AES-256-GCM", description="Encryption algorithm used")
    kdf: str = Field(default="Argon2id", description="Key derivation function used")
    salt: Optional[str] = Field(None, description="Base64 encoded salt (embedded in payload version 2.0+)")
    iv: Optional[str] = Field(None, description="Base64 encoded IV (embedded in payload version 2.0+)")
    version: str = Field(..., description="Payload version")
    timestamp: str = Field(..., description="Payload timestamp")
    statistics: DocumentSteganographyStatistics = Field(..., description="Extraction statistics")


class AudioSteganographyStatistics(BaseModel):
    """Statistics for audio steganography operations."""
    
    duration: float = Field(..., description="Audio duration in seconds")
    channels: int = Field(..., description="Number of audio channels")
    sampleRate: int = Field(..., description="Sample rate in Hz")
    bitDepth: int = Field(..., description="Bit depth per sample")
    totalSamples: int = Field(..., description="Total number of audio samples")
    payloadSize: int = Field(..., description="Payload size in bytes")
    headerSize: int = Field(..., description="Header size in bytes")
    totalBitsEmbedded: int = Field(..., description="Total bits embedded")
    capacityRemaining: int = Field(..., description="Remaining capacity in samples")
    capacityUsedPercent: float = Field(..., description="Percentage of capacity used")
    embeddingMethod: str = Field(default="Randomized WAV LSB", description="Steganography method used")
    processingTime: float = Field(..., description="Processing time in seconds")

class AudioExtractionStatistics(BaseModel):
    """Statistics for audio extraction operations."""

    duration: float
    channels: int
    sampleRate: int
    bitDepth: int
    totalSamples: int

    payloadSize: int
    headerSize: int

    totalBitsExtracted: int

    capacityRemaining: int
    capacityUsedPercent: float

    extractionMethod: str

    processingTime: float

class AudioEmbedResponse(BaseModel):
    """Response schema for audio steganography embed endpoint."""
    
    success: bool = Field(default=True)
    fileName: str = Field(..., description="Name of the stego audio file")
    originalFormat: str = Field(..., description="Original audio format")
    convertedFormat: str = Field(default="WAV", description="Converted audio format")
    statistics: AudioSteganographyStatistics = Field(..., description="Embedding statistics")
    debug: Optional[Dict[str, Any]] = Field(None, description="Development debug information")
    
    # Internal field for file path (not included in response)
    stegoAudioPath: Optional[str] = Field(None, exclude=True)


class AudioExtractResponse(BaseModel):
    """Response schema for audio steganography extract endpoint."""
    
    success: bool = Field(default=True)
    encryptedData: str = Field(..., description="Base64 encoded encrypted message")
    algorithm: str = Field(default="AES-256-GCM", description="Encryption algorithm used")
    kdf: str = Field(default="Argon2id", description="Key derivation function used")
    salt: Optional[str] = Field(None, description="Base64 encoded salt (embedded in payload version 2.0+)")
    iv: Optional[str] = Field(None, description="Base64 encoded IV (embedded in payload version 2.0+)")
    version: str = Field(..., description="Payload version")
    timestamp: str = Field(..., description="Payload timestamp")
    statistics: AudioExtractionStatistics = Field(..., description="Extraction statistics")
    debug: Optional[Dict[str, Any]] = Field(None, description="Development debug information")
