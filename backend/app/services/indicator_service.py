"""
Technical indicator calculations.

Educational Note:
A Simple Moving Average (SMA) gives equal weight to all prices in the window.
It smooths out price noise to reveal the underlying trend direction.
"""
import pandas as pd
from typing import Optional

from ..config import STRATEGY_CONFIG


def calculate_sma(prices: pd.Series, period: int) -> pd.Series:
    """
    Calculate Simple Moving Average.

    Args:
        prices: Series of closing prices
        period: Number of periods for the average

    Returns:
        Series with SMA values (NaN for first period-1 values)

    Example:
        If period=10, the SMA on day 10 is the average of days 1-10.
        Days 1-9 will have NaN values.
    """
    return prices.rolling(window=period).mean()


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add SMA indicators to a price DataFrame.

    Adds:
        - SMA_10: 10-day simple moving average
        - SMA_50: 50-day simple moving average

    Args:
        df: DataFrame with 'Close' column

    Returns:
        DataFrame with added indicator columns
    """
    df = df.copy()

    short_period = STRATEGY_CONFIG["short_ma_period"]
    long_period = STRATEGY_CONFIG["long_ma_period"]

    df[f"SMA_{short_period}"] = calculate_sma(df["Close"], short_period)
    df[f"SMA_{long_period}"] = calculate_sma(df["Close"], long_period)

    return df


def get_indicator_values(df: pd.DataFrame) -> dict:
    """
    Extract indicator values from DataFrame for API response.

    Returns dict with lists of indicator values (None for NaN).
    """
    short_period = STRATEGY_CONFIG["short_ma_period"]
    long_period = STRATEGY_CONFIG["long_ma_period"]

    # Add indicators if not present
    if f"SMA_{short_period}" not in df.columns:
        df = add_indicators(df)

    def series_to_list(s: pd.Series) -> list[Optional[float]]:
        return [None if pd.isna(v) else float(v) for v in s]

    return {
        f"sma_{short_period}": series_to_list(df[f"SMA_{short_period}"]),
        f"sma_{long_period}": series_to_list(df[f"SMA_{long_period}"]),
    }
