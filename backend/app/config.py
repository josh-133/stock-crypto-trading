"""
Configuration settings for the trading platform.
All strategy parameters are defined here for easy adjustment.
"""

# Strategy Parameters
STRATEGY_CONFIG = {
    "short_ma_period": 10,      # Fast moving average (2 weeks)
    "long_ma_period": 50,       # Slow moving average (2.5 months)
    "initial_stop_loss_pct": 0.07,    # 7% below entry
    "trailing_stop_pct": 0.10,         # 10% below highest high
    "max_risk_per_trade_pct": 0.02,    # Risk max 2% per trade
    "max_position_pct": 0.33,          # Max 33% of portfolio in one stock
    "max_positions": 3,                 # Maximum concurrent positions
}

# Paper Trading Settings
PAPER_TRADING_CONFIG = {
    "initial_balance": 10000.0,  # Starting with $10,000
    "currency": "USD",
}

# Stock Universe - Large-cap, liquid US stocks
STOCK_UNIVERSE = ["AAPL", "MSFT", "GOOGL", "SPY"]

# Data Settings
DATA_CONFIG = {
    "lookback_days": 365,       # 1 year of historical data
    "data_source": "yfinance",
}

# API Settings
API_CONFIG = {
    "title": "Stock Trading Platform API",
    "description": "A beginner-friendly paper trading platform with MA crossover strategy",
    "version": "1.0.0",
}
