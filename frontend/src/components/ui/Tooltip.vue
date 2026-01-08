<template>
  <span class="tooltip-wrapper relative inline-flex items-center">
    <slot></slot>
    <span
      class="ml-1 inline-flex items-center justify-center w-4 h-4 rounded-full bg-gray-600 hover:bg-gray-500 cursor-help text-xs text-gray-300"
      @mouseenter="show = true"
      @mouseleave="show = false"
    >
      ?
    </span>
    <transition name="fade">
      <div
        v-if="show"
        class="tooltip-content absolute z-50 px-3 py-2 text-sm bg-gray-700 border border-gray-600 rounded-lg shadow-lg"
        :class="positionClass"
        :style="{ width: width }"
      >
        <p class="font-medium text-white mb-1">{{ term }}</p>
        <p class="text-gray-300 text-xs">{{ definition }}</p>
      </div>
    </transition>
  </span>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  term: {
    type: String,
    required: true,
  },
  definition: {
    type: String,
    required: true,
  },
  position: {
    type: String,
    default: 'top', // top, bottom, left, right
  },
  width: {
    type: String,
    default: '250px',
  },
})

const show = ref(false)

const positionClass = computed(() => {
  switch (props.position) {
    case 'bottom':
      return 'top-full left-1/2 -translate-x-1/2 mt-2'
    case 'left':
      return 'right-full top-1/2 -translate-y-1/2 mr-2'
    case 'right':
      return 'left-full top-1/2 -translate-y-1/2 ml-2'
    default: // top
      return 'bottom-full left-1/2 -translate-x-1/2 mb-2'
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
