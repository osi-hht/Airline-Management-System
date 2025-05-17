/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['../templates/**/*.html'],
  theme: {
    extend: {
      colors: {
        'airline-blue': {
          50: '#f0f4fa',
          100: '#dce7f5',
          200: '#c0d4ed',
          300: '#94b6e0',
          400: '#6391d0',
          500: '#4271c2',
          600: '#3458a6',
          700: '#2c4787',
          800: '#293d6f',
          900: '#1a2544',
          950: '#111731',
        },
        'airline-gold': {
          50: '#fdf8ed',
          100: '#f9edd1',
          200: '#f3daa5',
          300: '#ecc06e',
          400: '#e6a944',
          500: '#da8f2a',
          600: '#c0701d',
          700: '#9f521c',
          800: '#83421d',
          900: '#6c371b',
          950: '#3e1d0c',
        },
        'airline-gray': {
          50: '#f7f8f9',
          100: '#eef0f2',
          200: '#d9dde3',
          300: '#b9c0cb',
          400: '#949eaf',
          500: '#768296',
          600: '#5f6a7e',
          700: '#4d5667',
          800: '#434a58',
          900: '#3a3f4a',
          950: '#25282f',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Montserrat', 'sans-serif'],
      },
      boxShadow: {
        'airline': '0 4px 20px rgba(0, 0, 0, 0.08)',
        'airline-lg': '0 10px 30px rgba(0, 0, 0, 0.1)',
      },
      backgroundImage: {
        'hero-pattern': "url('https://images.pexels.com/photos/2026324/pexels-photo-2026324.jpeg?auto=compress&cs=tinysrgb&w=1600')",
        'about-pattern': "url('https://images.pexels.com/photos/62623/wing-plane-flying-airplane-62623.jpeg?auto=compress&cs=tinysrgb&w=1600')",
        'service-pattern': "url('https://images.pexels.com/photos/1309644/pexels-photo-1309644.jpeg?auto=compress&cs=tinysrgb&w=1600')",
      },
    },
  },
  plugins: [],
};