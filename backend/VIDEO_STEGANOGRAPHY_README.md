# SecureStego - Video Steganography Module

## Project Overview

SecureStego is a comprehensive steganography system that provides both image and video-based hidden communication. This document specifically covers the **Video Steganography Module**, which implements professional-grade DCT-based video steganography for hiding encrypted messages within video files.

### Key Features

- **DCT-Based Block Steganography**: Uses Discrete Cosine Transform for frequency-domain embedding
- **Multi-Format Support**: Accepts MP4, AVI, and MOV input formats
- **MP4 Output**: All stego videos are output as MP4 for consistency
- **Audio Preservation**: Original audio tracks are preserved during processing
- **Capacity Analysis**: Automatic capacity checking before embedding
- **Frame Selection Strategies**: Multiple strategies for selecting embedding frames
- **Comprehensive Logging**: Detailed logging for debugging and audit trails
- **Modular Architecture**: Clean separation of concerns for maintainability

---

## Video Steganography Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                        │
│  - Video Upload UI                                          │
│  - Message Input                                            │
│  - Password Input                                            │
│  - Encryption Integration                                    │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Video Steganography Routes                     │  │
│  │  - POST /api/video/embed                              │  │
│  │  - POST /api/video/extract                            │  │
│  │  - GET  /api/video/download/{filename}                │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │      Video Steganography Service Layer                │  │
│  │  - Orchestrates entire workflow                       │  │
│  │  - Coordinates all components                         │  │
│  │  - Handles errors and cleanup                         │  │
│  └────────────────────┬─────────────────────────────────┘  │
└───────────────────────┼─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Video      │ │   DCT        │ │   Payload    │
│ Processing   │ │ Steganography│ │  Utilities   │
└──────────────┘ └──────────────┘ └──────────────┘
```

### Module Breakdown

#### 1. Video Processing Module (`app/video_processing/`)

Handles all video file operations:

- **video_validator.py**: Validates video files (format, size, integrity)
- **video_converter.py**: Converts videos to MP4 format
- **frame_extractor.py**: Extracts frames from videos
- **frame_rebuilder.py**: Rebuilds videos from processed frames
- **audio_handler.py**: Extracts and preserves audio tracks

#### 2. DCT Steganography Module (`app/steganography/video/`)

Implements frequency-domain steganography:

- **dct_transform.py**: Performs DCT and inverse DCT transformations
- **dct_embedder.py**: Embeds payload bits into DCT coefficients
- **dct_extractor.py**: Recovers payload bits from DCT coefficients
- **frame_selector.py**: Selects frames for embedding

#### 3. Service Layer (`app/services/`)

Coordinates the entire workflow:

- **video_steganography_service.py**: Orchestrates embedding and extraction

#### 4. API Layer (`app/routes/`)

Provides REST endpoints:

- **video_steganography.py**: Video steganography API endpoints

---

## Complete Workflow Diagram

### Embedding Workflow

```
User Uploads Video
         │
         ▼
┌─────────────────┐
│ Validate Video  │
│ - Check format  │
│ - Check size    │
│ - Check integrity│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Convert to MP4  │
│ - FFmpeg       │
│ - H.264 codec  │
│ - AAC audio    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Extract Audio   │
│ - Save track    │
│ - AAC format    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Extract Frames  │
│ - PNG format    │
│ - All frames    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Select Frames   │
│ - Strategy     │
│ - Capacity     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Serialize      │
│ Payload         │
│ - Add header   │
│ - JSON encode  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ DCT Embedding   │
│ - YCbCr convert │
│ - 8x8 blocks   │
│ - Mid-frequency│
│ - LSB modify   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Rebuild Video   │
│ - From frames   │
│ - Original FPS  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Reattach Audio  │
│ - Sync tracks   │
│ - AAC codec     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Return Stego    │
│ Video           │
└─────────────────┘
```

### Extraction Workflow

```
User Uploads Stego Video
         │
         ▼
┌─────────────────┐
│ Validate Video  │
│ - Check format  │
│ - Check MP4     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Extract Frames  │
│ - PNG format    │
│ - All frames    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ DCT Extraction  │
│ - Try frames    │
│ - Read LSBs     │
│ - Reconstruct   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validate Header │
│ - Magic sig     │
│ - Read length   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Deserialize     │
│ Payload         │
│ - JSON decode   │
│ - Extract data  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Return          │
│ Encrypted Data  │
└─────────────────┘
```

---

## Folder Structure

```
backend/
├── app/
│   ├── config/
│   │   └── settings.py              # Application configuration
│   ├── image_processing/            # Image steganography modules
│   │   ├── edge_detector.py
│   │   ├── image_converter.py
│   │   ├── image_loader.py
│   │   └── image_validator.py
│   ├── models/
│   │   └── schemas.py               # Pydantic models (includes video schemas)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── encryption.py            # Encryption endpoints
│   │   ├── steganography.py         # Image steganography endpoints
│   │   └── video_steganography.py   # Video steganography endpoints
│   ├── security/
│   │   └── encryption.py            # Encryption service
│   ├── services/
│   │   ├── crypto_service.py        # Cryptography operations
│   │   ├── steganography_service.py # Image steganography service
│   │   └── video_steganography_service.py  # Video steganography service
│   ├── steganography/
│   │   ├── __init__.py
│   │   ├── edge_lsb_embedder.py    # Image LSB embedder
│   │   ├── edge_lsb_extractor.py    # Image LSB extractor
│   │   └── video/                  # Video steganography modules
│   │       ├── __init__.py
│   │       ├── dct_transform.py    # DCT transformations
│   │       ├── dct_embedder.py     # DCT embedding
│   │       ├── dct_extractor.py    # DCT extraction
│   │       └── frame_selector.py   # Frame selection
│   ├── utils/
│   │   ├── payload_deserializer.py # Payload deserialization
│   │   └── payload_serializer.py   # Payload serialization
│   ├── video_processing/           # Video processing modules
│   │   ├── __init__.py
│   │   ├── audio_handler.py       # Audio extraction/preservation
│   │   ├── frame_extractor.py     # Frame extraction
│   │   ├── frame_rebuilder.py     # Video reconstruction
│   │   ├── video_converter.py     # MP4 conversion
│   │   └── video_validator.py     # Video validation
│   ├── __init__.py
│   └── main.py                     # FastAPI application
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore
└── README.md                      # This file
```

---

## Installation Instructions

### Prerequisites

1. **Python 3.9 or higher**
2. **FFmpeg** (required for video processing)
3. **Node.js 16+** (for frontend)

### Install FFmpeg

#### Windows
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
# Add to PATH
```

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Verify FFmpeg Installation
```bash
ffmpeg -version
ffprobe -version
```

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env with your configuration
# Set SERVER_MASTER_KEY (64-character hex string)
```

### Frontend Setup

```bash
# Navigate to project root
cd ..

# Install dependencies
npm install

# Start frontend
npm run dev
```

---

## Dependencies

### Python Dependencies (backend/requirements.txt)

```
fastapi==0.109.0              # Web framework
uvicorn[standard]==0.27.0     # ASGI server
pydantic==2.5.3               # Data validation
pydantic-settings==2.1.0      # Settings management
python-dotenv==1.0.0          # Environment variables
cryptography==41.0.7          # Encryption library
argon2-cffi==23.1.0           # Password hashing
Pillow==10.2.0                # Image processing
opencv-python==4.9.0.80       # Computer vision (DCT, frame processing)
numpy==1.26.3                 # Numerical computing
python-multipart==0.0.6       # Multipart form data
```

### System Dependencies

- **FFmpeg**: Video processing (conversion, frame extraction, audio handling)
- **ffprobe**: Video metadata extraction (included with FFmpeg)

### Frontend Dependencies

See `package.json` for frontend dependencies.

---

## Environment Variables

### Backend (.env)

```bash
# Application Settings
APP_NAME=SecureStego
APP_VERSION=1.0.0
DEBUG=True

# API Settings
API_PREFIX=/api
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# Security Settings
SERVER_MASTER_KEY=your_64_character_hex_key_here
```

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:8000
```

---

## Running Backend

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API Documentation:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

---

## Running Frontend

```bash
# From project root
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## Supported Video Formats

### Input Formats

✅ **MP4** - MPEG-4 Part 14
✅ **AVI** - Audio Video Interleave
✅ **MOV** - QuickTime File Format

### Output Format

✅ **MP4** - All output videos are converted to MP4 for consistency

### Conversion Examples

```
movie.mov    → movie_stego.mp4
clip.avi     → clip_stego.mp4
video.mp4    → video_stego.mp4
```

---

## MP4 Conversion Workflow

All uploaded videos undergo mandatory MP4 conversion:

### Why MP4?

- **Universal Compatibility**: Works on all platforms and devices
- **Efficient Compression**: Good quality-to-size ratio
- **Standard Codec**: H.264 video + AAC audio
- **Web-Friendly**: Optimized for streaming
- **Reliable Processing**: FFmpeg has excellent MP4 support

### Conversion Pipeline

```
Upload Video
     │
     ▼
┌─────────────────┐
│ Validate Format │
│ (MP4/AVI/MOV)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Create Temp     │
│ Working Copy    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ FFmpeg Convert  │
│ - Codec: H.264 │
│ - Audio: AAC   │
│ - Preset: medium│
│ - CRF: 23      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Verify MP4      │
│ Integrity       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Return MP4 Path │
└─────────────────┘
```

### FFmpeg Command Used

```bash
ffmpeg -i input_video \
       -c:v libx264 \
       -preset medium \
       -crf 23 \
       -c:a aac \
       -movflags +faststart \
       -y output.mp4
```

---

## DCT-Based Steganography Theory

### What is DCT?

Discrete Cosine Transform (DCT) converts spatial domain data (pixels) to frequency domain data (coefficients). This is the same technique used in JPEG compression.

### Why DCT for Steganography?

1. **Imperceptibility**: Changes in mid-frequency coefficients are less visible to the human eye
2. **Robustness**: Frequency-domain embedding resists compression and filtering
3. **Capacity**: Multiple coefficients per block provide good embedding capacity
4. **Standard**: DCT is well-understood and widely used in image/video processing

### DCT Process

```
Spatial Domain (Pixels)
         │
         ▼
    8x8 Block
         │
         ▼
   2D DCT Transform
         │
         ▼
Frequency Domain (Coefficients)
         │
         ▼
Modify Mid-Frequency Coefficients
         │
         ▼
   Inverse 2D DCT
         │
         ▼
Spatial Domain (Modified Pixels)
```

### Coefficient Frequency Ordering

```
Low Frequencies ──► High Frequencies
DC (0,0)         Very High
│                 │
▼                 ▼
Mid-Frequency ←───┘ (Ideal for embedding)
```

- **DC Coefficient (0,0)**: Represents average brightness - AVOID
- **Low Frequencies**: Visible changes - AVOID
- **Mid Frequencies**: Good balance - USE
- **High Frequencies**: May be lost in compression - AVOID

---

## Frame Selection Strategy

### Available Strategies

#### 1. Fixed Interval (Default)

Selects every Nth frame from the video.

```python
# Example: interval=10
Frames: 0, 10, 20, 30, 40, ...
```

**Pros**: Simple, predictable, evenly distributed
**Cons**: May miss important scenes

#### 2. Uniform Distribution

Spreads frames evenly throughout the entire video.

```python
# Example: 10 frames from 100-frame video
Frames: 0, 10, 20, 30, 40, 50, 60, 70, 80, 90
```

**Pros**: Optimal distribution, uses full video
**Cons**: More complex calculation

#### 3. Password-Derived

Uses password hash to generate deterministic frame sequence.

```python
# Same password always produces same sequence
Frames: [derived from SHA-256(password)]
```

**Pros**: Adds security layer, reproducible
**Cons**: Requires password during extraction

### Configuration

```python
# In API request
frameSelectionStrategy: "fixed_interval"  # or "uniform", "password_derived"
frameInterval: 10  # For fixed_interval strategy
```

---

## DCT Embedding Process

### Step-by-Step

1. **Convert Frame to YCbCr**
   - Separate luminance (Y) from chrominance (Cb, Cr)
   - Human eye less sensitive to luminance changes

2. **Extract Luminance Channel**
   - Use only Y channel for embedding
   - Preserves color information

3. **Split into 8x8 Blocks**
   - Standard JPEG block size
   - Pad if dimensions not divisible by 8

4. **Apply DCT to Each Block**
   - Convert spatial to frequency domain
   - Get 8x8 coefficient matrix

5. **Select Mid-Frequency Coefficients**
   - Use zig-zag pattern to identify mid-frequencies
   - Avoid DC and very high frequencies

6. **Modify Coefficient LSB**
   - Change least significant bit
   - Embed 0 or 1
   - Minimal distortion

7. **Apply Inverse DCT**
   - Convert back to spatial domain
   - Reconstruct modified block

8. **Reconstruct Frame**
   - Assemble all blocks
   - Convert back to RGB

### Coefficient Positions Used

```
Zig-Zag Order (indices 6-20 used):
(0,0)  ← DC (skip)
(0,1) (1,0)  ← Low (skip)
(2,0) (1,1) (0,2)  ← Low-mid
(0,3) (1,2) (2,1) (3,0)  ← Mid (USE)
(4,0) (3,1) (2,2) (1,3) (0,4)  ← Mid (USE)
...  ← Mid-high (USE)
...  ← High (skip)
```

---

## DCT Extraction Process

### Step-by-Step

1. **Convert Frame to YCbCr**
   - Same as embedding process

2. **Extract Luminance Channel**
   - Use only Y channel

3. **Split into 8x8 Blocks**
   - Same block structure as embedding

4. **Apply DCT to Each Block**
   - Get frequency domain coefficients

5. **Extract LSB from Coefficients**
   - Read LSB of selected coefficients
   - Reconstruct bit stream

6. **Convert Bits to Bytes**
   - Group 8 bits into bytes
   - Handle padding if needed

7. **Validate Header**
   - Check magic signature "VIDSTEGO"
   - Read payload length

8. **Extract Payload**
   - Read exact number of bytes
   - Return encrypted data

### Header Structure

```
Header (32 bytes total):
┌─────────────────┬─────────────────┬─────────────────┐
│ Magic Signature │ Payload Length  │ Reserved        │
│ (8 bytes)       │ (4 bytes)       │ (20 bytes)      │
│ "VIDSTEGO"      │ uint32 big-endian│ Future use     │
└─────────────────┴─────────────────┴─────────────────┘
```

---

## Audio Preservation Workflow

### Why Preserve Audio?

- User experience: Stego video should be watchable
- Naturalness: Audio makes video less suspicious
- Completeness: Preserves original video content

### Audio Workflow

```
Original Video
     │
     ▼
┌─────────────────┐
│ Extract Audio   │
│ - AAC codec     │
│ - Temp file     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Process Video   │
│ (Frame embed)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Reattach Audio  │
│ - Sync tracks   │
│ - AAC codec     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Final Stego     │
│ Video           │
└─────────────────┘
```

### FFmpeg Commands

**Extract Audio:**
```bash
ffmpeg -i video.mp4 -vn -acodec aac -y audio.aac
```

**Reattach Audio:**
```bash
ffmpeg -i video_no_audio.mp4 -i audio.aac \
       -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \
       -shortest -y video_with_audio.mp4
```

---

## API Documentation

### Embed Message

**Endpoint:** `POST /api/video/embed`

**Request:** `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| video | File | Yes | Video file (MP4, AVI, MOV) |
| encryptedMessage | string | Yes | Base64 encoded encrypted message |
| algorithm | string | No | Encryption algorithm (default: AES-256-GCM) |
| frameSelectionStrategy | string | No | Frame selection strategy (default: fixed_interval) |
| frameInterval | integer | No | Interval for fixed interval (default: 10) |

**Response:**

```json
{
  "success": true,
  "fileName": "video_stego.mp4",
  "originalFormat": ".avi",
  "convertedFormat": "MP4",
  "statistics": {
    "videoWidth": 1920,
    "videoHeight": 1080,
    "totalFrames": 300,
    "selectedFrames": 30,
    "frameSelectionStrategy": "fixed_interval",
    "frameInterval": 10,
    "payloadSize": 1234,
    "totalBitsEmbedded": 9872,
    "capacityRemaining": 50000,
    "capacityUsedPercent": 16.5,
    "embeddingMethod": "DCT-Based Block Steganography",
    "audioPreserved": true,
    "processingTime": 45.234,
    "debug": {
      "originalFormat": ".avi",
      "convertedFormat": "MP4",
      "resolution": "1920x1080",
      "frameCount": 300,
      "fps": 30.0,
      "duration": 10.0,
      "selectedFrames": [0, 10, 20, 30, 40],
      "dctBlocksUsed": 8100,
      "payloadSize": 1234,
      "capacityUsed": 9872,
      "capacityRemaining": 50000,
      "audioPreserved": true,
      "processingTime": 45.234,
      "embeddingMethod": "DCT-Based Block Steganography"
    }
  }
}
```

### Extract Message

**Endpoint:** `POST /api/video/extract`

**Request:** `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| video | File | Yes | Stego MP4 video file |

**Response:**

```json
{
  "success": true,
  "encryptedData": "base64_encoded_encrypted_message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "statistics": {
    "videoWidth": 1920,
    "videoHeight": 1080,
    "totalFrames": 300,
    "totalBlocks": 8100,
    "payloadSize": 1234,
    "totalBitsExtracted": 9872,
    "extractionMethod": "DCT-Based Block Steganography",
    "processingTime": 12.456,
    "debug": {
      "resolution": "1920x1080",
      "frameCount": 300,
      "fps": 30.0,
      "duration": 10.0,
      "payloadSize": 1234,
      "bitsExtracted": 9872,
      "processingTime": 12.456,
      "extractionMethod": "DCT-Based Block Steganography"
    }
  }
}
```

### Download Stego Video

**Endpoint:** `GET /api/video/download/{filename}`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filename | string | Yes | Name of stego video file |

**Response:** File download (video/mp4)

### Health Check

**Endpoint:** `GET /api/video/health`

**Response:**

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

---

## Request Examples

### Using cURL

#### Embed Message

```bash
curl -X POST http://localhost:8000/api/video/embed \
  -F "video=@/path/to/video.mp4" \
  -F "encryptedMessage=base64_encrypted_message" \
  -F "algorithm=AES-256-GCM" \
  -F "frameSelectionStrategy=fixed_interval" \
  -F "frameInterval=10"
```

#### Extract Message

```bash
curl -X POST http://localhost:8000/api/video/extract \
  -F "video=@/path/to/stego_video.mp4"
```

#### Download Stego Video

```bash
curl -X GET http://localhost:8000/api/video/download/video_stego.mp4 \
  --output downloaded_video.mp4
```

### Using JavaScript (Frontend)

#### Embed Message

```javascript
const formData = new FormData();
formData.append('video', videoFile);
formData.append('encryptedMessage', encryptedMessage);
formData.append('algorithm', 'AES-256-GCM');
formData.append('frameSelectionStrategy', 'fixed_interval');
formData.append('frameInterval', '10');

const response = await fetch('http://localhost:8000/api/video/embed', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

#### Extract Message

```javascript
const formData = new FormData();
formData.append('video', stegoVideoFile);

const response = await fetch('http://localhost:8000/api/video/extract', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result.encryptedData);
```

---

## Capacity Limitations

### Capacity Calculation

```
Total Capacity = (Number of Blocks) × (Coefficients per Block) × (Bits per Coefficient)

Where:
- Number of Blocks = (Width / 8) × (Height / 8) × Selected Frames
- Coefficients per Block = 15 (mid-frequency positions)
- Bits per Coefficient = 1 (LSB only)

Available Payload = Total Capacity - Header Size (32 bytes)
```

### Example Calculation

For a 1920x1080 video with 30 selected frames:

```
Blocks per frame = (1920 / 8) × (1080 / 8) = 240 × 135 = 32,400
Total blocks = 32,400 × 30 = 972,000
Total capacity = 972,000 × 15 × 1 = 14,580,000 bits
Total capacity (bytes) = 1,822,500 bytes
Available payload = 1,822,500 - 32 = 1,822,468 bytes (~1.74 MB)
```

### Capacity Factors

- **Video Resolution**: Higher resolution = more blocks = more capacity
- **Frame Count**: More frames = more capacity
- **Frame Selection**: More selected frames = more capacity
- **Payload Size**: Larger messages require more capacity
- **Header Overhead**: 32 bytes per video (negligible)

### Capacity Error

If payload exceeds capacity:

```json
{
  "detail": "Video capacity exceeded. Need 50000 bits but only have 30000 bits. Please upload a larger video."
}
```

---

## Debugging Guide

### Development Debug Information

The API response includes a `debug` field with detailed information:

```json
{
  "statistics": {
    "debug": {
      "originalFormat": ".avi",
      "convertedFormat": "MP4",
      "resolution": "1920x1080",
      "frameCount": 300,
      "fps": 30.0,
      "duration": 10.0,
      "selectedFrames": [0, 10, 20, 30, 40],
      "dctBlocksUsed": 8100,
      "payloadSize": 1234,
      "capacityUsed": 9872,
      "capacityRemaining": 50000,
      "audioPreserved": true,
      "processingTime": 45.234,
      "embeddingMethod": "DCT-Based Block Steganography"
    }
  }
}
```

### Common Issues

#### 1. FFmpeg Not Found

**Error:** `FFmpeg conversion failed: 'ffmpeg' is not recognized`

**Solution:** Install FFmpeg and add to PATH

#### 2. Capacity Exceeded

**Error:** `Video capacity exceeded`

**Solution:** Use a larger video or reduce payload size

#### 3. Invalid Video Format

**Error:** `Unsupported video format`

**Solution:** Use MP4, AVI, or MOV format

#### 4. Audio Extraction Failed

**Error:** `Audio extraction failed`

**Solution:** Video may not have audio track (this is OK)

#### 5. Frame Extraction Timeout

**Error:** `Frame extraction timed out`

**Solution:** Video may be too long or corrupted

### Logging

All operations are logged with detailed information:

```python
# Backend logs
INFO - Starting video embed workflow for: /path/to/video.mp4
INFO - Step 1: Validating video
INFO - Step 2: Converting video to MP4
INFO - Video converted: .avi -> MP4
INFO - Step 3: Extracting audio track
INFO - Audio extracted: /tmp/video_audio.aac
INFO - Step 4: Extracting frames
INFO - Extracted 300 frames
INFO - Step 5: Creating structured payload
INFO - Payload created: 1234 bytes
INFO - Step 6: Calculating frame capacity
INFO - Step 7: Selecting frames for embedding
INFO - Selected 30 frames for embedding
INFO - Step 8: Embedding payload into selected frames
INFO - Payload embedded: 9872 bits
INFO - Step 9: Rebuilding video from frames
INFO - Video rebuilt: /tmp/rebuilt_video.mp4
INFO - Step 10: Reattaching audio
INFO - Video embed workflow completed in 45.234s
```

### Testing Locally

```bash
# Test video validation
python -c "from app.video_processing.video_validator import video_validator; print(video_validator.validate_file('test.mp4'))"

# Test video conversion
python -c "from app.video_processing.video_converter import video_converter; print(video_converter.convert_to_mp4('test.mp4'))"

# Test frame extraction
python -c "from app.video_processing.frame_extractor import frame_extractor; print(frame_extractor.extract_frames('test.mp4'))"

# Test DCT transform
python -c "import cv2; from app.steganography.video.dct_transform import dct_transform; frame = cv2.imread('frame.png'); print(dct_transform.apply_dct(frame[:8,:8]))"
```

---

## Logging Guide

### Log Levels

- **INFO**: Normal operations (validation, conversion, embedding)
- **WARNING**: Non-critical issues (cleanup failures)
- **ERROR**: Critical errors (processing failures)

### Log Format

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

Example:
```
2024-01-15 10:30:00,123 - app.services.video_steganography_service - INFO - Starting video embed workflow for: /path/to/video.mp4
```

### Log Files

Logs are printed to console. For production, configure file logging in `main.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

# Add file handler
file_handler = RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
```

### Key Log Points

- Video validation start/end
- MP4 conversion start/end
- Audio extraction start/end
- Frame extraction start/end
- Frame selection
- Payload creation
- DCT embedding start/end
- Video reconstruction start/end
- Audio reattachment
- Processing time
- Errors and exceptions

---

## Security Considerations

### Input Validation

- File type validation (MP4, AVI, MOV only)
- File size limits (500 MB max)
- Video duration limits (10 minutes max)
- Resolution validation (minimum 320x240)
- Frame rate validation

### Temporary File Security

- Files created in system temp directory
- Automatic cleanup after processing
- Cleanup on error
- No file persistence beyond session

### Encryption Integration

- Uses existing encryption service (AES-256-GCM)
- Encrypted payload embedded, not plaintext
- Password-based key derivation
- Double-layer encryption (client + server)

### Steganography Security

- DCT-based embedding (harder to detect)
- Mid-frequency coefficients (less visible)
- Minimal coefficient modification (LSB only)
- No detectable patterns
- Deterministic extraction

### API Security

- CORS configuration
- File upload validation
- Error message sanitization
- No sensitive data in logs
- Rate limiting (recommended for production)

---

## Future Enhancements

### Planned Features

1. **Adaptive Frame Selection**: Select frames based on scene complexity
2. **Multi-Frame Distribution**: Distribute payload across multiple frames
3. **Error Correction**: Add Reed-Solomon codes for robustness
4. **Compression**: Compress payload before embedding
5. **Video Quality Options**: Allow quality vs capacity trade-off
6. **Batch Processing**: Process multiple videos simultaneously
7. **Progress Tracking**: WebSocket progress updates
8. **Cloud Storage**: S3/Google Cloud integration
9. **Advanced Codecs**: Support for H.265/VP9
10. **Real-time Processing**: Live video steganography

### Performance Optimizations

1. **Parallel Frame Processing**: Process multiple frames concurrently
2. **GPU Acceleration**: Use CUDA for DCT operations
3. **Caching**: Cache converted videos
4. **Streaming**: Process videos without full extraction
5. **Optimized DCT**: Use faster DCT implementations

### Security Enhancements

1. **Steganalysis Detection**: Detect if video has been analyzed
2. **Anti-Forensics**: Counter steganalysis techniques
3. **Payload Encryption**: Additional encryption layer
4. **Randomized Embedding**: Randomize coefficient selection
5. **Watermarking**: Add invisible watermark for verification

---

## Contributing

### Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings for all functions
- Comment complex logic
- Keep functions focused and small

### Testing

- Add unit tests for each module
- Test edge cases (empty files, large files, corrupted files)
- Test all supported formats
- Test error handling

### Documentation

- Update README for new features
- Add docstrings to new functions
- Update API documentation
- Add examples for new endpoints

---

## License

This project is part of a Final Year Project (FYP). Please refer to the main project LICENSE file.

---

## Contact

For questions or issues, please contact the development team.

---

## Appendix

### A. FFmpeg Reference

#### Common FFmpeg Commands

```bash
# Get video info
ffprobe -v error -show_entries format=duration -show_entries stream=width,height,r_frame_rate -of json video.mp4

# Convert to MP4
ffmpeg -i input.avi -c:v libx264 -preset medium -crf 23 -c:a aac -y output.mp4

# Extract frames
ffmpeg -i video.mp4 -vf "select='not(mod(n,10))'" fps=30 frame_%06d.png

# Rebuild video
ffmpeg -framerate 30 -i frame_%06d.png -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p -y video.mp4

# Extract audio
ffmpeg -i video.mp4 -vn -acodec aac -y audio.aac

# Add audio to video
ffmpeg -i video.mp4 -i audio.aac -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest -y output.mp4
```

### B. DCT Coefficient Zig-Zag Pattern

```
Zig-Zag order for 8x8 DCT block:

 0  1  5  6 14 15 27 28
 2  4  7 13 16 26 29 42
 3  8 12 17 25 30 41 43
 9 11 18 24 31 40 44 53
10 19 23 32 39 45 52 54
20 22 33 38 46 51 55 60
21 34 37 47 50 56 59 61
35 36 48 49 57 58 62 63

Mid-frequency indices: 6-20
```

### C. Payload Structure

```json
{
  "version": "1.0",
  "algorithm": "AES-256-GCM",
  "timestamp": "2024-01-15T10:30:00Z",
  "encryptedData": "base64_encoded_encrypted_message"
}
```

### D. Error Codes

| Error Code | Description |
|------------|-------------|
| 400 | Bad Request (invalid input) |
| 404 | File Not Found |
| 500 | Internal Server Error |

### E. Performance Benchmarks

Typical processing times (1920x1080, 30fps, 10 seconds):

- MP4 Conversion: ~5 seconds
- Frame Extraction: ~10 seconds
- DCT Embedding: ~20 seconds
- Video Rebuild: ~8 seconds
- Audio Reattach: ~2 seconds
- **Total**: ~45 seconds

---

**Last Updated:** January 2024
**Version:** 1.0.0
