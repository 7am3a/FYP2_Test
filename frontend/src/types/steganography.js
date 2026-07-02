/**
 * TypeScript-like type definitions for Steganography
 * 
 * Defines types for steganography operations.
 */

export const SteganographyStatistics = {
  imageWidth: 0,
  imageHeight: 0,
  totalPixels: 0,
  edgePixels: 0,
  payloadSize: 0,
  headerSize: 0,
  totalBitsUsed: 0,
  capacityRemaining: 0,
  capacityUsedPercent: 0,
  embeddingMethod: 'Edge-Based LSB',
  edgeDetectionMethod: 'Canny',
  processingTime: 0,
};

export const EmbedResponse = {
  success: true,
  fileName: '',
  originalFormat: '',
  convertedFormat: 'PNG',
  statistics: SteganographyStatistics,
};

export const ExtractResponse = {
  success: true,
  encryptedData: '',
  algorithm: 'AES-256-GCM',
  version: '1.0',
  timestamp: '',
  statistics: SteganographyStatistics,
};
