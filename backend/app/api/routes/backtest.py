"""
Backtesting API endpoints.
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ...services.backtest_service import run_backtest, BacktestResult
from ...services.watchlist_service import watchlist_service

logger = logging.getLogger(__name__)

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

        # Validate symbol exists (via watchlist service which uses yfinance)
        if not watchlist_service.validate_symbol(symbol):
            raise HTTPException(
                status_code=400,
                detail=f"{symbol} is not a valid stock symbol"
            )

        # Input validation: Check date format and logic
        if request.start_date:
            try:
                start_dt = datetime.strptime(request.start_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="start_date must be in YYYY-MM-DD format"
                )

        if request.end_date:
            try:
                end_dt = datetime.strptime(request.end_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="end_date must be in YYYY-MM-DD format"
                )
            # Check end date is not in the future
            if end_dt > datetime.now():
                raise HTTPException(
                    status_code=400,
                    detail="end_date cannot be in the future"
                )

        if request.start_date and request.end_date:
            if start_dt >= end_dt:
                raise HTTPException(
                    status_code=400,
                    detail="start_date must be before end_date"
                )

        # Input validation: Check initial capital bounds
        if request.initial_capital is not None:
            if request.initial_capital < 100 or request.initial_capital > 10000000:
                raise HTTPException(
                    status_code=400,
                    detail="initial_capital must be between $100 and $10,000,000"
                )

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

    except HTTPException:
        raise
    except ValueError as e:
        # ValueError is raised for known issues like insufficient data
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Backtest error for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to run backtest. Please try again.")
