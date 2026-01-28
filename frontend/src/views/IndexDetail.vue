<template>
  <div class="space-y-6 fade-in">
    <Loading v-if="loading" />
    
    <template v-else-if="indexData">
      <!-- Index Header -->
      <div class="card p-6">
        <div class="flex items-start justify-between">
          <div class="flex items-center space-x-4">
            <div class="w-14 h-14 bg-indigo-500/20 rounded-xl flex items-center justify-center">
              <svg class="w-7 h-7 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-white">{{ indexId }}</h1>
              <p class="text-gray-400 mt-1">{{ settingsStore.t('primaryKey') }}: {{ indexData.primaryKey || settingsStore.t('notSet') }}</p>
            </div>
          </div>
          <router-link :to="`/projects/${projectId}`" class="btn btn-ghost text-gray-400">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Top Navigation: Settings / Search Preview -->
      <div class="flex border-b border-dark-700">
        <button
          @click="activeTab = 'settings'"
          class="px-6 py-3 text-sm font-medium transition-colors border-b-2"
          :class="activeTab === 'settings' ? 'text-primary-400 border-primary-400' : 'text-gray-400 border-transparent hover:text-white'"
        >
          {{ settingsStore.t('settings') }}
        </button>
        <button
          @click="activeTab = 'search'"
          class="px-6 py-3 text-sm font-medium transition-colors border-b-2"
          :class="activeTab === 'search' ? 'text-primary-400 border-primary-400' : 'text-gray-400 border-transparent hover:text-white'"
        >
          {{ settingsStore.t('searchPreview') }}
        </button>
      </div>

      <!-- Settings Layout with Left Sidebar -->
      <div v-if="activeTab === 'settings'" class="flex gap-6">
        <!-- Left Sidebar Menu -->
        <div class="w-56 flex-shrink-0">
          <nav class="card p-2 space-y-1">
            <router-link
              v-for="item in menuItems"
              :key="item.name"
              :to="item.path"
              class="flex items-center px-3 py-2 text-sm rounded-lg transition-colors"
              :class="isActiveRoute(item.name) ? 'bg-primary-500/20 text-primary-400' : 'text-gray-400 hover:text-white hover:bg-dark-700'"
            >
              {{ item.label }}
            </router-link>
          </nav>
        </div>

        <!-- Right Content Area -->
        <div class="flex-1 card p-6">
          <router-view />
        </div>
      </div>

      <!-- Search Preview -->
      <div v-else class="card p-6">
        <IndexSearch />
      </div>
    </template>

    <Empty v-else :title="settingsStore.t('indexNotFound')" :description="error || settingsStore.t('indexNotFoundDesc')" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, provide } from 'vue'
import { useRoute } from 'vue-router'
import { useSettingsStore } from '@/store/settings'
import { indexApi } from '@/api'
import Loading from '@/components/common/Loading.vue'
import Empty from '@/components/common/Empty.vue'
import IndexSearch from '@/views/index/Search.vue'

const route = useRoute()
const settingsStore = useSettingsStore()

const indexData = ref(null)
const settings = ref(null)
const loading = ref(false)
const error = ref(null)
const activeTab = ref('settings')

const projectId = computed(() => route.params.projectId)
const indexId = computed(() => route.params.indexId)

// Menu items for settings sidebar
const menuItems = computed(() => [
  { name: 'IndexGeneral', label: settingsStore.t('general'), path: `/projects/${projectId.value}/indexes/${indexId.value}` },
  { name: 'IndexAttributes', label: settingsStore.t('attributes'), path: `/projects/${projectId.value}/indexes/${indexId.value}/attributes` },
  { name: 'IndexRankingRules', label: settingsStore.t('rankingRules'), path: `/projects/${projectId.value}/indexes/${indexId.value}/ranking-rules` },
  { name: 'IndexSynonyms', label: settingsStore.t('synonyms'), path: `/projects/${projectId.value}/indexes/${indexId.value}/synonyms` },
  { name: 'IndexTypoTolerance', label: settingsStore.t('typoTolerance'), path: `/projects/${projectId.value}/indexes/${indexId.value}/typo-tolerance` },
  { name: 'IndexPrefixSearch', label: settingsStore.t('prefixSearch'), path: `/projects/${projectId.value}/indexes/${indexId.value}/prefix-search` },
  { name: 'IndexStopWords', label: settingsStore.t('stopWords'), path: `/projects/${projectId.value}/indexes/${indexId.value}/stop-words` },
  { name: 'IndexSeparators', label: settingsStore.t('separators'), path: `/projects/${projectId.value}/indexes/${indexId.value}/separators` },
  { name: 'IndexDictionary', label: settingsStore.t('dictionary'), path: `/projects/${projectId.value}/indexes/${indexId.value}/dictionary` },
  { name: 'IndexPagination', label: settingsStore.t('pagination'), path: `/projects/${projectId.value}/indexes/${indexId.value}/pagination` },
  { name: 'IndexFaceting', label: settingsStore.t('faceting'), path: `/projects/${projectId.value}/indexes/${indexId.value}/faceting` },
  { name: 'IndexSearchCutoff', label: settingsStore.t('searchCutoff'), path: `/projects/${projectId.value}/indexes/${indexId.value}/search-cutoff` },
  { name: 'IndexEmbedders', label: settingsStore.t('embedders'), path: `/projects/${projectId.value}/indexes/${indexId.value}/embedders` },
])

const isActiveRoute = (routeName) => {
  return route.name === routeName
}

// Provide context to child components
provide('projectId', projectId)
provide('indexId', indexId)
provide('indexData', indexData)
provide('settings', settings)

const fetchIndex = async () => {
  loading.value = true
  error.value = null
  try {
    const result = await indexApi.get(projectId.value, indexId.value)
    indexData.value = result.data
    
    const settingsResult = await indexApi.getSettings(projectId.value, indexId.value)
    settings.value = settingsResult.data
  } catch (err) {
    console.error('Failed to fetch index:', err)
    error.value = err.response?.data?.error || err.message || 'Failed to fetch index'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchIndex()
})
</script>
