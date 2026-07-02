import React, { useState } from 'react';
import { Eye, Unlock, CheckCircle, Copy, FileText, Shield, Image as ImageIcon, ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import UploadCard from '../components/ui/UploadCard';
import PasswordCard from '../components/ui/PasswordCard';
import ActionCard from '../components/ui/ActionCard';
import SecurityInfoBar from '../components/ui/SecurityInfoBar';
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

  const handleRemoveFile = () => {
    setFile(null);
  };

  return (
    <div className="min-h-screen bg-bg-primary pt-24 pb-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-[1600px] mx-auto px-8">
        {/* Side Badges */}
        <div className="flex justify-between items-center mb-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-2 glass px-4 py-2 rounded-full"
          >
            <ShieldCheck className="w-5 h-5 text-success" />
            <span className="text-sm text-text-secondary font-medium">MILITARY GRADE ENCRYPTION</span>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-2 glass px-4 py-2 rounded-full"
          >
            <Shield className="w-5 h-5 text-accent-primary" />
            <span className="text-sm text-text-secondary font-medium">YOUR PRIVACY OUR PRIORITY</span>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-6xl md:text-7xl font-bold text-text-primary mb-4">
            Extract Secret Message
          </h1>
          <p className="text-xl text-text-secondary">
            Reveal hidden messages from encrypted images or videos
          </p>
        </motion.div>

        {!showResult ? (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6 items-stretch">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 }}
                className="h-full"
              >
                <UploadCard
                  onFileSelect={setFile}
                  file={file}
                  onRemove={handleRemoveFile}
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="h-full"
              >
                <ActionCard
                  onClick={handleExtract}
                  disabled={!file || !password || isProcessing}
                  isProcessing={isProcessing}
                  buttonText="Decrypt Message"
                  processingText="Decrypting..."
                  icon={Eye}
                  error={error}
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
                className="h-full"
              >
                <PasswordCard
                  password={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter the decryption password"
                  showStrength={false}
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="h-full"
              >
                <Card className="flex flex-col justify-start h-full">
                  <div className="flex items-start space-x-3">
                    <Shield className="w-5 h-5 text-success mt-1 flex-shrink-0" />
                    <div>
                      <h3 className="text-text-primary font-semibold text-sm mb-2">Security Note</h3>
                      <p className="text-text-muted text-xs leading-relaxed">
                        The extraction process automatically recovers encryption metadata from the embedded payload. 
                        Only your password is required to decrypt the hidden message. Incorrect passwords will not reveal the message.
                      </p>
                    </div>
                  </div>
                </Card>
              </motion.div>
            </div>

            <SecurityInfoBar />
          </>
        ) : (
          /* Result Panel */
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <Card className="text-center py-8">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                className="w-20 h-20 mx-auto mb-3 rounded-full bg-success/20 flex items-center justify-center"
              >
                <CheckCircle className="w-10 h-10 text-success" />
              </motion.div>
              
              <h2 className="text-2xl font-bold text-text-primary mb-2">
                Message Extracted Successfully!
              </h2>
              
              <p className="text-text-secondary mb-8 max-w-md mx-auto text-sm">
                Your secret message has been extracted and decrypted successfully.
              </p>
              
              <div className="glass p-6 rounded-xl mb-8 max-w-3xl mx-auto text-left">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <FileText className="w-5 h-5 text-accent-primary" />
                    <span className="text-text-primary font-medium text-sm">Extracted Message</span>
                  </div>
                  <Button
                    variant="secondary"
                    onClick={copyToClipboard}
                    className="px-3 py-1.5 text-xs"
                  >
                    <Copy className="w-3.5 h-3.5 mr-1.5" />
                    Copy
                  </Button>
                </div>
                <div className="bg-card-secondary rounded-lg p-4 max-h-48 overflow-y-auto">
                  <p className="text-text-primary whitespace-pre-wrap text-sm">{extractedMessage}</p>
                </div>
              </div>

              {/* Status Indicators */}
              <div className="grid grid-cols-3 gap-4 mb-8 max-w-lg mx-auto items-stretch">
                <div className="glass p-4 rounded-lg flex flex-col justify-center">
                  <div className="text-xs text-text-muted mb-1">Message Length</div>
                  <div className="text-text-primary font-medium text-sm">{extractedMessage.length} chars</div>
                </div>
                <div className="glass p-4 rounded-lg flex flex-col justify-center">
                  <div className="text-xs text-text-muted mb-1">Algorithm</div>
                  <div className="text-text-primary font-medium text-sm">
                    {typeof stegoData?.algorithm === 'string' ? stegoData.algorithm : 'AES-256-GCM'}
                  </div>
                </div>
                <div className="glass p-4 rounded-lg flex flex-col justify-center">
                  <div className="text-xs text-text-muted mb-1">Status</div>
                  <div className="text-success font-medium flex items-center text-sm">
                    <CheckCircle className="w-3.5 h-3.5 mr-1" />
                    Success
                  </div>
                </div>
              </div>

              {/* Steganography Information */}
              {stegoData && (
                <div className="glass p-6 rounded-xl mb-4 max-w-3xl mx-auto">
                  <div className="flex items-center justify-center space-x-2 mb-4">
                    <ImageIcon className="w-5 h-5 text-accent-primary" />
                    <span className="text-text-primary font-medium text-sm">Steganography Information</span>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <div className="text-text-muted mb-1">Edge Pixels</div>
                      <div className="text-text-primary font-medium">{stegoData.statistics?.edgePixels || 'N/A'}</div>
                    </div>
                    <div>
                      <div className="text-text-muted mb-1">Payload Size</div>
                      <div className="text-text-primary font-medium">{stegoData.statistics?.payloadSize || 'N/A'} bytes</div>
                    </div>
                    <div>
                      <div className="text-text-muted mb-1">Extraction Method</div>
                      <div className="text-text-primary font-medium">{stegoData.statistics?.extractionMethod || 'Edge-Based LSB'}</div>
                    </div>
                    <div>
                      <div className="text-text-muted mb-1">Processing Time</div>
                      <div className="text-text-primary font-medium">{stegoData?.processingTime || 'N/A'}s</div>
                    </div>
                  </div>
                </div>
              )}

              <div className="flex flex-col sm:flex-row gap-3 justify-center">
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
