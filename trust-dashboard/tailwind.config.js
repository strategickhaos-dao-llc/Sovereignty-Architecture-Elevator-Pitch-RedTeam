/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'dao-primary': '#6366f1',
        'dao-secondary': '#22c55e',
        'dao-accent': '#f59e0b',
        'dao-charity': '#10b981',
        'dao-operations': '#3b82f6',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'counter': 'counter 2s ease-out forwards',
      },
    },
  },
  plugins: [],
}
