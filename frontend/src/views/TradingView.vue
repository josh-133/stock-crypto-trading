<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-white">Trading</h1>
      <button
        @click="checkStops"
        class="btn btn-secondary"
      >
        Check Stop Losses
      </button>
    </div>

    <!-- Risk Warning -->
    <div class="bg-blue-900 border border-blue-700 rounded-lg p-4">
      <p class="text-blue-300 text-sm">
        <strong>Strategy Rules:</strong>
        Buy on Golden Cross (10-day MA crosses above 50-day MA).
        Position size is auto-calculated using the 2% risk rule.
        Stop loss at 7% below entry, trailing stop at 10% below highest price.
      </p>
    </div>

    <!-- Top Row: Signal Scanner + Trade Form -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2">
        <SignalScanner />
      </div>
      <div>
        <TradeForm />
      </div>
    </div>

    <!-- Chart -->
    <PriceChart />

    <!-- Open Positions -->
    <div class="card">
      <h2 class="text-lg font-semibold text-white mb-4">
        Open Positions ({{ positions.length }}/3)
      </h2>

      <div v-if="positions.length === 0" class="text-gray-400 text-center py-8">
        No open positions. Use the Signal Scanner above to find buy signals.
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <PositionCard
          v-for="position in positions"
          :key="position.symbol"
          :position="position"
        />
      </div>
    </div>

    <!-- Trade History -->
    <div class="card">
      <h2 class="text-lg font-semibold text-white mb-4">Trade History</h2>

      <div v-if="trades.length === 0" class="text-gray-400 text-center py-4">
        No trades yet
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-gray-400 border-b border-gray-700">
              <th class="pb-2">Date</th>
              <th class="pb-2">Symbol</th>
              <th class="pb-2">Action</th>
              <th class="pb-2">Shares</th>
              <th class="pb-2">Price</th>
              <th class="pb-2">P&L</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="trade in trades"
              :key="trade.id"
              class="border-b border-gray-700"
            >
              <td class="py-2 text-white">{{ formatDate(trade.timestamp) }}</td>
              <td class="py-2 text-white font-medium">{{ trade.symbol }}</td>
              <td class="py-2">
                <span
                  :class="trade.action === 'buy' ? 'text-green-400' : 'text-red-400'"
                >
                  {{ trade.action.toUpperCase() }}
                </span>
              </td>
              <td class="py-2 text-white">{{ trade.shares }}</td>
              <td class="py-2 text-white">${{ trade.price.toFixed(2) }}</td>
              <td class="py-2">
                <span
                  v-if="trade.pnl !== null"
                  :class="trade.pnl >= 0 ? 'text-profit' : 'text-loss'"
                >
                  {{ trade.pnl >= 0 ? '+' : '' }}${{ trade.pnl.toFixed(2) }}
                </span>
                <span v-else class="text-gray-500">-</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { usePortfolioStore } from '../stores/portfolio'
import { useSignalsStore } from '../stores/signals'
import { useToast } from '../composables/useToast'
import SignalScanner from '../components/trading/SignalScanner.vue'
import TradeForm from '../components/trading/TradeForm.vue'
import PriceChart from '../components/charts/PriceChart.vue'
import PositionCard from '../components/trading/PositionCard.vue'

const portfolioStore = usePortfolioStore()
const signalsStore = useSignalsStore()
const toast = useToast()

const positions = computed(() => portfolioStore.positions)
const trades = computed(() => portfolioStore.trades)

onMounted(async () => {
  await Promise.all([
    portfolioStore.fetchPortfolio(),
    portfolioStore.fetchTrades(),
    signalsStore.fetchSignals(),
  ])
})

async function checkStops() {
  const result = await portfolioStore.checkStops()
  if (result && result.triggered_count > 0) {
    toast.warning(`${result.triggered_count} position(s) hit stop loss and were sold.`)
  } else {
    toast.info('No positions hit their stop loss.')
  }
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>
