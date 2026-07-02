import React from 'react';
import { Shield, Heart } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="glass border-t border-border-primary mt-20">
      <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Brand */}
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Shield className="w-8 h-8 text-accent-primary" />
              <span className="text-xl font-bold text-gradient">SecureStego</span>
            </div>
            <p className="text-text-secondary text-sm">
              Securely hide encrypted messages inside images and videos using advanced steganography techniques.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-3">
            <h3 className="text-text-primary font-semibold">Quick Links</h3>
            <ul className="space-y-2 text-sm text-text-muted">
              <li><a href="/hide" className="hover:text-accent-primary transition-colors">Hide Message</a></li>
              <li><a href="/extract" className="hover:text-accent-primary transition-colors">Extract Message</a></li>
              <li><a href="/about" className="hover:text-accent-primary transition-colors">About</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-border-primary mt-6 pt-6 flex flex-col md:flex-row justify-between items-center space-y-3 md:space-y-0">
          <p className="text-text-muted text-sm">
            © 2026 SecureStego. All rights reserved.
          </p>
          <p className="text-text-muted text-sm flex items-center space-x-1">
            Made with <Heart className="w-4 h-4 text-accent-primary fill-current" /> for Final Year Project
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
