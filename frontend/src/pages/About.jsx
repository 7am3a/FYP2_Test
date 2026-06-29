import React from 'react';
import { ArrowDown, Lock, Shield, FileImage, Film, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import Card from '../components/ui/Card';

const About = () => {
  const steps = [
    {
      icon: FileText,
      title: 'Secret Message',
      description: 'Enter your confidential message that you want to hide securely',
      color: 'cyber-accent',
    },
    {
      icon: Lock,
      title: 'AES Encryption',
      description: 'Message is encrypted using AES-256 military-grade encryption',
      color: 'cyber-purple',
    },
    {
      icon: Shield,
      title: 'Encrypted Data',
      description: 'Encrypted data is prepared for steganography embedding',
      color: 'cyber-pink',
    },
    {
      icon: FileImage,
      title: 'Steganography',
      description: 'Data is hidden using LSB (Least Significant Bit) technique',
      color: 'cyber-green',
    },
    {
      icon: Film,
      title: 'Image / Video',
      description: 'Final secured file with hidden message ready for sharing',
      color: 'cyber-accent',
    },
  ];

  const features = [
    {
      icon: Lock,
      title: 'Military-Grade Encryption',
      description: 'AES-256 encryption ensures your messages are virtually unbreakable',
    },
    {
      icon: Shield,
      title: 'Advanced Steganography',
      description: 'LSB technique hides data imperceptibly in images and videos',
    },
    {
      icon: CheckCircle,
      title: '100% Secure',
      description: 'No data is stored on servers - everything happens locally',
    },
  ];

  return (
    <div className="min-h-screen bg-cyber-gradient pt-24 pb-20 px-4 sm:px-6 lg:px-8">
      {/* Background Effects */}
      <div className="absolute inset-0 glow-gradient opacity-20" />
      <div className="absolute top-40 right-20 w-96 h-96 bg-cyber-purple/10 rounded-full blur-3xl" />
      
      <div className="relative z-10 max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gradient mb-4">
            How SecureStego Works
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Understand the process of hiding and extracting secret messages using advanced encryption and steganography techniques
          </p>
        </motion.div>

        {/* Process Flow */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold text-white text-center mb-12">
            The Encryption Process
          </h2>
          
          <div className="relative">
            {/* Connection Line */}
            <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-cyber-accent via-cyber-purple to-cyber-green transform -translate-y-1/2 opacity-30" />
            
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
              {steps.map((step, index) => (
                <motion.div
                  key={step.title}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="relative"
                >
                  <Card className="text-center p-6 hover:border-cyber-accent/30 transition-all duration-300 group">
                    <motion.div
                      whileHover={{ scale: 1.1, rotate: 5 }}
                      className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-${step.color}/20 flex items-center justify-center group-hover:bg-${step.color}/30 transition-all"
                    >
                      <step.icon className={`w-8 h-8 text-${step.color}`} />
                    </motion.div>
                    <h3 className="text-lg font-semibold text-white mb-2">
                      {step.title}
                    </h3>
                    <p className="text-gray-400 text-sm">
                      {step.description}
                    </p>
                    
                    {/* Arrow for non-last items */}
                    {index < steps.length - 1 && (
                      <div className="hidden lg:block absolute -right-3 top-1/2 transform -translate-y-1/2 z-10">
                        <ArrowDown className="w-6 h-6 text-cyber-accent rotate-90" />
                      </div>
                    )}
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold text-white text-center mb-12">
            Key Features
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="p-6 hover:border-cyber-accent/30 transition-all duration-300 group">
                  <feature.icon className="w-10 h-10 text-cyber-accent mb-4 group-hover:scale-110 transition-transform" />
                  <h3 className="text-xl font-semibold text-white mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-400">
                    {feature.description}
                  </p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Technical Details */}
        <div className="mb-20">
          <h2 className="text-2xl font-bold text-white text-center mb-12">
            Technical Specifications
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="p-6">
              <h3 className="text-xl font-semibold text-white mb-4 flex items-center space-x-2">
                <Lock className="w-6 h-6 text-cyber-purple" />
                <span>AES-256 Encryption</span>
              </h3>
              <ul className="space-y-3 text-gray-400">
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-5 h-5 text-cyber-green mt-0.5 flex-shrink-0" />
                  <span>256-bit key length for maximum security</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-5 h-5 text-cyber-green mt-0.5 flex-shrink-0" />
                  <span>Government-approved encryption standard</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-5 h-5 text-cyber-green mt-0.5 flex-shrink-0" />
                  <span>Virtually impossible to crack without password</span>
                </li>
              </ul>
            </Card>

            <Card className="p-6">
              <h3 className="text-xl font-semibold text-white mb-4 flex items-center space-x-2">
                <Shield className="w-6 h-6 text-cyber-accent" />
                <span>LSB Steganography</span>
              </h3>
              <ul className="space-y-3 text-gray-400">
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-5 h-5 text-cyber-green mt-0.5 flex-shrink-0" />
                  <span>Modifies least significant bits of pixels</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-5 h-5 text-cyber-green mt-0.5 flex-shrink-0" />
                  <span>Invisible to the human eye</span>
                </li>
                <li className="flex items-start space-x-2">
                  <CheckCircle className="w-5 h-5 text-cyber-green mt-0.5 flex-shrink-0" />
                  <span>Supports both images and videos</span>
                </li>
              </ul>
            </Card>
          </div>
        </div>

        {/* Privacy Section */}
        <Card className="text-center p-8 border-cyber-green/30">
          <motion.div
            initial={{ scale: 0 }}
            whileInView={{ scale: 1 }}
            viewport={{ once: true }}
            transition={{ type: "spring", stiffness: 200 }}
            className="w-20 h-20 mx-auto mb-6 rounded-full bg-cyber-green/20 flex items-center justify-center"
          >
            <Shield className="w-10 h-10 text-cyber-green" />
          </motion.div>
          <h2 className="text-2xl font-bold text-white mb-4">
            Your Privacy Matters
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto mb-6">
            SecureStego processes all data locally in your browser. No files or messages are ever sent to any server. 
            Your secrets stay with you - always.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <div className="glass px-4 py-2 rounded-full text-sm text-gray-300">
              <CheckCircle className="w-4 h-4 inline mr-2 text-cyber-green" />
              No Server Storage
            </div>
            <div className="glass px-4 py-2 rounded-full text-sm text-gray-300">
              <CheckCircle className="w-4 h-4 inline mr-2 text-cyber-green" />
              Local Processing
            </div>
            <div className="glass px-4 py-2 rounded-full text-sm text-gray-300">
              <CheckCircle className="w-4 h-4 inline mr-2 text-cyber-green" />
              Zero Data Collection
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default About;
