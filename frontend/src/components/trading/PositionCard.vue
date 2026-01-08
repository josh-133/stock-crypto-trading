<template>
  <div class="bg-theme-tertiary rounded-lg p-4">
    <div class="flex justify-between items-start mb-3">
      <div>
        <h3 class="text-lg font-semibold text-theme-primary">{{ position.symbol }}</h3>
        <p class="text-sm text-theme-secondary">{{ position.shares }} shares</p>
      </div>
      <button
        @click="handleSell"
        :disabled="selling"
        class="btn btn-danger text-sm"
      >
        {{ selling ? 'Selling...' : 'Sell' }}
      </button>
    </div>

    <!-- Price Info -->
    <div class="grid grid-cols-2 gap-4 mb-3">
      <div>
        <p class="text-xs text-theme-secondary flex items-center">
          Entry Price
          <Tooltip
            :term="tradingTerms.entryPrice.term"
            :definition="tradingTerms.entryPrice.definition"
          />
        </p>
        <p class="text-theme-primary">${{ position.entry_price.toFixed(2) }}</p>
      </div>
      <div>
        <p class="text-xs text-theme-secondary">Current Price</p>
        <p class="text-theme-primary">${{ position.current_price.toFixed(2) }}</p>
      </div>
    </div>

    <!-- P&L -->
    <div class="mb-3">
      <p class="text-xs text-theme-secondary flex items-center">
        Unrealized P&L
        <Tooltip
          :term="tradingTerms.unrealizedPnL.term"
          :definition="tradingTerms.unrealizedPnL.definition"
        />
      </p>
      <p
        class="text-lg font-semibold"
        :class="position.unrealized_pnl >= 0 ? 'text-profit' : 'text-loss'"
      >
        {{ position.unrealized_pnl >= 0 ? '+' : '' }}${{ position.unrealized_pnl.toFixed(2) }}
        ({{ position.unrealized_pnl_percent >= 0 ? '+' : '' }}{{ position.unrealized_pnl_percent.toFixed(2) }}%)
      </p>
    </div>

    <!-- Stop Loss Info -->
    <div class="border-t border-theme pt-3">
      <p class="text-xs text-theme-secondary mb-2 flex items-center">
        Stop Loss Protection
        <Tooltip
          :term="tradingTerms.stopLoss.term"
          :definition="tradingTerms.stopLoss.definition"
        />
      </p>
      <div class="grid grid-cols-2 gap-2 text-sm">
        <div>
          <p class="text-theme-muted flex items-center">
            Initial (7%)
            <Tooltip
              :term="tradingTerms.initialStop.term"
              :definition="tradingTerms.initialStop.definition"
            />
          </p>
          <p class="text-theme-primary">${{ position.initial_stop.toFixed(2) }}</p>
        </div>
        <div>
          <p class="text-theme-muted flex items-center">
            Trailing (10%)
            <Tooltip
              :term="tradingTerms.trailingStop.term"
              :definition="tradingTerms.trailingStop.definition"
            />
          </p>
          <p class="text-theme-primary">${{ position.trailing_stop.toFixed(2) }}</p>
        </div>
      </div>
      <div class="mt-2">
        <p class="text-theme-muted text-sm">Active Stop</p>
        <p class="text-yellow-400 font-medium">${{ position.active_stop.toFixed(2) }}</p>
        <p class="text-xs text-theme-muted mt-1">
          Highest: ${{ position.highest_price.toFixed(2) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { usePortfolioStore } from '../../stores/portfolio'
import { tradingTerms } from '../../composables/useTooltips'
import Tooltip from '../ui/Tooltip.vue'

const props = defineProps({
  position: {
    type: Object,
    required: true,
  },
})

const portfolioStore = usePortfolioStore()
const selling = ref(false)

async function handleSell() {
  if (selling.value) return

  selling.value = true
  try {
    await portfolioStore.executeSell(props.position.symbol)
  } catch (err) {
    console.error('Error selling:', err)
    alert(err.message || 'Failed to sell position')
  } finally {
    selling.value = false
  }
}
</script>
