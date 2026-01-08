<template>
  <div class="card">
    <h2 class="text-lg font-semibold text-white mb-4">Execute Trade</h2>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Symbol Selection -->
      <div>
        <label class="label">Symbol</label>
        <select v-model="symbol" class="input w-full">
          <option v-for="s in availableSymbols" :key="s" :value="s">
            {{ s }}
          </option>
        </select>
      </div>

      <!-- Signal Status -->
      <div v-if="currentSignal" class="p-3 rounded-lg" :class="signalBgClass">
        <p class="text-sm font-medium" :class="signalTextClass">
          {{ signalMessage }}
        </p>
        <p v-if="currentSignal.days_since_signal !== null" class="text-xs mt-1 opacity-75">
          {{ currentSignal.days_since_signal }} days ago
        </p>
      </div>

      <!-- Auto Position Size -->
      <div class="p-3 bg-gray-700 rounded-lg">
        <p class="text-sm text-gray-400 mb-1">Position Size (Auto-calculated)</p>
        <p class="text-white">Based on 2% risk rule</p>
        <p class="text-xs text-gray-500 mt-1">
          Max risk: 2% of portfolio | Max position: 33% of portfolio
        </p>
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        :disabled="!canBuy || loading"
        class="btn btn-success w-full"
        :class="{ 'opacity-50 cursor-not-allowed': !canBuy || loading }"
      >
        {{ loading ? 'Executing...' : 'Buy' }}
      </button>

      <!-- Warning if no signal -->
      <p v-if="!hasGoldenCross" class="text-sm text-yellow-400">
        No active buy signal for this stock. Consider waiting for a golden cross.
      </p>

      <!-- Already have position -->
      <p v-if="hasPosition" class="text-sm text-red-400">
        You already have a position in {{ symbol }}.
      </p>

      <!-- Max positions -->
      <p v-if="maxPositionsReached" class="text-sm text-red-400">
        Maximum positions (3) reached. Sell a position to buy another.
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { usePortfolioStore } from '../../stores/portfolio'
import { useSignalsStore } from '../../stores/signals'

const portfolioStore = usePortfolioStore()
const signalsStore = useSignalsStore()

const symbol = ref('SPY')
const loading = ref(false)

const availableSymbols = ['AAPL', 'MSFT', 'GOOGL', 'SPY']

const currentSignal = computed(() => signalsStore.getSignalForSymbol(symbol.value))

const hasGoldenCross = computed(() =>
  currentSignal.value?.signal_type === 'golden_cross'
)

const hasPosition = computed(() =>
  portfolioStore.positions.some(p => p.symbol === symbol.value)
)

const maxPositionsReached = computed(() =>
  portfolioStore.positions.length >= 3
)

const canBuy = computed(() =>
  !hasPosition.value && !maxPositionsReached.value
)

const signalBgClass = computed(() => {
  if (!currentSignal.value) return 'bg-gray-700'
  switch (currentSignal.value.signal_type) {
    case 'golden_cross':
      return 'bg-green-900'
    case 'death_cross':
      return 'bg-red-900'
    default:
      return 'bg-gray-700'
  }
})

const signalTextClass = computed(() => {
  if (!currentSignal.value) return 'text-gray-400'
  switch (currentSignal.value.signal_type) {
    case 'golden_cross':
      return 'text-green-300'
    case 'death_cross':
      return 'text-red-300'
    default:
      return 'text-gray-400'
  }
})

const signalMessage = computed(() => {
  if (!currentSignal.value) return 'Loading signal...'
  switch (currentSignal.value.signal_type) {
    case 'golden_cross':
      return 'Golden Cross - Buy Signal Active'
    case 'death_cross':
      return 'Death Cross - Sell Signal (Not recommended to buy)'
    default:
      return 'No active signal'
  }
})

async function handleSubmit() {
  if (!canBuy.value || loading.value) return

  loading.value = true
  try {
    const trade = await portfolioStore.executeBuy(symbol.value)
    alert(`Bought ${trade.shares} shares of ${symbol.value} at $${trade.price.toFixed(2)}`)
  } catch (err) {
    alert(err.message || 'Trade failed')
  } finally {
    loading.value = false
  }
}
</script>
