<template>
  <div class="card">
    <h2 class="text-lg font-semibold text-white mb-4">Run Backtest</h2>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Symbol Selection -->
      <div>
        <label class="label">Symbol</label>
        <select v-model="symbol" class="input w-full">
          <option v-for="s in symbols" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>

      <!-- Date Range (Optional) -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">Start Date (Optional)</label>
          <input
            type="date"
            v-model="startDate"
            class="input w-full"
          />
        </div>
        <div>
          <label class="label">End Date (Optional)</label>
          <input
            type="date"
            v-model="endDate"
            class="input w-full"
          />
        </div>
      </div>

      <!-- Initial Capital -->
      <div>
        <label class="label">Initial Capital</label>
        <input
          type="number"
          v-model.number="initialCapital"
          class="input w-full"
          min="1000"
          step="1000"
        />
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        :disabled="loading"
        class="btn btn-primary w-full"
      >
        {{ loading ? 'Running Backtest...' : 'Run Backtest' }}
      </button>
    </form>

    <!-- Disclaimer -->
    <p class="mt-4 text-xs text-gray-500">
      Past performance does not guarantee future results.
      Backtesting shows hypothetical results only.
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['run'])

const symbols = ['AAPL', 'MSFT', 'GOOGL', 'SPY']
const symbol = ref('SPY')
const startDate = ref('')
const endDate = ref('')
const initialCapital = ref(10000)
const loading = ref(false)

async function handleSubmit() {
  loading.value = true
  emit('run', {
    symbol: symbol.value,
    startDate: startDate.value || null,
    endDate: endDate.value || null,
    initialCapital: initialCapital.value,
  })
}

defineExpose({
  setLoading: (val) => { loading.value = val }
})
</script>
