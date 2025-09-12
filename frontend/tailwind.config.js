/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cyber-dark': '#0a0a0a',
        'cyber-darker': '#050505',
        'cyber-blue': '#00d4ff',
        'cyber-purple': '#8b5cf6',
        'cyber-green': '#00ff88',
        'cyber-pink': '#ff0080',
        'cyber-yellow': '#ffff00',
        'cyber-gray': '#2a2a2a',
        'cyber-light-gray': '#4a4a4a',
      },
      fontFamily: {
        'mono': ['Fira Code', 'Roboto Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px #00d4ff' },
          '100%': { boxShadow: '0 0 20px #00d4ff, 0 0 30px #00d4ff' },
        }
      },
      boxShadow: {
        'cyber': '0 0 10px rgba(0, 212, 255, 0.5)',
        'cyber-strong': '0 0 20px rgba(0, 212, 255, 0.8)',
      }
    },
  },
  plugins: [],
}