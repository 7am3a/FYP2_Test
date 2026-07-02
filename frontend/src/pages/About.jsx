import React from 'react';
import { Lock, Shield, FileImage, Film, CheckCircle, Cpu, Database, Code, Key, Eye, QrCode } from 'lucide-react';
import { motion } from 'framer-motion';
import Card from '../components/ui/Card';

const About = () => {
  const technologies = [
    {
      icon: Lock,
      title: 'AES-256-GCM',
      description: 'Military-grade authenticated encryption with 256-bit keys',
      color: 'accent-primary',
    },
    {
      icon: Key,
      title: 'Argon2id',
      description: 'Memory-hard key derivation function for password hashing',
      color: 'btn-to',
    },
    {
      icon: Eye,
      title: 'Edge-Based LSB',
      description: 'Advanced steganography hiding data in edge pixels',
      color: 'success',
    },
    {
      icon: Film,
      title: 'Randomized Frame LSB',
      description: 'Video steganography with randomized frame selection',
      color: 'accent-secondary',
    },
    {
      icon: FileImage,
      title: 'Audio LSB',
      description: 'Audio steganography for secure voice message hiding',
      color: 'warning',
    },
    {
      icon: QrCode,
      title: 'QR Secure Sharing',
      description: 'QR code generation for secure key distribution',
      color: 'danger',
    },
    {
      icon: Shield,
      title: 'Platform Verification',
      description: 'Cross-platform integrity verification system',
      color: 'text-secondary',
    },
  ];

  const techStack = [
    {
      icon: Code,
      title: 'Frontend',
      items: ['React 18', 'Tailwind CSS', 'Framer Motion', 'Lucide Icons'],
    },
    {
      icon: Cpu,
      title: 'Backend',
      items: ['Node.js', 'Express', 'Python', 'OpenCV'],
    },
    {
      icon: Database,
      title: 'Database',
      items: ['PostgreSQL', 'MongoDB', 'Redis'],
    },
  ];

  return (
    <div className="min-h-screen bg-bg-primary pt-24 pb-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-[1400px] mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold text-text-primary mb-4">
            About SecureStego
          </h1>
          <p className="text-text-secondary text-lg max-w-2xl mx-auto">
            Advanced encryption and steganography for secure message hiding in images, videos, and audio files
          </p>
        </motion.div>

        {/* Technologies Grid */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-text-primary text-center mb-8">
            Core Technologies
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {technologies.map((tech, index) => (
              <motion.div
                key={tech.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
              >
                <Card className="p-6 h-full">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="w-10 h-10 rounded-xl bg-card-secondary border border-border-primary flex items-center justify-center">
                      <tech.icon className="w-5 h-5 text-accent-primary" />
                    </div>
                    <h3 className="text-base font-semibold text-text-primary">
                      {tech.title}
                    </h3>
                  </div>
                  <p className="text-text-muted text-sm leading-relaxed">
                    {tech.description}
                  </p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Technology Stack */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-text-primary text-center mb-8">
            Technology Stack
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {techStack.map((stack, index) => (
              <motion.div
                key={stack.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="p-6 h-full">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-10 h-10 rounded-xl bg-card-secondary border border-border-primary flex items-center justify-center">
                      <stack.icon className="w-5 h-5 text-accent-secondary" />
                    </div>
                    <h3 className="text-lg font-semibold text-text-primary">
                      {stack.title}
                    </h3>
                  </div>
                  <ul className="space-y-2">
                    {stack.items.map((item, i) => (
                      <li key={i} className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-success flex-shrink-0" />
                        <span className="text-text-muted text-sm">{item}</span>
                      </li>
                    ))}
                  </ul>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Privacy Section */}
        <Card className="text-center p-8 border-success/30">
          <motion.div
            initial={{ scale: 0 }}
            whileInView={{ scale: 1 }}
            viewport={{ once: true }}
            transition={{ type: "spring", stiffness: 200 }}
            className="w-20 h-20 mx-auto mb-6 rounded-full bg-success/20 flex items-center justify-center"
          >
            <Shield className="w-10 h-10 text-success" />
          </motion.div>
          <h2 className="text-2xl font-bold text-text-primary mb-4">
            Your Privacy Matters
          </h2>
          <p className="text-text-secondary max-w-2xl mx-auto mb-6">
            SecureStego processes all data locally in your browser. No files or messages are ever sent to any server. 
            Your secrets stay with you - always.
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            <div className="status-success">
              <CheckCircle className="w-3.5 h-3.5 inline mr-2" />
              No Server Storage
            </div>
            <div className="status-success">
              <CheckCircle className="w-3.5 h-3.5 inline mr-2" />
              Local Processing
            </div>
            <div className="status-success">
              <CheckCircle className="w-3.5 h-3.5 inline mr-2" />
              Zero Data Collection
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default About;
