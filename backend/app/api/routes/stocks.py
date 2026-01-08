"""
Stock data API endpoints.
"""
import logging
from fastapi import APIRouter, HTTPException
from datetime import datetime

from ...services.data_service import data_service
from ...services.indicator_service import add_indicators, get_indicator_values
from ...models.stock import StockData, StockPrice, StockLatest
from ...config import DATA_CONFIG, STOCK_UNIVERSE

logger = logging.getLogger(__name__)

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

        # Input validation: Check symbol is in allowed list
        if symbol not in STOCK_UNIVERSE:
            raise HTTPException(
                status_code=400,
                detail=f"Symbol must be one of: {', '.join(STOCK_UNIVERSE)}"
            )

        # Input validation: Bounds check on days
        if days < 1 or days > 1825:  # Max ~5 years
            raise HTTPException(
                status_code=400,
                detail="Days must be between 1 and 1825"
            )

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

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch stock data. Please try again.")


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

        # Input validation: Check symbol is in allowed list
        if symbol not in STOCK_UNIVERSE:
            raise HTTPException(
                status_code=400,
                detail=f"Symbol must be one of: {', '.join(STOCK_UNIVERSE)}"
            )

        latest = data_service.get_latest_price(symbol)

        return StockLatest(
            symbol=latest["symbol"],
            price=latest["price"],
            change=latest["change"],
            change_percent=latest["change_percent"],
            volume=latest["volume"],
            timestamp=latest["timestamp"],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch latest price. Please try again.")
