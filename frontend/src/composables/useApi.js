import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export function useApi() {
  // Stock data
  const getStockData = async (symbol, days = 365) => {
    const response = await api.get(`/stocks/${symbol}`, { params: { days } })
    return response.data
  }

  const getLatestPrice = async (symbol) => {
    const response = await api.get(`/stocks/${symbol}/latest`)
    return response.data
  }

  // Signals
  const getSignals = async () => {
    const response = await api.get('/signals')
    return response.data
  }

  const getSignal = async (symbol) => {
    const response = await api.get(`/signals/${symbol}`)
    return response.data
  }

  // Portfolio
  const getPortfolio = async () => {
    const response = await api.get('/portfolio')
    return response.data
  }

  const resetPortfolio = async () => {
    const response = await api.post('/portfolio/reset')
    return response.data
  }

  const getPortfolioHistory = async () => {
    const response = await api.get('/portfolio/history')
    return response.data
  }

  const getPortfolioStats = async () => {
    const response = await api.get('/portfolio/stats')
    return response.data
  }

  const checkStops = async () => {
    const response = await api.post('/portfolio/check-stops')
    return response.data
  }

  // Trades
  const executeTrade = async (symbol, action, shares = null) => {
    const response = await api.post('/trades', { symbol, action, shares })
    return response.data
  }

  const getTrades = async () => {
    const response = await api.get('/trades')
    return response.data
  }

  // Backtest
  const runBacktest = async (symbol, startDate = null, endDate = null, initialCapital = null) => {
    const response = await api.post('/backtest', {
      symbol,
      start_date: startDate,
      end_date: endDate,
      initial_capital: initialCapital,
    })
    return response.data
  }

  // Benchmark
  const getBenchmark = async (days = 365) => {
    const response = await api.get('/benchmark', { params: { days } })
    return response.data
  }

  // Watchlist
  const getWatchlist = async () => {
    const response = await api.get('/watchlist')
    return response.data
  }

  const addToWatchlist = async (symbol) => {
    const response = await api.post(`/watchlist/${symbol}`)
    return response.data
  }

  const removeFromWatchlist = async (symbol) => {
    const response = await api.delete(`/watchlist/${symbol}`)
    return response.data
  }

  const searchSymbols = async (query) => {
    const response = await api.get('/watchlist/search', { params: { q: query } })
    return response.data
  }

  const validateSymbol = async (symbol) => {
    const response = await api.get(`/watchlist/validate/${symbol}`)
    return response.data
  }

  return {
    getStockData,
    getLatestPrice,
    getSignals,
    getSignal,
    getPortfolio,
    resetPortfolio,
    getPortfolioHistory,
    getPortfolioStats,
    checkStops,
    executeTrade,
    getTrades,
    runBacktest,
    getBenchmark,
    getWatchlist,
    addToWatchlist,
    removeFromWatchlist,
    searchSymbols,
    validateSymbol,
  }
}
