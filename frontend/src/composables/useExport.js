/**
 * Export utilities for downloading trade data.
 */

export function useExport() {
  /**
   * Export trades to CSV file.
   * @param {Array} trades - Array of trade objects
   * @param {string} filename - Name for the downloaded file
   */
  function exportTradesToCSV(trades, filename = 'trades.csv') {
    if (!trades || trades.length === 0) {
      alert('No trades to export')
      return
    }

    // Define CSV headers
    const headers = [
      'Date',
      'Symbol',
      'Action',
      'Shares',
      'Price',
      'Total Value',
      'Entry Price',
      'P&L ($)',
      'P&L (%)',
      'Exit Reason',
    ]

    // Convert trades to CSV rows
    const rows = trades.map(trade => [
      formatDate(trade.timestamp),
      trade.symbol,
      trade.action.toUpperCase(),
      trade.shares,
      trade.price.toFixed(2),
      trade.total_value.toFixed(2),
      trade.entry_price ? trade.entry_price.toFixed(2) : '',
      trade.pnl !== null ? trade.pnl.toFixed(2) : '',
      trade.pnl_percent !== null ? trade.pnl_percent.toFixed(2) : '',
      trade.exit_reason || '',
    ])

    // Build CSV content
    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(',')),
    ].join('\n')

    // Download the file
    downloadFile(csvContent, filename, 'text/csv')
  }

  /**
   * Export backtest results to CSV.
   * @param {Object} results - Backtest results object
   * @param {string} filename - Name for the downloaded file
   */
  function exportBacktestToCSV(results, filename = 'backtest.csv') {
    if (!results) {
      alert('No backtest results to export')
      return
    }

    // Summary section
    const summary = [
      ['Backtest Summary'],
      ['Symbol', results.symbol],
      ['Period', `${formatDate(results.start_date)} to ${formatDate(results.end_date)}`],
      ['Initial Capital', results.initial_capital.toFixed(2)],
      ['Final Value', results.final_value.toFixed(2)],
      ['Total Return ($)', results.total_return.toFixed(2)],
      ['Total Return (%)', results.total_return_percent.toFixed(2)],
      ['Total Trades', results.total_trades],
      ['Winning Trades', results.winning_trades],
      ['Losing Trades', results.losing_trades],
      ['Win Rate (%)', results.win_rate.toFixed(1)],
      ['Max Drawdown ($)', results.max_drawdown.toFixed(2)],
      ['Max Drawdown (%)', results.max_drawdown_percent.toFixed(2)],
      [],
      ['Trade History'],
      ['Entry Date', 'Entry Price', 'Exit Date', 'Exit Price', 'Shares', 'P&L ($)', 'P&L (%)', 'Exit Reason'],
    ]

    // Add trades
    const tradeRows = results.trades.map(trade => [
      formatDate(trade.entry_date),
      trade.entry_price.toFixed(2),
      trade.exit_date ? formatDate(trade.exit_date) : '',
      trade.exit_price ? trade.exit_price.toFixed(2) : '',
      trade.shares,
      trade.pnl.toFixed(2),
      trade.pnl_percent.toFixed(2),
      formatExitReason(trade.exit_reason),
    ])

    const allRows = [...summary, ...tradeRows]
    const csvContent = allRows.map(row => row.map(cell => `"${cell}"`).join(',')).join('\n')

    downloadFile(csvContent, filename, 'text/csv')
  }

  /**
   * Export portfolio history to CSV.
   * @param {Object} portfolio - Portfolio object with positions
   * @param {Array} trades - Trade history
   */
  function exportPortfolioToCSV(portfolio, trades, filename = 'portfolio.csv') {
    const rows = [
      ['Portfolio Summary'],
      ['Total Value', portfolio.total_value.toFixed(2)],
      ['Cash', portfolio.cash.toFixed(2)],
      ['Invested', portfolio.invested_value.toFixed(2)],
      ['Total Return ($)', portfolio.total_return.toFixed(2)],
      ['Total Return (%)', portfolio.total_return_percent.toFixed(2)],
      [],
      ['Open Positions'],
      ['Symbol', 'Shares', 'Entry Price', 'Current Price', 'P&L ($)', 'P&L (%)', 'Stop Loss'],
    ]

    // Add positions
    portfolio.positions.forEach(pos => {
      rows.push([
        pos.symbol,
        pos.shares,
        pos.entry_price.toFixed(2),
        pos.current_price.toFixed(2),
        pos.unrealized_pnl.toFixed(2),
        pos.unrealized_pnl_percent.toFixed(2),
        pos.active_stop.toFixed(2),
      ])
    })

    rows.push([])
    rows.push(['Trade History'])
    rows.push(['Date', 'Symbol', 'Action', 'Shares', 'Price', 'P&L ($)'])

    trades.forEach(trade => {
      rows.push([
        formatDate(trade.timestamp),
        trade.symbol,
        trade.action.toUpperCase(),
        trade.shares,
        trade.price.toFixed(2),
        trade.pnl !== null ? trade.pnl.toFixed(2) : '',
      ])
    })

    const csvContent = rows.map(row => row.map(cell => `"${cell}"`).join(',')).join('\n')
    downloadFile(csvContent, filename, 'text/csv')
  }

  // Helper functions
  function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  function formatDate(dateStr) {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  function formatExitReason(reason) {
    switch (reason) {
      case 'signal': return 'Death Cross'
      case 'initial_stop': return 'Stop Loss (7%)'
      case 'trailing_stop': return 'Trailing Stop (10%)'
      case 'end_of_period': return 'End of Period'
      case 'manual': return 'Manual'
      default: return reason || ''
    }
  }

  return {
    exportTradesToCSV,
    exportBacktestToCSV,
    exportPortfolioToCSV,
  }
}
