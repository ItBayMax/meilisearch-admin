<template>
  <div
    v-if="visible"
    class="fixed inset-0 z-50 flex items-center justify-center"
    @click.self="closeOnOverlay && close()"
  >
    <!-- Overlay -->
    <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

    <!-- Modal -->
    <div
      class="relative bg-dark-900 rounded-xl border border-dark-700 shadow-2xl w-full max-h-[90vh] overflow-hidden fade-in"
      :class="sizeClass"
    >
      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-dark-700">
        <h3 class="text-lg font-semibold text-white">{{ title }}</h3>
        <button
          @click="close"
          class="p-1 rounded-lg text-gray-400 hover:text-white hover:bg-dark-700 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="px-6 py-4 overflow-y-auto max-h-[calc(90vh-130px)]">
        <slot></slot>
      </div>

      <!-- Footer -->
      <div v-if="$slots.footer" class="px-6 py-4 border-t border-dark-700 bg-dark-800/50">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch, onUnmounted } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: '',
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg', 'xl'].includes(v),
  },
  closeOnOverlay: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:visible', 'close'])

const sizeClass = computed(() => {
  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
  }
  return sizes[props.size]
})

const close = () => {
  emit('update:visible', false)
  emit('close')
}

// Lock body scroll when modal is open
watch(() => props.visible, (visible) => {
  document.body.style.overflow = visible ? 'hidden' : ''
})

// Restore scroll on unmount
onUnmounted(() => {
  document.body.style.overflow = ''
})
</script>
