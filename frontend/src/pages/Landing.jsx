import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Lock, Eye, ArrowRight, ShieldCheck, LockKeyhole } from 'lucide-react';
import { motion } from 'framer-motion';
import Button from '../components/ui/Button';

const Landing = () => {
  return (
    <div className="min-h-screen bg-cyber-gradient relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 glow-gradient opacity-30" />
      <div className="absolute top-20 left-10 w-72 h-72 bg-cyber-purple/20 rounded-full blur-3xl animate-pulse-slow" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-cyber-accent/20 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '2s' }} />
      
      {/* Hero Section */}
      <div className="relative z-10 pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="space-y-8"
            >
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="inline-flex items-center space-x-2 glass px-4 py-2 rounded-full"
              >
                <ShieldCheck className="w-5 h-5 text-cyber-green" />
                <span className="text-sm text-gray-300">Military-Grade Encryption</span>
              </motion.div>

              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="text-5xl md:text-7xl font-bold leading-tight"
              >
                <span className="text-gradient">SecureStego</span>
              </motion.h1>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="text-xl md:text-2xl text-gray-300 leading-relaxed"
              >
                Hide encrypted messages inside images and videos securely.
              </motion.p>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="flex flex-col sm:flex-row gap-4"
              >
                <Link to="/hide">
                  <Button className="w-full sm:w-auto flex items-center justify-center space-x-2">
                    <Lock className="w-5 h-5" />
                    <span>Hide Message</span>
                    <ArrowRight className="w-5 h-5" />
                  </Button>
                </Link>
                <Link to="/extract">
                  <Button variant="secondary" className="w-full sm:w-auto flex items-center justify-center space-x-2">
                    <Eye className="w-5 h-5" />
                    <span>Extract Message</span>
                  </Button>
                </Link>
              </motion.div>

              {/* Features */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="grid grid-cols-3 gap-4 pt-8"
              >
                <div className="text-center">
                  <div className="text-3xl font-bold text-cyber-accent">256</div>
                  <div className="text-sm text-gray-400">AES Encryption</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-cyber-purple">LSB</div>
                  <div className="text-sm text-gray-400">Steganography</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-cyber-green">100%</div>
                  <div className="text-sm text-gray-400">Secure</div>
                </div>
              </motion.div>
            </motion.div>

            {/* Right Content - Illustration */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="relative"
            >
              <div className="relative">
                {/* Central Shield */}
                <motion.div
                  animate={{ 
                    rotate: [0, 5, -5, 0],
                    scale: [1, 1.05, 1]
                  }}
                  transition={{ 
                    duration: 4,
                    repeat: Infinity,
                    repeatType: "reverse"
                  }}
                  className="relative z-10 flex justify-center"
                >
                  <div className="relative">
                    <Shield className="w-64 h-64 text-cyber-accent cyber-glow" />
                    <LockKeyhole className="w-32 h-32 text-cyber-purple absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
                  </div>
                </motion.div>

                {/* Floating Elements */}
                <motion.div
                  animate={{ y: [0, -20, 0] }}
                  transition={{ duration: 3, repeat: Infinity }}
                  className="absolute top-10 right-10 glass p-4 rounded-xl"
                >
                  <Lock className="w-8 h-8 text-cyber-green" />
                </motion.div>

                <motion.div
                  animate={{ y: [0, 20, 0] }}
                  transition={{ duration: 3, repeat: Infinity, delay: 0.5 }}
                  className="absolute bottom-10 left-10 glass p-4 rounded-xl"
                >
                  <Eye className="w-8 h-8 text-cyber-pink" />
                </motion.div>

                <motion.div
                  animate={{ y: [0, -15, 0] }}
                  transition={{ duration: 2.5, repeat: Infinity, delay: 1 }}
                  className="absolute top-1/2 -right-5 glass p-4 rounded-xl"
                >
                  <ShieldCheck className="w-8 h-8 text-cyber-accent" />
                </motion.div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Security Dashboard Preview */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
        className="relative z-10 px-4 sm:px-6 lg:px-8 pb-20"
      >
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gradient mb-4">
              Security Dashboard
            </h2>
            <p className="text-gray-400 text-lg">
              Real-time security metrics and encryption status
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { icon: LockKeyhole, label: 'Encryption', value: 'AES-256', color: 'cyber-accent' },
              { icon: Shield, label: 'Hidden Data', value: '0 KB', color: 'cyber-purple' },
              { icon: Eye, label: 'File Size', value: '0 MB', color: 'cyber-pink' },
              { icon: ShieldCheck, label: 'Security', value: 'Active', color: 'cyber-green' },
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="glass-card p-6 hover:border-cyber-accent/30 transition-all duration-300 group"
              >
                <stat.icon className={`w-8 h-8 text-${stat.color} mb-4 group-hover:scale-110 transition-transform`} />
                <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
                <div className="text-gray-400 text-sm">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Landing;
