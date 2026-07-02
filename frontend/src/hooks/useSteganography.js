/**
 * Custom Hook for Steganography Operations
 * 
 * This hook manages steganography state and operations.
 */

import { useState, useCallback } from 'react';
import { embedMessage, extractMessage, downloadStegoImage } from '../services';

export const useSteganography = () => {
  const [isEmbedding, setIsEmbedding] = useState(false);
  const [isExtracting, setIsExtracting] = useState(false);
  const [error, setError] = useState(null);

  const embed = useCallback(async (file, encryptedMessage, algorithm) => {
    setIsEmbedding(true);
    setError(null);
    try {
      const result = await embedMessage(file, encryptedMessage, algorithm);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsEmbedding(false);
    }
  }, []);

  const extract = useCallback(async (file) => {
    setIsExtracting(true);
    setError(null);
    try {
      const result = await extractMessage(file);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsExtracting(false);
    }
  }, []);

  const download = useCallback(async (filename) => {
    try {
      const blob = await downloadStegoImage(filename);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  return {
    embed,
    extract,
    download,
    isEmbedding,
    isExtracting,
    error,
  };
};
