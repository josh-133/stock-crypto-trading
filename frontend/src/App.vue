<template>
  <div class="min-h-screen bg-theme-primary transition-colors duration-200" :class="{ 'dark': settingsStore.isDarkMode, 'light': !settingsStore.isDarkMode }">
    <Navbar />
    <div class="flex">
      <Sidebar />
      <main class="flex-1 p-6">
        <router-view />
      </main>
    </div>
    <ToastContainer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Navbar from './components/layout/Navbar.vue'
import Sidebar from './components/layout/Sidebar.vue'
import ToastContainer from './components/ui/ToastContainer.vue'
import { useSettingsStore } from './stores/settings'

const settingsStore = useSettingsStore()

onMounted(() => {
  // Apply theme class to document on mount
  if (settingsStore.isDarkMode) {
    document.documentElement.classList.add('dark')
    document.documentElement.classList.remove('light')
  } else {
    document.documentElement.classList.add('light')
    document.documentElement.classList.remove('dark')
  }
})
</script>
