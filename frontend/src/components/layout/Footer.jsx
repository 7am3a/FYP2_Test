import React from 'react';
import { Shield, Github, Mail, Heart } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="glass border-t border-white/10 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Shield className="w-8 h-8 text-cyber-accent" />
              <span className="text-xl font-bold text-gradient">SecureStego</span>
            </div>
            <p className="text-gray-400 text-sm">
              Securely hide encrypted messages inside images and videos using advanced steganography techniques.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-white font-semibold">Quick Links</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="/hide" className="hover:text-cyber-accent transition-colors">Hide Message</a></li>
              <li><a href="/extract" className="hover:text-cyber-accent transition-colors">Extract Message</a></li>
              <li><a href="/about" className="hover:text-cyber-accent transition-colors">About</a></li>
              <li><a href="/contact" className="hover:text-cyber-accent transition-colors">Contact</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div className="space-y-4">
            <h3 className="text-white font-semibold">Connect</h3>
            <div className="flex space-x-4">
              <a
                href="#"
                className="p-2 rounded-lg glass hover:bg-white/10 transition-colors group"
              >
                <Github className="w-5 h-5 text-gray-400 group-hover:text-cyber-accent" />
              </a>
              <a
                href="#"
                className="p-2 rounded-lg glass hover:bg-white/10 transition-colors group"
              >
                <Mail className="w-5 h-5 text-gray-400 group-hover:text-cyber-accent" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-white/10 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <p className="text-gray-500 text-sm">
            © 2024 SecureStego. All rights reserved.
          </p>
          <p className="text-gray-500 text-sm flex items-center space-x-1">
            Made with <Heart className="w-4 h-4 text-cyber-pink fill-current" /> for Final Year Project
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
