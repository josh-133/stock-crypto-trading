<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-theme-primary">Dashboard</h1>

    <!-- Risk Warning -->
    <div class="bg-yellow-600 bg-opacity-20 border border-yellow-600 rounded-lg p-4">
      <p class="text-yellow-500 text-sm">
        This is a paper trading simulator for educational purposes only.
        No real money is at risk. Past performance does not guarantee future results.
      </p>
    </div>

    <!-- Top Row: Portfolio Summary + Signals -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2">
        <PortfolioSummary />
      </div>
      <div>
        <PerformanceMetrics />
      </div>
    </div>

    <!-- Chart -->
    <PriceChart />

    <!-- Signals + Positions -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <SignalAlerts />

      <!-- Open Positions -->
      <div class="card">
        <h2 class="text-lg font-semibold text-theme-primary mb-4 flex items-center">
          Open Positions
          <Tooltip
            :term="tradingTerms.positionSize.term"
            :definition="tradingTerms.positionSize.definition"
          />
        </h2>
        <div v-if="positions.length === 0" class="text-theme-secondary text-center py-8">
          No open positions. Watch for golden cross signals to buy.
        </div>
        <div v-else class="space-y-4">
          <PositionCard
            v-for="position in positions"
            :key="position.symbol"
            :position="position"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, watch, ref } from 'vue'
import { usePortfolioStore } from '../stores/portfolio'
import { useSignalsStore } from '../stores/signals'
import { useSettingsStore } from '../stores/settings'
import { tradingTerms } from '../composables/useTooltips'
import PortfolioSummary from '../components/dashboard/PortfolioSummary.vue'
import PerformanceMetrics from '../components/dashboard/PerformanceMetrics.vue'
import SignalAlerts from '../components/dashboard/SignalAlerts.vue'
import PriceChart from '../components/charts/PriceChart.vue'
import PositionCard from '../components/trading/PositionCard.vue'
import Tooltip from '../components/ui/Tooltip.vue'

const portfolioStore = usePortfolioStore()
const signalsStore = useSignalsStore()
const settingsStore = useSettingsStore()

const positions = computed(() => portfolioStore.positions)

// Track previous signals for sound alerts
const previousSignals = ref([])
let refreshInterval = null

onMounted(async () => {
  await loadData()
  setupAutoRefresh()
})

onUnmounted(() => {
  clearAutoRefresh()
})

// Watch for auto-refresh setting changes
watch(
  () => [settingsStore.autoRefreshEnabled, settingsStore.refreshInterval],
  () => {
    clearAutoRefresh()
    setupAutoRefresh()
  }
)

async function loadData() {
  // Store previous signals before fetching new ones
  previousSignals.value = [...signalsStore.signals]

  await Promise.all([
    portfolioStore.fetchPortfolio(),
    portfolioStore.fetchStats(),
    portfolioStore.fetchTrades(),
    signalsStore.fetchSignals(),
  ])

  // Check for new signals and play sound
  checkForNewSignals()

  // Check for stop loss triggers
  await portfolioStore.checkStops()
}

function checkForNewSignals() {
  if (!settingsStore.soundEnabled) return
  if (previousSignals.value.length === 0) return

  const newSignals = signalsStore.signals

  for (const signal of newSignals) {
    const prevSignal = previousSignals.value.find(s => s.symbol === signal.symbol)

    // If signal type changed, play sound
    if (prevSignal && prevSignal.signal_type !== signal.signal_type) {
      if (signal.signal_type === 'golden_cross') {
        settingsStore.playSound('buy')
      } else if (signal.signal_type === 'death_cross') {
        settingsStore.playSound('sell')
      }
    }
  }
}

function setupAutoRefresh() {
  if (settingsStore.autoRefreshEnabled) {
    const intervalMs = settingsStore.refreshInterval * 60 * 1000
    refreshInterval = setInterval(loadData, intervalMs)
  }
}

function clearAutoRefresh() {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}
</script>
