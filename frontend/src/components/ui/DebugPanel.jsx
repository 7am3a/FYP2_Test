import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Copy, CheckCircle, XCircle, Clock, Shield, Lock, Database } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const DebugPanel = ({ data, isOpen: defaultOpen = false }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const [copiedField, setCopiedField] = useState(null);

  const copyToClipboard = (text, field) => {
    navigator.clipboard.writeText(text);
    setCopiedField(field);
    setTimeout(() => setCopiedField(null), 2000);
  };

  if (!data) {
    return null;
  }

  const debugItems = [
    {
      label: 'Original Message',
      value: data.originalMessage || 'N/A',
      icon: <Database className="w-4 h-4" />,
      copyable: true,
      field: 'originalMessage'
    },
    {
      label: 'Password Length',
      value: data.passwordLength !== undefined ? `${data.passwordLength} characters` : 'N/A',
      icon: <Lock className="w-4 h-4" />,
      copyable: false
    },
    {
      label: 'Generated Salt',
      value: data.generatedSalt || 'N/A',
      icon: <Shield className="w-4 h-4" />,
      copyable: true,
      field: 'salt',
      truncate: true
    },
    {
      label: 'Generated IV',
      value: data.generatedIV || 'N/A',
      icon: <Lock className="w-4 h-4" />,
      copyable: true,
      field: 'iv',
      truncate: true
    },
    {
      label: 'Encryption Algorithm',
      value: data.encryptionAlgorithm || 'N/A',
      icon: <Shield className="w-4 h-4" />,
      copyable: false
    },
    {
      label: 'Key Derivation Function',
      value: data.keyDerivationFunction || 'N/A',
      icon: <Lock className="w-4 h-4" />,
      copyable: false
    },
    {
      label: 'Encrypted Output',
      value: data.encryptedOutput || 'N/A',
      icon: <Database className="w-4 h-4" />,
      copyable: true,
      field: 'ciphertext',
      truncate: true
    },
    {
      label: 'Backend Response',
      value: data.backendResponse ? JSON.stringify(data.backendResponse, null, 2) : 'N/A',
      icon: <Database className="w-4 h-4" />,
      copyable: true,
      field: 'backendResponse',
      isJson: true
    },
    {
      label: 'API Status',
      value: data.apiStatus || 'Success',
      icon: data.apiStatus === 'Success' ? <CheckCircle className="w-4 h-4 text-cyber-green" /> : <XCircle className="w-4 h-4 text-red-500" />,
      copyable: false
    },
    {
      label: 'Processing Time',
      value: data.processingTime ? `${data.processingTime}s` : 'N/A',
      icon: <Clock className="w-4 h-4" />,
      copyable: false
    }
  ];

  return (
    <div className="mt-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="border-2 border-yellow-500/30 rounded-2xl overflow-hidden"
      >
        {/* Header */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full px-6 py-4 bg-yellow-500/10 hover:bg-yellow-500/20 transition-colors flex items-center justify-between"
        >
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-full bg-yellow-500/20 flex items-center justify-center">
              <Shield className="w-4 h-4 text-yellow-500" />
            </div>
            <div className="text-left">
              <h3 className="text-yellow-500 font-bold text-lg">Encryption Debug Panel</h3>
              <p className="text-yellow-500/70 text-xs">FOR DEVELOPMENT AND TESTING ONLY</p>
            </div>
          </div>
          {isOpen ? <ChevronUp className="w-5 h-5 text-yellow-500" /> : <ChevronDown className="w-5 h-5 text-yellow-500" />}
        </button>

        {/* Content */}
        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="p-6 bg-black/30 space-y-3">
                {debugItems.map((item, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
                    <div className="flex-shrink-0 mt-0.5 text-cyber-accent">
                      {item.icon}
                    </div>
                    <div className="flex-grow min-w-0">
                      <div className="text-xs text-gray-400 mb-1">{item.label}</div>
                      <div className="text-sm text-white font-mono break-all">
                        {item.isJson ? (
                          <pre className="text-xs text-gray-300 whitespace-pre-wrap overflow-x-auto">
                            {item.value}
                          </pre>
                        ) : item.truncate && item.value.length > 100 ? (
                          <span title={item.value}>{item.value.substring(0, 100)}...</span>
                        ) : (
                          item.value
                        )}
                      </div>
                    </div>
                    {item.copyable && (
                      <button
                        onClick={() => copyToClipboard(item.value, item.field)}
                        className="flex-shrink-0 p-2 rounded-lg hover:bg-white/10 transition-colors group"
                        title="Copy to clipboard"
                      >
                        {copiedField === item.field ? (
                          <CheckCircle className="w-4 h-4 text-cyber-green" />
                        ) : (
                          <Copy className="w-4 h-4 text-gray-400 group-hover:text-white" />
                        )}
                      </button>
                    )}
                  </div>
                ))}

                {data.timestamp && (
                  <div className="pt-3 border-t border-white/10">
                    <div className="text-xs text-gray-500 flex items-center space-x-2">
                      <Clock className="w-3 h-3" />
                      <span>Timestamp: {new Date(data.timestamp).toLocaleString()}</span>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
};

export default DebugPanel;
