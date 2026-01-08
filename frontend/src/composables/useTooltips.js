/**
 * Trading term definitions for tooltips.
 * These explanations are written for beginners.
 */
export const tradingTerms = {
  // Moving Averages
  SMA: {
    term: 'SMA (Simple Moving Average)',
    definition: 'The average closing price over a set number of days. It smooths out price noise to show the trend direction.',
  },
  SMA_10: {
    term: 'SMA 10 (10-Day Moving Average)',
    definition: 'The average closing price over the last 10 trading days. Represents short-term momentum (~2 weeks).',
  },
  SMA_50: {
    term: 'SMA 50 (50-Day Moving Average)',
    definition: 'The average closing price over the last 50 trading days. Represents medium-term trend (~2.5 months).',
  },
  MA: {
    term: 'MA (Moving Average)',
    definition: 'A calculation that averages price over time to identify trends. Higher MA = uptrend, lower MA = downtrend.',
  },

  // Signals
  goldenCross: {
    term: 'Golden Cross',
    definition: 'A bullish (buy) signal that occurs when the short-term MA (10-day) crosses ABOVE the long-term MA (50-day). Suggests upward momentum is building.',
  },
  deathCross: {
    term: 'Death Cross',
    definition: 'A bearish (sell) signal that occurs when the short-term MA (10-day) crosses BELOW the long-term MA (50-day). Suggests the uptrend may be ending.',
  },

  // P&L Terms
  PnL: {
    term: 'P&L (Profit and Loss)',
    definition: 'The money you made or lost on a trade. Calculated as: (Exit Price - Entry Price) × Number of Shares.',
  },
  unrealizedPnL: {
    term: 'Unrealized P&L',
    definition: 'Paper profit or loss on positions you still hold. It\'s "unrealized" because you haven\'t sold yet - the final result could change.',
  },
  realizedPnL: {
    term: 'Realized P&L',
    definition: 'Actual profit or loss from trades you\'ve closed. This is real money made or lost.',
  },

  // Risk Management
  stopLoss: {
    term: 'Stop Loss',
    definition: 'A preset price level where you automatically sell to limit your loss. Like a safety net that prevents catastrophic losses.',
  },
  initialStop: {
    term: 'Initial Stop (7%)',
    definition: 'A stop loss set 7% below your entry price. If the stock drops 7% from where you bought, you sell to cut your losses.',
  },
  trailingStop: {
    term: 'Trailing Stop (10%)',
    definition: 'A stop loss that moves UP as the price rises, always staying 10% below the highest price since you bought. It locks in profits while letting winners run.',
  },
  activeStop: {
    term: 'Active Stop',
    definition: 'The stop loss level currently in effect - whichever is HIGHER between your initial stop and trailing stop. Higher = more protection.',
  },

  // Position Sizing
  positionSize: {
    term: 'Position Size',
    definition: 'How many shares to buy. Calculated based on how much you\'re willing to risk, not how much you want to spend.',
  },
  riskPerTrade: {
    term: 'Risk Per Trade (2%)',
    definition: 'The maximum amount you\'re willing to lose on any single trade - 2% of your total portfolio. This ensures one bad trade won\'t ruin you.',
  },
  maxPosition: {
    term: 'Max Position (33%)',
    definition: 'The maximum amount to invest in one stock - 33% of your portfolio. This forces diversification across at least 3 stocks.',
  },

  // Performance Metrics
  winRate: {
    term: 'Win Rate',
    definition: 'The percentage of trades that made money. Note: A 40% win rate can still be profitable if winners are bigger than losers!',
  },
  drawdown: {
    term: 'Drawdown',
    definition: 'The decline from a peak to a trough in your portfolio value. Max drawdown shows your worst "losing streak" - how much you would have lost at the worst point.',
  },
  maxDrawdown: {
    term: 'Max Drawdown',
    definition: 'The largest peak-to-valley decline in your portfolio during the period. Shows the worst-case scenario you would have experienced.',
  },
  equityCurve: {
    term: 'Equity Curve',
    definition: 'A chart showing your portfolio value over time. An upward slope = making money, downward slope = losing money.',
  },

  // Portfolio Terms
  totalValue: {
    term: 'Total Value',
    definition: 'Your cash plus the current value of all your stock positions. This is what your portfolio is worth right now.',
  },
  cash: {
    term: 'Cash',
    definition: 'Money available to buy stocks. When you buy, cash decreases. When you sell, cash increases.',
  },
  invested: {
    term: 'Invested',
    definition: 'The current market value of stocks you own. This changes as stock prices move up and down.',
  },
  totalReturn: {
    term: 'Total Return',
    definition: 'How much money you\'ve made or lost overall, compared to your starting amount ($10,000).',
  },

  // Trading Terms
  entry: {
    term: 'Entry Price',
    definition: 'The price at which you bought the stock. This is your starting point for calculating profit or loss.',
  },
  entryPrice: {
    term: 'Entry Price',
    definition: 'The price at which you bought the stock. This is your starting point for calculating profit or loss.',
  },
  exit: {
    term: 'Exit Price',
    definition: 'The price at which you sold the stock. Compare this to your entry price to see your profit or loss.',
  },
  shares: {
    term: 'Shares',
    definition: 'Units of ownership in a company. If you own 10 shares of AAPL at $150, your position is worth $1,500.',
  },

  // Backtest Terms
  backtest: {
    term: 'Backtest',
    definition: 'Testing a strategy on historical data to see how it would have performed. Warning: Past results don\'t guarantee future performance!',
  },
}

export function useTradingTerm(key) {
  return tradingTerms[key] || { term: key, definition: 'No definition available.' }
}
