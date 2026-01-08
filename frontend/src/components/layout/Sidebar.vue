<template>
  <aside class="w-64 min-h-screen border-r p-4 transition-colors duration-200 bg-theme-secondary border-theme">
    <nav class="space-y-2">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors"
        :class="[
          $route.path === item.path
            ? 'bg-blue-600 text-white'
            : 'text-theme-secondary hover:bg-theme-tertiary hover:text-theme-primary'
        ]"
      >
        <span class="text-lg">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </router-link>
    </nav>

    <!-- Strategy Info -->
    <div class="mt-8 p-4 rounded-lg bg-theme-tertiary">
      <h3 class="text-sm font-medium text-theme-primary mb-2">Strategy</h3>
      <p class="text-xs text-theme-secondary">10/50 MA Crossover</p>
      <div class="mt-2 space-y-1 text-xs text-theme-muted">
        <p>Buy: Golden Cross</p>
        <p>Sell: Death Cross</p>
        <p>Stop: 7% / 10% trailing</p>
      </div>
    </div>
  </aside>
</template>

<script setup>
const menuItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/trading', label: 'Trading', icon: '📈' },
  { path: '/backtest', label: 'Backtest', icon: '🔬' },
  { path: '/settings', label: 'Settings', icon: '⚙️' },
]
</script>
