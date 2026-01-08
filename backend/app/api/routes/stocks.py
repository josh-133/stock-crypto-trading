"""
Stock data API endpoints.
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime

from ...services.data_service import data_service
from ...services.indicator_service import add_indicators, get_indicator_values
from ...models.stock import StockData, StockPrice, StockLatest
from ...config import DATA_CONFIG

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/{symbol}", response_model=StockData)
async def get_stock_data(symbol: str, days: int = DATA_CONFIG["lookback_days"]):
    """
    Get historical price data and indicators for a stock.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT)
        days: Number of days of history (default 365)

    Returns:
        Stock data with OHLCV prices and SMA indicators
    """
    try:
        symbol = symbol.upper()
        df = data_service.get_stock_data(symbol, days=days)
        df = add_indicators(df)

        # Convert to response model
        prices = []
        for idx, row in df.iterrows():
            prices.append(StockPrice(
                date=idx.to_pydatetime(),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=int(row["Volume"]),
            ))

        indicators = get_indicator_values(df)

        # Calculate change percent
        if len(df) >= 2:
            change_pct = ((df["Close"].iloc[-1] / df["Close"].iloc[-2]) - 1) * 100
        else:
            change_pct = 0.0

        return StockData(
            symbol=symbol,
            prices=prices,
            sma_10=indicators["sma_10"],
            sma_50=indicators["sma_50"],
            current_price=float(df["Close"].iloc[-1]),
            change_percent=float(change_pct),
        )

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error fetching data for {symbol}: {str(e)}")


@router.get("/{symbol}/latest", response_model=StockLatest)
async def get_latest_price(symbol: str):
    """
    Get the latest price info for a stock.

    Args:
        symbol: Stock ticker symbol

    Returns:
        Current price, change, and volume
    """
    try:
        symbol = symbol.upper()
        latest = data_service.get_latest_price(symbol)

        return StockLatest(
            symbol=latest["symbol"],
            price=latest["price"],
            change=latest["change"],
            change_percent=latest["change_percent"],
            volume=latest["volume"],
            timestamp=latest["timestamp"],
        )

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error fetching price for {symbol}: {str(e)}")
