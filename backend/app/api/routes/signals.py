"""
Trading signals API endpoints.
"""
from fastapi import APIRouter, HTTPException

from ...services.signal_service import get_signal_for_stock, get_all_signals
from ...models.signal import Signal, SignalSummary

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("", response_model=SignalSummary)
async def get_signals():
    """
    Get current trading signals for all watched stocks.

    Returns:
        List of signals showing golden cross, death cross, or no signal
        for each stock in the universe (AAPL, MSFT, GOOGL, SPY)
    """
    try:
        return get_all_signals()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting signals: {str(e)}")


@router.get("/{symbol}", response_model=Signal)
async def get_signal(symbol: str):
    """
    Get current trading signal for a specific stock.

    Args:
        symbol: Stock ticker symbol

    Returns:
        Signal status (golden_cross, death_cross, or none)
        with current price and MA values
    """
    try:
        symbol = symbol.upper()
        return get_signal_for_stock(symbol)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error getting signal for {symbol}: {str(e)}")
