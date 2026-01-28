<template>
  <div class="space-y-6 fade-in">
    <Loading v-if="loading" />
    
    <template v-else-if="project">
      <!-- Project Header -->
      <div class="card p-6">
        <div class="flex items-start justify-between">
          <div class="flex items-center space-x-4">
            <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-indigo-500 rounded-xl flex items-center justify-center">
              <span class="text-white font-bold text-2xl">{{ project.name.charAt(0).toUpperCase() }}</span>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-white">{{ project.name }}</h1>
              <p class="text-gray-400 mt-1">{{ project.url }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <span class="badge badge-success">{{ settingsStore.t('connected') }}</span>
            <span v-if="stats?.version" class="badge badge-info">v{{ stats.version.pkgVersion }}</span>
          </div>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="card">
        <div class="flex border-b border-dark-700">
          <router-link
            :to="`/projects/${projectId}`"
            class="tab-item"
            :class="{ 'tab-item-active': $route.name === 'ProjectIndexes' }"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
            </svg>
            <span>{{ settingsStore.t('indexes') }}</span>
          </router-link>

          <router-link
            :to="`/projects/${projectId}/tasks`"
            class="tab-item"
            :class="{ 'tab-item-active': $route.name === 'ProjectTasks' }"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <span>{{ settingsStore.t('tasks') }}</span>
          </router-link>

          <router-link
            :to="`/projects/${projectId}/search`"
            class="tab-item"
            :class="{ 'tab-item-active': $route.name === 'ProjectSearch' }"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <span>{{ settingsStore.t('searchPreview') }}</span>
          </router-link>

          <router-link
            :to="`/projects/${projectId}/keys`"
            class="tab-item"
            :class="{ 'tab-item-active': $route.name === 'ProjectKeys' }"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
            </svg>
            <span>{{ settingsStore.t('keys') }}</span>
          </router-link>

          <router-link
            :to="`/projects/${projectId}/settings`"
            class="tab-item"
            :class="{ 'tab-item-active': $route.name === 'ProjectSettings' }"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>{{ settingsStore.t('settings') }}</span>
          </router-link>
        </div>

        <!-- Child Route View -->
        <div class="p-6">
          <router-view />
        </div>
      </div>
    </template>

    <Empty v-else :title="settingsStore.t('projectNotFound')" :description="settingsStore.t('projectNotFoundDesc')" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, provide } from 'vue'
import { useRoute } from 'vue-router'
import { useProjectStore } from '@/store/project'
import { useSettingsStore } from '@/store/settings'
import { projectApi } from '@/api'
import Loading from '@/components/common/Loading.vue'
import Empty from '@/components/common/Empty.vue'

const route = useRoute()
const projectStore = useProjectStore()
const settingsStore = useSettingsStore()

const stats = ref(null)
const projectId = computed(() => route.params.id)
const project = computed(() => projectStore.currentProject)
const loading = computed(() => projectStore.loading)

// Provide project context to child components
provide('projectId', projectId)
provide('project', project)

const fetchStats = async () => {
  try {
    const result = await projectApi.getStats(projectId.value)
    if (result.success) {
      stats.value = result.data
    }
  } catch (err) {
    console.error('Failed to fetch stats:', err)
  }
}

onMounted(async () => {
  await projectStore.fetchProject(projectId.value)
  fetchStats()
})
</script>

<style scoped>
.tab-item {
  @apply flex items-center space-x-2 px-6 py-4 text-gray-400 hover:text-white border-b-2 border-transparent transition-colors;
}

.tab-item-active {
  @apply text-primary-400 border-primary-400;
}
</style>
