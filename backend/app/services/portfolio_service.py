"""
Paper trading portfolio service.

This service manages the virtual portfolio for paper trading,
including positions, trades, and P&L calculations.
"""
import logging
import threading
import uuid
from datetime import datetime
from typing import Optional

from ..config import PAPER_TRADING_CONFIG, STRATEGY_CONFIG
from ..models.portfolio import Portfolio, Position, PortfolioStats
from ..models.trade import Trade, TradeAction, TradeHistory
from ..core.stop_loss import StopLossManager
from ..core.position_sizer import calculate_position_size, calculate_stop_loss_price
from .data_service import data_service

logger = logging.getLogger(__name__)


class PortfolioService:
    """
    Service for managing paper trading portfolio.

    Maintains:
    - Cash balance
    - Open positions with stop losses
    - Trade history
    - Portfolio value history
    """

    def __init__(self):
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self.reset()

    def reset(self) -> None:
        """Reset portfolio to initial state."""
        with self._lock:
            self.cash = PAPER_TRADING_CONFIG["initial_balance"]
            self.positions: dict[str, dict] = {}  # symbol -> position data
            self.trades: list[Trade] = []
            self.value_history: list[tuple[datetime, float]] = [
                (datetime.now(), self.cash)
            ]

    def get_portfolio(self) -> Portfolio:
        """Get current portfolio state."""
        with self._lock:
            positions = []
            invested_value = 0.0

            for symbol, pos_data in self.positions.items():
                try:
                    latest = data_service.get_latest_price(symbol)
                    current_price = latest["price"]
                except Exception:
                    current_price = pos_data["entry_price"]

                # Update stop loss manager with current price
                stop_manager: StopLossManager = pos_data["stop_manager"]
                stop_manager.update(current_price)

                # Calculate P&L
                entry_value = pos_data["shares"] * pos_data["entry_price"]
                current_value = pos_data["shares"] * current_price
                unrealized_pnl = current_value - entry_value
                unrealized_pnl_percent = (unrealized_pnl / entry_value) * 100 if entry_value > 0 else 0

                invested_value += current_value

                position = Position(
                    symbol=symbol,
                    shares=pos_data["shares"],
                    entry_price=pos_data["entry_price"],
                    entry_date=pos_data["entry_date"],
                    current_price=current_price,
                    highest_price=stop_manager.highest_price,
                    initial_stop=stop_manager.initial_stop,
                    trailing_stop=stop_manager.trailing_stop,
                    active_stop=stop_manager.get_active_stop(),
                    unrealized_pnl=round(unrealized_pnl, 2),
                    unrealized_pnl_percent=round(unrealized_pnl_percent, 2),
                )
                positions.append(position)

            total_value = self.cash + invested_value

            # Calculate daily P&L (vs last recorded value)
            if self.value_history:
                last_value = self.value_history[-1][1]
                daily_pnl = total_value - last_value
                daily_pnl_percent = (daily_pnl / last_value) * 100 if last_value > 0 else 0
            else:
                daily_pnl = 0.0
                daily_pnl_percent = 0.0

            # Calculate total return
            initial = PAPER_TRADING_CONFIG["initial_balance"]
            total_return = total_value - initial
            total_return_percent = (total_return / initial) * 100 if initial > 0 else 0

            return Portfolio(
                cash=round(self.cash, 2),
                positions=positions,
                total_value=round(total_value, 2),
                invested_value=round(invested_value, 2),
                daily_pnl=round(daily_pnl, 2),
                daily_pnl_percent=round(daily_pnl_percent, 2),
                total_return=round(total_return, 2),
                total_return_percent=round(total_return_percent, 2),
                last_updated=datetime.now(),
            )

    def buy(
        self,
        symbol: str,
        shares: Optional[int] = None,
        price: Optional[float] = None,
    ) -> Trade:
        """
        Execute a buy order.

        Args:
            symbol: Stock symbol to buy
            shares: Number of shares (if None, auto-calculate based on risk)
            price: Execution price (if None, use latest price)

        Returns:
            Trade object with execution details
        """
        with self._lock:
            # Check if already have position
            if symbol in self.positions:
                raise ValueError(f"Already have a position in {symbol}")

            # Check max positions
            if len(self.positions) >= STRATEGY_CONFIG["max_positions"]:
                raise ValueError(f"Maximum positions ({STRATEGY_CONFIG['max_positions']}) reached")

            # Get price
            if price is None:
                latest = data_service.get_latest_price(symbol)
                price = latest["price"]

            # Calculate stop loss price
            stop_loss_price = calculate_stop_loss_price(price)

            # Calculate position size if not specified
            if shares is None:
                portfolio = self.get_portfolio()
                sizing = calculate_position_size(
                    account_value=portfolio.total_value,
                    entry_price=price,
                    stop_loss_price=stop_loss_price,
                )
                shares = sizing["shares"]

            if shares <= 0:
                raise ValueError("Cannot buy zero shares")

            # Check if we have enough cash
            total_cost = shares * price
            if total_cost > self.cash:
                raise ValueError(f"Insufficient cash. Need ${total_cost:.2f}, have ${self.cash:.2f}")

            # Execute trade
            self.cash -= total_cost

            # Create stop loss manager
            stop_manager = StopLossManager(entry_price=price)

            # Record position
            self.positions[symbol] = {
                "shares": shares,
                "entry_price": price,
                "entry_date": datetime.now(),
                "stop_manager": stop_manager,
            }

            # Create trade record
            trade = Trade(
                id=str(uuid.uuid4()),
                symbol=symbol,
                action=TradeAction.BUY,
                shares=shares,
                price=price,
                total_value=round(total_cost, 2),
                timestamp=datetime.now(),
            )

            self.trades.append(trade)
            return trade

    def sell(
        self,
        symbol: str,
        price: Optional[float] = None,
        exit_reason: str = "manual",
    ) -> Trade:
        """
        Execute a sell order (close position).

        Args:
            symbol: Stock symbol to sell
            price: Execution price (if None, use latest price)
            exit_reason: Reason for exit ("signal", "initial_stop", "trailing_stop", "manual")

        Returns:
            Trade object with execution details
        """
        with self._lock:
            if symbol not in self.positions:
                raise ValueError(f"No position in {symbol}")

            pos_data = self.positions[symbol]
            shares = pos_data["shares"]
            entry_price = pos_data["entry_price"]

            # Get price
            if price is None:
                latest = data_service.get_latest_price(symbol)
                price = latest["price"]

            # Calculate P&L
            total_value = shares * price
            entry_value = shares * entry_price
            pnl = total_value - entry_value
            pnl_percent = (pnl / entry_value) * 100 if entry_value > 0 else 0

            # Execute trade
            self.cash += total_value

            # Remove position
            del self.positions[symbol]

            # Create trade record
            trade = Trade(
                id=str(uuid.uuid4()),
                symbol=symbol,
                action=TradeAction.SELL,
                shares=shares,
                price=price,
                total_value=round(total_value, 2),
                timestamp=datetime.now(),
                entry_price=entry_price,
                pnl=round(pnl, 2),
                pnl_percent=round(pnl_percent, 2),
                exit_reason=exit_reason,
            )

            self.trades.append(trade)
            return trade

    def check_stops(self) -> list[Trade]:
        """
        Check all positions for stop loss triggers.

        Returns list of executed sell trades for positions that hit their stops.
        """
        with self._lock:
            triggered_trades = []

            for symbol in list(self.positions.keys()):
                pos_data = self.positions[symbol]
                stop_manager: StopLossManager = pos_data["stop_manager"]

                try:
                    latest = data_service.get_latest_price(symbol)
                    current_price = latest["price"]

                    # Update stop with current price
                    stop_manager.update(current_price)

                    # Check if stopped out
                    is_stopped, reason = stop_manager.is_stopped_out(current_price)

                    if is_stopped:
                        trade = self.sell(symbol, price=current_price, exit_reason=reason)
                        triggered_trades.append(trade)

                except Exception as e:
                    logger.error(f"Error checking stop for {symbol}: {e}")

            return triggered_trades

    def get_trades(self) -> TradeHistory:
        """Get trade history."""
        with self._lock:
            return TradeHistory(
                trades=self.trades,
                total_trades=len(self.trades),
            )

    def get_stats(self) -> PortfolioStats:
        """Calculate portfolio performance statistics."""
        with self._lock:
            sell_trades = [t for t in self.trades if t.action == TradeAction.SELL]

            if not sell_trades:
                return PortfolioStats(
                    total_trades=len(self.trades),
                    winning_trades=0,
                    losing_trades=0,
                    win_rate=0.0,
                    average_win=0.0,
                    average_loss=0.0,
                    largest_win=0.0,
                    largest_loss=0.0,
                    max_drawdown=0.0,
                    max_drawdown_percent=0.0,
                )

            winners = [t for t in sell_trades if t.pnl and t.pnl > 0]
            losers = [t for t in sell_trades if t.pnl and t.pnl < 0]

            win_rate = len(winners) / len(sell_trades) * 100 if sell_trades else 0

            avg_win = sum(t.pnl for t in winners) / len(winners) if winners else 0
            avg_loss = sum(t.pnl for t in losers) / len(losers) if losers else 0

            largest_win = max((t.pnl for t in winners), default=0)
            largest_loss = min((t.pnl for t in losers), default=0)

            # Calculate max drawdown from value history
            max_drawdown = 0.0
            max_drawdown_pct = 0.0
            peak = PAPER_TRADING_CONFIG["initial_balance"]

            for _, value in self.value_history:
                if value > peak:
                    peak = value
                drawdown = peak - value
                drawdown_pct = (drawdown / peak) * 100 if peak > 0 else 0
                if drawdown > max_drawdown:
                    max_drawdown = drawdown
                    max_drawdown_pct = drawdown_pct

            return PortfolioStats(
                total_trades=len(self.trades),
                winning_trades=len(winners),
                losing_trades=len(losers),
                win_rate=round(win_rate, 1),
                average_win=round(avg_win, 2),
                average_loss=round(avg_loss, 2),
                largest_win=round(largest_win, 2),
                largest_loss=round(largest_loss, 2),
                max_drawdown=round(max_drawdown, 2),
                max_drawdown_percent=round(max_drawdown_pct, 2),
            )

    def record_daily_value(self) -> None:
        """Record current portfolio value for history tracking."""
        with self._lock:
            portfolio = self.get_portfolio()
            self.value_history.append((datetime.now(), portfolio.total_value))


# Singleton instance
portfolio_service = PortfolioService()
