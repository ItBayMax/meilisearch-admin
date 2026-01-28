<template>
  <div class="flex items-center justify-center py-12">
    <div class="flex flex-col items-center space-y-4">
      <div class="relative">
        <div class="w-12 h-12 border-4 border-dark-700 rounded-full"></div>
        <div class="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin absolute top-0 left-0"></div>
      </div>
      <p v-if="text" class="text-gray-400 text-sm">{{ text }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: 'Loading...',
  },
})
</script>
