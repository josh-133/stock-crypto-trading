"""
Stock data models for API responses.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StockPrice(BaseModel):
    """Single price bar (OHLCV)."""
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class StockData(BaseModel):
    """Stock data with indicators."""
    symbol: str
    prices: list[StockPrice]
    sma_10: list[Optional[float]]
    sma_50: list[Optional[float]]
    current_price: float
    change_percent: float


class StockLatest(BaseModel):
    """Latest price info for a stock."""
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: int
    timestamp: datetime
