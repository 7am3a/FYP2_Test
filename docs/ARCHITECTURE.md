# SecureStego Architecture Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Principles](#architecture-principles)
3. [System Architecture](#system-architecture)
4. [Backend Architecture](#backend-architecture)
5. [Frontend Architecture](#frontend-architecture)
6. [Data Flow](#data-flow)
7. [Security Architecture](#security-architecture)
8. [Steganography Architecture](#steganography-architecture)
9. [Scalability Considerations](#scalability-considerations)
10. [Deployment Architecture](#deployment-architecture)

## System Overview

SecureStego is a full-stack web application that implements secure steganography with strong encryption. The system follows a layered architecture with clear separation of concerns between frontend and backend.

### Key Components

- **Frontend**: React-based SPA with Vite
- **Backend**: FastAPI-based REST API
- **Encryption**: Argon2id + AES-256-GCM
- **Steganography**: Multi-media support (image, video, audio, document)
- **Verification**: HMAC-SHA256 platform signature system

## Architecture Principles

### 1. Separation of Concerns

Each layer has a specific responsibility:
- **Presentation Layer**: UI components and user interaction
- **API Layer**: HTTP endpoints and request/response handling
- **Service Layer**: Business logic and orchestration
- **Data Access Layer**: File operations and data persistence
- **Utility Layer**: Shared utilities (logging, exceptions, validation)

### 2. Single Responsibility Principle

Each module/class has one reason to change:
- `CryptoService`: Handles encryption/decryption only
- `SteganographyService`: Orchestrates steganography workflow only
- `PayloadSerializer`: Serializes payloads only
- `PlatformSignature`: Generates/verifies signatures only

### 3. Dependency Injection

Services are injected as dependencies:
- Routes depend on services
- Services depend on utilities
- No direct coupling between layers

### 4. Configuration Management

All configuration is centralized:
- Environment variables via `.env`
- Settings class with validation
- Type-safe configuration access

### 5. Error Handling

Centralized error handling:
- Custom exception hierarchy
- Consistent error responses
- Detailed logging for debugging

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Browser                        │
│                    (React SPA + Vite)                         │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
                         │ REST API
┌────────────────────────▼────────────────────────────────────┐
│                    FastAPI Backend                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Middleware │  │   Routes    │  │  Services   │          │
│  │  - CORS     │  │  - Encryption│  │  - Crypto   │          │
│  │  - Logging  │  │  - Stego     │  │  - Stego    │          │
│  │  - Errors   │  │  - Video     │  │  - Platform │          │
│  └─────────────┘  │  - Audio     │  │  - Payload  │          │
│                   │  - Document  │  └─────────────┘          │
│                   └─────────────┘                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Utils     │  │ Validators  │  │ Repositories│          │
│  │  - Logging  │  │  - File     │  │  - Base      │          │
│  │  - Exceptions│ │  - Payload  │  └─────────────┘          │
│  └─────────────┘  └─────────────┘                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ Processing  │  │Steganography│  │ Verification │          │
│  │  - Image    │  │  - LSB      │  │  - Signature │          │
│  │  - Video    │  │  - DCT      │  │  - HMAC     │          │
│  │  - Audio    │  │  - Random   │  └─────────────┘          │
│  │  - Document │  │  - Hybrid   │                             │
│  └─────────────┘  └─────────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

## Backend Architecture

### Layer Structure

```
backend/app/
├── main.py                    # Application entry point
├── config/                    # Configuration layer
│   └── settings.py           # Environment-based settings
├── models/                    # Data models
│   └── schemas.py            # Pydantic schemas for API
├── routes/                    # API endpoints
│   ├── encryption.py         # Encryption endpoints
│   ├── steganography.py      # Image steganography endpoints
│   ├── video_steganography.py
│   ├── audio_steganography.py
│   └── document_steganography.py
├── services/                  # Business logic
│   ├── crypto_service.py     # Encryption/decryption
│   ├── steganography_service.py
│   ├── video_steganography_service.py
│   ├── audio_steganography_service.py
│   ├── document_steganography_service.py
│   └── platform_verification_service.py
├── repositories/             # Data access (future DB integration)
│   └── base_repository.py
├── middleware/                # Request/response processing
│   ├── error_handler.py
│   └── request_logger.py
├── validators/               # Input validation
│   ├── file_validator.py
│   └── payload_validator.py
├── core/                      # Core application logic
│   └── app_state.py
├── utils/                     # Utilities
│   ├── logging_config.py
│   ├── exceptions.py
│   ├── payload_serializer.py
│   └── payload_deserializer.py
├── verification/             # Platform signature verification
│   ├── platform_signature.py
│   └── signature_constants.py
├── image_processing/         # Image processing modules
├── video_processing/         # Video processing modules
├── audio_processing/         # Audio processing modules
├── document_processing/      # Document processing modules
└── steganography/            # Steganography algorithms
```

### Service Layer Pattern

Each service follows a consistent pattern:

```python
class Service:
    """
    High-level service for operations.
    
    Why this exists:
    - Orchestrates all components
    - Provides clean API for routes
    - Handles error cases
    - Manages cleanup
    """
    
    def __init__(self):
        """Initialize the service."""
        pass
    
    async def operation(self, input_data) -> Dict:
        """
        Complete workflow for operation.
        
        This method:
        1. Validates input
        2. Processes data
        3. Returns result
        
        Returns:
        Dict: Result dictionary
        """
        pass
```

### Exception Hierarchy

```
SecureStegoException (base)
├── EncryptionError
│   ├── KeyDerivationError
│   └── DecryptionError
│       └── InvalidPasswordError
├── SteganographyError
│   ├── CapacityExceededError
│   ├── InvalidMediaError
│   ├── EmbeddingError
│   ├── ExtractionError
│   │   └── NoHiddenDataError
│   ├── ImageSteganographyError
│   │   ├── ImageConversionError
│   │   └── EdgeDetectionError
│   ├── VideoSteganographyError
│   ├── AudioSteganographyError
│   └── DocumentSteganographyError
├── VerificationError
│   ├── SignatureVerificationError
│   ├── MissingSignatureError
│   ├── InvalidSignatureError
│   ├── TamperedSignatureError
│   ├── VersionMismatchError
│   ├── PlatformMismatchError
│   └── MediaTypeMismatchError
├── FileProcessingError
│   ├── FileValidationError
│   ├── FileSizeExceededError
│   └── UnsupportedFormatError
├── ValidationError
│   ├── InvalidPayloadError
│   └── InvalidParameterError
└── ConfigurationError
    ├── MissingConfigurationError
    └── InvalidConfigurationError
```

## Frontend Architecture

### Component Structure

```
frontend/src/
├── components/
│   ├── layout/               # Layout components
│   │   ├── Navbar.jsx
│   │   └── Footer.jsx
│   └── ui/                   # Reusable UI components
├── pages/                    # Page components
│   ├── Landing.jsx
│   ├── HideMessage.jsx
│   ├── ExtractMessage.jsx
│   ├── About.jsx
│   └── Contact.jsx
├── services/                 # API services
│   ├── apiService.js
│   ├── encryptionService.js
│   └── index.js
├── utils/                    # Utilities
│   ├── api.js
│   ├── crypto.js
│   └── index.js
├── hooks/                    # Custom React hooks
│   ├── useEncryption.js
│   ├── useSteganography.js
│   └── index.js
├── context/                  # React context providers
│   ├── EncryptionContext.jsx
│   └── index.js
├── types/                    # Type definitions
│   ├── steganography.js
│   ├── encryption.js
│   └── index.js
├── constants/                # Application constants
│   ├── api.js
│   ├── media.js
│   └── index.js
├── assets/                   # Static assets
├── App.jsx                   # Main app with routing
└── main.jsx                  # React entry point
```

### State Management

State is managed through:
1. **Local State**: Component-level state with `useState`
2. **Context API**: Global state for encryption/decryption
3. **Custom Hooks**: Reusable stateful logic
4. **Service Layer**: API communication and data transformation

### API Communication

All API calls go through `apiService.js`:

```javascript
// Consistent API call pattern
export async function apiRequest(endpoint, options) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}
```

## Data Flow

### Encryption Flow

```
User Input (Message + Password)
    ↓
Frontend Validation
    ↓
POST /api/encryption/encrypt
    ↓
Encryption Route
    ↓
CryptoService.encrypt_message()
    ├─ Argon2id.derive_key(password, salt)
    ├─ AES-256-GCM.encrypt(plaintext, key, iv)
    └─ Return {ciphertext, salt, iv}
    ↓
Response to Frontend
    ↓
Frontend stores encryption data
```

### Steganography Embed Flow

```
Encrypted Message + Media File
    ↓
Frontend Validation
    ↓
POST /api/steganography/embed
    ↓
Steganography Route
    ↓
SteganographyService.embed_message()
    ├─ Validate media
    ├─ Convert to PNG
    ├─ Detect edges (Canny)
    ├─ Serialize payload
    ├─ Inject platform signature
    ├─ Check capacity
    ├─ Embed payload (Edge-based LSB)
    └─ Return stego file info
    ↓
Response to Frontend
    ↓
Frontend downloads stego file
```

### Steganography Extract Flow

```
Stego Media File
    ↓
Frontend Validation
    ↓
POST /api/steganography/extract
    ↓
Steganography Route
    ↓
SteganographyService.extract_message()
    ├─ Validate media
    ├─ Extract payload (Edge-based LSB)
    ├─ Verify platform signature
    ├─ Deserialize payload
    └─ Return encrypted data
    ↓
Response to Frontend
    ↓
POST /api/encryption/decrypt
    ↓
CryptoService.decrypt_message()
    ├─ Argon2id.derive_key(password, salt)
    ├─ AES-256-GCM.decrypt(ciphertext, key, iv)
    └─ Return plaintext
    ↓
Display original message
```

## Security Architecture

### Encryption Layer

```
Plaintext Message
    ↓
Argon2id Key Derivation
    ├─ Input: Password + Salt
    ├─ Parameters: time_cost=3, memory_cost=65536, parallelism=4
    ├─ Output: 256-bit key
    └─ Resistant to GPU/ASIC attacks
    ↓
AES-256-GCM Encryption
    ├─ Input: Plaintext + Key + IV
    ├─ Authenticated encryption (AES-GCM)
    ├─ Output: Ciphertext + Auth Tag
    └─ Provides confidentiality + integrity
    ↓
Base64 Encoding
    ↓
Ciphertext (Base64)
```

### Platform Signature Layer

```
Payload Data
    ↓
Platform Signature Generation
    ├─ HMAC-SHA256
    ├─ Key: platform_secret_key
    ├─ Data: platform + version + mediaType + createdAt + payloadHash
    ├─ Output: 256-bit signature
    └─ Provides authenticity verification
    ↓
Signature Serialization
    ↓
Combined Payload (Signature + Payload)
```

### Security Measures

1. **Key Derivation**: Argon2id (memory-hard, resistant to GPU/ASIC)
2. **Encryption**: AES-256-GCM (authenticated encryption)
3. **Signature**: HMAC-SHA256 (cryptographic verification)
4. **Randomness**: `secrets` module for cryptographically secure random
5. **Input Validation**: All inputs validated before processing
6. **Error Handling**: No sensitive data in error messages
7. **Logging**: Detailed logging for audit trail
8. **CORS**: Configured allowed origins
9. **File Size Limits**: Prevent resource exhaustion
10. **Temporary Files**: Cleanup after processing

## Steganography Architecture

### Image Steganography

```
Image File
    ↓
Validation (PNG, JPG, JPEG, HEIC)
    ↓
Conversion to PNG
    ↓
Edge Detection (Canny)
    ├─ Input: Grayscale image
    ├─ Process: Gaussian blur → Sobel → Threshold → Hysteresis
    └─ Output: Edge map
    ↓
Edge Pixel Selection
    ├─ Select edge pixels for embedding
    └─ Higher capacity in edge regions
    ↓
Payload Serialization JSON → UTF-8 bytes
    ↓
Platform Signature Injection
    ↓
Capacity Check
    ├─ Required: (payload + signature) * 8 bits
    ├─ Available: edge_pixels * 3 bits (RGB)
    └─ Verify: required <= available
    ↓
LSB Embedding
    ├─ Modify LSB of RGB channels
    ├─ Only at edge pixels
    └─ Preserve visual quality
    ↓
Stego Image (PNG)
```

### Video Steganography

```
Video File (MP4, AVI, MOV)
    ↓
Validation
    ↓
Conversion to MP4
    ↓
Audio Extraction
    ↓
Frame Extraction (all frames)
    ↓
Frame Selection
    ├─ Strategy: fixed_interval, uniform, password_derived
    ├─ Select subset of frames
    └─ Balance capacity vs. quality
    ↓
Payload Serialization
    ↓
Platform Signature Injection
    ↓
DCT-Based Embedding
    ├─ Divide frame into 8x8 blocks
    ├─ Apply DCT to each block
    ├─ Modify mid-frequency coefficients
    ├─ Inverse DCT to reconstruct
    └─ Preserve visual quality
    ↓
Video Reassembly
    ↓
Audio Reattachment
    ↓
Stego Video (MP4)
```

### Audio Steganography

```
Audio File (WAV, MP3, M4A, FLAC)
    ↓
Validation
    ↓
Conversion to WAV
    ↓
Sample Loading
    ↓
Randomized Sample Selection
    ├─ Input: Password
    ├─ Process: Hash → PRNG → Sample positions
    ├─ Output: Deterministic random positions
    └─ Same password = same positions
    ↓
Payload Serialization
    ↓
Platform Signature Injection
    ↓
LSB Embedding
    ├─ Modify LSB of audio samples
    ├─ Only at selected positions
    └─ Preserve audio quality
    ↓
Stego Audio (WAV)
```

### Document Steganography

```
Document File (PDF, TXT)
    ↓
Validation
    ↓
Type Detection
    ↓
TXT Processing
    ├─ Invisible Character Embedding
    │   ├─ Zero-width characters
    │   ├─ Randomized positions
    │   └─ Preserves visible text
    └─ Structure-Based Embedding
        ├─ Whitespace modification
        ├─ Line ending changes
        └─ Preserves formatting
    ↓
PDF Processing (Hybrid Dual-Layer)
    ├─ Text Layer
    │   ├─ Invisible character embedding
    │   └─ Structure-based embedding
    └─ Image Layer
        ├─ Extract embedded images
        ├─ Edge-based LSB embedding
        └─ Reinsert modified images
    ↓
PDF Reassembly
    ↓
Stego Document
```

## Scalability Considerations

### Current Limitations

1. **Temporary File Storage**: Uses system temp directory
2. **No Database**: All operations are stateless
3. **Single Instance**: No horizontal scaling
4. **No Caching**: Every request processes from scratch

### Future Scalability Improvements

1. **Persistent Storage**
   - S3 or similar for file storage
   - Database for metadata
   - Redis for caching

2. **Horizontal Scaling**
   - Load balancer
   - Multiple backend instances
   - Shared storage

3. **Queue Processing**
   - Background tasks for heavy operations
   - Celery or similar
   - Progress tracking

4. **CDN Integration**
   - Static asset delivery
   - Stego file distribution
   - Reduced latency

## Deployment Architecture

### Development Environment

```
┌─────────────────┐
│   Developer     │
└────────┬────────┘
         │
┌────────▼────────┐
│  Frontend Dev   │
│  (Vite Dev)     │
│  Port: 5173     │
└────────┬────────┘
         │ Proxy
┌────────▼────────┐
│  Backend Dev    │
│  (Uvicorn)      │
│  Port: 8000     │
└─────────────────┘
```

### Production Environment (Recommended)

```
┌─────────────────┐
│   CDN/CloudFlare│
└────────┬────────┘
         │
┌────────▼────────┐
│  Load Balancer  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│Frontend│ │Backend│
│Server  │ │Server 1│
│(Nginx) │ └───┬───┘
└───┬───┘     │
    │     ┌───▼────┐
    │     │Backend │
    │     │Server 2│
    │     └───┬───┘
    │         │
    │    ┌────▼────┐
    │    │Database │
    │    │(Postgres)│
    │    └────┬────┘
    │         │
    │    ┌────▼────┐
    │    │Redis    │
    │    │Cache    │
    │    └─────────┘
    │
┌───▼─────────────┐
│  S3/Storage     │
└─────────────────┘
```

### Docker Deployment

```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Frontend Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
```

## Monitoring and Logging

### Logging Strategy

- **Structured Logging**: JSON format for parsing
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Log Categories**: By module (encryption, steganography, etc.)
- **Audit Trail**: All operations logged with timestamps
- **Error Tracking**: Detailed error information

### Monitoring Metrics

- **API Response Times**: Per endpoint
- **Error Rates**: By type
- **File Processing Times**: By operation
- **Resource Usage**: CPU, memory, disk
- **Request Volume**: By endpoint

## Conclusion

SecureStego follows a professional, layered architecture with clear separation of concerns. The system is designed for security, maintainability, and future scalability. Each component is well-documented and follows industry best practices.
