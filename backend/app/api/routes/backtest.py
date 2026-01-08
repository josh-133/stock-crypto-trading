"""
Backtesting API endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ...services.backtest_service import run_backtest, BacktestResult

router = APIRouter(prefix="/backtest", tags=["backtest"])


class BacktestRequest(BaseModel):
    """Request model for backtesting."""
    symbol: str
    start_date: Optional[str] = None  # YYYY-MM-DD
    end_date: Optional[str] = None    # YYYY-MM-DD
    initial_capital: Optional[float] = None


class BacktestResponse(BaseModel):
    """Response model for backtesting."""
    symbol: str
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_value: float
    total_return: float
    total_return_percent: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    max_drawdown: float
    max_drawdown_percent: float
    equity_curve: list[dict]
    trades: list[dict]


@router.post("", response_model=BacktestResponse)
async def backtest(request: BacktestRequest):
    """
    Run a backtest of the MA crossover strategy.

    This simulates how the strategy would have performed
    on historical data. Results do NOT guarantee future performance.

    Args:
        request: Backtest parameters (symbol, date range, capital)

    Returns:
        Performance metrics, equity curve, and trade list
    """
    try:
        symbol = request.symbol.upper()

        result = run_backtest(
            symbol=symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital,
        )

        # Convert to response format
        equity_curve = [
            {"date": dt.isoformat(), "value": val}
            for dt, val in result.equity_curve
        ]

        trades = [
            {
                "entry_date": t.entry_date.isoformat(),
                "entry_price": t.entry_price,
                "exit_date": t.exit_date.isoformat() if t.exit_date else None,
                "exit_price": t.exit_price,
                "shares": t.shares,
                "pnl": t.pnl,
                "pnl_percent": t.pnl_percent,
                "exit_reason": t.exit_reason,
            }
            for t in result.trades
        ]

        return BacktestResponse(
            symbol=result.symbol,
            start_date=result.start_date,
            end_date=result.end_date,
            initial_capital=result.initial_capital,
            final_value=result.final_value,
            total_return=result.total_return,
            total_return_percent=result.total_return_percent,
            total_trades=result.total_trades,
            winning_trades=result.winning_trades,
            losing_trades=result.losing_trades,
            win_rate=result.win_rate,
            max_drawdown=result.max_drawdown,
            max_drawdown_percent=result.max_drawdown_percent,
            equity_curve=equity_curve,
            trades=trades,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backtest error: {str(e)}")
