# SecureStego Code Ownership Map

## Table of Contents
1. [Ownership Structure](#ownership-structure)
2. [Frontend Ownership](#frontend-ownership)
3. [Backend Ownership](#backend-ownership)
4. [Cross-Functional Ownership](#cross-functional-ownership)
5. [Module Ownership Matrix](#module-ownership-matrix)
6. [Feature Ownership](#feature-ownership)
7. [Testing Ownership](#testing-ownership)
8. [Documentation Ownership](#documentation-ownership)

---

## Ownership Structure

### Ownership Roles

| Role | Responsibilities | Areas |
|------|------------------|-------|
| Frontend Lead | React components, UI/UX, state management | All frontend code |
| Backend Lead | FastAPI routes, services, business logic | All backend code |
| Security Lead | Encryption, steganography algorithms, platform verification | crypto_service, steganography modules, verification modules |
| DevOps Lead | Deployment, configuration, CI/CD | Docker, environment configuration |
| QA Lead | Testing, quality assurance | Tests, test plans |

### Ownership Principles

1. **Single Owner**: Each module has a primary owner
2. **Secondary Review**: Changes require review from at least one other owner
3. **Cross-Functional Coordination**: Changes affecting multiple areas require coordination
4. **Documentation Updates**: Owners must update documentation for their changes

---

## Frontend Ownership

### Frontend Lead

**Primary Owner**: Frontend Lead

**Responsibilities**:
- All React components
- State management
- UI/UX implementation
- Frontend API integration
- Frontend testing

**Owned Modules**:

#### Pages
- `frontend/src/pages/Landing.jsx`
- `frontend/src/pages/HideMessage.jsx`
- `frontend/src/pages/ExtractMessage.jsx`
- `frontend/src/pages/About.jsx`
- `frontend/src/pages/Contact.jsx`

#### Components
- `frontend/src/components/layout/Navbar.jsx`
- `frontend/src/components/layout/Footer.jsx`
- `frontend/src/components/ui/Button.jsx`
- `frontend/src/components/ui/Card.jsx`
- `frontend/src/components/ui/FileUpload.jsx`
- `frontend/src/components/ui/PasswordInput.jsx`
- `frontend/src/components/ui/Textarea.jsx`
- `frontend/src/components/ui/DebugPanel.jsx`

#### Services
- `frontend/src/services/apiService.js`
- `frontend/src/services/encryptionService.js`

#### Hooks
- `frontend/src/hooks/useEncryption.js`
- `frontend/src/hooks/useSteganography.js`

#### Utilities
- `frontend/src/utils/api.js`
- `frontend/src/utils/crypto.js`

#### Configuration
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/tailwind.config.js`
- `frontend/.env`

**Review Required From**:
- Backend Lead (for API changes)
- Security Lead (for encryption changes)

---

## Backend Ownership

### Backend Lead

**Primary Owner**: Backend Lead

**Responsibilities**:
- FastAPI application setup
- API routes
- Service orchestration
- Configuration management
- Backend testing

**Owned Modules**:

#### Application Setup
- `backend/app/main.py`

#### Configuration
- `backend/app/config/settings.py`

#### Routes
- `backend/app/routes/encryption.py`
- `backend/app/routes/steganography.py`
- `backend/app/routes/video_steganography.py`
- `backend/app/routes/audio_steganography.py`
- `backend/app/routes/document_steganography.py`

#### Models
- `backend/app/models/schemas.py`

#### Services (Orchestration)
- `backend/app/services/steganography_service.py`
- `backend/app/services/video_steganography_service.py`
- `backend/app/services/audio_steganography_service.py`
- `backend/app/services/document_steganography_service.py`

#### Utilities
- `backend/app/utils/logging_config.py`
- `backend/app/utils/exceptions.py`
- `backend/app/utils/payload_serializer.py`
- `backend/app/utils/payload_deserializer.py`

#### Configuration
- `backend/requirements.txt`
- `backend/.env`

**Review Required From**:
- Security Lead (for security-related changes)
- Frontend Lead (for API contract changes)

---

## Cross-Functional Ownership

### Security Lead

**Primary Owner**: Security Lead

**Responsibilities**:
- Encryption algorithms
- Steganography algorithms
- Platform signature verification
- Security configuration
- Security testing

**Owned Modules**:

#### Encryption Service
- `backend/app/services/crypto_service.py`

#### Platform Verification Service
- `backend/app/services/platform_verification_service.py`

#### Verification Modules
- `backend/app/verification/platform_signature.py`
- `backend/app/verification/signature_validator.py`
- `backend/app/verification/signature_constants.py`
- `backend/app/verification/signature_exceptions.py`

#### Image Processing
- `backend/app/image_processing/edge_detector.py`
- `backend/app/image_processing/image_converter.py`
- `backend/app/image_processing/image_validator.py`

#### Steganography Algorithms
- `backend/app/steganography/edge_lsb_embedder.py`
- `backend/app/steganography/edge_lsb_extractor.py`

#### Video Processing
- `backend/app/video_processing/frame_extractor.py`
- `backend/app/video_processing/frame_rebuilder.py`
- `backend/app/video_processing/video_converter.py`
- `backend/app/video_processing/audio_handler.py`
- `backend/app/video_processing/video_validator.py`

#### Video Steganography
- `backend/app/steganography/video/dct_embedder.py`
- `backend/app/steganography/video/dct_extractor.py`
- `backend/app/steganography/video/frame_selector.py`
- `backend/app/steganography/video/dct_transform.py`

#### Audio Processing
- `backend/app/audio_processing/audio_converter.py`
- `backend/app/audio_processing/audio_loader.py`
- `backend/app/audio_processing/audio_writer.py`
- `backend/app/audio_processing/audio_validator.py`

#### Audio Steganography
- `backend/app/steganography/audio/audio_lsb_embedder.py`
- `backend/app/steganography/audio/audio_lsb_extractor.py`
- `backend/app/steganography/audio/sample_selector.py`

#### Document Processing
- `backend/app/document_processing/pdf_parser.py`
- `backend/app/document_processing/pdf_rebuilder.py`
- `backend/app/document_processing/txt_handler.py`
- `backend/app/document_processing/document_validator.py`

#### Document Steganography
- `backend/app/steganography/invisible_character_embedder.py`
- `backend/app/steganography/invisible_character_extractor.py`
- `backend/app/steganography/structure_embedder.py`
- `backend/app/steganography/structure_extractor.py`
- `backend/app/steganography/pdf_image_processor.py`

**Review Required From**:
- Backend Lead (for integration changes)
- Frontend Lead (for API contract changes)

---

### DevOps Lead

**Primary Owner**: DevOps Lead

**Responsibilities**:
- Deployment configuration
- Docker setup
- CI/CD pipelines
- Environment management
- Infrastructure

**Owned Modules**:

#### Deployment
- `Dockerfile` (if exists)
- `docker-compose.yml` (if exists)
- `.github/workflows/` (if exists)
- Deployment scripts

#### Environment
- `.env.example`
- Environment variable documentation

**Review Required From**:
- Backend Lead (for deployment configuration)
- Security Lead (for security configuration)

---

### QA Lead

**Primary Owner**: QA Lead

**Responsibilities**:
- Test planning
- Test implementation
- Quality assurance
- Bug tracking
- Test documentation

**Owned Modules**:

#### Tests
- `tests/` directory
- Test plans
- Test documentation

**Review Required From**:
- All leads (for test coverage)

---

## Module Ownership Matrix

| Module | Primary Owner | Secondary Reviewers | Notes |
|--------|---------------|-------------------|-------|
| Frontend Pages | Frontend Lead | Backend Lead | API integration |
| Frontend Components | Frontend Lead | None | UI only |
| Frontend Services | Frontend Lead | Backend Lead | API calls |
| Frontend Hooks | Frontend Lead | None | State management |
| Frontend Utils | Frontend Lead | Security Lead | Crypto utils |
| Backend Main | Backend Lead | Security Lead | App setup |
| Backend Config | Backend Lead | DevOps Lead | Settings |
| Backend Routes | Backend Lead | Frontend Lead | API contracts |
| Backend Models | Backend Lead | Frontend Lead | Schemas |
| Crypto Service | Security Lead | Backend Lead | Critical security |
| Steganography Service | Backend Lead | Security Lead | Orchestration |
| Video Service | Backend Lead | Security Lead | Orchestration |
| Audio Service | Backend Lead | Security Lead | Orchestration |
| Document Service | Backend Lead | Security Lead | Orchestration |
| Platform Verification | Security Lead | Backend Lead | Critical security |
| Image Processing | Security Lead | Backend Lead | Algorithms |
| Video Processing | Security Lead | Backend Lead | Algorithms |
| Audio Processing | Security Lead | Backend Lead | Algorithms |
| Document Processing | Security Lead | Backend Lead | Algorithms |
| Image Steganography | Security Lead | Backend Lead | Algorithms |
| Video Steganography | Security Lead | Backend Lead | Algorithms |
| Audio Steganography | Security Lead | Backend Lead | Algorithms |
| Document Steganography | Security Lead | Backend Lead | Algorithms |
| Backend Utils | Backend Lead | Security Lead | Logging, exceptions |
| Payload Serializer | Backend Lead | Security Lead | Data format |
| Payload Deserializer | Backend Lead | Security Lead | Data format |
| Verification Modules | Security Lead | Backend Lead | Critical security |
| Deployment | DevOps Lead | Backend Lead | Infrastructure |
| Tests | QA Lead | All leads | Quality assurance |

---

## Feature Ownership

### Encryption Feature

**Primary Owner**: Security Lead

**Secondary Owners**:
- Backend Lead (API routes)
- Frontend Lead (UI integration)

**Owned Files**:
- `backend/app/services/crypto_service.py`
- `backend/app/routes/encryption.py`
- `backend/app/models/schemas.py` (encryption schemas)
- `frontend/src/services/encryptionService.js`
- `frontend/src/hooks/useEncryption.js`
- `frontend/src/pages/HideMessage.jsx` (encryption part)
- `frontend/src/pages/ExtractMessage.jsx` (decryption part)

**Review Required For**:
- Algorithm changes
- Parameter changes
- API contract changes

---

### Image Steganography Feature

**Primary Owner**: Security Lead

**Secondary Owners**:
- Backend Lead (service orchestration)
- Frontend Lead (UI integration)

**Owned Files**:
- `backend/app/steganography/edge_lsb_embedder.py`
- `backend/app/steganography/edge_lsb_extractor.py`
- `backend/app/image_processing/edge_detector.py`
- `backend/app/image_processing/image_converter.py`
- `backend/app/image_processing/image_validator.py`
- `backend/app/services/steganography_service.py`
- `backend/app/routes/steganography.py`
- `backend/app/models/schemas.py` (image schemas)
- `frontend/src/hooks/useSteganography.js`
- `frontend/src/pages/HideMessage.jsx` (embedding part)
- `frontend/src/pages/ExtractMessage.jsx` (extraction part)

**Review Required For**:
- Algorithm changes
- Edge detection changes
- API contract changes

---

### Video Steganography Feature

**Primary Owner**: Security Lead

**Secondary Owners**:
- Backend Lead (service orchestration)
- Frontend Lead (UI integration - when implemented)

**Owned Files**:
- `backend/app/steganography/video/dct_embedder.py`
- `backend/app/steganography/video/dct_extractor.py`
- `backend/app/steganography/video/frame_selector.py`
- `backend/app/steganography/video/dct_transform.py`
- `backend/app/video_processing/frame_extractor.py`
- `backend/app/video_processing/frame_rebuilder.py`
- `backend/app/video_processing/video_converter.py`
- `backend/app/video_processing/audio_handler.py`
- `backend/app/video_processing/video_validator.py`
- `backend/app/services/video_steganography_service.py`
- `backend/app/routes/video_steganography.py`
- `backend/app/models/schemas.py` (video schemas)

**Review Required For**:
- Algorithm changes
- Frame selection changes
- API contract changes

---

### Audio Steganography Feature

**Primary Owner**: Security Lead

**Secondary Owners**:
- Backend Lead (service orchestration)
- Frontend Lead (UI integration - when implemented)

**Owned Files**:
- `backend/app/steganography/audio/audio_lsb_embedder.py`
- `backend/app/steganography/audio/audio_lsb_extractor.py`
- `backend/app/steganography/audio/sample_selector.py`
- `backend/app/audio_processing/audio_converter.py`
- `backend/app/audio_processing/audio_loader.py`
- `backend/app/audio_processing/audio_writer.py`
- `backend/app/audio_processing/audio_validator.py`
- `backend/app/services/audio_steganography_service.py`
- `backend/app/routes/audio_steganography.py`
- `backend/app/models/schemas.py` (audio schemas)

**Review Required For**:
- Algorithm changes
- Sample selection changes
- API contract changes

---

### Document Steganography Feature

**Primary Owner**: Security Lead

**Secondary Owners**:
- Backend Lead (service orchestration)
- Frontend Lead (UI integration - when implemented)

**Owned Files**:
- `backend/app/steganography/invisible_character_embedder.py`
- `backend/app/steganography/invisible_character_extractor.py`
- `backend/app/steganography/structure_embedder.py`
- `backend/app/steganography/structure_extractor.py`
- `backend/app/steganography/pdf_image_processor.py`
- `backend/app/document_processing/pdf_parser.py`
- `backend/app/document_processing/pdf_rebuilder.py`
- `backend/app/document_processing/txt_handler.py`
- `backend/app/document_processing/document_validator.py`
- `backend/app/services/document_steganography_service.py`
- `backend/app/routes/document_steganography.py`
- `backend/app/models/schemas.py` (document schemas)

**Review Required For**:
- Algorithm changes
- PDF processing changes
- API contract changes

---

### Platform Verification Feature

**Primary Owner**: Security Lead

**Secondary Owners**:
- Backend Lead (service integration)

**Owned Files**:
- `backend/app/services/platform_verification_service.py`
- `backend/app/verification/platform_signature.py`
- `backend/app/verification/signature_validator.py`
- `backend/app/verification/signature_constants.py`
- `backend/app/verification/signature_exceptions.py`
- `backend/app/config/settings.py` (platform_secret_key)

**Review Required For**:
- Algorithm changes
- Signature format changes
- Secret key changes

---

## Testing Ownership

### Frontend Testing

**Primary Owner**: QA Lead

**Secondary Owners**:
- Frontend Lead (test implementation)

**Owned Files**:
- `frontend/tests/` (if exists)
- Frontend test plans

**Review Required For**:
- Test coverage
- Test quality

---

### Backend Testing

**Primary Owner**: QA Lead

**Secondary Owners**:
- Backend Lead (test implementation)
- Security Lead (security tests)

**Owned Files**:
- `backend/tests/` (if exists)
- Backend test plans

**Review Required For**:
- Test coverage
- Test quality
- Security test coverage

---

### Integration Testing

**Primary Owner**: QA Lead

**Secondary Owners**:
- All leads

**Owned Files**:
- `tests/` (end-to-end tests)
- Integration test plans

**Review Required For**:
- Test coverage
- Test quality
- Workflow coverage

---

## Documentation Ownership

### API Documentation

**Primary Owner**: Backend Lead

**Secondary Owners**:
- Frontend Lead (frontend integration docs)
- Security Lead (security docs)

**Owned Files**:
- `API_MAP.md`
- FastAPI auto-generated docs (/api/docs)

**Review Required For**:
- API contract changes
- New endpoints
- Endpoint changes

---

### Architecture Documentation

**Primary Owner**: Backend Lead

**Secondary Owners**:
- Security Lead (security architecture)
- Frontend Lead (frontend architecture)

**Owned Files**:
- `PROJECT_BLUEPRINT.md`
- Architecture diagrams

**Review Required For**:
- Architecture changes
- New modules
- Module changes

---

### Workflow Documentation

**Primary Owner**: Backend Lead

**Secondary Owners**:
- Frontend Lead (frontend workflows)
- Security Lead (security workflows)

**Owned Files**:
- `WORKFLOWS.md`

**Review Required For**:
- Workflow changes
- New features
- Feature changes

---

### Debugging Documentation

**Primary Owner**: Backend Lead

**Secondary Owners**:
- Frontend Lead (frontend debugging)
- QA Lead (testing debugging)

**Owned Files**:
- `DEBUGGING_GUIDE.md`

**Review Required For**:
- New debugging procedures
- Bug fixes
- New issues

---

### Bug Location Documentation

**Primary Owner**: Backend Lead

**Secondary Owners**:
- Frontend Lead (frontend bugs)
- QA Lead (bug tracking)

**Owned Files**:
- `BUG_LOCATION_GUIDE.md`

**Review Required For**:
- New bug types
- Bug fixes
- New modules

---

### Dependency Documentation

**Primary Owner**: DevOps Lead

**Secondary Owners**:
- Backend Lead (backend dependencies)
- Frontend Lead (frontend dependencies)

**Owned Files**:
- `DEPENDENCY_MAP.md`

**Review Required For**:
- Dependency updates
- New dependencies
- Dependency removal

---

### Frontend-Backend Map Documentation

**Primary Owner**: Backend Lead

**Secondary Owners**:
- Frontend Lead (frontend integration)

**Owned Files**:
- `FRONTEND_BACKEND_MAP.md`

**Review Required For**:
- New API endpoints
- API changes
- New frontend components

---

### Code Ownership Documentation

**Primary Owner**: DevOps Lead

**Secondary Owners**:
- All leads (ownership updates)

**Owned Files**:
- `CODE_OWNERSHIP_MAP.md`

**Review Required For**:
- Ownership changes
- New modules
- Team changes

---

## Change Request Process

### Step 1: Identify Ownership

1. Identify the module(s) being changed
2. Identify the primary owner
3. Identify secondary reviewers

### Step 2: Request Review

1. Create pull request with clear description
2. Tag primary owner for review
3. Tag secondary reviewers for review

### Step 3: Review Process

1. Primary owner reviews for correctness
2. Secondary reviewers review for impact
3. All reviewers approve

### Step 4: Documentation Update

1. Update relevant documentation
2. Tag documentation owner for review
3. Documentation owner approves

### Step 5: Merge

1. Merge after all approvals
2. Close related issues
3. Update changelog

---

## Emergency Changes

### Definition

Emergency changes are those that:
- Fix critical security vulnerabilities
- Fix production outages
- Fix data loss bugs

### Process

1. **Immediate Action**: Primary owner can make immediate changes
2. **Notification**: Notify all leads of the change
3. **Follow-up Review**: Schedule review within 24 hours
4. **Documentation Update**: Update documentation immediately after

---

## Summary

This code ownership map provides comprehensive ownership information for the SecureStego project:

1. **Ownership Structure**: Roles and responsibilities
2. **Frontend Ownership**: All frontend modules and their owners
3. **Backend Ownership**: All backend modules and their owners
4. **Cross-Functional Ownership**: Security, DevOps, QA ownership
5. **Module Ownership Matrix**: Complete mapping of modules to owners
6. **Feature Ownership**: Ownership by feature
7. **Testing Ownership**: Test ownership and responsibilities
8. **Documentation Ownership**: Documentation ownership and responsibilities

This documentation enables developers to:
- Know who to contact for each module
- Understand review requirements
- Follow proper change request processes
- Coordinate cross-functional changes
- Maintain code quality and security
- Ensure proper documentation updates
