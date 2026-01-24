/** @type {import('tailwindcss').Config} */
const path = require('path');

module.exports = {
    content: [
        path.join(__dirname, 'furfeast/templates/**/*.html'),
        path.join(__dirname, 'furfeast/static/js/**/*.js'),
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: '#d4a23f',
                    foreground: '#ffffff',
                    light: '#fff7ed',
                    dark: '#b8912e',
                },
                secondary: {
                    DEFAULT: '#10b981',
                    foreground: '#ffffff',
                },
                accent: {
                    DEFAULT: '#f43f5e',
                },
                background: '#3A5A40',
                foreground: '#ffffff',
                card: '#ffffff',
                border: '#e2e8f0',
                muted: {
                    DEFAULT: '#f1f5f9',
                    foreground: '#d9d9d9',
                }
            },
            fontFamily: {
                heading: ['Nunito', 'sans-serif'],
                body: ['Inter', 'sans-serif'],
            },
            animation: {
                'slide-up': 'slide-up 0.5s ease-out forwards',
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'float': 'float 3s ease-in-out infinite',
            },
            keyframes: {
                'slide-up': {
                    '0%': { transform: 'translateY(20px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
                'float': {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                }
            }
        }
    },
    plugins: [],
}
