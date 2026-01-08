import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '../composables/useApi'

export const usePortfolioStore = defineStore('portfolio', () => {
  const api = useApi()

  // State
  const portfolio = ref(null)
  const stats = ref(null)
  const trades = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const positions = computed(() => portfolio.value?.positions || [])
  const cash = computed(() => portfolio.value?.cash || 0)
  const totalValue = computed(() => portfolio.value?.total_value || 0)
  const totalReturn = computed(() => portfolio.value?.total_return || 0)
  const totalReturnPercent = computed(() => portfolio.value?.total_return_percent || 0)

  // Actions
  async function fetchPortfolio() {
    loading.value = true
    error.value = null
    try {
      portfolio.value = await api.getPortfolio()
    } catch (err) {
      error.value = err.message
      console.error('Error fetching portfolio:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchStats() {
    try {
      stats.value = await api.getPortfolioStats()
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  async function fetchTrades() {
    try {
      const result = await api.getTrades()
      trades.value = result.trades
    } catch (err) {
      console.error('Error fetching trades:', err)
    }
  }

  async function resetPortfolio() {
    loading.value = true
    try {
      await api.resetPortfolio()
      await fetchPortfolio()
      await fetchStats()
      trades.value = []
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function executeBuy(symbol, shares = null) {
    loading.value = true
    error.value = null
    try {
      const trade = await api.executeTrade(symbol, 'buy', shares)
      await fetchPortfolio()
      await fetchTrades()
      return trade
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function executeSell(symbol) {
    loading.value = true
    error.value = null
    try {
      const trade = await api.executeTrade(symbol, 'sell')
      await fetchPortfolio()
      await fetchTrades()
      await fetchStats()
      return trade
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function checkStops() {
    try {
      const result = await api.checkStops()
      if (result.triggered_count > 0) {
        await fetchPortfolio()
        await fetchTrades()
        await fetchStats()
      }
      return result
    } catch (err) {
      console.error('Error checking stops:', err)
    }
  }

  return {
    // State
    portfolio,
    stats,
    trades,
    loading,
    error,
    // Getters
    positions,
    cash,
    totalValue,
    totalReturn,
    totalReturnPercent,
    // Actions
    fetchPortfolio,
    fetchStats,
    fetchTrades,
    resetPortfolio,
    executeBuy,
    executeSell,
    checkStops,
  }
})
