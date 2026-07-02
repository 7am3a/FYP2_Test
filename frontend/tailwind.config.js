/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Background colors
        bg: {
          primary: '#070B12',
          secondary: '#0E131B',
          tertiary: '#0A1628',
        },
        // Card colors
        card: {
          primary: '#0F172A',
          secondary: '#1B2234',
          tertiary: '#182235',
        },
        // Accent colors
        accent: {
          primary: '#00E5C2',
          secondary: '#00BFA5',
          hover: '#29F0C0',
        },
        // Status colors
        success: '#00E5C2',
        warning: '#FFC857',
        danger: '#FF5D73',
        // Text colors
        text: {
          primary: '#F5F7FA',
          secondary: '#94A3B8',
          muted: '#6D7788',
        },
        // Border colors
        border: {
          primary: 'rgba(0, 245, 195, 0.12)',
          secondary: 'rgba(0, 245, 195, 0.35)',
        },
      },
      backgroundImage: {
        'cyber-gradient': 'linear-gradient(135deg, #06090F 0%, #0E131B 50%, #0A1628 100%)',
      },
      boxShadow: {
        'glow': '0 0 20px rgba(0, 245, 195, 0.15)',
        'glow-hover': '0 0 30px rgba(0, 245, 195, 0.35)',
        'card': '0 4px 24px rgba(0, 0, 0, 0.3)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      }
    },
  },
  plugins: [],
}
