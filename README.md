# Stock Trading Platform - Paper Trading Simulator

A beginner-friendly paper trading platform with a 10/50 Moving Average Crossover strategy, built to help you learn how markets behave without risking real money.

## Features

- **Dashboard**: Portfolio overview, signals, and performance metrics
- **Interactive Charts**: Candlestick charts with MA overlays
- **Paper Trading**: $10,000 virtual balance to practice
- **Signal Scanner**: Watch AAPL, MSFT, GOOGL, SPY for crossover signals
- **Backtesting**: Test the strategy on historical data
- **Position Manager**: Track positions with automatic stop-loss

## Strategy Summary

| Rule | Value |
|------|-------|
| Buy Signal | 10-day MA crosses above 50-day MA (Golden Cross) |
| Sell Signal | 10-day MA crosses below 50-day MA (Death Cross) |
| Initial Stop | 7% below entry price |
| Trailing Stop | 10% below highest price since entry |
| Risk Per Trade | 2% of portfolio |
| Max Position | 33% of portfolio |

## Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: Vue 3 + Tailwind CSS
- **Data**: yfinance (Yahoo Finance)
- **Charts**: lightweight-charts

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend runs at: http://localhost:5173

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/stocks/{symbol}` | Get price data with indicators |
| `GET /api/signals` | Get current signals for all stocks |
| `GET /api/portfolio` | Get portfolio state |
| `POST /api/trades` | Execute buy/sell trade |
| `POST /api/backtest` | Run historical backtest |

## Disclaimer

**This is for educational purposes only - NOT financial advice.**

- Paper trading only - no real money at risk
- Past performance does not guarantee future results
- This strategy loses money in sideways and bear markets
- Always do your own research before trading with real money

## What You'll Learn

| Feature | Lesson |
|---------|--------|
| Signal Scanner | How trend signals form and trigger |
| Paper Trading | Emotional experience of wins and losses |
| Position Sizing | Why risk management prevents ruin |
| Stop Losses | How stops protect capital and lock gains |
| Backtesting | How strategies perform across market conditions |
