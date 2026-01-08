<template>
  <div class="relative">
    <div class="flex gap-2">
      <input
        v-model="searchQuery"
        @input="handleInput"
        @keydown.enter="handleAddSymbol"
        type="text"
        placeholder="Enter stock symbol (e.g., NVDA)"
        class="input flex-1 uppercase"
        :disabled="disabled"
      />
      <button
        @click="handleAddSymbol"
        :disabled="!searchQuery || loading || disabled"
        class="btn btn-primary"
      >
        {{ loading ? 'Adding...' : 'Add' }}
      </button>
    </div>

    <!-- Search Results Dropdown -->
    <div
      v-if="showResults && results.length > 0"
      class="absolute z-10 w-full mt-1 bg-theme-secondary rounded-lg shadow-lg border border-theme-tertiary"
    >
      <button
        v-for="result in results"
        :key="result.symbol"
        @click="selectResult(result)"
        class="w-full px-4 py-3 text-left hover:bg-theme-tertiary transition-colors first:rounded-t-lg last:rounded-b-lg"
        :disabled="result.in_watchlist"
      >
        <div class="flex justify-between items-center">
          <div>
            <span class="font-medium text-theme-primary">{{ result.symbol }}</span>
            <span class="text-sm text-theme-secondary ml-2">{{ result.name }}</span>
          </div>
          <div class="text-right">
            <span v-if="result.price" class="text-theme-primary">${{ result.price.toFixed(2) }}</span>
            <span v-if="result.in_watchlist" class="text-xs text-theme-muted ml-2">(already added)</span>
          </div>
        </div>
      </button>
    </div>

    <!-- Validation Status -->
    <div v-if="validating" class="mt-2 text-sm text-theme-secondary">
      Validating symbol...
    </div>
    <div v-if="validationError" class="mt-2 text-sm text-red-500">
      {{ validationError }}
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useWatchlistStore } from '../../stores/watchlist'
import { useToast } from '../../composables/useToast'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['added'])

const watchlistStore = useWatchlistStore()
const toast = useToast()

const searchQuery = ref('')
const results = ref([])
const showResults = ref(false)
const loading = ref(false)
const validating = ref(false)
const validationError = ref('')

let searchTimeout = null

function handleInput() {
  validationError.value = ''

  // Debounce search
  clearTimeout(searchTimeout)

  if (searchQuery.value.length >= 1) {
    searchTimeout = setTimeout(async () => {
      validating.value = true
      results.value = await watchlistStore.searchSymbols(searchQuery.value)
      showResults.value = results.value.length > 0
      validating.value = false
    }, 300)
  } else {
    results.value = []
    showResults.value = false
  }
}

function selectResult(result) {
  if (result.in_watchlist) return
  searchQuery.value = result.symbol
  showResults.value = false
  handleAddSymbol()
}

async function handleAddSymbol() {
  if (!searchQuery.value) return

  const symbol = searchQuery.value.toUpperCase().trim()

  if (watchlistStore.isInWatchlist(symbol)) {
    toast.warning(`${symbol} is already in your watchlist`)
    return
  }

  loading.value = true
  validationError.value = ''

  const result = await watchlistStore.addSymbol(symbol)

  if (result.success) {
    toast.success(result.message)
    searchQuery.value = ''
    results.value = []
    showResults.value = false
    emit('added', symbol)
  } else {
    validationError.value = result.message
    toast.error(result.message)
  }

  loading.value = false
}

// Close dropdown when clicking outside
watch(showResults, (show) => {
  if (show) {
    const closeOnClick = (e) => {
      if (!e.target.closest('.relative')) {
        showResults.value = false
        document.removeEventListener('click', closeOnClick)
      }
    }
    setTimeout(() => document.addEventListener('click', closeOnClick), 0)
  }
})
</script>
