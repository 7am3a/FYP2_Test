# Document Steganography Module

A professional-grade document steganography system for hiding encrypted messages within PDF and TXT files using hybrid dual-layer techniques.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Document Steganography Architecture](#document-steganography-architecture)
3. [Hybrid Dual-Layer Design](#hybrid-dual-layer-design)
4. [Folder Structure](#folder-structure)
5. [Installation Guide](#installation-guide)
6. [Dependencies](#dependencies)
7. [Environment Variables](#environment-variables)
8. [Running Backend](#running-backend)
9. [Supported Document Formats](#supported-document-formats)
10. [TXT Embedding Workflow](#txt-embedding-workflow)
11. [PDF Embedding Workflow](#pdf-embedding-workflow)
12. [Randomized Invisible Character Theory](#randomized-invisible-character-theory)
13. [Structure-Based Embedding Theory](#structure-based-embedding-theory)
14. [PDF Image Embedding Workflow](#pdf-image-embedding-workflow)
15. [Extraction Workflow](#extraction-workflow)
16. [Capacity Analysis](#capacity-analysis)
17. [API Documentation](#api-documentation)
18. [Request Examples](#request-examples)
19. [Response Examples](#response-examples)
20. [Debugging Guide](#debugging-guide)
21. [Logging Guide](#logging-guide)
22. [Security Considerations](#security-considerations)
23. [Known Limitations](#known-limitations)
24. [Future Enhancements](#future-enhancements)

---

## Project Overview

The Document Steganography Module is a production-quality system for hiding encrypted messages within document files. It implements a hybrid dual-layer approach that combines text-based steganography with image-based steganography for PDF files, providing maximum capacity and security.

### Key Features

- **Hybrid Dual-Layer Steganography**: Combines text and image steganography for PDFs
- **Multiple Text Methods**: Invisible character embedding and structure-based embedding
- **Randomized Placement**: Prevents detection through randomized insertion points
- **Capacity Analysis**: Pre-embedding capacity checking to ensure successful operations
- **Comprehensive Logging**: Detailed logging for debugging and audit trails
- **Debug Panel**: Development diagnostics for troubleshooting
- **Modular Architecture**: Clean separation of concerns for maintainability
- **Production Quality**: Suitable for Final Year Project and production use

---

## Document Steganography Architecture

The system is organized into several specialized modules, each with a specific responsibility:

### Module Overview

```
backend/app/
├── document_processing/          # Document parsing and validation
│   ├── document_validator.py    # File validation and type detection
│   ├── pdf_parser.py            # PDF content extraction
│   ├── pdf_rebuilder.py         # PDF reconstruction
│   └── txt_handler.py          # TXT file processing
├── steganography/               # Steganography algorithms
│   ├── invisible_character_embedder.py    # Invisible character hiding
│   ├── invisible_character_extractor.py  # Invisible character extraction
│   ├── structure_embedder.py             # Structure-based hiding
│   ├── structure_extractor.py           # Structure-based extraction
│   └── pdf_image_processor.py           # PDF image steganography
├── services/                     # Business logic layer
│   └── document_steganography_service.py # Orchestration service
├── routes/                       # API endpoints
│   └── document_steganography.py        # REST API routes
└── models/                       # Data models
    └── schemas.py               # Pydantic schemas
```

### Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Modularity**: Components can be tested and modified independently
3. **Reusability**: Image steganography module is reused for PDF images
4. **Extensibility**: Easy to add new steganography methods or document types
5. **Maintainability**: Clear structure with comprehensive documentation

---

## Hybrid Dual-Layer Design

The PDF steganography system uses a hybrid dual-layer approach to maximize capacity and security:

### Layer 1: Text Steganography

Hides data within the text content of the document using:
- **Invisible Character Embedding**: Uses zero-width Unicode characters
- **Structure-Based Embedding**: Uses whitespace and spacing patterns

### Layer 2: Image Steganography

Hides data within embedded images using:
- **Edge-Based LSB**: Reuses the existing image steganography module
- **PNG Conversion**: Converts images to PNG for lossless embedding
- **Edge Detection**: Uses Canny edge detection for optimal hiding locations

### Workflow Integration

For PDF files, the system:
1. Extracts text content and embedded images
2. Calculates capacity for both text and images
3. Splits payload between text and images based on capacity
4. Embeds in text using invisible characters or structure-based methods
5. Embeds in images using edge-based LSB
6. Rebuilds the PDF with modified content

---

## Folder Structure

### Document Processing Module

```
document_processing/
├── __init__.py                 # Module initialization
├── document_validator.py       # Validates document files
│   ├── File type validation
│   ├── MIME type checking
│   ├── Corruption detection
│   └── Encoding validation (TXT)
├── pdf_parser.py              # Extracts PDF content
│   ├── Text block extraction
│   ├── Image extraction
│   ├── Page analysis
│   └── Content statistics
├── pdf_rebuilder.py           # Rebuilds modified PDFs
│   ├── Text replacement
│   ├── Image reinsertion
│   ├── Structure preservation
│   └── Integrity validation
└── txt_handler.py             # Processes TXT files
    ├── Text reading/writing
    ├── Encoding handling
    ├── Capacity analysis
    └── Statistics calculation
```

### Text Steganography Module

```
steganography/
├── invisible_character_embedder.py    # Invisible character hiding
│   ├── Randomized placement
│   ├── Multiple character types
│   ├── Payload header
│   └── Capacity calculation
├── invisible_character_extractor.py  # Invisible character extraction
│   ├── Character detection
│   ├── Bit stream reconstruction
│   ├── Header validation
│   └── Payload extraction
├── structure_embedder.py             # Structure-based hiding
│   ├── Whitespace patterns
│   ├── Line ending encoding
│   ├── Spacing patterns
│   └── Capacity calculation
├── structure_extractor.py           # Structure-based extraction
│   ├── Pattern detection
│   ├── Bit stream reconstruction
│   ├── Header validation
│   └── Payload extraction
└── pdf_image_processor.py           # PDF image steganography
    ├── Image extraction
    ├── Capacity calculation
    ├── Edge-based LSB embedding
    ├── Payload distribution
    └── Image reinsertion
```

---

## Installation Guide

### Prerequisites

- Python 3.8 or higher
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

6. **Configure environment variables:**
   Edit `.env` file and set required variables (see [Environment Variables](#environment-variables))

---

## Dependencies

### Core Dependencies

```
fastapi==0.109.0              # Web framework
uvicorn[standard]==0.27.0     # ASGI server
pydantic==2.5.3               # Data validation
pydantic-settings==2.1.0      # Settings management
python-dotenv==1.0.0          # Environment variables
python-multipart==0.0.6       # Multipart form data
```

### Security Dependencies

```
cryptography==41.0.7          # Encryption operations
argon2-cffi==23.1.0           # Password hashing
```

### Document Processing Dependencies

```
PyMuPDF==1.23.8               # PDF processing
python-magic==0.4.27          # MIME type detection
```

### Image Processing Dependencies

```
Pillow==10.2.0                # Image processing
opencv-python==4.9.0.80       # Computer vision
numpy==1.26.3                 # Numerical operations
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SERVER_MASTER_KEY` | 64-character hex key for server-side encryption | `a1b2c3d4e5f6...` (64 chars) |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | SecureStego |
| `APP_VERSION` | Application version | 1.0.0 |
| `DEBUG` | Debug mode | False |
| `API_PREFIX` | API URL prefix | /api |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:5173,http://localhost:3000 |
| `PBKDF2_ITERATIONS` | PBKDF2 iterations | 100000 |
| `SALT_LENGTH` | Salt length in bytes | 32 |

### Generating Server Master Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Running Backend

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Accessing API Documentation

Once the server is running:
- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`

---

## Supported Document Formats

### Input Formats

| Format | Extension | MIME Type |
|--------|-----------|-----------|
| PDF | `.pdf` | `application/pdf` |
| TXT | `.txt` | `text/plain` |

### Output Formats

| Input Format | Output Format |
|--------------|---------------|
| PDF | PDF |
| TXT | TXT |

---

## TXT Embedding Workflow

### Process Flow

```
TXT Upload
    ↓
Validate TXT File
    ↓
Read Text Content
    ↓
Analyze Capacity
    ↓
Create Encrypted Payload
    ↓
Embed Using Invisible Characters
    ↓
Generate Stego TXT
    ↓
Validate Integrity
    ↓
Return Stego TXT
```

### Step Details

1. **Validation**: Checks file type, MIME type, encoding, and corruption
2. **Reading**: Reads text with automatic encoding detection (UTF-8, UTF-8-SIG, Latin-1, CP1252)
3. **Capacity Analysis**: Calculates available capacity based on word count and structure
4. **Payload Preparation**: Adds header with magic signature and payload length
5. **Embedding**: Uses randomized invisible character insertion
6. **Validation**: Ensures output file is valid and readable

---

## PDF Embedding Workflow

### Process Flow

```
PDF Upload
    ↓
Validate PDF File
    ↓
Parse PDF Structure
    ↓
Extract Text Blocks
    ↓
Extract Embedded Images
    ↓
Analyze Total Capacity
    ↓
Create Encrypted Payload
    ↓
Split Payload (Text + Images)
    ↓
Text Payload → Invisible Character Embedding
    ↓
Image Payload → Edge-Based LSB
    ↓
Rebuild PDF
    ↓
Validate PDF Integrity
    ↓
Return Stego PDF
```

### Step Details

1. **Validation**: Checks PDF structure, MIME type, and corruption
2. **Parsing**: Extracts text blocks and embedded images using PyMuPDF
3. **Capacity Analysis**: Calculates text capacity (invisible characters) and image capacity (edge-based LSB)
4. **Payload Splitting**: Divides payload between text and images based on available capacity
5. **Text Embedding**: Uses invisible character embedding in text content
6. **Image Embedding**: Uses existing edge-based LSB module for images
7. **Rebuilding**: Reconstructs PDF with modified text and images
8. **Validation**: Ensures output PDF is valid and readable

---

## Randomized Invisible Character Theory

### Concept

Invisible character steganography hides data by inserting invisible Unicode characters into text. These characters are not visible to readers but can be detected and decoded programmatically.

### Invisible Characters Used

| Character | Unicode | Bit Value | Description |
|-----------|---------|-----------|-------------|
| Zero Width Space | `\u200B` | 00 | Invisible space character |
| Zero Width Non-Joiner | `\u200C` | 01 | Prevents ligature formation |
| Zero Width Joiner | `\u200D` | 10 | Forces ligature formation |
| Zero Width No-Break Space | `\uFEFF` | 11 | Invisible no-break space |

### Encoding Process

1. **Payload Preparation**: Add header with magic signature (`DSTG`) and payload length
2. **Bit Conversion**: Convert payload bytes to bit stream
3. **Position Generation**: Randomly select insertion points (after spaces, punctuation)
4. **Character Insertion**: Insert invisible characters based on bit pairs (2 bits per character)
5. **Randomization**: Use random selection to avoid detectable patterns

### Decoding Process

1. **Character Detection**: Scan text for invisible characters
2. **Bit Reconstruction**: Convert characters back to bit stream
3. **Byte Conversion**: Convert bit stream to bytes
4. **Header Validation**: Verify magic signature and read payload length
5. **Payload Extraction**: Extract exact payload size

### Security Advantages

- **Invisible**: Characters are not visible to readers
- **Randomized**: Random insertion prevents pattern detection
- **Preserves Format**: Document appearance remains unchanged
- **Multiple Characters**: Four different characters for encoding
- **Header-Based**: Reliable extraction without guessing boundaries

---

## Structure-Based Embedding Theory

### Concept

Structure-based steganography hides data by modifying document structure elements like whitespace, line endings, and spacing patterns.

### Methods Implemented

#### 1. Whitespace Patterns

- **Single Space**: Represents bit 0
- **Double Space**: Represents bit 1
- **Location**: Trailing spaces at line ends

#### 2. Line Ending Patterns

- **`\n`**: Represents bit 0 (Unix-style)
- **`\r\n`**: Represents bit 1 (Windows-style)
- **Location**: Line endings throughout document

#### 3. Spacing Patterns

- **Normal Space**: Represents bit 0
- **Non-Breaking Space (`\u00A0`)**: Represents bit 1
- **Location**: Spaces between words

### Security Advantages

- **Subtle**: Modifications are difficult to notice
- **Preserves Readability**: Document remains readable
- **Multiple Methods**: Different patterns for flexibility
- **Structure-Aware**: Works with document structure

---

## PDF Image Embedding Workflow

### Process Flow

```
Extract Images from PDF
    ↓
Convert to PNG (if needed)
    ↓
Detect Edges Using Canny
    ↓
Calculate Edge Pixel Capacity
    ↓
Distribute Payload Across Images
    ↓
Embed Using Edge-Based LSB
    ↓
Reinsert Modified Images into PDF
    ↓
Validate Image Integrity
```

### Integration with Image Steganography

The PDF image processor reuses the existing edge-based LSB image steganography module:

1. **Edge Detection**: Uses Canny edge detection to find optimal hiding locations
2. **LSB Embedding**: Modifies least significant bits of edge pixels
3. **Capacity Calculation**: Each edge pixel can hide 3 bits (RGB channels)
4. **Payload Distribution**: Splits payload across multiple images if needed

### Advantages

- **Reuse**: Leverages tested image steganography module
- **Quality**: Edge-based embedding preserves image quality
- **Capacity**: Images provide significant capacity
- **Integration**: Seamless integration with PDF workflow

---

## Extraction Workflow

### TXT Extraction

```
Upload Stego TXT
    ↓
Validate TXT File
    ↓
Read Text Content
    ↓
Try Invisible Character Extraction
    ↓
If Failed, Try Structure-Based Extraction
    ↓
Validate Magic Signature
    ↓
Read Payload Length
    ↓
Extract Exact Payload
    ↓
Deserialize Payload
    ↓
Return Encrypted Data
```

### PDF Extraction

```
Upload Stego PDF
    ↓
Validate PDF File
    ↓
Parse PDF Structure
    ↓
Extract Text Content
    ↓
Extract Embedded Images
    ↓
Try Text Extraction (Invisible Characters)
    ↓
Try Image Extraction (Edge-Based LSB)
    ↓
Combine Payloads
    ↓
Validate Magic Signature
    ↓
Deserialize Payload
    ↓
Return Encrypted Data
```

### Fallback Mechanism

The system uses a fallback mechanism for extraction:
1. **Primary Method**: Invisible character extraction
2. **Fallback Method**: Structure-based extraction
3. **Image Extraction**: Edge-based LSB for images
4. **Combination**: Combines text and image payloads for PDFs

---

## Capacity Analysis

### TXT Capacity

Capacity is calculated based on:
- **Word Count**: Each word position can hide 2 bits (invisible characters)
- **Line Count**: Each line can hide 1-4 bits (structure-based)
- **Character Count**: Total characters for reference

### PDF Capacity

Capacity is calculated based on:
- **Text Capacity**: Based on text blocks and word count
- **Image Capacity**: Based on edge pixels in embedded images
- **Total Capacity**: Sum of text and image capacity

### Capacity Checking

Before embedding, the system:
1. Calculates total available capacity
2. Calculates required capacity (payload + header)
3. Compares available vs required
4. Rejects operation if insufficient capacity

### Example Calculation

**TXT File:**
- Words: 1000
- Invisible character capacity: 1000 positions × 2 bits = 2000 bits
- Header: 8 bytes × 8 bits = 64 bits
- Data capacity: 2000 - 64 = 1936 bits = 242 bytes

**PDF File:**
- Text words: 5000 → 10,000 bits
- Images: 2 images with 10,000 edge pixels each → 60,000 bits
- Total capacity: 70,000 bits
- Data capacity: ~8,700 bytes

---

## API Documentation

### POST /api/document/embed

Embed an encrypted message into a document.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `document`: Document file (PDF or TXT)
  - `encryptedMessage`: Base64 encoded encrypted message
  - `algorithm`: Encryption algorithm (default: AES-256-GCM)
  - `textMethod`: Text embedding method (default: invisible_character)
  - `useImages`: Use image steganography for PDFs (default: true)

**Response:**
```json
{
  "success": true,
  "fileName": "document_stego.pdf",
  "documentType": "pdf",
  "statistics": {
    "pageCount": 5,
    "textBlocks": 25,
    "imageCount": 2,
    "payloadSize": 1024,
    "capacityUsedPercent": 15.5,
    "embeddingMethod": "Hybrid Dual-Layer Document Steganography",
    "processingTime": 2.345,
    "debug": {
      "_note": "Development Debug Information"
    }
  }
}
```

### POST /api/document/extract

Extract an encrypted message from a stego document.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `document`: Stego document file (PDF or TXT)

**Response:**
```json
{
  "success": true,
  "encryptedData": "base64_encoded_encrypted_message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "statistics": {
    "documentType": "pdf",
    "payloadSize": 1024,
    "extractionMethod": "Hybrid Dual-Layer Document Steganography",
    "processingTime": 1.234,
    "debug": {
      "_note": "Development Debug Information"
    }
  }
}
```

### GET /api/document/download/{filename}

Download a stego document.

**Request:**
- Method: `GET`
- Parameter: `filename` - Name of the stego document

**Response:**
- File download with appropriate MIME type

### GET /api/document/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "document_steganography",
  "method": "Hybrid Dual-Layer Document Steganography",
  "textMethods": ["invisible_character", "structure"],
  "imageMethod": "Edge-Based LSB",
  "supportedFormats": ["PDF", "TXT"]
}
```

---

## Request Examples

### Embed Message in TXT

```bash
curl -X POST "http://localhost:8000/api/document/embed" \
  -F "document=@message.txt" \
  -F "encryptedMessage=base64_encrypted_message" \
  -F "algorithm=AES-256-GCM" \
  -F "textMethod=invisible_character"
```

### Embed Message in PDF

```bash
curl -X POST "http://localhost:8000/api/document/embed" \
  -F "document=@document.pdf" \
  -F "encryptedMessage=base64_encrypted_message" \
  -F "algorithm=AES-256-GCM" \
  -F "textMethod=invisible_character" \
  -F "useImages=true"
```

### Extract Message from TXT

```bash
curl -X POST "http://localhost:8000/api/document/extract" \
  -F "document=@message_stego.txt"
```

### Extract Message from PDF

```bash
curl -X POST "http://localhost:8000/api/document/extract" \
  -F "document=@document_stego.pdf"
```

---

## Response Examples

### Successful Embed Response

```json
{
  "success": true,
  "fileName": "document_stego.pdf",
  "documentType": "pdf",
  "statistics": {
    "pageCount": 10,
    "textBlocks": 50,
    "imageCount": 3,
    "payloadSize": 2048,
    "headerSize": 8,
    "textPayloadSize": 1024,
    "imagePayloadSize": 1024,
    "textCapacityBits": 10000,
    "imageCapacityBits": 60000,
    "totalCapacityBits": 70000,
    "capacityUsedPercent": 23.4,
    "embeddingMethod": "Hybrid Dual-Layer Document Steganography",
    "textMethod": "invisible_character",
    "useImages": true,
    "processingTime": 3.456,
    "debug": {
      "documentType": "PDF",
      "pageCount": 10,
      "textBlocks": 50,
      "imageCount": 3,
      "textCapacity": 10000,
      "imageCapacity": 60000,
      "payloadSize": 2048,
      "capacityUsed": 23.4,
      "embeddingMethod": "Hybrid Dual-Layer Document Steganography",
      "textMethod": "invisible_character",
      "useImages": true,
      "processingTime": 3.456,
      "integrityCheck": "PASSED",
      "_note": "Development Debug Information"
    }
  }
}
```

### Successful Extract Response

```json
{
  "success": true,
  "encryptedData": "base64_encoded_encrypted_message",
  "algorithm": "AES-256-GCM",
  "version": "1.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "statistics": {
    "documentType": "pdf",
    "pageCount": 10,
    "textBlocks": 50,
    "imageCount": 3,
    "payloadSize": 2048,
    "textPayloadSize": 1024,
    "imagePayloadSize": 1024,
    "extractionMethod": "Hybrid Dual-Layer Document Steganography",
    "processingTime": 2.345,
    "debug": {
      "documentType": "PDF",
      "pageCount": 10,
      "textBlocks": 50,
      "imageCount": 3,
      "payloadSize": 2048,
      "textPayloadSize": 1024,
      "imagePayloadSize": 1024,
      "extractionMethod": "Hybrid Dual-Layer Document Steganography",
      "processingTime": 2.345,
      "integrityCheck": "PASSED",
      "_note": "Development Debug Information"
    }
  }
}
```

### Error Response

```json
{
  "detail": "Document capacity exceeded. Need 50000 bits but only have 30000 bits. Please use a document with more content.",
  "status": "error"
}
```

---

## Debugging Guide

### Development Debug Panel

The system includes a development debug panel in the response statistics. This panel provides detailed diagnostic information:

**Debug Information Fields:**
- `documentType`: Type of document (PDF or TXT)
- `pageCount`: Number of pages (PDF only)
- `textBlocks`: Number of text blocks (PDF only)
- `imageCount`: Number of embedded images (PDF only)
- `textCapacity`: Text capacity in bits
- `imageCapacity`: Image capacity in bits
- `payloadSize`: Size of payload in bytes
- `capacityUsed`: Percentage of capacity used
- `embeddingMethod`: Steganography method used
- `textMethod`: Text embedding method used
- `useImages`: Whether image steganography was used
- `extractionMethod`: Extraction method used
- `processingTime`: Processing time in seconds
- `integrityCheck`: Integrity check status
- `_note`: "Development Debug Information"

### Common Issues and Solutions

#### Issue: Capacity Exceeded

**Error:** "Document capacity exceeded. Need X bits but only have Y bits."

**Solution:**
- Use a document with more text content
- Use a PDF with more or larger images
- Reduce the size of the encrypted message

#### Issue: No Hidden Payload Found

**Error:** "No hidden payload found in document."

**Solution:**
- Ensure the document was created with this steganography system
- Try the other extraction method (invisible character vs structure-based)
- Check if the document was corrupted

#### Issue: Invalid Magic Signature

**Error:** "Invalid magic signature. Expected DSTG but got XXXX."

**Solution:**
- The document may not be a valid stego document
- The document may have been modified after embedding
- Try extracting with the correct method

#### Issue: PDF Parsing Failed

**Error:** "Failed to parse PDF."

**Solution:**
- Ensure the PDF is not corrupted
- Check if the PDF is password-protected
- Try opening the PDF in a PDF viewer to verify integrity

### Logging

The system provides comprehensive logging at different levels:

**Log Levels:**
- `INFO`: Normal operations (embed, extract, validation)
- `WARNING`: Non-critical issues (cleanup failures)
- `ERROR`: Critical errors (validation failures, processing errors)

**Log Format:**
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

**Viewing Logs:**
Logs are output to the console when running the server. For production, configure a log file in the logging setup.

---

## Logging Guide

### Log Messages

The system logs important events throughout the workflow:

**Embedding Logs:**
- Document validation
- Capacity analysis
- Payload creation
- Text embedding
- Image embedding
- PDF rebuilding
- Processing time

**Extraction Logs:**
- Document validation
- Text extraction
- Image extraction
- Payload deserialization
- Processing time

**Error Logs:**
- Validation failures
- Capacity exceeded
- Parsing errors
- Embedding/extraction errors
- File cleanup failures

### Configuring Logging

To configure logging for production, modify the logging setup in `main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('document_steganography.log'),
        logging.StreamHandler()
    ]
)
```

### Log Analysis

For debugging:
1. Check log timestamps to correlate with API requests
2. Look for ERROR level messages for failures
3. Check processing time for performance issues
4. Verify capacity calculations for capacity errors

---

## Security Considerations

### Encryption

- **Double-Layer Encryption**: Uses existing encryption system (AES-256-GCM)
- **Password Protection**: Password is never sent as plaintext
- **Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations

### Steganography Security

- **Randomized Placement**: Prevents pattern detection
- **Multiple Methods**: Different embedding methods for flexibility
- **Header-Based**: Reliable extraction without guessing
- **Capacity Checking**: Prevents overflow attacks

### File Security

- **Validation**: All files are validated before processing
- **MIME Type Checking**: Prevents file type spoofing
- **Corruption Detection**: Detects corrupted files
- **Temporary File Cleanup**: Removes temporary files after processing

### API Security

- **CORS**: Configured CORS origins
- **Input Validation**: All inputs are validated
- **Error Handling**: Errors don't expose internal details
- **Rate Limiting**: Can be added for production

### Best Practices

1. **Never commit `.env` file**: Contains sensitive information
2. **Use strong passwords**: Minimum 12 characters recommended
3. **Rotate server master key**: Regularly rotate the server master key
4. **Use HTTPS in production**: Always use HTTPS in production
5. **Monitor logs**: Regularly monitor logs for suspicious activity
6. **Keep dependencies updated**: Regularly update dependencies

---

## Known Limitations

### Capacity Limitations

- **TXT Capacity**: Limited by word count and structure
- **PDF Text Capacity**: Limited by text content
- **PDF Image Capacity**: Limited by image size and edge pixels

### Format Limitations

- **PDF**: Only supports PDF format (not DOCX, ODT, etc.)
- **TXT**: Only supports plain text (not RTF, Markdown, etc.)
- **Images**: Only supports PNG for image steganography

### Processing Limitations

- **Large PDFs**: May take longer to process
- **Many Images**: Processing time increases with image count
- **Memory Usage**: Large files may require significant memory

### Extraction Limitations

- **Fallback Required**: May need to try multiple extraction methods
- **Corruption Detection**: Cannot detect all types of corruption
- **Modified Documents**: Extraction fails if document is modified after embedding

---

## Future Enhancements

### Planned Features

1. **Additional Document Formats**
   - DOCX support
   - ODT support
   - RTF support

2. **Advanced Steganography Methods**
   - Linguistic steganography
   - Syntactic steganography
   - Semantic steganography

3. **Improved Capacity**
   - Compression before embedding
   - Adaptive payload distribution
   - Multi-layer embedding

4. **Enhanced Security**
   - Steganography detection resistance
   - Anti-forensic techniques
   - Payload encryption within steganography

5. **Performance Improvements**
   - Parallel processing
   - Caching
   - Optimization for large files

6. **Additional Features**
   - Batch processing
   - Progress indicators
   - Web interface

### Contributing

To contribute to this project:
1. Follow the existing code style
2. Add comprehensive documentation
3. Include unit tests
4. Update this README
5. Follow security best practices

---

## License

This project is developed as a Final Year Project.

## Contact

For questions or issues, please refer to the project repository or contact the development team.
