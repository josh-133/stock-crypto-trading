"""
Benchmark API endpoint for comparing strategy vs buy-and-hold.
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta

from ...services.data_service import data_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/benchmark", tags=["benchmark"])


class BenchmarkResponse(BaseModel):
    """Response model for benchmark comparison."""
    spy_start_price: float
    spy_current_price: float
    spy_return_percent: float
    period_days: int
    start_date: str
    end_date: str


@router.get("", response_model=BenchmarkResponse)
async def get_benchmark(days: int = 365):
    """
    Get SPY benchmark performance for comparison.

    This returns the buy-and-hold return for SPY over the specified period,
    which can be compared to your strategy's performance.

    Args:
        days: Number of days to look back (default: 365)

    Returns:
        SPY start price, current price, and return percentage
    """
    try:
        # Input validation
        if days < 30 or days > 1825:
            raise HTTPException(
                status_code=400,
                detail="Days must be between 30 and 1825 (5 years)"
            )

        # Fetch SPY data
        df = data_service.get_stock_data("SPY", days=days)

        if len(df) < 2:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data for benchmark calculation"
            )

        start_price = float(df["Close"].iloc[0])
        current_price = float(df["Close"].iloc[-1])
        return_percent = ((current_price - start_price) / start_price) * 100

        start_date = df.index[0].strftime("%Y-%m-%d")
        end_date = df.index[-1].strftime("%Y-%m-%d")

        return BenchmarkResponse(
            spy_start_price=start_price,
            spy_current_price=current_price,
            spy_return_percent=return_percent,
            period_days=len(df),
            start_date=start_date,
            end_date=end_date,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting benchmark data: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch benchmark data. Please try again."
        )
