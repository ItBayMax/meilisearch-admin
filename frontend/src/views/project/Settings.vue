<template>
  <div class="space-y-6">
    <Loading v-if="loading" />

    <template v-else>
      <!-- Basic Info -->
      <div class="space-y-4">
        <h3 class="text-lg font-semibold text-white">{{ settingsStore.t('basicInfo') }}</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label">{{ settingsStore.t('projectName') }}</label>
            <input
              v-model="form.name"
              type="text"
              class="input"
              :placeholder="settingsStore.t('projectName')"
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('projectUrl') }}</label>
            <input
              v-model="form.url"
              type="url"
              class="input"
              placeholder="http://localhost:7700"
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('apiKey') }}</label>
            <input
              v-model="form.api_key"
              type="password"
              class="input"
              :placeholder="settingsStore.t('apiKey')"
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('description') }}</label>
            <input
              v-model="form.description"
              type="text"
              class="input"
              :placeholder="settingsStore.t('optionalDesc')"
            />
          </div>
        </div>

        <div class="flex space-x-3">
          <button @click="saveSettings" class="btn btn-primary" :disabled="saving">
            {{ saving ? settingsStore.t('saving') : settingsStore.t('saveChanges') }}
          </button>
          <button @click="testConnection" class="btn btn-secondary" :disabled="testing">
            {{ testing ? settingsStore.t('testing') : settingsStore.t('testConnection') }}
          </button>
        </div>
      </div>

      <!-- Instance Info -->
      <div class="space-y-4 pt-6 border-t border-dark-700">
        <h3 class="text-lg font-semibold text-white">{{ settingsStore.t('instanceInfo') }}</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="card p-4">
            <label class="text-gray-500 text-xs">{{ settingsStore.t('version') }}</label>
            <p class="text-white text-lg font-semibold">{{ instanceInfo.version || 'N/A' }}</p>
          </div>
          <div class="card p-4">
            <label class="text-gray-500 text-xs">{{ settingsStore.t('databaseSize') }}</label>
            <p class="text-white text-lg font-semibold">{{ instanceInfo.databaseSize || 'N/A' }}</p>
          </div>
          <div class="card p-4">
            <label class="text-gray-500 text-xs">{{ settingsStore.t('status') }}</label>
            <p>
              <span :class="instanceInfo.healthy ? 'badge badge-success' : 'badge badge-danger'">
                {{ instanceInfo.healthy ? settingsStore.t('healthy') : settingsStore.t('unhealthy') }}
              </span>
            </p>
          </div>
        </div>
      </div>

      <!-- Danger Zone -->
      <div class="space-y-4 pt-6 border-t border-dark-700">
        <h3 class="text-lg font-semibold text-red-400">{{ settingsStore.t('dangerZone') }}</h3>
        
        <div class="card border-red-500/30 p-4">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-white font-medium">{{ settingsStore.t('deleteProject') }}</h4>
              <p class="text-gray-500 text-sm">{{ settingsStore.t('deleteProjectDesc') }}</p>
            </div>
            <button @click="showDeleteModal = true" class="btn btn-danger">
              {{ settingsStore.t('deleteProject') }}
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- Delete Confirmation Modal -->
    <Modal v-model:visible="showDeleteModal" :title="settingsStore.t('deleteProject')" size="sm">
      <p class="text-gray-300">
        {{ settingsStore.t('deleteProjectConfirm') }}
      </p>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showDeleteModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="deleteProject" class="btn btn-danger" :disabled="deleting">
            {{ deleting ? settingsStore.t('deleting') : settingsStore.t('delete') }}
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '@/store/project'
import { useSettingsStore } from '@/store/settings'
import { projectApi } from '@/api'
import Modal from '@/components/common/Modal.vue'
import Loading from '@/components/common/Loading.vue'

const router = useRouter()
const projectId = inject('projectId')
const project = inject('project')
const projectStore = useProjectStore()
const settingsStore = useSettingsStore()

const loading = ref(false)
const saving = ref(false)
const testing = ref(false)
const deleting = ref(false)
const showDeleteModal = ref(false)

const form = reactive({
  name: '',
  url: '',
  api_key: '',
  description: '',
})

const instanceInfo = reactive({
  version: null,
  databaseSize: null,
  healthy: false,
})

const loadProjectData = () => {
  if (project.value) {
    form.name = project.value.name || ''
    form.url = project.value.url || ''
    form.api_key = project.value.api_key || ''
    form.description = project.value.description || ''
  }
}

const fetchInstanceInfo = async () => {
  try {
    const result = await projectApi.getStats(projectId.value)
    if (result.success && result.data) {
      instanceInfo.version = result.data.version?.pkgVersion
      instanceInfo.databaseSize = formatBytes(result.data.stats?.databaseSize)
      instanceInfo.healthy = result.data.healthy
    }
  } catch {
    instanceInfo.healthy = false
  }
}

const saveSettings = async () => {
  saving.value = true
  try {
    await projectStore.updateProject(projectId.value, form)
  } catch (err) {
    console.error('Failed to save settings:', err)
  } finally {
    saving.value = false
  }
}

const testConnection = async () => {
  testing.value = true
  try {
    const result = await projectApi.testConnection(form.url, form.api_key)
    if (result.success) {
      alert(settingsStore.t('connectionSuccess'))
      fetchInstanceInfo()
    } else {
      alert(settingsStore.t('connectionFailedMsg') + ': ' + result.error)
    }
  } catch (err) {
    alert(settingsStore.t('connectionFailedMsg'))
  } finally {
    testing.value = false
  }
}

const deleteProject = async () => {
  deleting.value = true
  try {
    await projectStore.deleteProject(parseInt(projectId.value))
    router.push('/projects')
  } catch (err) {
    console.error('Failed to delete project:', err)
  } finally {
    deleting.value = false
  }
}

const formatBytes = (bytes) => {
  if (!bytes) return 'N/A'
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  if (bytes === 0) return '0 Bytes'
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return parseFloat((bytes / Math.pow(1024, i)).toFixed(2)) + ' ' + sizes[i]
}

watch(project, loadProjectData, { immediate: true })

onMounted(() => {
  fetchInstanceInfo()
})
</script>
