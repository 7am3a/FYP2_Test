/**
 * Encryption Context for SecureStego
 * 
 * Provides encryption state and operations to the application.
 */

import React, { createContext, useContext, useReducer } from 'react';
import { encryptionService } from '../services';

const EncryptionContext = createContext();

const initialState = {
  encryptionData: null,
  decryptionData: null,
  isProcessing: false,
  error: null,
};

const encryptionReducer = (state, action) => {
  switch (action.type) {
    case 'SET_ENCRYPTION_DATA':
      return { ...state, encryptionData: action.payload };
    case 'SET_DECRYPTION_DATA':
      return { ...state, decryptionData: action.payload };
    case 'SET_PROCESSING':
      return { ...state, isProcessing: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'CLEAR_DATA':
      return initialState;
    default:
      return state;
  }
};

export const EncryptionProvider = ({ children }) => {
  const [state, dispatch] = useReducer(encryptionReducer, initialState);

  const setEncryptionData = (data) => {
    encryptionService.setEncryptionData(data);
    dispatch({ type: 'SET_ENCRYPTION_DATA', payload: data });
  };

  const setDecryptionData = (data) => {
    encryptionService.setDecryptionData(data);
    dispatch({ type: 'SET_DECRYPTION_DATA', payload: data });
  };

  const clearData = () => {
    encryptionService.clearEncryptionData();
    encryptionService.clearDecryptionData();
    dispatch({ type: 'CLEAR_DATA' });
  };

  const value = {
    ...state,
    setEncryptionData,
    setDecryptionData,
    clearData,
  };

  return (
    <EncryptionContext.Provider value={value}>
      {children}
    </EncryptionContext.Provider>
  );
};

export const useEncryptionContext = () => {
  const context = useContext(EncryptionContext);
  if (!context) {
    throw new Error('useEncryptionContext must be used within EncryptionProvider');
  }
  return context;
};
