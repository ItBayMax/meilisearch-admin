<template>
  <div class="h-full flex relative overflow-hidden">
    <!-- Left Sidebar -->
    <div 
      ref="sidebarRef"
      class="bg-dark-900 border-r border-dark-700 transition-all duration-300 ease-in-out relative flex-shrink-0 flex flex-col"
      :style="{
        width: sidebarCollapsed ? '3rem' : sidebarWidth + 'px'
      }"
    >
      <!-- Sidebar Header -->
      <div class="p-4 border-b border-dark-700 flex items-center justify-between flex-shrink-0">
        <div class="flex items-center gap-2">
          <!-- Collapsed state - Search icon only -->
          <div 
            v-show="sidebarCollapsed" 
            class="flex items-center justify-center w-8 h-8 text-gray-400 hover:text-white transition-colors cursor-pointer rounded-lg hover:bg-dark-800"
            @click="sidebarCollapsed = false"
            :title="settingsStore.t('searchControls')"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          
          <!-- Expanded state - Title -->
          <h3 
            v-show="!sidebarCollapsed" 
            class="text-lg font-semibold text-white truncate"
          >
            {{ settingsStore.t('searchControls') }}
          </h3>
        </div>
        <div class="flex items-center gap-2">
          <!-- Resize Handle -->
          <div 
            v-show="!sidebarCollapsed"
            class="w-1 h-6 bg-gray-600 rounded-full cursor-col-resize hover:bg-gray-500 transition-colors"
            @mousedown="startResize"
            :title="settingsStore.t('resizeSidebar') || '拖拽调整宽度'"
          ></div>
          <!-- Collapse/Expand Button - only show when sidebar is expanded -->
          <button 
            v-show="!sidebarCollapsed"
            @click="sidebarCollapsed = !sidebarCollapsed" 
            class="p-2 rounded-lg hover:bg-dark-800 transition-colors"
            :title="settingsStore.t('collapseSidebar')"
          >
            <svg 
              class="w-5 h-5 text-gray-400 hover:text-white transition-transform duration-200 rotate-180"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Sidebar Content -->
      <div v-show="!sidebarCollapsed" class="p-4 space-y-6 overflow-y-auto flex-1">
        <slot name="sidebar-content"></slot>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 overflow-auto">
      <div class="p-6 h-full flex flex-col">
        <slot name="main-content"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useSettingsStore } from '@/store/settings'

const settingsStore = useSettingsStore()

// Sidebar state
const sidebarCollapsed = ref(false)
const sidebarWidth = ref(400) // 默认宽度增加到400px
const sidebarRef = ref(null)

// Resize functionality
const isResizing = ref(false)

const startResize = (e) => {
  e.preventDefault()
  isResizing.value = true
  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'
}

const resize = (e) => {
  if (!isResizing.value || !sidebarRef.value) return
  
  const rect = sidebarRef.value.getBoundingClientRect()
  const newWidth = e.clientX - rect.left
  
  // 限制最小和最大宽度
  if (newWidth >= 300 && newWidth <= 600) {
    sidebarWidth.value = newWidth
  }
}

const stopResize = () => {
  isResizing.value = false
  document.body.style.cursor = ''
  document.body.style.userSelect = ''
}

// Event listeners
onMounted(() => {
  document.addEventListener('mousemove', resize)
  document.addEventListener('mouseup', stopResize)
})

onUnmounted(() => {
  document.removeEventListener('mousemove', resize)
  document.removeEventListener('mouseup', stopResize)
})

// Expose sidebar state and methods for parent components
defineExpose({
  sidebarCollapsed,
  sidebarWidth,
  startResize
})
</script>