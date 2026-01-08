"""
Portfolio API endpoints for paper trading.
"""
from fastapi import APIRouter, HTTPException

from ...services.portfolio_service import portfolio_service
from ...models.portfolio import Portfolio, PortfolioHistory, PortfolioStats

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("", response_model=Portfolio)
async def get_portfolio():
    """
    Get current portfolio state.

    Returns:
        Cash balance, open positions, total value, and P&L
    """
    try:
        return portfolio_service.get_portfolio()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting portfolio: {str(e)}")


@router.post("/reset")
async def reset_portfolio():
    """
    Reset portfolio to initial state ($10,000 cash, no positions).

    This clears all positions and trade history.
    """
    try:
        portfolio_service.reset()
        return {"message": "Portfolio reset to $10,000", "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting portfolio: {str(e)}")


@router.get("/history", response_model=PortfolioHistory)
async def get_portfolio_history():
    """
    Get historical portfolio values.

    Returns:
        List of dates and corresponding portfolio values
    """
    try:
        history = portfolio_service.value_history
        return PortfolioHistory(
            dates=[h[0] for h in history],
            values=[h[1] for h in history],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting history: {str(e)}")


@router.get("/stats", response_model=PortfolioStats)
async def get_portfolio_stats():
    """
    Get portfolio performance statistics.

    Returns:
        Win rate, average win/loss, max drawdown, etc.
    """
    try:
        return portfolio_service.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


@router.post("/check-stops")
async def check_stop_losses():
    """
    Check all positions for stop loss triggers.

    If any position hits its stop loss, it will be automatically sold.

    Returns:
        List of trades executed due to stop loss triggers
    """
    try:
        trades = portfolio_service.check_stops()
        return {
            "triggered_count": len(trades),
            "trades": [t.model_dump() for t in trades],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking stops: {str(e)}")
