"""
Data service for fetching stock data from yfinance.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional

from ..config import DATA_CONFIG, STOCK_UNIVERSE


class DataService:
    """Service for fetching and caching stock data."""

    def __init__(self):
        self._cache: dict[str, tuple[pd.DataFrame, datetime]] = {}
        self._cache_duration = timedelta(minutes=5)  # Cache for 5 minutes

    def get_stock_data(
        self,
        symbol: str,
        days: int = DATA_CONFIG["lookback_days"]
    ) -> pd.DataFrame:
        """
        Fetch historical daily data for a stock.

        Returns DataFrame with columns: Open, High, Low, Close, Volume
        Index is datetime.
        """
        # Check cache
        if symbol in self._cache:
            df, cached_at = self._cache[symbol]
            if datetime.now() - cached_at < self._cache_duration:
                return df

        # Fetch fresh data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date, interval="1d")

        if df.empty:
            raise ValueError(f"No data found for symbol: {symbol}")

        # Keep only needed columns
        df = df[["Open", "High", "Low", "Close", "Volume"]]

        # Cache the data
        self._cache[symbol] = (df, datetime.now())

        return df

    def get_latest_price(self, symbol: str) -> dict:
        """Get the latest price info for a stock."""
        df = self.get_stock_data(symbol, days=5)

        if len(df) < 2:
            raise ValueError(f"Insufficient data for symbol: {symbol}")

        latest = df.iloc[-1]
        previous = df.iloc[-2]

        change = latest["Close"] - previous["Close"]
        change_percent = (change / previous["Close"]) * 100

        return {
            "symbol": symbol,
            "price": float(latest["Close"]),
            "change": float(change),
            "change_percent": float(change_percent),
            "volume": int(latest["Volume"]),
            "timestamp": df.index[-1].to_pydatetime(),
        }

    def get_all_stocks_data(self) -> dict[str, pd.DataFrame]:
        """Fetch data for all stocks in the universe."""
        data = {}
        for symbol in STOCK_UNIVERSE:
            try:
                data[symbol] = self.get_stock_data(symbol)
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
        return data

    def clear_cache(self):
        """Clear the data cache."""
        self._cache.clear()


# Singleton instance
data_service = DataService()
