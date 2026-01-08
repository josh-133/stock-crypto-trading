<template>
  <div class="card">
    <h2 class="text-lg font-semibold text-theme-primary mb-4">Portfolio Summary</h2>

    <div v-if="loading" class="text-theme-secondary">Loading...</div>

    <div v-else-if="portfolio" class="space-y-4">
      <!-- Total Value -->
      <div class="flex justify-between items-center">
        <span class="text-theme-secondary flex items-center">
          Total Value
          <Tooltip
            :term="tradingTerms.totalValue.term"
            :definition="tradingTerms.totalValue.definition"
          />
        </span>
        <span class="text-2xl font-bold text-theme-primary">
          ${{ formatNumber(portfolio.total_value) }}
        </span>
      </div>

      <!-- Total Return -->
      <div class="flex justify-between items-center">
        <span class="text-theme-secondary flex items-center">
          Total Return
          <Tooltip
            :term="tradingTerms.totalReturn.term"
            :definition="tradingTerms.totalReturn.definition"
          />
        </span>
        <span
          class="text-lg font-semibold"
          :class="portfolio.total_return >= 0 ? 'text-profit' : 'text-loss'"
        >
          {{ portfolio.total_return >= 0 ? '+' : '' }}${{ formatNumber(portfolio.total_return) }}
          ({{ portfolio.total_return_percent >= 0 ? '+' : '' }}{{ portfolio.total_return_percent.toFixed(2) }}%)
        </span>
      </div>

      <hr class="border-theme" />

      <!-- Cash & Invested -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <p class="text-sm text-theme-secondary flex items-center">
            Cash
            <Tooltip
              :term="tradingTerms.cash.term"
              :definition="tradingTerms.cash.definition"
            />
          </p>
          <p class="text-lg font-medium text-theme-primary">${{ formatNumber(portfolio.cash) }}</p>
        </div>
        <div>
          <p class="text-sm text-theme-secondary flex items-center">
            Invested
            <Tooltip
              :term="tradingTerms.invested.term"
              :definition="tradingTerms.invested.definition"
            />
          </p>
          <p class="text-lg font-medium text-theme-primary">${{ formatNumber(portfolio.invested_value) }}</p>
        </div>
      </div>

      <!-- Daily P&L -->
      <div class="flex justify-between items-center pt-2">
        <span class="text-sm text-theme-secondary flex items-center">
          Daily P&L
          <Tooltip
            :term="tradingTerms.PnL.term"
            :definition="tradingTerms.PnL.definition"
          />
        </span>
        <span
          class="text-sm"
          :class="portfolio.daily_pnl >= 0 ? 'text-profit' : 'text-loss'"
        >
          {{ portfolio.daily_pnl >= 0 ? '+' : '' }}${{ formatNumber(portfolio.daily_pnl) }}
          ({{ portfolio.daily_pnl_percent >= 0 ? '+' : '' }}{{ portfolio.daily_pnl_percent.toFixed(2) }}%)
        </span>
      </div>

      <!-- Positions Count -->
      <div class="flex justify-between items-center">
        <span class="text-sm text-theme-secondary">Open Positions</span>
        <span class="text-sm text-theme-primary">{{ portfolio.positions.length }} / 3</span>
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

const portfolio = computed(() => portfolioStore.portfolio)
const loading = computed(() => portfolioStore.loading)

function formatNumber(num) {
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>
