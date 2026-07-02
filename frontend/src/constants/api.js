/**
 * API Constants for SecureStego
 * 
 * Defines API endpoints and configuration.
 */

export const API_ENDPOINTS = {
  ENCRYPTION: {
    ENCRYPT: '/api/encryption/encrypt',
    DECRYPT: '/api/encryption/decrypt',
    HEALTH: '/api/encryption/health',
  },
  STEGANOGRAPHY: {
    EMBED: '/api/steganography/embed',
    EXTRACT: '/api/steganography/extract',
    DOWNLOAD: '/api/steganography/download',
    HEALTH: '/api/steganography/health',
  },
  VIDEO: {
    EMBED: '/api/video/embed',
    EXTRACT: '/api/video/extract',
    DOWNLOAD: '/api/video/download',
    HEALTH: '/api/video/health',
  },
  AUDIO: {
    EMBED: '/api/audio/embed',
    EXTRACT: '/api/audio/extract',
    DOWNLOAD: '/api/audio/download',
    HEALTH: '/api/audio/health',
  },
  DOCUMENT: {
    EMBED: '/api/document/embed',
    EXTRACT: '/api/document/extract',
    DOWNLOAD: '/api/document/download',
    HEALTH: '/api/document/health',
  },
};

export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  TIMEOUT: 30000, // 30 seconds
};
