/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: '#0a0e1a',
        surface: '#111827',
        danger: '#ef4444',
        info: '#3b82f6',
        success: '#10b981',
        warning: '#f59e0b',
        textPrimary: '#f1f5f9',
        textSecondary: '#94a3b8',
      },
      animation: {
        pulseBorder: 'pulseBorder 2s ease-in-out infinite',
        needle: 'needle 1s ease-out forwards',
      },
      keyframes: {
        pulseBorder: {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(239, 68, 68, 0.4)' },
          '50%': { boxShadow: '0 0 0 8px rgba(239, 68, 68, 0)' },
        },
        needle: {
          from: { transform: 'rotate(-90deg)' },
          to: { transform: 'rotate(var(--needle-rotation))' },
        },
      },
    },
  },
  plugins: [],
}
