"""
Core trading strategy logic.

This module contains the main MA crossover strategy implementation.
"""
import pandas as pd
from datetime import datetime

from ..config import STRATEGY_CONFIG
from ..services.indicator_service import add_indicators


class MACrossoverStrategy:
    """
    10/50 Moving Average Crossover Strategy.

    Educational Summary:
    - Buy when 10-day MA crosses above 50-day MA (golden cross)
    - Sell when 10-day MA crosses below 50-day MA (death cross)
    - Use 7% initial stop-loss to limit downside
    - Use 10% trailing stop to protect profits
    """

    def __init__(self):
        self.short_period = STRATEGY_CONFIG["short_ma_period"]
        self.long_period = STRATEGY_CONFIG["long_ma_period"]

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals for historical data.

        Adds columns:
        - Signal: 1 for buy, -1 for sell, 0 for hold

        Used primarily for backtesting.
        """
        df = add_indicators(df.copy())

        sma_short = df[f"SMA_{self.short_period}"]
        sma_long = df[f"SMA_{self.long_period}"]

        df["Signal"] = 0

        # Detect crossovers
        for i in range(1, len(df)):
            prev_short = sma_short.iloc[i - 1]
            prev_long = sma_long.iloc[i - 1]
            curr_short = sma_short.iloc[i]
            curr_long = sma_long.iloc[i]

            # Skip if NaN
            if pd.isna(prev_short) or pd.isna(prev_long) or pd.isna(curr_short) or pd.isna(curr_long):
                continue

            # Golden cross - buy
            if prev_short <= prev_long and curr_short > curr_long:
                # Additional confirmation: price above long MA
                if df["Close"].iloc[i] > curr_long:
                    df.iloc[i, df.columns.get_loc("Signal")] = 1

            # Death cross - sell
            elif prev_short >= prev_long and curr_short < curr_long:
                df.iloc[i, df.columns.get_loc("Signal")] = -1

        return df

    def should_buy(self, df: pd.DataFrame) -> bool:
        """Check if current bar has a buy signal."""
        signals = self.generate_signals(df)
        return signals["Signal"].iloc[-1] == 1

    def should_sell(self, df: pd.DataFrame) -> bool:
        """Check if current bar has a sell signal."""
        signals = self.generate_signals(df)
        return signals["Signal"].iloc[-1] == -1


# Singleton instance
strategy = MACrossoverStrategy()
