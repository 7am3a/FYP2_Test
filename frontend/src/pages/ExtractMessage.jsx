import React, { useState } from 'react';
import { Eye, Unlock, CheckCircle, AlertCircle, Copy, FileText, Shield, Image as ImageIcon } from 'lucide-react';
import { motion } from 'framer-motion';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import FileUpload from '../components/ui/FileUpload';
import PasswordInput from '../components/ui/PasswordInput';
import { decryptMessage, extractMessage, encryptionService } from '../services';

const ExtractMessage = () => {
  const [file, setFile] = useState(null);
  const [password, setPassword] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [extractedMessage, setExtractedMessage] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [error, setError] = useState('');
  const [decryptionData, setDecryptionData] = useState(null);
  const [stegoData, setStegoData] = useState(null);

  const handleExtract = async () => {
    setIsProcessing(true);
    setError('');
    
    try {
      // Step 1: Extract encrypted message from stego image
      if (!file) {
        throw new Error('Please upload a stego media file');
      }
      
      const stegoResponse = await extractMessage(file, password);
      
      if (!stegoResponse.success) {
        throw new Error('Steganography extraction failed');
      }
      
      setStegoData(stegoResponse);
      
      // Step 2: Decrypt the extracted encrypted message
      // The stegoResponse contains encryptedData, salt, and iv (embedded in payload version 2.0+)
      const { encryptedData, salt, iv } = stegoResponse;
      
      if (!salt || !iv) {
        throw new Error('This media was encrypted with an older version. Please provide salt and IV manually.');
      }
      
      const decryptResponse = await decryptMessage(
        encryptedData,
        password,
        salt,
        iv
      );
      
      if (!decryptResponse.success) {
        throw new Error('Decryption failed');
      }
      
      // Store decryption data in service
      encryptionService.setDecryptionData(decryptResponse);
      
      // Prepare debug information
      const debugInfo = encryptionService.generateDebugInfo({
        ...decryptResponse,
        ciphertext: encryptedData,
        salt,
        iv,
        originalMessage: decryptResponse.message
      }, password);
      
      setDecryptionData(debugInfo);
      setExtractedMessage(decryptResponse.message);
      setShowResult(true);
      
    } catch (err) {
      console.error('Extraction/Decryption error:', err);
      setError(err.message || 'Failed to extract and decrypt message. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(extractedMessage);
  };

  return (
    <div className="min-h-screen bg-cyber-gradient pt-24 pb-20 px-4 sm:px-6 lg:px-8">
      {/* Background Effects */}
      <div className="absolute inset-0 glow-gradient opacity-20" />
      <div className="absolute top-40 left-20 w-96 h-96 bg-cyber-accent/10 rounded-full blur-3xl" />
      
      <div className="relative z-10 max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gradient mb-4">
            Extract Secret Message
          </h1>
          <p className="text-gray-400 text-lg">
            Reveal hidden messages from encrypted images or videos
          </p>
        </motion.div>

        {!showResult ? (
          <div className="space-y-6">
            {/* Step 1: Upload Encrypted File */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
            >
              <Card className="card-step">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 rounded-full bg-cyber-accent/20 flex items-center justify-center">
                    <span className="text-cyber-accent font-bold">1</span>
                  </div>
                  <h2 className="text-xl font-semibold text-white">Upload Encrypted File</h2>
                </div>
                <FileUpload
                  onFileSelect={setFile}
                  label="Select the image or video containing the hidden message"
                />
              </Card>
            </motion.div>

            {/* Step 2: Enter Password */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <Card className="card-step">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 rounded-full bg-cyber-purple/20 flex items-center justify-center">
                    <span className="text-cyber-purple font-bold">2</span>
                  </div>
                  <h2 className="text-xl font-semibold text-white">Enter Password</h2>
                </div>
                <PasswordInput
                  label="Enter the password used to encrypt the message"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter the decryption password"
                />
              </Card>
            </motion.div>


            {/* Error Display */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-6"
              >
                <Card className="bg-red-500/10 border-red-500/30 p-4">
                  <div className="flex items-center space-x-3">
                    <AlertCircle className="w-5 h-5 text-red-500" />
                    <span className="text-red-400 text-sm">{error}</span>
                  </div>
                </Card>
              </motion.div>
            )}

            {/* Step 3: Extract Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="flex justify-center"
            >
              <Button
                onClick={handleExtract}
                disabled={!file || !password || isProcessing}
                className="w-full md:w-auto px-12 py-4 text-lg"
              >
                {isProcessing ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      className="mr-2"
                    >
                      <Unlock className="w-5 h-5" />
                    </motion.div>
                    Decrypting...
                  </>
                ) : (
                  <>
                    <Eye className="w-5 h-5 mr-2" />
                    Decrypt Message
                  </>
                )}
              </Button>
            </motion.div>

            {/* Security Note */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <Card className="glass p-6 border-cyber-green/30">
                <div className="flex items-start space-x-3">
                  <Shield className="w-6 h-6 text-cyber-green mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-white font-semibold mb-2">Security Note</h3>
                    <p className="text-gray-400 text-sm">
                      The extraction process automatically recovers encryption metadata from the embedded payload. 
                      Only your password is required to decrypt the hidden message. Incorrect passwords will not reveal the message.
                    </p>
                  </div>
                </div>
              </Card>
            </motion.div>
          </div>
        ) : (
          /* Result Panel */
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <Card className="text-center py-12">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                className="w-24 h-24 mx-auto mb-6 rounded-full bg-cyber-green/20 flex items-center justify-center"
              >
                <CheckCircle className="w-12 h-12 text-cyber-green" />
              </motion.div>
              
              <h2 className="text-3xl font-bold text-white mb-4">
                Message Extracted Successfully!
              </h2>
              
              <div className="glass p-6 rounded-xl mb-8 max-w-2xl mx-auto text-left">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <FileText className="w-6 h-6 text-cyber-accent" />
                    <span className="text-white font-medium">Extracted Message</span>
                  </div>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={copyToClipboard}
                    className="px-4 py-2 text-sm"
                  >
                    <Copy className="w-4 h-4 mr-2" />
                    Copy
                  </Button>
                </div>
                <div className="bg-black/30 rounded-xl p-4 max-h-64 overflow-y-auto">
                  <p className="text-gray-300 whitespace-pre-wrap">{extractedMessage}</p>
                </div>
              </div>

              {/* Status Indicators */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 max-w-2xl mx-auto">
                <div className="glass p-4 rounded-xl">
                  <div className="text-sm text-gray-400 mb-1">Message Length</div>
                  <div className="text-white font-medium">{extractedMessage.length} characters</div>
                </div>
                <div className="glass p-4 rounded-xl">
                  <div className="text-sm text-gray-400 mb-1">Algorithm</div>
                  <div className="text-white font-medium">
                    {typeof stegoData?.algorithm === 'string' ? stegoData.algorithm : 'AES-256-GCM'}
                  </div>
                </div>
                <div className="glass p-4 rounded-xl">
                  <div className="text-sm text-gray-400 mb-1">Status</div>
                  <div className="text-cyber-green font-medium flex items-center">
                    <CheckCircle className="w-4 h-4 mr-1" />
                    Extracted & Decrypted
                  </div>
                </div>
              </div>

              {/* Steganography Information */}
              {stegoData && (
                <div className="glass p-6 rounded-xl mb-8 max-w-2xl mx-auto">
                  <div className="flex items-center justify-center space-x-3 mb-4">
                    <ImageIcon className="w-6 h-6 text-cyber-accent" />
                    <span className="text-white font-medium">Steganography Information</span>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-gray-400">Edge Pixels</div>
                      <div className="text-white font-medium">{stegoData.statistics?.edgePixels || 'N/A'}</div>
                    </div>
                    <div>
                      <div className="text-gray-400">Payload Size</div>
                      <div className="text-white font-medium">{stegoData.statistics?.payloadSize || 'N/A'} bytes</div>
                    </div>
                    <div>
                      <div className="text-gray-400">Extraction Method</div>
                      <div className="text-white font-medium">{stegoData.statistics?.extractionMethod || 'Edge-Based LSB'}</div>
                    </div>
                    <div>
                      <div className="text-gray-400">Processing Time</div>
                      <div className="text-white font-medium">{stegoData?.processingTime || 'N/A'}s</div>
                    </div>
                  </div>
                </div>
              )}

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button
                  variant="secondary"
                  onClick={() => {
                    setShowResult(false);
                    setFile(null);
                    setPassword('');
                    setExtractedMessage('');
                    setError('');
                    setDecryptionData(null);
                    setStegoData(null);
                    encryptionService.clearDecryptionData();
                  }}
                >
                  Extract Another Message
                </Button>
              </div>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default ExtractMessage;
