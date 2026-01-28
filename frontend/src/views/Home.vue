<template>
  <div class="space-y-6 fade-in">
    <!-- Welcome Section -->
    <div class="card p-8">
      <div class="flex items-start justify-between">
        <div>
          <h1 class="text-3xl font-bold text-white mb-2">{{ settingsStore.t('welcomeTitle') }}</h1>
          <p class="text-gray-400 max-w-2xl">
            {{ settingsStore.t('welcomeDesc') }}
          </p>
        </div>
        <div class="w-24 h-24 bg-gradient-to-br from-primary-500 to-indigo-500 rounded-2xl flex items-center justify-center">
          <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card p-6 card-hover">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-400 text-sm">{{ settingsStore.t('totalProjects') }}</p>
            <p class="text-3xl font-bold text-white mt-1">{{ projects.length }}</p>
          </div>
          <div class="w-12 h-12 bg-primary-500/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
        </div>
      </div>

      <div class="card p-6 card-hover">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-400 text-sm">{{ settingsStore.t('activeInstances') }}</p>
            <p class="text-3xl font-bold text-white mt-1">{{ activeCount }}</p>
          </div>
          <div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
      </div>

      <div class="card p-6 card-hover cursor-pointer" @click="$router.push('/projects')">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-400 text-sm">{{ settingsStore.t('quickAction') }}</p>
            <p class="text-lg font-semibold text-white mt-1">{{ settingsStore.t('viewAllProjects') }}</p>
          </div>
          <div class="w-12 h-12 bg-indigo-500/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Projects -->
    <div class="card">
      <div class="px-6 py-4 border-b border-dark-700 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-white">{{ settingsStore.t('recentProjects') }}</h2>
        <router-link to="/projects" class="text-primary-400 hover:text-primary-300 text-sm">
          {{ settingsStore.t('viewAll') }}
        </router-link>
      </div>
      <div v-if="loading" class="p-6">
        <Loading />
      </div>
      <div v-else-if="projects.length === 0" class="p-6">
        <Empty
          :title="settingsStore.t('noProjectsYet')"
          :description="settingsStore.t('noProjectsYetDesc')"
        >
          <template #action>
            <router-link to="/projects" class="btn btn-primary mt-4">
              {{ settingsStore.t('addProject') }}
            </router-link>
          </template>
        </Empty>
      </div>
      <div v-else class="divide-y divide-dark-700">
        <div
          v-for="project in recentProjects"
          :key="project.id"
          class="px-6 py-4 flex items-center justify-between hover:bg-dark-800/50 transition-colors cursor-pointer"
          @click="$router.push(`/projects/${project.id}`)"
        >
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-indigo-500 rounded-lg flex items-center justify-center">
              <span class="text-white font-semibold">{{ project.name.charAt(0).toUpperCase() }}</span>
            </div>
            <div>
              <h3 class="text-white font-medium">{{ project.name }}</h3>
              <p class="text-gray-500 text-sm">{{ project.url }}</p>
            </div>
          </div>
          <span class="badge badge-success">{{ settingsStore.t('active') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useProjectStore } from '@/store/project'
import { useSettingsStore } from '@/store/settings'
import Loading from '@/components/common/Loading.vue'
import Empty from '@/components/common/Empty.vue'

const projectStore = useProjectStore()
const settingsStore = useSettingsStore()

const projects = computed(() => projectStore.projects)
const loading = computed(() => projectStore.loading)
const activeCount = computed(() => projects.value.filter(p => p.is_active).length)
const recentProjects = computed(() => projects.value.slice(0, 5))

onMounted(() => {
  projectStore.fetchProjects()
})
</script>
