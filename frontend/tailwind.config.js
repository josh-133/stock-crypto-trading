/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom colors for trading UI
        profit: '#10b981',      // Green for gains
        loss: '#ef4444',        // Red for losses
        neutral: '#6b7280',     // Gray for neutral
        buy: '#3b82f6',         // Blue for buy signals
        sell: '#f59e0b',        // Orange for sell signals
      },
    },
  },
  plugins: [],
}
