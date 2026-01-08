<template>
  <div class="card">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-semibold text-white">Signal Scanner</h2>
      <button @click="refresh" class="btn btn-secondary text-sm">
        Refresh
      </button>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full">
        <thead>
          <tr class="text-left text-sm text-gray-400 border-b border-gray-700">
            <th class="pb-2">Symbol</th>
            <th class="pb-2">Price</th>
            <th class="pb-2">SMA 10</th>
            <th class="pb-2">SMA 50</th>
            <th class="pb-2">Signal</th>
            <th class="pb-2">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="signal in signals"
            :key="signal.symbol"
            class="border-b border-gray-700"
          >
            <td class="py-3 font-medium text-white">{{ signal.symbol }}</td>
            <td class="py-3 text-white">${{ signal.price.toFixed(2) }}</td>
            <td class="py-3 text-blue-400">${{ signal.sma_10.toFixed(2) }}</td>
            <td class="py-3 text-orange-400">${{ signal.sma_50.toFixed(2) }}</td>
            <td class="py-3">
              <span
                class="signal-badge"
                :class="getSignalClass(signal.signal_type)"
              >
                {{ getSignalLabel(signal.signal_type) }}
              </span>
            </td>
            <td class="py-3">
              <button
                v-if="signal.signal_type === 'golden_cross' && !hasPosition(signal.symbol)"
                @click="handleBuy(signal.symbol)"
                :disabled="maxPositionsReached"
                class="btn btn-success text-xs"
                :class="{ 'opacity-50 cursor-not-allowed': maxPositionsReached }"
              >
                Buy
              </button>
              <button
                v-else-if="hasPosition(signal.symbol)"
                @click="handleSell(signal.symbol)"
                class="btn btn-danger text-xs"
              >
                Sell
              </button>
              <span v-else class="text-gray-500 text-sm">-</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="loading" class="text-center py-4 text-gray-400">
      Loading signals...
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSignalsStore } from '../../stores/signals'
import { usePortfolioStore } from '../../stores/portfolio'

const signalsStore = useSignalsStore()
const portfolioStore = usePortfolioStore()

const signals = computed(() => signalsStore.signals)
const loading = computed(() => signalsStore.loading)

const maxPositionsReached = computed(() =>
  portfolioStore.positions.length >= 3
)

function hasPosition(symbol) {
  return portfolioStore.positions.some(p => p.symbol === symbol)
}

function refresh() {
  signalsStore.fetchSignals()
}

function getSignalClass(type) {
  switch (type) {
    case 'golden_cross':
      return 'signal-golden'
    case 'death_cross':
      return 'signal-death'
    default:
      return 'signal-none'
  }
}

function getSignalLabel(type) {
  switch (type) {
    case 'golden_cross':
      return 'Golden Cross'
    case 'death_cross':
      return 'Death Cross'
    default:
      return 'None'
  }
}

async function handleBuy(symbol) {
  try {
    const trade = await portfolioStore.executeBuy(symbol)
    alert(`Bought ${trade.shares} shares of ${symbol} at $${trade.price.toFixed(2)}`)
  } catch (err) {
    alert(err.message || 'Trade failed')
  }
}

async function handleSell(symbol) {
  try {
    const trade = await portfolioStore.executeSell(symbol)
    const pnlStr = trade.pnl >= 0 ? `+$${trade.pnl.toFixed(2)}` : `-$${Math.abs(trade.pnl).toFixed(2)}`
    alert(`Sold ${symbol} at $${trade.price.toFixed(2)}. P&L: ${pnlStr}`)
  } catch (err) {
    alert(err.message || 'Sell failed')
  }
}
</script>
