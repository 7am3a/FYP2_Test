# SecureStego - Image Steganography Module

Complete production-quality implementation of Edge-Based LSB steganography for hiding encrypted messages inside images.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Folder Structure](#folder-structure)
4. [Installation Guide](#installation-guide)
5. [Environment Setup](#environment-setup)
6. [Dependency Installation](#dependency-installation)
7. [Running Backend](#running-backend)
8. [Running Frontend](#running-frontend)
9. [Supported Image Formats](#supported-image-formats)
10. [PNG Conversion Workflow](#png-conversion-workflow)
11. [Edge-Based LSB Workflow](#edge-based-lsb-workflow)
12. [Embedding Process](#embedding-process)
13. [Extraction Process](#extraction-process)
14. [API Documentation](#api-documentation)
15. [Example Requests](#example-requests)
16. [Example Responses](#example-responses)
17. [Capacity Limitations](#capacity-limitations)
18. [Security Notes](#security-notes)
19. [Debugging Guide](#debugging-guide)
20. [Future Improvements](#future-improvements)

---

## Project Overview

SecureStego implements a sophisticated image steganography system that hides encrypted messages inside images using Edge-Based LSB (Least Significant Bit) steganography. This module integrates with the existing double-layer encryption system to provide end-to-end secure communication.

### Key Features

- **Edge-Based LSB Steganography**: Hides data only in edge pixels for minimal visual distortion
- **Canny Edge Detection**: Robust edge detection algorithm for optimal embedding locations
- **Multi-Format Support**: Accepts PNG, JPG, JPEG, and HEIC images
- **PNG Output**: Always outputs lossless PNG format for reliable data extraction
- **Structured Payloads**: Versioned payload format with metadata
- **Capacity Analysis**: Pre-embedding capacity checking
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

### Why Edge-Based Steganography?

Traditional LSB steganography embeds data sequentially across all pixels, which:
- Causes visible artifacts in smooth regions
- Is easily detected by statistical steganalysis
- Degrades image quality significantly

Edge-Based LSB addresses these issues by:
- Hiding data only in edge regions (less visually sensitive)
- Reducing perceptible distortion
- Improving resistance against simple steganalysis
- Better preserving overall image quality

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Upload     │    │   Encrypt    │    │   Download   │       │
│  │   Image      │───▶│   Message    │◀───│  Stego Image│       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend API (FastAPI)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Steganography Routes                        │   │
│  │  POST /api/steganography/embed                           │   │
│  │  POST /api/steganography/extract                         │   │
│  │  GET  /api/steganography/health                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Steganography Service Layer                    │   │
│  │  - Orchestrates embedding/extraction workflow            │   │
│  │  - Manages temporary files                               │   │
│  │  - Provides capacity checking                            │   │
│  │  - Returns comprehensive statistics                      │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Image Processing Modules                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Image      │  │   Image      │  │   Image      │           │
│  │  Validator   │  │  Converter   │  │   Loader     │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐                                               │
│  │   Edge       │                                               │
│  │  Detector    │                                               │
│  └──────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Steganography Modules                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Payload    │  │   Payload    │  │   Edge LSB   │           │
│  │  Serializer  │  │Deserializer  │  │   Embedder   │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐                                               │
│  │   Edge LSB   │                                               │
│  │  Extractor   │                                               │
│  └──────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py                  # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py                   # Pydantic models for API
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── encryption.py                # Encryption API endpoints
│   │   └── steganography.py             # Steganography API endpoints
│   ├── security/
│   │   ├── __init__.py
│   │   └── encryption.py                # Encryption service
│   ├── services/
│   │   ├── __init__.py
│   │   ├── crypto_service.py            # Crypto operations
│   │   └── steganography_service.py     # Steganography orchestration
│   ├── image_processing/                # Image processing modules
│   │   ├── __init__.py
│   │   ├── image_validator.py          # Image validation
│   │   ├── image_converter.py          # Format conversion
│   │   ├── image_loader.py             # Pixel data loading
│   │   └── edge_detector.py            # Canny edge detection
│   ├── steganography/                   # Steganography modules
│   │   ├── __init__.py
│   │   ├── edge_lsb_embedder.py         # Edge-based LSB embedding
│   │   └── edge_lsb_extractor.py        # Edge-based LSB extraction
│   └── utils/                           # Utility modules
│       ├── __init__.py
│       ├── payload_serializer.py        # Payload serialization
│       └── payload_deserializer.py      # Payload deserialization
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment template
├── .gitignore
└── STEGANOGRAPHY_README.md              # This file
```

---

## Installation Guide

### Prerequisites

- **Python 3.8 or higher**
- **Node.js 16 or higher**
- **pip** (Python package manager)
- **npm** or **yarn** (Node.js package manager)

### Step 1: Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Environment Setup

1. Create environment file:
```bash
cp .env.example .env
```

2. Generate a secure server master key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

3. Edit `.env` file and replace `SERVER_MASTER_KEY` with the generated key:
```env
SERVER_MASTER_KEY=your_generated_64_character_hex_key_here
APP_NAME=SecureStego
APP_VERSION=1.0.0
DEBUG=False
API_PREFIX=/api
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
PBKDF2_ITERATIONS=100000
SALT_LENGTH=32
```

### Step 3: Frontend Setup

1. Navigate to project root:
```bash
cd ..
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Edit `.env` file:
```env
VITE_API_URL=http://localhost:8000
```

---

## Dependency Installation

### Python Dependencies (requirements.txt)

```
fastapi==0.109.0              # Modern web framework
uvicorn[standard]==0.27.0     # ASGI server
pydantic==2.5.3               # Data validation
pydantic-settings==2.1.0      # Settings management
python-dotenv==1.0.0          # Environment variables
cryptography==41.0.7          # Encryption library
argon2-cffi==23.1.0           # Password hashing
Pillow==10.2.0                # Image processing
opencv-python==4.9.0.80       # Computer vision
numpy==1.26.3                 # Numerical computing
python-multipart==0.0.6       # Multipart form data
```

### Node.js Dependencies (package.json)

```
react==18.3.1                 # React framework
react-dom==18.3.1             # React DOM
react-router-dom==6.23.1      # Client-side routing
vite==8.0.16                  # Build tool
tailwindcss==3.4.3            # CSS framework
framer-motion==11.2.10        # Animation library
lucide-react==0.379.0         # Icon library
```

---

## Running Backend

### Development Mode

```bash
cd backend
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Verify Backend

- API Documentation: `http://localhost:8000/api/docs`
- Health Check: `http://localhost:8000/health`

---

## Running Frontend

### Development Mode

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Production Build

```bash
npm run build
npm run preview
```

---

## Supported Image Formats

### Input Formats

The steganography system accepts the following image formats:

- **PNG** (Portable Network Graphics)
  - Lossless compression
  - Ideal for steganography
  - No conversion needed

- **JPG/JPEG** (Joint Photographic Experts Group)
  - Lossy compression
  - Automatically converted to PNG
  - Common format for photos

- **HEIC** (High Efficiency Image Container)
  - Modern format (Apple devices)
  - Automatically converted to PNG
  - High compression efficiency

### Output Format

**All output images are PNG format**

Regardless of the input format, the stego image is always saved as PNG to ensure:
- Lossless compression for reliable data extraction
- Consistent pixel values
- Compatibility with LSB steganography

### Naming Convention

Input files are renamed with `_stego` suffix:

- `photo.jpg` → `photo_stego.png`
- `image.jpeg` → `image_stego.png`
- `iphone.heic` → `iphone_stego.png`
- `picture.png` → `picture_stego.png`

---

## PNG Conversion Workflow

### Why Convert to PNG?

1. **Lossless Compression**: PNG preserves exact pixel values
2. **LSB Compatibility**: LSB steganography requires precise pixel control
3. **Consistency**: All operations use the same format
4. **Reliability**: Prevents data corruption from lossy compression

### Conversion Pipeline

```
Upload Image
    ↓
Validate File Extension
    ↓
Validate File Content (MIME type check)
    ↓
Validate File Size (max 10 MB)
    ↓
Validate Image Integrity (can it be opened?)
    ↓
Validate Image Dimensions (10x10 to 10000x10000)
    ↓
Load Image with PIL
    ↓
Convert Mode to RGB if needed
    ↓
Save as Temporary PNG File
    ↓
Verify PNG Integrity
    ↓
Return PNG Path for Processing
```

### Module: image_converter.py

The `ImageConverter` class handles all format conversions:

```python
from app.image_processing.image_converter import image_converter

# Convert any supported format to PNG
png_path, original_format = image_converter.convert_to_png('photo.jpg')
# Returns: ('/tmp/tmpXXXXXX.png', 'JPEG')

# Check if format is supported
is_supported = image_converter.is_supported_format('photo.heic')
# Returns: True

# Get image format
format = image_converter.get_image_format('image.png')
# Returns: 'PNG'

# Cleanup temporary file
image_converter.cleanup_temp_file(png_path)
```

---

## Edge-Based LSB Workflow

### What is Edge-Based LSB?

Edge-Based LSB steganography is a technique that hides data only in the edge pixels of an image, rather than across all pixels. This provides:

- **Reduced Visual Distortion**: Edges are naturally noisy, so changes are less noticeable
- **Improved Security**: Harder to detect with statistical analysis
- **Better Quality**: Smooth regions remain untouched

### Edge Detection Algorithm

We use **Canny Edge Detection**, a multi-stage algorithm:

1. **Noise Reduction**: Gaussian blur to reduce noise
2. **Gradient Calculation**: Sobel operators to find intensity gradients
3. **Non-Maximum Suppression**: Thin edges to single pixel width
4. **Double Thresholding**: Identify strong and weak edges
5. **Edge Tracking**: Connect weak edges to strong edges

### Parameters

```python
CANNY_THRESHOLD1 = 50   # Lower threshold for edge linking
CANNY_THRESHOLD2 = 150  # Upper threshold for strong edges
CANNY_APERTURE_SIZE = 3 # Sobel operator aperture size
```

### Module: edge_detector.py

The `EdgeDetector` class handles edge detection:

```python
from app.image_processing.edge_detector import edge_detector

# Detect edges in an image
edge_map = edge_detector.detect_edges('image.png')
# Returns: numpy array (255 for edges, 0 for non-edges)

# Get edge pixel coordinates
coordinates = edge_detector.get_edge_pixel_coordinates(edge_map)
# Returns: [(row1, col1), (row2, col2), ...]

# Get edge pixel count
count = edge_detector.get_edge_pixel_count(edge_map)
# Returns: 12345

# Calculate capacity
capacity = edge_detector.calculate_capacity(edge_map, bits_per_pixel=3)
# Returns: 37035 (total bits available)
```

---

## Embedding Process

### Complete Embedding Workflow

```
1. Upload Image
   ↓
2. Validate Image (format, size, integrity)
   ↓
3. Convert to PNG (if not already PNG)
   ↓
4. Detect Edges (Canny edge detection)
   ↓
5. Get Edge Pixel Coordinates
   ↓
6. Create Structured Payload
   {
     "version": "1.0",
     "algorithm": "AES-256-GCM",
     "timestamp": "2024-01-01T00:00:00Z",
     "encryptedData": "base64_encoded_encrypted_message"
   }
   ↓
7. Serialize Payload to Binary (JSON + UTF-8)
   ↓
8. Check Capacity
   - Calculate required bits
   - Compare with available edge capacity
   - Reject if insufficient
   ↓
9. Embed Data
   - Add 4-byte header (payload length)
   - Convert to bit stream
   - Embed bits into LSB of edge pixels (3 bits per pixel)
   ↓
10. Save Stego PNG
    ↓
11. Return Stego Image and Statistics
```

### Module: steganography_service.py

The `SteganographyService` orchestrates the embedding:

```python
from app.services.steganography_service import steganography_service

result = steganography_service.embed_message(
    image_path='photo.jpg',
    encrypted_data='base64_encrypted_message',
    algorithm='AES-256-GCM'
)

# Returns:
# {
#     'stegoImagePath': '/tmp/tmpXXXXXX_stego.png',
#     'fileName': 'tmpXXXXXX_stego.png',
#     'originalFormat': 'JPEG',
#     'convertedFormat': 'PNG',
#     'statistics': {
#         'imageWidth': 1920,
#         'imageHeight': 1080,
#         'totalPixels': 2073600,
#         'edgePixels': 123456,
#         'payloadSize': 1024,
#         'headerSize': 4,
#         'totalBitsUsed': 8224,
#         'capacityRemaining': 367881,
#         'capacityUsedPercent': 2.19,
#         'embeddingMethod': 'Edge-Based LSB',
#         'edgeDetectionMethod': 'Canny',
#         'processingTime': 0.456
#     }
# }
```

### Module: edge_lsb_embedder.py

The `EdgeLSBEmbedder` handles the actual embedding:

```python
from app.steganography.edge_lsb_embedder import edge_lsb_embedder

stego_path, stats = edge_lsb_embedder.embed(
    image_path='image.png',
    payload=b'binary_payload_data',
    edge_coordinates=[(row1, col1), (row2, col2), ...]
)
```

### Payload Structure

Payloads are structured JSON objects:

```json
{
  "version": "1.0",
  "algorithm": "AES-256-GCM",
  "timestamp": "2024-01-01T00:00:00Z",
  "encryptedData": "base64_encoded_encrypted_message"
}
```

### Module: payload_serializer.py

The `PayloadSerializer` creates structured payloads:

```python
from app.utils.payload_serializer import payload_serializer

# Create payload
payload = payload_serializer.create_payload(
    encrypted_data='base64_encrypted_message',
    algorithm='AES-256-GCM'
)

# Serialize to binary
binary_data = payload_serializer.serialize_to_binary(payload)
```

---

## Extraction Process

### Complete Extraction Workflow

```
1. Upload Stego PNG Image
   ↓
2. Validate Image (must be PNG)
   ↓
3. Detect Edges (Canny edge detection)
   ↓
4. Get Edge Pixel Coordinates
   ↓
5. Extract Header (4 bytes = payload length)
   ↓
6. Validate Payload Length
   ↓
7. Extract Payload Data
   - Read LSBs from edge pixels
   - Convert bits to bytes
   ↓
8. Deserialize Payload
   - Parse JSON
   - Validate structure
   - Check version
   ↓
9. Extract Encrypted Data
   ↓
10. Return Encrypted Data and Statistics
```

### Module: steganography_service.py

The `SteganographyService` orchestrates extraction:

```python
from app.services.steganography_service import steganography_service

result = steganography_service.extract_message(
    image_path='stego_image.png'
)

# Returns:
# {
#     'encryptedData': 'base64_encoded_encrypted_message',
#     'algorithm': 'AES-256-GCM',
#     'version': '1.0',
#     'timestamp': '2024-01-01T00:00:00Z',
#     'statistics': {
#         'imageWidth': 1920,
#         'imageHeight': 1080,
#         'totalPixels': 2073600,
#         'edgePixels': 123456,
#         'payloadSize': 1024,
#         'headerSize': 4,
#         'totalBitsExtracted': 8224,
#         'extractionMethod': 'Edge-Based LSB',
#         'edgeDetectionMethod': 'Canny',
#         'processingTime': 0.234
#     }
# }
```

### Module: edge_lsb_extractor.py

The `EdgeLSBExtractor` handles the actual extraction:

```python
from app.steganography.edge_lsb_extractor import edge_lsb_extractor

payload, stats = edge_lsb_extractor.extract(
    image_path='stego_image.png',
    edge_coordinates=[(row1, col1), (row2, col2), ...]
)
```

### Module: payload_deserializer.py

The `PayloadDeserializer` handles deserialization:

```python
from app.utils.payload_deserializer import payload_deserializer

# Deserialize from binary
payload = payload_deserializer.deserialize_from_binary(binary_data)

# Extract encrypted data
encrypted_data = payload_deserializer.extract_encrypted_data(payload)

# Extract metadata
algorithm = payload_deserializer.extract_algorithm(payload)
version = payload_deserializer.extract_version(payload)
timestamp = payload_deserializer.extract_timestamp(payload)
```

---

## API Documentation

### POST /api/steganography/embed

Embed an encrypted message into an image.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `image`: Image file (PNG, JPG, JPEG, HEIC)
  - `encryptedMessage`: Base64 encoded encrypted message
  - `algorithm`: Encryption algorithm (default: "AES-256-GCM")

**Response:**
```json
{
  "success": true,
  "fileName": "tmpXXXXXX_stego.png",
  "originalFormat": "JPEG",
  "convertedFormat": "PNG",
  "statistics": {
    "imageWidth": 1920,
    "imageHeight": 1080,
    "totalPixels": 2073600,
    "edgePixels": 123456,
    "payloadSize": 1024,
    "headerSize": 4,
    "totalBitsUsed": 8224,
    "capacityRemaining": 367881,
    "capacityUsedPercent": 2.19,
    "embeddingMethod": "Edge-Based LSB",
    "edgeDetectionMethod": "Canny",
    "processingTime": 0.456
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid image format or insufficient capacity
- `500 Internal Server Error`: Processing error

### POST /api/steganography/extract

Extract an encrypted message from a stego image.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `image`: Stego PNG image file

**Response:**
```json
{
  "success": true,
  "encryptedData": "base64_encoded_encrypted_message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "statistics": {
    "imageWidth": 1920,
    "imageHeight": 1080,
    "totalPixels": 2073600,
    "edgePixels": 123456,
    "payloadSize": 1024,
    "headerSize": 4,
    "totalBitsExtracted": 8224,
    "extractionMethod": "Edge-Based LSB",
    "edgeDetectionMethod": "Canny",
    "processingTime": 0.234
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid image or no hidden data found
- `500 Internal Server Error`: Processing error

### GET /api/steganography/health

Health check for steganography service.

**Response:**
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

### GET /api/steganography/download/{filename}

Download a stego image file.

**Parameters:**
- `filename`: Name of the stego image file

**Response:**
- Content-Type: `image/png`
- Body: Binary image data

---

## Example Requests

### Using curl

#### Embed Message

```bash
curl -X POST "http://localhost:8000/api/steganography/embed" \
  -F "image=@photo.jpg" \
  -F "encryptedMessage=base64_encoded_encrypted_message" \
  -F "algorithm=AES-256-GCM"
```

#### Extract Message

```bash
curl -X POST "http://localhost:8000/api/steganography/extract" \
  -F "image=@stego_image.png"
```

#### Health Check

```bash
curl -X GET "http://localhost:8000/api/steganography/health"
```

#### Download Stego Image

```bash
curl -X GET "http://localhost:8000/api/steganography/download/tmpXXXXXX_stego.png" \
  --output downloaded_stego.png
```

### Using JavaScript/Fetch

#### Embed Message

```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('encryptedMessage', encryptedMessage);
formData.append('algorithm', 'AES-256-GCM');

const response = await fetch('http://localhost:8000/api/steganography/embed', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

#### Extract Message

```javascript
const formData = new FormData();
formData.append('image', stegoImageFile);

const response = await fetch('http://localhost:8000/api/steganography/extract', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

---

## Example Responses

### Successful Embed Response

```json
{
  "success": true,
  "fileName": "tmpabc123_stego.png",
  "originalFormat": "JPEG",
  "convertedFormat": "PNG",
  "statistics": {
    "imageWidth": 1920,
    "imageHeight": 1080,
    "totalPixels": 2073600,
    "edgePixels": 245678,
    "payloadSize": 2048,
    "headerSize": 4,
    "totalBitsUsed": 16416,
    "capacityRemaining": 720618,
    "capacityUsedPercent": 2.23,
    "embeddingMethod": "Edge-Based LSB",
    "edgeDetectionMethod": "Canny",
    "processingTime": 0.523
  }
}
```

### Successful Extract Response

```json
{
  "success": true,
  "encryptedData": "SGVsbG8gV29ybGQh",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:45Z",
  "statistics": {
    "imageWidth": 1920,
    "imageHeight": 1080,
    "totalPixels": 2073600,
    "edgePixels": 245678,
    "payloadSize": 2048,
    "headerSize": 4,
    "totalBitsExtracted": 16416,
    "extractionMethod": "Edge-Based LSB",
    "edgeDetectionMethod": "Canny",
    "processingTime": 0.312
  }
}
```

### Error Response (Insufficient Capacity)

```json
{
  "detail": "Image capacity exceeded. Need 50000 bits but only have 25000 bits. Please upload a larger image.",
  "status": "error"
}
```

### Error Response (Invalid Format)

```json
{
  "detail": "Unsupported image format. Allowed: .png, .jpg, .jpeg, .heic, .heif",
  "status": "error"
}
```

---

## Capacity Limitations

### Capacity Calculation

The steganography capacity depends on:

1. **Image Size**: Larger images have more pixels
2. **Edge Density**: Images with more edges have more embedding locations
3. **Bits Per Pixel**: We use 3 bits per edge pixel (1 per RGB channel)
4. **Header Size**: 4 bytes (32 bits) for payload length header

### Formula

```
Total Capacity (bits) = Edge Pixel Count × 3
Data Capacity (bits) = Total Capacity - 32 (header)
Data Capacity (bytes) = Data Capacity / 8
```

### Example Calculations

#### Small Image (640x480)

- Total pixels: 307,200
- Edge pixels (typical): ~15,000 (5%)
- Total capacity: 45,000 bits
- Data capacity: 44,968 bits = 5,621 bytes
- Can hide: ~5.5 KB of encrypted data

#### Medium Image (1920x1080)

- Total pixels: 2,073,600
- Edge pixels (typical): ~100,000 (5%)
- Total capacity: 300,000 bits
- Data capacity: 299,968 bits = 37,496 bytes
- Can hide: ~36.6 KB of encrypted data

#### Large Image (3840x2160)

- Total pixels: 8,294,400
- Edge pixels (typical): ~400,000 (5%)
- Total capacity: 1,200,000 bits
- Data capacity: 1,199,968 bits = 149,996 bytes
- Can hide: ~146.5 KB of encrypted data

### Factors Affecting Edge Density

- **Image Content**: Photos with textures have more edges than solid colors
- **Complexity**: Complex scenes have more edges than simple ones
- **Contrast**: High contrast images have more defined edges
- **Noise**: Noisy images may have false edges

### Capacity Checking

The system automatically checks capacity before embedding:

```python
# If payload exceeds capacity
if required_bits > available_bits:
    raise ValueError(
        f"Image capacity exceeded. "
        f"Need {required_bits} bits but only have {available_bits} bits. "
        f"Please upload a larger image."
    )
```

---

## Security Notes

### Security Features

1. **Edge-Based Embedding**: Reduces detectability by hiding in edge regions
2. **Structured Payloads**: Includes version and algorithm metadata
3. **Validation**: All inputs are validated before processing
4. **Temporary Files**: Cleaned up after use to prevent data leakage
5. **Error Handling**: Errors don't expose sensitive information

### Security Considerations

1. **Steganalysis Resistance**: Edge-based LSB is more resistant than sequential LSB
2. **Visual Quality**: Minimal distortion makes detection harder
3. **Payload Versioning**: Enables future security improvements
4. **Audit Trail**: Timestamps provide tracking capability

### Limitations

1. **Not Cryptographically Secure**: Steganography is not encryption
2. **Detectable by Advanced Analysis**: Professional steganalysis can detect it
3. **Capacity Limits**: Large messages require large images
4. **Image Dependency**: Edge density varies by image content

### Best Practices

1. **Use High-Resolution Images**: More pixels = more capacity
2. **Use Complex Images**: More edges = more capacity
3. **Combine with Encryption**: Always encrypt before embedding
4. **Use Strong Passwords**: For the encryption layer
5. **Don't Reuse Images**: Each message should use a fresh image

---

## Debugging Guide

### Enable Debug Logging

Set `DEBUG=True` in `.env` file:

```env
DEBUG=True
```

### Common Issues

#### Issue: "Image capacity exceeded"

**Cause**: The encrypted message is too large for the image's edge capacity.

**Solution**:
- Use a larger image
- Use an image with more edge content
- Compress the encrypted message

#### Issue: "Unsupported image format"

**Cause**: The image format is not supported.

**Solution**:
- Convert image to PNG, JPG, JPEG, or HEIC
- Check file extension matches actual format

#### Issue: "Invalid payload format"

**Cause**: The stego image does not contain valid hidden data.

**Solution**:
- Ensure the image was created by this steganography system
- Check the image hasn't been modified after embedding
- Verify the image is in PNG format

#### Issue: "Failed to detect edges"

**Cause**: Edge detection algorithm failed.

**Solution**:
- Check the image is valid and not corrupted
- Try a different image
- Check OpenCV installation

### Logging

All operations are logged with timestamps:

```
2024-01-15 10:30:45 - app.services.steganography_service - INFO - Starting embed workflow for: photo.jpg
2024-01-15 10:30:45 - app.services.steganography_service - INFO - Step 1: Validating image
2024-01-15 10:30:45 - app.image_processing.image_validator - INFO - Image validation passed: photo.jpg
2024-01-15 10:30:45 - app.services.steganography_service - INFO - Step 2: Converting image to PNG
2024-01-15 10:30:46 - app.image_processing.image_converter - INFO - Image converted: JPEG -> PNG
2024-01-15 10:30:46 - app.services.steganography_service - INFO - Step 3: Detecting edges
2024-01-15 10:30:46 - app.image_processing.edge_detector - INFO - Edge detection complete: 123456 edge pixels
2024-01-15 10:30:46 - app.services.steganography_service - INFO - Step 4: Creating structured payload
2024-01-15 10:30:46 - app.utils.payload_serializer - INFO - Payload created: 1024 bytes
2024-01-15 10:30:46 - app.services.steganography_service - INFO - Step 5: Checking capacity
2024-01-15 10:30:46 - app.services.steganography_service - INFO - Capacity check passed: 8224 bits needed, 370368 bits available
2024-01-15 10:30:46 - app.services.steganography_service - INFO - Step 6: Embedding payload
2024-01-15 10:30:47 - app.steganography.edge_lsb_embedder - INFO - Embedded 8224 bits into 2742 edge pixels
2024-01-15 10:30:47 - app.services.steganography_service - INFO - Embed workflow completed in 1.234s
```

### Testing

#### Test Embedding

```python
import requests

# Upload image and embed message
with open('test.jpg', 'rb') as f:
    files = {'image': f}
    data = {
        'encryptedMessage': 'base64_encoded_message',
        'algorithm': 'AES-256-GCM'
    }
    response = requests.post(
        'http://localhost:8000/api/steganography/embed',
        files=files,
        data=data
    )
    print(response.json())
```

#### Test Extraction

```python
import requests

# Upload stego image and extract message
with open('stego.png', 'rb') as f:
    files = {'image': f}
    response = requests.post(
        'http://localhost:8000/api/steganography/extract',
        files=files
    )
    print(response.json())
```

---

## Future Improvements

### Planned Enhancements

1. **Adaptive Edge Detection**
   - Adjust Canny thresholds based on image characteristics
   - Improve edge detection for different image types

2. **Multiple Bit Embedding**
   - Support embedding 2+ bits per channel
   - Trade-off between capacity and quality

3. **Error Correction**
   - Add Reed-Solomon error correction
   - Improve robustness against image modifications

4. **Video Steganography**
   - Extend to video frames
   - Temporal embedding strategies

5. **Audio Steganography**
   - Support for audio files
   - Frequency-domain embedding

6. **Advanced Steganalysis Resistance**
   - Implement statistical matching
   - Add noise injection

7. **Database Integration**
   - Store stego images securely
   - Track usage and expiration

8. **Batch Processing**
   - Support multiple images at once
   - Queue system for large jobs

9. **Performance Optimization**
   - GPU acceleration for edge detection
   - Parallel processing

10. **Web Interface**
    - Direct web-based embedding/extraction
    - No API required for basic use

### Contributing

To contribute to this project:

1. Follow the existing code style
2. Add comprehensive documentation
3. Include unit tests
4. Update this README

---

## License

This project is developed as a Final Year Project.

---

## Contact

For questions or issues:
- Check the API documentation at `/api/docs`
- Review the backend README in `backend/README.md`
- Contact through the Contact page in the application
