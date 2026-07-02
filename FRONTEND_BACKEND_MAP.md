# SecureStego Frontend-Backend Map

## Table of Contents
1. [Frontend Pages](#frontend-pages)
2. [Frontend Components](#frontend-components)
3. [Frontend Services](#frontend-services)
4. [Frontend Hooks](#frontend-hooks)
5. [Frontend Utilities](#frontend-utilities)
6. [Backend Routes](#backend-routes)
7. [Backend Services](#backend-services)
8. [Backend Utilities](#backend-utilities)
9. [API Communication Flow](#api-communication-flow)
10. [Data Flow Diagrams](#data-flow-diagrams)

---

## Frontend Pages

### Landing Page

**File**: `frontend/src/pages/Landing.jsx`

**Purpose**: Home page with hero section and feature overview

**Components Used**:
- Navbar
- Footer
- UI components (Button, Card)

**API Calls**: None

**Backend Routes**: None

**State Management**: Local component state

**Related Features**:
- User onboarding
- Feature showcase

---

### Hide Message Page

**File**: `frontend/src/pages/HideMessage.jsx`

**Purpose**: Encryption and embedding workflow for hiding messages

**Components Used**:
- Navbar
- Footer
- FileUpload
- PasswordInput
- Textarea
- Button
- Card
- DebugPanel

**API Calls**:
- `encryptMessage(message, password)` → POST /api/encryption/encrypt
- `embedMessage(imageFile, encryptedMessage, algorithm)` → POST /api/steganography/embed
- `downloadStegoImage(filename)` → GET /api/steganography/download/{filename}

**Backend Routes**:
- POST /api/encryption/encrypt
- POST /api/steganography/embed
- GET /api/steganography/download/{filename}

**Backend Services**:
- crypto_service.py
- steganography_service.py
- platform_verification_service.py

**State Management**:
- Local component state (file, password, message, isProcessing, error, encryptionData, stegoData)
- encryptionService (encryption data storage)

**Data Flow**:
```
User Input → encryptMessage() → crypto_service.encrypt_message() → EncryptResponse
User Input + EncryptResponse → embedMessage() → steganography_service.embed_message() → EmbedResponse
EmbedResponse → downloadStegoImage() → FileResponse → Browser Download
```

**Related Features**:
- Message encryption
- Image steganography embedding
- File download

---

### Extract Message Page

**File**: `frontend/src/pages/ExtractMessage.jsx`

**Purpose**: Extraction and decryption workflow for revealing hidden messages

**Components Used**:
- Navbar
- Footer
- FileUpload
- PasswordInput
- Button
- Card
- DebugPanel

**API Calls**:
- `extractMessage(imageFile)` → POST /api/steganography/extract
- `decryptMessage(ciphertext, password, salt, iv)` → POST /api/encryption/decrypt

**Backend Routes**:
- POST /api/steganography/extract
- POST /api/encryption/decrypt

**Backend Services**:
- steganography_service.py
- platform_verification_service.py
- crypto_service.py

**State Management**:
- Local component state (file, password, ciphertext, salt, iv, isProcessing, extractedMessage, decryptionData, stegoData)
- encryptionService (decryption data storage)

**Data Flow**:
```
User Input → extractMessage() → steganography_service.extract_message() → ExtractResponse
ExtractResponse + User Input → decryptMessage() → crypto_service.decrypt_message() → DecryptResponse
DecryptResponse → Display Message
```

**Related Features**:
- Image steganography extraction
- Message decryption
- Platform signature verification

---

### About Page

**File**: `frontend/src/pages/About.jsx`

**Purpose**: Information about the project, technology, and security

**Components Used**:
- Navbar
- Footer
- UI components (Card, Button)

**API Calls**: None

**Backend Routes**: None

**State Management**: None

**Related Features**:
- Project information
- Security information

---

### Contact Page

**File**: `frontend/src/pages/Contact.jsx`

**Purpose**: Contact form for user inquiries

**Components Used**:
- Navbar
- Footer
- UI components (Card, Button, Form inputs)

**API Calls**: None (currently not implemented)

**Backend Routes**: None

**State Management**: Local component state

**Related Features**:
- User contact

---

## Frontend Components

### Navbar

**File**: `frontend/src/components/layout/Navbar.jsx`

**Purpose**: Navigation menu for the application

**Used By**: All pages

**API Calls**: None

**Backend Routes**: None

**State Management**: None

---

### Footer

**File**: `frontend/src/components/layout/Footer.jsx`

**Purpose**: Footer with links and copyright

**Used By**: All pages

**API Calls**: None

**Backend Routes**: None

**State Management**: None

---

### Button

**File**: `frontend/src/components/ui/Button.jsx`

**Purpose**: Reusable button component with variants

**Used By**: All pages

**API Calls**: None

**Backend Routes**: None

**State Management**: None

---

### Card

**File**: `frontend/src/components/ui/Card.jsx`

**Purpose**: Reusable card container component

**Used By**: All pages

**API Calls**: None

**Backend Routes**: None

**State Management**: None

---

### FileUpload

**File**: `frontend/src/components/ui/FileUpload.jsx`

**Purpose**: File upload component with preview

**Used By**: HideMessage, ExtractMessage

**API Calls**: None

**Backend Routes**: None

**State Management**: Local component state

---

### PasswordInput

**File**: `frontend/src/components/ui/PasswordInput.jsx`

**Purpose**: Password input with strength indicator

**Used By**: HideMessage, ExtractMessage

**API Calls**: None

**Backend Routes**: None

**State Management**: Local component state

---

### Textarea

**File**: `frontend/src/components/ui/Textarea.jsx`

**Purpose**: Text area component for message input

**Used By**: HideMessage

**API Calls**: None

**Backend Routes**: None

**State Management**: Controlled by parent

---

### DebugPanel

**File**: `frontend/src/components/ui/DebugPanel.jsx`

**Purpose**: Debug information display panel

**Used By**: HideMessage, ExtractMessage

**API Calls**: None

**Backend Routes**: None

**State Management**: Controlled by parent

---

## Frontend Services

### apiService.js

**File**: `frontend/src/services/apiService.js`

**Purpose**: HTTP API client for backend communication

**Functions**:
- `encryptMessage(message, password)` → POST /api/encryption/encrypt
- `decryptMessage(ciphertext, password, salt, iv)` → POST /api/encryption/decrypt
- `embedMessage(imageFile, encryptedMessage, algorithm)` → POST /api/steganography/embed
- `extractMessage(imageFile)` → POST /api/steganography/extract
- `downloadStegoImage(filename)` → GET /api/steganography/download/{filename}
- `checkEncryptionHealth()` → GET /api/encryption/health
- `checkSteganographyHealth()` → GET /api/steganography/health

**Used By**:
- HideMessage page
- ExtractMessage page
- useEncryption hook
- useSteganography hook

**Backend Routes**:
- POST /api/encryption/encrypt
- POST /api/encryption/decrypt
- POST /api/steganography/embed
- POST /api/steganography/extract
- GET /api/steganography/download/{filename}
- GET /api/encryption/health
- GET /api/steganography/health

**Backend Services**:
- crypto_service.py
- steganography_service.py

**Error Handling**: Try-catch with error message extraction

---

### encryptionService.js

**File**: `frontend/src/services/encryptionService.js`

**Purpose**: Encryption state management and utilities

**Functions**:
- `setEncryptionData(data)` - Store encryption data
- `getEncryptionData()` - Retrieve encryption data
- `setDecryptionData(data)` - Store decryption data
- `getDecryptionData()` - Retrieve decryption data
- `clearEncryptionData()` - Clear encryption data
- `clearDecryptionData()` - Clear decryption data
- `evaluatePasswordStrength(password)` - Evaluate password strength
- `formatBytes(bytes)` - Format bytes to human-readable
- `generateDebugInfo(data, password)` - Generate debug information

**Used By**:
- HideMessage page
- ExtractMessage page

**Backend Routes**: None (state management only)

**Backend Services**: None

**Error Handling**: None (state management)

---

### index.js

**File**: `frontend/src/services/index.js`

**Purpose**: Service exports

**Exports**:
- apiService.js functions
- encryptionService.js

**Used By**: All pages and hooks

---

## Frontend Hooks

### useEncryption.js

**File**: `frontend/src/hooks/useEncryption.js`

**Purpose**: Custom hook for encryption operations

**State**:
- isEncrypting (boolean)
- isDecrypting (boolean)
- error (string)

**Functions**:
- `encryptMessage(message, password)` - Call apiService.encryptMessage
- `decryptMessage(ciphertext, password, salt, iv)` - Call apiService.decryptMessage

**Used By**:
- HideMessage page
- ExtractMessage page

**Backend Routes**:
- POST /api/encryption/encrypt
- POST /api/encryption/decrypt

**Backend Services**:
- crypto_service.py

**Error Handling**: Sets error state on failure

---

### useSteganography.js

**File**: `frontend/src/hooks/useSteganography.js`

**Purpose**: Custom hook for steganography operations

**State**:
- isEmbedding (boolean)
- isExtracting (boolean)
- error (string)

**Functions**:
- `embedMessage(imageFile, encryptedMessage, algorithm)` - Call apiService.embedMessage
- `extractMessage(imageFile)` - Call apiService.extractMessage
- `downloadStegoFile(filename, mediaType)` - Trigger file download

**Used By**:
- HideMessage page
- ExtractMessage page

**Backend Routes**:
- POST /api/steganography/embed
- POST /api/steganography/extract
- GET /api/steganography/download/{filename}

**Backend Services**:
- steganography_service.py

**Error Handling**: Sets error state on failure

---

### index.js

**File**: `frontend/src/hooks/index.js`

**Purpose**: Hook exports

**Exports**:
- useEncryption
- useSteganography

**Used By**: Pages

---

## Frontend Utilities

### api.js

**File**: `frontend/src/utils/api.js`

**Purpose**: API request helpers (legacy, not actively used)

**Functions**:
- `apiRequest(url, options)` - Generic API request
- `encryptWithBackend(message, passwordHash)` - Legacy encryption
- `decryptWithBackend(ciphertext, passwordHash)` - Legacy decryption
- `checkHealth()` - Health check

**Used By**: (Currently minimal)

**Backend Routes**: All endpoints

**Backend Services**: All services

**Error Handling**: Try-catch with error message extraction

---

### crypto.js

**File**: `frontend/src/utils/crypto.js`

**Purpose**: Web Crypto API utilities (client-side encryption)

**Functions**:
- `generateSalt()` - Generate random salt
- `generateNonce()` - Generate random nonce
- `stringToBytes(string)` - Convert string to bytes
- `bytesToString(bytes)` - Convert bytes to string
- `bytesToBase64(bytes)` - Convert bytes to base64
- `base64ToBytes(base64)` - Convert base64 to bytes
- `bytesToHex(bytes)` - Convert bytes to hex
- `hexToBytes(hex)` - Convert hex to bytes
- `sha256Hash(data)` - Generate SHA-256 hash
- `deriveKey(password, salt)` - Derive key using PBKDF2
- `encryptMessage(message, key, nonce)` - Encrypt using AES-256-GCM
- `decryptMessage(ciphertext, key, nonce)` - Decrypt using AES-256-GCM

**Used By**: (Currently minimal - encryption moved to backend)

**Backend Routes**: None (client-side only)

**Backend Services**: None

**Error Handling**: Try-catch with error throwing

---

### index.js

**File**: `frontend/src/utils/index.js`

**Purpose**: Utility exports

**Exports**:
- api.js functions
- crypto.js functions

**Used By**: Services and pages

---

## Backend Routes

### encryption.py

**File**: `backend/app/routes/encryption.py`

**Purpose**: Encryption API endpoints

**Endpoints**:
- POST /api/encryption/encrypt
- POST /api/encryption/decrypt
- GET /api/encryption/health

**Frontend Callers**:
- apiService.js (encryptMessage, decryptMessage, checkEncryptionHealth)

**Backend Services**:
- crypto_service.py

**Response Flow**:
```
Request → Route → Service → Response
```

---

### steganography.py

**File**: `backend/app/routes/steganography.py`

**Purpose**: Image steganography API endpoints

**Endpoints**:
- POST /api/steganography/embed
- POST /api/steganography/extract
- GET /api/steganography/download/{filename}
- GET /api/steganography/health

**Frontend Callers**:
- apiService.js (embedMessage, extractMessage, downloadStegoImage, checkSteganographyHealth)

**Backend Services**:
- steganography_service.py

**Response Flow**:
```
Request → Route → Service → Response
```

---

### video_steganography.py

**File**: `backend/app/routes/video_steganography.py`

**Purpose**: Video steganography API endpoints

**Endpoints**:
- POST /api/video/embed
- POST /api/video/extract
- GET /api/video/download/{filename}
- GET /api/video/health

**Frontend Callers**: None (frontend not yet implemented)

**Backend Services**:
- video_steganography_service.py

**Response Flow**:
```
Request → Route → Service → Response
```

---

### audio_steganography.py

**File**: `backend/app/routes/audio_steganography.py`

**Purpose**: Audio steganography API endpoints

**Endpoints**:
- POST /api/audio/embed
- POST /api/audio/extract
- GET /api/audio/download/{filename}
- GET /api/audio/health

**Frontend Callers**: None (frontend not yet implemented)

**Backend Services**:
- audio_steganography_service.py

**Response Flow**:
```
Request → Route → Service → Response
```

---

### document_steganography.py

**File**: `backend/app/routes/document_steganography.py`

**Purpose**: Document steganography API endpoints

**Endpoints**:
- POST /api/document/embed
- POST /api/document/extract
- GET /api/document/download/{filename}
- GET /api/document/health

**Frontend Callers**: None (frontend not yet implemented)

**Backend Services**:
- document_steganography_service.py

**Response Flow**:
```
Request → Route → Service → Response
```

---

## Backend Services

### crypto_service.py

**File**: `backend/app/services/crypto_service.py`

**Purpose**: Argon2id + AES-256-GCM encryption service

**Functions**:
- `encrypt_message(message, password)` - Encrypt message
- `decrypt_message(ciphertext, password, salt, iv)` - Decrypt message
- `derive_key(password, salt)` - Derive key using Argon2id
- `generate_salt()` - Generate random salt
- `generate_iv()` - Generate random IV

**Used By**:
- encryption.py (routes)

**Frontend Callers**: apiService.js (via encryption route)

**Backend Routes**:
- POST /api/encryption/encrypt
- POST /api/encryption/decrypt

**Dependencies**:
- argon2-cffi
- cryptography

**Database Access**: None

---

### steganography_service.py

**File**: `backend/app/services/steganography_service.py`

**Purpose**: Image steganography orchestration service

**Functions**:
- `embed_message(image_path, encrypted_data, algorithm)` - Embed message into image
- `extract_message(image_path)` - Extract message from image
- `cleanup_stego_file(file_path)` - Clean up stego file

**Used By**:
- steganography.py (routes)

**Frontend Callers**: apiService.js (via steganography route)

**Backend Routes**:
- POST /api/steganography/embed
- POST /api/steganography/extract

**Dependencies**:
- image_processing modules
- steganography modules
- verification modules
- utils modules

**Database Access**: None

---

### video_steganography_service.py

**File**: `backend/app/services/video_steganography_service.py`

**Purpose**: Video steganography orchestration service

**Functions**:
- `embed_message(video_path, encrypted_data, algorithm, frame_selection_strategy, frame_interval)` - Embed message into video
- `extract_message(video_path)` - Extract message from video

**Used By**:
- video_steganography.py (routes)

**Frontend Callers**: None (frontend not yet implemented)

**Backend Routes**:
- POST /api/video/embed
- POST /api/video/extract

**Dependencies**:
- video_processing modules
- steganography/video modules
- verification modules
- utils modules

**Database Access**: None

---

### audio_steganography_service.py

**File**: `backend/app/services/audio_steganography_service.py`

**Purpose**: Audio steganography orchestration service

**Functions**:
- `embed_message(audio_path, encrypted_data, password, algorithm)` - Embed message into audio
- `extract_message(audio_path, password)` - Extract message from audio

**Used By**:
- audio_steganography.py (routes)

**Frontend Callers**: None (frontend not yet implemented)

**Backend Routes**:
- POST /api/audio/embed
- POST /api/audio/extract

**Dependencies**:
- audio_processing modules
- steganography/audio modules
- verification modules
- utils modules

**Database Access**: None

---

### document_steganography_service.py

**File**: `backend/app/services/document_steganography_service.py`

**Purpose**: Document steganography orchestration service

**Functions**:
- `embed_message(document_path, encrypted_data, algorithm, text_method, use_images)` - Embed message into document
- `extract_message(document_path)` - Extract message from document

**Used By**:
- document_steganography.py (routes)

**Frontend Callers**: None (frontend not yet implemented)

**Backend Routes**:
- POST /api/document/embed
- POST /api/document/extract

**Dependencies**:
- document_processing modules
- steganography modules
- verification modules
- utils modules

**Database Access**: None

---

### platform_verification_service.py

**File**: `backend/app/services/platform_verification_service.py`

**Purpose**: Platform signature verification service

**Functions**:
- `prepare_payload_for_embedding(encrypted_payload_binary, media_type)` - Prepare payload with signature
- `extract_and_verify_signature(combined_payload, actual_media_type)` - Extract and verify signature
- `verify_file_before_extraction(combined_payload, actual_media_type)` - Verify file before extraction
- `get_error_response(error)` - Generate error response
- `get_verification_diagnostics(verification_result)` - Format diagnostics

**Used By**:
- steganography_service.py
- video_steganography_service.py
- audio_steganography_service.py
- document_steganography_service.py

**Frontend Callers**: None (backend-only)

**Backend Routes**: None (used by services)

**Dependencies**:
- verification modules
- utils modules

**Database Access**: None

---

## Backend Utilities

### logging_config.py

**File**: `backend/app/utils/logging_config.py`

**Purpose**: Centralized logging configuration

**Functions**:
- `setup_logging()` - Configure logging
- `get_logger(name)` - Get logger instance

**Used By**: All backend modules

**Frontend Callers**: None

**Backend Routes**: None

**Dependencies**: logging

---

### exceptions.py

**File**: `backend/app/utils/exceptions.py`

**Purpose**: Custom exception classes

**Exceptions**:
- Various custom exceptions for error handling

**Used By**: All backend modules

**Frontend Callers**: None

**Backend Routes**: None

**Dependencies**: None

---

### payload_serializer.py

**File**: `backend/app/utils/payload_serializer.py`

**Purpose**: Payload serialization for embedding

**Functions**:
- `create_payload(encrypted_data, algorithm, version)` - Create structured payload
- `serialize_to_binary(payload)` - Serialize to binary
- `get_payload_size(payload)` - Calculate payload size

**Used By**:
- steganography_service.py
- video_steganography_service.py
- audio_steganography_service.py
- document_steganography_service.py

**Frontend Callers**: None

**Backend Routes**: None

**Dependencies**: json

---

### payload_deserializer.py

**File**: `backend/app/utils/payload_deserializer.py`

**Purpose**: Payload deserialization for extraction

**Functions**:
- `deserialize_from_binary(payload_binary)` - Deserialize from binary
- `extract_encrypted_data(payload_dict)` - Extract encrypted data

**Used By**:
- steganography_service.py
- video_steganography_service.py
- audio_steganography_service.py
- document_steganography_service.py

**Frontend Callers**: None

**Backend Routes**: None

**Dependencies**: json

---

## API Communication Flow

### Encryption Flow

**Frontend**:
```
HideMessage.jsx
  ↓
apiService.js (encryptMessage)
  ↓
HTTP POST /api/encryption/encrypt
```

**Backend**:
```
encryption.py (encrypt_message)
  ↓
crypto_service.py (encrypt_message)
  ↓
argon2-cffi + cryptography
  ↓
EncryptResponse
  ↓
HTTP 200 OK
```

**Frontend**:
```
apiService.js (receives EncryptResponse)
  ↓
HideMessage.jsx (stores encryptionData)
```

---

### Steganography Embed Flow

**Frontend**:
```
HideMessage.jsx
  ↓
apiService.js (embedMessage)
  ↓
HTTP POST /api/steganography/embed
```

**Backend**:
```
steganography.py (embed_message)
  ↓
steganography_service.py (embed_message)
  ↓
  ├─ image_converter.py (convert_to_png)
  ├─ edge_detector.py (detect_edges)
  ├─ payload_serializer.py (create_payload)
  ├─ platform_verification_service.py (prepare_payload_for_embedding)
  └─ edge_lsb_embedder.py (embed)
  ↓
EmbedResponse
  ↓
HTTP 200 OK
```

**Frontend**:
```
apiService.js (receives EmbedResponse)
  ↓
HideMessage.jsx (displays success)
```

---

### Steganography Extract Flow

**Frontend**:
```
ExtractMessage.jsx
  ↓
apiService.js (extractMessage)
  ↓
HTTP POST /api/steganography/extract
```

**Backend**:
```
steganography.py (extract_message)
  ↓
steganography_service.py (extract_message)
  ↓
  ├─ edge_detector.py (detect_edges)
  ├─ edge_lsb_extractor.py (extract)
  ├─ platform_verification_service.py (extract_and_verify_signature)
  └─ payload_deserializer.py (deserialize_from_binary)
  ↓
ExtractResponse
  ↓
HTTP 200 OK
```

**Frontend**:
```
apiService.js (receives ExtractResponse)
  ↓
ExtractMessage.jsx (stores encryptedData)
```

---

### Decryption Flow

**Frontend**:
```
ExtractMessage.jsx
  ↓
apiService.js (decryptMessage)
  ↓
HTTP POST /api/encryption/decrypt
```

**Backend**:
```
encryption.py (decrypt_message)
  ↓
crypto_service.py (decrypt_message)
  ↓
argon2-cffi + cryptography
  ↓
DecryptResponse
  ↓
HTTP 200 OK
```

**Frontend**:
```
apiService.js (receives DecryptResponse)
  ↓
ExtractMessage.jsx (displays message)
```

---

### Download Flow

**Frontend**:
```
HideMessage.jsx
  ↓
apiService.js (downloadStegoImage)
  ↓
HTTP GET /api/steganography/download/{filename}
```

**Backend**:
```
steganography.py (download_stego_image)
  ↓
FileResponse
  ↓
HTTP 200 OK
```

**Frontend**:
```
apiService.js (receives blob)
  ↓
Browser download triggered
```

---

## Data Flow Diagrams

### Complete Hide Message Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                            │
├─────────────────────────────────────────────────────────────┤
│  HideMessage.jsx                                            │
│    ├─ User Input (message, password, image)               │
│    ├─ apiService.encryptMessage()                           │
│    └─ apiService.embedMessage()                            │
└───────────────────────┬───────────────────────────────────┘
                        │ HTTP POST
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                        Backend                             │
├─────────────────────────────────────────────────────────────┤
│  encryption.py (encrypt_message)                            │
│    └─ crypto_service.encrypt_message()                     │
│        ├─ Argon2id key derivation                          │
│        └─ AES-256-GCM encryption                           │
│  steganography.py (embed_message)                           │
│    └─ steganography_service.embed_message()                 │
│        ├─ image_converter.convert_to_png()                 │
│        ├─ edge_detector.detect_edges()                     │
│        ├─ payload_serializer.create_payload()              │
│        ├─ platform_verification_service.prepare_payload()   │
│        └─ edge_lsb_embedder.embed()                        │
└───────────────────────┬───────────────────────────────────┘
                        │ HTTP 200 OK
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                            │
├─────────────────────────────────────────────────────────────┤
│  apiService.js (receives responses)                        │
│  HideMessage.jsx (displays success)                        │
│  apiService.downloadStegoImage()                           │
│    └─ Browser download                                     │
└─────────────────────────────────────────────────────────────┘
```

---

### Complete Extract Message Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                            │
├─────────────────────────────────────────────────────────────┤
│  ExtractMessage.jsx                                         │
│    ├─ User Input (stego image, password, salt, iv)       │
│    ├─ apiService.extractMessage()                          │
│    └─ apiService.decryptMessage()                          │
└───────────────────────┬───────────────────────────────────┘
                        │ HTTP POST
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                        Backend                             │
├─────────────────────────────────────────────────────────────┤
│  steganography.py (extract_message)                        │
│    └─ steganography_service.extract_message()              │
│        ├─ edge_detector.detect_edges()                     │
│        ├─ edge_lsb_extractor.extract()                      │
│        ├─ platform_verification_service.extract_and_verify() │
│        └─ payload_deserializer.deserialize_from_binary()    │
│  encryption.py (decrypt_message)                           │
│    └─ crypto_service.decrypt_message()                     │
│        ├─ Argon2id key derivation                          │
│        └─ AES-256-GCM decryption                          │
└───────────────────────┬───────────────────────────────────┘
                        │ HTTP 200 OK
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                            │
├─────────────────────────────────────────────────────────────┤
│  apiService.js (receives responses)                        │
│  ExtractMessage.jsx (displays message)                     │
└─────────────────────────────────────────────────────────────┘
```

---

### Platform Signature Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Backend (Embedding)                      │
├─────────────────────────────────────────────────────────────┤
│  steganography_service.embed_message()                      │
│    ├─ payload_serializer.create_payload()                  │
│    └─ platform_verification_service.prepare_payload()       │
│        ├─ platform_signature.generate_signature()           │
│        │   └─ HMAC-SHA256 generation                      │
│        └─ Combine signature + payload                      │
│    └─ edge_lsb_embedder.embed(combined_payload)            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Backend (Extraction)                      │
├─────────────────────────────────────────────────────────────┤
│  steganography_service.extract_message()                     │
│    ├─ edge_lsb_extractor.extract()                          │
│    │   └─ Returns combined_payload                          │
│    └─ platform_verification_service.extract_and_verify()    │
│        ├─ Extract signature                                 │
│        ├─ Extract encrypted payload                         │
│        └─ signature_validator.verify_from_binary()          │
│            ├─ Verify HMAC-SHA256                            │
│            ├─ Validate platform                              │
│            ├─ Validate version                              │
│            └─ Validate media type                           │
│    └─ payload_deserializer.deserialize_from_binary()       │
└─────────────────────────────────────────────────────────────┘
```

---

## Summary

This frontend-backend map provides comprehensive documentation of the relationship between frontend and backend components:

1. **Frontend Pages**: All pages with their components, API calls, and state management
2. **Frontend Components**: All UI components with their usage
3. **Frontend Services**: All services with their functions and backend routes
4. **Frontend Hooks**: All custom hooks with their state and functions
5. **Frontend Utilities**: All utility functions
6. **Backend Routes**: All API endpoints with their services and frontend callers
7. **Backend Services**: All services with their functions and dependencies
8. **Backend Utilities**: All utility modules
9. **API Communication Flow**: Detailed flow for each API call
10. **Data Flow Diagrams**: Visual representation of complete workflows

This documentation enables developers to:
- Understand frontend-backend communication
- Trace API calls from frontend to backend
- Understand data flow through the system
- Locate where frontend and backend interact
- Debug communication issues
- Understand the complete request/response cycle
