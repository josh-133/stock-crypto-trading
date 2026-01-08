import { ref, onUnmounted } from 'vue'

export function useWebSocket() {
  const prices = ref({})
  const connected = ref(false)
  const error = ref(null)

  let ws = null
  let reconnectTimeout = null
  const RECONNECT_DELAY = 5000

  function connect() {
    if (ws && ws.readyState === WebSocket.OPEN) {
      return
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.hostname
    const port = '8000' // Backend port
    const url = `${protocol}//${host}:${port}/ws/prices`

    try {
      ws = new WebSocket(url)

      ws.onopen = () => {
        connected.value = true
        error.value = null
        console.log('WebSocket connected')
      }

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)

          if (message.type === 'initial_prices') {
            // Initial batch of prices
            prices.value = message.data
          } else if (message.type === 'price_update') {
            // Single price update
            const priceData = message.data
            prices.value = {
              ...prices.value,
              [priceData.symbol]: priceData
            }
          }
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e)
        }
      }

      ws.onclose = () => {
        connected.value = false
        console.log('WebSocket disconnected')

        // Auto-reconnect
        reconnectTimeout = setTimeout(() => {
          console.log('Attempting to reconnect...')
          connect()
        }, RECONNECT_DELAY)
      }

      ws.onerror = (e) => {
        error.value = 'WebSocket error'
        console.error('WebSocket error:', e)
      }
    } catch (e) {
      error.value = 'Failed to connect'
      console.error('Failed to create WebSocket:', e)
    }
  }

  function disconnect() {
    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout)
      reconnectTimeout = null
    }

    if (ws) {
      ws.close()
      ws = null
    }

    connected.value = false
  }

  function subscribe(symbol) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ action: 'subscribe', symbol }))
    }
  }

  function unsubscribe(symbol) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ action: 'unsubscribe', symbol }))
    }
  }

  function getPrice(symbol) {
    return prices.value[symbol?.toUpperCase()] || null
  }

  // Cleanup on unmount
  onUnmounted(() => {
    disconnect()
  })

  return {
    prices,
    connected,
    error,
    connect,
    disconnect,
    subscribe,
    unsubscribe,
    getPrice,
  }
}
