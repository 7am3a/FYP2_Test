import React from 'react';
import { motion } from 'framer-motion';

const Button = ({ children, variant = 'primary', className = '', ...props }) => {
  const baseStyles = 'font-semibold px-8 py-3 rounded-xl transition-all duration-300 transform hover:scale-105';
  
  const variants = {
    primary: 'bg-gradient-to-r from-cyber-accent to-cyber-purple text-cyber-darker cyber-glow hover:opacity-90',
    secondary: 'glass text-white border border-cyber-accent/30 hover:bg-white/10',
    outline: 'border-2 border-cyber-accent text-cyber-accent hover:bg-cyber-accent/10',
    danger: 'bg-gradient-to-r from-red-500 to-pink-500 text-white hover:opacity-90',
  };

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`${baseStyles} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </motion.button>
  );
};

export default Button;
