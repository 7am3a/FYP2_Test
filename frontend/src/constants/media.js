/**
 * Media Constants for SecureStego
 * 
 * Defines media type constants and limits.
 */

export const MEDIA_TYPES = {
  IMAGE: {
    ALLOWED_EXTENSIONS: ['.png', '.jpg', '.jpeg', '.heic', '.heif'],
    MAX_SIZE_MB: 50,
  },
  VIDEO: {
    ALLOWED_EXTENSIONS: ['.mp4', '.avi', '.mov'],
    MAX_SIZE_MB: 500,
  },
  AUDIO: {
    ALLOWED_EXTENSIONS: ['.wav', '.mp3', '.m4a', '.flac'],
    MAX_SIZE_MB: 100,
  },
  DOCUMENT: {
    ALLOWED_EXTENSIONS: ['.pdf', '.txt'],
    MAX_SIZE_MB: 50,
  },
};

export const STEGANOGRAPHY_METHODS = {
  IMAGE: 'Edge-Based LSB',
  VIDEO: 'DCT-Based Block Steganography',
  AUDIO: 'Randomized WAV LSB',
  DOCUMENT: 'Hybrid Dual-Layer Document Steganography',
};
