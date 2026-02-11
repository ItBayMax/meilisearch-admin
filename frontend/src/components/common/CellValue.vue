<template>
  <div class="relative group">
    <!-- Image -->
    <img v-if="isImage" :src="value" class="w-10 h-10 object-cover rounded" />
    
    <!-- Complex value (Array/Object) -->
    <div v-else-if="isComplex" class="flex items-center gap-1 max-w-full">
      <div class="cursor-pointer flex-1 min-w-0" @click="toggleExpand">
        <span v-if="!expanded" class="text-primary-400 text-xs hover:underline truncate block">
          {{ complexLabel }}
        </span>
        <div 
          v-else 
          class="text-xs max-w-full overflow-auto bg-dark-800 p-3 rounded border border-dark-600"
          style="white-space: pre-wrap; word-break: break-word; word-wrap: break-word; overflow-wrap: break-word; font-family: ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace; line-height: 1.4;"
        ><div v-for="(line, index) in formattedJsonLines" :key="index" class="py-0.5">{{ line }}</div></div>
      </div>
      <button 
        @click="copyValue" 
        class="opacity-0 group-hover:opacity-100 transition-opacity p-1 text-gray-400 hover:text-white"
        :title="settingsStore.t('copy')"
      >
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
      </button>
    </div>
    
    <!-- Long text -->
    <div v-else-if="isLongText" class="flex items-center gap-1 max-w-full">
      <div class="cursor-pointer flex-1 min-w-0" @click="toggleExpand">
        <span v-if="!expanded" class="truncate block">{{ truncatedValue }}</span>
        <span 
          v-else 
          class="block max-w-full"
          style="white-space: pre-wrap !important; word-break: break-word !important; word-wrap: break-word !important; overflow-wrap: break-word !important;"
        >{{ value }}</span>
      </div>
      <button 
        @click="copyValue" 
        class="opacity-0 group-hover:opacity-100 transition-opacity p-1 text-gray-400 hover:text-white"
        :title="settingsStore.t('copy')"
      >
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
      </button>
    </div>
    
    <!-- Medium length text (show copy button on hover) -->
    <div v-else-if="isMediumText" class="flex items-center gap-1 max-w-full">
      <span class="truncate block flex-1 min-w-0">{{ displayValue }}</span>
      <button 
        @click="copyValue" 
        class="opacity-0 group-hover:opacity-100 transition-opacity p-1 text-gray-400 hover:text-white"
        :title="settingsStore.t('copy')"
      >
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
      </button>
    </div>
    
    <!-- Short text (show copy button on hover) -->
    <div v-else class="flex items-center gap-1 max-w-full">
      <span class="truncate block flex-1 min-w-0">{{ displayValue }}</span>
      <button 
        @click="copyValue" 
        class="opacity-0 group-hover:opacity-100 transition-opacity p-1 text-gray-400 hover:text-white"
        :title="settingsStore.t('copy')"
      >
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useSettingsStore } from '@/store/settings'

const props = defineProps({
  value: {
    type: [String, Number, Boolean, Array, Object, null],
    default: null
  },
  cellKey: {
    type: String,
    default: ''
  },
  maxLength: {
    type: Number,
    default: 50
  },
  mediumLength: {
    type: Number,
    default: 20
  }
})

const settingsStore = useSettingsStore()
const expanded = ref(false)

const isImage = computed(() => {
  if (typeof props.value !== 'string') return false
  return /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(props.value)
})

const isComplex = computed(() => {
  return props.value !== null && typeof props.value === 'object'
})

const isLongText = computed(() => {
  return typeof props.value === 'string' && props.value.length > props.maxLength
})

const isMediumText = computed(() => {
  return typeof props.value === 'string' && 
         props.value.length > props.mediumLength && 
         props.value.length <= props.maxLength
})

const formattedJsonLines = computed(() => {
  if (!isComplex.value) return []
  try {
    const jsonString = JSON.stringify(props.value, null, 2)
    return jsonString.split('\n')
  } catch (error) {
    return [String(props.value)]
  }
})

const complexLabel = computed(() => {
  if (Array.isArray(props.value)) {
    return `Array[${props.value.length}]`
  }
  return `Object{${Object.keys(props.value).length}}`
})

const truncatedValue = computed(() => {
  if (typeof props.value === 'string' && props.value.length > props.maxLength) {
    return props.value.substring(0, props.maxLength) + '...'
  }
  return props.value
})

const displayValue = computed(() => {
  if (props.value === null || props.value === undefined) return '-'
  return String(props.value)
})

const toggleExpand = () => {
  expanded.value = !expanded.value
}

const copyValue = async () => {
  try {
    let textToCopy = ''
    
    if (props.value === null || props.value === undefined) {
      textToCopy = ''
    } else if (typeof props.value === 'object') {
      textToCopy = JSON.stringify(props.value, null, 2)
    } else {
      textToCopy = String(props.value)
    }
    
    await navigator.clipboard.writeText(textToCopy)
    
    // 可以在这里添加复制成功的提示
    console.log('Value copied to clipboard')
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}
</script>
