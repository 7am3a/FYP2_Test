/**
 * API Service for SecureStego
 * 
 * Handles all API communication with the backend.
 * Uses the new Argon2id-based encryption endpoints.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Make API request with error handling
 * @param {string} endpoint - API endpoint
 * @param {object} options - Fetch options
 * @returns {Promise<object>} Response data
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options
  };
  
  try {
    const response = await fetch(url, defaultOptions);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request error:', error);
    throw error;
  }
}

/**
 * Encrypt a message using the backend API
 * @param {string} message - Plaintext message to encrypt
 * @param {string} password - User password
 * @returns {Promise<object>} Encryption response with ciphertext, salt, iv, etc.
 */
export async function encryptMessage(message, password) {
  const startTime = performance.now();
  
  try {
    const response = await apiRequest('/api/encryption/encrypt', {
      method: 'POST',
      body: JSON.stringify({
        message,
        password
      })
    });
    
    const endTime = performance.now();
    const processingTime = ((endTime - startTime) / 1000).toFixed(3);
    
    return {
      ...response,
      processingTime,
      originalMessage: message
    };
  } catch (error) {
    console.error('Encryption API error:', error);
    throw new Error(error.message || 'Failed to encrypt message');
  }
}

/**
 * Decrypt a message using the backend API
 * @param {string} ciphertext - Base64 encoded ciphertext
 * @param {string} password - User password
 * @param {string} salt - Base64 encoded salt
 * @param {string} iv - Base64 encoded IV
 * @returns {Promise<object>} Decryption response with original message
 */
export async function decryptMessage(ciphertext, password, salt, iv) {
  const startTime = performance.now();
  
  try {
    const response = await apiRequest('/api/encryption/decrypt', {
      method: 'POST',
      body: JSON.stringify({
        ciphertext,
        password,
        salt,
        iv
      })
    });
    
    const endTime = performance.now();
    const processingTime = ((endTime - startTime) / 1000).toFixed(3);
    
    return {
      ...response,
      processingTime
    };
  } catch (error) {
    console.error('Decryption API error:', error);
    throw new Error(error.message || 'Failed to decrypt message');
  }
}

/**
 * Check backend health
 * @returns {Promise<object>} Health status
 */
export async function checkHealth() {
  return apiRequest('/health');
}

/**
 * Check encryption service health
 * @returns {Promise<object>} Encryption service status
 */
export async function checkEncryptionHealth() {
  return apiRequest('/api/encryption/health');
}

/**
 * Get API base URL
 * @returns {string} API base URL
 */
export function getApiBaseUrl() {
  return API_BASE_URL;
}

/**
 * Embed encrypted message into an image using steganography
 * @param {File} file - Image file to embed message into
 * @param {string} encryptedMessage - Base64 encoded encrypted message
 * @param {string} salt - Base64 encoded salt for key derivation
 * @param {string} iv - Base64 encoded IV for encryption
 * @param {string} algorithm - Encryption algorithm used (default: AES-256-GCM)
 * @param {string} kdf - Key derivation function used (default: Argon2id)
 * @returns {Promise<object>} Embed response with stego image information
 */
export async function embedMessage(
    file,
    encryptedMessage,
    salt,
    iv,
    password = null,
    algorithm = 'AES-256-GCM',
    kdf = 'Argon2id') {
  const startTime = performance.now();
  
  try {
    const formData = new FormData();

    let endpoint = '';
    let fileField = '';

    if (file.type.startsWith('image/')) {
        endpoint = '/api/steganography/embed';
        fileField = 'image';
    }
    else if (file.type.startsWith('audio/')) {
        endpoint = '/api/audio/embed';
        fileField = 'audio';
    }
    else if (file.type.startsWith('video/')) {
        endpoint = '/api/video/embed';
        fileField = 'video';
    }
    else {
        throw new Error('Unsupported media type');
    }

    formData.append(fileField, file);
    formData.append('encryptedMessage', encryptedMessage);
    formData.append('salt', salt);
    formData.append('iv', iv);
    formData.append('password', password);

    formData.append('algorithm', algorithm);
    formData.append('kdf', kdf);
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    
    const endTime = performance.now();
    const processingTime = ((endTime - startTime) / 1000).toFixed(3);
    
    return {
      ...result,
      processingTime,
      originalFileName: file.name
    };
  } catch (error) {
    console.error('Embed API error:', error);
    throw new Error(error.message || 'Failed to embed message');
  }
}

/**
 * Extract encrypted message from a stego image
 * @param {File} file - Stego image file containing hidden message
 * @returns {Promise<object>} Extract response with encrypted message and statistics
 */
export async function extractMessage(file, password) {
  const startTime = performance.now();

  try {
    const formData = new FormData();

    let endpoint = '';
    let fileField = '';

    if (file.type.startsWith('image/')) {
      endpoint = '/api/steganography/extract';
      fileField = 'image';
    }
    else if (file.type.startsWith('audio/')) {
      endpoint = '/api/audio/extract';
      fileField = 'audio';
    }
    else if (file.type.startsWith('video/')) {
      endpoint = '/api/video/extract';
      fileField = 'video';
    }
    else {
      throw new Error('Unsupported media type');
    }

    formData.append(fileField, file);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        detail: 'Unknown error'
      }));

      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    const endTime = performance.now();

    return {
      ...result,
      processingTime: ((endTime - startTime) / 1000).toFixed(3),
      originalFileName: file.name
    };

  } catch (error) {
    console.error('Extract API error:', error);
    throw new Error(error.message || 'Failed to extract message');
  }
}

/**
 * Download stego image from server
 * @param {string} filename - Name of the stego image file
 * @returns {Promise<Blob>} Blob of the stego image
 */
export async function downloadStegoImage(filename) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/steganography/download/${filename}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.blob();
  } catch (error) {
    console.error('Download error:', error);
    throw new Error(error.message || 'Failed to download stego image');
  }
}

/**
 * Check steganography service health
 * @returns {Promise<object>} Steganography service status
 */
export async function checkSteganographyHealth() {
  return apiRequest('/api/steganography/health');
}
