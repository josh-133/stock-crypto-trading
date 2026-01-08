# Frontend - Vue 3 Trading Platform

## Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── main.js              # Vue entry point
│   ├── App.vue              # Root component
│   ├── router/              # Vue Router
│   ├── stores/              # Pinia stores
│   ├── composables/         # Composable functions
│   ├── components/          # Vue components
│   │   ├── layout/          # Navbar, Sidebar
│   │   ├── dashboard/       # Dashboard widgets
│   │   ├── charts/          # Chart components
│   │   ├── trading/         # Trading UI
│   │   └── backtest/        # Backtest UI
│   └── views/               # Page views
├── index.html
└── package.json
```

## Views

- **Dashboard** (`/`) - Portfolio overview and signals
- **Trading** (`/trading`) - Execute trades and manage positions
- **Backtest** (`/backtest`) - Test strategy on historical data
- **Settings** (`/settings`) - Reset portfolio and view strategy info
