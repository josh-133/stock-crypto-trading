import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApi } from '../composables/useApi'

export const useSignalsStore = defineStore('signals', () => {
  const api = useApi()

  // State
  const signals = ref([])
  const lastUpdated = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const buySignals = computed(() =>
    signals.value.filter(s => s.signal_type === 'golden_cross')
  )

  const sellSignals = computed(() =>
    signals.value.filter(s => s.signal_type === 'death_cross')
  )

  const hasActiveSignals = computed(() =>
    buySignals.value.length > 0 || sellSignals.value.length > 0
  )

  // Actions
  async function fetchSignals() {
    loading.value = true
    error.value = null
    try {
      const result = await api.getSignals()
      signals.value = result.signals
      lastUpdated.value = result.last_updated
    } catch (err) {
      error.value = err.message
      console.error('Error fetching signals:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchSignal(symbol) {
    try {
      return await api.getSignal(symbol)
    } catch (err) {
      console.error(`Error fetching signal for ${symbol}:`, err)
      throw err
    }
  }

  function getSignalForSymbol(symbol) {
    return signals.value.find(s => s.symbol === symbol)
  }

  return {
    // State
    signals,
    lastUpdated,
    loading,
    error,
    // Getters
    buySignals,
    sellSignals,
    hasActiveSignals,
    // Actions
    fetchSignals,
    fetchSignal,
    getSignalForSymbol,
  }
})
