/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#0a0a0f',
          surface: '#151520',
          border: '#252535',
          text: '#e0e0e0',
          accent: '#6366f1',
        }
      }
    },
  },
  plugins: [],
}







