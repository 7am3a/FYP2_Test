/**
 * Encryption Service for SecureStego
 * 
 * This service handles encryption-related operations and data management.
 * Since encryption is performed on the backend using Argon2id, this service
 * primarily manages encryption state and provides utility functions.
 */

class EncryptionService {
  constructor() {
    this.currentEncryptionData = null;
    this.currentDecryptionData = null;
  }

  /**
   * Store encryption result data
   * @param {Object} data - Encryption response data
   */
  setEncryptionData(data) {
    this.currentEncryptionData = {
      ...data,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Get current encryption data
   * @returns {Object|null} Current encryption data
   */
  getEncryptionData() {
    return this.currentEncryptionData;
  }

  /**
   * Clear encryption data
   */
  clearEncryptionData() {
    this.currentEncryptionData = null;
  }

  /**
   * Store decryption result data
   * @param {Object} data - Decryption response data
   */
  setDecryptionData(data) {
    this.currentDecryptionData = {
      ...data,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Get current decryption data
   * @returns {Object|null} Current decryption data
   */
  getDecryptionData() {
    return this.currentDecryptionData;
  }

  /**
   * Clear decryption data
   */
  clearDecryptionData() {
    this.currentDecryptionData = null;
  }

  /**
   * Calculate password strength score
   * @param {string} password - Password to evaluate
   * @returns {Object} Strength score and label
   */
  evaluatePasswordStrength(password) {
    if (!password) {
      return { score: 0, label: 'No password', color: 'gray' };
    }

    let score = 0;
    
    // Length check
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (password.length >= 16) score++;
    
    // Complexity checks
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^a-zA-Z0-9]/.test(password)) score++;

    // Normalize to 0-4 scale
    const normalizedScore = Math.min(Math.floor(score / 2), 4);

    const labels = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong'];
    const colors = ['red', 'orange', 'yellow', 'green', 'cyber-green'];

    return {
      score: normalizedScore,
      label: labels[normalizedScore],
      color: colors[normalizedScore]
    };
  }

  /**
   * Format bytes to human-readable string
   * @param {number} bytes - Bytes to format
   * @returns {string} Formatted string
   */
  formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }

  /**
   * Truncate string for display
   * @param {string} str - String to truncate
   * @param {number} maxLength - Maximum length
   * @returns {string} Truncated string
   */
  truncateString(str, maxLength = 50) {
    if (!str) return '';
    if (str.length <= maxLength) return str;
    return str.substring(0, maxLength) + '...';
  }

  /**
   * Generate debug information for display
   * @param {Object} data - Encryption/decryption data
   * @param {string} password - Password used (for length display)
   * @returns {Object} Debug information
   */
  generateDebugInfo(data, password = '') {
    return {
      originalMessage: data.originalMessage || 'N/A',
      passwordLength: password.length,
      generatedSalt: data.salt || 'N/A',
      generatedIV: data.iv || 'N/A',
      encryptionAlgorithm: data.algorithm || 'AES-256-GCM',
      keyDerivationFunction: data.kdf || 'Argon2id',
      encryptedOutput: data.ciphertext || 'N/A',
      processingTime: data.processingTime || 'N/A',
      timestamp: data.timestamp || new Date().toISOString()
    };
  }
}

// Export singleton instance
export const encryptionService = new EncryptionService();
