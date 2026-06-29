# SecureStego Bug Location Guide

## Table of Contents
1. [Issue Type Classification](#issue-type-classification)
2. [Encryption Issues](#encryption-issues)
3. [Decryption Issues](#decryption-issues)
4. [Image Steganography Issues](#image-steganography-issues)
5. [Video Steganography Issues](#video-steganography-issues)
6. [Audio Steganography Issues](#audio-steganography-issues)
7. [Document Steganography Issues](#document-steganography-issues)
8. [Platform Verification Issues](#platform-verification-issues)
9. [Frontend Issues](#frontend-issues)
10. [Backend Issues](#backend-issues)
11. [Configuration Issues](#configuration-issues)
12. [Performance Issues](#performance-issues)

---

## Issue Type Classification

### Issue Categories

| Category | Description | Severity |
|-----------|-------------|----------|
| Encryption | Encryption/decryption failures | High |
| Steganography | Embedding/extraction failures | High |
| Platform Verification | Signature generation/verification failures | High |
| Frontend | UI/UX issues, state management | Medium |
| Backend | API issues, service failures | High |
| Configuration | Environment variable issues | High |
| Performance | Slow operations, memory issues | Medium |

---

## Encryption Issues

### Issue: Encryption fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Empty message or password | `frontend/src/pages/HideMessage.jsx` | encryptionService.js | POST /api/encryption/encrypt |
| Backend not running | `backend/app/main.py` | None | All APIs |
| Missing dependencies | `backend/requirements.txt` | crypto_service.py | POST /api/encryption/encrypt |
| Argon2id parameters invalid | `backend/.env` | crypto_service.py | POST /api/encryption/encrypt |
| Salt/IV generation failed | `backend/app/services/crypto_service.py` | crypto_service.py | POST /api/encryption/encrypt |
| AES-256-GCM encryption failed | `backend/app/services/crypto_service.py` | crypto_service.py | POST /api/encryption/encrypt |

**Debugging Priority**:
1. Check backend is running
2. Check dependencies are installed
3. Check Argon2id parameters in .env
4. Check crypto_service.py logs

---

### Issue: Decryption fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Wrong password | `frontend/src/pages/ExtractMessage.jsx` | encryptionService.js | POST /api/encryption/decrypt |
| Wrong salt | `frontend/src/pages/ExtractMessage.jsx` | encryptionService.js | POST /api/encryption/decrypt |
| Wrong IV | `frontend/src/pages/ExtractMessage.jsx` | encryptionService.js | POST /api/encryption/decrypt |
| Tampered ciphertext | `frontend/src/services/apiService.js` | crypto_service.py | POST /api/encryption/decrypt |
| Argon2id parameters mismatch | `backend/.env` | crypto_service.py | POST /api/encryption/decrypt |
| AES-256-GCM decryption failed | `backend/app/services/crypto_service.py` | crypto_service.py | POST /api/encryption/decrypt |

**Debugging Priority**:
1. Verify password matches encryption password
2. Verify salt and IV match encryption values
3. Check Argon2id parameters match encryption
4. Check crypto_service.py logs

---

### Issue: Slow encryption

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Argon2id parameters too high | `backend/.env` | crypto_service.py | POST /api/encryption/encrypt |
| Large message size | `frontend/src/pages/HideMessage.jsx` | crypto_service.py | POST /api/encryption/encrypt |
| System resource constraints | System | crypto_service.py | POST /api/encryption/encrypt |

**Debugging Priority**:
1. Check Argon2id parameters in .env
2. Reduce time_cost or memory_cost
3. Check system resources

---

## Decryption Issues

### Issue: Wrong password error

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| User entered wrong password | `frontend/src/pages/ExtractMessage.jsx` | encryptionService.js | POST /api/encryption/decrypt |
| Password not stored correctly | `frontend/src/services/encryptionService.js` | encryptionService.js | POST /api/encryption/decrypt |
| Password encoding issue | `frontend/src/services/apiService.js` | crypto_service.py | POST /api/encryption/decrypt |

**Debugging Priority**:
1. Verify user input matches encryption password
2. Check password storage in encryptionService.js
3. Check password encoding in API request

---

### Issue: Wrong salt/IV error

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Salt not stored correctly | `frontend/src/services/encryptionService.js` | encryptionService.js | POST /api/encryption/decrypt |
| IV not stored correctly | `frontend/src/services/encryptionService.js` | encryptionService.js | POST /api/encryption/decrypt |
| Base64 encoding issue | `frontend/src/services/apiService.js` | crypto_service.py | POST /api/encryption/decrypt |

**Debugging Priority**:
1. Verify salt and IV are stored in encryptionService.js
2. Check base64 encoding in API request
3. Verify salt and IV match encryption values

---

## Image Steganography Issues

### Issue: Image embedding fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Invalid image format | `frontend/src/pages/HideMessage.jsx` | steganography_service.py | POST /api/steganography/embed |
| Image size exceeded | `backend/app/config/settings.py` | steganography_service.py | POST /api/steganography/embed |
| Image conversion failed | `backend/app/image_processing/image_converter.py` | steganography_service.py | POST /api/steganography/embed |
| Edge detection failed | `backend/app/image_processing/edge_detector.py` | steganography_service.py | POST /api/steganography/embed |
| Capacity exceeded | `backend/app/steganography/edge_lsb_embedder.py` | steganography_service.py | POST /api/steganography/embed |
| Platform signature error | `backend/app/services/platform_verification_service.py` | platform_verification_service.py | POST /api/steganography/embed |
| LSB embedding failed | `backend/app/steganography/edge_lsb_embedder.py` | steganography_service.py | POST /api/steganography/embed |

**Debugging Priority**:
1. Check image format (PNG, JPG, JPEG, HEIC)
2. Check image size limits in settings.py
3. Check image_converter.py logs
4. Check edge_detector.py logs
5. Check capacity calculation
6. Check platform_secret_key in .env
7. Check edge_lsb_embedder.py logs

---

### Issue: Image extraction fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Invalid image format (not PNG) | `frontend/src/pages/ExtractMessage.jsx` | steganography_service.py | POST /api/steganography/extract |
| No hidden data found | `backend/app/steganography/edge_lsb_extractor.py` | steganography_service.py | POST /api/steganography/extract |
| Edge detection mismatch | `backend/app/image_processing/edge_detector.py` | steganography_service.py | POST /api/steganography/extract |
| Platform signature verification failed | `backend/app/services/platform_verification_service.py` | platform_verification_service.py | POST /api/steganography/extract |
| Payload deserialization failed | `backend/app/utils/payload_deserializer.py` | steganography_service.py | POST /api/steganography/extract |
| LSB extraction failed | `backend/app/steganography/edge_lsb_extractor.py` | steganography_service.py | POST /api/steganography/extract |

**Debugging Priority**:
1. Check image format (must be PNG)
2. Check edge_detector.py logs
3. Check platform signature verification
4. Check payload_deserializer.py logs
5. Check edge_lsb_extractor.py logs

---

### Issue: Stego image corrupted

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| LSB embedding error | `backend/app/steganography/edge_lsb_embedder.py` | steganography_service.py | POST /api/steganography/embed |
| Image save error | `backend/app/steganography/edge_lsb_embedder.py` | steganography_service.py | POST /api/steganography/embed |
| Edge pixel coordinates invalid | `backend/app/image_processing/edge_detector.py` | steganography_service.py | POST /api/steganography/embed |

**Debugging Priority**:
1. Check edge_lsb_embedder.py logs
2. Check edge pixel coordinates
3. Check image save operation

---

### Issue: Capacity exceeded error

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Image too small | `frontend/src/pages/HideMessage.jsx` | steganography_service.py | POST /api/steganography/embed |
| Message too large | `frontend/src/pages/HideMessage.jsx` | steganography_service.py | POST /api/steganography/embed |
| Too few edge pixels | `backend/app/image_processing/edge_detector.py` | steganography_service.py | POST /api/steganography/embed |
| Capacity calculation error | `backend/app/steganography/edge_lsb_embedder.py` | steganography_service.py | POST /api/steganography/embed |

**Debugging Priority**:
1. Check image size and edge pixel count
2. Check message size
3. Check capacity calculation in edge_lsb_embedder.py
4. Use larger image with more edges

---

## Video Steganography Issues

### Issue: Video embedding fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Invalid video format | `backend/app/routes/video_steganography.py` | video_steganography_service.py | POST /api/video/embed |
| FFmpeg not installed | System | video_steganography_service.py | POST /api/video/embed |
| Frame extraction failed | `backend/app/video_processing/frame_extractor.py` | video_steganography_service.py | POST /api/video/embed |
| Frame selection failed | `backend/app/steganography/video/frame_selector.py` | video_steganography_service.py | POST /api/video/embed |
| DCT embedding failed | `backend/app/steganography/video/dct_embedder.py` | video_steganography_service.py | POST /api/video/embed |
| Video rebuilding failed | `backend/app/video_processing/frame_rebuilder.py` | video_steganography_service.py | POST /api/video/embed |
| Platform signature error | `backend/app/services/platform_verification_service.py` | platform_verification_service.py | POST /api/video/embed |

**Debugging Priority**:
1. Check video format (MP4, AVI, MOV)
2. Check FFmpeg installation
3. Check frame_extractor.py logs
4. Check frame_selector.py logs
5. Check dct_embedder.py logs
6. Check frame_rebuilder.py logs
7. Check platform_secret_key in .env

---

### Issue: Video extraction fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Invalid video format (not MP4) | `backend/app/routes/video_steganography.py` | video_steganography_service.py | POST /api/video/extract |
| No hidden data found | `backend/app/steganography/video/dct_extractor.py` | video_steganography_service.py | POST /api/video/extract |
| Frame selection mismatch | `backend/app/steganography/video/frame_selector.py` | video_steganography_service.py | POST /api/video/extract |
| Platform signature verification failed | `backend/app/services/platform_verification_service.py` | platform_verification_service.py | POST /api/video/extract |
| DCT extraction failed | `backend/app/steganography/video/dct_extractor.py` | video_steganography_service.py | POST /api/video/extract |

**Debugging Priority**:
1. Check video format (must be MP4)
2. Check frame_selector.py logs
3. Check platform signature verification
4. Check dct_extractor.py logs

---

### Issue: FFmpeg not found

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| FFmpeg not installed | System | video_steganography_service.py | POST /api/video/embed |
| FFmpeg not in PATH | System | video_steganography_service.py | POST /api/video/embed |
| Wrong FFmpeg version | System | video_steganography_service.py | POST /api/video/embed |

**Debugging Priority**:
1. Check FFmpeg installation
2. Check FFmpeg in PATH
3. Check FFmpeg version

---

## Audio Steganography Issues

### Issue: Audio embedding fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Invalid audio format | `backend/app/routes/audio_steganography.py` | audio_steganography_service.py | POST /api/audio/embed |
| FFmpeg not installed | System | audio_steganography_service.py | POST /api/audio/embed |
| Audio conversion failed | `backend/app/audio_processing/audio_converter.py` | audio_steganography_service.py | POST /api/audio/embed |
| Audio loading failed | `backend/app/audio_processing/audio_loader.py` | audio_steganography_service.py | POST /api/audio/embed |
| Sample position generation failed | `backend/app/steganography/audio/sample_selector.py` | audio_steganography_service.py | POST /api/audio/embed |
| LSB embedding failed | `backend/app/channels/audio/audio_lsb_embedder.py` | audio_steganography_service.py | POST /api/audio/embed |
| Audio writing failed | `backend/app/audio_processing/audio_writer.py` | audio_steganography_service.py | POST /api/audio/embed |
| Platform signature error | `backend/app/services/platform_verification_service.py` | platform_verification_service.py | POST /api/audio/embed |

**Debugging Priority**:
1. Check audio format (WAV, MP3, M4A, FLAC)
2. Check FFmpeg installation
3. Check audio_converter.py logs
4. Check audio_loader.py logs
5. Check sample_selector.py logs
6. Check audio_lsb_embedder.py logs
7. Check audio_writer.py logs
8. Check platform_secret_key in .env

---

### Issue: Audio extraction fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Invalid audio format (not WAV) | `backend/app/routes/audio_steganography.py` | audio_steganography_service.py | POST /api/audio/extract |
| No hidden data found | `backend/app/steganography/audio/audio_lsb_extractor.py` | audio_steganography_service.py | POST /api/audio/extract |
| Wrong password | `frontend/src/pages/ExtractMessage.jsx` | audio_steganography_service.py | POST /api/audio/extract |
| Sample position mismatch | `backend/app/steganography/audio/sample_selector.py` | audio_steganography_service.py | POST /api/audio/extract |
| Platform signature verification failed | `backend/app/services/platform_verification_service.py` | platform_verification_service.py | POST /api/audio/extract |
| LSB extraction failed | `backend/app/steganography/audio/audio_lsb_extractor.py` | audio_steganography_service.py | POST /api/audio/extract |

**Debugging Priority**:
1. Check audio format (must be WAV)
2. Verify password matches embedding password
3. Check sample_selector.py logs
4. Check platform signature verification
5. Check audio_lsb_extractor.py logs

---

### Issue: Sample position generation fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Empty password | `frontend/src/pages/HideMessage.jsx` | audio_steganography_service.py | POST /api/audio/embed |
| Password encoding issue | `frontend/src/services/apiService.js` | sample_selector.py | POST /api/audio/embed |
| Random seed generation failed | `backend/app/steganography/audio/sample_selector.py` | sample_selector.py | POST /api/audio/embed |

**Debugging Priority**:
1. Check password is not empty
2. Check password encoding
3. Check sample_selector.py implementation

---

## Document Steganography Issues

### Issue: Document embedding fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Invalid document format | `backend/app/routes/document_steganography.py` | document_steganography_service.py | POST /api/document/embed |
| PDF parsing failed | `backend/app/document_processing/pdf_parser.py` | document_steganography_service.py | POST /api/document/embed |
| Text embedding failed | `backend/app/steganography/invisible_character_embedder.py` | document_steganography_service.py | POST /api/document/embed |
| Structure embedding failed | `backend/app/steganography/structure_embedder.py` | document_steganography_service.py | POST /api/document/embed |
| Image embedding failed | `backend/app/steganography/pdf_image_processor.py` | document_steganography_service.py | POST /api/document/embed |
| PDF rebuilding failed | `backend/app/document_processing/pdf_rebuilder.py` | document_steganography_service.py | POST /api/document/embed |
| Platform signature error | `backend/app/services/platform_verification_service.py` | platform_verification_service.py | POST /api/document/embed |

**Debugging Priority**:
1. Check document format (PDF or TXT)
2. Check pdf_parser.py logs
3. Check invisible_character_embedder.py logs
4. Check structure_embedder.py logs
5. Check pdf_image_processor.py logs
6. Check pdf_rebuilder.py logs
7. Check platform_secret_key in .env

---

### Issue: Document extraction fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Invalid document format | `backend/app/routes/document_steganography.py` | document_steganography_service.py | POST /api/document/extract |
| No hidden data found | `backend/app/steganography/invisible_character_extractor.py` | document_steganography_service.py | POST /api/document/extract |
| Text extraction failed | `backend/app/steganography/invisible_character_extractor.py` | document_steganography_service.py | POST /api/document/extract |
| Structure extraction failed | `backend/app/steganography/structure_extractor.py` | document_steganography_service.py | POST /api/document/extract |
| Image extraction failed | `backend/app/steganography/pdf_image_processor.py` | document_steganography_service.py | POST /api/document/extract |
| Payload combination failed | `backend/app/services/document_steganography_service.py` | document_steganography_service.py | POST /api/document/extract |
| Platform signature verification failed | `backend/app/services/platform_verification_service.py` | platform_verification_service.py | POST /api/document/extract |

**Debugging Priority**:
1. Check document format (PDF or TXT)
2. Check invisible_character_extractor.py logs
3. Check structure_extractor.py logs
4. Check pdf_image_processor.py logs
5. Check payload combination logic
6. Check platform signature verification

---

### Issue: PDF parsing fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| PyMuPDF not installed | `backend/requirements.txt` | document_steganography_service.py | POST /api/document/embed |
| Corrupted PDF file | `backend/app/document_processing/pdf_parser.py` | document_steganography_service.py | POST /api/document/embed |
| Unsupported PDF version | `backend/app/document_processing/pdf_parser.py` | document_steganography_service.py | POST /api/document/embed |

**Debugging Priority**:
1. Check PyMuPDF installation
2. Check PDF file integrity
3. Check PDF version compatibility

---

## Platform Verification Issues

### Issue: Signature generation fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| platform_secret_key not set | `backend/.env` | platform_verification_service.py | All steganography APIs |
| Invalid secret key format | `backend/.env` | platform_signature.py | All steganography APIs |
| Payload too large | `backend/app/services/platform_verification_service.py` | platform_verification_service.py | All steganography APIs |
| HMAC generation failed | `backend/app/verification/platform_signature.py` | platform_signature.py | All steganography APIs |

**Debugging Priority**:
1. Check PLATFORM_SECRET_KEY in .env
2. Verify secret key is 64-character hex string
3. Check payload size
4. Check platform_signature.py logs

---

### Issue: Signature verification fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Signature missing | `backend/app/services/platform_verification_service.py` | platform_verification_service.py | All steganography extraction APIs |
| Invalid signature format | `backend/app/verification/signature_validator.py` | platform_verification_service.py | All steganography extraction APIs |
| Tampered signature | `backend/app/verification/signature_validator.py` | platform_verification_service.py | All steganography extraction APIs |
| Platform mismatch | `backend/app/verification/signature_validator.py` | platform_verification_service.py | All steganography extraction APIs |
| Version mismatch | `backend/app/verification/signature_validator.py` | platform_verification_service.py | All steganography extraction APIs |
| Media type mismatch | `backend/app/verification/signature_validator.py` | platform_verification_service.py | All steganography extraction APIs |
| platform_secret_key mismatch | `backend/.env` | platform_signature.py | All steganography extraction APIs |

**Debugging Priority**:
1. Check signature extraction
2. Check signature format
3. Check HMAC verification
4. Check platform identity
5. Check version compatibility
6. Check media type match
7. Check platform_secret_key matches

---

### Issue: Platform signature error

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| MissingSignatureError | `backend/app/verification/signature_exceptions.py` | platform_verification_service.py | All steganography extraction APIs |
| InvalidSignatureError | `backend/app/verification/signature_exceptions.py` | platform_verification_service.py | All steganography extraction APIs |
| TamperedSignatureError | `backend/app/verification/signature_exceptions.py` | platform_verification_service.py | All steganography extraction APIs |
| VersionMismatchError | `backend/app/verification/signature_exceptions.py` | platform_verification_service.py | All steganography extraction APIs |
| PlatformMismatchError | `backend/app/verification/signature_exceptions.py` | platform_verification_service.py | All steganography extraction APIs |
| MediaTypeMismatchError | `backend/app/verification/signature_exceptions.py` | platform_verification_service.py | All steganography extraction APIs |

**Debugging Priority**:
1. Check specific error type
2. Check signature_exceptions.py for error details
3. Check verification diagnostics
4. Check platform_signature.py constants

---

## Frontend Issues

### Issue: Page not loading

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| React error | `frontend/src/main.jsx` | None | None |
| Router error | `frontend/src/App.jsx` | None | None |
| Component error | `frontend/src/pages/*.jsx` | None | None |
| Import error | `frontend/src/*.jsx` | None | None |

**Debugging Priority**:
1. Check browser console for errors
2. Check React DevTools
3. Check imports in main.jsx and App.jsx
4. Check component syntax

---

### Issue: API call fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Backend not running | System | None | All APIs |
| CORS error | `backend/app/config/settings.py` | None | All APIs |
| Wrong API URL | `frontend/.env` | apiService.js | All APIs |
| Network error | System | apiService.js | All APIs |
| Request format error | `frontend/src/services/apiService.js` | apiService.js | All APIs |

**Debugging Priority**:
1. Check backend is running
2. Check CORS configuration
3. Check VITE_API_URL in .env
4. Check network tab in browser
5. Check request format in apiService.js

---

### Issue: State not updating

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| React state error | `frontend/src/pages/*.jsx` | None | None |
| Hook error | `frontend/src/hooks/*.js` | None | None |
| Service error | `frontend/src/services/*.js` | None | None |

**Debugging Priority**:
1. Check React state management
2. Check custom hooks
3. Check service state management
4. Use React DevTools to inspect state

---

### Issue: File upload fails

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| File too large | `backend/app/config/settings.py` | None | All upload APIs |
| Invalid file format | `frontend/src/components/ui/FileUpload.jsx` | None | All upload APIs |
| File read error | `frontend/src/components/ui/FileUpload.jsx` | None | All upload APIs |

**Debugging Priority**:
1. Check file size limits in settings.py
2. Check file format validation
3. Check FileUpload component

---

## Backend Issues

### Issue: Server not starting

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Port already in use | System | None | None |
| Missing dependencies | `backend/requirements.txt` | None | None |
| Configuration error | `backend/.env` | None | None |
| Import error | `backend/app/main.py` | None | None |

**Debugging Priority**:
1. Check port 8000 availability
2. Install dependencies
3. Check .env configuration
4. Check imports in main.py

---

### Issue: Route not found

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Router not registered | `backend/app/main.py` | None | All APIs |
| Wrong URL path | `frontend/src/services/apiService.js` | None | All APIs |
| Wrong HTTP method | `frontend/src/services/apiService.js` | None | All APIs |

**Debugging Priority**:
1. Check router registration in main.py
2. Check URL path in apiService.js
3. Check HTTP method in apiService.js

---

### Issue: CORS error

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| CORS not configured | `backend/app/config/settings.py` | None | All APIs |
| Wrong CORS origins | `backend/.env` | None | All APIs |
| Preflight request failed | `backend/app/main.py` | None | All APIs |

**Debugging Priority**:
1. Check CORS configuration in settings.py
2. Check cors_origins in .env
3. Check CORS middleware in main.py

---

### Issue: Service error

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Service not initialized | `backend/app/services/*.py` | All services | All APIs |
| Service method error | `backend/app/services/*.py` | All services | All APIs |
| Dependency error | `backend/requirements.txt` | All services | All APIs |

**Debugging Priority**:
1. Check service initialization
2. Check service method implementation
3. Check dependencies

---

## Configuration Issues

### Issue: Environment variable not loaded

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| .env file missing | `backend/.env` | All services | All APIs |
| .env file in wrong location | `backend/.env` | All services | All APIs |
- Variable name typo | `backend/.env` | All services | All APIs |
- python-dotenv not installed | `backend/requirements.txt` | All services | All APIs |

**Debugging Priority**:
1. Check .env file exists
2. Check .env file location
3. Check variable names
4. Install python-dotenv

---

### Issue: Argon2id parameters invalid

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
| Parameters not set | `backend/.env` | crypto_service.py | POST /api/encryption/encrypt |
| Parameter type error | `backend/.env` | crypto_service.py | POST /api/encryption/encrypt |
- Parameter out of range | `backend/.env` | crypto_service.py | POST /api/encryption/encrypt |

**Debugging Priority**:
1. Check Argon2id parameters in .env
2. Check parameter types
3. Check parameter ranges

---

### Issue: Platform secret key invalid

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
- Secret key not set | `backend/.env` | platform_signature.py | All steganography APIs |
- Invalid format (not hex) | `backend/.env` | platform_signature.py | All steganography APIs |
- Wrong length (not 64 chars) | `backend/.env` | platform_signature.py | All steganography APIs |

**Debugging Priority**:
1. Check PLATFORM_SECRET_KEY in .env
2. Verify format is hex
3. Verify length is 64 characters

---

### Issue: File size limits exceeded

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
- Limit too low | `backend/app/config/settings.py` | All services | All upload APIs |
- File too large | User upload | All services | All upload APIs |

**Debugging Priority**:
1. Check file size limits in settings.py
2. Increase limits if needed
3. Inform user of limits

---

## Performance Issues

### Issue: Slow encryption

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
- Argon2id parameters too high | `backend/.env` | crypto_service.py | POST /api/encryption/encrypt |
- Large message size | User input | crypto_service.py | POST /api/encryption/encrypt |
- System resource constraints | System | crypto_service.py | POST /api/encryption/encrypt |

**Debugging Priority**:
1. Check Argon2id parameters
2. Reduce time_cost or memory_cost
3. Check system resources

---

### Issue: Slow steganography

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
- Large image/video/audio | User upload | All steganography services | All steganography APIs |
- Inefficient algorithm | `backend/app/steganography/*.py` | All steganography services | All steganography APIs |
- System resource constraints | System | All steganography services | All steganography APIs |

**Debugging Priority**:
1. Check file size
2. Check algorithm efficiency
3. Check system resources

---

### Issue: Memory leak

| Possible Root Cause | Files to Check | Services | APIs |
|---------------------|---------------|----------|------|
- Temporary files not cleaned | `backend/app/routes/*.py` | All services | All APIs |
- Large file in memory | `backend/app/services/*.py` | All services | All APIs |
- Image/video not released | `backend/app/*_processing/*.py` | All services | All APIs |

**Debugging Priority**:
1. Check temporary file cleanup
2. Check memory usage
3. Check file release

---

## Summary

This bug location guide provides a comprehensive mapping of issue types to possible files, services, and APIs:

1. **Issue Type Classification**: Categories and severity levels
2. **Encryption Issues**: Encryption and decryption failures
3. **Decryption Issues**: Password, salt, IV issues
4. **Image Steganography Issues**: Embedding, extraction, capacity issues
5. **Video Steganography Issues**: Embedding, extraction, FFmpeg issues
6. **Audio Steganography Issues**: Embedding, extraction, sample position issues
7. **Document Steganography Issues**: Embedding, extraction, PDF parsing issues
8. **Platform Verification Issues**: Signature generation and verification failures
9. **Frontend Issues**: Page loading, API calls, state management
10. **Backend Issues**: Server startup, routes, services
11. **Configuration Issues**: Environment variables, parameters
12. **Performance Issues**: Slow operations, memory leaks

This documentation enables developers to:
- Quickly locate the source of any bug
- Identify which files to check for each issue type
- Understand which services and APIs are involved
- Prioritize debugging steps
- Apply targeted solutions
- Troubleshoot efficiently
