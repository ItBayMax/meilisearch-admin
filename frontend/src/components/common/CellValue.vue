<template>
  <div>
    <!-- Image -->
    <img v-if="isImage" :src="value" class="w-10 h-10 object-cover rounded" />
    
    <!-- Complex value (Array/Object) -->
    <div v-else-if="isComplex" class="cursor-pointer" @click="toggleExpand">
      <span v-if="!expanded" class="text-primary-400 text-xs hover:underline">
        {{ complexLabel }}
      </span>
      <pre v-else class="text-xs whitespace-pre-wrap max-w-[300px] overflow-auto">{{ JSON.stringify(value, null, 2) }}</pre>
    </div>
    
    <!-- Long text -->
    <div v-else-if="isLongText" class="cursor-pointer" @click="toggleExpand">
      <span v-if="!expanded" class="truncate block">{{ truncatedValue }}</span>
      <span v-else class="whitespace-pre-wrap">{{ value }}</span>
    </div>
    
    <!-- Normal value -->
    <span v-else class="truncate block">{{ displayValue }}</span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

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
  }
})

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
</script>
