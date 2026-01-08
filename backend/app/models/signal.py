"""
Trading signal models.
"""
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional


class SignalType(str, Enum):
    """Type of trading signal."""
    GOLDEN_CROSS = "golden_cross"  # Buy signal
    DEATH_CROSS = "death_cross"    # Sell signal
    NONE = "none"                   # No signal


class Signal(BaseModel):
    """Trading signal for a stock."""
    symbol: str
    signal_type: SignalType
    price: float
    sma_10: float
    sma_50: float
    timestamp: datetime
    days_since_signal: Optional[int] = None


class SignalSummary(BaseModel):
    """Summary of current signals across all watched stocks."""
    signals: list[Signal]
    last_updated: datetime
