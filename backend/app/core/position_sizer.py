"""
Position sizing calculator using the 2% risk rule.

Educational Note:
The 2% rule ensures that no single trade can significantly damage your account.
Even 10 consecutive losses only results in a ~20% drawdown, which is recoverable.

Compare to 10% risk: 10 losses = 65% drawdown, requires 186% gain to recover!
"""
from ..config import STRATEGY_CONFIG


def calculate_position_size(
    account_value: float,
    entry_price: float,
    stop_loss_price: float,
    max_risk_pct: float = None,
    max_position_pct: float = None,
) -> dict:
    """
    Calculate the number of shares to buy based on risk management rules.

    Args:
        account_value: Total portfolio value
        entry_price: Price at which we plan to buy
        stop_loss_price: Price at which we would exit for a loss
        max_risk_pct: Maximum percentage of account to risk (default from config)
        max_position_pct: Maximum percentage of account for one position (default from config)

    Returns:
        dict with:
            - shares: Number of shares to buy
            - position_value: Total dollar value of position
            - risk_amount: Dollar amount at risk
            - risk_percent: Percentage of account at risk

    Raises:
        ValueError: If stop loss is not below entry price
    """
    if max_risk_pct is None:
        max_risk_pct = STRATEGY_CONFIG["max_risk_per_trade_pct"]
    if max_position_pct is None:
        max_position_pct = STRATEGY_CONFIG["max_position_pct"]

    # Validate inputs
    if entry_price <= 0:
        raise ValueError("Entry price must be positive")
    if stop_loss_price >= entry_price:
        raise ValueError("Stop loss must be below entry price")
    if account_value <= 0:
        raise ValueError("Account value must be positive")

    # Calculate risk per share
    risk_per_share = entry_price - stop_loss_price

    # Maximum dollars we're willing to risk (2% of account)
    max_risk_dollars = account_value * max_risk_pct

    # Shares based on risk constraint
    shares_by_risk = int(max_risk_dollars / risk_per_share)

    # Maximum position size constraint (33% of account)
    max_position_dollars = account_value * max_position_pct
    shares_by_position = int(max_position_dollars / entry_price)

    # Take the smaller of the two constraints
    shares = min(shares_by_risk, shares_by_position)

    # Ensure at least 1 share if we can afford it
    if shares == 0 and account_value >= entry_price:
        shares = 1

    # Calculate actual values
    position_value = shares * entry_price
    risk_amount = shares * risk_per_share
    risk_percent = (risk_amount / account_value) * 100 if account_value > 0 else 0

    return {
        "shares": shares,
        "position_value": round(position_value, 2),
        "risk_amount": round(risk_amount, 2),
        "risk_percent": round(risk_percent, 2),
    }


def calculate_stop_loss_price(entry_price: float, stop_pct: float = None) -> float:
    """
    Calculate the initial stop loss price.

    Args:
        entry_price: Price at which we bought
        stop_pct: Stop loss percentage (default 7% from config)

    Returns:
        Stop loss price
    """
    if stop_pct is None:
        stop_pct = STRATEGY_CONFIG["initial_stop_loss_pct"]

    return round(entry_price * (1 - stop_pct), 2)
