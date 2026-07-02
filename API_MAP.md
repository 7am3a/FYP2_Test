# SecureStego API Map

## Table of Contents
1. [System Endpoints](#system-endpoints)
2. [Encryption Endpoints](#encryption-endpoints)
3. [Image Steganography Endpoints](#image-steganography-endpoints)
4. [Video Steganography Endpoints](#video-steganography-endpoints)
5. [Audio Steganography Endpoints](#audio-steganography-endpoints)
6. [Document Steganography Endpoints](#document-steganography-endpoints)
7. [Error Codes](#error-codes)
8. [Common Response Formats](#common-response-formats)

---

## System Endpoints

### GET /

**Purpose**: Root endpoint with API information

**Request**:
- Method: GET
- Path: `/`
- Headers: None
- Body: None

**Response**:
```json
{
  "name": "SecureStego",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "docs": "/api/docs",
    "health": "/health",
    "encryption": {
      "health": "/api/encryption/health",
      "encrypt": "/api/encryption/encrypt",
      "decrypt": "/api/encryption/decrypt"
    },
    "steganography": {
      "health": "/api/steganography/health",
      "embed": "/api/steganography/embed",
      "extract": "/api/steganography/extract"
    },
    "video_steganography": {
      "health": "/api/video/health",
      "embed": "/api/video/embed",
      "extract": "/api/video/extract",
      "download": "/api/video/download/{filename}"
    },
    "document_steganography": {
      "health": "/api/document/health",
      "embed": "/api/document/embed",
      "extract": "/api/document/extract",
      "download": "/api/document/download/{filename}"
    },
    "audio_steganography": {
      "health": "/api/audio/health",
      "embed": "/api/audio/embed",
      "extract": "/api/audio/extract",
      "download": "/api/audio/download/{filename}"
    }
  }
}
```

**Implementation**:
- File: `backend/app/main.py`
- Function: `root()`
- Line: 57-96

**Frontend Callers**: None (informational)

**Dependencies**: None

---

### GET /health

**Purpose**: Health check endpoint

**Request**:
- Method: GET
- Path: `/health`
- Headers: None
- Body: None

**Response**:
```json
{
  "status": "healthy",
  "service": "SecureStego",
  "version": "1.0.0"
}
```

**Implementation**:
- File: `backend/app/main.py`
- Function: `health()`
- Line: 99-106

**Frontend Callers**: None (health monitoring)

**Dependencies**: None

---

## Encryption Endpoints

### POST /api/encryption/encrypt

**Purpose**: Encrypt a message using Argon2id key derivation and AES-256-GCM

**Request**:
- Method: POST
- Path: `/api/encryption/encrypt`
- Headers: `Content-Type: application/json`
- Body:
```json
{
  "message": "plaintext message to encrypt",
  "password": "user password"
}
```

**Request Schema**: `EncryptRequest`
- message (string, required): Plaintext message to encrypt
- password (string, required): User password for key derivation

**Response**:
```json
{
  "success": true,
  "ciphertext": "base64 encoded ciphertext",
  "salt": "base64 encoded salt",
  "iv": "base64 encoded iv",
  "algorithm": "AES-256-GCM",
  "kdf": "Argon2id"
}
```

**Response Schema**: `EncryptResponse`
- success (boolean): Operation success status
- ciphertext (string): Base64 encoded ciphertext
- salt (string): Base64 encoded salt
- iv (string): Base64 encoded IV
- algorithm (string): Encryption algorithm used
- kdf (string): Key derivation function used

**Implementation**:
- File: `backend/app/routes/encryption.py`
- Function: `encrypt_message(request: EncryptRequest)`
- Line: 12-56
- Service: `backend/app/services/crypto_service.py`
- Function: `encrypt_message(message, password)`
- Line: 91-136

**Frontend Callers**:
- File: `frontend/src/services/apiService.js`
- Function: `encryptMessage(message, password)`
- Line: 12-35
- Used by: `frontend/src/pages/HideMessage.jsx`

**Dependencies**:
- argon2-cffi
- cryptography
- Pydantic

**Error Responses**:
- 500 Internal Server Error: Encryption failed

---

### POST /api/encryption/decrypt

**Purpose**: Decrypt a message using Argon2id key derivation and AES-256-GCM

**Request**:
- Method: POST
- Path: `/api/encryption/decrypt`
- Headers: `Content-Type: application/json`
- Body:
```json
{
  "ciphertext": "base64 encoded ciphertext",
  "password": "user password",
  "salt": "base64 encoded salt",
  "iv": "base64 encoded iv"
}
```

**Request Schema**: `DecryptRequest`
- ciphertext (string, required): Base64 encoded ciphertext
- password (string, required): User password for key derivation
- salt (string, required): Base64 encoded salt
- iv (string, required): Base64 encoded IV

**Response**:
```json
{
  "success": true,
  "message": "decrypted plaintext message"
}
```

**Response Schema**: `DecryptResponse`
- success (boolean): Operation success status
- message (string): Decrypted plaintext message

**Implementation**:
- File: `backend/app/routes/encryption.py`
- Function: `decrypt_message(request: DecryptRequest)`
- Line: 59-107
- Service: `backend/app/services/crypto_service.py`
- Function: `decrypt_message(ciphertext, password, salt, iv)`
- Line: 138-177

**Frontend Callers**:
- File: `frontend/src/services/apiService.js`
- Function: `decryptMessage(ciphertext, password, salt, iv)`
- Line: 37-60
- Used by: `frontend/src/pages/ExtractMessage.jsx`

**Dependencies**:
- argon2-cffi
- cryptography
- Pydantic

**Error Responses**:
- 400 Bad Request: Decryption validation error (wrong password)
- 500 Internal Server Error: Decryption failed

---

### GET /api/encryption/health

**Purpose**: Health check endpoint for encryption service

**Request**:
- Method: GET
- Path: `/api/encryption/health`
- Headers: None
- Body: None

**Response**:
```json
{
  "status": "healthy",
  "service": "encryption",
  "algorithm": "AES-256-GCM",
  "keyDerivation": "Argon2id"
}
```

**Implementation**:
- File: `backend/app/routes/encryption.py`
- Function: `health_check()`
- Line: 110-118

**Frontend Callers**:
- File: `frontend/src/services/apiService.js`
- Function: `checkEncryptionHealth()`
- Line: 229-239

**Dependencies**: None

---

## Image Steganography Endpoints

### POST /api/steganography/embed

**Purpose**: Embed an encrypted message into an image using edge-based LSB steganography

**Request**:
- Method: POST
- Path: `/api/steganography/embed`
- Headers: `Content-Type: multipart/form-data`
- Body (FormData):
  - image (file, required): Image file to embed message into
  - encryptedMessage (string, required): Base64 encoded encrypted message
  - algorithm (string, optional): Encryption algorithm used (default: "AES-256-GCM")

**Supported Formats**: PNG, JPG, JPEG, HEIC
**Max File Size**: 50 MB

**Response**:
```json
{
  "success": true,
  "fileName": "stego_image_filename.png",
  "originalFormat": "jpg",
  "convertedFormat": "png",
  "statistics": {
    "imageWidth": 1920,
    "imageHeight": 1080,
    "totalPixels": 2073600,
    "edgePixels": 52340,
    "payloadSize": 1024,
    "headerSize": 4,
    "totalBitsUsed": 8192,
    "capacityRemaining": 146808,
    "capacityUsedPercent": 5.29,
    "embeddingMethod": "Edge-Based LSB",
    "edgeDetectionMethod": "Canny",
    "processingTime": 0.452
  },
  "stegoImagePath": "/tmp/stego_image_filename.png"
}
```

**Response Schema**: `EmbedResponse`
- success (boolean): Operation success status
- fileName (string): Name of the stego image file
- originalFormat (string): Original image format
- convertedFormat (string): Converted image format
- statistics (object): Embedding statistics
  - imageWidth (integer): Image width in pixels
  - imageHeight (integer): Image height in pixels
  - totalPixels (integer): Total number of pixels
  - edgePixels (integer): Number of edge pixels detected
  - payloadSize (integer): Payload size in bytes
  - headerSize (integer): Header size in bytes
  - totalBitsUsed (integer): Total bits used for embedding
  - capacityRemaining (integer): Remaining capacity in bits
  - capacityUsedPercent (float): Percentage of capacity used
  - embeddingMethod (string): Steganography method used
  - edgeDetectionMethod (string): Edge detection method used
  - processingTime (float): Processing time in seconds
- stegoImagePath (string): Path to stego image for download (internal)

**Implementation**:
- File: `backend/app/routes/steganography.py`
- Function: `embed_message(image, encryptedMessage, algorithm)`
- Line: 26-124
- Service: `backend/app/services/steganography_service.py`
- Function: `embed_message(image_path, encrypted_data, algorithm)`
- Line: 64-218
- Dependencies:
  - `backend/app/image_processing/image_converter.py`
  - `backend/app/image_processing/edge_detector.py`
  - `backend/app/image_processing/image_validator.py`
  - `backend/app/steganography/edge_lsb_embedder.py`
  - `backend/app/utils/payload_serializer.py`
  - `backend/app/services/platform_verification_service.py`

**Frontend Callers**:
- File: `frontend/src/services/apiService.js`
- Function: `embedMessage(imageFile, encryptedMessage, algorithm)`
- Line: 62-95
- Used by: `frontend/src/pages/HideMessage.jsx`

**Dependencies**:
- OpenCV
- Pillow
- NumPy
- Pydantic

**Error Responses**:
- 400 Bad Request: Unsupported image format
- 400 Bad Request: Image capacity exceeded
- 500 Internal Server Error: Embedding failed

---

### POST /api/steganography/extract

**Purpose**: Extract an encrypted message from a stego image

**Request**:
- Method: POST
- Path: `/api/steganography/extract`
- Headers: `Content-Type: multipart/form-data`
- Body (FormData):
  - image (file, required): Stego PNG image file containing hidden message

**Supported Formats**: PNG only
**Max File Size**: 50 MB

**Response**:
```json
{
  "success": true,
  "encryptedData": "base64 encoded encrypted message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "statistics": {
    "imageWidth": 1920,
    "imageHeight": 1080,
    "totalPixels": 2073600,
    "edgePixels": 52340,
    "payloadSize": 1024,
    "headerSize": 4,
    "totalBitsExtracted": 8192,
    "extractionMethod": "Edge-Based LSB",
    "edgeDetectionMethod": "Canny",
    "processingTime": 0.387
  }
}
```

**Response Schema**: `ExtractResponse`
- success (boolean): Operation success status
- encryptedData (string): Base64 encoded encrypted message
- algorithm (string): Encryption algorithm used
- version (string): Payload version
- timestamp (string): Payload timestamp
- statistics (object): Extraction statistics
  - imageWidth (integer): Image width in pixels
  - imageHeight (integer): Image height in pixels
  - totalPixels (integer): Total number of pixels
  - edgePixels (integer): Number of edge pixels detected
  - payloadSize (integer): Payload size in bytes
  - headerSize (integer): Header size in bytes
  - totalBitsExtracted (integer): Total bits extracted
  - extractionMethod (string): Steganography method used
  - edgeDetectionMethod (string): Edge detection method used
  - processingTime (float): Processing time in seconds

**Implementation**:
- File: `backend/app/routes/steganography.py`
- Function: `extract_message(image)`
- Line: 127-214
- Service: `backend/app/services/steganography_service.py`
- Function: `extract_message(image_path)`
- Line: 220-336
- Dependencies:
  - `backend/app/image_processing/edge_detector.py`
  - `backend/app/steganography/edge_lsb_extractor.py`
  - `backend/app/utils/payload_deserializer.py`
  - `backend/app/services/platform_verification_service.py`

**Frontend Callers**:
- File: `frontend/src/services/apiService.js`
- Function: `extractMessage(imageFile)`
- Line: 97-130
- Used by: `frontend/src/pages/ExtractMessage.jsx`

**Dependencies**:
- OpenCV
- Pillow
- NumPy
- Pydantic

**Error Responses**:
- 400 Bad Request: Invalid image format (must be PNG)
- 400 Bad Request: No hidden data found
- 400 Bad Request: Invalid platform signature
- 500 Internal Server Error: Extraction failed

---

### GET /api/steganography/download/{filename}

**Purpose**: Download a stego image file

**Request**:
- Method: GET
- Path: `/api/steganography/download/{filename}`
- Headers: None
- Body: None
- Path Parameters:
  - filename (string, required): Name of the stego image file to download

**Response**:
- Content-Type: image/png
- Content-Disposition: attachment; filename="{filename}"
- Body: Binary image file

**Implementation**:
- File: `backend/app/routes/steganography.py`
- Function: `download_stego_image(filename)`
- Line: 217-259

**Frontend Callers**:
- File: `frontend/src/services/apiService.js`
- Function: `downloadStegoImage(filename)`
- Line: 133-155
- Used by: `frontend/src/pages/HideMessage.jsx`

**Dependencies**: None

**Error Responses**:
- 404 Not Found: Stego image not found or expired
- 500 Internal Server Error: Download failed

---

### GET /api/steganography/health

**Purpose**: Health check endpoint for steganography service

**Request**:
- Method: GET
- Path: `/api/steganography/health`
- Headers: None
- Body: None

**Response**:
```json
{
  "status": "healthy",
  "service": "steganography",
  "method": "Edge-Based LSB",
  "edgeDetection": "Canny",
  "supportedFormats": ["PNG", "JPG", "JPEG", "HEIC"],
  "outputFormat": "PNG"
}
```

**Implementation**:
- File: `backend/app/routes/steganography.py`
- Function: `health_check()`
- Line: 262-272

**Frontend Callers**:
- File: `frontend/src/services/apiService.js`
- Function: `checkSteganographyHealth()`
- Line: 157-167

**Dependencies**: None

---

## Video Steganography Endpoints

### POST /api/video/embed

**Purpose**: Embed an encrypted message into a video using DCT-based steganography

**Request**:
- Method: POST
- Path: `/api/video/embed`
- Headers: `Content-Type: multipart/form-data`
- Body (FormData):
  - video (file, required): Video file to embed message into
  - encryptedMessage (string, required): Base64 encoded encrypted message
  - algorithm (string, optional): Encryption algorithm used (default: "AES-256-GCM")
  - frameSelectionStrategy (string, optional): Frame selection strategy (default: "fixed_interval")
  - frameInterval (integer, optional): Interval for fixed interval selection (default: 10)

**Supported Formats**: MP4, AVI, MOV
**Max File Size**: 500 MB

**Response**:
```json
{
  "success": true,
  "fileName": "stego_video_filename.mp4",
  "originalFormat": "avi",
  "convertedFormat": "mp4",
  "statistics": {
    "videoWidth": 1920,
    "videoHeight": 1080,
    "totalFrames": 3000,
    "selectedFrames": 300,
    "frameSelectionStrategy": "fixed_interval",
    "frameInterval": 10,
    "payloadSize": 1024,
    "totalBitsEmbedded": 8192,
    "capacityRemaining": 2391808,
    "capacityUsedPercent": 0.34,
    "embeddingMethod": "DCT-Based Block Steganography",
    "audioPreserved": true,
    "processingTime": 15.432
  },
  "stegoVideoPath": "/tmp/stego_video_filename.mp4"
}
```

**Response Schema**: `VideoEmbedResponse`
- success (boolean): Operation success status
- fileName (string): Name of the stego video file
- originalFormat (string): Original video format
- convertedFormat (string): Converted video format
- statistics (object): Embedding statistics
  - videoWidth (integer): Video width in pixels
  - videoHeight (integer): Video height in pixels
  - totalFrames (integer): Total number of frames in video
  - selectedFrames (integer): Number of frames selected for embedding
  - frameSelectionStrategy (string): Frame selection strategy used
  - frameInterval (integer): Interval for fixed interval selection
  - payloadSize (integer): Payload size in bytes
  - totalBitsEmbedded (integer): Total bits embedded
  - capacityRemaining (integer): Remaining capacity in bytes
  - capacityUsedPercent (float): Percentage of capacity used
  - embeddingMethod (string): Steganography method used
  - audioPreserved (boolean): Whether audio track was preserved
  - processingTime (float): Processing time in seconds
- stegoVideoPath (string): Path to stego video for download (internal)

**Implementation**:
- File: `backend/app/routes/video_steganography.py`
- Function: `embed_message(video, encryptedMessage, algorithm, frameSelectionStrategy, frameInterval)`
- Line: 27-131
- Service: `backend/app/services/video_steganography_service.py`
- Function: `embed_message(video_path, encrypted_data, algorithm, frame_selection_strategy, frame_interval)`
- Dependencies:
  - `backend/app/video_processing/frame_extractor.py`
  - `backend/app/video_processing/frame_rebuilder.py`
  - `backend/app/video_processing/video_converter.py`
  - `backend/app/video_processing/video_validator.py`
  - `backend/app/video_processing/audio_handler.py`
  - `backend/app/steganography/video/dct_embedder.py`
  - `backend/app/steganography/video/frame_selector.py`
  - `backend/app/utils/payload_serializer.py`
  - `backend/app/services/platform_verification_service.py`

**Frontend Callers**: None (frontend not yet implemented)

**Dependencies**:
- OpenCV
- NumPy
- FFmpeg (external)
- Pydantic

**Error Responses**:
- 400 Bad Request: Unsupported video format
- 400 Bad Request: Video capacity exceeded
- 500 Internal Server Error: Video embedding failed

---

### POST /api/video/extract

**Purpose**: Extract an encrypted message from a stego video

**Request**:
- Method: POST
- Path: `/api/video/extract`
- Headers: `Content-Type: multipart/form-data`
- Body (FormData):
  - video (file, required): Stego MP4 video file containing hidden message

**Supported Formats**: MP4 only
**Max File Size**: 500 MB

**Response**:
```json
{
  "success": true,
  "encryptedData": "base64 encoded encrypted message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "statistics": {
    "videoWidth": 1920,
    "videoHeight": 1080,
    "totalFrames": 3000,
    "selectedFrames": 300,
    "frameSelectionStrategy": "fixed_interval",
    "frameInterval": 10,
    "payloadSize": 1024,
    "totalBitsEmbedded": 8192,
    "embeddingMethod": "DCT-Based Block Steganography",
    "processingTime": 12.234
  }
}
```

**Response Schema**: `VideoExtractResponse`
- success (boolean): Operation success status
- encryptedData (string): Base64 encoded encrypted message
- algorithm (string): Encryption algorithm used
- version (string): Payload version
- timestamp (string): Payload timestamp
- statistics (object): Extraction statistics
  - videoWidth (integer): Video width in pixels
  - videoHeight (integer): Video height in pixels
  - totalFrames (integer): Total number of frames in video
  - selectedFrames (integer): Number of frames selected for extraction
  - frameSelectionStrategy (string): Frame selection strategy used
  - frameInterval (integer): Interval for fixed interval selection
  - payloadSize (integer): Payload size in bytes
  - totalBitsEmbedded (integer): Total bits extracted
  - embeddingMethod (string): Steganography method used
  - processingTime (float): Processing time in seconds

**Implementation**:
- File: `backend/app/routes/video_steganography.py`
- Function: `extract_message(video)`
- Line: 134-221
- Service: `backend/app/services/video_steganography_service.py`
- Function: `extract_message(video_path)`
- Dependencies:
  - `backend/app/video_processing/frame_extractor.py`
  - `backend/app/steganography/video/dct_extractor.py`
  - `backend/app/steganography/video/frame_selector.py`
  - `backend/app/utils/payload_deserializer.py`
  - `backend/app/services/platform_verification_service.py`

**Frontend Callers**: None (frontend not yet implemented)

**Dependencies**:
- OpenCV
- NumPy
- FFmpeg (external)
- Pydantic

**Error Responses**:
- 400 Bad Request: Invalid video format (must be MP4)
- 400 Bad Request: No hidden data found
- 400 Bad Request: Invalid platform signature
- 500 Internal Server Error: Video extraction failed

---

### GET /api/video/download/{filename}

**Purpose**: Download a stego video file

**Request**:
- Method: GET
- Path: `/api/video/download/{filename}`
- Headers: None
- Body: None
- Path Parameters:
  - filename (string, required): Name of the stego video file to download

**Response**:
- Content-Type: video/mp4
- Content-Disposition: attachment; filename="{filename}"
- Body: Binary video file

**Implementation**:
- File: `backend/app/routes/video_steganography.py`
- Function: `download_stego_video(filename)`
- Line: 224-266

**Frontend Callers**: None (frontend not yet implemented)

**Dependencies**: None

**Error Responses**:
- 404 Not Found: Stego video not found or expired
- 500 Internal Server Error: Download failed

---

### GET /api/video/health

**Purpose**: Health check endpoint for video steganography service

**Request**:
- Method: GET
- Path: `/api/video/health`
- Headers: None
- Body: None

**Response**:
```json
{
  "status": "healthy",
  "service": "video-steganography",
  "method": "DCT-Based Block Steganography",
  "supportedFormats": ["MP4", "AVI", "MOV"],
  "outputFormat": "MP4",
  "frameSelectionStrategies": ["fixed_interval", "uniform", "password_derived"],
  "audioPreservation": true
}
```

**Implementation**:
- File: `backend/app/routes/video_steganography.py`
- Function: `health_check()`
- Line: 269-280

**Frontend Callers**: None

**Dependencies**: None

---

## Audio Steganography Endpoints

### POST /api/audio/embed

**Purpose**: Embed an encrypted message into an audio file using randomized LSB steganography

**Request**:
- Method: POST
- Path: `/api/audio/embed`
- Headers: `Content-Type: multipart/form-data`
- Body (FormData):
  - audio (file, required): Audio file to embed message into
  - encryptedMessage (string, required): Base64 encoded encrypted message
  - password (string, required): Password for sample position generation
  - algorithm (string, optional): Encryption algorithm used (default: "AES-256-GCM")

**Supported Formats**: WAV, MP3, M4A, FLAC
**Max File Size**: 100 MB

**Response**:
```json
{
  "success": true,
  "fileName": "stego_audio_filename.wav",
  "originalFormat": "mp3",
  "convertedFormat": "wav",
  "statistics": {
    "duration": 180.5,
    "channels": 2,
    "sampleRate": 44100,
    "bitDepth": 16,
    "totalSamples": 7938000,
    "payloadSize": 1024,
    "headerSize": 4,
    "totalBitsEmbedded": 8192,
    "capacityRemaining": 12620800,
    "capacityUsedPercent": 0.06,
    "embeddingMethod": "Randomized WAV LSB",
    "processingTime": 2.345
  },
  "stegoAudioPath": "/tmp/stego_audio_filename.wav"
}
```

**Response Schema**: `AudioEmbedResponse`
- success (boolean): Operation success status
- fileName (string): Name of the stego audio file
- originalFormat (string): Original audio format
- convertedFormat (string): Converted audio format
- statistics (object): Embedding statistics
  - duration (float): Audio duration in seconds
  - channels (integer): Number of audio channels
  - sampleRate (integer): Sample rate in Hz
  - bitDepth (integer): Bit depth per sample
  - totalSamples (integer): Total number of audio samples
  - payloadSize (integer): Payload size in bytes
  - headerSize (integer): Header size in bytes
  - totalBitsEmbedded (integer): Total bits embedded
  - capacityRemaining (integer): Remaining capacity in samples
  - capacityUsedPercent (float): Percentage of capacity used
  - embeddingMethod (string): Steganography method used
  - processingTime (float): Processing time in seconds
- stegoAudioPath (string): Path to stego audio for download (internal)

**Implementation**:
- File: `backend/app/routes/audio_steganography.py`
- Function: `embed_message(audio, encryptedMessage, password, algorithm)`
- Line: 27-130
- Service: `backend/app/services/audio_steganography_service.py`
- Function: `embed_message(audio_path, encrypted_data, password, algorithm)`
- Dependencies:
  - `backend/app/audio_processing/audio_converter.py`
  - `backend/app/audio_processing/audio_loader.py`
  - `backend/app/audio_processing/audio_writer.py`
  - `backend/app/audio_processing/audio_validator.py`
  - `backend/app/steganography/audio/audio_lsb_embedder.py`
  - `backend/app/steganography/audio/sample_selector.py`
  - `backend/app/utils/payload_serializer.py`
  - `backend/app/services/platform_verification_service.py`

**Frontend Callers**: None (frontend not yet implemented)

**Dependencies**:
- NumPy
- FFmpeg (external)
- Pydantic

**Error Responses**:
- 400 Bad Request: Unsupported audio format
- 400 Bad Request: Audio capacity exceeded
- 500 Internal Server Error: Audio embedding failed

---

### POST /api/audio/extract

**Purpose**: Extract an encrypted message from a stego audio file

**Request**:
- Method: POST
- Path: `/api/audio/extract`
- Headers: `Content-Type: multipart/form-data`
- Body (FormData):
  - audio (file, required): Stego WAV audio file containing hidden message
  - password (string, required): Password for sample position generation

**Supported Formats**: WAV only
**Max File Size**: 100 MB

**Response**:
```json
{
  "success": true,
  "encryptedData": "base64 encoded encrypted message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "statistics": {
    "duration": 180.5,
    "channels": 2,
    "sampleRate": 44100,
    "bitDepth": 16,
    "totalSamples": 7938000,
    "payloadSize": 1024,
    "headerSize": 4,
    "totalBitsEmbedded": 8192,
    "embeddingMethod": "Randomized WAV LSB",
    "processingTime": 1.876
  }
}
```

**Response Schema**: `AudioExtractResponse`
- success (boolean): Operation success status
- encryptedData (string): Base64 encoded encrypted message
- algorithm (string): Encryption algorithm used
- version (string): Payload version
- timestamp (string): Payload timestamp
- statistics (object): Extraction statistics
  - duration (float): Audio duration in seconds
  - channels (integer): Number of audio channels
  - sampleRate (integer): Sample rate in Hz
  - bitDepth (integer): Bit depth per sample
  - totalSamples (integer): Total number of audio samples
  - payloadSize (integer): Payload size in bytes
  - headerSize (integer): Header size in bytes
  - totalBitsEmbedded (integer): Total bits extracted
  - embeddingMethod (string): Steganography method used
  - processingTime (float): Processing time in seconds

**Implementation**:
- File: `backend/app/routes/audio_steganography.py`
- Function: `extract_message(audio, password)`
- Line: 133-225
- Service: `backend/app/services/audio_steganography_service.py`
- Function: `extract_message(audio_path, password)`
- Dependencies:
  - `backend/app/audio_processing/audio_loader.py`
  - `backend/app/steganography/audio/audio_lsb_extractor.py`
  - `backend/app/steganography/audio/sample_selector.py`
  - `backend/app/utils/payload_deserializer.py`
  - `backend/app/services/platform_verification_service.py`

**Frontend Callers**: None (frontend not yet implemented)

**Dependencies**:
- NumPy
- FFmpeg (external)
- Pydantic

**Error Responses**:
- 400 Bad Request: Invalid audio format (must be WAV)
- 400 Bad Request: No hidden data found
- 400 Bad Request: Invalid platform signature
- 500 Internal Server Error: Audio extraction failed

---

### GET /api/audio/download/{filename}

**Purpose**: Download a stego audio file

**Request**:
- Method: GET
- Path: `/api/audio/download/{filename}`
- Headers: None
- Body: None
- Path Parameters:
  - filename (string, required): Name of the stego audio file to download

**Response**:
- Content-Type: audio/wav
- Content-Disposition: attachment; filename="{filename}"
- Body: Binary audio file

**Implementation**:
- File: `backend/app/routes/audio_steganography.py`
- Function: `download_stego_audio(filename)`
- Line: 228-270

**Frontend Callers**: None (frontend not yet implemented)

**Dependencies**: None

**Error Responses**:
- 404 Not Found: Stego audio not found or expired
- 500 Internal Server Error: Download failed

---

### GET /api/audio/health

**Purpose**: Health check endpoint for audio steganography service

**Request**:
- Method: GET
- Path: `/api/audio/health`
- Headers: None
- Body: None

**Response**:
```json
{
  "status": "healthy",
  "service": "audio_steganography",
  "method": "Randomized WAV LSB",
  "supportedFormats": ["WAV", "MP3", "M4A", "FLAC"],
  "outputFormat": "WAV",
  "embeddingMethod": "Randomized LSB",
  "sampleSelection": "Password-Derived Deterministic Random"
}
```

**Implementation**:
- File: `backend/app/routes/audio_steganography.py`
- Function: `health_check()`
- Line: 273-284

**Frontend Callers**: None

**Dependencies**: None

---

## Document Steganography Endpoints

### POST /api/document/embed

**Purpose**: Embed an encrypted message into a document using hybrid dual-layer steganography

**Request**:
- Method: POST
- Path: `/api/document/embed`
- Headers: `Content-Type: multipart/form-data`
- Body (FormData):
  - document (file, required): Document file (PDF or TXT) to embed message into
  - encryptedMessage (string, required): Base64 encoded encrypted message
  - algorithm (string, optional): Encryption algorithm used (default: "AES-256-GCM")
  - textMethod (string, optional): Text embedding method (default: "invisible_character")
  - useImages (boolean, optional): Use image steganography for PDFs (default: true)

**Supported Formats**: PDF, TXT
**Max File Size**: 50 MB

**Response**:
```json
{
  "success": true,
  "fileName": "stego_document_filename.pdf",
  "documentType": "pdf",
  "statistics": {
    "documentType": "pdf",
    "pageCount": 10,
    "textBlocks": 50,
    "imageCount": 5,
    "originalLength": null,
    "stegoLength": null,
    "payloadSize": 1024,
    "headerSize": 4,
    "totalBitsEmbedded": 8192,
    "textPayloadSize": 4096,
    "imagePayloadSize": 4096,
    "textCapacityBits": 50000,
    "imageCapacityBits": 100000,
    "totalCapacityBits": 150000,
    "capacityUsedPercent": 5.46,
    "embeddingMethod": "Hybrid Dual-Layer Document Steganography",
    "textMethod": "invisible_character",
    "useImages": true,
    "processingTime": 3.456
  },
  "stegoDocumentPath": "/tmp/stego_document_filename.pdf"
}
```

**Response Schema**: `DocumentEmbedResponse`
- success (boolean): Operation success status
- fileName (string): Name of the stego document file
- documentType (string): Type of document (pdf or txt)
- statistics (object): Embedding statistics
  - documentType (string): Type of document (txt or pdf)
  - pageCount (integer, optional): Number of pages (PDF only)
  - textBlocks (integer, optional): Number of text blocks (PDF only)
  - imageCount (integer, optional): Number of embedded images (PDF only)
  - originalLength (integer, optional): Original text length (TXT only)
  - stegoLength (integer, optional): Stego text length (TXT only)
  - payloadSize (integer): Payload size in bytes
  - headerSize (integer): Header size in bytes
  - totalBitsEmbedded (integer, optional): Total bits used for embedding
  - textPayloadSize (integer, optional): Text payload size in bytes (PDF only)
  - imagePayloadSize (integer, optional): Image payload size in bytes (PDF only)
  - textCapacityBits (integer, optional): Text capacity in bits (PDF only)
  - imageCapacityBits (integer, optional): Image capacity in bits (PDF only)
  - totalCapacityBits (integer, optional): Total capacity in bits (PDF only)
  - capacityUsedPercent (float): Percentage of capacity used
  - embeddingMethod (string): Steganography method used
  - textMethod (string, optional): Text embedding method used
  - useImages (boolean, optional): Whether image steganography was used (PDF only)
  - processingTime (float): Processing time in seconds
- stegoDocumentPath (string): Path to stego document for download (internal)

**Implementation**:
- File: `backend/app/routes/document_steganography.py`
- Function: `embed_message(document, encryptedMessage, algorithm, textMethod, useImages)`
- Line: 28-131
- Service: `backend/app/services/document_steganography_service.py`
- Function: `embed_message(document_path, encrypted_data, algorithm, text_method, use_images)`
- Dependencies:
  - `backend/app/document_processing/pdf_parser.py`
  - `backend/app/document_processing/pdf_rebuilder.py`
  - `backend/app/document_processing/txt_handler.py`
  - `backend/app/document_processing/document_validator.py`
  - `backend/app/steganography/invisible_character_embedder.py`
  - `backend/app/steganography/structure_embedder.py`
  - `backend/app/steganography/pdf_image_processor.py`
  - `backend/app/utils/payload_serializer.py`
  - `backend/app/services/platform_verification_service.py`

**Frontend Callers**: None (frontend not yet implemented)

**Dependencies**:
- PyMuPDF (fitz)
- Pydantic

**Error Responses**:
- 400 Bad Request: Unsupported document format
- 400 Bad Request: Document capacity exceeded
- 500 Internal Server Error: Document embedding failed

---

### POST /api/document/extract

**Purpose**: Extract an encrypted message from a stego document

**Request**:
- Method: POST
- Path: `/api/document/extract`
- Headers: `Content-Type: multipart/form-data`
- Body (FormData):
  - document (file, required): Stego document file containing hidden message

**Supported Formats**: PDF, TXT
**Max File Size**: 50 MB

**Response**:
```json
{
  "success": true,
  "encryptedData": "base64 encoded encrypted message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "statistics": {
    "documentType": "pdf",
    "pageCount": 10,
    "textBlocks": 50,
    "imageCount": 5,
    "payloadSize": 1024,
    "headerSize": 4,
    "totalBitsEmbedded": 8192,
    "textPayloadSize": 4096,
    "imagePayloadSize": 4096,
    "textCapacityBits": 50000,
    "imageCapacityBits": 100000,
    "totalCapacityBits": 150000,
    "capacityUsedPercent": 5.46,
    "embeddingMethod": "Hybrid Dual-Layer Document Steganography",
    "textMethod": "invisible_character",
    "useImages": true,
    "processingTime": 2.876
  }
}
```

**Response Schema**: `DocumentExtractResponse`
- success (boolean): Operation success status
- encryptedData (string): Base64 encoded encrypted message
- algorithm (string): Encryption algorithm used
- version (string): Payload version
- timestamp (string): Payload timestamp
- statistics (object): Extraction statistics
  - documentType (string): Type of document (txt or pdf)
  - pageCount (integer, optional): Number of pages (PDF only)
  - textBlocks (integer, optional): Number of text blocks (PDF only)
  - imageCount (integer, optional): Number of embedded images (PDF only)
  - payloadSize (integer): Payload size in bytes
  - headerSize (integer): Header size in bytes
  - totalBitsEmbedded (integer, optional): Total bits extracted
  - textPayloadSize (integer, optional): Text payload size in bytes (PDF only)
  - imagePayloadSize (integer, optional): Image payload size in bytes (PDF only)
  - textCapacityBits (integer, optional): Text capacity in bits (PDF only)
  - imageCapacityBits (integer, optional): Image capacity in bits (PDF only)
  - totalCapacityBits (integer, optional): Total capacity in bits (PDF only)
  - capacityUsedPercent (float): Percentage of capacity used
  - embeddingMethod (string): Steganography method used
  - textMethod (string, optional): Text embedding method used
  - useImages (boolean, optional): Whether image steganography was used (PDF only)
  - processingTime (float): Processing time in seconds

**Implementation**:
- File: `backend/app/routes/document_steganography.py`
- Function: `extract_message(document)`
- Line: 134-225
- Service: `backend/app/services/document_steganography_service.py`
- Function: `extract_message(document_path)`
- Dependencies:
  - `backend/app/document_processing/pdf_parser.py`
  - `backend/app/document_processing/txt_handler.py`
  - `backend/app/steganography/invisible_character_extractor.py`
  - `backend/app/steganography/structure_extractor.py`
  - `backend/app/steganography/pdf_image_processor.py`
  - `backend/app/utils/payload_deserializer.py`
  - `backend/app/services/platform_verification_service.py`

**Frontend Callers**: None (frontend not yet implemented)

**Dependencies**:
- PyMuPDF (fitz)
- Pydantic

**Error Responses**:
- 400 Bad Request: Unsupported document format
- 400 Bad Request: No hidden data found
- 400 Bad Request: Invalid platform signature
- 500 Internal Server Error: Document extraction failed

---

### GET /api/document/download/{filename}

**Purpose**: Download a stego document file

**Request**:
- Method: GET
- Path: `/api/document/download/{filename}`
- Headers: None
- Body: None
- Body: None
- Path Parameters:
  - filename (string, required): Name of the stego document file to download

**Response**:
- Content-Type: application/pdf (for PDF) or text/plain (for TXT)
- Content-Disposition: attachment; filename="{filename}"
- Body: Binary document file

**Implementation**:
- File: `backend/app/routes/document_steganography.py`
- Function: `download_stego_document(filename)`
- Line: 228-278

**Frontend Callers**: None (frontend not yet implemented)

**Dependencies**: None

**Error Responses**:
- 404 Not Found: Stego document not found or expired
- 500 Internal Server Error: Download failed

---

### GET /api/document/health

**Purpose**: Health check endpoint for document steganography service

**Request**:
- Method: GET
- Path: `/api/document/health`
- Headers: None
- Body: None

**Response**:
```json
{
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
```

**Implementation**:
- File: `backend/app/routes/document_steganography.py`
- Function: `health_check()`
- Line: 281-295

**Frontend Callers**: None

**Dependencies**: None

---

## Error Codes

### HTTP Status Codes

| Status Code | Description | Common Causes |
|------------|-------------|---------------|
| 200 OK | Request succeeded | Operation completed successfully |
| 400 Bad Request | Invalid request | Invalid input, validation failed, capacity exceeded |
| 404 Not Found | Resource not found | File not found, expired file |
| 500 Internal Server Error | Server error | Processing failure, unexpected error |

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Messages

**Encryption Errors**:
- "Encryption failed. Please try again."
- "Decryption failed. Please check your password and try again."

**Steganography Errors**:
- "Unsupported image format. Allowed: PNG, JPG, JPEG, HEIC"
- "Image capacity exceeded. Please upload a larger image."
- "Invalid image format. Only PNG files are supported for extraction."
- "Stego image not found. It may have expired."

**Video Errors**:
- "Unsupported video format. Allowed: MP4, AVI, MOV"
- "Video embedding failed. Please try again."
- "Invalid video format. Only MP4 files are supported for extraction."

**Audio Errors**:
- "Unsupported audio format. Allowed: WAV, MP3, M4A, FLAC"
- "Embedding failed. Please try again."
- "Invalid audio format. Only WAV files are supported for extraction."

**Document Errors**:
- "Unsupported document format. Allowed: PDF, TXT"
- "Embedding failed. Please try again."
- "Extraction failed. Please check the document and try again."

**Platform Verification Errors**:
- "Platform signature verification failed: Invalid signature"
- "Platform signature verification failed: Tampered signature"
- "Platform signature verification failed: Version mismatch"
- "Platform signature verification failed: Platform mismatch"
- "Platform signature verification failed: Media type mismatch"

---

## Common Response Formats

### Success Response

All successful responses follow this pattern:
```json
{
  "success": true,
  ...additional fields...
}
```

### Error Response

All error responses follow this pattern:
```json
{
  "detail": "Error message"
}
```

### Statistics Response

Statistics are included in all steganography responses:
```json
{
  "statistics": {
    ...statistics fields...
    "processingTime": 0.123
  }
}
```

---

## Summary

This API map provides comprehensive documentation for all SecureStego API endpoints:

1. **System Endpoints**: Root and health check
2. **Encryption Endpoints**: Encrypt and decrypt messages
3. **Image Steganography Endpoints**: Embed and extract from images
4. **Video Steganography Endpoints**: Embed and extract from videos
5. **Audio Steganography Endpoints**: Embed and extract from audio
6. **Document Steganography Endpoints**: Embed and extract from documents

Each endpoint includes:
- Purpose
- Request details (method, path, headers, body)
- Request schema
- Response details
- Response schema
- Implementation location (file, function, line)
- Frontend callers
- Dependencies
- Error responses

This documentation enables developers to:
- Understand all available API endpoints
- Know how to call each endpoint
- Understand request/response formats
- Locate implementation code
- Debug API issues
- Integrate with the backend
