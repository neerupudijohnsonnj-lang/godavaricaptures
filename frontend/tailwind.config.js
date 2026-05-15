/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'luxury-black': '#000000',
        'luxury-card': '#0A0A0A',
        'luxury-alt': '#050505',
        'luxury-gold': '#D4AF37',
        'luxury-gold-hover': '#C5A017',
      },
      fontFamily: {
        'display': ['Playfair Display', 'serif'],
        'body': ['Manrope', 'sans-serif'],
      },
      borderRadius: {
        'none': '0',
      },
    },
  },
  plugins: [],
}
