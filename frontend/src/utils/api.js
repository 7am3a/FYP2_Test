/**
 * SecureStego API Client
 * 
 * Handles communication with the FastAPI backend
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
 * Encrypt message using double-layer encryption
 * @param {string} encryptedMessage - Client-side encrypted message (base64)
 * @param {string} passwordHash - SHA-256 hash of password (hex)
 * @returns {Promise<object>} Response with doubleEncryptedMessage
 */
export async function encryptWithBackend(encryptedMessage, passwordHash) {
  return apiRequest('/api/encryption/encrypt', {
    method: 'POST',
    body: JSON.stringify({
      encryptedMessage,
      passwordHash
    })
  });
}

/**
 * Decrypt double-encrypted message
 * @param {string} doubleEncryptedMessage - Double-encrypted message (base64)
 * @param {string} passwordHash - SHA-256 hash of password (hex)
 * @returns {Promise<object>} Response with encryptedMessage
 */
export async function decryptWithBackend(doubleEncryptedMessage, passwordHash) {
  return apiRequest('/api/encryption/decrypt', {
    method: 'POST',
    body: JSON.stringify({
      doubleEncryptedMessage,
      passwordHash
    })
  });
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
