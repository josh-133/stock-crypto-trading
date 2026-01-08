import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApi } from '../composables/useApi'

export const useStocksStore = defineStore('stocks', () => {
  const api = useApi()

  // State
  const stockData = ref({}) // symbol -> data
  const latestPrices = ref({}) // symbol -> latest price info
  const selectedSymbol = ref('SPY')
  const loading = ref(false)
  const error = ref(null)

  // Stock universe
  const symbols = ['AAPL', 'MSFT', 'GOOGL', 'SPY']

  // Actions
  async function fetchStockData(symbol, days = 365) {
    loading.value = true
    error.value = null
    try {
      const data = await api.getStockData(symbol, days)
      stockData.value[symbol] = data
      return data
    } catch (err) {
      error.value = err.message
      console.error(`Error fetching data for ${symbol}:`, err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchLatestPrice(symbol) {
    try {
      const data = await api.getLatestPrice(symbol)
      latestPrices.value[symbol] = data
      return data
    } catch (err) {
      console.error(`Error fetching price for ${symbol}:`, err)
      throw err
    }
  }

  async function fetchAllLatestPrices() {
    const promises = symbols.map(symbol => fetchLatestPrice(symbol))
    await Promise.allSettled(promises)
  }

  function setSelectedSymbol(symbol) {
    selectedSymbol.value = symbol
  }

  function getStockData(symbol) {
    return stockData.value[symbol]
  }

  function getLatestPrice(symbol) {
    return latestPrices.value[symbol]
  }

  return {
    // State
    stockData,
    latestPrices,
    selectedSymbol,
    loading,
    error,
    symbols,
    // Actions
    fetchStockData,
    fetchLatestPrice,
    fetchAllLatestPrices,
    setSelectedSymbol,
    getStockData,
    getLatestPrice,
  }
})
