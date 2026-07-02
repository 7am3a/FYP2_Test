# SecureStego Workflow Documentation

## Table of Contents
1. [Image Workflow](#image-workflow)
2. [Video Workflow](#video-workflow)
3. [Audio Workflow](#audio-workflow)
4. [Document Workflow](#document-workflow)
5. [Encryption Workflow](#encryption-workflow)
6. [Decryption Workflow](#decryption-workflow)
7. [Platform Verification Workflow](#platform-verification-workflow)
8. [Upload Workflow](#upload-workflow)
9. [Download Workflow](#download-workflow)
10. [Extraction Workflow](#extraction-workflow)

---

## Image Workflow

### Image Embedding Workflow

**Purpose**: Hide an encrypted message inside an image using edge-based LSB steganography

**Prerequisites**:
- Backend server running on port 8000
- Frontend running on port 5173
- User has an image file (PNG, JPG, JPEG, HEIC)
- User has a secret message
- User has a password

**Steps**:

1. **User Input** (`frontend/src/pages/HideMessage.jsx`)
   - User uploads image file
   - User enters secret message
   - User enters password
   - System validates password strength

2. **Encryption Request** (`frontend/src/services/apiService.js`)
   - Frontend calls `encryptMessage(message, password)`
   - Sends POST request to `/api/encryption/encrypt`
   - Request body: `{ message, password }`

3. **Encryption Processing** (`backend/app/routes/encryption.py` → `backend/app/services/crypto_service.py`)
   - Backend receives encryption request
   - Generates random salt (16 bytes)
   - Derives encryption key using Argon2id:
     - time_cost: 3
     - memory_cost: 65536 KiB (64 MB)
     - parallelism: 4
     - hash_len: 32 bytes (256 bits)
   - Generates random IV (12 bytes)
   - Encrypts message using AES-256-GCM
   - Returns: ciphertext, salt, iv, algorithm, kdf

4. **Encryption Response** (`backend/app/routes/encryption.py`)
   - Returns EncryptResponse with:
     - success: true
     - ciphertext (base64)
     - salt (base64)
     - iv (base64)
     - algorithm: "AES-256-GCM"
     - kdf: "Argon2id"

5. **Steganography Request** (`frontend/src/services/apiService.js`)
   - Frontend receives encryption response
   - Calls `embedMessage(imageFile, encryptedMessage, algorithm)`
   - Sends POST request to `/api/steganography/embed`
   - FormData: image file, encryptedMessage, algorithm

6. **Image Validation** (`backend/app/routes/steganography.py` → `backend/app/image_processing/image_validator.py`)
   - Backend receives steganography request
   - Validates file format (PNG, JPG, JPEG, HEIC)
   - Validates file size (max 50 MB)
   - Saves uploaded file to temporary location

7. **Image Conversion** (`backend/app/image_processing/image_converter.py`)
   - Converts image to PNG format (if not already PNG)
   - Ensures lossless format for LSB embedding
   - Saves converted image to temporary location

8. **Edge Detection** (`backend/app/image_processing/edge_detector.py`)
   - Loads image in grayscale
   - Applies Gaussian blur to reduce noise
   - Runs Canny edge detection:
     - Lower threshold: 50
     - Upper threshold: 150
     - Aperture size: 3
   - Returns binary edge map
   - Extracts edge pixel coordinates

9. **Payload Serialization** (`backend/app/utils/payload_serializer.py`)
   - Creates structured payload:
     ```json
     {
       "version": "1.0",
       "algorithm": "AES-256-GCM",
       "timestamp": "ISO-8601 timestamp",
       "encryptedData": "base64 ciphertext"
     }
     ```
   - Serializes to binary (JSON + UTF-8)

10. **Platform Signature Injection** (`backend/app/services/platform_verification_service.py`)
    - Generates HMAC-SHA256 signature:
      - Platform: "SecureStego"
      - Version: "1.0.0"
      - Media type: "image"
      - Timestamp: current time
      - Payload data: encrypted payload
    - Combines signature with payload:
      - Format: [signature_length (4 bytes)][signature][payload]
    - Returns combined payload

11. **Capacity Check** (`backend/app/steganography/edge_lsb_embedder.py`)
    - Calculates required capacity:
      - Header size: 4 bytes (32 bits)
      - Payload size: len(combined_payload) * 8 bits
    - Calculates available capacity:
      - Edge pixels count * 3 bits per pixel
    - Validates: required_bits <= available_bits
    - Raises error if capacity exceeded

12. **LSB Embedding** (`backend/app/steganography/edge_lsb_embedder.py`)
    - Loads PNG image pixels
    - Embeds payload length header (4 bytes, big-endian)
    - Embeds payload data into edge pixels:
      - Uses 1 LSB per RGB channel (3 bits per pixel)
      - Modifies only edge pixels
      - Preserves image quality
    - Saves stego image to temporary location

13. **Steganography Response** (`backend/app/routes/steganography.py`)
    - Returns EmbedResponse with:
      - success: true
      - fileName: stego image filename
      - originalFormat: original image format
      - convertedFormat: "PNG"
      - statistics:
        - imageWidth, imageHeight
        - totalPixels, edgePixels
        - payloadSize, headerSize
        - totalBitsUsed, capacityRemaining
        - capacityUsedPercent
        - embeddingMethod: "Edge-Based LSB"
        - edgeDetectionMethod: "Canny"
        - processingTime

14. **Cleanup** (`backend/app/routes/steganography.py`)
    - Removes temporary uploaded file
    - Keeps stego image for download

15. **Frontend Display** (`frontend/src/pages/HideMessage.jsx`)
    - Displays success message
    - Shows steganography statistics
    - Shows download button

16. **File Download** (`frontend/src/services/apiService.js`)
    - User clicks download button
    - Calls `downloadStegoImage(filename)`
    - Sends GET request to `/api/steganography/download/{filename}`
    - Receives file blob
    - Triggers browser download

17. **File Serving** (`backend/app/routes/steganography.py`)
    - Backend serves stego image from temp directory
    - Returns FileResponse with media_type "image/png"

**Success Criteria**:
- Message encrypted successfully
- Message embedded into image successfully
- Stego image downloaded
- Image quality preserved
- Edge pixels used for embedding

**Error Handling**:
- Invalid image format → 400 Bad Request
- Image size exceeded → 400 Bad Request
- Capacity exceeded → 400 Bad Request
- Encryption failure → 500 Internal Server Error
- Steganography failure → 500 Internal Server Error

---

### Image Extraction Workflow

**Purpose**: Extract and decrypt a hidden message from a stego image

**Prerequisites**:
- Backend server running on port 8000
- Frontend running on port 5173
- User has a stego PNG image
- User has the password used for encryption
- User has the salt and IV from original encryption

**Steps**:

1. **User Input** (`frontend/src/pages/ExtractMessage.jsx`)
   - User uploads stego PNG image
   - User enters password
   - User enters salt (from original encryption)
   - User enters IV (from original encryption)

2. **Steganography Request** (`frontend/src/services/apiService.js`)
   - Frontend calls `extractMessage(imageFile)`
   - Sends POST request to `/api/steganography/extract`
   - FormData: image file

3. **Image Validation** (`backend/app/routes/steganography.py`)
   - Backend receives steganography request
   - Validates file format (must be PNG)
   - Saves uploaded file to temporary location

4. **Edge Detection** (`backend/app/image_processing/edge_detector.py`)
   - Loads stego image in grayscale
   - Applies Gaussian blur
   - Runs Canny edge detection
   - Returns binary edge map
   - Extracts edge pixel coordinates

5. **LSB Extraction** (`backend/app/steganography/edge_lsb_extractor.py`)
   - Loads stego image pixels
   - Extracts bits from edge pixels:
     - Reads 1 LSB per RGB channel
     - Reconstructs bit stream
   - Reads payload length header (first 4 bytes)
   - Extracts payload data based on length
   - Returns combined payload

6. **Platform Signature Verification** (`backend/app/services/platform_verification_service.py`)
   - Extracts signature length (first 4 bytes)
   - Extracts signature binary
   - Extracts encrypted payload binary
   - Verifies HMAC-SHA256 signature:
     - Validates platform identity ("SecureStego")
     - Validates version compatibility ("1.0.0")
     - Validates media type match ("image")
     - Recomputes HMAC and compares
   - Returns encrypted payload and verification result

7. **Signature Validation** (`backend/app/verification/signature_validator.py`)
   - If signature invalid → raises SignatureVerificationError
   - If signature tampered → raises TamperedSignatureError
   - If version mismatch → raises VersionMismatchError
   - If platform mismatch → raises PlatformMismatchError
   - If media type mismatch → raises MediaTypeMismatchError

8. **Payload Deserialization** (`backend/app/utils/payload_deserializer.py`)
   - Deserializes binary to JSON
   - Validates payload structure
   - Extracts encrypted data
   - Returns encrypted data and metadata

9. **Steganography Response** (`backend/app/routes/steganography.py`)
   - Returns ExtractResponse with:
     - success: true
     - encryptedData (base64)
     - algorithm: "AES-256-GCM"
     - version: "1.0"
     - timestamp: "ISO-8601 timestamp"
     - statistics:
       - imageWidth, imageHeight
       - totalPixels, edgePixels
       - payloadSize, headerSize
       - totalBitsExtracted
       - extractionMethod: "Edge-Based LSB"
       - edgeDetectionMethod: "Canny"
       - processingTime

10. **Cleanup** (`backend/app/routes/steganography.py`)
    - Removes temporary uploaded file

11. **Frontend Display** (`frontend/src/pages/ExtractMessage.jsx`)
    - Displays extracted encrypted data
    - Shows steganography statistics

12. **Decryption Request** (`frontend/src/services/apiService.js`)
    - Frontend calls `decryptMessage(ciphertext, password, salt, iv)`
    - Sends POST request to `/api/encryption/decrypt`
    - Request body: { ciphertext, password, salt, iv }

13. **Decryption Processing** (`backend/app/routes/encryption.py` → `backend/app/services/crypto_service.py`)
    - Backend receives decryption request
    - Decodes base64 (ciphertext, salt, iv)
    - Derives encryption key using Argon2id (same parameters)
    - Decrypts using AES-256-GCM
    - Returns plaintext message

14. **Decryption Response** (`backend/app/routes/encryption.py`)
    - Returns DecryptResponse with:
      - success: true
      - message (plaintext)

15. **Frontend Display** (`frontend/src/pages/ExtractMessage.jsx`)
    - Displays decrypted message
    - Shows copy to clipboard button
    - Displays decryption statistics

**Success Criteria**:
- Message extracted successfully
- Platform signature verified
- Message decrypted successfully
- Original message displayed

**Error Handling**:
- Invalid image format → 400 Bad Request
- No hidden data found → 400 Bad Request
- Invalid signature → 400 Bad Request
- Tampered signature → 400 Bad Request
- Wrong password → 400 Bad Request
- Decryption failure → 500 Internal Server Error

---

## Video Workflow

### Video Embedding Workflow

**Purpose**: Hide an encrypted message inside a video using DCT-based steganography

**Prerequisites**:
- Backend server running on port 8000
- FFmpeg installed on system
- User has a video file (MP4, AVI, MOV)
- User has an encrypted message
- User has selected frame selection strategy

**Steps**:

1. **User Input** (Frontend - not yet implemented)
   - User uploads video file
   - User provides encrypted message
   - User selects frame selection strategy (fixed_interval, random, keyframe)
   - User sets frame interval (if applicable)

2. **Steganography Request** (`backend/app/routes/video_steganography.py`)
   - Backend receives POST request to `/api/video/embed`
   - FormData: video file, encryptedMessage, algorithm, frameSelectionStrategy, frameInterval

3. **Video Validation** (`backend/app/video_processing/video_validator.py`)
   - Validates file format (MP4, AVI, MOV)
   - Validates file size (max 500 MB)
   - Saves uploaded file to temporary location

4. **Video Conversion** (`backend/app/video_processing/video_converter.py`)
   - Converts video to MP4 format (if not already MP4)
   - Extracts audio track for preservation
   - Saves converted video to temporary location

5. **Frame Extraction** (`backend/app/video_processing/frame_extractor.py`)
   - Extracts frames from video using FFmpeg
   - Saves frames to temporary directory
   - Returns frame count and frame paths

6. **Frame Selection** (`backend/app/steganography/video/frame_selector.py`)
   - Selects frames for embedding based on strategy:
     - fixed_interval: Every Nth frame
     - random: Random frames
     - keyframe: Keyframes only
   - Returns selected frame indices

7. **Payload Serialization** (`backend/app/utils/payload_serializer.py`)
   - Creates structured payload with metadata
   - Serializes to binary

8. **Platform Signature Injection** (`backend/app/services/platform_verification_service.py`)
   - Generates HMAC-SHA256 signature for video
   - Combines signature with payload
   - Returns combined payload

9. **Capacity Check** (`backend/app/steganography/video/dct_embedder.py`)
   - Calculates required capacity
   - Calculates available capacity in selected frames
   - Validates capacity

10. **DCT Embedding** (`backend/app/steganography/video/dct_embedder.py`)
    - Loads selected frames
    - Applies DCT transform to each frame
    - Embeds payload into DCT coefficients
    - Applies inverse DCT
    - Saves modified frames

11. **Video Rebuilding** (`backend/app/video_processing/frame_rebuilder.py`)
    - Rebuilds video from modified frames
    - Preserves audio track
    - Saves stego video to temporary location

12. **Cleanup** (`backend/app/video_processing/frame_extractor.py`)
    - Removes temporary frames
    - Removes temporary uploaded file

13. **Response** (`backend/app/routes/video_steganography.py`)
    - Returns VideoEmbedResponse with:
      - success: true
      - fileName: stego video filename
      - originalFormat, convertedFormat
      - statistics:
        - videoWidth, videoHeight
        - totalFrames, selectedFrames
        - frameSelectionStrategy, frameInterval
        - payloadSize, totalBitsEmbedded
        - capacityRemaining, capacityUsedPercent
        - embeddingMethod: "DCT-Based Block Steganography"
        - audioPreserved: true
        - processingTime

**Success Criteria**:
- Message embedded into video
- Audio track preserved
- Video quality maintained
- Frame selection strategy applied

---

### Video Extraction Workflow

**Purpose**: Extract a hidden message from a stego video

**Prerequisites**:
- Backend server running on port 8000
- FFmpeg installed on system
- User has a stego MP4 video

**Steps**:

1. **User Input** (Frontend - not yet implemented)
   - User uploads stego video file

2. **Steganography Request** (`backend/app/routes/video_steganography.py`)
   - Backend receives POST request to `/api/video/extract`
   - FormData: video file

3. **Video Validation** (`backend/app/video_processing/video_validator.py`)
   - Validates file format (must be MP4)
   - Saves uploaded file to temporary location

4. **Frame Extraction** (`backend/app/video_processing/frame_extractor.py`)
   - Extracts frames from stego video
   - Saves frames to temporary directory

5. **Frame Selection** (`backend/app/steganography/video/frame_selector.py`)
   - Selects frames for extraction (same strategy as embedding)
   - Returns selected frame indices

6. **DCT Extraction** (`backend/app/steganography/video/dct_extractor.py`)
    - Loads selected frames
    - Applies DCT transform
    - Extracts payload from DCT coefficients
    - Returns combined payload

7. **Platform Signature Verification** (`backend/app/services/platform_verification_service.py`)
    - Extracts and verifies platform signature
    - Validates platform, version, media type
    - Returns encrypted payload

8. **Payload Deserialization** (`backend/app/utils/payload_deserializer.py`)
    - Deserializes binary to JSON
    - Extracts encrypted data

9. **Cleanup** (`backend/app/video_processing/frame_extractor.py`)
    - Removes temporary frames
    - Removes temporary uploaded file

10. **Response** (`backend/app/routes/video_steganography.py`)
    - Returns VideoExtractResponse with:
      - success: true
      - encryptedData
      - algorithm, version, timestamp
      - statistics:
        - videoWidth, videoHeight
        - totalFrames, selectedFrames
        - frameSelectionStrategy, frameInterval
        - payloadSize, totalBitsEmbedded
        - embeddingMethod: "DCT-Based Block Steganography"
        - processingTime

**Success Criteria**:
- Message extracted from video
- Platform signature verified
- Encrypted data returned

---

## Audio Workflow

### Audio Embedding Workflow

**Purpose**: Hide an encrypted message inside audio using randomized LSB steganography

**Prerequisites**:
- Backend server running on port 8000
- FFmpeg installed on system
- User has an audio file (WAV, MP3, M4A, FLAC)
- User has an encrypted message
- User has a password for sample position generation

**Steps**:

1. **User Input** (Frontend - not yet implemented)
   - User uploads audio file
   - User provides encrypted message
   - User provides password for sample positions

2. **Steganography Request** (`backend/app/routes/audio_steganography.py`)
   - Backend receives POST request to `/api/audio/embed`
   - FormData: audio file, encryptedMessage, password, algorithm

3. **Audio Validation** (`backend/app/audio_processing/audio_validator.py`)
   - Validates file format (WAV, MP3, M4A, FLAC)
   - Validates file size (max 100 MB)
   - Saves uploaded file to temporary location

4. **Audio Conversion** (`backend/app/audio_processing/audio_converter.py`)
   - Converts audio to WAV format (if not already WAV)
   - Ensures uncompressed format for LSB embedding
   - Saves converted audio to temporary location

5. **Audio Loading** (`backend/app/audio_processing/audio_loader.py`)
   - Loads WAV audio file
   - Extracts audio data (samples)
   - Returns sample rate, bit depth, channels

6. **Sample Position Generation** (`backend/app/steganography/audio/sample_selector.py`)
   - Generates random sample positions from password
   - Uses deterministic random (seeded by password)
   - Returns sample indices for embedding

7. **Payload Serialization** (`backend/app/utils/payload_serializer.py`)
   - Creates structured payload with metadata
   - Serializes to binary

8. **Platform Signature Injection** (`backend/app/services/platform_verification_service.py`)
   - Generates HMAC-SHA256 signature for audio
   - Combines signature with payload
   - Returns combined payload

9. **Capacity Check** (`backend/app/steganography/audio/audio_lsb_embedder.py`)
   - Calculates required capacity
   - Calculates available capacity in selected samples
   - Validates capacity

10. **LSB Embedding** (`backend/app/steganography/audio/audio_lsb_embedder.py`)
    - Loads audio samples
    - Embeds payload into LSB of selected samples
    - Preserves audio quality
    - Returns modified audio data

11. **Audio Writing** (`backend/app/audio_processing/audio_writer.py`)
    - Writes stego audio to WAV file
    - Saves to temporary location

12. **Cleanup** (`backend/app/routes/audio_steganography.py`)
    - Removes temporary uploaded file

13. **Response** (`backend/app/routes/audio_steganography.py`)
    - Returns AudioEmbedResponse with:
      - success: true
      - fileName: stego audio filename
      - originalFormat, convertedFormat
      - statistics:
        - duration, channels, sampleRate, bitDepth
        - totalSamples, payloadSize, headerSize
        - totalBitsEmbedded, capacityRemaining
        - capacityUsedPercent
        - embeddingMethod: "Randomized WAV LSB"
        - processingTime

**Success Criteria**:
- Message embedded into audio
- Audio quality preserved
- Sample positions derived from password
- Randomized embedding applied

---

### Audio Extraction Workflow

**Purpose**: Extract a hidden message from stego audio

**Prerequisites**:
- Backend server running on port 8000
- FFmpeg installed on system
- User has a stego WAV audio
- User has the password used for embedding

**Steps**:

1. **User Input** (Frontend - not yet implemented)
   - User uploads stego audio file
   - User provides password for sample positions

2. **Steganography Request** (`backend/app/routes/audio_steganography.py`)
   - Backend receives POST request to `/api/audio/extract`
   - FormData: audio file, password

3. **Audio Validation** (`backend/app/audio_processing/audio_validator.py`)
   - Validates file format (must be WAV)
   - Saves uploaded file to temporary location

4. **Audio Loading** (`backend/app/audio_processing/audio_loader.py`)
   - Loads WAV audio file
   - Extracts audio samples
   - Returns sample rate, bit depth, channels

5. **Sample Position Generation** (`backend/app/steganography/audio/sample_selector.py`)
   - Generates sample positions from password (same as embedding)
   - Returns sample indices for extraction

6. **LSB Extraction** (`backend/app/steganography/audio/audio_lsb_extractor.py`)
    - Loads audio samples
    - Extracts bits from LSB of selected samples
    - Reconstructs combined payload
    - Returns combined payload

7. **Platform Signature Verification** (`backend/app/services/platform_verification_service.py`)
    - Extracts and verifies platform signature
    - Validates platform, version, media type
    - Returns encrypted payload

8. **Payload Deserialization** (`backend/app/utils/payload_deserializer.py`)
    - Deserializes binary to JSON
    - Extracts encrypted data

9. **Cleanup** (`backend/app/routes/audio_steganography.py`)
    - Removes temporary uploaded file

10. **Response** (`backend/app/routes/audio_steganography.py`)
    - Returns AudioExtractResponse with:
      - success: true
      - encryptedData
      - algorithm, version, timestamp
      - statistics:
        - duration, channels, sampleRate, bitDepth
        - totalSamples, payloadSize, headerSize
        - totalBitsEmbedded
        - embeddingMethod: "Randomized WAV LSB"
        - processingTime

**Success Criteria**:
- Message extracted from audio
- Platform signature verified
- Password-derived positions matched

---

## Document Workflow

### Document Embedding Workflow

**Purpose**: Hide an encrypted message inside a document using hybrid steganography

**Prerequisites**:
- Backend server running on port 8000
- User has a document file (PDF or TXT)
- User has an encrypted message
- User has selected text embedding method

**Steps**:

1. **User Input** (Frontend - not yet implemented)
   - User uploads document file (PDF or TXT)
   - User provides encrypted message
   - User selects text method (invisible_character or structure_based)
   - User selects whether to use images (for PDF)

2. **Steganography Request** (`backend/app/routes/document_steganography.py`)
   - Backend receives POST request to `/api/document/embed`
   - FormData: document file, encryptedMessage, algorithm, textMethod, useImages

3. **Document Validation** (`backend/app/document_processing/document_validator.py`)
   - Validates file format (PDF or TXT)
   - Validates file size (max 50 MB)
   - Saves uploaded file to temporary location

4. **Document Processing**
   - **For PDF** (`backend/app/document_processing/pdf_parser.py`):
     - Parses PDF structure
     - Extracts text blocks
     - Extracts embedded images
     - Returns document structure
   - **For TXT** (`backend/app/document_processing/txt_handler.py`):
     - Loads text file
     - Analyzes text structure
     - Returns text content

5. **Payload Serialization** (`backend/app/utils/payload_serializer.py`)
   - Creates structured payload with metadata
   - Serializes to binary

6. **Platform Signature Injection** (`backend/app/services/platform_verification_service.py`)
   - Generates HMAC-SHA256 signature for document
   - Combines signature with payload
   - Returns combined payload

7. **Payload Splitting** (`backend/app/services/document_steganography_service.py`)
   - Splits payload for hybrid embedding:
     - Part for text embedding
     - Part for image embedding (if PDF and useImages)
   - Calculates capacity for each layer

8. **Text Embedding**
   - **Invisible Character** (`backend/app/steganography/invisible_character_embedder.py`):
     - Embeds payload using invisible Unicode characters
     - Inserts between words/characters
     - Preserves visible text
   - **Structure-Based** (`backend/app/steganography/structure_embedder.py`):
     - Embeds payload using text structure (spacing, case)
     - Modifies whitespace and capitalization
     - Preserves readability

9. **Image Embedding** (if PDF and useImages) (`backend/app/steganography/pdf_image_processor.py`)
   - Extracts embedded images from PDF
   - Applies edge-based LSB to each image
   - Embeds image portion of payload
   - Returns modified images

10. **Document Rebuilding**
    - **For PDF** (`backend/app/document_processing/pdf_rebuilder.py`):
      - Rebuilds PDF with modified text
      - Rebuilds PDF with modified images
      - Saves stego PDF
    - **For TXT** (`backend/app/document_processing/txt_handler.py`):
      - Saves stego TXT with embedded data

11. **Cleanup** (`backend/app/routes/document_steganography.py`)
    - Removes temporary uploaded file

12. **Response** (`backend/app/routes/document_steganography.py`)
    - Returns DocumentEmbedResponse with:
      - success: true
      - fileName: stego document filename
      - documentType: "pdf" or "txt"
      - statistics:
        - pageCount, textBlocks, imageCount (PDF)
        - originalLength, stegoLength (TXT)
        - payloadSize, headerSize
        - textPayloadSize, imagePayloadSize (PDF)
        - textCapacityBits, imageCapacityBits (PDF)
        - totalCapacityBits
        - capacityUsedPercent
        - embeddingMethod: "Hybrid Dual-Layer Document Steganography"
        - textMethod, useImages
        - processingTime

**Success Criteria**:
- Message embedded into document
- Text embedding applied
- Image embedding applied (if applicable)
- Document structure preserved

---

### Document Extraction Workflow

**Purpose**: Extract a hidden message from a stego document

**Prerequisites**:
- Backend server running on port 8000
- User has a stego document (PDF or TXT)

**Steps**:

1. **User Input** (Frontend - not yet implemented)
   - User uploads stego document file

2. **Steganography Request** (`backend/app/routes/document_steganography.py`)
   - Backend receives POST request to `/api/document/extract`
   - FormData: document file

3. **Document Validation** (`backend/app/document_processing/document_validator.py`)
   - Validates file format (PDF or TXT)
   - Saves uploaded file to temporary location

4. **Document Processing**
   - **For PDF** (`backend/app/document_processing/pdf_parser.py`):
     - Parses PDF structure
     - Extracts text blocks
     - Extracts embedded images
   - **For TXT** (`backend/app/document_processing/txt_handler.py`):
     - Loads text file

5. **Text Extraction**
   - **Invisible Character** (`backend/app/steganography/invisible_character_extractor.py`):
     - Extracts invisible characters
     - Reconstructs text payload
   - **Structure-Based** (`backend/app/steganography/structure_extractor.py`):
     - Extracts structure-based data
     - Reconstructs text payload

6. **Image Extraction** (if PDF has images) (`backend/app/steganography/pdf_image_processor.py`)
   - Extracts embedded images from PDF
   - Applies edge-based LSB extraction
   - Extracts image payload
   - Returns image payload

7. **Payload Combination** (`backend/app/services/document_steganography_service.py`)
   - Combines text and image payloads
   - Reconstructs combined payload

8. **Platform Signature Verification** (`backend/app/services/platform_verification_service.py`)
    - Extracts and verifies platform signature
    - Validates platform, version, media type
    - Returns encrypted payload

9. **Payload Deserialization** (`backend/app/utils/payload_deserializer.py`)
    - Deserializes binary to JSON
    - Extracts encrypted data

10. **Cleanup** (`backend/app/routes/document_steganography.py`)
    - Removes temporary uploaded file

11. **Response** (`backend/app/routes/document_steganography.py`)
    - Returns DocumentExtractResponse with:
      - success: true
      - encryptedData
      - algorithm, version, timestamp
      - statistics:
        - pageCount, textBlocks, imageCount
        - payloadSize, headerSize
        - textPayloadSize, imagePayloadSize
        - textCapacityBits, imageCapacityBits
        - totalCapacityBits
        - capacityUsedPercent
        - embeddingMethod: "Hybrid Dual-Layer Document Steganography"
        - textMethod, useImages
        - processingTime

**Success Criteria**:
- Message extracted from document
- Text extraction successful
- Image extraction successful (if applicable)
- Platform signature verified

---

## Encryption Workflow

**Purpose**: Encrypt a plaintext message using Argon2id key derivation and AES-256-GCM

**Prerequisites**:
- Backend server running on port 8000
- User has a plaintext message
- User has a password

**Steps**:

1. **User Input** (`frontend/src/pages/HideMessage.jsx`)
   - User enters plaintext message
   - User enters password
   - System validates password strength

2. **Encryption Request** (`frontend/src/services/apiService.js`)
   - Frontend calls `encryptMessage(message, password)`
   - Sends POST request to `/api/encryption/encrypt`
   - Request body: `{ message, password }`

3. **Request Validation** (`backend/app/routes/encryption.py`)
   - Validates message is not empty
   - Validates password is not empty
   - Validates message length
   - Validates password length

4. **Salt Generation** (`backend/app/services/crypto_service.py`)
   - Generates random salt (16 bytes)
   - Uses `secrets.token_bytes(16)`
   - Ensures cryptographic randomness

5. **IV Generation** (`backend/app/services/crypto_service.py`)
   - Generates random IV (12 bytes)
   - Uses `secrets.token_bytes(12)`
   - Ensures cryptographic randomness

6. **Key Derivation** (`backend/app/services/crypto_service.py`)
   - Derives 256-bit encryption key using Argon2id:
     - Input: password + salt
     - Parameters (from settings):
       - time_cost: 3
       - memory_cost: 65536 KiB (64 MB)
       - parallelism: 4
       - hash_len: 32 bytes (256 bits)
       - salt_len: 16 bytes (128 bits)
     - Output: 32-byte key

7. **Encryption** (`backend/app/services/crypto_service.py`)
   - Encrypts message using AES-256-GCM:
     - Input: plaintext message + derived key + IV
     - Algorithm: AES-256-GCM
     - Mode: Authenticated encryption
     - Output: ciphertext + authentication tag

8. **Encoding** (`backend/app/services/crypto_service.py`)
   - Encodes ciphertext to base64
   - Encodes salt to base64
   - Encodes IV to base64
   - Ensures safe transmission

9. **Response** (`backend/app/routes/encryption.py`)
   - Returns EncryptResponse with:
     - success: true
     - ciphertext (base64)
     - salt (base64)
     - iv (base64)
     - algorithm: "AES-256-GCM"
     - kdf: "Argon2id"

10. **Frontend Storage** (`frontend/src/services/encryptionService.js`)
    - Stores encryption data in service
    - Generates debug information
    - Makes data available for steganography

**Success Criteria**:
- Message encrypted successfully
- Random salt and IV generated
- Key derived using Argon2id
- Ciphertext returned in base64

**Error Handling**:
- Empty message → 400 Bad Request
- Empty password → 400 Bad Request
- Encryption failure → 500 Internal Server Error

---

## Decryption Workflow

**Purpose**: Decrypt an encrypted message using Argon2id key derivation and AES-256-GCM

**Prerequisites**:
- Backend server running on port 8000
- User has ciphertext (base64)
- User has password
- User has salt (base64)
- User has IV (base64)

**Steps**:

1. **User Input** (`frontend/src/pages/ExtractMessage.jsx`)
   - User enters password
   - User enters salt (from original encryption)
   - User enters IV (from original encryption)
   - System has ciphertext (from steganography extraction)

2. **Decryption Request** (`frontend/src/services/apiService.js`)
   - Frontend calls `decryptMessage(ciphertext, password, salt, iv)`
   - Sends POST request to `/api/encryption/decrypt`
   - Request body: { ciphertext, password, salt, iv }

3. **Request Validation** (`backend/app/routes/encryption.py`)
   - Validates ciphertext is not empty
   - Validates password is not empty
   - Validates salt is not empty
   - Validates IV is not empty
   - Validates base64 format

4. **Decoding** (`backend/app/services/crypto_service.py`)
   - Decodes ciphertext from base64
   - Decodes salt from base64
   - Decodes IV from base64
   - Converts to bytes

5. **Key Derivation** (`backend/app/services/crypto_service.py`)
   - Derives 256-bit encryption key using Argon2id:
     - Input: password + salt (same as encryption)
     - Parameters (from settings, same as encryption):
       - time_cost: 3
       - memory_cost: 65536 KiB
       - parallelism: 4
       - hash_len: 32 bytes
       - salt_len: 16 bytes
     - Output: 32-byte key

6. **Decryption** (`backend/app/services/crypto_service.py`)
   - Decrypts ciphertext using AES-256-GCM:
     - Input: ciphertext + derived key + IV
     - Algorithm: AES-256-GCM
     - Mode: Authenticated decryption
     - Output: plaintext bytes

7. **Decoding** (`backend/app/services/crypto_service.py`)
   - Decodes plaintext bytes to string
   - Uses UTF-8 encoding
   - Returns original message

8. **Response** (`backend/app/routes/encryption.py`)
   - Returns DecryptResponse with:
     - success: true
     - message (plaintext)

9. **Frontend Display** (`frontend/src/pages/ExtractMessage.jsx`)
   - Displays decrypted message
   - Shows copy to clipboard button

**Success Criteria**:
- Message decrypted successfully
- Original message recovered
- Authentication verified (GCM)

**Error Handling**:
- Wrong password → 400 Bad Request (decryption fails)
- Wrong salt → 400 Bad Request (key derivation fails)
- Wrong IV → 400 Bad Request (decryption fails)
- Tampered ciphertext → 400 Bad Request (authentication fails)
- Decryption failure → 500 Internal Server Error

---

## Platform Verification Workflow

### Platform Signature Generation

**Purpose**: Generate HMAC-SHA256 platform signature for authenticity

**Prerequisites**:
- Backend server running on port 8000
- platform_secret_key configured in environment
- Payload data ready for embedding

**Steps**:

1. **Signature Request** (`backend/app/services/platform_verification_service.py`)
   - Called by steganography service before embedding
   - Input: encrypted_payload_binary, media_type

2. **Media Type Validation** (`backend/app/services/platform_verification_service.py`)
   - Validates media_type is supported
   - Supported: image, video, audio, document
   - Raises error if unsupported

3. **Timestamp Generation** (`backend/app/verification/platform_signature.py`)
   - Generates ISO-8601 timestamp
   - Format: UTC with 'Z' suffix
   - Used for audit trail

4. **Data Preparation** (`backend/app/verification/platform_signature.py`)
   - Creates data to sign:
     ```json
     {
       "platform": "SecureStego",
       "version": "1.0.0",
       "mediaType": "image",
       "createdAt": "timestamp",
       "payloadHash": "SHA256 of payload" (optional)
     }
     ```
   - Converts to JSON string (sorted keys, no spaces)

5. **HMAC Generation** (`backend/app/verification/platform_signature.py`)
   - Generates HMAC-SHA256:
     - Key: platform_secret_key (from environment)
     - Data: JSON string
     - Algorithm: SHA256
   - Returns 32-byte signature

6. **Signature Encoding** (`backend/app/verification/platform_signature.py`)
   - Encodes signature to base64
   - Creates signature structure:
     ```json
     {
       "platform": "SecureStego",
       "version": "1.0",
       "signature": "base64 signature",
       "createdAt": "timestamp",
       "mediaType": "image"
     }
     ```

7. **Signature Serialization** (`backend/app/verification/platform_signature.py`)
   - Serializes signature structure to binary
   - Converts to JSON string
   - Encodes to UTF-8 bytes

8. **Payload Combination** (`backend/app/services/platform_verification_service.py`)
   - Creates combined payload:
     - Format: [signature_length (4 bytes)][signature_binary][encrypted_payload_binary]
   - signature_length: 4 bytes, big-endian
   - Returns combined payload and signature info

**Success Criteria**:
- Signature generated successfully
- HMAC-SHA256 computed correctly
- Signature bound to payload (if payloadHash included)
- Signature includes timestamp and media type

---

### Platform Signature Verification

**Purpose**: Verify HMAC-SHA256 platform signature for authenticity

**Prerequisites**:
- Backend server running on port 8000
- platform_secret_key configured in environment
- Combined payload extracted from media

**Steps**:

1. **Verification Request** (`backend/app/services/platform_verification_service.py`)
   - Called by steganography service after extraction
   - Input: combined_payload, actual_media_type

2. **Payload Validation** (`backend/app/services/platform_verification_service.py`)
   - Validates combined_payload size >= 4 bytes
   - Raises MissingSignatureError if too small

3. **Signature Length Extraction** (`backend/app/services/platform_verification_service.py`)
   - Extracts signature_length from first 4 bytes
   - Decodes as big-endian integer
   - Validates length is valid

4. **Signature Extraction** (`backend/app/services/platform_verification_service.py`)
   - Extracts signature_binary from bytes 4 to 4+signature_length
   - Extracts encrypted_payload from bytes 4+signature_length to end
   - Validates extraction succeeded

5. **Signature Deserialization** (`backend/app/verification/signature_validator.py`)
   - Deserializes signature_binary to JSON
   - Validates signature structure
   - Extracts signature fields

6. **Platform Validation** (`backend/app/verification/signature_validator.py`)
   - Validates platform == "SecureStego"
   - Raises PlatformMismatchError if invalid

7. **Version Validation** (`backend/app/verification/signature_validator.py`)
   - Validates version == "1.0"
   - Raises VersionMismatchError if invalid

8. **Media Type Validation** (`backend/app/verification/signature_validator.py`)
   - Validates mediaType == actual_media_type
   - Raises MediaTypeMismatchError if invalid

9. **HMAC Verification** (`backend/app/verification/signature_validator.py`)
   - Recomputes HMAC-SHA256:
     - Key: platform_secret_key
     - Data: signature metadata + payload data
   - Compares with stored signature
   - Raises TamperedSignatureError if mismatch

10. **Verification Result** (`backend/app/services/platform_verification_service.py`)
    - Returns encrypted_payload and verification_result
    - verification_result includes:
      - valid: true/false
      - platform: "SecureStego"
      - version: "1.0"
      - mediaType: "image"
      - diagnostics: detailed verification info

**Success Criteria**:
- Signature verified successfully
- Platform identity confirmed
- Version compatibility confirmed
- Media type match confirmed
- HMAC integrity confirmed

**Error Handling**:
- Missing signature → MissingSignatureError
- Invalid signature format → InvalidSignatureError
- Platform mismatch → PlatformMismatchError
- Version mismatch → VersionMismatchError
- Media type mismatch → MediaTypeMismatchError
- HMAC mismatch → TamperedSignatureError

---

## Upload Workflow

**Purpose**: Handle file uploads for steganography operations

**Prerequisites**:
- Backend server running on port 8000
- User has a file to upload

**Steps**:

1. **File Selection** (`frontend/src/components/ui/FileUpload.jsx`)
   - User selects file via file input
   - Frontend validates file type
   - Frontend validates file size
   - Displays file preview

2. **Upload Request** (`frontend/src/services/apiService.js`)
   - Frontend creates FormData
   - Appends file to FormData
   - Sends POST request with FormData
   - Content-Type: multipart/form-data

3. **File Reception** (`backend/app/routes/*.py`)
   - Backend receives UploadFile
   - Validates file is present
   - Validates file extension
   - Saves to temporary location

4. **File Validation** (`backend/app/*_processing/*_validator.py`)
   - Validates file format
   - Validates file size limits
   - Validates file integrity
   - Raises error if invalid

5. **Temporary Storage** (`backend/app/routes/*.py`)
   - Uses tempfile.NamedTemporaryFile
   - Sets delete=False for later cleanup
   - Returns file path for processing

6. **Processing** (various services)
   - Processing modules use temporary file path
   - Read and process file
   - Generate output

**Success Criteria**:
- File uploaded successfully
- File validated successfully
- File saved to temporary location
- File path available for processing

**Error Handling**:
- No file uploaded → 400 Bad Request
- Invalid file format → 400 Bad Request
- File size exceeded → 400 Bad Request
- File corruption → 400 Bad Request

---

## Download Workflow

**Purpose**: Serve stego files for download

**Prerequisites**:
- Backend server running on port 8000
- Stego file exists in temporary directory
- User has filename from embed response

**Steps**:

1. **Download Request** (`frontend/src/services/apiService.js`)
   - Frontend calls download function
   - Sends GET request to `/api/{media}/download/{filename}`
   - Accepts binary response

2. **File Lookup** (`backend/app/routes/*.py`)
   - Backend receives filename
   - Constructs file path in temp directory
   - Checks if file exists

3. **File Validation** (`backend/app/routes/*.py`)
   - Validates file exists
   - Raises 404 if not found
   - Validates file is accessible

4. **File Serving** (`backend/app/routes/*.py`)
   - Returns FileResponse
   - Sets appropriate media_type:
     - image: "image/png"
     - video: "video/mp4"
     - audio: "audio/wav"
     - document: "application/pdf" or "text/plain"
   - Sets filename for download

5. **Blob Reception** (`frontend/src/services/apiService.js`)
   - Frontend receives blob
   - Creates object URL
   - Creates download link
   - Triggers browser download

6. **URL Cleanup** (`frontend/src/services/apiService.js`)
   - Revokes object URL after download
   - Removes download link from DOM

**Success Criteria**:
- File downloaded successfully
- File content preserved
- Correct filename used
- Correct media type served

**Error Handling**:
- File not found → 404 Not Found
- File expired → 404 Not Found
- Server error → 500 Internal Server Error

---

## Extraction Workflow

**Purpose**: Extract hidden data from stego media

**Prerequisites**:
- Backend server running on port 8000
- User has stego media file
- User has password (for audio) or salt/IV (for images)

**Steps**:

1. **File Upload** (Upload Workflow)
   - User uploads stego file
   - Backend validates file
   - Backend saves to temporary location

2. **Media Processing** (various processing modules)
   - **Image**: Edge detection
   - **Video**: Frame extraction
   - **Audio**: Audio loading
   - **Document**: Document parsing

3. **Data Extraction** (various steganography modules)
   - **Image**: LSB extraction from edge pixels
   - **Video**: DCT extraction from selected frames
   - **Audio**: LSB extraction from selected samples
   - **Document**: Invisible character/structure extraction

4. **Platform Verification** (Platform Verification Workflow)
   - Extract platform signature
   - Verify HMAC-SHA256
   - Validate platform, version, media type
   - Return encrypted payload if valid

5. **Payload Deserialization** (`backend/app/utils/payload_deserializer.py`)
   - Deserialize binary to JSON
   - Validate payload structure
   - Extract encrypted data

6. **Response** (various routes)
   - Return encrypted data and metadata
   - Include extraction statistics
   - Include processing time

7. **Decryption** (Decryption Workflow)
   - User provides password, salt, IV
   - Backend decrypts encrypted data
   - Returns plaintext message

**Success Criteria**:
- Data extracted successfully
- Platform signature verified
- Payload deserialized successfully
- Message decrypted successfully

**Error Handling**:
- Invalid file format → 400 Bad Request
- No hidden data → 400 Bad Request
- Invalid signature → 400 Bad Request
- Wrong password → 400 Bad Request
- Decryption failure → 500 Internal Server Error

---

## Summary

This workflow documentation provides detailed step-by-step procedures for all major operations in SecureStego:

1. **Image Workflow**: Embedding and extraction using edge-based LSB
2. **Video Workflow**: Embedding and extraction using DCT-based steganography
3. **Audio Workflow**: Embedding and extraction using randomized LSB
4. **Document Workflow**: Embedding and extraction using hybrid steganography
5. **Encryption Workflow**: Argon2id + AES-256-GCM encryption
6. **Decryption Workflow**: Argon2id + AES-256-GCM decryption
7. **Platform Verification Workflow**: HMAC-SHA256 signature generation and verification
8. **Upload Workflow**: File upload and validation
9. **Download Workflow**: File serving and download
10. **Extraction Workflow**: General extraction process

Each workflow includes:
- Prerequisites
- Detailed step-by-step process
- File locations and function calls
- Success criteria
- Error handling

This documentation enables developers to:
- Understand the complete flow of each operation
- Debug issues by tracing through the workflow
- Identify where failures occur
- Understand the interaction between components
- Implement new features following established patterns
