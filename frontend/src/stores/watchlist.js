import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '../composables/useApi'

export const useWatchlistStore = defineStore('watchlist', () => {
  const api = useApi()

  // State
  const symbols = ref([])
  const maxSize = ref(50)
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const count = computed(() => symbols.value.length)
  const isFull = computed(() => count.value >= maxSize.value)

  // Actions
  async function fetchWatchlist() {
    loading.value = true
    error.value = null
    try {
      const data = await api.getWatchlist()
      symbols.value = data.symbols
      maxSize.value = data.max_size
    } catch (e) {
      error.value = e.response?.data?.detail || 'Failed to load watchlist'
      console.error('Failed to fetch watchlist:', e)
    } finally {
      loading.value = false
    }
  }

  async function addSymbol(symbol) {
    loading.value = true
    error.value = null
    try {
      const data = await api.addToWatchlist(symbol)
      symbols.value = data.symbols
      return { success: true, message: data.message }
    } catch (e) {
      const message = e.response?.data?.detail || 'Failed to add symbol'
      error.value = message
      return { success: false, message }
    } finally {
      loading.value = false
    }
  }

  async function removeSymbol(symbol) {
    loading.value = true
    error.value = null
    try {
      const data = await api.removeFromWatchlist(symbol)
      symbols.value = data.symbols
      return { success: true, message: data.message }
    } catch (e) {
      const message = e.response?.data?.detail || 'Failed to remove symbol'
      error.value = message
      return { success: false, message }
    } finally {
      loading.value = false
    }
  }

  async function searchSymbols(query) {
    if (!query || query.length < 1) return []
    try {
      return await api.searchSymbols(query)
    } catch (e) {
      console.error('Failed to search symbols:', e)
      return []
    }
  }

  function isInWatchlist(symbol) {
    return symbols.value.includes(symbol.toUpperCase())
  }

  return {
    // State
    symbols,
    maxSize,
    loading,
    error,
    // Computed
    count,
    isFull,
    // Actions
    fetchWatchlist,
    addSymbol,
    removeSymbol,
    searchSymbols,
    isInWatchlist,
  }
})
