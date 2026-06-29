# SecureStego API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, the API does not require authentication. In production, implement API key or JWT authentication.

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "detail": "Error message",
  "status": "error"
}
```

## Endpoints

### Encryption Endpoints

#### POST /api/encryption/encrypt

Encrypt a message using Argon2id key derivation and AES-256-GCM.

**Request Body:**
```json
{
  "message": "string (required, min_length=1)",
  "password": "string (required, min_length=1)"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "ciphertext": "string (base64 encoded)",
  "salt": "string (base64 encoded)",
  "iv": "string (base64 encoded)",
  "algorithm": "AES-256-GCM",
  "kdf": "Argon2id"
}
```

**Error Responses:**
- `500 Internal Server Error`: Encryption failed

**Example:**
```bash
curl -X POST "http://localhost:8000/api/encryption/encrypt" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Secret message",
    "password": "my_secure_password"
  }'
```

---

#### POST /api/encryption/decrypt

Decrypt a message using Argon2id key derivation and AES-256-GCM.

**Request Body:**
```json
{
  "ciphertext": "string (required, min_length=1, base64 encoded)",
  "password": "string (required, min_length=1)",
  "salt": "string (required, min_length=1, base64 encoded)",
  "iv": "string (required, min_length=1, base64 encoded)"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "string (decrypted plaintext)"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid password or decryption parameters
- `500 Internal Server Error`: Decryption failed

**Example:**
```bash
curl -X POST "http://localhost:8000/api/encryption/decrypt" \
  -H "Content-Type: application/json" \
  -d '{
    "ciphertext": "base64_ciphertext_here",
    "password": "my_secure_password",
    "salt": "base64_salt_here",
    "iv": "base64_iv_here"
  }'
```

---

#### GET /api/encryption/health

Health check for encryption service.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "encryption",
  "algorithm": "AES-256-GCM",
  "keyDerivation": "Argon2id"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/encryption/health"
```

---

### Image Steganography Endpoints

#### POST /api/steganography/embed

Embed an encrypted message into an image using edge-based LSB steganography.

**Request:**
- `image` (file, required): Image file (PNG, JPG, JPEG, HEIC)
- `encryptedMessage` (string, required): Base64 encoded encrypted message
- `algorithm` (string, optional): Encryption algorithm used (default: "AES-256-GCM")

**Response (200 OK):**
```json
{
  "success": true,
  "fileName": "string (stego image filename)",
  "originalFormat": "string (original image format)",
  "convertedFormat": "PNG",
  "statistics": {
    "imageWidth": 1920,
    "imageHeight": 1080,
    "totalPixels": 2073600,
    "edgePixels": 450000,
    "payloadSize": 512,
    "headerSize": 32,
    "totalBitsUsed": 4096,
    "capacityRemaining": 896000,
    "capacityUsedPercent": 15.2,
    "embeddingMethod": "Edge-Based LSB",
    "edgeDetectionMethod": "Canny",
    "processingTime": 2.3
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid image or payload
- `500 Internal Server Error`: Embedding failed

**Example:**
```bash
curl -X POST "http://localhost:8000/api/steganography/embed" \
  -F "image=@image.png" \
  -F "encryptedMessage=base64_encrypted_message" \
  -F "algorithm=AES-256-GCM"
```

---

#### POST /api/steganography/extract

Extract an encrypted message from an image using edge-based LSB steganography.

**Request:**
- `image` (file, required): Stego image file (PNG, JPG, JPEG, HEIC)

**Response (200 OK):**
```json
{
  "success": true,
  "encryptedData": "string (base64 encoded encrypted message)",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "statistics": {
    "imageWidth": 1920,
    "imageHeight": 1080,
    "totalPixels": 2073600,
    "edgePixels": 450000,
    "payloadSize": 512,
    "headerSize": 32,
    "totalBitsUsed": 4096,
    "capacityRemaining": 896000,
    "capacityUsedPercent": 15.2,
    "embeddingMethod": "Edge-Based LSB",
    "edgeDetectionMethod": "Canny",
    "processingTime": 1.8
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid image or no hidden data found
- `500 Internal Server Error`: Extraction failed

**Example:**
```bash
curl -X POST "http://localhost:8000/api/steganography/extract" \
  -F "image=@stego_image.png"
```

---

#### GET /api/steganography/download/{filename}

Download a stego image file.

**Parameters:**
- `filename` (path parameter): Name of the stego image file

**Response (200 OK):**
- Binary file download

**Error Responses:**
- `404 Not Found`: File not found

**Example:**
```bash
curl -X GET "http://localhost:8000/api/steganography/download/stego_image.png" \
  --output downloaded_image.png
```

---

#### GET /api/steganography/health

Health check for image steganography service.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "steganography",
  "embeddingMethod": "Edge-Based LSB",
  "supportedFormats": ["PNG", "JPG", "JPEG", "HEIC"]
}
```

---

### Video Steganography Endpoints

#### POST /api/video/embed

Embed an encrypted message into a video using DCT-based block steganography.

**Request:**
- `video` (file, required): Video file (MP4, AVI, MOV)
- `encryptedMessage` (string, required): Base64 encoded encrypted message
- `algorithm` (string, optional): Encryption algorithm used (default: "AES-256-GCM")
- `frameSelectionStrategy` (string, optional): Frame selection strategy (default: "fixed_interval", options: "fixed_interval", "random", "keyframe")
- `frameInterval` (integer, optional): Interval for fixed interval selection (default: 30)

**Response (200 OK):**
```json
{
  "success": true,
  "fileName": "string (stego video filename)",
  "originalFormat": "string (original video format)",
  "convertedFormat": "MP4",
  "statistics": {
    "videoWidth": 1920,
    "videoHeight": 1080,
    "totalFrames": 3000,
    "selectedFrames": 100,
    "frameSelectionStrategy": "fixed_interval",
    "frameInterval": 30,
    "payloadSize": 512,
    "totalBitsEmbedded": 4096,
    "capacityRemaining": 500000,
    "capacityUsedPercent": 10.5,
    "embeddingMethod": "DCT-Based Block Steganography",
    "audioPreserved": true,
    "processingTime": 15.2
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid video or payload
- `500 Internal Server Error`: Embedding failed

**Example:**
```bash
curl -X POST "http://localhost:8000/api/video/embed" \
  -F "video=@video.mp4" \
  -F "encryptedMessage=base64_encrypted_message" \
  -F "algorithm=AES-256-GCM" \
  -F "frameSelectionStrategy=fixed_interval" \
  -F "frameInterval=30"
```

---

#### POST /api/video/extract

Extract an encrypted message from a video using DCT-based block steganography.

**Request:**
- `video` (file, required): Stego video file (MP4, AVI, MOV)

**Response (200 OK):**
```json
{
  "success": true,
  "encryptedData": "string (base64 encoded encrypted message)",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "statistics": {
    "videoWidth": 1920,
    "videoHeight": 1080,
    "totalFrames": 3000,
    "selectedFrames": 100,
    "frameSelectionStrategy": "fixed_interval",
    "frameInterval": 30,
    "payloadSize": 512,
    "totalBitsEmbedded": 4096,
    "capacityRemaining": 500000,
    "capacityUsedPercent": 10.5,
    "embeddingMethod": "DCT-Based Block Steganography",
    "audioPreserved": true,
    "processingTime": 12.8
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid video or no hidden data found
- `500 Internal Server Error`: Extraction failed

**Example:**
```bash
curl -X POST "http://localhost:8000/api/video/extract" \
  -F "video=@stego_video.mp4"
```

---

#### GET /api/video/download/{filename}

Download a stego video file.

**Parameters:**
- `filename` (path parameter): Name of the stego video file

**Response (200 OK):**
- Binary file download

**Error Responses:**
- `404 Not Found`: File not found

**Example:**
```bash
curl -X GET "http://localhost:8000/api/video/download/stego_video.mp4" \
  --output downloaded_video.mp4
```

---

#### GET /api/video/health

Health check for video steganography service.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "video-steganography",
  "embeddingMethod": "DCT-Based Block Steganography",
  "supportedFormats": ["MP4", "AVI", "MOV"]
}
```

---

### Audio Steganography Endpoints

#### POST /api/audio/embed

Embed an encrypted message into audio using randomized LSB steganography.

**Request:**
- `audio` (file, required): Audio file (WAV, MP3, M4A, FLAC)
- `encryptedMessage` (string, required): Base64 encoded encrypted message
- `password` (string, required): Password for sample position generation
- `algorithm` (string, optional): Encryption algorithm used (default: "AES-256-GCM")

**Response (200 OK):**
```json
{
  "success": true,
  "fileName": "string (stego audio filename)",
  "originalFormat": "string (original audio format)",
  "convertedFormat": "WAV",
  "statistics": {
    "duration": 180.5,
    "channels": 2,
    "sampleRate": 44100,
    "bitDepth": 16,
    "totalSamples": 7938000,
    "payloadSize": 512,
    "headerSize": 32,
    "totalBitsEmbedded": 4096,
    "capacityRemaining": 15872000,
    "capacityUsedPercent": 5.2,
    "embeddingMethod": "Randomized WAV LSB",
    "processingTime": 3.2
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid audio or payload
- `500 Internal Server Error`: Embedding failed

**Example:**
```bash
curl -X POST "http://localhost:8000/api/audio/embed" \
  -F "audio=@audio.mp3" \
  -F "encryptedMessage=base64_encrypted_message" \
  -F "password=my_secure_password" \
  -F "algorithm=AES-256-GCM"
```

---

#### POST /api/audio/extract

Extract an encrypted message from audio using randomized LSB steganography.

**Request:**
- `audio` (file, required): Stego audio file (WAV, MP3, M4A, FLAC)
- `password` (string, required): Password for sample position generation

**Response (200 OK):**
```json
{
  "success": true,
  "encryptedData": "string (base64 encoded encrypted message)",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "statistics": {
    "duration": 180.5,
    "channels": 2,
    "sampleRate": 44100,
    "bitDepth": 16,
    "totalSamples": 7938000,
    "payloadSize": 512,
    "headerSize": 32,
    "totalBitsEmbedded": 4096,
    "capacityRemaining": 15872000,
    "capacityUsedPercent": 5.2,
    "embeddingMethod": "Randomized WAV LSB",
    "processingTime": 2.8
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid audio or no hidden data found
- `500 Internal Server Error`: Extraction failed

**Example:**
```bash
curl -X POST "http://localhost:8000/api/audio/extract" \
  -F "audio=@stego_audio.wav" \
  -F "password=my_secure_password"
```

---

#### GET /api/audio/download/{filename}

Download a stego audio file.

**Parameters:**
- `filename` (path parameter): Name of the stego audio file

**Response (200 OK):**
- Binary file download

**Error Responses:**
- `404 Not Found`: File not found

**Example:**
```bash
curl -X GET "http://localhost:8000/api/audio/download/stego_audio.wav" \
  --output downloaded_audio.wav
```

---

#### GET /api/audio/health

Health check for audio steganography service.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "audio-steganography",
  "embeddingMethod": "Randomized WAV LSB",
  "supportedFormats": ["WAV", "MP3", "M4A", "FLAC"]
}
```

---

### Document Steganography Endpoints

#### POST /api/document/embed

Embed an encrypted message into a document using hybrid steganography.

**Request:**
- `document` (file, required): Document file (PDF, TXT)
- `encryptedMessage` (string, required): Base64 encoded encrypted message
- `algorithm` (string, optional): Encryption algorithm used (default: "AES-256-GCM")
- `textMethod` (string, optional): Text embedding method (default: "invisible_character", options: "invisible_character", "structure_based")
- `useImages` (boolean, optional): Use image steganography for PDF (default: true)

**Response (200 OK):**
```json
{
  "success": true,
  "fileName": "string (stego document filename)",
  "documentType": "pdf",
  "statistics": {
    "documentType": "pdf",
    "pageCount": 10,
    "textBlocks": 150,
    "imageCount": 5,
    "payloadSize": 512,
    "headerSize": 32,
    "totalBitsEmbedded": 4096,
    "textPayloadSize": 256,
    "imagePayloadSize": 256,
    "textCapacityBits": 50000,
    "imageCapacityBits": 100000,
    "totalCapacityBits": 150000,
    "capacityUsedPercent": 8.5,
    "embeddingMethod": "Hybrid Dual-Layer Document Steganography",
    "textMethod": "invisible_character",
    "useImages": true,
    "processingTime": 5.2
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid document or payload
- `500 Internal Server Error`: Embedding failed

**Example:**
```bash
curl -X POST "http://localhost:8000/api/document/embed" \
  -F "document=@document.pdf" \
  -F "encryptedMessage=base64_encrypted_message" \
  -F "algorithm=AES-256-GCM" \
  -F "textMethod=invisible_character" \
  -F "useImages=true"
```

---

#### POST /api/document/extract

Extract an encrypted message from a document using hybrid steganography.

**Request:**
- `document` (file, required): Stego document file (PDF, TXT)
- `textMethod` (string, optional): Text embedding method (default: "invisible_character")
- `useImages` (boolean, optional): Use image steganography for PDF (default: true)

**Response (200 OK):**
```json
{
  "success": true,
  "encryptedData": "string (base64 encoded encrypted message)",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "statistics": {
    "documentType": "pdf",
    "pageCount": 10,
    "textBlocks": 150,
    "imageCount": 5,
    "payloadSize": 512,
    "headerSize": 32,
    "totalBitsEmbedded": 4096,
    "textPayloadSize": 256,
    "imagePayloadSize": 256,
    "textCapacityBits": 50000,
    "imageCapacityBits": 100000,
    "totalCapacityBits": 150000,
    "capacityUsedPercent": 8.5,
    "embeddingMethod": "Hybrid Dual-Layer Document Steganography",
    "textMethod": "invisible_character",
    "useImages": true,
    "processingTime": 4.8
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid document or no hidden data found
- `500 Internal Server Error`: Extraction failed

**Example:**
```bash
curl -X POST "http://localhost:8000/api/document/extract" \
  -F "document=@stego_document.pdf" \
  -F "textMethod=invisible_character" \
  -F "useImages=true"
```

---

#### GET /api/document/download/{filename}

Download a stego document file.

**Parameters:**
- `filename` (path parameter): Name of the stego document file

**Response (200 OK):**
- Binary file download

**Error Responses:**
- `404 Not Found`: File not found

**Example:**
```bash
curl -X GET "http://localhost:8000/api/document/download/stego_document.pdf" \
  --output downloaded_document.pdf
```

---

#### GET /api/document/health

Health check for document steganography service.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "document-steganography",
  "embeddingMethod": "Hybrid Dual-Layer Document Steganography",
  "supportedFormats": ["PDF", "TXT"]
}
```

---

### System Endpoints

#### GET /

Root endpoint with API information.

**Response (200 OK):**
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
      "extract": "/api/steganography/extract",
      "download": "/api/steganography/download/{filename}"
    },
    "video": {
      "health": "/api/video/health",
      "embed": "/api/video/embed",
      "extract": "/api/video/extract",
      "download": "/api/video/download/{filename}"
    },
    "audio": {
      "health": "/api/audio/health",
      "embed": "/api/audio/embed",
      "extract": "/api/audio/extract",
      "download": "/api/audio/download/{filename}"
    },
    "document": {
      "health": "/api/document/health",
      "embed": "/api/document/embed",
      "extract": "/api/document/extract",
      "download": "/api/document/download/{filename}"
    }
  }
}
```

---

#### GET /health

Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "SecureStego",
  "version": "1.0.0"
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input parameters |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server-side error |

## Rate Limiting

Currently, rate limiting is not implemented. In production, implement rate limiting to prevent abuse.

## File Size Limits

| Media Type | Max Size |
|------------|----------|
| Image | 50 MB |
| Video | 500 MB |
| Audio | 100 MB |
| Document | 50 MB |
| General | 100 MB |

## Supported Formats

### Images
- PNG
- JPG/JPEG
- HEIC

### Videos
- MP4
- AVI
- MOV

### Audio
- WAV
- MP3
- M4A
- FLAC

### Documents
- PDF
- TXT

## Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Authentication**: Implement API key or JWT authentication
3. **Input Validation**: All inputs are validated server-side
4. **File Size Limits**: Enforce file size limits to prevent DoS
5. **Platform Signature**: All stego files include platform signature for verification
6. **Encryption**: All messages encrypted with Argon2id + AES-256-GCM
7. **Secrets**: Store secrets in environment variables
8. **CORS**: Configure CORS origins properly

## Interactive Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- OpenAPI JSON: `http://localhost:8000/api/openapi.json`
