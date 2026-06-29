import React from 'react';
import { Mail, Github, Linkedin, Send, MapPin, Phone } from 'lucide-react';
import { motion } from 'framer-motion';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Textarea from '../components/ui/Textarea';

const Contact = () => {
  return (
    <div className="min-h-screen bg-cyber-gradient pt-24 pb-20 px-4 sm:px-6 lg:px-8">
      {/* Background Effects */}
      <div className="absolute inset-0 glow-gradient opacity-20" />
      <div className="absolute bottom-40 left-20 w-96 h-96 bg-cyber-accent/10 rounded-full blur-3xl" />
      
      <div className="relative z-10 max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gradient mb-4">
            Contact Us
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Have questions about SecureStego? We'd love to hear from you.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Information */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-6"
          >
            <Card className="p-6">
              <h2 className="text-2xl font-bold text-white mb-6">Get in Touch</h2>
              <p className="text-gray-400 mb-8">
                Whether you have questions about the project, want to report a bug, or just want to say hello, feel free to reach out.
              </p>

              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 rounded-xl bg-cyber-accent/20 flex items-center justify-center flex-shrink-0">
                    <Mail className="w-6 h-6 text-cyber-accent" />
                  </div>
                  <div>
                    <h3 className="text-white font-semibold mb-1">Email</h3>
                    <p className="text-gray-400">contact@securestego.com</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 rounded-xl bg-cyber-purple/20 flex items-center justify-center flex-shrink-0">
                    <Github className="w-6 h-6 text-cyber-purple" />
                  </div>
                  <div>
                    <h3 className="text-white font-semibold mb-1">GitHub</h3>
                    <p className="text-gray-400">github.com/securestego</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 rounded-xl bg-cyber-pink/20 flex items-center justify-center flex-shrink-0">
                    <Linkedin className="w-6 h-6 text-cyber-pink" />
                  </div>
                  <div>
                    <h3 className="text-white font-semibold mb-1">LinkedIn</h3>
                    <p className="text-gray-400">linkedin.com/company/securestego</p>
                  </div>
                </div>
              </div>
            </Card>

            {/* Social Links */}
            <Card className="p-6">
              <h3 className="text-white font-semibold mb-4">Follow Us</h3>
              <div className="flex space-x-4">
                {[
                  { icon: Github, color: 'cyber-purple', label: 'GitHub' },
                  { icon: Linkedin, color: 'cyber-pink', label: 'LinkedIn' },
                  { icon: Mail, color: 'cyber-accent', label: 'Email' },
                ].map((social) => (
                  <motion.a
                    key={social.label}
                    href="#"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-12 h-12 rounded-xl glass flex items-center justify-center hover:bg-white/10 transition-colors group"
                  >
                    <social.icon className={`w-6 h-6 text-gray-400 group-hover:text-${social.color} transition-colors`} />
                  </motion.a>
                ))}
              </div>
            </Card>
          </motion.div>

          {/* Contact Form */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card className="p-6">
              <h2 className="text-2xl font-bold text-white mb-6">Send a Message</h2>
              
              <form className="space-y-6">
                <Input
                  label="Your Name"
                  placeholder="John Doe"
                />
                
                <Input
                  label="Email Address"
                  type="email"
                  placeholder="john@example.com"
                />
                
                <Input
                  label="Subject"
                  placeholder="How can we help?"
                />
                
                <Textarea
                  label="Message"
                  placeholder="Type your message here..."
                  rows={6}
                />
                
                <Button className="w-full flex items-center justify-center space-x-2">
                  <Send className="w-5 h-5" />
                  <span>Send Message</span>
                </Button>
              </form>
            </Card>
          </motion.div>
        </div>

        {/* Project Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="mt-16"
        >
          <Card className="text-center p-8 border-cyber-accent/30">
            <h2 className="text-2xl font-bold text-white mb-4">
              Final Year Project
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto mb-6">
              SecureStego is developed as a Final Year Project to demonstrate the practical application of 
              cryptography and steganography in modern cybersecurity.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <div className="glass px-4 py-2 rounded-full text-sm text-gray-300">
                React
              </div>
              <div className="glass px-4 py-2 rounded-full text-sm text-gray-300">
                Tailwind CSS
              </div>
              <div className="glass px-4 py-2 rounded-full text-sm text-gray-300">
                AES-256 Encryption
              </div>
              <div className="glass px-4 py-2 rounded-full text-sm text-gray-300">
                LSB Steganography
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  );
};

export default Contact;
