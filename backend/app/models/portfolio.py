"""
Portfolio and position models for paper trading.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Position(BaseModel):
    """An open position in a stock."""
    symbol: str
    shares: int
    entry_price: float
    entry_date: datetime
    current_price: float
    highest_price: float          # For trailing stop calculation
    initial_stop: float           # 7% below entry
    trailing_stop: float          # 10% below highest
    active_stop: float            # The higher of initial/trailing
    unrealized_pnl: float
    unrealized_pnl_percent: float


class Portfolio(BaseModel):
    """Paper trading portfolio state."""
    cash: float
    positions: list[Position]
    total_value: float
    invested_value: float
    daily_pnl: float
    daily_pnl_percent: float
    total_return: float
    total_return_percent: float
    last_updated: datetime


class PortfolioHistory(BaseModel):
    """Historical portfolio values."""
    dates: list[datetime]
    values: list[float]


class PortfolioStats(BaseModel):
    """Portfolio performance statistics."""
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    average_win: float
    average_loss: float
    largest_win: float
    largest_loss: float
    max_drawdown: float
    max_drawdown_percent: float
