/**
 * TypeScript-like type definitions for Encryption
 * 
 * Defines types for encryption operations.
 */

export const EncryptResponse = {
  success: true,
  ciphertext: '',
  salt: '',
  iv: '',
  algorithm: 'AES-256-GCM',
  kdf: 'Argon2id',
};

export const DecryptResponse = {
  success: true,
  message: '',
};
