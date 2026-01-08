<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-theme-primary">Settings</h1>

    <!-- Appearance & Notifications -->
    <div class="card">
      <h2 class="text-lg font-semibold text-theme-primary mb-4">Appearance & Notifications</h2>

      <div class="space-y-4">
        <!-- Theme Toggle -->
        <div class="flex justify-between items-center">
          <div>
            <p class="text-theme-primary">Theme</p>
            <p class="text-sm text-theme-secondary">
              Switch between dark and light mode
            </p>
          </div>
          <button
            @click="settingsStore.toggleTheme"
            class="btn btn-secondary flex items-center space-x-2"
          >
            <span>{{ settingsStore.isDarkMode ? '☀️ Light Mode' : '🌙 Dark Mode' }}</span>
          </button>
        </div>

        <!-- Sound Alerts -->
        <div class="flex justify-between items-center">
          <div>
            <p class="text-theme-primary">Sound Alerts</p>
            <p class="text-sm text-theme-secondary">
              Play sounds when signals trigger
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="testSound"
              class="btn btn-secondary text-sm"
            >
              Test
            </button>
            <button
              @click="settingsStore.toggleSound"
              class="btn"
              :class="settingsStore.soundEnabled ? 'btn-success' : 'btn-secondary'"
            >
              {{ settingsStore.soundEnabled ? '🔔 On' : '🔕 Off' }}
            </button>
          </div>
        </div>

        <!-- Auto-Refresh -->
        <div class="flex justify-between items-center">
          <div>
            <p class="text-theme-primary">Auto-Refresh Signals</p>
            <p class="text-sm text-theme-secondary">
              Automatically refresh signals at set interval
            </p>
          </div>
          <div class="flex items-center space-x-3">
            <select
              v-model="settingsStore.refreshInterval"
              class="input text-sm"
              :disabled="!settingsStore.autoRefreshEnabled"
            >
              <option :value="1">1 min</option>
              <option :value="5">5 min</option>
              <option :value="15">15 min</option>
              <option :value="30">30 min</option>
            </select>
            <button
              @click="settingsStore.toggleAutoRefresh"
              class="btn"
              :class="settingsStore.autoRefreshEnabled ? 'btn-success' : 'btn-secondary'"
            >
              {{ settingsStore.autoRefreshEnabled ? 'On' : 'Off' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Data Export -->
    <div class="card">
      <h2 class="text-lg font-semibold text-theme-primary mb-4">Export Data</h2>
      <p class="text-sm text-theme-secondary mb-4">
        Download your trading data as CSV files for analysis in Excel or Google Sheets.
      </p>

      <div class="flex flex-wrap gap-3">
        <button @click="handleExportTrades" class="btn btn-primary">
          📥 Export Trades
        </button>
        <button @click="handleExportPortfolio" class="btn btn-primary">
          📥 Export Portfolio
        </button>
      </div>
    </div>

    <!-- Portfolio Reset -->
    <div class="card">
      <h2 class="text-lg font-semibold text-theme-primary mb-4">Portfolio</h2>

      <div class="space-y-4">
        <div class="flex justify-between items-center">
          <div>
            <p class="text-theme-primary">Reset Portfolio</p>
            <p class="text-sm text-theme-secondary">
              Clear all positions and trades, reset to $10,000
            </p>
          </div>
          <button
            @click="handleReset"
            :disabled="resetting"
            class="btn btn-danger"
          >
            {{ resetting ? 'Resetting...' : 'Reset Portfolio' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Strategy Settings (Read-only for learning) -->
    <div class="card">
      <h2 class="text-lg font-semibold text-theme-primary mb-4">
        Strategy Parameters
        <Tooltip
          term="Strategy Parameters"
          definition="The fixed rules that define when to buy, sell, and how much to risk. These are set for learning purposes."
          position="right"
        />
      </h2>
      <p class="text-sm text-theme-secondary mb-4">
        These settings are fixed for the learning strategy.
        Understanding why these values were chosen is part of learning.
      </p>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <p class="text-sm text-theme-secondary flex items-center">
            Short MA Period
            <Tooltip
              :term="tradingTerms.SMA_10.term"
              :definition="tradingTerms.SMA_10.definition"
            />
          </p>
          <p class="text-theme-primary text-lg">10 days</p>
          <p class="text-xs text-theme-muted">~2 weeks of trading</p>
        </div>
        <div>
          <p class="text-sm text-theme-secondary flex items-center">
            Long MA Period
            <Tooltip
              :term="tradingTerms.SMA_50.term"
              :definition="tradingTerms.SMA_50.definition"
            />
          </p>
          <p class="text-theme-primary text-lg">50 days</p>
          <p class="text-xs text-theme-muted">~2.5 months of trading</p>
        </div>
        <div>
          <p class="text-sm text-theme-secondary flex items-center">
            Initial Stop Loss
            <Tooltip
              :term="tradingTerms.initialStop.term"
              :definition="tradingTerms.initialStop.definition"
            />
          </p>
          <p class="text-theme-primary text-lg">7%</p>
          <p class="text-xs text-theme-muted">Limits loss if signal is wrong</p>
        </div>
        <div>
          <p class="text-sm text-theme-secondary flex items-center">
            Trailing Stop
            <Tooltip
              :term="tradingTerms.trailingStop.term"
              :definition="tradingTerms.trailingStop.definition"
            />
          </p>
          <p class="text-theme-primary text-lg">10%</p>
          <p class="text-xs text-theme-muted">Protects profits as price rises</p>
        </div>
        <div>
          <p class="text-sm text-theme-secondary flex items-center">
            Max Risk Per Trade
            <Tooltip
              :term="tradingTerms.riskPerTrade.term"
              :definition="tradingTerms.riskPerTrade.definition"
            />
          </p>
          <p class="text-theme-primary text-lg">2%</p>
          <p class="text-xs text-theme-muted">Survives losing streaks</p>
        </div>
        <div>
          <p class="text-sm text-theme-secondary flex items-center">
            Max Position Size
            <Tooltip
              :term="tradingTerms.maxPosition.term"
              :definition="tradingTerms.maxPosition.definition"
            />
          </p>
          <p class="text-theme-primary text-lg">33%</p>
          <p class="text-xs text-theme-muted">Forces diversification</p>
        </div>
      </div>
    </div>

    <!-- Stock Watchlist -->
    <div class="card">
      <h2 class="text-lg font-semibold text-theme-primary mb-4">
        Stock Watchlist
        <span class="text-sm font-normal text-theme-secondary ml-2">
          ({{ watchlistStore.count }}/{{ watchlistStore.maxSize }})
        </span>
      </h2>
      <p class="text-sm text-theme-secondary mb-4">
        Add any US stock to your watchlist. Signals will be scanned for these symbols.
      </p>

      <!-- Add Stock Search -->
      <div class="mb-4">
        <StockSearch :disabled="watchlistStore.isFull" @added="onSymbolAdded" />
        <p v-if="watchlistStore.isFull" class="text-sm text-yellow-500 mt-2">
          Watchlist is full. Remove a symbol to add more.
        </p>
      </div>

      <!-- Watchlist Symbols -->
      <div v-if="watchlistStore.loading && watchlistStore.count === 0" class="text-theme-secondary">
        Loading watchlist...
      </div>
      <div v-else class="flex flex-wrap gap-2">
        <span
          v-for="symbol in watchlistStore.symbols"
          :key="symbol"
          class="group px-3 py-1 rounded-full text-theme-primary bg-theme-tertiary flex items-center gap-2"
        >
          {{ symbol }}
          <button
            @click="handleRemoveSymbol(symbol)"
            class="opacity-50 hover:opacity-100 hover:text-red-500 transition-opacity"
            title="Remove from watchlist"
          >
            x
          </button>
        </span>
      </div>
    </div>

    <!-- Educational Info -->
    <div class="card">
      <h2 class="text-lg font-semibold text-theme-primary mb-4">Learning Resources</h2>

      <div class="space-y-4 text-sm">
        <div>
          <h3 class="text-theme-primary font-medium flex items-center">
            Why 10/50 Moving Averages?
            <Tooltip
              :term="tradingTerms.MA.term"
              :definition="tradingTerms.MA.definition"
            />
          </h3>
          <p class="text-theme-secondary">
            The 10-day MA represents short-term momentum (~2 weeks).
            The 50-day MA represents medium-term trend (~2.5 months).
            When short-term momentum exceeds the medium-term trend, it suggests
            an emerging uptrend.
          </p>
        </div>

        <div>
          <h3 class="text-theme-primary font-medium flex items-center">
            Why 7% Initial Stop?
            <Tooltip
              :term="tradingTerms.stopLoss.term"
              :definition="tradingTerms.stopLoss.definition"
            />
          </h3>
          <p class="text-theme-secondary">
            Large-cap stocks typically move 1-2% daily. A 7% stop gives the trade
            room to breathe while limiting loss if the signal was wrong.
            Historically, if a stock drops 7% after a golden cross, the signal
            was likely false.
          </p>
        </div>

        <div>
          <h3 class="text-theme-primary font-medium flex items-center">
            Why 2% Risk Rule?
            <Tooltip
              :term="tradingTerms.riskPerTrade.term"
              :definition="tradingTerms.riskPerTrade.definition"
            />
          </h3>
          <p class="text-theme-secondary">
            Even 10 consecutive losses only costs ~20% of your account.
            A 20% loss requires a 25% gain to recover (manageable).
            Compare to 10% risk: 10 losses = 65% drawdown, requires 186% gain to recover!
          </p>
        </div>

        <div>
          <h3 class="text-theme-primary font-medium flex items-center">
            When Does This Strategy Fail?
            <Tooltip
              :term="tradingTerms.drawdown.term"
              :definition="tradingTerms.drawdown.definition"
            />
          </h3>
          <p class="text-theme-secondary">
            1. Sideways/choppy markets (whipsaw - multiple false signals)<br>
            2. Sharp V-shaped reversals (gives back gains before exit signal)<br>
            3. Bear markets (repeated failed buy signals)<br>
            4. Gap downs through stop loss (overnight bad news)
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePortfolioStore } from '../stores/portfolio'
import { useSettingsStore } from '../stores/settings'
import { useWatchlistStore } from '../stores/watchlist'
import { useExport } from '../composables/useExport'
import { useToast } from '../composables/useToast'
import { tradingTerms } from '../composables/useTooltips'
import Tooltip from '../components/ui/Tooltip.vue'
import StockSearch from '../components/trading/StockSearch.vue'

const portfolioStore = usePortfolioStore()
const settingsStore = useSettingsStore()
const watchlistStore = useWatchlistStore()
const { exportTradesToCSV, exportPortfolioToCSV } = useExport()
const toast = useToast()

const resetting = ref(false)

onMounted(async () => {
  await portfolioStore.fetchPortfolio()
  await portfolioStore.fetchTrades()
  await watchlistStore.fetchWatchlist()
})

async function handleReset() {
  if (!confirm('Are you sure you want to reset your portfolio? All positions and trade history will be cleared.')) {
    return
  }

  resetting.value = true
  try {
    await portfolioStore.resetPortfolio()
    toast.success('Portfolio reset to $10,000')
  } catch (err) {
    toast.error('Failed to reset portfolio')
  } finally {
    resetting.value = false
  }
}

function handleExportTrades() {
  const trades = portfolioStore.trades
  if (trades.length === 0) {
    toast.warning('No trades to export yet')
    return
  }
  exportTradesToCSV(trades, `trades_${new Date().toISOString().split('T')[0]}.csv`)
  toast.success('Trades exported successfully')
}

function handleExportPortfolio() {
  const portfolio = portfolioStore.portfolio
  const trades = portfolioStore.trades
  if (!portfolio) {
    toast.warning('No portfolio data available')
    return
  }
  exportPortfolioToCSV(portfolio, trades, `portfolio_${new Date().toISOString().split('T')[0]}.csv`)
  toast.success('Portfolio exported successfully')
}

function testSound() {
  settingsStore.playSound('buy')
}

async function handleRemoveSymbol(symbol) {
  const result = await watchlistStore.removeSymbol(symbol)
  if (result.success) {
    toast.success(result.message)
  } else {
    toast.error(result.message)
  }
}

function onSymbolAdded(symbol) {
  // Symbol was added successfully, nothing extra to do
  // The watchlist store is already updated
}
</script>
