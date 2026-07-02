# SecureStego Testing Guide

This guide provides instructions for testing the SecureStego encryption system with Argon2id key derivation.

## Prerequisites

Before testing, ensure:
- Backend server is running on `http://localhost:8000`
- Frontend is running on `http://localhost:5173`
- Backend `.env` file is configured (no SERVER_MASTER_KEY needed for Argon2id)
- Frontend `.env` file is configured with correct `VITE_API_URL`
- argon2-cffi is installed in the backend

## Backend Setup

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Backend Testing

### 1. Health Check

Test if the backend is running:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "SecureStego",
  "version": "1.0.0"
}
```

### 2. Encryption Service Health

Test the encryption service:

```bash
curl http://localhost:8000/api/encryption/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "encryption",
  "algorithm": "AES-256-GCM",
  "keyDerivation": "Argon2id"
}
```

### 3. API Documentation

Open `http://localhost:8000/api/docs` in your browser to access the Swagger UI documentation.

## Frontend Testing

### Test Complete Encryption Workflow

1. **Navigate to Hide Message Page**
   - Open `http://localhost:5173/hide`

2. **Enter Secret Message**
   - Type a secret message in the message field
   - Example: "Hello World"

3. **Enter Password**
   - Enter a strong password (minimum 1 character for testing)
   - Example: "MyPassword123"
   - Verify password strength indicator updates

4. **Click Encrypt Message**
   - Click the "Encrypt Message" button
   - Verify loading animation appears
   - Wait for processing to complete
   - Verify success message appears
   - Check browser console for any errors

5. **Verify Encryption Output**
   - Open the "Encryption Debug Panel" (yellow panel)
   - Verify the following are displayed:
     - Original Message
     - Password Length
     - Generated Salt (base64)
     - Generated IV (base64)
     - Encryption Algorithm: AES-256-GCM
     - Key Derivation Function: Argon2id
     - Encrypted Output (ciphertext)
     - Processing Time
     - API Status: Success

6. **Copy Encryption Data**
   - Copy the Ciphertext, Salt, and IV from the debug panel
   - You'll need these for decryption testing

### Test Complete Decryption Workflow

1. **Navigate to Extract Message Page**
   - Open `http://localhost:5173/extract`

2. **Enter Password**
   - Enter the same password used for encryption
   - Example: "MyPassword123"

3. **Enter Encryption Data**
   - Paste the Ciphertext from the encryption output
   - Paste the Salt from the encryption output
   - Paste the IV from the encryption output

4. **Click Decrypt Message**
   - Click the "Decrypt Message" button
   - Verify loading animation appears
   - Wait for processing to complete
   - Verify success message appears
   - Check browser console for any errors

5. **Verify Decryption Output**
   - Verify the original message is displayed
   - Example: "Hello World"
   - Open the "Encryption Debug Panel" to see decryption details
   - Verify processing time is displayed

6. **Verify Error Handling**
   - Try decrypting with wrong password
   - Verify appropriate error message appears
   - Try decrypting with missing fields
   - Verify appropriate error message appears

## API Testing with curl

### Test Encryption Endpoint

```bash
curl -X POST "http://localhost:8000/api/encryption/encrypt" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello World",
    "password": "MyPassword123"
  }'
```

Expected response:
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

### Test Decryption Endpoint

```bash
curl -X POST "http://localhost:8000/api/encryption/decrypt" \
  -H "Content-Type: application/json" \
  -d '{
    "ciphertext": "base64_encoded_ciphertext",
    "password": "MyPassword123",
    "salt": "base64_encoded_salt",
    "iv": "base64_encoded_iv"
  }'
```

Expected response:
```json
{
  "success": true,
  "message": "Hello World"
}
```

## Error Scenarios

### Test Missing Fields

```bash
curl -X POST "http://localhost:8000/api/encryption/encrypt" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "test"
  }'
```

Expected: 422 Validation Error

### Test Wrong Password for Decryption

```bash
curl -X POST "http://localhost:8000/api/encryption/decrypt" \
  -H "Content-Type: application/json" \
  -d '{
    "ciphertext": "base64_ciphertext",
    "password": "wrong_password",
    "salt": "base64_salt",
    "iv": "base64_iv"
  }'
```

Expected: 400 Bad Request with "Decryption failed" error

## Browser Console Testing

### Test API Connection

Open browser console on the frontend:

```javascript
// Test health check
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log);

// Test encryption health
fetch('http://localhost:8000/api/encryption/health')
  .then(r => r.json())
  .then(console.log);
```

## Test Checklist

- [ ] Backend health check passes
- [ ] Encryption service health check passes
- [ ] API documentation accessible
- [ ] Encrypt message with "Hello World" and "MyPassword123"
- [ ] Verify ciphertext, salt, and iv are generated
- [ ] Verify Argon2id is used as KDF
- [ ] Verify AES-256-GCM is used as algorithm
- [ ] Debug panel displays all encryption details
- [ ] Decrypt message using same password
- [ ] Verify original message is recovered
- [ ] Error handling works for missing fields
- [ ] Error handling works for wrong password
- [ ] Processing time is displayed
- [ ] Copy buttons work in debug panel

## Next Steps

After successful testing:
1. Implement steganography integration
2. Add database support
3. Implement user authentication
4. Add rate limiting
5. Deploy to production
