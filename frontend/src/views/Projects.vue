<template>
  <div class="space-y-6 fade-in">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-white">{{ settingsStore.t('projects') }}</h1>
        <p class="text-gray-400 mt-1">{{ settingsStore.t('manageInstances') }}</p>
      </div>
      <button @click="showCreateModal = true" class="btn btn-primary flex items-center space-x-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span>{{ settingsStore.t('addProject') }}</span>
      </button>
    </div>

    <!-- Loading -->
    <Loading v-if="loading" />

    <!-- Empty State -->
    <Empty
      v-else-if="projects.length === 0"
      :title="settingsStore.t('noProjects')"
      :description="settingsStore.t('noProjectsDesc')"
    >
      <template #action>
        <button @click="showCreateModal = true" class="btn btn-primary mt-4">
          {{ settingsStore.t('addProject') }}
        </button>
      </template>
    </Empty>

    <!-- Project Cards -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="project in projects"
        :key="project.id"
        class="card card-hover cursor-pointer"
        @click="$router.push(`/projects/${project.id}`)"
      >
        <div class="p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-indigo-500 rounded-xl flex items-center justify-center">
              <span class="text-white font-bold text-lg">{{ project.name.charAt(0).toUpperCase() }}</span>
            </div>
            <span class="badge badge-success">{{ settingsStore.t('active') }}</span>
          </div>

          <h3 class="text-lg font-semibold text-white mb-1">{{ project.name }}</h3>
          <p class="text-gray-500 text-sm truncate mb-4">{{ project.url }}</p>

          <div class="grid grid-cols-3 gap-4 pt-4 border-t border-dark-700">
            <div class="text-center">
              <p class="text-xl font-bold text-white">{{ projectStats[project.id]?.indexes || '-' }}</p>
              <p class="text-xs text-gray-500">{{ settingsStore.t('indexes') }}</p>
            </div>
            <div class="text-center">
              <p class="text-xl font-bold text-white">{{ projectStats[project.id]?.documents || '-' }}</p>
              <p class="text-xs text-gray-500">{{ settingsStore.t('documents') }}</p>
            </div>
            <div class="text-center">
              <p class="text-xl font-bold text-white">{{ projectStats[project.id]?.searches || '-' }}</p>
              <p class="text-xs text-gray-500">{{ settingsStore.t('searches') }}</p>
            </div>
          </div>
        </div>

        <div class="px-6 py-3 bg-dark-800/50 border-t border-dark-700 flex items-center justify-between">
          <button
            @click.stop="copyToClipboard(project.url)"
            class="text-gray-400 hover:text-white text-sm flex items-center space-x-1"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            <span>{{ settingsStore.t('copyUrl') }}</span>
          </button>
          <button
            @click.stop="$router.push(`/projects/${project.id}/search`)"
            class="text-primary-400 hover:text-primary-300 text-sm"
          >
            {{ settingsStore.t('searchPreview') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Create Project Modal -->
    <Modal v-model:visible="showCreateModal" :title="settingsStore.t('addProject')" size="md">
      <form @submit.prevent="createProject" class="space-y-4">
        <div>
          <label class="label">{{ settingsStore.t('projectName') }} *</label>
          <input
            v-model="form.name"
            type="text"
            class="input"
            placeholder="My Meilisearch Instance"
            required
          />
        </div>

        <div>
          <label class="label">{{ settingsStore.t('projectUrl') }} *</label>
          <input
            v-model="form.url"
            type="url"
            class="input"
            placeholder="http://localhost:7700"
            required
          />
        </div>

        <div>
          <label class="label">{{ settingsStore.t('masterApiKey') }}</label>
          <input
            v-model="form.api_key"
            type="password"
            class="input"
            :placeholder="settingsStore.t('optional')"
          />
        </div>

        <div>
          <label class="label">{{ settingsStore.t('description') }}</label>
          <textarea
            v-model="form.description"
            class="input"
            rows="3"
            :placeholder="settingsStore.t('optionalDesc')"
          ></textarea>
        </div>

        <div class="flex items-center space-x-3">
          <button
            type="button"
            @click="testConnection"
            class="btn btn-secondary flex items-center space-x-2"
            :disabled="testing || !form.url"
          >
            <svg v-if="testing" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>{{ testing ? settingsStore.t('testing') : settingsStore.t('testConnection') }}</span>
          </button>
          <span v-if="connectionStatus === 'success'" class="text-green-400 text-sm">{{ settingsStore.t('connected') }}</span>
          <span v-if="connectionStatus === 'error'" class="text-red-400 text-sm">{{ settingsStore.t('connectionFailed') }}</span>
        </div>
      </form>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showCreateModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="createProject" class="btn btn-primary" :disabled="!form.name || !form.url || creating">
            {{ creating ? settingsStore.t('creating') : settingsStore.t('createProject') }}
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useProjectStore } from '@/store/project'
import { useSettingsStore } from '@/store/settings'
import { projectApi } from '@/api'
import Modal from '@/components/common/Modal.vue'
import Loading from '@/components/common/Loading.vue'
import Empty from '@/components/common/Empty.vue'

const projectStore = useProjectStore()
const settingsStore = useSettingsStore()

const showCreateModal = ref(false)
const testing = ref(false)
const creating = ref(false)
const connectionStatus = ref(null)
const projectStats = reactive({})

const form = reactive({
  name: '',
  url: '',
  api_key: '',
  description: '',
})

const projects = computed(() => projectStore.projects)
const loading = computed(() => projectStore.loading)

const resetForm = () => {
  form.name = ''
  form.url = ''
  form.api_key = ''
  form.description = ''
  connectionStatus.value = null
}

const testConnection = async () => {
  testing.value = true
  connectionStatus.value = null
  try {
    const result = await projectApi.testConnection(form.url, form.api_key)
    connectionStatus.value = result.success ? 'success' : 'error'
  } catch {
    connectionStatus.value = 'error'
  } finally {
    testing.value = false
  }
}

const createProject = async () => {
  if (!form.name || !form.url) return
  creating.value = true
  try {
    await projectStore.createProject({
      name: form.name,
      url: form.url,
      api_key: form.api_key,
      description: form.description,
    })
    showCreateModal.value = false
    resetForm()
  } catch (err) {
    console.error('Failed to create project:', err)
  } finally {
    creating.value = false
  }
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
  } catch {
    console.error('Failed to copy')
  }
}

const fetchProjectStats = async () => {
  for (const project of projects.value) {
    try {
      const result = await projectApi.getStats(project.id)
      if (result.success && result.data?.stats) {
        const stats = result.data.stats
        projectStats[project.id] = {
          indexes: Object.keys(stats.indexes || {}).length,
          documents: Object.values(stats.indexes || {}).reduce((sum, idx) => sum + (idx.numberOfDocuments || 0), 0),
          searches: '-',
        }
      }
    } catch {
      projectStats[project.id] = { indexes: '-', documents: '-', searches: '-' }
    }
  }
}

onMounted(async () => {
  await projectStore.fetchProjects()
  fetchProjectStats()
})
</script>
