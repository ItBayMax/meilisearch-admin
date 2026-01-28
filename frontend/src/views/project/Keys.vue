<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-semibold text-white">{{ settingsStore.t('apiKeys') }}</h2>
      <button @click="showCreateModal = true" class="btn btn-primary flex items-center space-x-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span>{{ settingsStore.t('createKey') }}</span>
      </button>
    </div>

    <!-- Loading -->
    <Loading v-if="loading" />

    <!-- Keys List -->
    <div v-else class="space-y-4">
      <div
        v-for="key in keys"
        :key="key.uid"
        class="card p-5"
      >
        <div class="flex items-start justify-between mb-4">
          <div>
            <h3 class="text-white font-medium">{{ key.name || settingsStore.t('unnamedKey') }}</h3>
            <p class="text-gray-500 text-sm">{{ key.description || settingsStore.t('noDescription') }}</p>
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click="copyKey(key.key)"
              class="btn btn-ghost text-sm"
            >
              {{ settingsStore.t('copyKey') }}
            </button>
            <button
              v-if="!isDefaultKey(key)"
              @click="confirmDelete(key)"
              class="btn btn-ghost text-red-400 text-sm"
            >
              {{ settingsStore.t('delete') }}
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('key') }}</label>
            <div class="flex items-center space-x-2">
              <p class="text-gray-300 font-mono text-xs truncate flex-1">
                {{ visibleKeys[key.uid] ? key.key : maskKey(key.key) }}
              </p>
              <button
                @click="toggleKeyVisibility(key.uid)"
                class="p-1 text-gray-400 hover:text-white transition-colors"
                :title="visibleKeys[key.uid] ? 'Hide' : 'Show'"
              >
                <!-- Eye Open Icon -->
                <svg v-if="visibleKeys[key.uid]" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <!-- Eye Closed Icon -->
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('uid') }}</label>
            <p class="text-gray-300 font-mono">{{ key.uid }}</p>
          </div>
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('actions') }}</label>
            <div class="flex flex-wrap gap-1 mt-1">
              <span
                v-for="action in key.actions"
                :key="action"
                class="badge badge-info text-xs"
              >
                {{ action }}
              </span>
            </div>
          </div>
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('indexes') }}</label>
            <div class="flex flex-wrap gap-1 mt-1">
              <span
                v-for="idx in key.indexes"
                :key="idx"
                class="badge badge-info text-xs"
              >
                {{ idx }}
              </span>
            </div>
          </div>
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('createdAt') }}</label>
            <p class="text-gray-300">{{ formatDate(key.createdAt) }}</p>
          </div>
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('expiresAt') }}</label>
            <p class="text-gray-300">{{ key.expiresAt ? formatDate(key.expiresAt) : settingsStore.t('never') }}</p>
          </div>
        </div>
      </div>

      <Empty v-if="keys.length === 0" :title="settingsStore.t('noApiKeys')" :description="settingsStore.t('noApiKeysDesc')" />
    </div>

    <!-- Create Key Modal -->
    <Modal v-model:visible="showCreateModal" :title="settingsStore.t('createApiKey')" size="lg">
      <form @submit.prevent="createKey" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">{{ settingsStore.t('name') }}</label>
            <input
              v-model="createForm.name"
              type="text"
              class="input"
              :placeholder="settingsStore.t('name')"
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('uidOptional') }}</label>
            <input
              v-model="createForm.uid"
              type="text"
              class="input"
              :placeholder="settingsStore.t('customUid')"
            />
          </div>
        </div>

        <div>
          <label class="label">{{ settingsStore.t('description') }}</label>
          <input
            v-model="createForm.description"
            type="text"
            class="input"
            :placeholder="settingsStore.t('description')"
          />
        </div>

        <div>
          <label class="label">{{ settingsStore.t('expiresAt') }}</label>
          <input
            v-model="createForm.expiresAt"
            type="datetime-local"
            class="input"
          />
        </div>

        <div>
          <label class="label">{{ settingsStore.t('actionsRequired') }}</label>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-2 mt-2">
            <label
              v-for="action in availableActions"
              :key="action"
              class="flex items-center space-x-2 p-2 rounded-lg bg-dark-800 cursor-pointer hover:bg-dark-700"
            >
              <input
                type="checkbox"
                :value="action"
                v-model="createForm.actions"
              />
              <span class="text-sm text-gray-300">{{ action }}</span>
            </label>
          </div>
        </div>

        <div>
          <label class="label">{{ settingsStore.t('indexesRequired') }}</label>
          <input
            v-model="createForm.indexesInput"
            type="text"
            class="input"
            placeholder="* (all) or index1, index2"
          />
          <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('indexesHint') }}</p>
        </div>
      </form>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showCreateModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="createKey" class="btn btn-primary" :disabled="!isValidForm || creating">
            {{ creating ? settingsStore.t('creating') : settingsStore.t('createKey') }}
          </button>
        </div>
      </template>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal v-model:visible="showDeleteModal" :title="settingsStore.t('deleteApiKey')" size="sm">
      <p class="text-gray-300">
        {{ settingsStore.t('deleteApiKeyConfirm') }}
      </p>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showDeleteModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="deleteKey" class="btn btn-danger" :disabled="deleting">
            {{ deleting ? settingsStore.t('deleting') : settingsStore.t('delete') }}
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject, onMounted } from 'vue'
import { useSettingsStore } from '@/store/settings'
import { keyApi } from '@/api'
import Modal from '@/components/common/Modal.vue'
import Loading from '@/components/common/Loading.vue'
import Empty from '@/components/common/Empty.vue'

const settingsStore = useSettingsStore()
const projectId = inject('projectId')

const keys = ref([])
const loading = ref(false)
const creating = ref(false)
const deleting = ref(false)
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const selectedKey = ref(null)
const visibleKeys = reactive({})

const maskKey = (key) => {
  if (!key) return ''
  return key.substring(0, 8) + '••••••••••••••••' + key.substring(key.length - 4)
}

const toggleKeyVisibility = (uid) => {
  visibleKeys[uid] = !visibleKeys[uid]
}

const availableActions = [
  '*', 'search', 'documents.add', 'documents.get', 'documents.delete',
  'indexes.create', 'indexes.get', 'indexes.update', 'indexes.delete', 'indexes.swap',
  'tasks.get', 'tasks.cancel', 'tasks.delete',
  'settings.get', 'settings.update',
  'stats.get', 'dumps.create', 'snapshots.create',
  'version', 'keys.get', 'keys.create', 'keys.update', 'keys.delete'
]

const createForm = reactive({
  name: '',
  uid: '',
  description: '',
  expiresAt: '',
  actions: [],
  indexesInput: '*',
})

const isValidForm = computed(() => {
  return createForm.actions.length > 0 && createForm.indexesInput.trim()
})

const fetchKeys = async () => {
  loading.value = true
  try {
    const result = await keyApi.getAll(projectId.value)
    keys.value = result.data?.results || []
  } catch (err) {
    console.error('Failed to fetch keys:', err)
  } finally {
    loading.value = false
  }
}

const createKey = async () => {
  if (!isValidForm.value) return
  creating.value = true
  try {
    const indexes = createForm.indexesInput.trim() === '*' 
      ? ['*']
      : createForm.indexesInput.split(',').map(s => s.trim()).filter(Boolean)

    const data = {
      actions: createForm.actions,
      indexes: indexes,
    }
    if (createForm.name) data.name = createForm.name
    if (createForm.uid) data.uid = createForm.uid
    if (createForm.description) data.description = createForm.description
    if (createForm.expiresAt) data.expiresAt = new Date(createForm.expiresAt).toISOString()

    await keyApi.create(projectId.value, data)
    showCreateModal.value = false
    resetForm()
    fetchKeys()
  } catch (err) {
    console.error('Failed to create key:', err)
  } finally {
    creating.value = false
  }
}

const confirmDelete = (key) => {
  selectedKey.value = key
  showDeleteModal.value = true
}

const deleteKey = async () => {
  if (!selectedKey.value) return
  deleting.value = true
  try {
    await keyApi.delete(projectId.value, selectedKey.value.key)
    showDeleteModal.value = false
    fetchKeys()
  } catch (err) {
    console.error('Failed to delete key:', err)
  } finally {
    deleting.value = false
  }
}

const copyKey = async (key) => {
  try {
    await navigator.clipboard.writeText(key)
  } catch {
    console.error('Failed to copy')
  }
}

const isDefaultKey = (key) => {
  return key.name === 'Default Search API Key' || key.name === 'Default Admin API Key'
}

const resetForm = () => {
  createForm.name = ''
  createForm.uid = ''
  createForm.description = ''
  createForm.expiresAt = ''
  createForm.actions = []
  createForm.indexesInput = '*'
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  fetchKeys()
})
</script>
