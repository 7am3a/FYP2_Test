import React from 'react';
import { motion } from 'framer-motion';

const Button = ({ children, variant = 'primary', className = '', ...props }) => {
  const baseStyles = 'font-semibold px-6 py-3 rounded-xl transition-all duration-300 flex items-center justify-center';
  
  const variants = {
    primary: 'bg-gradient-to-r from-accent-primary to-accent-secondary text-white hover:opacity-90 shadow-glow hover:shadow-glow-hover',
    secondary: 'glass text-text-primary border border-border-primary hover:bg-white/5',
    outline: 'border-2 border-accent-primary text-accent-primary hover:bg-accent-primary/10',
    danger: 'bg-danger/10 border border-danger text-danger hover:bg-danger/20',
  };

  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={`${baseStyles} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </motion.button>
  );
};

export default Button;
