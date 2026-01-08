<template>
  <div class="card">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-semibold text-white">{{ symbol }} Price Chart</h2>
      <div class="flex space-x-2">
        <button
          v-for="s in symbols"
          :key="s"
          @click="changeSymbol(s)"
          class="px-3 py-1 rounded text-sm"
          :class="symbol === s ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
        >
          {{ s }}
        </button>
      </div>
    </div>

    <div ref="chartContainer" class="h-96 w-full"></div>

    <!-- Legend -->
    <div class="mt-4 flex items-center space-x-6 text-sm">
      <span class="flex items-center">
        <span class="w-3 h-0.5 bg-blue-500 mr-2"></span>
        SMA 10
      </span>
      <span class="flex items-center">
        <span class="w-3 h-0.5 bg-orange-500 mr-2"></span>
        SMA 50
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { createChart } from 'lightweight-charts'
import { useStocksStore } from '../../stores/stocks'

const stocksStore = useStocksStore()

const chartContainer = ref(null)
const symbol = ref('SPY')
const symbols = ['AAPL', 'MSFT', 'GOOGL', 'SPY']

let chart = null
let candlestickSeries = null
let sma10Series = null
let sma50Series = null

onMounted(async () => {
  createChartInstance()
  await loadData()
})

onUnmounted(() => {
  if (chart) {
    chart.remove()
  }
})

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
    height: 384,
    timeScale: {
      timeVisible: true,
      secondsVisible: false,
    },
  })

  // Candlestick series
  candlestickSeries = chart.addCandlestickSeries({
    upColor: '#10b981',
    downColor: '#ef4444',
    borderUpColor: '#10b981',
    borderDownColor: '#ef4444',
    wickUpColor: '#10b981',
    wickDownColor: '#ef4444',
  })

  // SMA 10 line
  sma10Series = chart.addLineSeries({
    color: '#3b82f6',
    lineWidth: 2,
    title: 'SMA 10',
  })

  // SMA 50 line
  sma50Series = chart.addLineSeries({
    color: '#f97316',
    lineWidth: 2,
    title: 'SMA 50',
  })

  // Handle resize
  window.addEventListener('resize', handleResize)
}

function handleResize() {
  if (chart && chartContainer.value) {
    chart.applyOptions({ width: chartContainer.value.clientWidth })
  }
}

async function loadData() {
  try {
    const data = await stocksStore.fetchStockData(symbol.value)

    // Convert to chart format
    const candleData = data.prices.map(p => ({
      time: p.date.split('T')[0],
      open: p.open,
      high: p.high,
      low: p.low,
      close: p.close,
    }))

    const sma10Data = data.sma_10
      .map((v, i) => ({
        time: data.prices[i].date.split('T')[0],
        value: v,
      }))
      .filter(d => d.value !== null)

    const sma50Data = data.sma_50
      .map((v, i) => ({
        time: data.prices[i].date.split('T')[0],
        value: v,
      }))
      .filter(d => d.value !== null)

    candlestickSeries.setData(candleData)
    sma10Series.setData(sma10Data)
    sma50Series.setData(sma50Data)

    chart.timeScale().fitContent()
  } catch (err) {
    console.error('Error loading chart data:', err)
  }
}

async function changeSymbol(newSymbol) {
  symbol.value = newSymbol
  stocksStore.setSelectedSymbol(newSymbol)
  await loadData()
}

watch(() => stocksStore.selectedSymbol, (newSymbol) => {
  if (newSymbol !== symbol.value) {
    symbol.value = newSymbol
    loadData()
  }
})
</script>
