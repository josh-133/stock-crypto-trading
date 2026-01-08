<template>
  <div class="card">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-semibold text-theme-primary flex items-center">
        Signal Scanner
        <Tooltip
          term="Signal Scanner"
          definition="Monitors stocks for buy and sell signals based on the moving average crossover strategy."
        />
      </h2>
      <button @click="refresh" class="text-sm text-blue-400 hover:text-blue-300">
        Refresh
      </button>
    </div>

    <div v-if="loading" class="text-theme-secondary">Scanning...</div>

    <div v-else class="space-y-3">
      <div
        v-for="signal in signals"
        :key="signal.symbol"
        class="flex items-center justify-between p-3 bg-theme-tertiary rounded-lg"
      >
        <div class="flex items-center space-x-3">
          <span class="font-medium text-theme-primary">{{ signal.symbol }}</span>
          <span class="text-sm text-theme-secondary">${{ signal.price.toFixed(2) }}</span>
        </div>

        <div class="flex items-center space-x-2">
          <!-- Signal Badge -->
          <span
            class="signal-badge"
            :class="getSignalClass(signal.signal_type)"
          >
            {{ getSignalLabel(signal.signal_type) }}
          </span>

          <!-- Days since signal -->
          <span
            v-if="signal.days_since_signal !== null"
            class="text-xs text-theme-muted"
          >
            {{ signal.days_since_signal }}d ago
          </span>
        </div>
      </div>

      <div v-if="signals.length === 0" class="text-theme-secondary text-center py-4">
        No active signals
      </div>
    </div>

    <!-- Legend -->
    <div class="mt-4 pt-4 border-t border-theme">
      <p class="text-xs text-theme-muted mb-2">Signal Legend:</p>
      <div class="flex space-x-4 text-xs text-theme-secondary">
        <span class="flex items-center">
          <span class="w-2 h-2 bg-green-500 rounded-full mr-1"></span>
          Golden Cross (Buy)
          <Tooltip
            :term="tradingTerms.goldenCross.term"
            :definition="tradingTerms.goldenCross.definition"
          />
        </span>
        <span class="flex items-center">
          <span class="w-2 h-2 bg-red-500 rounded-full mr-1"></span>
          Death Cross (Sell)
          <Tooltip
            :term="tradingTerms.deathCross.term"
            :definition="tradingTerms.deathCross.definition"
          />
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSignalsStore } from '../../stores/signals'
import { tradingTerms } from '../../composables/useTooltips'
import Tooltip from '../ui/Tooltip.vue'

const signalsStore = useSignalsStore()

const signals = computed(() => signalsStore.signals)
const loading = computed(() => signalsStore.loading)

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
      return 'No Signal'
  }
}
</script>
