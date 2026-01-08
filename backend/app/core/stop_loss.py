"""
Stop loss management for protecting capital and profits.

Educational Note:
Stop losses serve two purposes:
1. Initial stop: Limits loss if your trade thesis was wrong
2. Trailing stop: Protects profits as price moves in your favor

The trailing stop only moves UP, never down. This lets winners run while
ensuring you keep most of your gains.
"""
from ..config import STRATEGY_CONFIG


class StopLossManager:
    """
    Manages initial and trailing stop losses for a position.

    Example Usage:
        manager = StopLossManager(entry_price=150.00)
        manager.update(160.00)  # Price rose, trailing stop moves up
        manager.update(155.00)  # Price fell, trailing stop stays same
        if manager.is_stopped_out(148.00):
            print("Sell!")
    """

    def __init__(
        self,
        entry_price: float,
        initial_stop_pct: float = None,
        trailing_stop_pct: float = None,
    ):
        """
        Initialize stop loss manager.

        Args:
            entry_price: Price at which position was opened
            initial_stop_pct: Percentage for initial stop (default 7%)
            trailing_stop_pct: Percentage for trailing stop (default 10%)
        """
        if initial_stop_pct is None:
            initial_stop_pct = STRATEGY_CONFIG["initial_stop_loss_pct"]
        if trailing_stop_pct is None:
            trailing_stop_pct = STRATEGY_CONFIG["trailing_stop_pct"]

        self.entry_price = entry_price
        self.initial_stop_pct = initial_stop_pct
        self.trailing_stop_pct = trailing_stop_pct

        # Calculate initial stop (7% below entry)
        self.initial_stop = round(entry_price * (1 - initial_stop_pct), 2)

        # Track highest price for trailing stop
        self.highest_price = entry_price

        # Calculate trailing stop (10% below highest)
        self.trailing_stop = round(entry_price * (1 - trailing_stop_pct), 2)

    def update(self, current_price: float) -> None:
        """
        Update the trailing stop based on current price.

        If price made a new high, the trailing stop moves up.
        Trailing stop never moves down.

        Args:
            current_price: Current market price
        """
        if current_price > self.highest_price:
            self.highest_price = current_price
            self.trailing_stop = round(
                current_price * (1 - self.trailing_stop_pct), 2
            )

    def get_active_stop(self) -> float:
        """
        Get the currently active stop loss level.

        Returns the HIGHER of the initial stop and trailing stop.
        This provides the most protection.
        """
        return max(self.initial_stop, self.trailing_stop)

    def is_stopped_out(self, current_price: float) -> tuple[bool, str]:
        """
        Check if current price triggers a stop loss.

        Args:
            current_price: Current market price

        Returns:
            (is_stopped, reason)
            - is_stopped: True if stop was triggered
            - reason: "initial_stop" or "trailing_stop" if triggered
        """
        active_stop = self.get_active_stop()

        if current_price < active_stop:
            # Determine which stop was hit
            if self.trailing_stop >= self.initial_stop:
                return True, "trailing_stop"
            else:
                return True, "initial_stop"

        return False, ""

    def get_status(self) -> dict:
        """Get current stop loss status for display."""
        return {
            "entry_price": self.entry_price,
            "highest_price": self.highest_price,
            "initial_stop": self.initial_stop,
            "trailing_stop": self.trailing_stop,
            "active_stop": self.get_active_stop(),
            "initial_stop_pct": self.initial_stop_pct * 100,
            "trailing_stop_pct": self.trailing_stop_pct * 100,
        }
