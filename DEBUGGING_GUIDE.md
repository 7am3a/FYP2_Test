# SecureStego Debugging Guide

## Table of Contents
1. [General Debugging Approach](#general-debugging-approach)
2. [Encryption Debugging](#encryption-debugging)
3. [Decryption Debugging](#decryption-debugging)
4. [Image Steganography Debugging](#image-steganography-debugging)
5. [Video Steganography Debugging](#video-steganography-debugging)
6. [Audio Steganography Debugging](#audio-steganography-debugging)
7. [Document Steganography Debugging](#document-steganography-debugging)
8. [Platform Verification Debugging](#platform-verification-debugging)
9. [Frontend Debugging](#frontend-debugging)
10. [Backend Debugging](#backend-debugging)
11. [Common Issues and Solutions](#common-issues-and-solutions)

---

## General Debugging Approach

### Debugging Checklist

1. **Check Logs**
   - Frontend: Browser console (F12)
   - Backend: Terminal output or log file

2. **Check Network Requests**
   - Browser DevTools → Network tab
   - Check request/response status codes
   - Check request/response payloads

3. **Check Configuration**
   - Frontend: VITE_API_URL in .env
   - Backend: .env file with all required variables

4. **Check Dependencies**
   - Frontend: npm install
   - Backend: pip install -r requirements.txt

5. **Check External Tools**
   - FFmpeg installed and in PATH
   - Browser supports Web Crypto API

---

## Encryption Debugging

### Feature: Message Encryption

**Files to Check** (in order):
1. `frontend/src/pages/HideMessage.jsx` - User input and API call
2. `frontend/src/services/apiService.js` - API request
3. `backend/app/routes/encryption.py` - Route handler
4. `backend/app/services/crypto_service.py` - Encryption logic
5. `backend/app/config/settings.py` - Argon2id parameters

**Logs to Check**:
- Frontend: Console errors in HideMessage.jsx
- Backend: "Received encryption request" in encryption.py
- Backend: "Encryption completed successfully" in crypto_service.py
- Backend: "Encryption error" in crypto_service.py

**API Endpoints**:
- POST /api/encryption/encrypt

**Services Involved**:
- crypto_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Encryption fails | Empty message or password | Validate input before sending |
| Encryption fails | Backend not running | Start backend server |
| Encryption fails | Missing dependencies | Run `pip install -r requirements.txt` |
| Slow encryption | Argon2id parameters too high | Adjust argon2 parameters in .env |
| Wrong ciphertext | Salt/IV not stored correctly | Ensure salt/IV are saved and transmitted |

**Debugging Steps**:

1. **Frontend Debugging**:
   ```javascript
   // In HideMessage.jsx, add console.log
   console.log('Encrypting:', message, password);
   console.log('Response:', encryptionResponse);
   ```

2. **Backend Debugging**:
   ```python
   # In crypto_service.py, logs are already present
   # Check backend terminal for:
   # - "Starting encryption process"
   # - "Encryption completed successfully"
   # - "Encryption error"
   ```

3. **Configuration Check**:
   ```bash
   # Check .env file has:
   # - argon2_time_cost
   # - argon2_memory_cost
   # - argon2_parallelism
   # - argon2_hash_len
   # - argon2_salt_len
   ```

---

## Decryption Debugging

### Feature: Message Decryption

**Files to Check** (in order):
1. `frontend/src/pages/ExtractMessage.jsx` - User input and API call
2. `frontend/src/services/apiService.js` - API request
3. `backend/app/routes/encryption.py` - Route handler
4. `backend/app/services/crypto_service.py` - Decryption logic
5. `backend/app/config/settings.py` - Argon2id parameters

**Logs to Check**:
- Frontend: Console errors in ExtractMessage.jsx
- Backend: "Received decryption request" in encryption.py
- Backend: "Decryption completed successfully" in crypto_service.py
- Backend: "Decryption error" in crypto_service.py

**API Endpoints**:
- POST /api/encryption/decrypt

**Services Involved**:
- crypto_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Decryption fails | Wrong password | Verify password matches encryption password |
| Decryption fails | Wrong salt | Verify salt matches encryption salt |
| Decryption fails | Wrong IV | Verify IV matches encryption IV |
| Decryption fails | Tampered ciphertext | Data corruption during transmission |
| Decryption fails | Wrong Argon2id parameters | Parameters must match encryption |

**Debugging Steps**:

1. **Frontend Debugging**:
   ```javascript
   // In ExtractMessage.jsx, add console.log
   console.log('Decrypting:', ciphertext, password, salt, iv);
   console.log('Response:', decryptResponse);
   ```

2. **Backend Debugging**:
   ```python
   # In crypto_service.py, logs are already present
   # Check backend terminal for:
   # - "Starting decryption process"
   # - "Decryption completed successfully"
   # - "Decryption error"
   ```

3. **Validation Check**:
   ```python
   # Verify salt/IV are valid base64
   import base64
   try:
       base64.b64decode(salt)
       base64.b64decode(iv)
   except Exception as e:
       print(f"Invalid base64: {e}")
   ```

---

## Image Steganography Debugging

### Feature: Image Embedding

**Files to Check** (in order):
1. `frontend/src/pages/HideMessage.jsx` - User input and API call
2. `frontend/src/services/apiService.js` - API request
3. `backend/app/routes/steganography.py` - Route handler
4. `backend/app/services/steganography_service.py` - Orchestration
5. `backend/app/image_processing/image_validator.py` - Image validation
6. `backend/app/image_processing/image_converter.py` - Image conversion
7. `backend/app/image_processing/edge_detector.py` - Edge detection
8. `backend/app/utils/payload_serializer.py` - Payload serialization
9. `backend/app/services/platform_verification_service.py` - Signature injection
10. `backend/app/steganography/edge_lsb_embedder.py` - LSB embedding

**Logs to Check**:
- Frontend: Console errors in HideMessage.jsx
- Backend: "Received steganography embed request" in steganography.py
- Backend: "Image uploaded" in steganography.py
- Backend: "Edge detection complete" in edge_detector.py
- Backend: "Payload created" in payload_serializer.py
- Backend: "Platform signature injected" in platform_verification_service.py
- Backend: "Payload embedded" in steganography_service.py
- Backend: "Embed workflow completed" in steganography_service.py

**API Endpoints**:
- POST /api/steganography/embed

**Services Involved**:
- steganography_service.py
- platform_verification_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Embedding fails | Invalid image format | Use PNG, JPG, JPEG, or HEIC |
| Embedding fails | Image size exceeded | Use smaller image or increase limit |
| Embedding fails | Capacity exceeded | Use larger image with more edges |
| Embedding fails | Edge detection failed | Check OpenCV installation |
| Embedding fails | Platform signature error | Check platform_secret_key in .env |
| Stego image corrupted | LSB embedding error | Check edge_lsb_embedder.py logs |

**Debugging Steps**:

1. **Frontend Debugging**:
   ```javascript
   // In HideMessage.jsx, add console.log
   console.log('Embedding:', file, encryptedMessage);
   console.log('Response:', stegoResponse);
   ```

2. **Backend Debugging**:
   ```python
   # In steganography_service.py, logs are already present
   # Check backend terminal for each step:
   # - "Starting embed workflow"
   # - "Step 1: Validating image"
   # - "Step 2: Converting image to PNG"
   # - "Step 3: Detecting edges"
   # - "Step 4: Creating structured payload"
   # - "Step 4.5: Injecting platform signature"
   # - "Step 5: Checking capacity"
   # - "Step 6: Embedding payload"
   # - "Embed workflow completed"
   ```

3. **Image Validation**:
   ```python
   # Manually test image loading
   from PIL import Image
   img = Image.open('test.jpg')
   print(f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}")
   ```

4. **Edge Detection Test**:
   ```python
   # Manually test edge detection
   import cv2
   img = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)
   edges = cv2.Canny(img, 50, 150)
   print(f"Edge pixels: {cv2.countNonZero(edges)}")
   ```

---

### Feature: Image Extraction

**Files to Check** (in order):
1. `frontend/src/pages/ExtractMessage.jsx` - User input and API call
2. `frontend/src/services/apiService.js` - API request
3. `backend/app/routes/steganography.py` - Route handler
4. `backend/app/services/steganography_service.py` - Orchestration
5. `backend/app/image_processing/edge_detector.py` - Edge detection
6. `backend/app/steganography/edge_lsb_extractor.py` - LSB extraction
7. `backend/app/services/platform_verification_service.py` - Signature verification
8. `backend/app/utils/payload_deserializer.py` - Payload deserialization

**Logs to Check**:
- Frontend: Console errors in ExtractMessage.jsx
- Backend: "Received steganography extract request" in steganography.py
- Backend: "Stego image uploaded" in steganography.py
- Backend: "Edge detection complete" in edge_detector.py
- Backend: "Combined payload extracted" in steganography_service.py
- Backend: "Platform signature verified" in platform_verification_service.py
- Backend: "Platform signature verification failed" in platform_verification_service.py
- Backend: "Extract workflow completed" in steganography_service.py

**API Endpoints**:
- POST /api/steganography/extract

**Services Involved**:
- steganography_service.py
- platform_verification_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Extraction fails | Invalid image format | Must be PNG |
| Extraction fails | No hidden data | Image does not contain hidden message |
| Extraction fails | Invalid signature | Platform signature verification failed |
| Extraction fails | Signature tampered | File was modified after embedding |
| Extraction fails | Wrong edge detection | Edge detection parameters changed |
| Wrong message extracted | Edge coordinates mismatch | Edge detection must be deterministic |

**Debugging Steps**:

1. **Frontend Debugging**:
   ```javascript
   // In ExtractMessage.jsx, add console.log
   console.log('Extracting:', file);
   console.log('Response:', stegoResponse);
   ```

2. **Backend Debugging**:
   ```python
   # In steganography_service.py, logs are already present
   # Check backend terminal for each step:
   # - "Starting extract workflow"
   # - "Step 1: Validating image"
   # - "Step 2: Detecting edges"
   # - "Step 3: Extracting payload"
   # - "Step 3.5: Verifying platform signature"
   # - "Step 4: Deserializing payload"
   # - "Extract workflow completed"
   ```

3. **Signature Verification**:
   ```python
   # Check signature verification diagnostics
   # In platform_verification_service.py, look for:
   # - "Platform signature verified successfully"
   # - "Platform signature verification failed"
   # - Verification result diagnostics
   ```

4. **Edge Detection Consistency**:
   ```python
   # Ensure edge detection is deterministic
   # Same image should produce same edge map
   # Check Canny parameters are consistent
   ```

---

## Video Steganography Debugging

### Feature: Video Embedding

**Files to Check** (in order):
1. `backend/app/routes/video_steganography.py` - Route handler
2. `backend/app/services/video_steganography_service.py` - Orchestration
3. `backend/app/video_processing/video_validator.py` - Video validation
4. `backend/app/video_processing/video_converter.py` - Video conversion
5. `backend/app/video_processing/frame_extractor.py` - Frame extraction
6. `backend/app/steganography/video/frame_selector.py` - Frame selection
7. `backend/app/steganography/video/dct_embedder.py` - DCT embedding
8. `backend/app/video_processing/frame_rebuilder.py` - Video rebuilding

**Logs to Check**:
- Backend: "Received video steganography embed request" in video_steganography.py
- Backend: "Video uploaded" in video_steganography.py
- Backend: Frame extraction logs
- Backend: Frame selection logs
- Backend: DCT embedding logs
- Backend: Video rebuilding logs

**API Endpoints**:
- POST /api/video/embed

**Services Involved**:
- video_steganography_service.py
- platform_verification_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Embedding fails | Invalid video format | Use MP4, AVI, or MOV |
| Embedding fails | FFmpeg not installed | Install FFmpeg and add to PATH |
| Embedding fails | Frame extraction failed | Check FFmpeg installation |
| Embedding fails | Capacity exceeded | Use longer video or reduce payload |
| Embedding fails | Audio preservation failed | Check audio_handler.py |
| Stego video corrupted | Frame rebuilding failed | Check frame_rebuilder.py |

**Debugging Steps**:

1. **FFmpeg Check**:
   ```bash
   # Check FFmpeg installation
   ffmpeg -version
   
   # Check if FFmpeg is in PATH
   which ffmpeg
   ```

2. **Frame Extraction Test**:
   ```python
   # Manually test frame extraction
   import cv2
   cap = cv2.VideoCapture('test.mp4')
   frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
   print(f"Total frames: {frame_count}")
   ```

3. **DCT Transform Test**:
   ```python
   # Test DCT transform
   import numpy as np
   from scipy.fftpack import dct, idct
   block = np.random.rand(8, 8)
   dct_block = dct(dct(block, axis=0), axis=1)
   reconstructed = idct(idct(dct_block, axis=0), axis=1)
   ```

---

### Feature: Video Extraction

**Files to Check** (in order):
1. `backend/app/routes/video_steganography.py` - Route handler
2. `backend/app/services/video_steganography_service.py` - Orchestration
3. `backend/app/video_processing/frame_extractor.py` - Frame extraction
4. `backend/app/steganography/video/frame_selector.py` - Frame selection
5. `backend/app/steganography/video/dct_extractor.py` - DCT extraction

**Logs to Check**:
- Backend: "Received video steganography extract request" in video_steganography.py
- Backend: Frame extraction logs
- Backend: Frame selection logs
- Backend: DCT extraction logs

**API Endpoints**:
- POST /api/video/extract

**Services Involved**:
- video_steganography_service.py
- platform_verification_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Extraction fails | Invalid video format | Must be MP4 |
| Extraction fails | No hidden data | Video does not contain hidden message |
| Extraction fails | Frame selection mismatch | Frame selection strategy must match |
| Extraction fails | DCT extraction failed | Check dct_extractor.py |

**Debugging Steps**:

1. **Frame Selection Consistency**:
   ```python
   # Ensure frame selection is deterministic
   # Same strategy and parameters should select same frames
   ```

2. **DCT Extraction Test**:
   ```python
   # Test DCT extraction
   # Verify DCT coefficients are correctly extracted
   ```

---

## Audio Steganography Debugging

### Feature: Audio Embedding

**Files to Check** (in order):
1. `backend/app/routes/audio_steganography.py` - Route handler
2. `backend/app/services/audio_steganography_service.py` - Orchestration
3. `backend/app/audio_processing/audio_validator.py` - Audio validation
4. `backend/app/audio_processing/audio_converter.py` - Audio conversion
5. `backend/app/audio_processing/audio_loader.py` - Audio loading
6. `backend/app/steganography/audio/sample_selector.py` - Sample position generation
7. `backend/app/steganography/audio/audio_lsb_embedder.py` - LSB embedding
8. `backend/app/audio_processing/audio_writer.py` - Audio writing

**Logs to Check**:
- Backend: "Received audio steganography embed request" in audio_steganography.py
- Backend: "Audio uploaded" in audio_steganography.py
- Backend: Audio conversion logs
- Backend: Sample position generation logs
- Backend: LSB embedding logs

**API Endpoints**:
- POST /api/audio/embed

**Services Involved**:
- audio_steganography_service.py
- platform_verification_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Embedding fails | Invalid audio format | Use WAV, MP3, M4A, or FLAC |
| Embedding fails | FFmpeg not installed | Install FFmpeg and add to PATH |
| Embedding fails | Audio conversion failed | Check FFmpeg installation |
| Embedding fails | Capacity exceeded | Use longer audio or reduce payload |
| Embedding fails | Sample position generation failed | Check password and sample_selector.py |
| Stego audio corrupted | LSB embedding failed | Check audio_lsb_embedder.py |

**Debugging Steps**:

1. **FFmpeg Check**:
   ```bash
   # Check FFmpeg installation
   ffmpeg -version
   ```

2. **Audio Loading Test**:
   ```python
   # Manually test audio loading
   import numpy as np
   # Test with scipy or soundfile
   from scipy.io import wavfile
   sample_rate, data = wavfile.read('test.wav')
   print(f"Sample rate: {sample_rate}, Shape: {data.shape}")
   ```

3. **Sample Position Test**:
   ```python
   # Test sample position generation
   # Ensure same password generates same positions
   ```

---

### Feature: Audio Extraction

**Files to Check** (in order):
1. `backend/app/routes/audio_steganography.py` - Route handler
2. `backend/app/services/audio_steganography_service.py` - Orchestration
3. `backend/app/audio_processing/audio_loader.py` - Audio loading
4. `backend/app/steganography/audio/sample_selector.py` - Sample position generation
5. `backend/app/steganography/audio/audio_lsb_extractor.py` - LSB extraction

**Logs to Check**:
- Backend: "Received audio steganography extract request" in audio_steganography.py
- Backend: Sample position generation logs
- Backend: LSB extraction logs

**API Endpoints**:
- POST /api/audio/extract

**Services Involved**:
- audio_steganography_service.py
- platform_verification_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Extraction fails | Invalid audio format | Must be WAV |
| Extraction fails | No hidden data | Audio does not contain hidden message |
| Extraction fails | Wrong password | Sample positions depend on password |
| Extraction fails | Sample position mismatch | Password must match embedding password |

**Debugging Steps**:

1. **Sample Position Consistency**:
   ```python
   # Ensure sample positions are deterministic
   # Same password should generate same positions
   ```

2. **LSB Extraction Test**:
   ```python
   # Test LSB extraction
   # Verify bits are correctly extracted
   ```

---

## Document Steganography Debugging

### Feature: Document Embedding

**Files to Check** (in order):
1. `backend/app/routes/document_steganography.py` - Route handler
2. `backend/app/services/document_steganography_service.py` - Orchestration
3. `backend/app/document_processing/document_validator.py` - Document validation
4. `backend/app/document_processing/pdf_parser.py` - PDF parsing
5. `backend/app/document_processing/txt_handler.py` - TXT handling
6. `backend/app/steganography/invisible_character_embedder.py` - Invisible character embedding
7. `backend/app/steganography/structure_embedder.py` - Structure embedding
8. `backend/app/steganography/pdf_image_processor.py` - PDF image processing

**Logs to Check**:
- Backend: "Received document steganography embed request" in document_steganography.py
- Backend: "Document uploaded" in document_steganography.py
- Backend: PDF parsing logs
- Backend: Text embedding logs
- Backend: Image embedding logs

**API Endpoints**:
- POST /api/document/embed

**Services Involved**:
- document_steganography_service.py
- platform_verification_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Embedding fails | Invalid document format | Use PDF or TXT |
| Embedding fails | PDF parsing failed | Check PyMuPDF installation |
| Embedding fails | Capacity exceeded | Use longer document or reduce payload |
| Embedding fails | Text embedding failed | Check invisible_character_embedder.py |
| Embedding fails | Image embedding failed | Check pdf_image_processor.py |
| Stego document corrupted | PDF rebuilding failed | Check pdf_rebuilder.py |

**Debugging Steps**:

1. **PyMuPDF Check**:
   ```python
   # Check PyMuPDF installation
   import fitz
   print(f"PyMuPDF version: {fitz.version}")
   ```

2. **PDF Parsing Test**:
   ```python
   # Manually test PDF parsing
   import fitz
   doc = fitz.open('test.pdf')
   print(f"Pages: {len(doc)}")
   for page in doc:
       print(f"Page {page.number}: {page.get_text()}")
   ```

3. **Invisible Character Test**:
   ```python
   # Test invisible character embedding
   # Verify invisible characters are preserved
   ```

---

### Feature: Document Extraction

**Files to Check** (in order):
1. `backend/app/routes/document_steganography.py` - Route handler
2. `backend/app/services/document_steganography_service.py` - Orchestration
3. `backend/app/document_processing/pdf_parser.py` - PDF parsing
4. `backend/app/document_processing/txt_handler.py` - TXT handling
5. `backend/app/steganography/invisible_character_extractor.py` - Invisible character extraction
6. `backend/app/steganography/structure_extractor.py` - Structure extraction
7. `backend/app/steganography/pdf_image_processor.py` - PDF image processing

**Logs to Check**:
- Backend: "Received document steganography extract request" in document_steganography.py
- Backend: PDF parsing logs
- Backend: Text extraction logs
- Backend: Image extraction logs

**API Endpoints**:
- POST /api/document/extract

**Services Involved**:
- document_steganography_service.py
- platform_verification_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Extraction fails | Invalid document format | Use PDF or TXT |
| Extraction fails | No hidden data | Document does not contain hidden message |
| Extraction fails | Text extraction failed | Check invisible_character_extractor.py |
| Extraction fails | Image extraction failed | Check pdf_image_processor.py |
| Extraction fails | Payload combination failed | Check payload combination logic |

**Debugging Steps**:

1. **Invisible Character Extraction**:
   ```python
   # Test invisible character extraction
   # Verify invisible characters are correctly extracted
   ```

2. **Payload Combination**:
   ```python
   # Test payload combination
   # Verify text and image payloads are correctly combined
   ```

---

## Platform Verification Debugging

### Feature: Platform Signature Generation

**Files to Check** (in order):
1. `backend/app/services/platform_verification_service.py` - Orchestration
2. `backend/app/verification/platform_signature.py` - Signature generation
3. `backend/app/config/settings.py` - Platform secret key

**Logs to Check**:
- Backend: "Preparing payload for embedding" in platform_verification_service.py
- Backend: "Platform signature generated" in platform_signature.py
- Backend: "Payload prepared for embedding" in platform_verification_service.py

**Services Involved**:
- platform_verification_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Signature generation fails | platform_secret_key not set | Set PLATFORM_SECRET_KEY in .env |
| Signature generation fails | Invalid secret key format | Must be 64-character hex string |
| Signature generation fails | Payload too large | Reduce payload size |

**Debugging Steps**:

1. **Configuration Check**:
   ```bash
   # Check .env file
   # PLATFORM_SECRET_KEY must be set
   # Format: 64-character hex string
   ```

2. **Secret Key Validation**:
   ```python
   # Validate secret key format
   import re
   key = settings.platform_secret_key
   if not re.match(r'^[a-fA-F0-9]{64}$', key):
       print("Invalid secret key format")
   ```

3. **Signature Test**:
   ```python
   # Manually test signature generation
   from app.verification.platform_signature import platform_signature
   sig = platform_signature.generate_signature("image", b"test")
   print(f"Signature: {sig}")
   ```

---

### Feature: Platform Signature Verification

**Files to Check** (in order):
1. `backend/app/services/platform_verification_service.py` - Orchestration
2. `backend/app/verification/signature_validator.py` - Signature validation
3. `backend/app/verification/platform_signature.py` - Signature generation (for recomputation)
4. `backend/app/config/settings.py` - Platform secret key

**Logs to Check**:
- Backend: "Extracting and verifying signature" in platform_verification_service.py
- Backend: "Platform signature verified successfully" in platform_verification_service.py
- Backend: "Platform signature verification failed" in platform_verification_service.py
- Backend: Verification diagnostics

**Services Involved**:
- platform_verification_service.py

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Verification fails | Signature missing | File does not contain platform signature |
| Verification fails | Invalid signature format | Signature corrupted during extraction |
| Verification fails | Tampered signature | File was modified after embedding |
| Verification fails | Platform mismatch | Different platform generated signature |
| Verification fails | Version mismatch | Incompatible signature version |
| Verification fails | Media type mismatch | Media type does not match embedding |

**Debugging Steps**:

1. **Signature Extraction**:
   ```python
   # Check signature extraction
   # Verify signature length is correct
   # Verify signature binary is valid JSON
   ```

2. **HMAC Verification**:
   ```python
   # Manually test HMAC verification
   # Recompute HMAC and compare
   ```

3. **Diagnostics Check**:
   ```python
   # Check verification diagnostics
   # Look for specific error type
   # - MissingSignatureError
   # - InvalidSignatureError
   # - TamperedSignatureError
   # - VersionMismatchError
   # - PlatformMismatchError
   # - MediaTypeMismatchError
   ```

---

## Frontend Debugging

### General Frontend Debugging

**Files to Check**:
1. `frontend/src/main.jsx` - Entry point
2. `frontend/src/App.jsx` - Router setup
3. `frontend/src/pages/*.jsx` - Page components
4. `frontend/src/services/*.js` - API services
5. `frontend/src/hooks/*.js` - Custom hooks

**Logs to Check**:
- Browser console (F12)
- Network tab (F12)

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Page not loading | React error | Check browser console |
| API call fails | Backend not running | Start backend server |
| API call fails | CORS error | Check CORS configuration |
| API call fails | Wrong API URL | Check VITE_API_URL in .env |
| State not updating | React state issue | Check state management |
| File upload fails | File too large | Check file size limits |

**Debugging Steps**:

1. **Browser Console**:
   ```javascript
   // Open browser console (F12)
   // Check for errors and warnings
   // Add console.log for debugging
   console.log('Debug info');
   ```

2. **Network Tab**:
   ```
   // Open Network tab (F12)
   // Check API requests
   // Check request/response status codes
   // Check request/response payloads
   ```

3. **React DevTools**:
   ```
   // Install React DevTools extension
   // Check component state and props
   // Check component hierarchy
   ```

---

### HideMessage Page Debugging

**Files to Check**:
1. `frontend/src/pages/HideMessage.jsx`
2. `frontend/src/services/apiService.js`
3. `frontend/src/hooks/useEncryption.js`
4. `frontend/src/hooks/useSteganography.js`

**Debugging Steps**:

```javascript
// Add console.log in HideMessage.jsx
const handleEncrypt = async () => {
  console.log('Starting encryption');
  console.log('Message:', message);
  console.log('Password:', password);
  console.log('File:', file);
  
  const encryptionResponse = await encryptMessage(message, password);
  console.log('Encryption response:', encryptionResponse);
  
  const stegoResponse = await embedMessage(file, encryptionResponse.ciphertext, encryptionResponse.algorithm);
  console.log('Steganography response:', stegoResponse);
};
```

---

### ExtractMessage Page Debugging

**Files to Check**:
1. `frontend/src/pages/ExtractMessage.jsx`
2. `frontend/src/services/apiService.js`
3. `frontend/src/hooks/useEncryption.js`
4. `frontend/src/hooks/useSteganography.js`

**Debugging Steps**:

```javascript
// Add console.log in ExtractMessage.jsx
const handleExtract = async () => {
  console.log('Starting extraction');
  console.log('File:', file);
  console.log('Password:', password);
  console.log('Salt:', salt);
  console.log('IV:', iv);
  
  const stegoResponse = await extractMessage(file);
  console.log('Steganography response:', stegoResponse);
  
  const decryptResponse = await decryptMessage(stegoResponse.encryptedData, password, salt, iv);
  console.log('Decryption response:', decryptResponse);
};
```

---

## Backend Debugging

### General Backend Debugging

**Files to Check**:
1. `backend/app/main.py` - Entry point
2. `backend/app/routes/*.py` - Route handlers
3. `backend/app/services/*.py` - Business logic
4. `backend/app/config/settings.py` - Configuration

**Logs to Check**:
- Terminal output
- Log file (if configured)

**Common Issues**:

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Server not starting | Port already in use | Change port or kill process |
| Server not starting | Missing dependencies | Run `pip install -r requirements.txt` |
| API not responding | Route not registered | Check router registration in main.py |
| API not responding | CORS error | Check CORS configuration |
| Service error | Configuration missing | Check .env file |

**Debugging Steps**:

1. **Terminal Output**:
   ```bash
   # Start backend with verbose logging
   uvicorn app.main:app --reload --log-level debug
   ```

2. **Configuration Check**:
   ```python
   # Check settings are loaded correctly
   from app.config import settings
   print(f"App name: {settings.app_name}")
   print(f"Debug mode: {settings.debug}")
   print(f"API prefix: {settings.api_prefix}")
   ```

3. **Route Registration**:
   ```python
   # Check routes are registered
   # Visit /api/docs to see all available routes
   ```

---

### Encryption Service Debugging

**Files to Check**:
1. `backend/app/services/crypto_service.py`
2. `backend/app/config/settings.py`

**Debugging Steps**:

```python
# Add debug logging in crypto_service.py
def encrypt_message(self, message: str, password: str) -> Dict[str, str]:
    logger.info(f"Message length: {len(message)}")
    logger.info(f"Password length: {len(password)}")
    logger.info(f"Argon2id parameters: time_cost={self.argon2_time_cost}, memory_cost={self.argon2_memory_cost}")
    # ... rest of function
```

---

### Steganography Service Debugging

**Files to Check**:
1. `backend/app/services/steganography_service.py`
2. `backend/app/image_processing/*.py`
3. `backend/app/steganography/*.py`

**Debugging Steps**:

```python
# Add debug logging in steganography_service.py
def embed_message(self, image_path: str, encrypted_data: str, algorithm: str = "AES-256-GCM") -> Dict:
    logger.info(f"Image path: {image_path}")
    logger.info(f"Encrypted data length: {len(encrypted_data)}")
    logger.info(f"Algorithm: {algorithm}")
    # ... rest of function
```

---

## Common Issues and Solutions

### Issue: Backend not starting

**Possible Causes**:
- Port already in use
- Missing dependencies
- Configuration error

**Solutions**:
```bash
# Kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Install dependencies
pip install -r requirements.txt

# Check configuration
cat .env
```

---

### Issue: Frontend cannot connect to backend

**Possible Causes**:
- Backend not running
- CORS error
- Wrong API URL

**Solutions**:
```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Check CORS configuration
# In backend/app/config/settings.py
cors_origins = ["http://localhost:5173", "http://localhost:3000"]

# Check frontend API URL
# In frontend/.env
VITE_API_URL=http://localhost:8000/api
```

---

### Issue: File upload fails

**Possible Causes**:
- File too large
- Invalid file format
- Missing multipart support

**Solutions**:
```python
# Check file size limits in settings.py
max_file_size_mb: int = 100
max_image_size_mb: int = 50

# Check file format validation in routes
allowed_extensions = ['.png', '.jpg', '.jpeg', '.heic']
```

---

### Issue: Encryption fails

**Possible Causes**:
- Empty message or password
- Wrong Argon2id parameters
- Missing dependencies

**Solutions**:
```bash
# Install dependencies
pip install argon2-cffi cryptography

# Check Argon2id parameters in .env
argon2_time_cost=3
argon2_memory_cost=65536
argon2_parallelism=4
argon2_hash_len=32
argon2_salt_len=16
```

---

### Issue: Steganography fails

**Possible Causes**:
- Capacity exceeded
- Edge detection failed
- Platform signature error

**Solutions**:
```python
# Check capacity calculation
# Use larger image with more edges

# Check OpenCV installation
pip install opencv-python

# Check platform secret key
PLATFORM_SECRET_KEY=<64-character hex string>
```

---

### Issue: Platform signature verification fails

**Possible Causes**:
- platform_secret_key not set
- Signature corrupted
- File tampered

**Solutions**:
```bash
# Set platform secret key in .env
PLATFORM_SECRET_KEY=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef

# Ensure secret key is 64-character hex string
```

---

### Issue: Video/Audio processing fails

**Possible Causes**:
- FFmpeg not installed
- FFmpeg not in PATH
- Invalid file format

**Solutions**:
```bash
# Install FFmpeg
# Windows: Download from https://ffmpeg.org/
# Linux/Mac: brew install ffmpeg

# Check FFmpeg installation
ffmpeg -version

# Add FFmpeg to PATH
# Windows: Add to System Environment Variables
# Linux/Mac: Add to ~/.bashrc or ~/.zshrc
```

---

## Summary

This debugging guide provides comprehensive debugging instructions for all features in SecureStego:

1. **General Debugging Approach**: Debugging checklist and methodology
2. **Encryption Debugging**: Files, logs, APIs, services, common issues
3. **Decryption Debugging**: Files, logs, APIs, services, common issues
4. **Image Steganography Debugging**: Embedding and extraction debugging
5. **Video Steganography Debugging**: Embedding and extraction debugging
6. **Audio Steganography Debugging**: Embedding and extraction debugging
7. **Document Steganography Debugging**: Embedding and extraction debugging
8. **Platform Verification Debugging**: Signature generation and verification
9. **Frontend Debugging**: General and page-specific debugging
10. **Backend Debugging**: General and service-specific debugging
11. **Common Issues and Solutions**: Common problems and their solutions

This documentation enables developers to:
- Debug any feature systematically
- Identify where issues occur
- Check logs at each step
- Understand common failure modes
- Apply targeted solutions
- Troubleshoot effectively
