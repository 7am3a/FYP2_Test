import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Lock, Eye, ArrowRight, ShieldCheck, LockKeyhole } from 'lucide-react';
import { motion } from 'framer-motion';
import Button from '../components/ui/Button';

const Landing = () => {
  return (
    <div className="min-h-screen bg-bg-primary">
      {/* Hero Section */}
      <div className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-[1400px] mx-auto">
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
                <ShieldCheck className="w-5 h-5 text-success" />
                <span className="text-sm text-text-secondary">Military-Grade Encryption</span>
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
                className="text-xl md:text-2xl text-text-secondary leading-relaxed"
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
                  <div className="text-3xl font-bold text-accent-primary">256</div>
                  <div className="text-sm text-text-muted">AES Encryption</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-accent-secondary">LSB</div>
                  <div className="text-sm text-text-muted">Steganography</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-success">100%</div>
                  <div className="text-sm text-text-muted">Secure</div>
                </div>
              </motion.div>
            </motion.div>

            {/* Right Content - Illustration */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="flex justify-center items-center"
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
                  className="flex justify-center"
                >
                  <div className="relative">
                    <Shield className="w-64 h-64 text-accent-primary shadow-glow" />
                    <LockKeyhole className="w-32 h-32 text-accent-secondary absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
                  </div>
                </motion.div>

                {/* Floating Elements */}
                <motion.div
                  animate={{ y: [0, -20, 0] }}
                  transition={{ duration: 3, repeat: Infinity }}
                  className="absolute top-10 right-10 glass p-4 rounded-xl"
                >
                  <Lock className="w-8 h-8 text-success" />
                </motion.div>

                <motion.div
                  animate={{ y: [0, 20, 0] }}
                  transition={{ duration: 3, repeat: Infinity, delay: 0.5 }}
                  className="absolute bottom-10 left-10 glass p-4 rounded-xl"
                >
                  <Eye className="w-8 h-8 text-danger" />
                </motion.div>

                <motion.div
                  animate={{ y: [0, -15, 0] }}
                  transition={{ duration: 2.5, repeat: Infinity, delay: 1 }}
                  className="absolute top-1/2 -right-5 glass p-4 rounded-xl"
                >
                  <ShieldCheck className="w-8 h-8 text-accent-primary" />
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
        className="px-4 sm:px-6 lg:px-8 pb-20"
      >
        <div className="max-w-[1400px] mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gradient mb-4">
              Security Dashboard
            </h2>
            <p className="text-text-secondary text-lg">
              Real-time security metrics and encryption status
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { icon: LockKeyhole, label: 'Encryption', value: 'AES-256', color: 'accent-primary' },
              { icon: Shield, label: 'Hidden Data', value: '0 KB', color: 'accent-secondary' },
              { icon: Eye, label: 'File Size', value: '0 MB', color: 'danger' },
              { icon: ShieldCheck, label: 'Security', value: 'Active', color: 'success' },
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="glass-card p-6 hover:border-border-secondary transition-all duration-300 group"
              >
                <stat.icon className={`w-8 h-8 text-${stat.color} mb-4 group-hover:scale-110 transition-transform`} />
                <div className="text-2xl font-bold text-text-primary mb-1">{stat.value}</div>
                <div className="text-text-muted text-sm">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Landing;
