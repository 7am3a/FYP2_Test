/**
 * SecureStego Client-Side Crypto Utilities
 * 
 * Uses Web Crypto API for client-side encryption/decryption
 * Implements AES-256-GCM with PBKDF2 key derivation
 */

/**
 * Generate a random salt for key derivation
 * @param {number} length - Salt length in bytes (default: 16)
 * @returns {Uint8Array} Random salt
 */
export function generateSalt(length = 16) {
  return crypto.getRandomValues(new Uint8Array(length));
}

/**
 * Generate a random nonce for AES-GCM
 * @param {number} length - Nonce length in bytes (default: 12)
 * @returns {Uint8Array} Random nonce
 */
export function generateNonce(length = 12) {
  return crypto.getRandomValues(new Uint8Array(length));
}

/**
 * Convert string to Uint8Array
 * @param {string} str - Input string
 * @returns {Uint8Array} Byte array
 */
export function stringToBytes(str) {
  return new TextEncoder().encode(str);
}

/**
 * Convert Uint8Array to string
 * @param {Uint8Array} bytes - Byte array
 * @returns {string} Decoded string
 */
export function bytesToString(bytes) {
  return new TextDecoder().decode(bytes);
}

/**
 * Convert Uint8Array to base64 string
 * @param {Uint8Array} bytes - Byte array
 * @returns {string} Base64 encoded string
 */
export function bytesToBase64(bytes) {
  const binaryString = Array.from(bytes, byte => String.fromCharCode(byte)).join('');
  return btoa(binaryString);
}

/**
 * Convert base64 string to Uint8Array
 * @param {string} base64 - Base64 encoded string
 * @returns {Uint8Array} Byte array
 */
export function base64ToBytes(base64) {
  const binaryString = atob(base64);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes;
}

/**
 * Convert hex string to Uint8Array
 * @param {string} hex - Hex string
 * @returns {Uint8Array} Byte array
 */
export function hexToBytes(hex) {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.substr(i, 2), 16);
  }
  return bytes;
}

/**
 * Convert Uint8Array to hex string
 * @param {Uint8Array} bytes - Byte array
 * @returns {string} Hex string
 */
export function bytesToHex(bytes) {
  return Array.from(bytes, byte => byte.toString(16).padStart(2, '0')).join('');
}

/**
 * Generate SHA-256 hash of a string
 * @param {string} data - Input string
 * @returns {Promise<string>} Hex encoded hash
 */
export async function sha256(data) {
  const bytes = stringToBytes(data);
  const hashBuffer = await crypto.subtle.digest('SHA-256', bytes);
  const hashArray = new Uint8Array(hashBuffer);
  return bytesToHex(hashArray);
}

/**
 * Derive encryption key from password using PBKDF2
 * @param {string} password - User password
 * @param {Uint8Array} salt - Salt for key derivation
 * @param {number} iterations - PBKDF2 iterations (default: 100000)
 * @returns {Promise<CryptoKey>} Derived key
 */
export async function deriveKey(password, salt, iterations = 100000) {
  const passwordBytes = stringToBytes(password);
  
  // Import password as key material
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    passwordBytes,
    'PBKDF2',
    false,
    ['deriveKey']
  );
  
  // Derive AES-GCM key
  return crypto.subtle.deriveKey(
    {
      name: 'PBKDF2',
      salt: salt,
      iterations: iterations,
      hash: 'SHA-256'
    },
    keyMaterial,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt']
  );
}

/**
 * Encrypt data using AES-256-GCM
 * @param {string} plaintext - Data to encrypt
 * @param {string} password - User password
 * @returns {Promise<string>} Base64 encoded encrypted data (salt + nonce + ciphertext)
 */
export async function encryptMessage(plaintext, password) {
  try {
    // Generate salt and nonce
    const salt = generateSalt(16);
    const nonce = generateNonce(12);
    
    // Derive key from password
    const key = await deriveKey(password, salt);
    
    // Encrypt data
    const plaintextBytes = stringToBytes(plaintext);
    const encryptedBuffer = await crypto.subtle.encrypt(
      {
        name: 'AES-GCM',
        iv: nonce
      },
      key,
      plaintextBytes
    );
    
    // Combine salt + nonce + ciphertext
    const encryptedBytes = new Uint8Array(encryptedBuffer);
    const combined = new Uint8Array(salt.length + nonce.length + encryptedBytes.length);
    combined.set(salt, 0);
    combined.set(nonce, salt.length);
    combined.set(encryptedBytes, salt.length + nonce.length);
    
    // Return base64 encoded
    return bytesToBase64(combined);
  } catch (error) {
    console.error('Encryption error:', error);
    throw new Error('Failed to encrypt message');
  }
}

/**
 * Decrypt data using AES-256-GCM
 * @param {string} encryptedData - Base64 encoded encrypted data
 * @param {string} password - User password
 * @returns {Promise<string>} Decrypted plaintext
 */
export async function decryptMessage(encryptedData, password) {
  try {
    // Decode base64
    const combined = base64ToBytes(encryptedData);
    
    // Extract components
    const salt = combined.slice(0, 16);
    const nonce = combined.slice(16, 28);
    const ciphertext = combined.slice(28);
    
    // Derive key from password
    const key = await deriveKey(password, salt);
    
    // Decrypt data
    const decryptedBuffer = await crypto.subtle.decrypt(
      {
        name: 'AES-GCM',
        iv: nonce
      },
      key,
      ciphertext
    );
    
    // Convert to string
    const decryptedBytes = new Uint8Array(decryptedBuffer);
    return bytesToString(decryptedBytes);
  } catch (error) {
    console.error('Decryption error:', error);
    throw new Error('Failed to decrypt message. Check your password.');
  }
}

/**
 * Generate password hash for transmission to backend
 * @param {string} password - User password
 * @returns {Promise<string>} SHA-256 hex hash
 */
export async function generatePasswordHash(password) {
  return sha256(password);
}

/**
 * Complete encryption workflow for frontend
 * @param {string} message - Secret message
 * @param {string} password - User password
 * @returns {Promise<{encryptedMessage: string, passwordHash: string}>}
 */
export async function prepareForEncryption(message, password) {
  const encryptedMessage = await encryptMessage(message, password);
  const passwordHash = await generatePasswordHash(password);
  
  return {
    encryptedMessage,
    passwordHash
  };
}

/**
 * Complete decryption workflow for frontend
 * @param {string} encryptedMessage - Client-side encrypted message
 * @param {string} password - User password
 * @returns {Promise<string>} Decrypted message
 */
export async function decryptClientMessage(encryptedMessage, password) {
  return decryptMessage(encryptedMessage, password);
}
