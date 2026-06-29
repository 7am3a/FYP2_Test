# SecureStego - Secure Steganography Platform

A production-ready full-stack web application for securely hiding encrypted messages inside images, videos, audio, and documents using advanced steganographic techniques and Argon2id encryption.

## Project Overview

SecureStego is a Final Year Project that implements:
- **Advanced Steganography**: Edge-based LSB (images), DCT-based block (videos), randomized LSB (audio), hybrid text/image (documents)
- **Strong Encryption**: Argon2id key derivation with AES-256-GCM authenticated encryption (OWASP-recommended)
- **Platform Signature Verification**: HMAC-SHA256 based signature system for authenticity
- **Modern React frontend** with cybersecurity-inspired design
- **FastAPI backend** with production-ready architecture
- **Multi-Media Support**: PNG, JPG/JPEG, HEIC, MP4, AVI, MOV, WAV, MP3, M4A, FLAC, PDF, TXT

## Architecture

### Encryption Flow

```
User Message
    ↓
[Encryption] Argon2id Key Derivation + AES-256-GCM
    ↓
Encrypted Message (Base64)
    ↓
[Serialization] Structured Payload with Metadata
    ↓
[Platform Signature] HMAC-SHA256 Signature Injection
    ↓
[Steganography] Embed into Media (Image/Video/Audio/Document)
    ↓
Stego File Download
```

### Decryption Flow

```
Stego File Upload
    ↓
[Steganography] Extract from Media
    ↓
[Platform Signature] Verify HMAC-SHA256 Signature
    ↓
[Deserialization] Extract Encrypted Message
    ↓
[Decryption] Argon2id Key Derivation + AES-256-GCM
    ↓
Original Message
```

## Project Structure

```
project-root/
├── frontend/                    # Frontend (React + Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/          # Navbar, Footer
│   │   │   └── ui/              # Reusable UI components
│   │   ├── pages/               # Page components
│   │   ├── services/             # API services
│   │   ├── utils/               # Utilities
│   │   ├── hooks/               # Custom React hooks
│   │   ├── context/             # React context providers
│   │   ├── types/               # Type definitions
│   │   ├── constants/           # Application constants
│   │   ├── assets/              # Static assets
│   │   ├── App.jsx              # Main app with routing
│   │   └── main.jsx             # React entry point
│   ├── public/                  # Public assets
│   ├── package.json             # Node.js dependencies
│   ├── vite.config.js           # Vite configuration
│   ├── tailwind.config.js       # Tailwind configuration
│   └── .env.example             # Environment template
├── backend/                     # Backend (FastAPI)
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config/              # Configuration
│   │   ├── models/              # Pydantic models/schemas
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── repositories/        # Data access layer
│   │   ├── middleware/          # Custom middleware
│   │   ├── validators/          # Input validation
│   │   ├── core/                # Core application logic
│   │   ├── utils/               # Utilities (logging, exceptions)
│   │   ├── verification/        # Platform signature verification
│   │   ├── audio_processing/    # Audio processing modules
│   │   ├── video_processing/    # Video processing modules
│   │   ├── document_processing/# Document processing modules
│   │   ├── image_processing/    # Image processing modules
│   │   ├── steganography/       # Steganography algorithms
│   │   └── __init__.py
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment template
├── docs/                        # Documentation
├── scripts/                     # Utility scripts
├── tests/                       # End-to-end tests
├── deployment/                  # Deployment configurations
└── README.md                    # This file
```

## 🚀 Tech Stack

### Frontend
- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Lucide React** - Modern icon library
- **Framer Motion** - Animation library
- **Web Crypto API** - Client-side encryption

### Backend
- **Python 3.8+** - Programming language
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **Cryptography** - Encryption library
- **Pydantic** - Data validation
- **Python-dotenv** - Environment variables

## 🛠️ Installation & Setup

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **npm** or **yarn**
- **pip**

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

5. Create environment file:
```bash
cp .env.example .env
```

6. Generate a secure platform secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

7. Edit `.env` file and replace `platform_secret_key` with the generated key:
```env
platform_secret_key=your_generated_64_character_hex_key_here
```

8. Start the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### Step 2: Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Start the frontend development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Step 3: Verify Setup

1. Open `http://localhost:8000/api/docs` to see the API documentation
2. Open `http://localhost:5173` to see the frontend application
3. Test the encryption workflow in the Hide Message page

## 🔒 Security Features

### Encryption
- **AES-256-GCM**: Military-grade authenticated encryption
- **Argon2id**: OWASP-recommended memory-hard key derivation (resistant to GPU/ASIC attacks)
- **Configurable Parameters**: Time cost, memory cost, parallelism from environment
- **Random salt generation**: Unique salt for each encryption
- **Random nonce generation**: Unique nonce for each GCM operation

### Security Practices
- **Password never sent as plaintext**: Only SHA-256 hash transmitted
- **Environment variables**: Secrets stored securely
- **Input validation**: All inputs validated
- **Error handling**: Comprehensive error handling
- **Logging**: Detailed logging for monitoring
- **CORS protection**: Configured CORS origins

## 📡 API Endpoints

### POST /api/encryption/encrypt
Encrypt a message using Argon2id key derivation and AES-256-GCM.

**Request:**
```json
{
  "message": "plaintext message",
  "password": "user password"
}
```

**Response:**
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

### POST /api/encryption/decrypt
Decrypt a message using Argon2id key derivation and AES-256-GCM.

**Request:**
```json
{
  "ciphertext": "base64_encoded_ciphertext",
  "password": "user password",
  "salt": "base64_encoded_salt",
  "iv": "base64_encoded_iv"
}
```

**Response:**
```json
{
  "success": true,
  "message": "decrypted plaintext message"
}
```

### GET /api/encryption/health
Health check for encryption service.

**Response:**
```json
{
  "status": "healthy",
  "service": "encryption",
  "algorithm": "AES-256-GCM",
  "keyDerivation": "Argon2id"
}
```

### POST /api/steganography/embed
Embed encrypted message into image.

### POST /api/steganography/extract
Extract encrypted message from image.

### POST /api/video/embed
Embed encrypted message into video.

### POST /api/video/extract
Extract encrypted message from video.

### POST /api/audio/embed
Embed encrypted message into audio.

### POST /api/audio/extract
Extract encrypted message from audio.

### POST /api/document/embed
Embed encrypted message into document.

### POST /api/document/extract
Extract encrypted message from document.

## 🎨 Frontend Features

### Pages
- **Landing Page**: Hero section with dashboard preview
- **Hide Message**: Multi-step encryption interface
- **Extract Message**: Multi-step decryption interface
- **About**: Process flow and technical details
- **Contact**: Contact form and information

### UI Components
- **Glassmorphism**: Modern glass-like effects
- **Dark Theme**: Cybersecurity-inspired design
- **Responsive**: Mobile, tablet, and desktop support
- **Animations**: Smooth transitions with Framer Motion
- **Accessibility**: Keyboard navigation and proper contrast

## 🧪 Testing

### Test Encryption Workflow

1. Navigate to `http://localhost:5173/hide`
2. Upload a file (placeholder for steganography)
3. Enter a strong password
4. Type a secret message
5. Click "Encrypt & Hide Message"
6. Verify success message appears

### Test Decryption Workflow

1. Navigate to `http://localhost:5173/extract`
2. Upload an encrypted file (placeholder)
3. Enter the same password used for encryption
4. Click "Extract Secret Message"
5. Verify the original message is displayed

### API Testing with curl

**Encrypt:**
```bash
curl -X POST "http://localhost:8000/api/encryption/encrypt" \
  -H "Content-Type: application/json" \
  -d '{
    "encryptedMessage": "your_base64_encrypted_message",
    "passwordHash": "your_64_character_sha256_hash"
  }'
```

**Decrypt:**
```bash
curl -X POST "http://localhost:8000/api/encryption/decrypt" \
  -H "Content-Type: application/json" \
  -d '{
    "doubleEncryptedMessage": "your_base64_double_encrypted_message",
    "passwordHash": "your_64_character_sha256_hash"
  }'
```

## 🚧 Future Development

### Steganography Integration
- **LSB (Least Significant Bit)** technique for images
- **Video frame encoding** for videos
- **Capacity calculation** based on file size
- **Extraction algorithm** to retrieve hidden data

### Additional Features
- **Database integration** for storing encrypted messages
- **User authentication** system
- **Message expiration** functionality
- **Audit logging** for security monitoring
- **Rate limiting** for API protection
- **File storage** with secure access

## � Documentation

- **Backend API**: `http://localhost:8000/api/docs` (Swagger UI)
- **Backend README**: See `backend/README.md`
- **Frontend Components**: See `src/components/`
- **Crypto Utilities**: See `src/utils/crypto.js`

## 🔧 Configuration

### Backend Environment Variables
Edit `backend/.env`:
```env
platform_secret_key=your_64_character_hex_key
app_name=SecureStego
app_version=1.0.0
debug=False
api_prefix=/api
cors_origins=http://localhost:5173,http://localhost:3000
argon2_time_cost=3
argon2_memory_cost=65536
argon2_parallelism=4
argon2_hash_len=32
argon2_salt_len=16
max_file_size_mb=100
max_image_size_mb=50
max_video_size_mb=500
max_audio_size_mb=100
max_document_size_mb=50
log_level=INFO
```

### Frontend Environment Variables
Edit `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Backend Issues
- **ImportError**: Ensure virtual environment is activated
- **KeyError**: Check `.env` file exists and has correct values
- **CORS errors**: Verify `CORS_ORIGINS` includes frontend URL

### Frontend Issues
- **API connection failed**: Verify backend is running on port 8000
- **Encryption failed**: Check browser console for Web Crypto API errors
- **Build errors**: Clear node_modules and reinstall dependencies

## Documentation

- **API Documentation**: See `docs/API.md` for detailed API reference
- **Architecture**: See `docs/ARCHITECTURE.md` for system architecture details
- **Developer Guide**: See `docs/DEVELOPER_GUIDE.md` for development instructions
- **Backend API**: `http://localhost:8000/api/docs` (Swagger UI)

## License

This project is developed as a Final Year Project.

## Development Team

This project demonstrates:
- Modern full-stack development with frontend/backend separation
- Security best practices (Argon2id, AES-256-GCM, HMAC-SHA256)
- Professional code architecture with layered design
- Production-ready implementation with proper error handling and logging

## Support

For questions or issues:
- Check the API documentation at `/api/docs`
- Review the documentation in the `docs/` folder
- Contact through the Contact page in the application
