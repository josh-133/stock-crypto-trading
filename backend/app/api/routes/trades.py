"""
Trade execution API endpoints.
"""
import logging
from fastapi import APIRouter, HTTPException

from ...services.portfolio_service import portfolio_service
from ...services.watchlist_service import watchlist_service
from ...models.trade import Trade, TradeRequest, TradeHistory

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trades", tags=["trades"])


@router.post("", response_model=Trade)
async def execute_trade(request: TradeRequest):
    """
    Execute a buy or sell trade.

    For buy orders:
        - If shares not specified, auto-calculates based on 2% risk rule
        - Checks that we don't exceed max positions (3)
        - Creates stop loss levels automatically

    For sell orders:
        - Closes the entire position
        - Records P&L

    Args:
        request: Trade request with symbol, action (buy/sell), and optional shares

    Returns:
        Executed trade details
    """
    try:
        symbol = request.symbol.upper()

        # Validate symbol exists (via watchlist service which uses yfinance)
        if not watchlist_service.validate_symbol(symbol):
            raise HTTPException(
                status_code=400,
                detail=f"{symbol} is not a valid stock symbol"
            )

        if request.action.value == "buy":
            trade = portfolio_service.buy(
                symbol=symbol,
                shares=request.shares,
            )
        else:
            trade = portfolio_service.sell(
                symbol=symbol,
                exit_reason="manual",
            )

        return trade

    except HTTPException:
        raise
    except ValueError as e:
        # ValueError is raised for known business logic errors (e.g., insufficient cash)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing trade for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to execute trade. Please try again.")


@router.get("", response_model=TradeHistory)
async def get_trades():
    """
    Get trade history.

    Returns:
        List of all executed trades with P&L for closed positions
    """
    try:
        return portfolio_service.get_trades()
    except Exception as e:
        logger.error(f"Error getting trades: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve trades. Please try again.")


@router.get("/{trade_id}", response_model=Trade)
async def get_trade(trade_id: str):
    """
    Get details of a specific trade.

    Args:
        trade_id: Unique trade identifier

    Returns:
        Trade details
    """
    try:
        trades = portfolio_service.get_trades()
        for trade in trades.trades:
            if trade.id == trade_id:
                return trade
        raise HTTPException(status_code=404, detail="Trade not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trade {trade_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve trade. Please try again.")
