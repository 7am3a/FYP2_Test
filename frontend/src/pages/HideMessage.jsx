import React, { useState } from 'react';
import { Lock, Shield, CheckCircle, Download, AlertCircle, HardDrive, FileText, Image as ImageIcon } from 'lucide-react';
import { motion } from 'framer-motion';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import FileUpload from '../components/ui/FileUpload';
import PasswordInput from '../components/ui/PasswordInput';
import Textarea from '../components/ui/Textarea';
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

  return (
    <div className="min-h-screen bg-cyber-gradient pt-24 pb-20 px-4 sm:px-6 lg:px-8">
      {/* Background Effects */}
      <div className="absolute inset-0 glow-gradient opacity-20" />
      <div className="absolute top-40 right-20 w-96 h-96 bg-cyber-purple/10 rounded-full blur-3xl" />
      
      <div className="relative z-10 max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gradient mb-4">
            Hide Secret Message
          </h1>
          <p className="text-gray-400 text-lg">
            Encrypt and hide your message securely inside an image or video
          </p>
        </motion.div>

        {!showSuccess ? (
          <div className="space-y-6">
            {/* Step 1: File Upload */}
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
                  <h2 className="text-xl font-semibold text-white">Upload File</h2>
                </div>
                <FileUpload
                  onFileSelect={setFile}
                  label="Select an image or video file"
                />
              </Card>
            </motion.div>

            {/* Step 2: Password */}
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
                  <h2 className="text-xl font-semibold text-white">Set Password</h2>
                </div>
                <PasswordInput
                  label="Enter encryption password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter a strong password"
                />
                
                {/* Password Strength Indicator */}
                <div className="mt-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm text-gray-400">Password Strength</span>
                    <span className={`text-sm font-medium text-${strength.color}`}>
                      {strength.label}
                    </span>
                  </div>
                  <div className="flex space-x-1">
                    {[1, 2, 3, 4].map((i) => (
                      <div
                        key={i}
                        className={`h-2 flex-1 rounded-full transition-all duration-300 ${
                          i <= strength.score
                            ? `bg-${strength.color === 'cyber-green' ? 'cyber-green' : strength.color}`
                            : 'bg-white/10'
                        }`}
                      />
                    ))}
                  </div>
                </div>
              </Card>
            </motion.div>

            {/* Step 3: Secret Message */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Card className="card-step">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-10 h-10 rounded-full bg-cyber-pink/20 flex items-center justify-center">
                    <span className="text-cyber-pink font-bold">3</span>
                  </div>
                  <h2 className="text-xl font-semibold text-white">Secret Message</h2>
                </div>
                <Textarea
                  label="Enter your secret message"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Type your confidential message here..."
                  rows={6}
                />
                <div className="flex justify-between items-center mt-2">
                  <span className="text-sm text-gray-400">
                    {message.length} / 10000 characters
                  </span>
                  <span className="text-sm text-cyber-green">
                    Capacity: ~{(file ? (file.size / 1024).toFixed(0) : '0')} KB available
                  </span>
                </div>
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

            {/* Step 5: Encrypt Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex justify-center"
            >
              <Button
                onClick={handleEncrypt}
                disabled={!password || !message || isProcessing}
                className="w-full md:w-auto px-12 py-4 text-lg"
              >
                {isProcessing ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      className="mr-2"
                    >
                      <Lock className="w-5 h-5" />
                    </motion.div>
                    Encrypting...
                  </>
                ) : (
                  <>
                    <Lock className="w-5 h-5 mr-2" />
                    Encrypt Message
                  </>
                )}
              </Button>
            </motion.div>

          </div>
        ) : (
          /* Success Result Section */
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
                Message Hidden Successfully!
              </h2>
              
              <p className="text-gray-400 mb-8 max-w-md mx-auto">
                Your secret message has been encrypted and securely hidden inside the file. 
                The file is ready for download.
              </p>

              <div className="glass p-6 rounded-xl mb-8 max-w-md mx-auto">
                <div className="flex items-center justify-center space-x-3 mb-4">
                  <ImageIcon className="w-8 h-8 text-cyber-accent" />
                  <span className="text-white font-medium">Message Hidden Successfully</span>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="text-gray-400">Algorithm</div>
                    <div className="text-white font-medium">{encryptionData?.encryptionAlgorithm || 'AES-256-GCM'}</div>
                  </div>
                  <div>
                    <div className="text-gray-400">KDF</div>
                    <div className="text-white font-medium">{encryptionData?.keyDerivationFunction || 'Argon2id'}</div>
                  </div>
                  <div>
                    <div className="text-gray-400">Message Length</div>
                    <div className="text-white font-medium">{message.length} chars</div>
                  </div>
                  <div>
                    <div className="text-gray-400">Processing Time</div>
                    <div className="text-white font-medium">{stegoData?.processingTime || 'N/A'}s</div>
                  </div>
                  <div>
                    <div className="text-gray-400">Original Format</div>
                    <div className="text-white font-medium">{stegoData?.originalFormat || 'N/A'}</div>
                  </div>
                  <div>
                    <div className="text-gray-400">Edge Pixels</div>
                    <div className="text-white font-medium">{stegoData?.statistics?.edgePixels || 'N/A'}</div>
                  </div>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
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
