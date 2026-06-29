# SecureStego Backend API

FastAPI backend for SecureStego with double-layer encryption using AES-256-GCM and PBKDF2.

## Architecture

The encryption system uses two layers of encryption:

1. **Client-side encryption** (JavaScript/Web Crypto API)
   - AES-256-GCM encryption
   - PBKDF2-HMAC-SHA256 key derivation
   - Password is never sent as plaintext

2. **Server-side encryption** (Python/FastAPI)
   - AES-256-GCM encryption
   - PBKDF2-HMAC-SHA256 key derivation
   - Combines password hash with server master key

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── encryption.py       # API endpoints
│   └── security/
│       ├── __init__.py
│       └── encryption.py       # Encryption service
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

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

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create environment file:
```bash
cp .env.example .env
```

6. Generate a secure server master key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

7. Edit `.env` file and replace `SERVER_MASTER_KEY` with the generated key:
```env
SERVER_MASTER_KEY=your_generated_64_character_hex_key_here
```

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## API Endpoints

### POST /api/encryption/encrypt

Encrypt a message using double-layer encryption.

**Request:**
```json
{
  "encryptedMessage": "base64_encoded_client_encrypted_message",
  "passwordHash": "64_character_sha256_hex_hash"
}
```

**Response:**
```json
{
  "doubleEncryptedMessage": "base64_encoded_double_encrypted_message",
  "status": "success",
  "metadata": {
    "algorithm": "AES-256-GCM",
    "encryptionLayers": 2,
    "keyDerivation": "PBKDF2-HMAC-SHA256",
    "iterations": 100000
  }
}
```

### POST /api/encryption/decrypt

Decrypt a double-encrypted message.

**Request:**
```json
{
  "doubleEncryptedMessage": "base64_encoded_double_encrypted_message",
  "passwordHash": "64_character_sha256_hex_hash"
}
```

**Response:**
```json
{
  "encryptedMessage": "base64_encoded_client_encrypted_message",
  "status": "success"
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
  "keyDerivation": "PBKDF2-HMAC-SHA256"
}
```

### GET /

Root endpoint with API information.

**Response:**
```json
{
  "name": "SecureStego",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "docs": "/api/docs",
    "health": "/api/encryption/health",
    "encrypt": "/api/encryption/encrypt",
    "decrypt": "/api/encryption/decrypt"
  }
}
```

## Security Features

- **AES-256-GCM**: Military-grade encryption
- **PBKDF2-HMAC-SHA256**: Secure key derivation with 100,000 iterations
- **Random salt generation**: Unique salt for each encryption
- **Random nonce generation**: Unique nonce for each GCM operation
- **Environment variables**: Secrets stored securely
- **Input validation**: All inputs validated
- **Error handling**: Comprehensive error handling
- **Logging**: Detailed logging for monitoring

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_MASTER_KEY` | 64-character hex key for server-side encryption | Required |
| `APP_NAME` | Application name | SecureStego |
| `APP_VERSION` | Application version | 1.0.0 |
| `DEBUG` | Debug mode | False |
| `API_PREFIX` | API URL prefix | /api |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:5173,http://localhost:3000 |
| `PBKDF2_ITERATIONS` | PBKDF2 iterations | 100000 |
| `SALT_LENGTH` | Salt length in bytes | 32 |

## Testing

### Using curl

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

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful operation
- `400 Bad Request`: Invalid input or validation error
- `500 Internal Server Error`: Server error

Error responses follow this format:
```json
{
  "detail": "Error message",
  "status": "error"
}
```

## Logging

The application logs important events:
- Startup and shutdown
- Encryption/decryption requests
- Validation errors
- Encryption/decryption errors

Logs are output to the console with timestamp, logger name, log level, and message.

## Security Best Practices

1. **Never commit `.env` file** - It contains sensitive information
2. **Use strong passwords** - Minimum 12 characters recommended
3. **Rotate server master key** - Regularly rotate the server master key
4. **Use HTTPS in production** - Always use HTTPS in production
5. **Monitor logs** - Regularly monitor logs for suspicious activity
6. **Keep dependencies updated** - Regularly update dependencies

## Future Enhancements

- Rate limiting
- Request authentication
- Database integration for storing encrypted messages
- Message expiration
- Audit logging
- Key rotation mechanism

## License

This project is developed as a Final Year Project.
