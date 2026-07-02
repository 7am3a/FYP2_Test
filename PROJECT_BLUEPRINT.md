# SecureStego Project Blueprint

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Overview](#architecture-overview)
3. [Folder Map](#folder-map)
4. [File Map](#file-map)
5. [Feature Traceability Map](#feature-traceability-map)
6. [End-to-End Flow Mapping](#end-to-end-flow-mapping)

---

## System Overview

### Project Purpose
SecureStego is a production-ready full-stack web application for securely hiding encrypted messages inside images, videos, audio, and documents using advanced steganographic techniques and Argon2id encryption.

### Core Functionality
- **Encryption**: Argon2id key derivation with AES-256-GCM authenticated encryption (OWASP-recommended)
- **Steganography**: 
  - Images: Edge-based LSB (Least Significant Bit) with Canny edge detection
  - Videos: DCT-based block steganography with frame selection strategies
  - Audio: Randomized LSB with password-derived sample positions
  - Documents: Hybrid dual-layer (invisible characters + image steganography)
- **Platform Verification**: HMAC-SHA256 signature system for authenticity verification
- **Multi-Media Support**: PNG, JPG/JPEG, HEIC, MP4, AVI, MOV, WAV, MP3, M4A, FLAC, PDF, TXT

### Technology Stack

#### Frontend
- React 18 - Modern React with hooks
- Vite - Fast build tool and dev server
- Tailwind CSS - Utility-first CSS framework
- React Router - Client-side routing
- Lucide React - Modern icon library
- Framer Motion - Animation library

#### Backend
- Python 3.8+ - Programming language
- FastAPI - Modern web framework
- Uvicorn - ASGI server
- Pydantic - Data validation
- Cryptography - Encryption library
- Argon2-cffi - Password hashing
- Pillow (PIL) - Image processing
- OpenCV (cv2) - Computer vision
- NumPy - Numerical computing
- PyMuPDF (fitz) - PDF processing
- Python-multipart - File upload handling
- Python-dotenv - Environment variables

### Security Architecture

#### Encryption Layer
- **Algorithm**: AES-256-GCM (Authenticated Encryption)
  - Key size: 256 bits
  - IV size: 96 bits (12 bytes)
  - Provides confidentiality and integrity
- **Key Derivation**: Argon2id (Memory-Hard KDF)
  - time_cost: 3 iterations
  - memory_cost: 65536 KiB (64 MB)
  - parallelism: 4 threads
  - hash_len: 32 bytes (256 bits)
  - salt_len: 16 bytes (128 bits)

#### Platform Signature Layer
- **Algorithm**: HMAC-SHA256
- Secret key: 64-character hex from environment
- Provides cryptographic integrity
- Binds signature to specific payload
- Includes timestamp for audit trail
- Includes media type for replay protection

#### Steganography Layer
- **Image**: Edge-Based LSB with Canny edge detection
- **Video**: DCT-Based Block with frame selection
- **Audio**: Randomized LSB with password-derived positions
- **Document**: Hybrid text/image steganography

---

## Architecture Overview

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

---

## Folder Map

### Root Level

#### `/frontend/`
**Purpose**: React frontend application

**Responsibilities**:
- User interface for encryption and steganography operations
- Client-side API communication
- User input validation
- File upload handling
- Result display

**Connected Modules**:
- Backend API (via HTTP requests)
- Encryption service (via API)
- Steganography services (via API)

**Dependencies**:
- React, Vite, Tailwind CSS
- React Router, Lucide React, Framer Motion

---

#### `/backend/`
**Purpose**: FastAPI backend application

**Responsibilities**:
- API endpoint implementation
- Encryption/decryption operations
- Steganography processing
- Platform signature verification
- File processing and validation

**Connected Modules**:
- Frontend (serves API)
- All processing modules
- Configuration management

**Dependencies**:
- FastAPI, Uvicorn, Pydantic
- Cryptography, Argon2-cffi
- Pillow, OpenCV, NumPy
- PyMuPDF, Python-multipart

---

#### `/docs/`
**Purpose**: Project documentation

**Responsibilities**:
- API documentation
- Architecture documentation
- Developer guide

**Connected Modules**:
- Entire project

---

#### `/tests/`
**Purpose**: End-to-end tests

**Responsibilities**:
- Integration testing
- Workflow validation

**Connected Modules**:
- Frontend and Backend

---

### Frontend Structure

#### `/frontend/src/components/layout/`
**Purpose**: Layout components

**Responsibilities**:
- Navigation bar
- Footer
- Page structure

**Used By**:
- All pages

**Files**:
- `Navbar.jsx` - Navigation menu
- `Footer.jsx` - Footer component

---

#### `/frontend/src/components/ui/`
**Purpose**: Reusable UI components

**Responsibilities**:
- Button, Card, FileUpload
- PasswordInput, Textarea
- DebugPanel

**Used By**:
- HideMessage page
- ExtractMessage page
- All pages with UI elements

**Files**:
- `Button.jsx` - Reusable button component
- `Card.jsx` - Card container component
- `FileUpload.jsx` - File upload component
- `PasswordInput.jsx` - Password input with strength indicator
- `Textarea.jsx` - Text area component
- `DebugPanel.jsx` - Debug information display

---

#### `/frontend/src/pages/`
**Purpose**: Page components

**Responsibilities**:
- Landing page
- Hide message page
- Extract message page
- About page
- Contact page

**Used By**:
- App.jsx (routing)

**Files**:
- `Landing.jsx` - Home page with hero section
- `HideMessage.jsx` - Encryption and embedding workflow
- `ExtractMessage.jsx` - Extraction and decryption workflow
- `About.jsx` - Information about the project
- `Contact.jsx` - Contact form

---

#### `/frontend/src/services/`
**Purpose**: API and business logic services

**Responsibilities**:
- API communication
- Encryption state management
- Password strength evaluation

**Used By**:
- HideMessage page
- ExtractMessage page
- All pages needing API access

**Files**:
- `apiService.js` - HTTP API client
- `encryptionService.js` - Encryption state management
- `index.js` - Service exports

---

#### `/frontend/src/utils/`
**Purpose**: Utility functions

**Responsibilities**:
- API helpers
- Cryptographic utilities
- Data formatting

**Used By**:
- Services
- Pages

**Files**:
- `api.js` - API request helpers
- `crypto.js` - Web Crypto API utilities
- `index.js` - Utility exports

---

#### `/frontend/src/hooks/`
**Purpose**: Custom React hooks

**Responsibilities**:
- Encryption state management
- Steganography state management

**Used By**:
- HideMessage page
- ExtractMessage page

**Files**:
- `useEncryption.js` - Encryption operations hook
- `useSteganography.js` - Steganography operations hook
- `index.js` - Hook exports

---

#### `/frontend/src/types/`
**Purpose**: Type definitions

**Responsibilities**:
- Encryption types
- Steganography types

**Used By**:
- Services
- Hooks

**Files**:
- `encryption.js` - Encryption-related types
- `steganography.js` - Steganography-related types
- `index.js` - Type exports

---

#### `/frontend/src/constants/`
**Purpose**: Application constants

**Responsibilities**:
- API endpoints
- Configuration values

**Used By**:
- Services
- Utils

**Files**:
- `api.js` - API endpoint constants
- `encryption.js` - Encryption constants
- `index.js` - Constant exports

---

#### `/frontend/src/context/`
**Purpose**: React context providers

**Responsibilities**:
- Global state management

**Used By**:
- App.jsx

**Files**:
- (Currently minimal, for future expansion)

---

#### `/frontend/src/assets/`
**Purpose**: Static assets

**Responsibilities**:
- Images
- Icons
- Static files

**Used By**:
- Components
- Pages

---

### Backend Structure

#### `/backend/app/config/`
**Purpose**: Configuration management

**Responsibilities**:
- Environment variable loading
- Application settings
- Security parameters

**Used By**:
- All backend modules

**Files**:
- `settings.py` - Pydantic settings class
- `__init__.py` - Config exports

**Configuration**:
- platform_secret_key
- argon2 parameters (time_cost, memory_cost, parallelism, hash_len, salt_len)
- API prefix
- CORS origins
- File size limits
- Logging configuration

---

#### `/backend/app/models/`
**Purpose**: Pydantic models/schemas

**Responsibilities**:
- Request/response schemas
- Data validation
- Type definitions

**Used By**:
- All routes
- All services

**Files**:
- `schemas.py` - All Pydantic models
- `__init__.py` - Model exports

**Models**:
- EncryptRequest, EncryptResponse
- DecryptRequest, DecryptResponse
- EmbedResponse, ExtractResponse
- VideoEmbedResponse, VideoExtractResponse
- AudioEmbedResponse, AudioExtractResponse
- DocumentEmbedResponse, DocumentExtractResponse
- Statistics models for each media type

---

#### `/backend/app/routes/`
**Purpose**: API endpoint definitions

**Responsibilities**:
- HTTP request handling
- Input validation
- Response formatting
- Error handling

**Used By**:
- main.py (router registration)

**Files**:
- `encryption.py` - Encryption endpoints
- `steganography.py` - Image steganography endpoints
- `video_steganography.py` - Video steganography endpoints
- `audio_steganography.py` - Audio steganography endpoints
- `document_steganography.py` - Document steganography endpoints
- `__init__.py` - Router exports

---

#### `/backend/app/services/`
**Purpose**: Business logic layer

**Responsibilities**:
- Encryption/decryption operations
- Steganography orchestration
- Platform verification
- High-level workflow coordination

**Used By**:
- Routes (call services)
- Other services (composition)

**Files**:
- `crypto_service.py` - Argon2id + AES-256-GCM encryption
- `steganography_service.py` - Image steganography orchestration
- `video_steganography_service.py` - Video steganography orchestration
- `audio_steganography_service.py` - Audio steganography orchestration
- `document_steganography_service.py` - Document steganography orchestration
- `platform_verification_service.py` - Platform signature operations
- `__init__.py` - Service exports

---

#### `/backend/app/image_processing/`
**Purpose**: Image processing modules

**Responsibilities**:
- Edge detection
- Image conversion
- Image loading
- Image validation

**Used By**:
- steganography_service.py
- edge_lsb_embedder.py
- edge_lsb_extractor.py

**Files**:
- `edge_detector.py` - Canny edge detection
- `image_converter.py` - Format conversion (PNG)
- `image_loader.py` - Image loading utilities
- `image_validator.py` - Image validation
- `__init__.py` - Module exports

---

#### `/backend/app/video_processing/`
**Purpose**: Video processing modules

**Responsibilities**:
- Frame extraction
- Frame rebuilding
- Video conversion
- Audio track handling
- Video validation

**Used By**:
- video_steganography_service.py
- video/dct_embedder.py
- video/dct_extractor.py

**Files**:
- `frame_extractor.py` - Video frame extraction
- `frame_rebuilder.py` - Video frame rebuilding
- `video_converter.py` - Video format conversion
- `audio_handler.py` - Audio track handling
- `video_validator.py` - Video validation
- `__init__.py` - Module exports

---

#### `/backend/app/audio_processing/`
**Purpose**: Audio processing modules

**Responsibilities**:
- Audio conversion
- Audio loading
- Audio writing
- Audio validation

**Used By**:
- audio_steganography_service.py
- audio/audio_lsb_embedder.py
- audio/audio_lsb_extractor.py

**Files**:
- `audio_converter.py` - Audio format conversion
- `audio_loader.py` - Audio loading
- `audio_writer.py` - Audio writing
- `audio_validator.py` - Audio validation
- `__init__.py` - Module exports

---

#### `/backend/app/document_processing/`
**Purpose**: Document processing modules

**Responsibilities**:
- PDF parsing
- PDF rebuilding
- TXT file handling
- Document validation

**Used By**:
- document_steganography_service.py
- invisible_character_embedder.py
- structure_embedder.py
- pdf_image_processor.py

**Files**:
- `pdf_parser.py` - PDF parsing
- `pdf_rebuilder.py` - PDF rebuilding
- `txt_handler.py` - TXT file handling
- `document_validator.py` - Document validation
- `__init__.py` - Module exports

---

#### `/backend/app/steganography/`
**Purpose**: Steganography algorithms

**Responsibilities**:
- Edge-based LSB embedding/extraction
- DCT-based video steganography
- Audio LSB steganography
- Document steganography

**Used By**:
- steganography_service.py
- video_steganography_service.py
- audio_steganography_service.py
- document_steganography_service.py

**Files**:
- `edge_lsb_embedder.py` - Edge-based LSB embedding
- `edge_lsb_extractor.py` - Edge-based LSB extraction
- `invisible_character_embedder.py` - Invisible character embedding
- `invisible_character_extractor.py` - Invisible character extraction
- `structure_embedder.py` - Structure-based embedding
- `structure_extractor.py` - Structure-based extraction
- `pdf_image_processor.py` - PDF image steganography
- `__init__.py` - Module exports

---

#### `/backend/app/steganography/video/`
**Purpose**: Video steganography algorithms

**Responsibilities**:
- Frame selection strategies
- DCT-based embedding
- DCT-based extraction
- DCT transform utilities

**Used By**:
- video_steganography_service.py

**Files**:
- `frame_selector.py` - Frame selection strategies
- `dct_embedder.py` - DCT-based embedding
- `dct_extractor.py` - DCT-based extraction
- `dct_transform.py` - DCT transform utilities
- `__init__.py` - Module exports

---

#### `/backend/app/steganography/audio/`
**Purpose**: Audio steganography algorithms

**Responsibilities**:
- Sample position generation
- Audio LSB embedding
- Audio LSB extraction

**Used By**:
- audio_steganography_service.py

**Files**:
- `sample_selector.py` - Sample position generation
- `audio_lsb_embedder.py` - Audio LSB embedding
- `audio_lsb_extractor.py` - Audio LSB extraction
- `__init__.py` - Module exports

---

#### `/backend/app/verification/`
**Purpose**: Platform signature verification

**Responsibilities**:
- Platform signature generation
- Signature validation
- Signature constants
- Signature exceptions

**Used By**:
- platform_verification_service.py
- All steganography services

**Files**:
- `platform_signature.py` - HMAC-SHA256 signature generation
- `signature_validator.py` - Signature validation
- `signature_constants.py` - Signature constants
- `signature_exceptions.py` - Custom exceptions
- `__init__.py` - Module exports

---

#### `/backend/app/utils/`
**Purpose**: Utility modules

**Responsibilities**:
- Logging configuration
- Custom exceptions
- Payload serialization
- Payload deserialization

**Used By**:
- All backend modules

**Files**:
- `logging_config.py` - Centralized logging
- `exceptions.py` - Custom exceptions
- `payload_serializer.py` - Payload serialization
- `payload_deserializer.py` - Payload deserialization
- `__init__.py` - Utility exports

---

#### `/backend/app/validators/`
**Purpose**: Input validation

**Responsibilities**:
- Request validation
- Data validation

**Used By**:
- Routes

**Files**:
- (Currently minimal, for future expansion)

---

#### `/backend/app/middleware/`
**Purpose**: Custom middleware

**Responsibilities**:
- Request processing
- Response processing

**Used By**:
- main.py

**Files**:
- (Currently minimal, for future expansion)

---

#### `/backend/app/repositories/`
**Purpose**: Data access layer

**Responsibilities**:
- Database operations
- Data persistence

**Used By**:
- Services

**Files**:
- (Currently minimal, for future database integration)

---

#### `/backend/app/core/`
**Purpose**: Core application logic

**Responsibilities**:
- Application initialization
- Core utilities

**Used By**:
- main.py

**Files**:
- (Currently minimal, for future expansion)

---

#### `/backend/app/security/`
**Purpose**: Security utilities

**Responsibilities**:
- Security helpers
- Security validation

**Used By**:
- Services
- Routes

**Files**:
- (Currently minimal, for future expansion)

---

## File Map

### Frontend Files

#### `frontend/src/App.jsx`
**Purpose**: Main React application with routing configuration

**Used By**:
- main.jsx (entry point)

**Dependencies**:
- React Router
- All page components
- Layout components

**Related Features**:
- All features (routing)

**Connected API**: None (routing only)

---

#### `frontend/src/main.jsx`
**Purpose**: React entry point

**Used By**:
- Browser (via index.html)

**Dependencies**:
- React
- App.jsx

**Related Features**:
- Application initialization

**Connected API**: None

---

#### `frontend/src/services/apiService.js`
**Purpose**: HTTP API client for backend communication

**Used By**:
- HideMessage page
- ExtractMessage page
- useEncryption hook
- useSteganography hook

**Dependencies**:
- None (uses fetch API)

**Related Features**:
- Encryption
- Decryption
- Image steganography
- Video steganography
- Audio steganography
- Document steganography

**Connected API**:
- POST /api/encryption/encrypt
- POST /api/encryption/decrypt
- POST /api/steganography/embed
- POST /api/steganography/extract
- GET /api/steganography/download/{filename}
- GET /api/encryption/health
- GET /api/steganography/health

---

#### `frontend/src/services/encryptionService.js`
**Purpose**: Encryption state management and utilities

**Used By**:
- HideMessage page
- ExtractMessage page

**Dependencies**:
- None

**Related Features**:
- Encryption state tracking
- Password strength evaluation
- Debug information generation

**Connected API**: None (state management only)

---

#### `frontend/src/utils/api.js`
**Purpose**: API request helpers (legacy, not actively used)

**Used By**:
- (Currently minimal)

**Dependencies**:
- None

**Related Features**:
- API communication

**Connected API**: All endpoints

---

#### `frontend/src/utils/crypto.js`
**Purpose**: Web Crypto API utilities (client-side encryption)

**Used By**:
- (Currently minimal - encryption moved to backend)

**Dependencies**:
- Web Crypto API

**Related Features**:
- Client-side encryption (legacy)

**Connected API**: None

---

#### `frontend/src/hooks/useEncryption.js`
**Purpose**: Custom hook for encryption operations

**Used By**:
- HideMessage page
- ExtractMessage page

**Dependencies**:
- apiService.js

**Related Features**:
- Encryption
- Decryption

**Connected API**:
- POST /api/encryption/encrypt
- POST /api/encryption/decrypt

---

#### `frontend/src/hooks/useSteganography.js`
**Purpose**: Custom hook for steganography operations

**Used By**:
- HideMessage page
- ExtractMessage page

**Dependencies**:
- apiService.js

**Related Features**:
- Image steganography
- File download

**Connected API**:
- POST /api/steganography/embed
- POST /api/steganography/extract
- GET /api/steganography/download/{filename}

---

#### `frontend/src/pages/HideMessage.jsx`
**Purpose**: Encryption and embedding workflow page

**Used By**:
- App.jsx (routing)

**Dependencies**:
- apiService.js
- encryptionService.js
- UI components

**Related Features**:
- Message encryption
- Image steganography embedding
- File download

**Connected API**:
- POST /api/encryption/encrypt
- POST /api/steganography/embed
- GET /api/steganography/download/{filename}

---

#### `frontend/src/pages/ExtractMessage.jsx`
**Purpose**: Extraction and decryption workflow page

**Used By**:
- App.jsx (routing)

**Dependencies**:
- apiService.js
- encryptionService.js
- UI components

**Related Features**:
- Image steganography extraction
- Message decryption

**Connected API**:
- POST /api/steganography/extract
- POST /api/encryption/decrypt

---

### Backend Files

#### `backend/app/main.py`
**Purpose**: FastAPI application entry point

**Used By**:
- Uvicorn (server startup)

**Dependencies**:
- All routers
- Configuration
- Logging

**Related Features**:
- All features (application initialization)

**Connected API**: All endpoints (router registration)

---

#### `backend/app/config/settings.py`
**Purpose**: Application configuration management

**Used By**:
- All backend modules

**Dependencies**:
- Pydantic Settings
- Environment variables

**Related Features**:
- All features (configuration)

**Connected API**: None (configuration only)

---

#### `backend/app/models/schemas.py`
**Purpose**: Pydantic models for request/response validation

**Used By**:
- All routes
- All services

**Dependencies**:
- Pydantic

**Related Features**:
- All features (data validation)

**Connected API**: All endpoints (request/response schemas)

---

#### `backend/app/routes/encryption.py`
**Purpose**: Encryption API endpoints

**Used By**:
- main.py (router registration)

**Dependencies**:
- crypto_service.py
- models/schemas.py

**Related Features**:
- Message encryption
- Message decryption

**Connected API**:
- POST /api/encryption/encrypt
- POST /api/encryption/decrypt
- GET /api/encryption/health

---

#### `backend/app/routes/steganography.py`
**Purpose**: Image steganography API endpoints

**Used By**:
- main.py (router registration)

**Dependencies**:
- steganography_service.py
- models/schemas.py

**Related Features**:
- Image steganography embedding
- Image steganography extraction
- File download

**Connected API**:
- POST /api/steganography/embed
- POST /api/steganography/extract
- GET /api/steganography/download/{filename}
- GET /api/steganography/health

---

#### `backend/app/routes/video_steganography.py`
**Purpose**: Video steganography API endpoints

**Used By**:
- main.py (router registration)

**Dependencies**:
- video_steganography_service.py
- models/schemas.py

**Related Features**:
- Video steganography embedding
- Video steganography extraction
- File download

**Connected API**:
- POST /api/video/embed
- POST /api/video/extract
- GET /api/video/download/{filename}
- GET /api/video/health

---

#### `backend/app/routes/audio_steganography.py`
**Purpose**: Audio steganography API endpoints

**Used By**:
- main.py (router registration)

**Dependencies**:
- audio_steganography_service.py
- models/schemas.py

**Related Features**:
- Audio steganography embedding
- Audio steganography extraction
- File download

**Connected API**:
- POST /api/audio/embed
- POST /api/audio/extract
- GET /api/audio/download/{filename}
- GET /api/audio/health

---

#### `backend/app/routes/document_steganography.py`
**Purpose**: Document steganography API endpoints

**Used By**:
- main.py (router registration)

**Dependencies**:
- document_steganography_service.py
- models/schemas.py

**Related Features**:
- Document steganography embedding
- Document steganography extraction
- File download

**Connected API**:
- POST /api/document/embed
- POST /api/document/extract
- GET /api/document/download/{filename}
- GET /api/document/health

---

#### `backend/app/services/crypto_service.py`
**Purpose**: Argon2id + AES-256-GCM encryption service

**Used By**:
- encryption.py (routes)

**Dependencies**:
- argon2-cffi
- cryptography
- settings.py

**Related Features**:
- Message encryption
- Message decryption

**Connected API**: None (service layer)

---

#### `backend/app/services/steganography_service.py`
**Purpose**: Image steganography orchestration service

**Used By**:
- steganography.py (routes)

**Dependencies**:
- image_processing modules
- steganography modules
- verification modules
- utils modules

**Related Features**:
- Image steganography embedding
- Image steganography extraction
- Platform signature verification

**Connected API**: None (service layer)

---

#### `backend/app/services/video_steganography_service.py`
**Purpose**: Video steganography orchestration service

**Used By**:
- video_steganography.py (routes)

**Dependencies**:
- video_processing modules
- steganography/video modules
- verification modules
- utils modules

**Related Features**:
- Video steganography embedding
- Video steganography extraction
- Platform signature verification

**Connected API**: None (service layer)

---

#### `backend/app/services/audio_steganography_service.py`
**Purpose**: Audio steganography orchestration service

**Used By**:
- audio_steganography.py (routes)

**Dependencies**:
- audio_processing modules
- steganography/audio modules
- verification modules
- utils modules

**Related Features**:
- Audio steganography embedding
- Audio steganography extraction
- Platform signature verification

**Connected API**: None (service layer)

---

#### `backend/app/services/document_steganography_service.py`
**Purpose**: Document steganography orchestration service

**Used By**:
- document_steganography.py (routes)

**Dependencies**:
- document_processing modules
- steganography modules
- verification modules
- utils modules

**Related Features**:
- Document steganography embedding
- Document steganography extraction
- Platform signature verification

**Connected API**: None (service layer)

---

#### `backend/app/services/platform_verification_service.py`
**Purpose**: Platform signature verification service

**Used By**:
- All steganography services

**Dependencies**:
- verification modules
- utils modules

**Related Features**:
- Platform signature generation
- Platform signature verification
- Platform signature extraction

**Connected API**: None (service layer)

---

#### `backend/app/steganography/edge_lsb_embedder.py`
**Purpose**: Edge-based LSB embedding algorithm

**Used By**:
- steganography_service.py

**Dependencies**:
- OpenCV
- NumPy

**Related Features**:
- Image steganography embedding

**Connected API**: None (algorithm layer)

---

#### `backend/app/steganography/edge_lsb_extractor.py`
**Purpose**: Edge-based LSB extraction algorithm

**Used By**:
- steganography_service.py

**Dependencies**:
- OpenCV
- NumPy

**Related Features**:
- Image steganography extraction

**Connected API**: None (algorithm layer)

---

#### `backend/app/image_processing/edge_detector.py`
**Purpose**: Canny edge detection

**Used By**:
- steganography_service.py
- edge_lsb_embedder.py
- edge_lsb_extractor.py

**Dependencies**:
- OpenCV

**Related Features**:
- Image steganography (edge detection)

**Connected API**: None (processing layer)

---

#### `backend/app/verification/platform_signature.py`
**Purpose**: HMAC-SHA256 signature generation

**Used By**:
- platform_verification_service.py

**Dependencies**:
- hmac
- hashlib
- settings.py

**Related Features**:
- Platform signature generation

**Connected API**: None (verification layer)

---

#### `backend/app/utils/payload_serializer.py`
**Purpose**: Payload serialization for embedding

**Used By**:
- steganography_service.py
- All steganography services

**Dependencies**:
- json

**Related Features**:
- All steganography features (payload creation)

**Connected API**: None (utility layer)

---

#### `backend/app/utils/payload_deserializer.py`
**Purpose**: Payload deserialization for extraction

**Used By**:
- steganography_service.py
- All steganography services

**Dependencies**:
- json

**Related Features**:
- All steganography features (payload extraction)

**Connected API**: None (utility layer)

---

## Feature Traceability Map

### Feature: Message Encryption

**Purpose**: Encrypt plaintext messages using Argon2id key derivation and AES-256-GCM

**Frontend Files**:
- `frontend/src/pages/HideMessage.jsx`
- `frontend/src/services/apiService.js`
- `frontend/src/hooks/useEncryption.js`

**Backend Files**:
- `backend/app/routes/encryption.py`
- `backend/app/services/crypto_service.py`
- `backend/app/models/schemas.py`

**Services**:
- crypto_service.py

**Routes**:
- POST /api/encryption/encrypt
- POST /api/encryption/decrypt
- GET /api/encryption/health

**Utilities**:
- None

**Database Tables**:
- None (no database)

**Configuration**:
- backend/.env
  - argon2_time_cost
  - argon2_memory_cost
  - argon2_parallelism
  - argon2_hash_len
  - argon2_salt_len

**Dependencies**:
- argon2-cffi
- cryptography

---

### Feature: Message Decryption

**Purpose**: Decrypt encrypted messages using Argon2id key derivation and AES-256-GCM

**Frontend Files**:
- `frontend/src/pages/ExtractMessage.jsx`
- `frontend/src/services/apiService.js`
- `frontend/src/hooks/useEncryption.js`

**Backend Files**:
- `backend/app/routes/encryption.py`
- `backend/app/services/crypto_service.py`
- `backend/app/models/schemas.py`

**Services**:
- crypto_service.py

**Routes**:
- POST /api/encryption/decrypt

**Utilities**:
- None

**Database Tables**:
- None

**Configuration**:
- backend/.env
  - argon2_time_cost
  - argon2_memory_cost
  - argon2_parallelism
  - argon2_hash_len
  - argon2_salt_len

**Dependencies**:
- argon2-cffi
- cryptography

---

### Feature: Image Steganography (Embed)

**Purpose**: Embed encrypted messages into images using edge-based LSB

**Frontend Files**:
- `frontend/src/pages/HideMessage.jsx`
- `frontend/src/services/apiService.js`
- `frontend/src/hooks/useSteganography.js`

**Backend Files**:
- `backend/app/routes/steganography.py`
- `backend/app/services/steganography_service.py`
- `backend/app/steganography/edge_lsb_embedder.py`
- `backend/app/image_processing/edge_detector.py`
- `backend/app/image_processing/image_converter.py`
- `backend/app/image_processing/image_validator.py`
- `backend/app/verification/platform_signature.py`
- `backend/app/utils/payload_serializer.py`
- `backend/app/models/schemas.py`

**Services**:
- steganography_service.py
- platform_verification_service.py

**Routes**:
- POST /api/steganography/embed
- GET /api/steganography/download/{filename}

**Utilities**:
- payload_serializer.py
- logging_config.py

**Database Tables**:
- None

**Configuration**:
- backend/.env
  - max_image_size_mb
  - platform_secret_key

**Dependencies**:
- OpenCV
- Pillow
- NumPy

---

### Feature: Image Steganography (Extract)

**Purpose**: Extract encrypted messages from images using edge-based LSB

**Frontend Files**:
- `frontend/src/pages/ExtractMessage.jsx`
- `frontend/src/services/apiService.js`
- `frontend/src/hooks/useSteganography.js`

**Backend Files**:
- `backend/app/routes/steganography.py`
- `backend/app/services/steganography_service.py`
- `backend/app/steganography/edge_lsb_extractor.py`
- `backend/app/image_processing/edge_detector.py`
- `backend/app/verification/signature_validator.py`
- `backend/app/utils/payload_deserializer.py`
- `backend/app/models/schemas.py`

**Services**:
- steganography_service.py
- platform_verification_service.py

**Routes**:
- POST /api/steganography/extract

**Utilities**:
- payload_deserializer.py
- logging_config.py

**Database Tables**:
- None

**Configuration**:
- backend/.env
  - platform_secret_key

**Dependencies**:
- OpenCV
- Pillow
- NumPy

---

### Feature: Video Steganography (Embed)

**Purpose**: Embed encrypted messages into videos using DCT-based steganography

**Frontend Files**:
- (Currently not implemented in frontend)

**Backend Files**:
- `backend/app/routes/video_steganography.py`
- `backend/app/services/video_steganography_service.py`
- `backend/app/steganography/video/dct_embedder.py`
- `backend/app/steganography/video/frame_selector.py`
- `backend/app/video_processing/frame_extractor.py`
- `backend/app/video_processing/frame_rebuilder.py`
- `backend/app/video_processing/video_converter.py`
- `backend/app/video_processing/video_validator.py`
- `backend/app/video_processing/audio_handler.py`
- `backend/app/verification/platform_signature.py`
- `backend/app/utils/payload_serializer.py`
- `backend/app/models/schemas.py`

**Services**:
- video_steganography_service.py
- platform_verification_service.py

**Routes**:
- POST /api/video/embed
- GET /api/video/download/{filename}

**Utilities**:
- payload_serializer.py
- logging_config.py

**Database Tables**:
- None

**Configuration**:
- backend/.env
  - max_video_size_mb
  - platform_secret_key

**Dependencies**:
- OpenCV
- NumPy
- FFmpeg (external)

---

### Feature: Video Steganography (Extract)

**Purpose**: Extract encrypted messages from videos using DCT-based steganography

**Frontend Files**:
- (Currently not implemented in frontend)

**Backend Files**:
- `backend/app/routes/video_steganography.py`
- `backend/app/services/video_steganography_service.py`
- `backend/app/steganography/video/dct_extractor.py`
- `backend/app/steganography/video/frame_selector.py`
- `backend/app/video_processing/frame_extractor.py`
- `backend/app/verification/signature_validator.py`
- `backend/app/utils/payload_deserializer.py`
- `backend/app/models/schemas.py`

**Services**:
- video_steganography_service.py
- platform_verification_service.py

**Routes**:
- POST /api/video/extract

**Utilities**:
- payload_deserializer.py
- logging_config.py

**Database Tables**:
- None

**Configuration**:
- backend/.env
  - platform_secret_key

**Dependencies**:
- OpenCV
- NumPy
- FFmpeg (external)

---

### Feature: Audio Steganography (Embed)

**Purpose**: Embed encrypted messages into audio using randomized LSB

**Frontend Files**:
- (Currently not implemented in frontend)

**Backend Files**:
- `backend/app/routes/audio_steganography.py`
- `backend/app/services/audio_steganography_service.py`
- `backend/app/steganography/audio/audio_lsb_embedder.py`
- `backend/app/steganography/audio/sample_selector.py`
- `backend/app/audio_processing/audio_converter.py`
- `backend/app/audio_processing/audio_loader.py`
- `backend/app/audio_processing/audio_writer.py`
- `backend/app/audio_processing/audio_validator.py`
- `backend/app/verification/platform_signature.py`
- `backend/app/utils/payload_serializer.py`
- `backend/app/models/schemas.py`

**Services**:
- audio_steganography_service.py
- platform_verification_service.py

**Routes**:
- POST /api/audio/embed
- GET /api/audio/download/{filename}

**Utilities**:
- payload_serializer.py
- logging_config.py

**Database Tables**:
- None

**Configuration**:
- backend/.env
  - max_audio_size_mb
  - platform_secret_key

**Dependencies**:
- NumPy
- FFmpeg (external)

---

### Feature: Audio Steganography (Extract)

**Purpose**: Extract encrypted messages from audio using randomized LSB

**Frontend Files**:
- (Currently not implemented in frontend)

**Backend Files**:
- `backend/app/routes/audio_steganography.py`
- `backend/app/services/audio_steganography_service.py`
- `backend/app/steganography/audio/audio_lsb_extractor.py`
- `backend/app/steganography/audio/sample_selector.py`
- `backend/app/audio_processing/audio_loader.py`
- `backend/app/verification/signature_validator.py`
- `backend/app/utils/payload_deserializer.py`
- `backend/app/models/schemas.py`

**Services**:
- audio_steganography_service.py
- platform_verification_service.py

**Routes**:
- POST /api/audio/extract

**Utilities**:
- payload_deserializer.py
- logging_config.py

**Database Tables**:
- None

**Configuration**:
- backend/.env
  - platform_secret_key

**Dependencies**:
- NumPy
- FFmpeg (external)

---

### Feature: Document Steganography (Embed)

**Purpose**: Embed encrypted messages into documents using hybrid steganography

**Frontend Files**:
- (Currently not implemented in frontend)

**Backend Files**:
- `backend/app/routes/document_steganography.py`
- `backend/app/services/document_steganography_service.py`
- `backend/app/steganography/invisible_character_embedder.py`
- `backend/app/steganography/structure_embedder.py`
- `backend/app/steganography/pdf_image_processor.py`
- `backend/app/document_processing/pdf_parser.py`
- `backend/app/document_processing/pdf_rebuilder.py`
- `backend/app/document_processing/txt_handler.py`
- `backend/app/document_processing/document_validator.py`
- `backend/app/verification/platform_signature.py`
- `backend/app/utils/payload_serializer.py`
- `backend/app/models/schemas.py`

**Services**:
- document_steganography_service.py
- platform_verification_service.py

**Routes**:
- POST /api/document/embed
- GET /api/document/download/{filename}

**Utilities**:
- payload_serializer.py
- logging_config.py

**Database Tables**:
- None

**Configuration**:
- backend/.env
  - max_document_size_mb
  - platform_secret_key

**Dependencies**:
- PyMuPDF (fitz)

---

### Feature: Document Steganography (Extract)

**Purpose**: Extract encrypted messages from documents using hybrid steganography

**Frontend Files**:
- (Currently not implemented in frontend)

**Backend Files**:
- `backend/app/routes/document_steganography.py`
- `backend/app/services/document_steganography_service.py`
- `backend/app/steganography/invisible_character_extractor.py`
- `backend/app/steganography/structure_extractor.py`
- `backend/app/steganography/pdf_image_processor.py`
- `backend/app/document_processing/pdf_parser.py`
- `backend/app/document_processing/txt_handler.py`
- `backend/app/verification/signature_validator.py`
- `backend/app/utils/payload_deserializer.py`
- `backend/app/models/schemas.py`

**Services**:
- document_steganography_service.py
- platform_verification_service.py

**Routes**:
- POST /api/document/extract

**Utilities**:
- payload_deserializer.py
- logging_config.py

**Database Tables**:
- None

**Configuration**:
- backend/.env
  - platform_secret_key

**Dependencies**:
- PyMuPDF (fitz)

---

### Feature: Platform Signature Verification

**Purpose**: Generate and verify HMAC-SHA256 platform signatures for authenticity

**Frontend Files**:
- None (backend-only)

**Backend Files**:
- `backend/app/services/platform_verification_service.py`
- `backend/app/verification/platform_signature.py`
- `backend/app/verification/signature_validator.py`
- `backend/app/verification/signature_constants.py`
- `backend/app/verification/signature_exceptions.py`

**Services**:
- platform_verification_service.py

**Routes**:
- None (used by all steganography services)

**Utilities**:
- logging_config.py
- exceptions.py

**Database Tables**:
- None

**Configuration**:
- backend/.env
  - platform_secret_key

**Dependencies**:
- hmac
- hashlib

---

## End-to-End Flow Mapping

### Workflow: Image Embedding (Hide Message)

**Step 1**: User enters message and password
- **File**: `frontend/src/pages/HideMessage.jsx`
- **Action**: User inputs message, password, and uploads image

**Step 2**: Frontend calls encryption API
- **File**: `frontend/src/services/apiService.js`
- **Function**: `encryptMessage(message, password)`
- **API**: POST /api/encryption/encrypt

**Step 3**: Backend receives encryption request
- **File**: `backend/app/routes/encryption.py`
- **Function**: `encrypt_message(request: EncryptRequest)`

**Step 4**: Backend performs encryption
- **File**: `backend/app/services/crypto_service.py`
- **Function**: `encrypt_message(message, password)`
- **Process**: 
  - Generate random salt (16 bytes)
  - Derive key using Argon2id
  - Generate random IV (12 bytes)
  - Encrypt using AES-256-GCM
  - Return ciphertext, salt, iv

**Step 5**: Backend returns encryption response
- **File**: `backend/app/routes/encryption.py`
- **Response**: EncryptResponse with ciphertext, salt, iv, algorithm, kdf

**Step 6**: Frontend receives encryption response
- **File**: `frontend/src/pages/HideMessage.jsx`
- **Action**: Stores encryption data in encryptionService

**Step 7**: Frontend calls steganography embed API
- **File**: `frontend/src/services/apiService.js`
- **Function**: `embedMessage(imageFile, encryptedMessage, algorithm)`
- **API**: POST /api/steganography/embed

**Step 8**: Backend receives steganography embed request
- **File**: `backend/app/routes/steganography.py`
- **Function**: `embed_message(image, encryptedMessage, algorithm)`

**Step 9**: Backend validates image
- **File**: `backend/app/image_processing/image_validator.py`
- **Function**: `validate_file(image_path)`

**Step 10**: Backend converts image to PNG
- **File**: `backend/app/image_processing/image_converter.py`
- **Function**: `convert_to_png(image_path)`

**Step 11**: Backend detects edges
- **File**: `backend/app/image_processing/edge_detector.py`
- **Function**: `detect_edges(image_path)`
- **Function**: `get_edge_pixel_coordinates(edge_map)`

**Step 12**: Backend creates structured payload
- **File**: `backend/app/utils/payload_serializer.py`
- **Function**: `create_payload(encrypted_data, algorithm)`
- **Function**: `serialize_to_binary(payload_dict)`

**Step 13**: Backend injects platform signature
- **File**: `backend/app/services/platform_verification_service.py`
- **Function**: `prepare_payload_for_embedding(encrypted_payload_binary, media_type)`
- **Process**:
  - Generate HMAC-SHA256 signature
  - Combine signature with payload
  - Return combined payload

**Step 14**: Backend checks capacity
- **File**: `backend/app/steganography/edge_lsb_embedder.py`
- **Function**: `calculate_capacity(edge_count)`

**Step 15**: Backend embeds payload
- **File**: `backend/app/steganography/edge_lsb_embedder.py`
- **Function**: `embed(image_path, payload, combined_payload, edge_coordinates)`
- **Process**:
  - Embed payload length header
  - Embed payload data into edge pixels
  - Save stego image

**Step 16**: Backend returns steganography response
- **File**: `backend/app/routes/steganography.py`
- **Response**: EmbedResponse with fileName, statistics

**Step 17**: Frontend receives steganography response
- **File**: `frontend/src/pages/HideMessage.jsx`
- **Action**: Displays success message and download button

**Step 18**: User downloads stego image
- **File**: `frontend/src/services/apiService.js`
- **Function**: `downloadStegoImage(filename)`
- **API**: GET /api/steganography/download/{filename}

**Step 19**: Backend serves file
- **File**: `backend/app/routes/steganography.py`
- **Function**: `download_stego_image(filename)`

---

### Workflow: Image Extraction (Extract Message)

**Step 1**: User uploads stego image and enters password
- **File**: `frontend/src/pages/ExtractMessage.jsx`
- **Action**: User uploads stego image, enters password, salt, and iv

**Step 2**: Frontend calls steganography extract API
- **File**: `frontend/src/services/apiService.js`
- **Function**: `extractMessage(imageFile)`
- **API**: POST /api/steganography/extract

**Step 3**: Backend receives steganography extract request
- **File**: `backend/app/routes/steganography.py`
- **Function**: `extract_message(image)`

**Step 4**: Backend validates image
- **File**: `backend/app/steganography/edge_lsb_extractor.py`
- **Function**: `validate_image(image_path)`

**Step 5**: Backend detects edges
- **File**: `backend/app/image_processing/edge_detector.py`
- **Function**: `detect_edges(image_path)`
- **Function**: `get_edge_pixel_coordinates(edge_map)`

**Step 6**: Backend extracts payload
- **File**: `backend/app/steganography/edge_lsb_extractor.py`
- **Function**: `extract(image_path, edge_coordinates)`
- **Process**:
  - Read header to get payload size
  - Extract bits from edge pixels
  - Reconstruct combined payload

**Step 7**: Backend verifies platform signature
- **File**: `backend/app/services/platform_verification_service.py`
- **Function**: `extract_and_verify_signature(combined_payload, actual_media_type)`
- **Process**:
  - Extract signature length
  - Extract signature binary
  - Extract encrypted payload
  - Verify HMAC-SHA256 signature
  - Validate platform, version, media type

**Step 8**: Backend deserializes payload
- **File**: `backend/app/utils/payload_deserializer.py`
- **Function**: `deserialize_from_binary(payload_binary)`
- **Function**: `extract_encrypted_data(payload_dict)`

**Step 9**: Backend returns extraction response
- **File**: `backend/app/routes/steganography.py`
- **Response**: ExtractResponse with encryptedData, algorithm, version, timestamp, statistics

**Step 10**: Frontend receives extraction response
- **File**: `frontend/src/pages/ExtractMessage.jsx`
- **Action**: Stores extracted encrypted data

**Step 11**: Frontend calls decryption API
- **File**: `frontend/src/services/apiService.js`
- **Function**: `decryptMessage(ciphertext, password, salt, iv)`
- **API**: POST /api/encryption/decrypt

**Step 12**: Backend receives decryption request
- **File**: `backend/app/routes/encryption.py`
- **Function**: `decrypt_message(request: DecryptRequest)`

**Step 13**: Backend performs decryption
- **File**: `backend/app/services/crypto_service.py`
- **Function**: `decrypt_message(ciphertext, password, salt, iv)`
- **Process**:
  - Decode base64
  - Derive key using Argon2id
  - Decrypt using AES-256-GCM
  - Return plaintext

**Step 14**: Backend returns decryption response
- **File**: `backend/app/routes/encryption.py`
- **Response**: DecryptResponse with message

**Step 15**: Frontend receives decryption response
- **File**: `frontend/src/pages/ExtractMessage.jsx`
- **Action**: Displays decrypted message

---

### Workflow: Video Embedding

**Step 1**: User uploads video and encrypted message
- **File**: (Frontend not yet implemented)

**Step 2**: Backend receives video embed request
- **File**: `backend/app/routes/video_steganography.py`
- **Function**: `embed_message(video, encryptedMessage, algorithm, frameSelectionStrategy, frameInterval)`

**Step 3**: Backend validates video
- **File**: `backend/app/video_processing/video_validator.py`
- **Function**: `validate_file(video_path)`

**Step 4**: Backend converts video to MP4
- **File**: `backend/app/video_processing/video_converter.py`
- **Function**: `convert_to_mp4(video_path)`

**Step 5**: Backend extracts frames
- **File**: `backend/app/video_processing/frame_extractor.py`
- **Function**: `extract_frames(video_path)`

**Step 6**: Backend selects embedding frames
- **File**: `backend/app/steganography/video/frame_selector.py`
- **Function**: `select_frames(total_frames, strategy, interval)`

**Step 7**: Backend creates structured payload
- **File**: `backend/app/utils/payload_serializer.py`
- **Function**: `create_payload(encrypted_data, algorithm)`

**Step 8**: Backend injects platform signature
- **File**: `backend/app/services/platform_verification_service.py`
- **Function**: `prepare_payload_for_embedding(encrypted_payload_binary, media_type)`

**Step 9**: Backend embeds payload using DCT
- **File**: `backend/app/steganography/video/dct_embedder.py`
- **Function**: `embed(frames, payload, frame_indices)`

**Step 10**: Backend rebuilds video
- **File**: `backend/app/video_processing/frame_rebuilder.py`
- **Function**: `rebuild_video(frames, audio_path, output_path)`

**Step 11**: Backend returns video embed response
- **File**: `backend/app/routes/video_steganography.py`
- **Response**: VideoEmbedResponse with fileName, statistics

---

### Workflow: Audio Embedding

**Step 1**: User uploads audio and encrypted message
- **File**: (Frontend not yet implemented)

**Step 2**: Backend receives audio embed request
- **File**: `backend/app/routes/audio_steganography.py`
- **Function**: `embed_message(audio, encryptedMessage, password, algorithm)`

**Step 3**: Backend validates audio
- **File**: `backend/app/audio_processing/audio_validator.py`
- **Function**: `validate_file(audio_path)`

**Step 4**: Backend converts audio to WAV
- **File**: `backend/app/audio_processing/audio_converter.py`
- **Function**: `convert_to_wav(audio_path)`

**Step 5**: Backend loads audio
- **File**: `backend/app/audio_processing/audio_loader.py`
- **Function**: `load_audio(audio_path)`

**Step 6**: Backend generates sample positions
- **File**: `backend/app/steganography/audio/sample_selector.py`
- **Function**: `generate_sample_positions(password, total_samples)`

**Step 7**: Backend creates structured payload
- **File**: `backend/app/utils/payload_serializer.py`
- **Function**: `create_payload(encrypted_data, algorithm)`

**Step 8**: Backend injects platform signature
- **File**: `backend/app/services/platform_verification_service.py`
- **Function**: `prepare_payload_for_embedding(encrypted_payload_binary, media_type)`

**Step 9**: Backend embeds payload using LSB
- **File**: `backend/app/steganography/audio/audio_lsb_embedder.py`
- **Function**: `embed(audio_data, payload, sample_positions)`

**Step 10**: Backend writes stego audio
- **File**: `backend/app/audio_processing/audio_writer.py`
- **Function**: `write_audio(audio_data, output_path)`

**Step 11**: Backend returns audio embed response
- **File**: `backend/app/routes/audio_steganography.py`
- **Response**: AudioEmbedResponse with fileName, statistics

---

### Workflow: Document Embedding

**Step 1**: User uploads document and encrypted message
- **File**: (Frontend not yet implemented)

**Step 2**: Backend receives document embed request
- **File**: `backend/app/routes/document_steganography.py`
- **Function**: `embed_message(document, encryptedMessage, algorithm, textMethod, useImages)`

**Step 3**: Backend validates document
- **File**: `backend/app/document_processing/document_validator.py`
- **Function**: `validate_file(document_path)`

**Step 4**: Backend processes document
- **For PDF**:
  - **File**: `backend/app/document_processing/pdf_parser.py`
  - **Function**: `parse_pdf(pdf_path)`
- **For TXT**:
  - **File**: `backend/app/document_processing/txt_handler.py`
  - **Function**: `load_txt(txt_path)`

**Step 5**: Backend creates structured payload
- **File**: `backend/app/utils/payload_serializer.py`
- **Function**: `create_payload(encrypted_data, algorithm)`

**Step 6**: Backend injects platform signature
- **File**: `backend/app/services/platform_verification_service.py`
- **Function**: `prepare_payload_for_embedding(encrypted_payload_binary, media_type)`

**Step 7**: Backend embeds payload
- **For TXT**:
  - **Invisible Character**: `backend/app/steganography/invisible_character_embedder.py`
  - **Structure-Based**: `backend/app/steganography/structure_embedder.py`
- **For PDF**:
  - **Text**: `backend/app/steganography/invisible_character_embedder.py` or `structure_embedder.py`
  - **Images**: `backend/app/steganography/pdf_image_processor.py`

**Step 8**: Backend rebuilds document
- **For PDF**: `backend/app/document_processing/pdf_rebuilder.py`
- **For TXT**: `backend/app/document_processing/txt_handler.py`

**Step 9**: Backend returns document embed response
- **File**: `backend/app/routes/document_steganography.py`
- **Response**: DocumentEmbedResponse with fileName, statistics

---

## Summary

This blueprint provides a comprehensive overview of the SecureStego project, including:

1. **System Overview**: Project purpose, core functionality, technology stack, and security architecture
2. **Folder Map**: Detailed explanation of every folder's purpose, responsibilities, connections, and dependencies
3. **File Map**: Detailed explanation of every important file's purpose, usage, dependencies, and related features
4. **Feature Traceability Map**: Complete mapping of every feature to its participating files, services, routes, utilities, and configuration
5. **End-to-End Flow Mapping**: Step-by-step workflow documentation for all major operations

This documentation enables developers to:
- Instantly locate any feature
- Instantly locate any bug source
- Understand frontend-backend communication
- Understand API communication
- Understand encryption flow
- Understand steganography flow
- Understand platform verification flow
- Understand dependency relationships
- Understand where every important piece of logic exists
