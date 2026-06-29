/**
 * Custom Hook for Encryption Operations
 * 
 * This hook manages encryption state and operations.
 */

import { useState, useCallback } from 'react';
import { encryptMessage, decryptMessage } from '../services';

export const useEncryption = () => {
  const [isEncrypting, setIsEncrypting] = useState(false);
  const [isDecrypting, setIsDecrypting] = useState(false);
  const [error, setError] = useState(null);

  const encrypt = useCallback(async (message, password) => {
    setIsEncrypting(true);
    setError(null);
    try {
      const result = await encryptMessage(message, password);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsEncrypting(false);
    }
  }, []);

  const decrypt = useCallback(async (ciphertext, password, salt, iv) => {
    setIsDecrypting(true);
    setError(null);
    try {
      const result = await decryptMessage(ciphertext, password, salt, iv);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsDecrypting(false);
    }
  }, []);

  return {
    encrypt,
    decrypt,
    isEncrypting,
    isDecrypting,
    error,
  };
};
