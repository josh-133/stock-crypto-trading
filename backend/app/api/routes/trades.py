"""
Trade execution API endpoints.
"""
from fastapi import APIRouter, HTTPException

from ...services.portfolio_service import portfolio_service
from ...models.trade import Trade, TradeRequest, TradeHistory

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

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing trade: {str(e)}")


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
        raise HTTPException(status_code=500, detail=f"Error getting trades: {str(e)}")


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
        raise HTTPException(status_code=404, detail=f"Trade {trade_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting trade: {str(e)}")
