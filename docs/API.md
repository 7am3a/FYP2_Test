# SecureStego API Documentation

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL](#base-url)
4. [Response Format](#response-format)
5. [Error Handling](#error-handling)
6. [Encryption Endpoints](#encryption-endpoints)
7. [Image Steganography Endpoints](#image-steganography-endpoints)
8. [Video Steganography Endpoints](#video-steganography-endpoints)
9. [Audio Steganography Endpoints](#audio-steganography-endpoints)
10. [Document Steganography Endpoints](#document-steganography-endpoints)
11. [Health Check Endpoints](#health-check-endpoints)
12. [Rate Limiting](#rate-limiting)
13. [CORS](#cors)

## Overview

SecureStego provides a RESTful API for secure steganography operations. All endpoints follow REST conventions and return JSON responses.

### API Version

- **Current Version**: v1.0
- **Base Path**: `/api`

### Supported Media Types

- **Request**: `application/json`, `multipart/form-data`
- **Response**: `application/json`

## Authentication

Currently, the API does not require authentication. Future versions may implement:
- API key authentication
- JWT token authentication
- OAuth 2.0

## Base URL

### Development
```
http://localhost:8000/api
```

### Production
```
https://api.securestego.com/api
```

## Response Format

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
  "success": false,
  "error": "Error message",
  "errorType": "ExceptionClassName",
  "details": { ... }
}
```

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Internal Server Error |

### Error Types

| Error Type | Description |
|------------|-------------|
| `EncryptionError` | Encryption operation failed |
| `DecryptionError` | Decryption operation failed |
| `InvalidPasswordError` | Password is invalid or incorrect |
| `SteganographyError` | Steganography operation failed |
| `CapacityExceededError` | Payload exceeds media capacity |
| `InvalidMediaError` | Media file is invalid or unsupported |
| `EmbeddingError` | Embedding operation failed |
| `ExtractionError` | Extraction operation failed |
| `NoHiddenDataError` | No hidden data found in media |
| `SignatureVerificationError` | Platform signature verification failed |
| `FileValidationError` | File validation failed |
| `UnsupportedFormatError` | File format is not supported |

## Encryption Endpoints

### Encrypt Message

Encrypt a message using Argon2id key derivation and AES-256-GCM.

**Endpoint**: `POST /api/encryption/encrypt`

**Request Body**:
```json
{
  "message": "plaintext message",
  "password": "user password"
}
```

**Response**:
```json
{
  "success": true,
  "ciphertext": "base64_encoded_ciphertext",
  "salt": "base64_encoded_salt",
  "iv": "base64_encoded_iv",
  "algorithm": "AES-256-GCM",
  "kdf": "Argon2id"
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/encryption/encrypt" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, World!",
    "password": "mySecurePassword123"
  }'
```

### Decrypt Message

Decrypt a message using Argon2id key derivation and AES-256-GCM.

**Endpoint**: `POST /api/encryption/decrypt`

**Request Body**:
```json
{
  "ciphertext": "base64_encoded_ciphertext",
  "password": "user password",
  "salt": "base64_encoded_salt",
  "iv": "base64_encoded_iv"
}
```

**Response**:
```json
{
  "success": true,
  "message": "decrypted plaintext message"
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/encryption/decrypt" \
  -H "Content-Type: application/json" \
  -d '{
    "ciphertext": "base64_encoded_ciphertext",
    "password": "mySecurePassword123",
    "salt": "base64_encoded_salt",
    "iv": "base64_encoded_iv"
  }'
```

### Encryption Health Check

Check the health of the encryption service.

**Endpoint**: `GET /api/encryption/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "encryption",
  "algorithm": "AES-256-GCM",
  "keyDerivation": "Argon2id"
}
```

## Image Steganography Endpoints

### Embed Message in Image

Embed an encrypted message into an image using edge-based LSB steganography.

**Endpoint**: `POST /api/steganography/embed`

**Request**: `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image | File | Yes | Image file (PNG, JPG, JPEG, HEIC) |
| encryptedMessage | String | Yes | Base64 encoded encrypted message |
| algorithm | String | No | Encryption algorithm (default: AES-256-GCM) |

**Response**:
```json
{
  "success": true,
  "fileName": "stego_image.png",
  "originalFormat": "jpg",
  "convertedFormat": "png",
  "statistics": {
    "imageWidth": 1920,
    "imageHeight": 1080,
    "totalPixels": 2073600,
    "edgePixels": 524288,
    "payloadSize": 256,
    "headerSize": 64,
    "totalBitsUsed": 262144,
    "capacityRemaining": 1310720,
    "capacityUsedPercent": 16.67,
    "embeddingMethod": "Edge-Based LSB",
    "edgeDetectionMethod": "Canny",
    "processingTime": 2.345
  }
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/steganography/embed" \
  -F "image=@image.jpg" \
  -F "encryptedMessage=base64_encoded_message" \
  -F "algorithm=AES-256-GCM"
```

### Extract Message from Image

Extract an encrypted message from a stego image.

**Endpoint**: `POST /api/steganography/extract`

**Request**: `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image | File | Yes | Stego PNG image file |

**Response**:
```json
{
  "success": true,
  "encryptedData": "base64_encrypted_message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "statistics": {
    "imageWidth": 1920,
    "imageHeight": 1080,
    "totalPixels": 2073600,
    "edgePixels": 524288,
    "payloadSize": 256,
    "headerSize": 64,
    "totalBitsUsed": 262144,
    "capacityRemaining": 1310720,
    "capacityUsedPercent": 16.67,
    "embeddingMethod": "Edge-Based LSB",
    "edgeDetectionMethod": "Canny",
    "processingTime": 1.234
  }
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/steganography/extract" \
  -F "image=@stego_image.png"
```

### Download Stego Image

Download a stego image file.

**Endpoint**: `GET /api/steganography/download/{filename}`

**Parameters**:
- `filename` (path parameter): Name of the stego image file

**Response**: Binary file (image/png)

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/steganography/download/stego_image.png" \
  --output stego_image.png
```

### Image Steganography Health Check

Check the health of the image steganography service.

**Endpoint**: `GET /api/steganography/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "steganography",
  "method": "Edge-Based LSB",
  "supportedFormats": ["PNG", "JPG", "JPEG", "HEIC"],
  "outputFormat": "PNG",
  "edgeDetectionMethod": "Canny"
}
```

## Video Steganography Endpoints

### Embed Message in Video

Embed an encrypted message into a video using DCT-based steganography.

**Endpoint**: `POST /api/video/embed`

**Request**: `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| video | File | Yes | Video file (MP4, AVI, MOV) |
| encryptedMessage | String | Yes | Base64 encoded encrypted message |
| algorithm | String | No | Encryption algorithm (default: AES-256-GCM) |
| frameSelectionStrategy | String | No | Frame selection strategy (default: fixed_interval) |
| frameInterval | Integer | No | Interval for fixed interval selection (default: 10) |

**Response**:
```json
{
  "success": true,
  "fileName": "stego_video.mp4",
  "originalFormat": "avi",
  "convertedFormat": "mp4",
  "statistics": {
    "videoWidth": 1920,
    "videoHeight": 1080,
    "totalFrames": 300,
    "selectedFrames": 30,
    "frameSelectionStrategy": "fixed_interval",
    "frameInterval": 10,
    "payloadSize": 256,
    "totalBitsEmbedded": 2048,
    "capacityRemaining": 98304,
    "capacityUsedPercent": 2.04,
    "embeddingMethod": "DCT-Based Block Steganography",
    "audioPreserved": true,
    "processingTime": 15.678
  }
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/video/embed" \
  -F "video=@video.mp4" \
  -F "encryptedMessage=base64_encoded_message" \
  -F "frameSelectionStrategy=fixed_interval" \
  -F "frameInterval=10"
```

### Extract Message from Video

Extract an encrypted message from a stego video.

**Endpoint**: `POST /api/video/extract`

**Request**: `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| video | File | Yes | Stego MP4 video file |

**Response**:
```json
{
  "success": true,
  "encryptedData": "base64_encrypted_message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "statistics": {
    "videoWidth": 1920,
    "videoHeight": 1080,
    "totalFrames": 300,
    "totalBlocks": 120000,
    "payloadSize": 256,
    "totalBitsExtracted": 2048,
    "extractionMethod": "DCT-Based Block Steganography",
    "processingTime": 8.456
  }
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/video/extract" \
  -F "video=@stego_video.mp4"
```

### Download Stego Video

Download a stego video file.

**Endpoint**: `GET /api/video/download/{filename}`

**Parameters**:
- `filename` (path parameter): Name of the stego video file

**Response**: Binary file (video/mp4)

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/video/download/stego_video.mp4" \
  --output stego_video.mp4
```

### Video Steganography Health Check

Check the health of the video steganography service.

**Endpoint**: `GET /api/video/health`

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

## Audio Steganography Endpoints

### Embed Message in Audio

Embed an encrypted message into an audio file using randomized LSB steganography.

**Endpoint**: `POST /api/audio/embed`

**Request**: `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| audio | File | Yes | Audio file (WAV, MP3, M4A, FLAC) |
| encryptedMessage | String | Yes | Base64 encoded encrypted message |
| password | String | Yes | Password for sample position generation |
| algorithm | String | No | Encryption algorithm (default: AES-256-GCM) |

**Response**:
```json
{
  "success": true,
  "fileName": "stego_audio.wav",
  "originalFormat": "mp3",
  "convertedFormat": "wav",
  "statistics": {
    "duration": 180.5,
    "channels": 2,
    "sampleRate": 44100,
    "bitDepth": 16,
    "totalSamples": 15897600,
    "payloadSize": 256,
    "headerSize": 64,
    "totalBitsEmbedded": 2048,
    "capacityRemaining": 47732800,
    "capacityUsedPercent": 0.004,
    "embeddingMethod": "Randomized WAV LSB",
    "processingTime": 3.456
  }
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/audio/embed" \
  -F "audio=@audio.mp3" \
  -F "encryptedMessage=base64_encoded_message" \
  -F "password=myPassword123"
```

### Extract Message from Audio

Extract an encrypted message from a stego audio file.

**Endpoint**: `POST /api/audio/extract`

**Request**: `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| audio | File | Yes | Stego WAV audio file |
| password | String | Yes | Password for sample position generation |

**Response**:
```json
{
  "success": true,
  "encryptedData": "base64_encrypted_message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "statistics": {
    "duration": 180.5,
    "channels": 2,
    "sampleRate": 44100,
    "bitDepth": 16,
    "totalSamples": 15897600,
    "payloadSize": 256,
    "headerSize": 64,
    "totalBitsExtracted": 2048,
    "capacityRemaining": 47732800,
    "capacityUsedPercent": 0.004,
    "extractionMethod": "Randomized WAV LSB",
    "processingTime": 2.123
  }
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/audio/extract" \
  -F "audio=@stego_audio.wav" \
  -F "password=myPassword123"
```

### Download Stego Audio

Download a stego audio file.

**Endpoint**: `GET /api/audio/download/{filename}`

**Parameters**:
- `filename` (path parameter): Name of the stego audio file

**Response**: Binary file (audio/wav)

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/audio/download/stego_audio.wav" \
  --output stego_audio.wav
```

### Audio Steganography Health Check

Check the health of the audio steganography service.

**Endpoint**: `GET /api/audio/health`

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

## Document Steganography Endpoints

### Embed Message in Document

Embed an encrypted message into a document using hybrid dual-layer steganography.

**Endpoint**: `POST /api/document/embed`

**Request**: `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| document | File | Yes | Document file (PDF or TXT) |
| encryptedMessage | String | Yes | Base64 encoded encrypted message |
| algorithm | String | No | Encryption algorithm (default: AES-256-GCM) |
| textMethod | String | No | Text embedding method (default: invisible_character) |
| useImages | Boolean | No | Use image steganography for PDFs (default: true) |

**Response**:
```json
{
  "success": true,
  "fileName": "stego_document.pdf",
  "documentType": "pdf",
  "statistics": {
    "pageCount": 10,
    "textBlocks": 150,
    "imageCount": 5,
    "payloadSize": 256,
    "textPayloadSize": 200,
    "imagePayloadSize": 56,
    "textCapacityBits": 50000,
    "imageCapacityBits": 100000,
    "totalCapacityBits": 150000,
    "capacityUsedPercent": 1.36,
    "embeddingMethod": "Hybrid Dual-Layer Document Steganography",
    "textMethod": "invisible_character",
    "useImages": true,
    "processingTime": 5.678
  }
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/document/embed" \
  -F "document=@document.pdf" \
  -F "encryptedMessage=base64_encoded_message" \
  -F "textMethod=invisible_character" \
  -F "useImages=true"
```

### Extract Message from Document

Extract an encrypted message from a stego document.

**Endpoint**: `POST /api/document/extract`

**Request**: `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| document | File | Yes | Stego document file (PDF or TXT) |

**Response**:
```json
{
  "success": true,
  "encryptedData": "base64_encrypted_message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "statistics": {
    "pageCount": 10,
    "textBlocks": 150,
    "imageCount": 5,
    "payloadSize": 256,
    "textPayloadSize": 200,
    "imagePayloadSize": 56,
    "extractionMethod": "Hybrid Dual-Layer Document Steganography",
    "processingTime": 4.321
  }
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/document/extract" \
  -F "document=@stego_document.pdf"
```

### Download Stego Document

Download a stego document file.

**Endpoint**: `GET /api/document/download/{filename}`

**Parameters**:
- `filename` (path parameter): Name of the stego document file

**Response**: Binary file (application/pdf or text/plain)

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/document/download/stego_document.pdf" \
  --output stego_document.pdf
```

### Document Steganography Health Check

Check the health of the document steganography service.

**Endpoint**: `GET /api/document/health`

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

## Health Check Endpoints

### Root Health Check

Check the health of the entire API.

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "SecureStego API",
  "version": "1.0.0"
}
```

### Root Endpoint

Get API information.

**Endpoint**: `GET /api/`

**Response**:
```json
{
  "message": "SecureStego API",
  "version": "1.0.0",
  "docs": "/api/docs"
}
```

## Rate Limiting

Currently, the API does not implement rate limiting. Future versions may include:
- Per-IP rate limiting
- Per-endpoint rate limiting
- Configurable rate limits

## CORS

The API implements CORS with the following configuration:

### Allowed Origins

- `http://localhost:5173` (Development)
- `http://localhost:3000` (Development)

### Allowed Methods

- `GET`
- `POST`
- `PUT`
- `DELETE`
- `OPTIONS`

### Allowed Headers

- `Content-Type`
- `Authorization`
- `X-Requested-With`

## Interactive Documentation

Interactive API documentation is available via Swagger UI:

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **OpenAPI JSON**: `http://localhost:8000/api/openapi.json`

## SDKs and Libraries

### JavaScript/TypeScript

```javascript
import { encryptMessage, embedMessage } from '@securestego/sdk';

// Encrypt message
const encrypted = await encryptMessage(message, password);

// Embed in image
const stego = await embedMessage(imageFile, encrypted.ciphertext);
```

### Python

```python
from securestego import SecureStegoClient

client = SecureStegoClient(api_url="http://localhost:8000")

# Encrypt message
encrypted = client.encrypt_message(message, password)

# Embed in image
stego = client.embed_message(image_file, encrypted.ciphertext)
```

## Support

For API support:
- Check the interactive documentation at `/api/docs`
- Review error messages for troubleshooting
- Contact through the Contact page in the application
