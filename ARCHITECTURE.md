# SecureStego Architecture Documentation

## Overview

SecureStego is a secure steganography platform that enables hiding encrypted messages within various media types (images, videos, audio, documents) using advanced steganographic techniques and Argon2id encryption.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Landing    │  │ Hide Message │  │Extract Message│      │
│  │     Page     │  │     Page     │  │     Page      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            │                                │
│                    ┌───────▼───────┐                        │
│                    │  API Service  │                        │
│                    │  (apiService) │                        │
│                    └───────┬───────┘                        │
└────────────────────────────┼────────────────────────────────┘
                             │ HTTP/REST
┌────────────────────────────┼────────────────────────────────┐
│                    ┌───────▼───────┐                        │
│                    │  FastAPI App  │                        │
│                    │   (main.py)   │                        │
│                    └───────┬───────┘                        │
│                            │                                │
│         ┌──────────────────┼──────────────────┐             │
│         │                  │                  │             │
│  ┌──────▼──────┐  ┌───────▼───────┐  ┌──────▼──────┐        │
│  │ Encryption  │  │ Steganography │  │Verification │        │
│  │   Router    │  │   Routers     │  │   Service   │        │
│  └──────┬──────┘  └───────┬───────┘  └──────┬──────┘        │
│         │                  │                  │             │
│  ┌──────▼──────┐  ┌───────▼───────┐  ┌──────▼──────┐        │
│  │ Crypto      │  │ Steganography │  │ Platform    │        │
│  │ Service     │  │   Services    │  │ Signature   │        │
│  │ (Argon2id)  │  │               │  │ Validator   │        │
│  └──────┬──────┘  └───────┬───────┘  └──────┬──────┘        │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            │                                │
│                    ┌───────▼───────┐                        │
│                    │  Core Utils   │                        │
│                    │ (Logging,     │                        │
│                    │  Exceptions,  │                        │
│                    │  Serializer)  │                        │
│                    └───────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend (React)

#### Directory Structure
```
src/
├── components/
│   ├── layout/           # Layout components (Navbar, Footer)
│   └── ui/               # Reusable UI components
├── pages/                # Page components
│   ├── About.jsx
│   ├── Contact.jsx
│   ├── EmbedMessage.jsx
│   └── ExtractMessage.jsx
├── services/             # API and encryption services
│   ├── apiService.js     # API client
│   └── encryptionService.js
├── utils/                # Utility functions
│   ├── api.js
│   └── crypto.js
├── App.jsx               # Main app with routing
└── main.jsx              # React entry point
```

#### Key Components

**API Service (`apiService.js`)**
- Handles all HTTP requests to backend
- Manages encryption/decryption API calls
- Manages steganography API calls (image, video, audio, document)
- Provides error handling

**Encryption Service (`encryptionService.js`)**
- Manages encryption state
- Evaluates password strength
- Formats bytes and strings
- Provides debug information

### Backend (FastAPI)

#### Directory Structure
```
backend/app/
├── main.py                    # FastAPI application entry point
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration management
├── models/
│   ├── __init__.py
│   └── schemas.py             # Pydantic models for requests/responses
├── routes/
│   ├── encryption.py          # Encryption endpoints
│   ├── steganography.py       # Image steganography endpoints
│   ├── video_steganography.py # Video steganography endpoints
│   ├── audio_steganography.py # Audio steganography endpoints
│   └── document_steganography.py # Document steganography endpoints
├── services/
│   ├── crypto_service.py      # Argon2id + AES-256-GCM encryption
│   ├── steganography_service.py # Image steganography orchestration
│   ├── video_steganography_service.py # Video steganography orchestration
│   ├── audio_steganography_service.py # Audio steganography orchestration
│   ├── document_steganography_service.py # Document steganography orchestration
│   └── platform_verification_service.py # Platform signature operations
├── verification/
│   ├── platform_signature.py  # HMAC-SHA256 signature generation
│   ├── signature_validator.py # Signature validation
│   ├── signature_constants.py # Signature constants
│   └── signature_exceptions.py # Custom exceptions
├── utils/
│   ├── logging_config.py      # Centralized logging configuration
│   ├── exceptions.py          # Custom exceptions
│   ├── payload_serializer.py  # Payload serialization
│   └── payload_deserializer.py # Payload deserialization
├── image_processing/
│   ├── edge_detector.py       # Edge detection for LSB
│   ├── image_converter.py     # Image format conversion
│   ├── image_loader.py        # Image loading utilities
│   └── image_validator.py     # Image validation
├── video_processing/
│   ├── frame_extractor.py     # Video frame extraction
│   ├── frame_rebuilder.py     # Video frame rebuilding
│   ├── video_converter.py     # Video format conversion
│   ├── audio_handler.py       # Audio track handling
│   └── video_validator.py     # Video validation
├── audio_processing/
│   ├── audio_converter.py     # Audio format conversion
│   ├── audio_loader.py        # Audio loading
│   ├── audio_writer.py        # Audio writing
│   └── audio_validator.py     # Audio validation
├── document_processing/
│   ├── pdf_parser.py          # PDF parsing
│   ├── pdf_rebuilder.py       # PDF rebuilding
│   ├── txt_handler.py         # TXT file handling
│   └── document_validator.py  # Document validation
└── steganography/
    ├── edge_lsb_embedder.py   # Edge-based LSB embedding
    ├── edge_lsb_extractor.py  # Edge-based LSB extraction
    ├── video/
    │   ├── frame_selector.py  # Frame selection strategies
    │   ├── dct_embedder.py    # DCT-based embedding
    │   └── dct_extractor.py   # DCT-based extraction
    ├── audio/
    │   ├── sample_selector.py # Sample position generation
    │   ├── audio_lsb_embedder.py # Audio LSB embedding
    │   └── audio_lsb_extractor.py # Audio LSB extraction
    ├── invisible_character_embedder.py # Invisible character embedding
    ├── invisible_character_extractor.py # Invisible character extraction
    ├── structure_embedder.py  # Structure-based embedding
    ├── structure_extractor.py # Structure-based extraction
    └── pdf_image_processor.py # PDF image steganography
```

## Data Flow

### Encryption Flow

```
1. User Input (Frontend)
   - Message: "Secret message"
   - Password: "user_password"

2. API Request (Frontend → Backend)
   POST /api/encryption/encrypt
   {
     "message": "Secret message",
     "password": "user_password"
   }

3. Encryption (Backend - CryptoService)
   - Generate random salt (16 bytes)
   - Derive key using Argon2id:
     * time_cost: 3
     * memory_cost: 65536 KiB (64 MB)
     * parallelism: 4
     * hash_len: 32 bytes (256 bits)
     * salt_len: 16 bytes (128 bits)
   - Generate random IV (12 bytes)
   - Encrypt message using AES-256-GCM
   - Return: ciphertext, salt, iv

4. API Response (Backend → Frontend)
   {
     "success": true,
     "ciphertext": "base64_encoded_ciphertext",
     "salt": "base64_encoded_salt",
     "iv": "base64_encoded_iv",
     "algorithm": "AES-256-GCM",
     "kdf": "Argon2id"
   }
```

### Embedding Flow (Image Example)

```
1. User Input (Frontend)
   - Image file: image.png
   - Encrypted message: (from encryption step)
   - Algorithm: "AES-256-GCM"

2. API Request (Frontend → Backend)
   POST /api/steganography/embed
   - image: image.png
   - encryptedMessage: base64_ciphertext
   - algorithm: "AES-256-GCM"

3. Steganography Service (Backend)
   a. Image Validation
      - Check file format (PNG, JPG, JPEG, HEIC)
      - Check file size limits
   
   b. Image Conversion
      - Convert to PNG (if needed)
      - Ensure lossless format
   
   c. Edge Detection
      - Apply Canny edge detection
      - Identify edge pixels for LSB embedding
   
   d. Payload Serialization
      - Create structured payload:
        {
          "version": "1.0",
          "algorithm": "AES-256-GCM",
          "timestamp": "ISO-8601",
          "encryptedData": "base64_ciphertext"
        }
      - Serialize to binary (JSON + UTF-8)
   
   e. Platform Signature Injection
      - Generate HMAC-SHA256 signature:
        * Platform: "SecureStego"
        * Version: "1.0.0"
        * Media type: "image"
        * Timestamp: current time
        * Payload data: encrypted payload
      - Combine: [signature_length][signature][payload]
   
   f. LSB Embedding
      - Embed combined payload into edge pixels
      - Use 2 LSB per pixel for capacity
      - Store header with payload size
   
   g. File Generation
      - Save stego image to temporary directory
      - Return file path and statistics

4. API Response (Backend → Frontend)
   {
     "success": true,
     "fileName": "stego_image.png",
     "statistics": {
       "imageWidth": 1920,
       "imageHeight": 1080,
       "edgePixels": 450000,
       "payloadSize": 512,
       "capacityUsedPercent": 15.2,
       "processingTime": 2.3
     }
   }

5. File Download (Frontend)
   - GET /api/steganography/download/{filename}
   - User downloads stego image
```

### Extraction Flow (Image Example)

```
1. User Input (Frontend)
   - Stego image file: stego_image.png

2. API Request (Frontend → Backend)
   POST /api/steganography/extract
   - image: stego_image.png

3. Steganography Service (Backend)
   a. Image Validation
      - Check file format
      - Check file size limits
   
   b. LSB Extraction
      - Extract bits from edge pixels
      - Read header to get payload size
      - Extract combined payload
   
   c. Platform Signature Verification
      - Extract signature length (first 4 bytes)
      - Extract signature binary
      - Extract encrypted payload
      - Verify HMAC-SHA256 signature:
        * Check platform identity
        * Check version compatibility
        * Check media type match
        * Reject if invalid
   
   d. Payload Deserialization
      - Deserialize binary to JSON
      - Validate payload structure
      - Extract encrypted data
   
   e. Return encrypted data and metadata

4. API Response (Backend → Frontend)
   {
     "success": true,
     "encryptedData": "base64_ciphertext",
     "algorithm": "AES-256-GCM",
     "version": "1.0",
     "timestamp": "2024-01-15T10:30:00Z",
     "statistics": {...}
   }

5. Decryption (Frontend → Backend)
   POST /api/encryption/decrypt
   {
     "ciphertext": "base64_ciphertext",
     "password": "user_password",
     "salt": "base64_salt",
     "iv": "base64_iv"
   }

6. Decryption (Backend - CryptoService)
   - Derive key using Argon2id (same parameters)
   - Decrypt using AES-256-GCM
   - Return plaintext message

7. Final Response
   {
     "success": true,
     "message": "Secret message"
   }
```

## Security Architecture

### Encryption Layer

**Algorithm**: AES-256-GCM (Authenticated Encryption)
- Key size: 256 bits
- IV size: 96 bits (12 bytes)
- Provides confidentiality and integrity
- Authenticated encryption prevents tampering

**Key Derivation**: Argon2id (Memory-Hard KDF)
- OWASP-recommended parameters:
  - time_cost: 3 iterations
  - memory_cost: 65536 KiB (64 MB)
  - parallelism: 4 threads
  - hash_len: 32 bytes (256 bits)
  - salt_len: 16 bytes (128 bits)
- Resistant to GPU/ASIC attacks
- Resistant to side-channel attacks

### Platform Signature Layer

**Algorithm**: HMAC-SHA256
- Secret key: 64-character hex from environment
- Provides cryptographic integrity
- Binds signature to specific payload
- Includes timestamp for audit trail
- Includes media type for replay protection

**Signature Structure**:
```json
{
  "platform": "SecureStego",
  "version": "1.0.0",
  "signature": "hmac_sha256_hash",
  "createdAt": "ISO-8601 timestamp",
  "mediaType": "image|video|audio|document"
}
```

**Verification Process**:
1. Extract signature from payload
2. Deserialize signature structure
3. Validate platform identity
4. Validate version compatibility
5. Validate media type match
6. Recompute HMAC-SHA256
7. Compare with stored signature
8. Reject if any validation fails

### Steganography Layer

**Image Steganography**: Edge-Based LSB
- Canny edge detection for edge pixel identification
- 2 LSB per pixel for embedding
- Higher capacity in edge regions
- Less perceptible to human eye
- Resistant to statistical analysis

**Video Steganography**: DCT-Based Block
- Frame selection strategies (fixed interval, random, keyframe)
- DCT coefficient modification
- Audio track preservation
- Higher capacity than image steganography

**Audio Steganography**: Randomized LSB
- Password-based sample position generation
- Randomized LSB embedding in WAV
- Resistant to detection
- Preserves audio quality

**Document Steganography**: Hybrid Approach
- TXT: Invisible character or structure-based embedding
- PDF: Hybrid text + image steganography
- Text: Invisible character embedding
- Images: Edge-based LSB for embedded images

## Configuration Management

### Environment Variables

**Backend Configuration** (`.env`):
```env
# Platform Signature
PLATFORM_SECRET_KEY=64_character_hex_key

# Application
APP_NAME=SecureStego
APP_VERSION=1.0.0
DEBUG=False

# API
API_PREFIX=/api
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Argon2id Parameters
ARGON2_TIME_COST=3
ARGON2_MEMORY_COST=65536
ARGON2_PARALLELISM=4
ARGON2_HASH_LEN=32
ARGON2_SALT_LEN=16

# File Upload Limits
MAX_FILE_SIZE_MB=100
MAX_IMAGE_SIZE_MB=50
MAX_VIDEO_SIZE_MB=500
MAX_AUDIO_SIZE_MB=100
MAX_DOCUMENT_SIZE_MB=50
```

**Configuration Loading** (`config/settings.py`):
- Uses Pydantic BaseSettings
- Loads from `.env` file
- Type-safe configuration
- Default values provided
- Case-insensitive

## Logging Architecture

### Centralized Logging

**Logging Configuration** (`utils/logging_config.py`):
- Single source of truth for logging
- Configured at application startup
- Consistent log format across all modules
- Structured logging support

**Log Format**:
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

**Usage**:
```python
from app.utils.logging_config import get_logger

logger = get_logger(__name__)
logger.info("Processing request")
logger.error("Error occurred", exc_info=True)
```

## Exception Handling

### Custom Exceptions

**Base Exception**: `SecureStegoException`
- All custom exceptions inherit from this
- Provides `to_dict()` method for API responses
- Includes error details for debugging

**Exception Hierarchy**:
```
SecureStegoException
├── EncryptionError
│   ├── DecryptionError
│   │   └── InvalidPasswordError
│   └── KeyDerivationError
├── SteganographyError
│   ├── CapacityExceededError
│   ├── InvalidMediaError
│   ├── EmbeddingError
│   └── ExtractionError
│       └── NoHiddenDataError
├── VerificationError
│   └── SignatureVerificationError
│       ├── MissingSignatureError
│       ├── InvalidSignatureError
│       ├── TamperedSignatureError
│       ├── VersionMismatchError
│       ├── PlatformMismatchError
│       └── MediaTypeMismatchError
└── FileProcessingError
    ├── FileValidationError
    │   ├── FileSizeExceededError
    │   └── UnsupportedFormatError
    └── ValidationError
```

## Performance Considerations

### Encryption Performance
- Argon2id parameters balance security and performance
- Memory-hard KDF prevents GPU/ASIC attacks
- AES-256-GCM is hardware-accelerated on modern CPUs

### Steganography Performance
- Edge detection is computationally intensive (images)
- Frame extraction/rebuilding is I/O intensive (videos)
- Audio conversion requires FFmpeg (external dependency)
- PDF processing is memory-intensive

### Optimization Strategies
- Temporary file cleanup after operations
- Parallel processing where possible
- Efficient algorithms for edge detection
- Frame selection strategies to reduce processing

## Scalability Considerations

### Current Limitations
- Single-server deployment
- In-memory processing
- No database persistence
- No distributed processing

### Future Scalability
- Database integration for message storage
- Distributed processing for large files
- Caching layer for frequently accessed data
- Load balancing for API endpoints
- Message queue for async processing

## Security Best Practices

### Implemented
- Environment variables for secrets
- Input validation on all endpoints
- File size limits
- Format validation
- Platform signature verification
- Authenticated encryption
- Memory-hard key derivation
- CORS protection
- Error handling without sensitive data leakage

### Recommendations
- Rate limiting on API endpoints
- Request authentication
- Audit logging
- Secure file storage
- Regular security audits
- Dependency updates
- HTTPS in production
- Secret rotation

## Technology Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- React Router
- Lucide React
- Framer Motion

### Backend
- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Cryptography
- Argon2-cffi
- Pillow (PIL)
- OpenCV (cv2)
- NumPy
- PyMuPDF (fitz)
- Python-multipart
- Python-dotenv

### External Dependencies
- FFmpeg (for audio/video conversion)

## Deployment Architecture

### Development
- Frontend: Vite dev server (localhost:5173)
- Backend: Uvicorn with reload (localhost:8000)
- CORS enabled for development origins

### Production (Recommended)
- Frontend: Static files served by Nginx
- Backend: Uvicorn with Gunicorn workers
- Reverse proxy: Nginx
- Process manager: Systemd or Supervisor
- SSL/TLS termination at Nginx
- Environment variables for secrets
