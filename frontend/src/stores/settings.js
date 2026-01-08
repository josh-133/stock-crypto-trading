import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  // Theme
  const isDarkMode = ref(true) // Default to dark mode

  // Sound alerts
  const soundEnabled = ref(true)
  const soundVolume = ref(0.5) // 0-1

  // Auto-refresh
  const autoRefreshEnabled = ref(false)
  const refreshInterval = ref(5) // minutes

  // Load settings from localStorage
  function loadSettings() {
    const saved = localStorage.getItem('tradingPlatformSettings')
    if (saved) {
      try {
        const settings = JSON.parse(saved)
        isDarkMode.value = settings.isDarkMode ?? true
        soundEnabled.value = settings.soundEnabled ?? true
        soundVolume.value = settings.soundVolume ?? 0.5
        autoRefreshEnabled.value = settings.autoRefreshEnabled ?? false
        refreshInterval.value = settings.refreshInterval ?? 5
      } catch (e) {
        console.error('Failed to load settings:', e)
      }
    }
    applyTheme()
  }

  // Save settings to localStorage
  function saveSettings() {
    const settings = {
      isDarkMode: isDarkMode.value,
      soundEnabled: soundEnabled.value,
      soundVolume: soundVolume.value,
      autoRefreshEnabled: autoRefreshEnabled.value,
      refreshInterval: refreshInterval.value,
    }
    localStorage.setItem('tradingPlatformSettings', JSON.stringify(settings))
  }

  // Apply theme to document
  function applyTheme() {
    if (isDarkMode.value) {
      document.documentElement.classList.add('dark')
      document.documentElement.classList.remove('light')
    } else {
      document.documentElement.classList.add('light')
      document.documentElement.classList.remove('dark')
    }
  }

  // Toggle theme
  function toggleTheme() {
    isDarkMode.value = !isDarkMode.value
    applyTheme()
    saveSettings()
  }

  // Play notification sound
  function playSound(type = 'signal') {
    if (!soundEnabled.value) return

    // Create audio context for generating sounds
    try {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)()
      const oscillator = audioContext.createOscillator()
      const gainNode = audioContext.createGain()

      oscillator.connect(gainNode)
      gainNode.connect(audioContext.destination)

      // Different sounds for different events
      if (type === 'buy') {
        // Rising tone for buy signal
        oscillator.frequency.setValueAtTime(440, audioContext.currentTime)
        oscillator.frequency.linearRampToValueAtTime(880, audioContext.currentTime + 0.2)
      } else if (type === 'sell') {
        // Falling tone for sell signal
        oscillator.frequency.setValueAtTime(880, audioContext.currentTime)
        oscillator.frequency.linearRampToValueAtTime(440, audioContext.currentTime + 0.2)
      } else {
        // Default notification beep
        oscillator.frequency.setValueAtTime(660, audioContext.currentTime)
      }

      gainNode.gain.setValueAtTime(soundVolume.value * 0.3, audioContext.currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3)

      oscillator.start(audioContext.currentTime)
      oscillator.stop(audioContext.currentTime + 0.3)
    } catch (e) {
      console.error('Failed to play sound:', e)
    }
  }

  // Toggle sound
  function toggleSound() {
    soundEnabled.value = !soundEnabled.value
    saveSettings()
  }

  // Set refresh interval
  function setRefreshInterval(minutes) {
    refreshInterval.value = minutes
    saveSettings()
  }

  // Toggle auto-refresh
  function toggleAutoRefresh() {
    autoRefreshEnabled.value = !autoRefreshEnabled.value
    saveSettings()
  }

  // Watch for changes and save
  watch([isDarkMode, soundEnabled, soundVolume, autoRefreshEnabled, refreshInterval], () => {
    saveSettings()
  })

  // Initialize
  loadSettings()

  return {
    // State
    isDarkMode,
    soundEnabled,
    soundVolume,
    autoRefreshEnabled,
    refreshInterval,
    // Actions
    toggleTheme,
    toggleSound,
    playSound,
    setRefreshInterval,
    toggleAutoRefresh,
    loadSettings,
    saveSettings,
  }
})
