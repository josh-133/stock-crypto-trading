<template>
  <nav class="border-b px-6 py-4 transition-colors duration-200 bg-theme-secondary border-theme">
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <h1 class="text-xl font-bold text-theme-primary">Stock Trading Platform</h1>
        <span class="px-2 py-1 bg-yellow-600 text-yellow-100 text-xs rounded-full">
          PAPER TRADING
        </span>
      </div>
      <div class="flex items-center space-x-4">
        <!-- Auto-refresh indicator -->
        <div v-if="settingsStore.autoRefreshEnabled" class="flex items-center text-sm text-theme-secondary">
          <span class="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
          Auto-refresh: {{ settingsStore.refreshInterval }}m
        </div>

        <!-- Sound toggle -->
        <button
          @click="settingsStore.toggleSound"
          class="p-2 rounded-lg hover:bg-theme-tertiary transition-colors"
          :title="settingsStore.soundEnabled ? 'Sound On' : 'Sound Off'"
        >
          <span v-if="settingsStore.soundEnabled">🔔</span>
          <span v-else>🔕</span>
        </button>

        <!-- Theme toggle -->
        <button
          @click="settingsStore.toggleTheme"
          class="p-2 rounded-lg hover:bg-theme-tertiary transition-colors"
          :title="settingsStore.isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        >
          <span v-if="settingsStore.isDarkMode">☀️</span>
          <span v-else>🌙</span>
        </button>

        <div class="text-sm text-theme-secondary hidden md:block">
          Educational purposes only
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useSettingsStore } from '../../stores/settings'

const settingsStore = useSettingsStore()
</script>
