<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-50 flex flex-col space-y-2 max-w-sm">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="toast"
          :class="toastClass(toast.type)"
          @click="dismiss(toast.id)"
        >
          <div class="flex items-start space-x-3">
            <span class="toast-icon">{{ getIcon(toast.type) }}</span>
            <p class="flex-1 text-sm">{{ toast.message }}</p>
            <button
              @click.stop="dismiss(toast.id)"
              class="text-current opacity-60 hover:opacity-100 transition-opacity"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useToastStore } from '../../stores/toast'

const toastStore = useToastStore()
const toasts = computed(() => toastStore.toasts)

function dismiss(id) {
  toastStore.removeToast(id)
}

function toastClass(type) {
  switch (type) {
    case 'success':
      return 'toast-success'
    case 'error':
      return 'toast-error'
    case 'warning':
      return 'toast-warning'
    case 'info':
    default:
      return 'toast-info'
  }
}

function getIcon(type) {
  switch (type) {
    case 'success':
      return '+'
    case 'error':
      return '!'
    case 'warning':
      return '?'
    case 'info':
    default:
      return 'i'
  }
}
</script>

<style scoped>
.toast {
  @apply px-4 py-3 rounded-lg shadow-lg cursor-pointer;
  @apply transform transition-all duration-300 ease-out;
  min-width: 280px;
}

.toast-success {
  @apply bg-green-600 text-white;
}

.toast-error {
  @apply bg-red-600 text-white;
}

.toast-warning {
  @apply bg-yellow-500 text-gray-900;
}

.toast-info {
  @apply bg-blue-600 text-white;
}

.toast-icon {
  @apply w-5 h-5 flex items-center justify-center rounded-full text-xs font-bold;
  @apply bg-white bg-opacity-20;
}

/* Transition animations */
.toast-enter-active {
  animation: toast-in 0.3s ease-out;
}

.toast-leave-active {
  animation: toast-out 0.3s ease-in;
}

@keyframes toast-in {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes toast-out {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}
</style>
