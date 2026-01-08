<template>
  <div class="card">
    <h2 class="text-lg font-semibold text-white mb-4">Equity Curve</h2>

    <div ref="chartContainer" class="h-64 w-full"></div>

    <div class="mt-4 grid grid-cols-3 gap-4 text-sm">
      <div>
        <p class="text-gray-400">Start</p>
        <p class="text-white">${{ formatNumber(initialCapital) }}</p>
      </div>
      <div>
        <p class="text-gray-400">End</p>
        <p class="text-white">${{ formatNumber(finalValue) }}</p>
      </div>
      <div>
        <p class="text-gray-400">Return</p>
        <p :class="totalReturn >= 0 ? 'text-profit' : 'text-loss'">
          {{ totalReturn >= 0 ? '+' : '' }}{{ totalReturnPercent.toFixed(2) }}%
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { createChart } from 'lightweight-charts'

const props = defineProps({
  data: {
    type: Array,
    default: () => [],
  },
  initialCapital: {
    type: Number,
    default: 10000,
  },
  finalValue: {
    type: Number,
    default: 10000,
  },
})

const chartContainer = ref(null)
let chart = null
let areaSeries = null

const totalReturn = ref(0)
const totalReturnPercent = ref(0)

onMounted(() => {
  createChartInstance()
  updateChart()
})

onUnmounted(() => {
  if (chart) {
    chart.remove()
  }
})

watch(() => props.data, () => {
  updateChart()
}, { deep: true })

function createChartInstance() {
  chart = createChart(chartContainer.value, {
    layout: {
      background: { color: '#1f2937' },
      textColor: '#9ca3af',
    },
    grid: {
      vertLines: { color: '#374151' },
      horzLines: { color: '#374151' },
    },
    width: chartContainer.value.clientWidth,
    height: 256,
    timeScale: {
      timeVisible: true,
    },
  })

  areaSeries = chart.addAreaSeries({
    lineColor: '#3b82f6',
    topColor: 'rgba(59, 130, 246, 0.4)',
    bottomColor: 'rgba(59, 130, 246, 0.0)',
    lineWidth: 2,
  })

  window.addEventListener('resize', handleResize)
}

function handleResize() {
  if (chart && chartContainer.value) {
    chart.applyOptions({ width: chartContainer.value.clientWidth })
  }
}

function updateChart() {
  if (!props.data || props.data.length === 0) return

  const chartData = props.data.map(d => ({
    time: d.date.split('T')[0],
    value: d.value,
  }))

  areaSeries.setData(chartData)
  chart.timeScale().fitContent()

  // Calculate return
  totalReturn.value = props.finalValue - props.initialCapital
  totalReturnPercent.value = ((props.finalValue / props.initialCapital) - 1) * 100
}

function formatNumber(num) {
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>
