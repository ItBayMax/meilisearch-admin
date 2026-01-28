<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-semibold text-white">{{ settingsStore.t('indexes') }}</h2>
      <button @click="showCreateModal = true" class="btn btn-primary flex items-center space-x-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span>{{ settingsStore.t('createIndex') }}</span>
      </button>
    </div>

    <!-- Loading -->
    <Loading v-if="loading" />

    <!-- Empty State -->
    <Empty
      v-else-if="indexes.length === 0"
      :title="settingsStore.t('noIndexes')"
      :description="settingsStore.t('noIndexesDesc')"
    >
      <template #action>
        <button @click="showCreateModal = true" class="btn btn-primary mt-4">
          {{ settingsStore.t('createIndex') }}
        </button>
      </template>
    </Empty>

    <!-- Index Cards -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="index in indexes"
        :key="index.uid"
        class="card card-hover p-5 cursor-pointer"
        @click="goToIndex(index.uid)"
      >
        <div class="flex items-start justify-between mb-3">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-indigo-500/20 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
              </svg>
            </div>
            <div>
              <h3 class="text-white font-medium">{{ index.uid }}</h3>
              <p class="text-gray-500 text-xs">{{ settingsStore.t('primaryKey') }}: {{ index.primaryKey || settingsStore.t('notSet') }}</p>
            </div>
          </div>

          <!-- Actions Menu -->
          <div class="relative" @click.stop>
            <button
              @click="toggleMenu(index.uid)"
              class="p-1 rounded hover:bg-dark-700 text-gray-400 hover:text-white"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
              </svg>
            </button>
            <div
              v-if="activeMenu === index.uid"
              class="absolute right-0 mt-1 w-40 bg-dark-800 rounded-lg shadow-lg border border-dark-600 py-1 z-10"
            >
              <button
                @click="goToIndex(index.uid)"
                class="w-full px-4 py-2 text-left text-sm text-gray-300 hover:bg-dark-700 hover:text-white"
              >
                {{ settingsStore.t('settings') }}
              </button>
              <button
                @click="openAddDocuments(index)"
                class="w-full px-4 py-2 text-left text-sm text-gray-300 hover:bg-dark-700 hover:text-white"
              >
                {{ settingsStore.t('addDocuments') }}
              </button>
              <button
                @click="goToSearch(index.uid)"
                class="w-full px-4 py-2 text-left text-sm text-gray-300 hover:bg-dark-700 hover:text-white"
              >
                {{ settingsStore.t('preview') }}
              </button>
              <hr class="my-1 border-dark-600" />
              <button
                @click="confirmDelete(index)"
                class="w-full px-4 py-2 text-left text-sm text-red-400 hover:bg-dark-700"
              >
                {{ settingsStore.t('delete') }}
              </button>
            </div>
          </div>
        </div>

        <div class="flex items-center space-x-4 text-sm">
          <div class="flex items-center space-x-1 text-gray-400">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>{{ indexStats[index.uid]?.numberOfDocuments || 0 }} docs</span>
          </div>
          <div class="text-gray-500 text-xs">
            {{ settingsStore.t('updated') }}: {{ formatDate(index.updatedAt) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Create Index Modal -->
    <Modal v-model:visible="showCreateModal" :title="settingsStore.t('createIndex')" size="md">
      <form @submit.prevent="createIndex" class="space-y-4">
        <div>
          <label class="label">{{ settingsStore.t('indexUid') }} *</label>
          <input
            v-model="createForm.uid"
            type="text"
            class="input"
            placeholder="my_index"
            pattern="^[a-zA-Z][a-zA-Z0-9_-]*$"
            required
          />
          <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('uidHint') }}</p>
        </div>

        <div>
          <label class="label">{{ settingsStore.t('primaryKey') }}</label>
          <input
            v-model="createForm.primaryKey"
            type="text"
            class="input"
            :placeholder="settingsStore.t('optional')"
          />
          <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('primaryKeyHint') }}</p>
        </div>
      </form>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showCreateModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="createIndex" class="btn btn-primary" :disabled="!createForm.uid || creating">
            {{ creating ? settingsStore.t('creating') : settingsStore.t('create') }}
          </button>
        </div>
      </template>
    </Modal>

    <!-- Add Documents Modal -->
    <Modal v-model:visible="showAddDocsModal" :title="settingsStore.t('addDocuments')" size="lg">
      <div class="space-y-4">
        <div v-if="selectedIndex?.primaryKey" class="bg-dark-800 rounded-lg p-3 flex items-center space-x-2">
          <svg class="w-5 h-5 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-gray-300 text-sm">{{ settingsStore.t('primaryKey') }}: <code class="text-primary-400">{{ selectedIndex.primaryKey }}</code></span>
        </div>

        <div v-else>
          <label class="label">{{ settingsStore.t('primaryKey') }} *</label>
          <input
            v-model="docsForm.primaryKey"
            type="text"
            class="input"
            placeholder="id"
            required
          />
        </div>

        <div>
          <label class="label">{{ settingsStore.t('jsonDocuments') }}</label>
          <textarea
            v-model="docsForm.json"
            class="input font-mono text-sm"
            rows="12"
            placeholder='[{"id": 1, "title": "Document 1"}, {"id": 2, "title": "Document 2"}]'
          ></textarea>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showAddDocsModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="addDocuments" class="btn btn-primary" :disabled="!docsForm.json || addingDocs">
            {{ addingDocs ? settingsStore.t('adding') : settingsStore.t('addDocuments') }}
          </button>
        </div>
      </template>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal v-model:visible="showDeleteModal" :title="settingsStore.t('deleteIndex')" size="sm">
      <p class="text-gray-300">
        {{ settingsStore.t('deleteConfirm') }} <span class="text-white font-semibold">{{ selectedIndex?.uid }}</span>?
        {{ settingsStore.t('cannotUndo') }}
      </p>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showDeleteModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="deleteIndex" class="btn btn-danger" :disabled="deleting">
            {{ deleting ? settingsStore.t('deleting') : settingsStore.t('delete') }}
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSettingsStore } from '@/store/settings'
import { indexApi } from '@/api'
import Modal from '@/components/common/Modal.vue'
import Loading from '@/components/common/Loading.vue'
import Empty from '@/components/common/Empty.vue'

const router = useRouter()
const settingsStore = useSettingsStore()
const projectId = inject('projectId')

const indexes = ref([])
const indexStats = reactive({})
const loading = ref(false)
const creating = ref(false)
const deleting = ref(false)
const addingDocs = ref(false)
const activeMenu = ref(null)

const showCreateModal = ref(false)
const showAddDocsModal = ref(false)
const showDeleteModal = ref(false)
const selectedIndex = ref(null)

const createForm = reactive({ uid: '', primaryKey: '' })
const docsForm = reactive({ primaryKey: '', json: '' })

const fetchIndexes = async () => {
  loading.value = true
  try {
    const result = await indexApi.getAll(projectId.value)
    indexes.value = result.data || []
    // Fetch stats for each index
    for (const index of indexes.value) {
      try {
        const statsResult = await indexApi.getStats(projectId.value, index.uid)
        if (statsResult.success) {
          indexStats[index.uid] = statsResult.data
        }
      } catch {
        // Ignore stats errors
      }
    }
  } catch (err) {
    console.error('Failed to fetch indexes:', err)
  } finally {
    loading.value = false
  }
}

const createIndex = async () => {
  if (!createForm.uid) return
  creating.value = true
  try {
    await indexApi.create(projectId.value, createForm.uid, createForm.primaryKey || null)
    showCreateModal.value = false
    createForm.uid = ''
    createForm.primaryKey = ''
    fetchIndexes()
  } catch (err) {
    console.error('Failed to create index:', err)
  } finally {
    creating.value = false
  }
}

const openAddDocuments = (index) => {
  selectedIndex.value = index
  docsForm.primaryKey = ''
  docsForm.json = ''
  activeMenu.value = null
  showAddDocsModal.value = true
}

const addDocuments = async () => {
  if (!docsForm.json) return
  addingDocs.value = true
  try {
    const documents = JSON.parse(docsForm.json)
    const primaryKey = selectedIndex.value?.primaryKey || docsForm.primaryKey || null
    await indexApi.addDocuments(projectId.value, selectedIndex.value.uid, documents, primaryKey)
    showAddDocsModal.value = false
    fetchIndexes()
  } catch (err) {
    console.error('Failed to add documents:', err)
    alert('Invalid JSON format or failed to add documents')
  } finally {
    addingDocs.value = false
  }
}

const confirmDelete = (index) => {
  selectedIndex.value = index
  activeMenu.value = null
  showDeleteModal.value = true
}

const deleteIndex = async () => {
  if (!selectedIndex.value) return
  deleting.value = true
  try {
    await indexApi.delete(projectId.value, selectedIndex.value.uid)
    showDeleteModal.value = false
    fetchIndexes()
  } catch (err) {
    console.error('Failed to delete index:', err)
  } finally {
    deleting.value = false
  }
}

const goToIndex = (uid) => {
  router.push(`/projects/${projectId.value}/indexes/${uid}`)
}

const goToSearch = (uid) => {
  router.push(`/projects/${projectId.value}/search?index=${uid}`)
  activeMenu.value = null
}

const toggleMenu = (uid) => {
  activeMenu.value = activeMenu.value === uid ? null : uid
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString()
}

const closeMenu = () => {
  activeMenu.value = null
}

onMounted(() => {
  fetchIndexes()
  document.addEventListener('click', closeMenu)
})

onUnmounted(() => {
  document.removeEventListener('click', closeMenu)
})
</script>
