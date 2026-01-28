<template>
  <div class="flex flex-col items-center justify-center py-12 text-center">
    <div class="w-16 h-16 bg-dark-800 rounded-full flex items-center justify-center mb-4">
      <svg class="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
      </svg>
    </div>
    <h3 class="text-lg font-medium text-gray-300 mb-2">{{ title }}</h3>
    <p class="text-gray-500 text-sm max-w-sm">{{ description }}</p>
    <slot name="action"></slot>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: 'No Data',
  },
  description: {
    type: String,
    default: 'There is no data to display.',
  },
})
</script>
