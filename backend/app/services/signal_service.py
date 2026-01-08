"""
Signal detection service for MA crossover strategy.

Educational Note:
- Golden Cross: Short MA crosses ABOVE long MA = bullish (buy signal)
- Death Cross: Short MA crosses BELOW long MA = bearish (sell signal)

These signals work best in trending markets and struggle in sideways markets.
"""
import logging
import pandas as pd
from datetime import datetime
from typing import Optional

from ..config import STRATEGY_CONFIG
from ..models.signal import Signal, SignalType, SignalSummary
from .data_service import data_service
from .indicator_service import add_indicators
from .watchlist_service import watchlist_service

logger = logging.getLogger(__name__)


def detect_crossover(df: pd.DataFrame) -> tuple[SignalType, Optional[int]]:
    """
    Detect the current signal state and days since last signal.

    Returns:
        (signal_type, days_since_signal)
        - signal_type: GOLDEN_CROSS, DEATH_CROSS, or NONE
        - days_since_signal: Days since the crossover occurred (None if no recent signal)
    """
    short_period = STRATEGY_CONFIG["short_ma_period"]
    long_period = STRATEGY_CONFIG["long_ma_period"]

    # Ensure indicators are present
    if f"SMA_{short_period}" not in df.columns:
        df = add_indicators(df)

    sma_short = df[f"SMA_{short_period}"]
    sma_long = df[f"SMA_{long_period}"]

    # Need at least long_period + 1 data points
    if len(df) < long_period + 1:
        return SignalType.NONE, None

    # Find most recent crossover
    for i in range(len(df) - 1, 0, -1):
        curr_short = sma_short.iloc[i]
        curr_long = sma_long.iloc[i]
        prev_short = sma_short.iloc[i - 1]
        prev_long = sma_long.iloc[i - 1]

        # Skip if any values are NaN
        if pd.isna(curr_short) or pd.isna(curr_long) or pd.isna(prev_short) or pd.isna(prev_long):
            continue

        # Golden Cross: short crosses above long
        if prev_short <= prev_long and curr_short > curr_long:
            days_since = len(df) - 1 - i
            return SignalType.GOLDEN_CROSS, days_since

        # Death Cross: short crosses below long
        if prev_short >= prev_long and curr_short < curr_long:
            days_since = len(df) - 1 - i
            return SignalType.DEATH_CROSS, days_since

    # No crossover found, determine current state
    curr_short = sma_short.iloc[-1]
    curr_long = sma_long.iloc[-1]

    if pd.isna(curr_short) or pd.isna(curr_long):
        return SignalType.NONE, None

    # Return the current trend state (but not as a new signal)
    return SignalType.NONE, None


def is_buy_signal(df: pd.DataFrame) -> bool:
    """
    Check if current conditions warrant a buy signal.

    Buy conditions:
    1. Golden cross occurred (10-day crossed above 50-day)
    2. Current price is above the 50-day MA
    """
    short_period = STRATEGY_CONFIG["short_ma_period"]
    long_period = STRATEGY_CONFIG["long_ma_period"]

    if f"SMA_{short_period}" not in df.columns:
        df = add_indicators(df)

    signal_type, days_since = detect_crossover(df)

    # Must be a golden cross
    if signal_type != SignalType.GOLDEN_CROSS:
        return False

    # Signal should be recent (within last 3 days)
    if days_since is not None and days_since > 3:
        return False

    # Price must be above 50-day MA
    current_price = df["Close"].iloc[-1]
    sma_long = df[f"SMA_{long_period}"].iloc[-1]

    if pd.isna(sma_long):
        return False

    return current_price > sma_long


def is_sell_signal(df: pd.DataFrame) -> bool:
    """
    Check if current conditions warrant a sell signal.

    Sell condition:
    - Death cross occurred (10-day crossed below 50-day)
    """
    signal_type, days_since = detect_crossover(df)

    # Must be a death cross
    if signal_type != SignalType.DEATH_CROSS:
        return False

    # Signal should be recent (within last 3 days)
    if days_since is not None and days_since > 3:
        return False

    return True


def get_signal_for_stock(symbol: str) -> Signal:
    """Get the current signal status for a stock."""
    df = data_service.get_stock_data(symbol)
    df = add_indicators(df)

    short_period = STRATEGY_CONFIG["short_ma_period"]
    long_period = STRATEGY_CONFIG["long_ma_period"]

    signal_type, days_since = detect_crossover(df)

    current_price = float(df["Close"].iloc[-1])
    sma_short = df[f"SMA_{short_period}"].iloc[-1]
    sma_long = df[f"SMA_{long_period}"].iloc[-1]

    return Signal(
        symbol=symbol,
        signal_type=signal_type,
        price=current_price,
        sma_10=float(sma_short) if not pd.isna(sma_short) else 0.0,
        sma_50=float(sma_long) if not pd.isna(sma_long) else 0.0,
        timestamp=df.index[-1].to_pydatetime(),
        days_since_signal=days_since,
    )


def get_all_signals() -> SignalSummary:
    """Get signals for all stocks in the user's watchlist."""
    signals = []

    for symbol in watchlist_service.get_watchlist():
        try:
            signal = get_signal_for_stock(symbol)
            signals.append(signal)
        except Exception as e:
            logger.error(f"Error getting signal for {symbol}: {e}")

    return SignalSummary(
        signals=signals,
        last_updated=datetime.now(),
    )
