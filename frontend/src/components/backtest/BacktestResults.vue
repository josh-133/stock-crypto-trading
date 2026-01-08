<template>
  <div class="space-y-6">
    <!-- Summary Stats -->
    <div class="card">
      <h2 class="text-lg font-semibold text-white mb-4">
        Backtest Results: {{ results.symbol }}
      </h2>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <!-- Total Return -->
        <div>
          <p class="text-sm text-gray-400">Total Return</p>
          <p
            class="text-xl font-bold"
            :class="results.total_return >= 0 ? 'text-profit' : 'text-loss'"
          >
            {{ results.total_return >= 0 ? '+' : '' }}${{ formatNumber(results.total_return) }}
          </p>
          <p
            class="text-sm"
            :class="results.total_return_percent >= 0 ? 'text-profit' : 'text-loss'"
          >
            ({{ results.total_return_percent >= 0 ? '+' : '' }}{{ results.total_return_percent.toFixed(2) }}%)
          </p>
        </div>

        <!-- Final Value -->
        <div>
          <p class="text-sm text-gray-400">Final Value</p>
          <p class="text-xl font-bold text-white">
            ${{ formatNumber(results.final_value) }}
          </p>
          <p class="text-sm text-gray-500">
            from ${{ formatNumber(results.initial_capital) }}
          </p>
        </div>

        <!-- Win Rate -->
        <div>
          <p class="text-sm text-gray-400">Win Rate</p>
          <p
            class="text-xl font-bold"
            :class="results.win_rate >= 50 ? 'text-profit' : 'text-loss'"
          >
            {{ results.win_rate.toFixed(1) }}%
          </p>
          <p class="text-sm text-gray-500">
            {{ results.winning_trades }}W / {{ results.losing_trades }}L
          </p>
        </div>

        <!-- Max Drawdown -->
        <div>
          <p class="text-sm text-gray-400">Max Drawdown</p>
          <p class="text-xl font-bold text-loss">
            -${{ formatNumber(results.max_drawdown) }}
          </p>
          <p class="text-sm text-loss">
            (-{{ results.max_drawdown_percent.toFixed(1) }}%)
          </p>
        </div>
      </div>

      <!-- Date Range -->
      <div class="mt-4 pt-4 border-t border-gray-700">
        <p class="text-sm text-gray-400">
          Period: {{ formatDate(results.start_date) }} to {{ formatDate(results.end_date) }}
        </p>
        <p class="text-sm text-gray-400">
          Total Trades: {{ results.total_trades }}
        </p>
      </div>
    </div>

    <!-- Equity Curve -->
    <EquityCurve
      :data="results.equity_curve"
      :initial-capital="results.initial_capital"
      :final-value="results.final_value"
    />

    <!-- Trade List -->
    <div class="card">
      <h3 class="text-lg font-semibold text-white mb-4">Trade History</h3>

      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-gray-400 border-b border-gray-700">
              <th class="pb-2">Entry Date</th>
              <th class="pb-2">Entry Price</th>
              <th class="pb-2">Exit Date</th>
              <th class="pb-2">Exit Price</th>
              <th class="pb-2">Shares</th>
              <th class="pb-2">P&L</th>
              <th class="pb-2">Exit Reason</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(trade, index) in results.trades"
              :key="index"
              class="border-b border-gray-700"
            >
              <td class="py-2 text-white">{{ formatDate(trade.entry_date) }}</td>
              <td class="py-2 text-white">${{ trade.entry_price.toFixed(2) }}</td>
              <td class="py-2 text-white">{{ trade.exit_date ? formatDate(trade.exit_date) : '-' }}</td>
              <td class="py-2 text-white">{{ trade.exit_price ? `$${trade.exit_price.toFixed(2)}` : '-' }}</td>
              <td class="py-2 text-white">{{ trade.shares }}</td>
              <td
                class="py-2 font-medium"
                :class="trade.pnl >= 0 ? 'text-profit' : 'text-loss'"
              >
                {{ trade.pnl >= 0 ? '+' : '' }}${{ trade.pnl.toFixed(2) }}
                ({{ trade.pnl_percent >= 0 ? '+' : '' }}{{ trade.pnl_percent.toFixed(1) }}%)
              </td>
              <td class="py-2 text-gray-400">{{ formatExitReason(trade.exit_reason) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="results.trades.length === 0" class="text-gray-400 text-center py-4">
        No trades in this period
      </div>
    </div>
  </div>
</template>

<script setup>
import EquityCurve from '../charts/EquityCurve.vue'

const props = defineProps({
  results: {
    type: Object,
    required: true,
  },
})

function formatNumber(num) {
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function formatExitReason(reason) {
  switch (reason) {
    case 'signal':
      return 'Death Cross'
    case 'initial_stop':
      return 'Stop Loss (7%)'
    case 'trailing_stop':
      return 'Trailing Stop (10%)'
    case 'end_of_period':
      return 'End of Period'
    default:
      return reason || '-'
  }
}
</script>
