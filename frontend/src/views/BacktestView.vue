<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-white">Backtest</h1>

    <!-- Info Box -->
    <div class="bg-purple-900 border border-purple-700 rounded-lg p-4">
      <p class="text-purple-300 text-sm">
        <strong>About Backtesting:</strong>
        Test how the 10/50 MA Crossover strategy would have performed on historical data.
        Remember: past performance does NOT guarantee future results.
        Markets change, and strategies that worked before may not work in the future.
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div>
        <BacktestForm ref="formRef" @run="runBacktest" />
      </div>

      <div class="lg:col-span-2">
        <div v-if="loading" class="card flex items-center justify-center h-64">
          <div class="text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p class="text-gray-400">Running backtest...</p>
          </div>
        </div>

        <div v-else-if="error" class="card bg-red-900 border border-red-700">
          <p class="text-red-300">{{ error }}</p>
        </div>

        <div v-else-if="!results" class="card flex items-center justify-center h-64">
          <div class="text-center text-gray-400">
            <p class="text-4xl mb-2">📊</p>
            <p>Configure and run a backtest to see results</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Results -->
    <BacktestResults v-if="results && !loading" :results="results" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useApi } from '../composables/useApi'
import BacktestForm from '../components/backtest/BacktestForm.vue'
import BacktestResults from '../components/backtest/BacktestResults.vue'

const api = useApi()

const formRef = ref(null)
const results = ref(null)
const loading = ref(false)
const error = ref(null)

async function runBacktest(params) {
  loading.value = true
  error.value = null

  try {
    results.value = await api.runBacktest(
      params.symbol,
      params.startDate,
      params.endDate,
      params.initialCapital
    )
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Backtest failed'
    results.value = null
  } finally {
    loading.value = false
    if (formRef.value) {
      formRef.value.setLoading(false)
    }
  }
}
</script>
