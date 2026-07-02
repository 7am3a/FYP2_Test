import React, { useState } from 'react';
import { Lock, CheckCircle, Download, Image as ImageIcon, ShieldCheck, Shield } from 'lucide-react';
import { motion } from 'framer-motion';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import UploadCard from '../components/ui/UploadCard';
import PasswordCard from '../components/ui/PasswordCard';
import MessageCard from '../components/ui/MessageCard';
import ActionCard from '../components/ui/ActionCard';
import SecurityInfoBar from '../components/ui/SecurityInfoBar';
import { encryptMessage, embedMessage, encryptionService } from '../services';

const HideMessage = () => {
  const [file, setFile] = useState(null);
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState('');
  const [encryptionData, setEncryptionData] = useState(null);
  const [stegoData, setStegoData] = useState(null);

  const passwordStrength = () => {
    if (!password) return { score: 0, label: 'No password', color: 'gray' };
    if (password.length < 8) return { score: 1, label: 'Weak', color: 'red' };
    if (password.length < 12) return { score: 2, label: 'Medium', color: 'yellow' };
    if (password.length < 16) return { score: 3, label: 'Strong', color: 'green' };
    return { score: 4, label: 'Very Strong', color: 'cyber-green' };
  };

  const strength = passwordStrength();

  const handleEncrypt = async () => {
    setIsProcessing(true);
    setError('');
    
    try {
      // Step 1: Encrypt using backend API with Argon2id
      const encryptionResponse = await encryptMessage(message, password);
      
      if (!encryptionResponse.success) {
        throw new Error('Encryption failed');
      }
      
      // Store encryption data in service
      encryptionService.setEncryptionData(encryptionResponse);
      
      // Prepare debug information
      const debugInfo = encryptionService.generateDebugInfo({
        ...encryptionResponse,
        originalMessage: message
      }, password);
      
      setEncryptionData(debugInfo);
      
      // Step 2: Embed encrypted message into image using steganography
      if (!file) {
        throw new Error('Please upload an image file');
      }
      
      const stegoResponse = await embedMessage(
        file,
        encryptionResponse.ciphertext,
        encryptionResponse.salt,
        encryptionResponse.iv,
        password,
        encryptionResponse.algorithm,
        encryptionResponse.kdf
      );
      
      if (!stegoResponse.success) {
        throw new Error('Steganography embedding failed');
      }
      
      setStegoData(stegoResponse);
      setShowSuccess(true);
      
    } catch (err) {
      console.error('Encryption/Steganography error:', err);
      setError(err.message || 'Failed to process message. Please try again.');
    } finally {
      setIsProcessing(false);
    }
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
            Hide Secret Message
          </h1>
          <p className="text-xl text-text-secondary">
            Encrypt and hide your message securely inside an image or video
          </p>
        </motion.div>

        {!showSuccess ? (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 }}
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
              >
                <MessageCard
                  message={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Type your confidential message here..."
                  maxLength={10000}
                  showCapacity={true}
                  capacityText={`Capacity: ~${file ? (file.size / 1024).toFixed(0) : '0'} KB available`}
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
              >
                <PasswordCard
                  password={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter a strong password"
                  showStrength={true}
                  strength={strength}
                />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
              >
                <ActionCard
                  onClick={handleEncrypt}
                  disabled={!password || !message || isProcessing}
                  isProcessing={isProcessing}
                  buttonText="Encrypt Message"
                  processingText="Encrypting..."
                  icon={Lock}
                  error={error}
                />
              </motion.div>
            </div>

            <SecurityInfoBar />
          </>
        ) : (
          /* Success Result Section */
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
                className="w-20 h-20 mx-auto mb-4 rounded-full bg-success/20 flex items-center justify-center"
              >
                <CheckCircle className="w-10 h-10 text-success" />
              </motion.div>
              
              <h2 className="text-2xl font-bold text-text-primary mb-3">
                Message Hidden Successfully!
              </h2>
              
              <p className="text-text-secondary mb-6 max-w-md mx-auto text-sm">
                Your secret message has been encrypted and securely hidden inside the file. 
                The file is ready for download.
              </p>

              <div className="glass p-5 rounded-xl mb-6 max-w-lg mx-auto">
                <div className="grid grid-cols-3 gap-4 text-xs">
                  <div>
                    <div className="text-text-muted mb-1">Algorithm</div>
                    <div className="text-text-primary font-medium">{encryptionData?.encryptionAlgorithm || 'AES-256-GCM'}</div>
                  </div>
                  <div>
                    <div className="text-text-muted mb-1">KDF</div>
                    <div className="text-text-primary font-medium">{encryptionData?.keyDerivationFunction || 'Argon2id'}</div>
                  </div>
                  <div>
                    <div className="text-text-muted mb-1">Message Length</div>
                    <div className="text-text-primary font-medium">{message.length} chars</div>
                  </div>
                  <div>
                    <div className="text-text-muted mb-1">Processing Time</div>
                    <div className="text-text-primary font-medium">{stegoData?.processingTime || 'N/A'}s</div>
                  </div>
                  <div>
                    <div className="text-text-muted mb-1">Original Format</div>
                    <div className="text-text-primary font-medium">{stegoData?.originalFormat || 'N/A'}</div>
                  </div>
                  <div>
                    <div className="text-text-muted mb-1">Edge Pixels</div>
                    <div className="text-text-primary font-medium">{stegoData?.statistics?.edgePixels || 'N/A'}</div>
                  </div>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <Button
                  onClick={async () => {
                    try {
                      const { downloadStegoImage } = await import('../services');
                      const blob = await downloadStegoImage(stegoData.fileName);
                      const url = window.URL.createObjectURL(blob);
                      const a = document.createElement('a');
                      a.href = url;
                      a.download = stegoData.fileName;
                      document.body.appendChild(a);
                      a.click();
                      window.URL.revokeObjectURL(url);
                      document.body.removeChild(a);
                    } catch (err) {
                      console.error('Download error:', err);
                      setError('Failed to download stego image. Please try again.');
                    }
                  }}
                >
                  <Download className="w-5 h-5 mr-2" />
                  Download Stego Image
                </Button>
                <Button
                  variant="secondary"
                  onClick={() => {
                    setShowSuccess(false);
                    setFile(null);
                    setPassword('');
                    setMessage('');
                    setEncryptionData(null);
                    setStegoData(null);
                    encryptionService.clearEncryptionData();
                  }}
                >
                  Hide Another Message
                </Button>
              </div>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default HideMessage;
