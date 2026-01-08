<template>
  <div class="card">
    <h2 class="text-lg font-semibold text-theme-primary mb-4 flex items-center">
      Portfolio Allocation
      <Tooltip
        term="Portfolio Allocation"
        definition="Visual breakdown of how your portfolio value is distributed across cash and stock positions."
      />
    </h2>

    <div v-if="!portfolio" class="text-theme-secondary text-center py-8">
      Loading portfolio data...
    </div>

    <div v-else class="flex flex-col md:flex-row items-center gap-6">
      <!-- Pie Chart SVG -->
      <div class="relative">
        <svg :width="size" :height="size" class="transform -rotate-90">
          <circle
            v-for="(slice, index) in slices"
            :key="index"
            :cx="center"
            :cy="center"
            :r="radius"
            fill="transparent"
            :stroke="slice.color"
            :stroke-width="strokeWidth"
            :stroke-dasharray="slice.dashArray"
            :stroke-dashoffset="slice.dashOffset"
            class="transition-all duration-500"
          />
        </svg>
        <!-- Center text -->
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <span class="text-2xl font-bold text-theme-primary">
            ${{ formatNumber(portfolio.total_value) }}
          </span>
          <span class="text-xs text-theme-secondary">Total Value</span>
        </div>
      </div>

      <!-- Legend -->
      <div class="flex-1 space-y-3">
        <div
          v-for="(item, index) in legendItems"
          :key="index"
          class="flex items-center justify-between"
        >
          <div class="flex items-center space-x-2">
            <span
              class="w-3 h-3 rounded-full"
              :style="{ backgroundColor: item.color }"
            ></span>
            <span class="text-sm text-theme-primary">{{ item.label }}</span>
          </div>
          <div class="text-right">
            <span class="text-sm font-medium text-theme-primary">
              ${{ formatNumber(item.value) }}
            </span>
            <span class="text-xs text-theme-secondary ml-2">
              ({{ item.percent.toFixed(1) }}%)
            </span>
          </div>
        </div>

        <!-- Diversification Note -->
        <div class="mt-4 pt-4 border-t border-theme">
          <p class="text-xs text-theme-muted">
            <span v-if="portfolio.positions.length === 0">
              No positions held. Portfolio is 100% cash.
            </span>
            <span v-else-if="portfolio.positions.length < 3">
              {{ 3 - portfolio.positions.length }} more position(s) available for diversification.
            </span>
            <span v-else>
              Maximum positions reached (3/3).
            </span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePortfolioStore } from '../../stores/portfolio'
import Tooltip from '../ui/Tooltip.vue'

const portfolioStore = usePortfolioStore()
const portfolio = computed(() => portfolioStore.portfolio)

// Chart dimensions
const size = 180
const center = size / 2
const strokeWidth = 35
const radius = (size - strokeWidth) / 2
const circumference = 2 * Math.PI * radius

// Color palette for positions
const colors = {
  cash: '#6b7280', // gray-500
  AAPL: '#3b82f6', // blue-500
  MSFT: '#10b981', // emerald-500
  GOOGL: '#f97316', // orange-500
  SPY: '#8b5cf6', // violet-500
}

const legendItems = computed(() => {
  if (!portfolio.value) return []

  const items = []
  const total = portfolio.value.total_value || 1

  // Add cash
  items.push({
    label: 'Cash',
    value: portfolio.value.cash,
    percent: (portfolio.value.cash / total) * 100,
    color: colors.cash,
  })

  // Add positions
  for (const position of portfolio.value.positions) {
    const positionValue = position.shares * position.current_price
    items.push({
      label: position.symbol,
      value: positionValue,
      percent: (positionValue / total) * 100,
      color: colors[position.symbol] || '#64748b',
    })
  }

  return items
})

const slices = computed(() => {
  if (!legendItems.value.length) return []

  const result = []
  let cumulativePercent = 0

  for (const item of legendItems.value) {
    const percent = item.percent / 100
    const dashArray = `${circumference * percent} ${circumference * (1 - percent)}`
    const dashOffset = -circumference * cumulativePercent

    result.push({
      color: item.color,
      dashArray,
      dashOffset,
    })

    cumulativePercent += percent
  }

  return result
})

function formatNumber(num) {
  return num.toLocaleString('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })
}
</script>
