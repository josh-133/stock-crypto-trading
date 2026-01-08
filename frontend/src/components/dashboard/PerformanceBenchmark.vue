<template>
  <div class="card">
    <h2 class="text-lg font-semibold text-theme-primary mb-4 flex items-center">
      Strategy vs Benchmark
      <Tooltip
        term="Benchmark Comparison"
        definition="Compare your strategy's return against SPY buy-and-hold. Outperforming the benchmark suggests the strategy adds value."
      />
    </h2>

    <div v-if="loading" class="text-theme-secondary text-center py-8">
      Loading benchmark data...
    </div>

    <div v-else-if="error" class="text-red-400 text-center py-8">
      {{ error }}
    </div>

    <div v-else class="space-y-4">
      <!-- Strategy Return -->
      <div class="flex justify-between items-center p-3 bg-theme-tertiary rounded-lg">
        <div>
          <p class="text-sm text-theme-secondary">Your Strategy</p>
          <p class="text-xs text-theme-muted">MA Crossover</p>
        </div>
        <div class="text-right">
          <p
            class="text-xl font-bold"
            :class="strategyReturn >= 0 ? 'text-profit' : 'text-loss'"
          >
            {{ strategyReturn >= 0 ? '+' : '' }}{{ strategyReturn.toFixed(2) }}%
          </p>
          <p class="text-xs text-theme-muted">
            ${{ formatNumber(portfolioValue) }}
          </p>
        </div>
      </div>

      <!-- Benchmark Return -->
      <div class="flex justify-between items-center p-3 bg-theme-tertiary rounded-lg">
        <div>
          <p class="text-sm text-theme-secondary">SPY Buy & Hold</p>
          <p class="text-xs text-theme-muted">{{ benchmark?.period_days || 0 }} days</p>
        </div>
        <div class="text-right">
          <p
            class="text-xl font-bold"
            :class="benchmarkReturn >= 0 ? 'text-profit' : 'text-loss'"
          >
            {{ benchmarkReturn >= 0 ? '+' : '' }}{{ benchmarkReturn.toFixed(2) }}%
          </p>
          <p class="text-xs text-theme-muted">
            ${{ formatNumber(benchmarkValue) }}
          </p>
        </div>
      </div>

      <!-- Performance Difference -->
      <div class="border-t border-theme pt-4">
        <div class="flex justify-between items-center">
          <span class="text-sm text-theme-secondary flex items-center">
            Alpha (Outperformance)
            <Tooltip
              term="Alpha"
              definition="The excess return over the benchmark. Positive alpha means your strategy beat buy-and-hold; negative means it underperformed."
            />
          </span>
          <span
            class="font-bold"
            :class="alpha >= 0 ? 'text-profit' : 'text-loss'"
          >
            {{ alpha >= 0 ? '+' : '' }}{{ alpha.toFixed(2) }}%
          </span>
        </div>

        <!-- Visual Bar -->
        <div class="mt-3 h-2 bg-theme-tertiary rounded-full overflow-hidden">
          <div
            class="h-full transition-all duration-500"
            :class="alpha >= 0 ? 'bg-green-500' : 'bg-red-500'"
            :style="{ width: barWidth }"
          ></div>
        </div>

        <p class="text-xs text-theme-muted mt-2">
          <span v-if="alpha > 0">
            Your strategy is outperforming SPY buy-and-hold by {{ alpha.toFixed(1) }} percentage points.
          </span>
          <span v-else-if="alpha < 0">
            Your strategy is underperforming SPY buy-and-hold by {{ Math.abs(alpha).toFixed(1) }} percentage points.
          </span>
          <span v-else>
            Your strategy is matching SPY buy-and-hold performance.
          </span>
        </p>
      </div>

      <!-- Period Info -->
      <div class="text-xs text-theme-muted text-center pt-2">
        Comparing from {{ benchmark?.start_date || 'N/A' }} to {{ benchmark?.end_date || 'N/A' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePortfolioStore } from '../../stores/portfolio'
import { useApi } from '../../composables/useApi'
import Tooltip from '../ui/Tooltip.vue'

const portfolioStore = usePortfolioStore()
const api = useApi()

const benchmark = ref(null)
const loading = ref(true)
const error = ref(null)

const INITIAL_CAPITAL = 10000

onMounted(async () => {
  await fetchBenchmark()
})

async function fetchBenchmark() {
  loading.value = true
  error.value = null
  try {
    benchmark.value = await api.getBenchmark(365)
  } catch (err) {
    console.error('Error fetching benchmark:', err)
    error.value = 'Failed to load benchmark data'
  } finally {
    loading.value = false
  }
}

const portfolioValue = computed(() => {
  return portfolioStore.portfolio?.total_value || INITIAL_CAPITAL
})

const strategyReturn = computed(() => {
  return portfolioStore.portfolio?.total_return_percent || 0
})

const benchmarkReturn = computed(() => {
  return benchmark.value?.spy_return_percent || 0
})

const benchmarkValue = computed(() => {
  // Calculate what $10k would be worth with buy-and-hold
  return INITIAL_CAPITAL * (1 + benchmarkReturn.value / 100)
})

const alpha = computed(() => {
  return strategyReturn.value - benchmarkReturn.value
})

const barWidth = computed(() => {
  // Normalize alpha to a percentage width (cap at 50% on either side)
  const maxAlpha = 50
  const normalized = Math.min(Math.abs(alpha.value), maxAlpha) / maxAlpha
  return `${normalized * 100}%`
})

function formatNumber(num) {
  return num.toLocaleString('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })
}
</script>
