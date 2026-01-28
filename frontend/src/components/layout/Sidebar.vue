<template>
  <aside class="w-64 bg-dark-900 border-r border-dark-700 flex flex-col">
    <!-- Logo -->
    <div class="h-16 flex items-center px-6 border-b border-dark-700">
      <router-link to="/" class="flex items-center space-x-3">
        <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-indigo-500 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-sm">M</span>
        </div>
        <span class="text-lg font-semibold text-white">Meilisearch</span>
      </router-link>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 px-4 py-6 space-y-2">
      <router-link
        to="/"
        class="nav-item"
        :class="{ 'nav-item-active': $route.path === '/' }"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        <span>{{ settingsStore.t('dashboard') }}</span>
      </router-link>

      <router-link
        to="/projects"
        class="nav-item"
        :class="{ 'nav-item-active': $route.path.startsWith('/projects') }"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <span>{{ settingsStore.t('projects') }}</span>
      </router-link>
    </nav>

    <!-- Footer -->
    <div class="p-4 border-t border-dark-700">
      <div class="text-xs text-gray-500 text-center">
        Meilisearch Admin v1.0.0
      </div>
    </div>
  </aside>
</template>

<script setup>
import { useSettingsStore } from '@/store/settings'

const settingsStore = useSettingsStore()
</script>

<style scoped>
.nav-item {
  @apply flex items-center space-x-3 px-4 py-2.5 rounded-lg text-gray-400 hover:text-white hover:bg-dark-800 transition-colors;
}

.nav-item-active {
  @apply bg-primary-600/20 text-primary-400;
}
</style>
