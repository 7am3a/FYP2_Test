# Audio Steganography Module - Complete Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Audio Steganography Architecture](#audio-steganography-architecture)
3. [Complete Workflow Diagram](#complete-workflow-diagram)
4. [Folder Structure](#folder-structure)
5. [Installation Guide](#installation-guide)
6. [Dependencies](#dependencies)
7. [Environment Variables](#environment-variables)
8. [Running Backend](#running-backend)
9. [Running Frontend](#running-frontend)
10. [Supported Audio Formats](#supported-audio-formats)
11. [WAV Normalization Workflow](#wav-normalization-workflow)
12. [Randomized LSB Theory](#randomized-lsb-theory)
13. [Sample Selection Strategy](#sample-selection-strategy)
14. [Embedding Workflow](#embedding-workflow)
15. [Extraction Workflow](#extraction-workflow)
16. [Payload Header Structure](#payload-header-structure)
17. [Capacity Analysis](#capacity-analysis)
18. [Verification Workflow](#verification-workflow)
19. [API Documentation](#api-documentation)
20. [Request Examples](#request-examples)
21. [Response Examples](#response-examples)
22. [Debugging Guide](#debugging-guide)
23. [Logging Guide](#logging-guide)
24. [Security Considerations](#security-considerations)
25. [Known Limitations](#known-limitations)
26. [Future Enhancements](#future-enhancements)

---

## Project Overview

The Audio Steganography Module is a professional-grade implementation of audio steganography for the SecureStego project. It enables users to hide encrypted messages within audio files using randomized Least Significant Bit (LSB) steganography.

### Key Features

- **Multiple Format Support**: Accepts WAV, MP3, M4A, and FLAC audio files
- **WAV Normalization**: All audio is converted to WAV for processing
- **Randomized LSB**: Uses password-derived deterministic random sample selection
- **Capacity Analysis**: Pre-embedding capacity checking prevents failures
- **Integrity Verification**: Automatic verification after embedding
- **Comprehensive Logging**: Detailed logging for all operations
- **Debug Panel**: Development diagnostics panel for troubleshooting
- **Modular Architecture**: Clean separation of concerns for maintainability

### Integration with Existing System

The audio steganography module integrates seamlessly with:
- Existing encryption system (AES-256-GCM with PBKDF2)
- Existing payload serialization/deserialization
- Existing API patterns and logging architecture
- Existing Pydantic schema patterns

---

## Audio Steganography Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     API Layer (Routes)                      │
│  - audio_steganography.py                                   │
│  - POST /api/audio/embed                                    │
│  - POST /api/audio/extract                                  │
└────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Service Layer                              │
│  - audio_steganography_service.py                           │
│  - Orchestrates all components                               │
│  - Manages workflow coordination                             │
└────────────────────────┬────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│ Audio Processing │ │ Steganography│ │  Payload Utils   │
│                  │ │              │ │                  │
│ - validator      │ │ - selector   │ │ - serializer     │
│ - converter      │ │ - embedder   │ │ - deserializer   │
│ - loader         │ │ - extractor  │ │                  │
│ - writer         │ │              │ │                  │
└──────────────────┘ └──────────────┘ └──────────────────┘
```

### Module Responsibilities

#### Audio Processing Module (`audio_processing/`)

- **audio_validator.py**: Validates audio file format, integrity, and parameters
- **audio_converter.py**: Converts various formats to WAV using FFmpeg
- **audio_loader.py**: Loads audio samples from WAV files
- **audio_writer.py**: Generates WAV output files from modified samples

#### Steganography Module (`steganography/audio/`)

- **sample_selector.py**: Generates deterministic randomized sample positions
- **audio_lsb_embedder.py**: Embeds payload bits into audio samples
- **audio_lsb_extractor.py**: Extracts payload bits from audio samples

#### Service Layer (`services/`)

- **audio_steganography_service.py**: Orchestrates the complete workflow

#### API Layer (`routes/`)

- **audio_steganography.py**: Provides REST API endpoints

---

## Complete Workflow Diagram

### Embedding Workflow

```
User Uploads Audio
        │
        ▼
┌───────────────────────┐
│ Validate Audio Format │
│ - Check extension     │
│ - Verify signature    │
│ - Check corruption    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Convert to WAV        │
│ - Use FFmpeg          │
│ - Standardize params  │
│ - Create temp file    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Load Audio Samples    │
│ - Parse WAV header    │
│ - Extract samples     │
│ - Get metadata        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Serialize Payload     │
│ - Add metadata        │
│ - Convert to JSON    │
│ - Encode to bytes    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Calculate Capacity    │
│ - Total samples      │
│ - Available capacity │
│ - Required capacity  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Generate Positions    │
│ - Hash password       │
│ - Derive seed         │
│ - Generate positions  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Embed Payload         │
│ - Add header          │
│ - Convert to bits     │
│ - Embed at positions  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Verify Embedding      │
│ - Extract bits        │
│ - Compare with original│
│ - Confirm integrity   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Generate Stego WAV    │
│ - Write WAV file      │
│ - Add proper header   │
│ - Save to temp        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Return Response       │
│ - File path           │
│ - Statistics          │
│ - Debug info          │
└───────────────────────┘
```

### Extraction Workflow

```
User Uploads Stego Audio
        │
        ▼
┌───────────────────────┐
│ Validate Audio Format │
│ - Must be WAV         │
│ - Check integrity     │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Load Audio Samples    │
│ - Parse WAV header    │
│ - Extract samples     │
│ - Get metadata        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Generate Positions    │
│ - Hash password       │
│ - Derive seed         │
│ - Generate positions  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Extract Header        │
│ - Get first positions │
│ - Extract LSB bits    │
│ - Parse header        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Extract Payload       │
│ - Get full positions  │
│ - Extract LSB bits    │
│ - Convert to bytes   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Deserialize Payload   │
│ - Remove header       │
│ - Parse JSON          │
│ - Validate structure │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Return Response       │
│ - Encrypted data      │
│ - Statistics          │
│ - Debug info          │
└───────────────────────┘
```

---

## Folder Structure

```
backend/
├── app/
│   ├── audio_processing/
│   │   ├── __init__.py
│   │   ├── audio_validator.py      # Audio file validation
│   │   ├── audio_converter.py      # Format conversion to WAV
│   │   ├── audio_loader.py         # Sample loading from WAV
│   │   └── audio_writer.py         # WAV file generation
│   │
│   ├── steganography/
│   │   ├── audio/
│   │   │   ├── __init__.py
│   │   │   ├── sample_selector.py  # Randomized position generation
│   │   │   ├── audio_lsb_embedder.py  # LSB embedding
│   │   │   └── audio_lsb_extractor.py # LSB extraction
│   │   │
│   │   └── ... (existing image/video steganography)
│   │
│   ├── services/
│   │   ├── audio_steganography_service.py  # Workflow orchestration
│   │   └── ... (existing services)
│   │
│   ├── routes/
│   │   ├── audio_steganography.py  # API endpoints
│   │   └── ... (existing routes)
│   │
│   ├── models/
│   │   └── schemas.py              # Pydantic schemas (updated)
│   │
│   └── main.py                     # Application entry (updated)
│
├── requirements.txt                # Dependencies (updated)
└── AUDIO_STEGANOGRAPHY_README.md   # This documentation
```

---

## Installation Guide

### Prerequisites

1. **Python 3.8 or higher**
2. **FFmpeg** (required for audio conversion)
3. **Git** (for cloning the repository)

### Step 1: Install FFmpeg

#### Windows

```bash
# Download from https://ffmpeg.org/download.html
# Extract and add to system PATH
# Verify installation:
ffmpeg -version
```

#### macOS

```bash
brew install ffmpeg
# Verify installation:
ffmpeg -version
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install ffmpeg
# Verify installation:
ffmpeg -version
```

### Step 2: Clone Repository

```bash
git clone <repository-url>
cd FYP-2\ project/backend
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your configuration
# Required: SERVER_MASTER_KEY (64-character hex)
```

---

## Dependencies

### Python Packages

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0
cryptography==41.0.7
argon2-cffi==23.1.0
Pillow==10.2.0
opencv-python==4.9.0.80
numpy==1.26.3
python-multipart==0.0.6
PyMuPDF==1.23.8
python-magic==0.4.27
```

### System Dependencies

- **FFmpeg**: Required for audio format conversion
  - Windows: Download from official site
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

---

## Environment Variables

### Required Variables

```env
# Server Master Key (64-character hex for AES-256)
SERVER_MASTER_KEY=your_64_character_hex_key_here

# Optional: PBKDF2 iterations (default: 100000)
PBKDF2_ITERATIONS=100000

# Optional: Salt length (default: 32)
SALT_LENGTH=32

# Optional: Debug mode (default: False)
DEBUG=False

# Optional: API prefix (default: /api)
API_PREFIX=/api

# Optional: CORS origins (default: localhost)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Generating Server Master Key

```python
import secrets

# Generate 64-character hex key (32 bytes)
key = secrets.token_hex(32)
print(key)
```

---

## Running Backend

### Development Mode

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Verify Backend is Running

```bash
# Check health endpoint
curl http://localhost:8000/health

# Check API documentation
# Open browser at: http://localhost:8000/api/docs
```

---

## Running Frontend

### Development Mode

```bash
cd ../
npm install
npm run dev
```

### Production Build

```bash
npm run build
npm run preview
```

---

## Supported Audio Formats

### Input Formats

✅ **WAV** - Uncompressed audio format (preferred)

✅ **MP3** - Compressed audio format

✅ **M4A** - Apple audio format

✅ **FLAC** - Lossless compressed audio format

### Output Format

All generated stego audio files are **WAV** format:

```
song.mp3 → song_stego.wav
recording.m4a → recording_stego.wav
music.flac → music_stego.wav
audio.wav → audio_stego.wav
```

### Format Specifications

| Format | Bit Depth | Sample Rate | Channels |
|--------|-----------|-------------|----------|
| WAV    | 16-bit    | 44.1 kHz    | Stereo   |
| MP3    | Variable  | Variable    | Variable |
| M4A    | Variable  | Variable    | Variable |
| FLAC   | Variable  | Variable    | Variable |

**Note**: All input formats are converted to 16-bit, 44.1 kHz, stereo WAV for processing.

---

## WAV Normalization Workflow

### Why WAV Normalization?

1. **Uncompressed Format**: WAV provides raw sample access
2. **Consistency**: Ensures uniform processing regardless of input
3. **Quality**: Prevents loss from multiple compression cycles
4. **Reliability**: Well-documented and stable format
5. **Capacity**: Maximizes available samples for embedding

### Normalization Pipeline

```
Input Audio (any format)
        │
        ▼
┌───────────────────────┐
│ Format Validation     │
│ - Check extension     │
│ - Verify signature    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ FFmpeg Conversion     │
│ - Input: any format   │
│ - Codec: PCM S16LE    │
│ - Sample Rate: 44100  │
│ - Channels: 2         │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ WAV Output            │
│ - 16-bit samples      │
│ - 44.1 kHz rate       │
│ - Stereo channels     │
│ - PCM encoding        │
└───────────┬───────────┘
            │
            ▼
Working WAV Copy (for steganography)
```

### FFmpeg Conversion Command

```bash
ffmpeg -y -i input.mp3 -acodec pcm_s16le -ar 44100 -ac 2 output.wav
```

**Parameters**:
- `-y`: Overwrite output if exists
- `-i input.mp3`: Input file
- `-acodec pcm_s16le`: 16-bit little-endian PCM
- `-ar 44100`: Sample rate 44.1 kHz
- `-ac 2`: Stereo channels
- `output.wav`: Output file

---

## Randomized LSB Theory

### Why Randomized LSB?

**Sequential LSB Problems**:
- Predictable embedding pattern
- Easily detected by steganalysis
- Concentrates changes in one area
- Higher risk of audible distortion

**Randomized LSB Advantages**:
- Unpredictable embedding pattern
- Resistant to steganalysis
- Distributes changes across entire file
- Minimizes audible distortion
- Enhanced security

### Deterministic Randomness

The same password must always generate the same sample positions to ensure reliable extraction.

**Algorithm**:
```
Password
    │
    ▼
SHA-256 Hash
    │
    ▼
64-bit Seed
    │
    ▼
Deterministic RNG (numpy)
    │
    ▼
Sample Positions
```

### Security Properties

1. **Password-Derived**: Positions depend on user password
2. **Deterministic**: Same password = same positions
3. **Randomized**: Positions appear random to analysis
4. **Unique**: No duplicate positions
5. **Distributed**: Positions spread across entire audio

---

## Sample Selection Strategy

### Position Generation Algorithm

```python
def generate_sample_positions(password, total_samples, num_positions):
    # Step 1: Hash password to create seed
    seed = sha256(password.encode()).digest()[:8]
    
    # Step 2: Initialize deterministic RNG
    np.random.seed(seed)
    
    # Step 3: Generate all possible positions
    all_positions = np.arange(total_samples)
    
    # Step 4: Randomly shuffle
    np.random.shuffle(all_positions)
    
    # Step 5: Select first N positions
    selected = all_positions[:num_positions]
    
    # Step 6: Sort for predictable order
    return np.sort(selected)
```

### Position Distribution

- **Uniform Distribution**: Positions evenly distributed
- **No Clustering**: Avoids concentration in one area
- **Full Coverage**: Uses entire audio file
- **Deterministic**: Same password = same positions

### Capacity Calculation

```
Total Samples = Duration × Sample Rate × Channels
Available Bits = Total Samples - Header Size
Payload Capacity = Available Bits / 8
```

**Example**:
- Duration: 60 seconds
- Sample Rate: 44,100 Hz
- Channels: 2
- Total Samples: 5,292,000
- Header Size: 9 bytes = 72 bits
- Available Bits: 5,291,928
- Payload Capacity: ~661 KB

---

## Embedding Workflow

### Step-by-Step Process

#### 1. Audio Validation

```python
is_valid, error = audio_validator.validate_file(audio_path)
if not is_valid:
    raise ValueError(error)
```

**Checks**:
- File exists and readable
- Supported format (WAV, MP3, M4A, FLAC)
- Valid file signature
- File size reasonable
- Format-specific structure

#### 2. WAV Conversion

```python
temp_wav_path, original_format = audio_converter.convert_to_wav(audio_path)
```

**Process**:
- Uses FFmpeg for conversion
- Standardizes to 16-bit, 44.1 kHz, stereo
- Creates temporary working copy
- Returns path and original format

#### 3. Sample Loading

```python
samples, metadata = audio_loader.load_wav_samples(temp_wav_path)
```

**Metadata Includes**:
- Sample rate
- Number of channels
- Bit depth
- Total samples
- Duration

#### 4. Payload Serialization

```python
payload_dict = payload_serializer.create_payload(
    encrypted_data=encrypted_message,
    algorithm="AES-256-GCM"
)
payload_binary = payload_serializer.serialize_to_binary(payload_dict)
```

**Payload Structure**:
```json
{
    "version": "1.0",
    "algorithm": "AES-256-GCM",
    "timestamp": "2024-01-01T00:00:00Z",
    "encryptedData": "base64_encoded_encrypted_message"
}
```

#### 5. Capacity Check

```python
capacity_info = audio_lsb_embedder.calculate_capacity(total_samples)
required_bits = (payload_size * 8) + (header_size * 8)

if required_bits > capacity_info['availableCapacityBits']:
    raise ValueError("Insufficient capacity")
```

#### 6. Position Generation

```python
positions = sample_selector.generate_bit_positions(
    password=password,
    total_samples=total_samples,
    num_bits=required_bits
)
```

#### 7. LSB Embedding

```python
stego_samples, stats = audio_lsb_embedder.embed(
    samples=samples,
    payload=payload_binary,
    positions=positions
)
```

**Process**:
- Adds header to payload
- Converts to bit stream
- Embeds bits at randomized positions
- Modifies LSB of each sample

#### 8. Integrity Verification

```python
# Extract embedded bits
extracted_bits = extract_lsb(stego_samples, positions)

# Compare with original
if extracted_bits == original_bits:
    verification_passed = True
```

#### 9. Stego WAV Generation

```python
stego_path = audio_writer.create_stego_wav(
    samples=stego_samples,
    original_path=audio_path,
    metadata=metadata
)
```

---

## Extraction Workflow

### Step-by-Step Process

#### 1. Audio Validation

```python
is_valid, error = audio_validator.validate_file(audio_path)
if not is_valid:
    raise ValueError(error)

# Must be WAV for extraction
if file_ext != '.wav':
    raise ValueError("Only WAV files supported for extraction")
```

#### 2. Sample Loading

```python
samples, metadata = audio_loader.load_wav_samples(audio_path)
```

#### 3. Header Extraction

```python
# Generate positions for header
header_positions = sample_selector.generate_bit_positions(
    password=password,
    total_samples=total_samples,
    num_bits=header_size * 8
)

# Extract header bits
header_bits = extract_lsb(samples, header_positions)
header_bytes = bits_to_bytes(header_bits)

# Parse header to get payload length
payload_length = parse_header(header_bytes)
```

#### 4. Full Payload Extraction

```python
# Generate positions for full payload
total_bits = (header_size + payload_length) * 8
full_positions = sample_selector.generate_bit_positions(
    password=password,
    total_samples=total_samples,
    num_bits=total_bits
)

# Extract payload bits
payload_bits = extract_lsb(samples, full_positions)
payload_bytes = bits_to_bytes(payload_bits)

# Remove header
actual_payload = payload_bytes[header_size:]
```

#### 5. Payload Deserialization

```python
payload_dict = payload_deserializer.deserialize_from_binary(actual_payload)
encrypted_data = payload_deserializer.extract_encrypted_data(payload_dict)
```

---

## Payload Header Structure

### Header Format

```
┌─────────────────────────────────────────┐
│ MAGIC SIGNATURE (4 bytes)              │
│ "STEG"                                  │
├─────────────────────────────────────────┤
│ VERSION (1 byte)                        │
│ 1 (current version)                     │
├─────────────────────────────────────────┤
│ PAYLOAD LENGTH (4 bytes)               │
│ Big-endian integer                      │
├─────────────────────────────────────────┤
│ PAYLOAD DATA (variable)                │
│ Actual encrypted payload                │
└─────────────────────────────────────────┘
```

### Header Size

- **Total**: 9 bytes
- **Magic**: 4 bytes
- **Version**: 1 byte
- **Length**: 4 bytes
- **Data**: Variable

### Header Parsing

```python
def parse_header(header_bytes):
    magic = header_bytes[:4]
    if magic != b'STEG':
        raise ValueError("Invalid magic signature")
    
    version = header_bytes[4]
    payload_length = int.from_bytes(header_bytes[5:9], byteorder='big')
    
    return payload_length
```

---

## Capacity Analysis

### Capacity Calculation

```python
def calculate_capacity(total_samples):
    total_capacity_bits = total_samples  # 1 bit per sample
    header_bits = 9 * 8  # 9 bytes * 8 bits
    available_bits = total_capacity_bits - header_bits
    available_bytes = available_bits // 8
    
    return {
        'totalSamples': total_samples,
        'totalCapacityBits': total_capacity_bits,
        'headerSizeBits': header_bits,
        'availableCapacityBits': available_bits,
        'availableCapacityBytes': available_bytes
    }
```

### Capacity Examples

| Duration | Samples | Available Capacity |
|----------|---------|-------------------|
| 10 sec   | 882,000 | ~110 KB          |
| 30 sec   | 2,646,000 | ~330 KB       |
| 60 sec   | 5,292,000 | ~661 KB       |
| 120 sec  | 10,584,000 | ~1.3 MB      |
| 300 sec  | 26,460,000 | ~3.3 MB      |

**Note**: Capacity based on 44.1 kHz, stereo, 16-bit audio.

### Capacity Check Before Embedding

```python
required_bits = (payload_size * 8) + (header_size * 8)
available_bits = capacity_info['availableCapacityBits']

if required_bits > available_bits:
    raise ValueError(
        f"Audio capacity exceeded. "
        f"Need {required_bits} bits but only have {available_bits} bits. "
        f"Please upload a longer audio file."
    )
```

---

## Verification Workflow

### Why Verification?

- Ensures embedding was successful
- Detects corruption early
- Provides confidence in output
- Prevents returning invalid files

### Verification Process

```python
def verify_embedding(stego_samples, original_bits, positions):
    # Extract bits from embedded positions
    extracted_bits = []
    for position in positions:
        sample = stego_samples[position]
        bit = sample & 1  # Extract LSB
        extracted_bits.append(bit)
    
    # Compare with original
    if extracted_bits == original_bits:
        return True
    else:
        return False
```

### Verification Statistics

```python
statistics = {
    'verificationStatus': 'PASSED',
    'bitsEmbedded': total_bits,
    'bitsVerified': total_bits,
    'mismatches': 0,
    'distortion': calculate_distortion(original, stego)
}
```

---

## API Documentation

### Endpoints

#### 1. POST /api/audio/embed

Embed an encrypted message into an audio file.

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - `audio`: Audio file (WAV, MP3, M4A, FLAC)
  - `encryptedMessage`: Base64 encoded encrypted message
  - `password`: Password for sample position generation
  - `algorithm`: Encryption algorithm (default: AES-256-GCM)

**Response**:
```json
{
    "success": true,
    "fileName": "audio_stego.wav",
    "originalFormat": "mp3",
    "convertedFormat": "WAV",
    "statistics": {
        "duration": 60.5,
        "channels": 2,
        "sampleRate": 44100,
        "bitDepth": 16,
        "totalSamples": 5292000,
        "payloadSize": 1024,
        "headerSize": 9,
        "totalBitsEmbedded": 8264,
        "capacityRemaining": 5283736,
        "capacityUsedPercent": 0.1563,
        "embeddingMethod": "Randomized WAV LSB",
        "processingTime": 2.543
    },
    "debug": {
        "originalFormat": "mp3",
        "convertedFormat": "WAV",
        "duration": 60.5,
        "channels": 2,
        "sampleRate": 44100,
        "bitDepth": 16,
        "totalSamples": 5292000,
        "availableCapacityBytes": 660467,
        "usedCapacityBytes": 1024,
        "remainingCapacityBytes": 659443,
        "embeddingMethod": "Randomized WAV LSB",
        "payloadSize": 1024,
        "verificationStatus": "PASSED",
        "processingTime": 2.543
    }
}
```

#### 2. POST /api/audio/extract

Extract an encrypted message from a stego audio file.

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - `audio`: Stego WAV audio file
  - `password`: Password for sample position generation

**Response**:
```json
{
    "success": true,
    "encryptedData": "base64_encoded_encrypted_message",
    "algorithm": "AES-256-GCM",
    "version": "1.0",
    "timestamp": "2024-01-01T00:00:00Z",
    "statistics": {
        "duration": 60.5,
        "channels": 2,
        "sampleRate": 44100,
        "bitDepth": 16,
        "totalSamples": 5292000,
        "payloadSize": 1024,
        "headerSize": 9,
        "totalBitsExtracted": 8264,
        "capacityRemaining": 5283736,
        "capacityUsedPercent": 0.1563,
        "extractionMethod": "Randomized WAV LSB",
        "processingTime": 1.234
    },
    "debug": {
        "format": "WAV",
        "duration": 60.5,
        "channels": 2,
        "sampleRate": 44100,
        "bitDepth": 16,
        "totalSamples": 5292000,
        "payloadSize": 1024,
        "extractionMethod": "Randomized WAV LSB",
        "processingTime": 1.234
    }
}
```

#### 3. GET /api/audio/download/{filename}

Download a stego audio file.

**Request**:
- Method: GET
- Parameter: `filename` - Name of the stego audio file

**Response**:
- Content-Type: audio/wav
- Body: Binary audio file

#### 4. GET /api/audio/health

Health check endpoint for audio steganography service.

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

---

## Request Examples

### Embed Request (cURL)

```bash
curl -X POST "http://localhost:8000/api/audio/embed" \
  -F "audio=@/path/to/audio.mp3" \
  -F "encryptedMessage=SGVsbG8gV29ybGQ=" \
  -F "password=mysecretpassword" \
  -F "algorithm=AES-256-GCM"
```

### Embed Request (JavaScript/Fetch)

```javascript
const formData = new FormData();
formData.append('audio', audioFile);
formData.append('encryptedMessage', encryptedMessage);
formData.append('password', password);
formData.append('algorithm', 'AES-256-GCM');

const response = await fetch('http://localhost:8000/api/audio/embed', {
  method: 'POST',
  body: formData
});

const result = await response.json();
```

### Extract Request (cURL)

```bash
curl -X POST "http://localhost:8000/api/audio/extract" \
  -F "audio=@/path/to/audio_stego.wav" \
  -F "password=mysecretpassword"
```

### Extract Request (JavaScript/Fetch)

```javascript
const formData = new FormData();
formData.append('audio', stegoAudioFile);
formData.append('password', password);

const response = await fetch('http://localhost:8000/api/audio/extract', {
  method: 'POST',
  body: formData
});

const result = await response.json();
```

---

## Response Examples

### Successful Embed Response

```json
{
    "success": true,
    "fileName": "song_stego.wav",
    "originalFormat": "mp3",
    "convertedFormat": "WAV",
    "statistics": {
        "duration": 180.5,
        "channels": 2,
        "sampleRate": 44100,
        "bitDepth": 16,
        "totalSamples": 15920400,
        "payloadSize": 2048,
        "headerSize": 9,
        "totalBitsEmbedded": 16456,
        "capacityRemaining": 15903944,
        "capacityUsedPercent": 0.1033,
        "embeddingMethod": "Randomized WAV LSB",
        "processingTime": 5.234
    },
    "debug": {
        "originalFormat": "mp3",
        "convertedFormat": "WAV",
        "duration": 180.5,
        "channels": 2,
        "sampleRate": 44100,
        "bitDepth": 16,
        "totalSamples": 15920400,
        "availableCapacityBytes": 1987993,
        "usedCapacityBytes": 2048,
        "remainingCapacityBytes": 1985945,
        "embeddingMethod": "Randomized WAV LSB",
        "payloadSize": 2048,
        "verificationStatus": "PASSED",
        "processingTime": 5.234
    }
}
```

### Error Response (Insufficient Capacity)

```json
{
    "detail": "Audio capacity exceeded. Need 50000 bits but only have 10000 bits. Please upload a longer audio file."
}
```

### Error Response (Invalid Format)

```json
{
    "detail": "Unsupported audio format. Allowed: .wav, .mp3, .m4a, .flac"
}
```

### Successful Extract Response

```json
{
    "success": true,
    "encryptedData": "SGVsbG8gV29ybGQ=",
    "algorithm": "AES-256-GCM",
    "version": "1.0",
    "timestamp": "2024-01-01T00:00:00Z",
    "statistics": {
        "duration": 180.5,
        "channels": 2,
        "sampleRate": 44100,
        "bitDepth": 16,
        "totalSamples": 15920400,
        "payloadSize": 2048,
        "headerSize": 9,
        "totalBitsExtracted": 16456,
        "capacityRemaining": 15903944,
        "capacityUsedPercent": 0.1033,
        "extractionMethod": "Randomized WAV LSB",
        "processingTime": 2.123
    },
    "debug": {
        "format": "WAV",
        "duration": 180.5,
        "channels": 2,
        "sampleRate": 44100,
        "bitDepth": 16,
        "totalSamples": 15920400,
        "payloadSize": 2048,
        "extractionMethod": "Randomized WAV LSB",
        "processingTime": 2.123
    }
}
```

---

## Debugging Guide

### Development Debug Information

The API responses include a `debug` field with detailed diagnostic information:

```json
"debug": {
    "originalFormat": "mp3",
    "convertedFormat": "WAV",
    "duration": 60.5,
    "channels": 2,
    "sampleRate": 44100,
    "bitDepth": 16,
    "totalSamples": 5292000,
    "availableCapacityBytes": 660467,
    "usedCapacityBytes": 1024,
    "remainingCapacityBytes": 659443,
    "embeddingMethod": "Randomized WAV LSB",
    "payloadSize": 1024,
    "verificationStatus": "PASSED",
    "processingTime": 2.543
}
```

### Common Issues and Solutions

#### 1. FFmpeg Not Found

**Error**: `FFmpeg is not installed or not in system PATH`

**Solution**:
```bash
# Windows: Download and add to PATH
# macOS:
brew install ffmpeg

# Linux:
sudo apt install ffmpeg

# Verify:
ffmpeg -version
```

#### 2. Insufficient Capacity

**Error**: `Audio capacity exceeded`

**Solution**:
- Upload a longer audio file
- Reduce the message size
- Use a higher sample rate audio file

#### 3. Invalid Audio Format

**Error**: `Unsupported audio format`

**Solution**:
- Ensure file extension matches actual format
- Use supported formats: WAV, MP3, M4A, FLAC
- Check file is not corrupted

#### 4. Extraction Fails

**Error**: `Payload validation failed`

**Solution**:
- Ensure correct password is used
- Verify file is a valid stego audio
- Check file was not modified after embedding

#### 5. Conversion Timeout

**Error**: `FFmpeg conversion timed out`

**Solution**:
- Check FFmpeg is working correctly
- Try with a smaller audio file
- Increase timeout in audio_converter.py

### Logging

All operations are logged with detailed information:

```python
# Log levels
logger.info()  # General information
logger.warning()  # Non-critical issues
logger.error()  # Errors and failures
```

**View Logs**:
```bash
# Development: logs to console
# Production: configure file logging in main.py
```

---

## Logging Guide

### Log Levels

- **INFO**: Normal operations (validation, conversion, embedding)
- **WARNING**: Non-critical issues (capacity warnings, format issues)
- **ERROR**: Failures (validation errors, conversion failures)

### Log Format

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

**Example**:
```
2024-01-01 12:00:00 - app.audio_processing.audio_validator - INFO - Validating audio file: audio.mp3
2024-01-01 12:00:01 - app.audio_processing.audio_converter - INFO - Converting audio to WAV: audio.mp3
2024-01-01 12:00:02 - app.steganography.audio.sample_selector - INFO - Generating sample positions
2024-01-01 12:00:03 - app.steganography.audio.audio_lsb_embedder - INFO - Embedding payload
2024-01-01 12:00:04 - app.services.audio_steganography_service - INFO - Audio embed workflow completed in 4.5s
```

### Enabling Debug Logging

```python
# In main.py
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for verbose logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## Security Considerations

### Password Security

- **Never log passwords**: Passwords are used only for position generation
- **Hash passwords**: SHA-256 hashing before use
- **No storage**: Passwords are not stored anywhere

### Payload Security

- **Encrypted payload**: Only encrypted data is embedded
- **Existing encryption**: Uses project's AES-256-GCM encryption
- **Double-layer encryption**: Client + server encryption

### Steganography Security

- **Randomized positions**: Prevents pattern detection
- **Deterministic**: Same password = same positions
- **No metadata**: Payload hidden in audio data, not metadata
- **Minimal distortion**: LSB changes are inaudible

### File Security

- **Temporary files**: Cleaned up after use
- **No persistence**: Files stored only in temp directory
- **Access control**: Server-side file access only

### API Security

- **CORS configured**: Only allowed origins
- **Input validation**: All inputs validated
- **Error handling**: No sensitive data in error messages
- **Rate limiting**: Consider implementing for production

---

## Known Limitations

### Capacity Limitations

- **Text only**: Designed for text messages, not large files
- **Capacity depends on duration**: Longer audio = more capacity
- **Header overhead**: 9 bytes per payload

### Format Limitations

- **FFmpeg required**: Must be installed on system
- **WAV output only**: All output is WAV format
- **16-bit limit**: Currently supports 16-bit audio only

### Performance Limitations

- **Processing time**: Depends on audio duration
- **Memory usage**: Large audio files require more memory
- **Conversion time**: FFmpeg conversion adds overhead

### Security Limitations

- **LSB detection**: Advanced steganalysis may detect LSB modifications
- **Password strength**: Weak passwords reduce security
- **No authentication**: API endpoints require authentication in production

---

## Future Enhancements

### Planned Features

1. **Multi-bit LSB**: Embed multiple bits per sample for higher capacity
2. **Adaptive LSB**: Use variable bit depth based on audio content
3. **Frequency Domain**: Implement DCT-based steganography
4. **Spread Spectrum**: Use spread spectrum techniques
5. **Audio Quality Analysis**: Analyze audio before embedding
6. **Batch Processing**: Support multiple files at once
7. **Progress Indicators**: Real-time progress updates
8. **Compression**: Compress payload before embedding

### Performance Improvements

1. **Parallel Processing**: Use multiprocessing for large files
2. **Caching**: Cache converted WAV files
3. **Streaming**: Process audio in chunks
4. **GPU Acceleration**: Use GPU for processing

### Security Enhancements

1. **Authentication**: Add API authentication
2. **Rate Limiting**: Implement rate limiting
3. **Encryption Options**: Support multiple encryption algorithms
4. **Watermarking**: Add digital watermarking
5. **Anti-Steganalysis**: Implement detection resistance

### Usability Improvements

1. **Web Interface**: Built-in web interface
2. **CLI Tool**: Command-line interface
3. **Mobile App**: Mobile application
4. **Browser Extension**: Browser-based tool
5. **API Documentation**: Enhanced API docs

---

## Conclusion

The Audio Steganography Module provides a professional, production-ready implementation of audio steganography for the SecureStego project. It follows best practices in software architecture, security, and usability.

### Key Achievements

- ✅ Modular, maintainable architecture
- ✅ Integration with existing systems
- ✅ Comprehensive documentation
- ✅ Security-first design
- ✅ Extensive logging and debugging
- ✅ Multiple format support
- ✅ Randomized LSB steganography
- ✅ Capacity analysis and verification

### Next Steps

1. Install FFmpeg on your system
2. Install Python dependencies
3. Configure environment variables
4. Run the backend server
5. Test with sample audio files
6. Integrate with frontend

For questions or issues, refer to the debugging guide or check the logs for detailed error information.

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Author**: SecureStego Development Team
