<template>
  <div class="card">
    <h2 class="text-lg font-semibold text-theme-primary mb-4 flex items-center">
      Performance Metrics
      <Tooltip
        term="Performance Metrics"
        definition="Statistics showing how well your trading strategy has performed, including win rate, average gains/losses, and maximum drawdown."
      />
    </h2>

    <div v-if="!stats" class="text-theme-secondary">No trades yet</div>

    <div v-else class="grid grid-cols-2 gap-4">
      <!-- Total Trades -->
      <div>
        <p class="text-sm text-theme-secondary">Total Trades</p>
        <p class="text-xl font-medium text-theme-primary">{{ stats.total_trades }}</p>
      </div>

      <!-- Win Rate -->
      <div>
        <p class="text-sm text-theme-secondary flex items-center">
          Win Rate
          <Tooltip
            :term="tradingTerms.winRate.term"
            :definition="tradingTerms.winRate.definition"
          />
        </p>
        <p
          class="text-xl font-medium"
          :class="stats.win_rate >= 50 ? 'text-profit' : 'text-loss'"
        >
          {{ stats.win_rate.toFixed(1) }}%
        </p>
      </div>

      <!-- Winning Trades -->
      <div>
        <p class="text-sm text-theme-secondary">Winning</p>
        <p class="text-lg font-medium text-profit">{{ stats.winning_trades }}</p>
      </div>

      <!-- Losing Trades -->
      <div>
        <p class="text-sm text-theme-secondary">Losing</p>
        <p class="text-lg font-medium text-loss">{{ stats.losing_trades }}</p>
      </div>

      <!-- Average Win -->
      <div>
        <p class="text-sm text-theme-secondary">Avg Win</p>
        <p class="text-lg font-medium text-profit">
          ${{ formatNumber(stats.average_win) }}
        </p>
      </div>

      <!-- Average Loss -->
      <div>
        <p class="text-sm text-theme-secondary">Avg Loss</p>
        <p class="text-lg font-medium text-loss">
          ${{ formatNumber(Math.abs(stats.average_loss)) }}
        </p>
      </div>

      <!-- Max Drawdown -->
      <div class="col-span-2 pt-2 border-t border-theme">
        <p class="text-sm text-theme-secondary flex items-center">
          Max Drawdown
          <Tooltip
            :term="tradingTerms.drawdown.term"
            :definition="tradingTerms.drawdown.definition"
          />
        </p>
        <p class="text-lg font-medium text-loss">
          ${{ formatNumber(stats.max_drawdown) }}
          ({{ stats.max_drawdown_percent.toFixed(1) }}%)
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePortfolioStore } from '../../stores/portfolio'
import { tradingTerms } from '../../composables/useTooltips'
import Tooltip from '../ui/Tooltip.vue'

const portfolioStore = usePortfolioStore()

const stats = computed(() => portfolioStore.stats)

function formatNumber(num) {
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>
