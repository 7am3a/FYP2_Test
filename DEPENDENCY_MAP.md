# SecureStego Dependency Map

## Table of Contents
1. [Frontend Dependencies](#frontend-dependencies)
2. [Backend Dependencies](#backend-dependencies)
3. [Service Dependencies](#service-dependencies)
4. [Module Dependencies](#module-dependencies)
5. [Circular Dependencies](#circular-dependencies)
6. [Unused Dependencies](#unused-dependencies)
7. [External Dependencies](#external-dependencies)

---

## Frontend Dependencies

### package.json Dependencies

**Runtime Dependencies**:
- react: ^18.2.0 - React library
- react-dom: ^18.2.0 - React DOM renderer
- react-router-dom: ^6.20.0 - React Router for routing
- framer-motion: ^10.16.4 - Animation library
- lucide-react: ^0.294.0 - Icon library

**Dev Dependencies**:
- vite: ^5.0.0 - Build tool and dev server
- tailwindcss: ^3.3.6 - CSS framework
- autoprefixer: ^10.4.16 - CSS autoprefixer
- postcss: ^8.4.32 - CSS processor
- @vitejs/plugin-react: ^4.2.1 - Vite React plugin

---

### Frontend Module Dependencies

#### App.jsx
**Dependencies**:
- React (implicit)
- React Router
- All page components (Landing, HideMessage, ExtractMessage, About, Contact)
- Layout components (Navbar, Footer)

**Dependents**:
- main.jsx (entry point)

---

#### pages/HideMessage.jsx
**Dependencies**:
- React (implicit)
- Framer Motion
- UI components (Button, Card, FileUpload, PasswordInput, Textarea, DebugPanel)
- Services (apiService, encryptionService)
- Lucide React icons

**Dependents**:
- App.jsx (routing)

---

#### pages/ExtractMessage.jsx
**Dependencies**:
- React (implicit)
- Framer Motion
- UI components (Button, Card, FileUpload, PasswordInput, DebugPanel)
- Services (apiService, encryptionService)
- Lucide React icons

**Dependents**:
- App.jsx (routing)

---

#### services/apiService.js
**Dependencies**:
- None (uses fetch API)

**Dependents**:
- pages/HideMessage.jsx
- pages/ExtractMessage.jsx
- hooks/useEncryption.js
- hooks/useSteganography.js

---

#### services/encryptionService.js
**Dependencies**:
- None

**Dependents**:
- pages/HideMessage.jsx
- pages/ExtractMessage.jsx

---

#### hooks/useEncryption.js
**Dependencies**:
- React (implicit)
- services/apiService.js

**Dependents**:
- pages/HideMessage.jsx
- pages/ExtractMessage.jsx

---

#### hooks/useSteganography.js
**Dependencies**:
- React (implicit)
- services/apiService.js

**Dependents**:
- pages/HideMessage.jsx
- pages/ExtractMessage.jsx

---

#### utils/api.js
**Dependencies**:
- None

**Dependents**:
- (Currently minimal - legacy code)

---

#### utils/crypto.js
**Dependencies**:
- Web Crypto API (browser native)

**Dependents**:
- (Currently minimal - encryption moved to backend)

---

#### components/ui/*
**Dependencies**:
- React (implicit)
- Lucide React (some components)

**Dependents**:
- All pages

---

## Backend Dependencies

### requirements.txt Dependencies

**Core Framework**:
- fastapi: ^0.104.0 - Web framework
- uvicorn: ^0.24.0 - ASGI server
- pydantic: ^2.5.0 - Data validation
- pydantic-settings: ^2.1.0 - Settings management
- python-multipart: ^0.0.6 - File upload handling

**Security**:
- cryptography: ^41.0.0 - Encryption library
- argon2-cffi: ^23.1.0 - Password hashing

**Image Processing**:
- Pillow: ^10.1.0 - Image processing
- opencv-python: ^4.8.1 - Computer vision
- numpy: ^1.26.0 - Numerical computing

**Video Processing**:
- (Uses FFmpeg externally)

**Audio Processing**:
- (Uses FFmpeg externally)

**Document Processing**:
- PyMuPDF: ^1.23.8 - PDF processing

**Utilities**:
- python-dotenv: ^1.0.0 - Environment variables

---

### Backend Module Dependencies

#### main.py
**Dependencies**:
- FastAPI
- CORSMiddleware
- contextlib
- config/settings.py
- routes/* (all routers)
- utils/logging_config.py

**Dependents**:
- None (entry point)

---

#### config/settings.py
**Dependencies**:
- Pydantic Settings
- typing
- Pydantic field_validator

**Dependents**:
- main.py
- All services
- All verification modules

---

#### models/schemas.py
**Dependencies**:
- Pydantic BaseModel
- typing

**Dependents**:
- All routes
- All services

---

#### routes/encryption.py
**Dependencies**:
- FastAPI
- models/schemas.py
- services/crypto_service.py
- utils/logging_config.py

**Dependents**:
- main.py

---

#### routes/steganography.py
**Dependencies**:
- FastAPI
- models/schemas.py
- services/steganography_service.py
- utils/logging_config.py

**Dependents**:
- main.py

---

#### routes/video_steganography.py
**Dependencies**:
- FastAPI
- models/schemas.py
- services/video_steganography_service.py
- utils/logging_config.py

**Dependents**:
- main.py

---

#### routes/audio_steganography.py
**Dependencies**:
- FastAPI
- models/schemas.py
- services/audio_steganography_service.py
- utils/logging_config.py

**Dependents**:
- main.py

---

#### routes/document_steganography.py
**Dependencies**:
- FastAPI
- models/schemas.py
- services/document_steganography_service.py
- utils/logging_config.py

**Dependents**:
- main.py

---

#### services/crypto_service.py
**Dependencies**:
- argon2-cffi
- cryptography
- config/settings.py
- utils/logging_config.py

**Dependents**:
- routes/encryption.py

---

#### services/steganography_service.py
**Dependencies**:
- image_processing/* (image_converter, edge_detector, image_validator)
- steganography/* (edge_lsb_embedder, edge_lsb_extractor)
- utils/* (payload_serializer, payload_deserializer)
- services/platform_verification_service.py
- utils/logging_config.py

**Dependents**:
- routes/steganography.py

---

#### services/video_steganography_service.py
**Dependencies**:
- video_processing/* (frame_extractor, frame_rebuilder, video_converter, video_validator, audio_handler)
- steganography/video/* (dct_embedder, dct_extractor, frame_selector)
- utils/* (payload_serializer, payload_deserializer)
- services/platform_verification_service.py
- utils/logging_config.py

**Dependents**:
- routes/video_steganography.py

---

#### services/audio_steganography_service.py
**Dependencies**:
- audio_processing/* (audio_converter, audio_loader, audio_writer, audio_validator)
- steganography/audio/* (audio_lsb_embedder, audio_lsb_extractor, sample_selector)
- utils/* (payload_serializer, payload_deserializer)
- services/platform_verification_service.py
- utils/logging_config.py

**Dependents**:
- routes/audio_steganography.py

---

#### services/document_steganography_service.py
**Dependencies**:
- document_processing/* (pdf_parser, pdf_rebuilder, txt_handler, document_validator)
- steganography/* (invisible_character_embedder, invisible_character_extractor, structure_embedder, structure_extractor, pdf_image_processor)
- utils/* (payload_serializer, payload_deserializer)
- services/platform_verification_service.py
- utils/logging_config.py

**Dependents**:
- routes/document_steganography.py

---

#### services/platform_verification_service.py
**Dependencies**:
- verification/* (platform_signature, signature_validator, signature_constants, signature_exceptions)
- utils/logging_config.py

**Dependents**:
- services/steganography_service.py
- services/video_steganography_service.py
- services/audio_steganography_service.py
- services/document_steganography_service.py

---

#### image_processing/edge_detector.py
**Dependencies**:
- OpenCV (cv2)
- NumPy

**Dependents**:
- services/steganography_service.py
- steganography/edge_lsb_embedder.py
- steganography/edge_lsb_extractor.py

---

#### image_processing/image_converter.py
**Dependencies**:
- Pillow (PIL)

**Dependents**:
- services/steganography_service.py

---

#### image_processing/image_validator.py
**Dependencies**:
- Pillow (PIL)

**Dependents**:
- services/steganography_service.py

---

#### steganography/edge_lsb_embedder.py
**Dependencies**:
- OpenCV (cv2)
- NumPy
- struct

**Dependents**:
- services/steganography_service.py

---

#### steganography/edge_lsb_extractor.py
**Dependencies**:
- OpenCV (cv2)
- NumPy
- struct

**Dependents**:
- services/steganography_service.py

---

#### verification/platform_signature.py
**Dependencies**:
- hmac
- hashlib
- json
- base64
- datetime
- config/settings.py

**Dependents**:
- services/platform_verification_service.py

---

#### verification/signature_validator.py
**Dependencies**:
- hmac
- hashlib
- json
- verification/signature_constants.py
- verification/signature_exceptions.py

**Dependents**:
- services/platform_verification_service.py

---

#### utils/payload_serializer.py
**Dependencies**:
- json
- datetime

**Dependents**:
- services/steganography_service.py
- services/video_steganography_service.py
- services/audio_steganography_service.py
- services/document_steganography_service.py

---

#### utils/payload_deserializer.py
**Dependencies**:
- json

**Dependents**:
- services/steganography_service.py
- services/video_steganography_service.py
- services/audio_steganography_service.py
- services/document_steganography_service.py

---

#### utils/logging_config.py
**Dependencies**:
- logging

**Dependents**:
- All backend modules

---

#### utils/exceptions.py
**Dependencies**:
- None

**Dependents**:
- All backend modules

---

## Service Dependencies

### crypto_service.py
**Direct Dependencies**:
- argon2-cffi (argon2, PasswordHasher, Type)
- cryptography (AESGCM, default_backend)
- config/settings.py
- utils/logging_config.py

**Indirect Dependencies**:
- None

**Dependency Graph**:
```
crypto_service.py
  ├─ argon2-cffi
  ├─ cryptography
  ├─ settings.py
  └─ logging_config.py
```

---

### steganography_service.py
**Direct Dependencies**:
- image_processing/image_converter.py
- image_processing/edge_detector.py
- image_processing/image_validator.py
- steganography/edge_lsb_embedder.py
- steganography/edge_lsb_extractor.py
- utils/payload_serializer.py
- utils/payload_deserializer.py
- services/platform_verification_service.py
- utils/logging_config.py

**Indirect Dependencies**:
- OpenCV (via edge_detector, edge_lsb_embedder, edge_lsb_extractor)
- Pillow (via image_converter, image_validator)
- NumPy (via edge_detector, edge_lsb_embedder, edge_lsb_extractor)
- verification modules (via platform_verification_service)

**Dependency Graph**:
```
steganography_service.py
  ├─ image_converter.py
  │   └─ Pillow
  ├─ edge_detector.py
  │   └─ OpenCV, NumPy
  ├─ image_validator.py
  │   └─ Pillow
  ├─ edge_lsb_embedder.py
  │   └─ OpenCV, NumPy
  ├─ edge_lsb_extractor.py
  │   └─ OpenCV, NumPy
  ├─ payload_serializer.py
  ├─ payload_deserializer.py
  ├─ platform_verification_service.py
  │   └─ verification/*
  └─ logging_config.py
```

---

### video_steganography_service.py
**Direct Dependencies**:
- video_processing/frame_extractor.py
- video_processing/frame_rebuilder.py
- video_processing/video_converter.py
- video_processing/video_validator.py
- video_processing/audio_handler.py
- steganography/video/dct_embedder.py
- steganography/video/dct_extractor.py
- steganography/video/frame_selector.py
- utils/payload_serializer.py
- utils/payload_deserializer.py
- services/platform_verification_service.py
- utils/logging_config.py

**Indirect Dependencies**:
- OpenCV (via video processing modules)
- NumPy (via video processing modules)
- FFmpeg (external, via video processing)
- verification modules (via platform_verification_service)

**Dependency Graph**:
```
video_steganography_service.py
  ├─ frame_extractor.py
  │   └─ OpenCV, FFmpeg
  ├─ frame_rebuilder.py
  │   └─ OpenCV, FFmpeg
  ├─ video_converter.py
  │   └─ FFmpeg
  ├─ video_validator.py
  ├─ audio_handler.py
  │   └─ FFmpeg
  ├─ dct_embedder.py
  │   └─ NumPy
  ├─ dct_extractor.py
  │   └─ NumPy
  ├─ frame_selector.py
  ├─ payload_serializer.py
  ├─ payload_deserializer.py
  ├─ platform_verification_service.py
  │   └─ verification/*
  └─ logging_config.py
```

---

### audio_steganography_service.py
**Direct Dependencies**:
- audio_processing/audio_converter.py
- audio_processing/audio_loader.py
- audio_processing/audio_writer.py
- audio_processing/audio_validator.py
- steganography/audio/audio_lsb_embedder.py
- steganography/audio/audio_lsb_extractor.py
- steganography/audio/sample_selector.py
- utils/payload_serializer.py
- utils/payload_deserializer.py
- services/platform_verification_service.py
- utils/logging_config.py

**Indirect Dependencies**:
- NumPy (via audio processing modules)
- FFmpeg (external, via audio processing)
- verification modules (via platform_verification_service)

**Dependency Graph**:
```
audio_steganography_service.py
  ├─ audio_converter.py
  │   └─ FFmpeg
  ├─ audio_loader.py
  │   └─ NumPy
  ├─ audio_writer.py
  │   └─ NumPy
  ├─ audio_validator.py
  ├─ audio_lsb_embedder.py
  │   └─ NumPy
  ├─ audio_lsb_extractor.py
  │   └─ NumPy
  ├─ sample_selector.py
  ├─ payload_serializer.py
  ├─ payload_deserializer.py
  ├─ platform_verification_service.py
  │   └─ verification/*
  └─ logging_config.py
```

---

### document_steganography_service.py
**Direct Dependencies**:
- document_processing/pdf_parser.py
- document_processing/pdf_rebuilder.py
- document_processing/txt_handler.py
- document_processing/document_validator.py
- steganography/invisible_character_embedder.py
- steganography/invisible_character_extractor.py
- steganography/structure_embedder.py
- steganography/structure_extractor.py
- steganography/pdf_image_processor.py
- utils/payload_serializer.py
- utils/payload_deserializer.py
- services/platform_verification_service.py
- utils/logging_config.py

**Indirect Dependencies**:
- PyMuPDF (via pdf_parser, pdf_rebuilder)
- verification modules (via platform_verification_service)

**Dependency Graph**:
```
document_steganography_service.py
  ├─ pdf_parser.py
  │   └─ PyMuPDF
  ├─ pdf_rebuilder.py
  │   └─ PyMuPDF
  ├─ txt_handler.py
  ├─ document_validator.py
  ├─ invisible_character_embedder.py
  ├─ invisible_character_extractor.py
  ├─ structure_embedder.py
  ├─ structure_extractor.py
  ├─ pdf_image_processor.py
  │   └─ OpenCV, Pillow
  ├─ payload_serializer.py
  ├─ payload_deserializer.py
  ├─ platform_verification_service.py
  │   └─ verification/*
  └─ logging_config.py
```

---

### platform_verification_service.py
**Direct Dependencies**:
- verification/platform_signature.py
- verification/signature_validator.py
- verification/signature_constants.py
- verification/signature_exceptions.py
- utils/logging_config.py

**Indirect Dependencies**:
- config/settings.py (via platform_signature.py)
- hmac, hashlib (via verification modules)

**Dependency Graph**:
```
platform_verification_service.py
  ├─ platform_signature.py
  │   ├─ settings.py
  │   ├─ hmac
  │   └─ hashlib
  ├─ signature_validator.py
  │   ├─ signature_constants.py
  │   ├─ signature_exceptions.py
  │   ├─ hmac
  │   └─ hashlib
  ├─ signature_constants.py
  ├─ signature_exceptions.py
  └─ logging_config.py
```

---

## Module Dependencies

### Image Processing Modules

#### edge_detector.py
**Dependencies**:
- OpenCV (cv2)
- NumPy

**Dependents**:
- steganography_service.py
- edge_lsb_embedder.py
- edge_lsb_extractor.py

---

#### image_converter.py
**Dependencies**:
- Pillow (PIL)

**Dependents**:
- steganography_service.py

---

#### image_validator.py
**Dependencies**:
- Pillow (PIL)

**Dependents**:
- steganography_service.py

---

### Video Processing Modules

#### frame_extractor.py
**Dependencies**:
- OpenCV (cv2)
- FFmpeg (external)

**Dependents**:
- video_steganography_service.py

---

#### frame_rebuilder.py
**Dependencies**:
- OpenCV (cv2)
- FFmpeg (external)

**Dependents**:
- video_steganography_service.py

---

#### video_converter.py
**Dependencies**:
- FFmpeg (external)

**Dependents**:
- video_steganography_service.py

---

#### audio_handler.py
**Dependencies**:
- FFmpeg (external)

**Dependents**:
- video_steganography_service.py

---

#### video_validator.py
**Dependencies**:
- OpenCV (cv2)

**Dependents**:
- video_steganography_service.py

---

### Audio Processing Modules

#### audio_converter.py
**Dependencies**:
- FFmpeg (external)

**Dependents**:
- audio_steganography_service.py

---

#### audio_loader.py
**Dependencies**:
- NumPy

**Dependents**:
- audio_steganography_service.py

---

#### audio_writer.py
**Dependencies**:
- NumPy

**Dependents**:
- audio_steganography_service.py

---

#### audio_validator.py
**Dependencies**:
- NumPy

**Dependents**:
- audio_steganography_service.py

---

### Document Processing Modules

#### pdf_parser.py
**Dependencies**:
- PyMuPDF (fitz)

**Dependents**:
- document_steganography_service.py

---

#### pdf_rebuilder.py
**Dependencies**:
- PyMuPDF (fitz)

**Dependents**:
- document_steganography_service.py

---

#### txt_handler.py
**Dependencies**:
- None

**Dependents**:
- document_steganography_service.py

---

#### document_validator.py
**Dependencies**:
- PyMuPDF (fitz)

**Dependents**:
- document_steganography_service.py

---

### Steganography Modules

#### edge_lsb_embedder.py
**Dependencies**:
- OpenCV (cv2)
- NumPy
- struct

**Dependents**:
- steganography_service.py

---

#### edge_lsb_extractor.py
**Dependencies**:
- OpenCV (cv2)
- NumPy
- struct

**Dependents**:
- steganography_service.py

---

#### invisible_character_embedder.py
**Dependencies**:
- None

**Dependents**:
- document_steganography_service.py

---

#### invisible_character_extractor.py
**Dependencies**:
- None

**Dependents**:
- document_steganography_service.py

---

#### structure_embedder.py
**Dependencies**:
- None

**Dependents**:
- document_steganography_service.py

---

#### structure_extractor.py
**Dependencies**:
- None

**Dependents**:
- document_steganography_service.py

---

#### pdf_image_processor.py
**Dependencies**:
- OpenCV (cv2)
- Pillow (PIL)

**Dependents**:
- document_steganography_service.py

---

### Video Steganography Modules

#### dct_embedder.py
**Dependencies**:
- NumPy

**Dependents**:
- video_steganography_service.py

---

#### dct_extractor.py
**Dependencies**:
- NumPy

**Dependents**:
- video_steganography_service.py

---

#### frame_selector.py
**Dependencies**:
- None

**Dependents**:
- video_steganography_service.py

---

#### dct_transform.py
**Dependencies**:
- NumPy

**Dependents**:
- dct_embedder.py
- dct_extractor.py

---

### Audio Steganography Modules

#### audio_lsb_embedder.py
**Dependencies**:
- NumPy

**Dependents**:
- audio_steganography_service.py

---

#### audio_lsb_extractor.py
**Dependencies**:
- NumPy

**Dependents**:
- audio_steganography_service.py

---

#### sample_selector.py
**Dependencies**:
- None

**Dependents**:
- audio_steganography_service.py

---

### Verification Modules

#### platform_signature.py
**Dependencies**:
- hmac
- hashlib
- json
- base64
- datetime
- config/settings.py

**Dependents**:
- platform_verification_service.py

---

#### signature_validator.py
**Dependencies**:
- hmac
- hashlib
- json
- signature_constants.py
- signature_exceptions.py

**Dependents**:
- platform_verification_service.py

---

#### signature_constants.py
**Dependencies**:
- None

**Dependents**:
- platform_signature.py
- signature_validator.py
- platform_verification_service.py

---

#### signature_exceptions.py
**Dependencies**:
- None

**Dependents**:
- platform_verification_service.py
- signature_validator.py

---

### Utility Modules

#### payload_serializer.py
**Dependencies**:
- json
- datetime

**Dependents**:
- steganography_service.py
- video_steganography_service.py
- audio_steganography_service.py
- document_steganography_service.py

---

#### payload_deserializer.py
**Dependencies**:
- json

**Dependents**:
- steganography_service.py
- video_steganography_service.py
- audio_steganography_service.py
- document_steganography_service.py

---

#### logging_config.py
**Dependencies**:
- logging

**Dependents**:
- All backend modules

---

#### exceptions.py
**Dependencies**:
- None

**Dependents**:
- All backend modules

---

## Circular Dependencies

### Analysis

**No circular dependencies detected.**

The project follows a clean layered architecture:
- Routes → Services → Processing/Algorithm Modules → Utilities
- No module imports from a higher layer to a lower layer
- No mutual imports between modules

**Dependency Hierarchy**:
```
Level 1: Utilities (logging_config, exceptions, payload_serializer, payload_deserializer)
Level 2: Verification Modules (platform_signature, signature_validator, etc.)
Level 3: Processing Modules (image_processing, video_processing, audio_processing, document_processing)
Level 4: Steganography Modules (edge_lsb_embedder, dct_embedder, etc.)
Level 5: Services (crypto_service, steganography_service, etc.)
Level 6: Routes (encryption.py, steganography.py, etc.)
Level 7: Main (main.py)
```

---

## Unused Dependencies

### Frontend

**Potentially Unused**:
- `frontend/src/utils/api.js` - Legacy code, not actively used
- `frontend/src/utils/crypto.js` - Client-side encryption, not actively used (encryption moved to backend)

**Recommendation**:
- Consider removing or documenting these as legacy code
- If client-side encryption is needed in the future, document the use case

---

### Backend

**No unused dependencies detected.**

All dependencies in requirements.txt are actively used:
- fastapi, uvicorn, pydantic - Core framework
- cryptography, argon2-cffi - Encryption
- Pillow, opencv-python, numpy - Image processing
- PyMuPDF - Document processing
- python-multipart - File uploads
- python-dotenv - Configuration

---

## External Dependencies

### FFmpeg

**Purpose**: Video and audio processing

**Used By**:
- video_processing/frame_extractor.py
- video_processing/frame_rebuilder.py
- video_processing/video_converter.py
- video_processing/audio_handler.py
- audio_processing/audio_converter.py

**Installation**:
- Must be installed separately on the system
- Not included in requirements.txt

**Version Requirements**:
- Any recent version with standard codecs

**Notes**:
- Critical for video and audio functionality
- Must be available in system PATH

---

### System Requirements

**Python Version**: 3.8+

**Node.js Version**: 16+ (for Vite)

**Operating System**: Windows, Linux, macOS (cross-platform)

**Browser**: Modern browser with Web Crypto API support

---

## Summary

This dependency map provides comprehensive documentation of all dependencies in the SecureStego project:

1. **Frontend Dependencies**: All npm packages and module dependencies
2. **Backend Dependencies**: All Python packages and module dependencies
3. **Service Dependencies**: Dependency graphs for each service
4. **Module Dependencies**: Dependencies for each processing and steganography module
5. **Circular Dependencies**: Analysis of circular dependencies (none detected)
6. **Unused Dependencies**: Identification of potentially unused code
7. **External Dependencies**: External tools like FFmpeg

This documentation enables developers to:
- Understand the complete dependency tree
- Identify where dependencies are used
- Understand the dependency hierarchy
- Detect potential circular dependencies
- Identify unused dependencies for cleanup
- Understand external tool requirements
- Plan dependency updates
- Troubleshoot dependency issues
