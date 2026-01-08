"""
Trade models for paper trading.
"""
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional


class TradeAction(str, Enum):
    """Trade action type."""
    BUY = "buy"
    SELL = "sell"


class TradeRequest(BaseModel):
    """Request to execute a trade."""
    symbol: str
    action: TradeAction
    shares: Optional[int] = None  # If None, auto-calculate based on risk


class Trade(BaseModel):
    """Executed trade record."""
    id: str
    symbol: str
    action: TradeAction
    shares: int
    price: float
    total_value: float
    timestamp: datetime

    # For sell trades, track P&L
    entry_price: Optional[float] = None
    pnl: Optional[float] = None
    pnl_percent: Optional[float] = None

    # Exit reason for sells
    exit_reason: Optional[str] = None  # "signal", "initial_stop", "trailing_stop", "manual"


class TradeHistory(BaseModel):
    """List of all trades."""
    trades: list[Trade]
    total_trades: int
