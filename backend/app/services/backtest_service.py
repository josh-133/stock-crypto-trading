"""
Backtesting service for testing strategy on historical data.

Educational Note:
Backtesting shows how a strategy WOULD have performed in the past.
It does NOT guarantee future performance. Markets change, and
strategies that worked before may not work in the future.
"""
import pandas as pd
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from ..config import STRATEGY_CONFIG, PAPER_TRADING_CONFIG
from ..core.strategy import MACrossoverStrategy
from ..core.stop_loss import StopLossManager
from ..core.position_sizer import calculate_position_size, calculate_stop_loss_price
from .data_service import data_service
from .indicator_service import add_indicators


@dataclass
class BacktestTrade:
    """A trade in the backtest."""
    entry_date: datetime
    entry_price: float
    exit_date: Optional[datetime] = None
    exit_price: Optional[float] = None
    shares: int = 0
    pnl: float = 0.0
    pnl_percent: float = 0.0
    exit_reason: str = ""


@dataclass
class BacktestResult:
    """Results from a backtest run."""
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
    equity_curve: list[tuple[datetime, float]]
    trades: list[BacktestTrade]


def run_backtest(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    initial_capital: float = None,
) -> BacktestResult:
    """
    Run a backtest of the MA crossover strategy.

    Args:
        symbol: Stock symbol to backtest
        start_date: Start date (YYYY-MM-DD format, default 1 year ago)
        end_date: End date (YYYY-MM-DD format, default today)
        initial_capital: Starting capital (default from config)

    Returns:
        BacktestResult with performance metrics
    """
    if initial_capital is None:
        initial_capital = PAPER_TRADING_CONFIG["initial_balance"]

    # Calculate how many days of data we need
    # Need extra buffer for MA calculation (50 days) before the start date
    if start_date:
        start_dt = pd.to_datetime(start_date)
        days_from_start = (datetime.now() - start_dt).days
        days_needed = days_from_start + 100  # Extra buffer for MA warmup
        days_needed = max(days_needed, 500)  # At least ~2 years
    else:
        days_needed = 500  # Default to ~2 years

    # Fetch data with enough history
    df = data_service.get_stock_data(symbol, days=days_needed)
    df = add_indicators(df)

    # Convert index to timezone-naive for comparison
    # yfinance returns timezone-aware timestamps (America/New_York)
    df.index = df.index.tz_localize(None)

    # Filter by date range if specified
    if start_date:
        df = df[df.index >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df.index <= pd.to_datetime(end_date)]

    if len(df) < STRATEGY_CONFIG["long_ma_period"] + 1:
        raise ValueError(f"Insufficient data for backtest. Need at least {STRATEGY_CONFIG['long_ma_period'] + 1} trading days. Try a wider date range or check that the dates are valid.")

    # Initialize backtest state
    cash = initial_capital
    position: Optional[dict] = None
    trades: list[BacktestTrade] = []
    equity_curve: list[tuple[datetime, float]] = []

    short_ma = f"SMA_{STRATEGY_CONFIG['short_ma_period']}"
    long_ma = f"SMA_{STRATEGY_CONFIG['long_ma_period']}"

    # Run through each day
    for i in range(1, len(df)):
        date = df.index[i].to_pydatetime()
        close = df["Close"].iloc[i]
        prev_close = df["Close"].iloc[i - 1]

        sma_short = df[short_ma].iloc[i]
        sma_long = df[long_ma].iloc[i]
        prev_sma_short = df[short_ma].iloc[i - 1]
        prev_sma_long = df[long_ma].iloc[i - 1]

        # Skip if indicators not ready
        if pd.isna(sma_short) or pd.isna(sma_long) or pd.isna(prev_sma_short) or pd.isna(prev_sma_long):
            portfolio_value = cash + (position["shares"] * close if position else 0)
            equity_curve.append((date, portfolio_value))
            continue

        # Check for signals and stops
        if position:
            # Update stop loss
            stop_manager: StopLossManager = position["stop_manager"]
            stop_manager.update(close)

            # Check stop loss
            is_stopped, stop_reason = stop_manager.is_stopped_out(close)

            # Check death cross
            death_cross = prev_sma_short >= prev_sma_long and sma_short < sma_long

            if is_stopped or death_cross:
                # Sell
                exit_reason = stop_reason if is_stopped else "signal"
                exit_price = close

                pnl = (exit_price - position["entry_price"]) * position["shares"]
                pnl_pct = (exit_price / position["entry_price"] - 1) * 100

                trade = BacktestTrade(
                    entry_date=position["entry_date"],
                    entry_price=position["entry_price"],
                    exit_date=date,
                    exit_price=exit_price,
                    shares=position["shares"],
                    pnl=round(pnl, 2),
                    pnl_percent=round(pnl_pct, 2),
                    exit_reason=exit_reason,
                )
                trades.append(trade)

                cash += position["shares"] * exit_price
                position = None

        else:
            # Check for golden cross
            golden_cross = prev_sma_short <= prev_sma_long and sma_short > sma_long
            price_above_ma = close > sma_long

            if golden_cross and price_above_ma:
                # Calculate position size
                portfolio_value = cash
                stop_price = calculate_stop_loss_price(close)

                sizing = calculate_position_size(
                    account_value=portfolio_value,
                    entry_price=close,
                    stop_loss_price=stop_price,
                )

                shares = sizing["shares"]

                if shares > 0 and shares * close <= cash:
                    # Buy
                    cost = shares * close
                    cash -= cost

                    position = {
                        "shares": shares,
                        "entry_price": close,
                        "entry_date": date,
                        "stop_manager": StopLossManager(entry_price=close),
                    }

        # Record equity
        portfolio_value = cash + (position["shares"] * close if position else 0)
        equity_curve.append((date, portfolio_value))

    # Close any open position at end
    if position:
        final_price = df["Close"].iloc[-1]
        pnl = (final_price - position["entry_price"]) * position["shares"]
        pnl_pct = (final_price / position["entry_price"] - 1) * 100

        trade = BacktestTrade(
            entry_date=position["entry_date"],
            entry_price=position["entry_price"],
            exit_date=df.index[-1].to_pydatetime(),
            exit_price=final_price,
            shares=position["shares"],
            pnl=round(pnl, 2),
            pnl_percent=round(pnl_pct, 2),
            exit_reason="end_of_period",
        )
        trades.append(trade)
        cash += position["shares"] * final_price

    # Calculate stats
    final_value = cash
    total_return = final_value - initial_capital
    total_return_pct = (total_return / initial_capital) * 100

    winners = [t for t in trades if t.pnl > 0]
    losers = [t for t in trades if t.pnl < 0]
    win_rate = len(winners) / len(trades) * 100 if trades else 0

    # Max drawdown
    max_dd = 0.0
    max_dd_pct = 0.0
    peak = initial_capital

    for _, value in equity_curve:
        if value > peak:
            peak = value
        dd = peak - value
        dd_pct = (dd / peak) * 100 if peak > 0 else 0
        if dd > max_dd:
            max_dd = dd
            max_dd_pct = dd_pct

    return BacktestResult(
        symbol=symbol,
        start_date=df.index[0].to_pydatetime(),
        end_date=df.index[-1].to_pydatetime(),
        initial_capital=initial_capital,
        final_value=round(final_value, 2),
        total_return=round(total_return, 2),
        total_return_percent=round(total_return_pct, 2),
        total_trades=len(trades),
        winning_trades=len(winners),
        losing_trades=len(losers),
        win_rate=round(win_rate, 1),
        max_drawdown=round(max_dd, 2),
        max_drawdown_percent=round(max_dd_pct, 2),
        equity_curve=equity_curve,
        trades=trades,
    )
