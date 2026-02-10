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
        <!-- Tabs for import method selection -->
        <div class="flex border-b border-dark-600 mb-4">
          <button
            @click="docsForm.importMethod = 'json'"
            :class="['px-4 py-2 font-medium text-sm', docsForm.importMethod === 'json' ? 'text-white border-b-2 border-primary-500' : 'text-gray-400 hover:text-white']"
          >
            {{ settingsStore.t('jsonTabLabel') }}
          </button>
          <button
            @click="docsForm.importMethod = 'file'"
            :class="['px-4 py-2 font-medium text-sm', docsForm.importMethod === 'file' ? 'text-white border-b-2 border-primary-500' : 'text-gray-400 hover:text-white']"
          >
            {{ settingsStore.t('fileTabLabel') }}
          </button>
          <button
            @click="docsForm.importMethod = 'url'"
            :class="['px-4 py-2 font-medium text-sm', docsForm.importMethod === 'url' ? 'text-white border-b-2 border-primary-500' : 'text-gray-400 hover:text-white']"
          >
            {{ settingsStore.t('urlTabLabel') }}
          </button>
        </div>

        <!-- Primary Key Info (always visible) -->
        <div v-if="selectedIndex?.primaryKey" class="bg-dark-800 rounded-lg p-3 flex items-center space-x-2 mb-4">
          <svg class="w-5 h-5 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-gray-300 text-sm">{{ settingsStore.t('primaryKey') }}: <code class="text-primary-400">{{ selectedIndex.primaryKey }}</code></span>
        </div>

        <!-- JSON Input Tab -->
        <div v-show="docsForm.importMethod === 'json'" class="space-y-4">
          <div v-if="!selectedIndex?.primaryKey">
            <label class="label">{{ settingsStore.t('primaryKey') }}</label>
            <input
              v-model="docsForm.primaryKey"
              type="text"
              class="input"
              :placeholder="settingsStore.t('optional')"
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('pasteJson') }}</label>
            <textarea
              v-model="docsForm.json"
              class="input font-mono text-sm"
              rows="12"
              :placeholder="settingsStore.t('jsonDocuments') + ' [{\'id\': 1, \'title\': \'Document 1\'}, {\'id\': 2, \'title\': \'Document 2\'}]'"
            ></textarea>
          </div>
        </div>

        <!-- File Upload Tab -->
        <div v-show="docsForm.importMethod === 'file'" class="space-y-4">
          <div v-if="!selectedIndex?.primaryKey">
            <label class="label">{{ settingsStore.t('primaryKey') }}</label>
            <input
              v-model="docsForm.filePrimaryKey"
              type="text"
              class="input"
              :placeholder="settingsStore.t('optional')"
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('file') }}</label>
            <div class="relative">
              <input
                type="file"
                ref="fileInputRef"
                @change="onFileChange"
                accept=".json,.csv"
                class="hidden"
              />
              <button
                @click="$refs.fileInputRef.click()"
                type="button"
                class="w-full flex items-center justify-center px-4 py-2 border border-dark-600 rounded-lg bg-dark-800 hover:bg-dark-700 text-gray-300"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                {{ docsForm.selectedFile ? docsForm.selectedFile.name : settingsStore.t('chooseFile') }}
              </button>
              <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('uploadJsonCsv') }}</p>
            </div>
          </div>
        </div>

        <!-- URL Fetch Tab -->
        <div v-show="docsForm.importMethod === 'url'" class="space-y-4">
          <div v-if="!selectedIndex?.primaryKey">
            <label class="label">{{ settingsStore.t('primaryKey') }}</label>
            <input
              v-model="docsForm.urlPrimaryKey"
              type="text"
              class="input"
              :placeholder="settingsStore.t('optional')"
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('remoteUrl') }}</label>
            <input
              v-model="docsForm.url"
              type="url"
              class="input"
              :placeholder="settingsStore.t('enterValidUrl')"
              required
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('fieldPath') }}</label>
            <input
              v-model="docsForm.fieldPath"
              type="text"
              class="input"
              :placeholder="settingsStore.t('fieldPathPlaceholder')"
            />
            <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('fieldPathHint') }}</p>
          </div>
          <div>
            <label class="label">{{ settingsStore.t('headers') }}</label>
            <textarea
              v-model="docsForm.headers"
              class="input font-mono text-sm"
              rows="2"
              :placeholder="settingsStore.t('headersPlaceholder')"
            ></textarea>
            <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('headersHint') }}</p>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showAddDocsModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="addDocuments" class="btn btn-primary" :disabled="isAddDisabled" :title="getAddButtonTitle">
            {{ addingDocs ? settingsStore.t('adding') : settingsStore.t('import') }}
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
import { ref, reactive, computed, inject, onMounted, onUnmounted } from 'vue'
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
const docsForm = reactive({
  importMethod: 'json',  // json, file, or url
  primaryKey: '',
  json: '',
  selectedFile: null,
  filePrimaryKey: '',
  url: '',
  fieldPath: '',
  urlPrimaryKey: '',
  headers: ''
})

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
  // Reset form when opening
  docsForm.json = ''
  docsForm.selectedFile = null
  docsForm.primaryKey = ''
  docsForm.filePrimaryKey = ''
  docsForm.url = ''
  docsForm.fieldPath = ''
  docsForm.urlPrimaryKey = ''
  docsForm.headers = ''
  activeMenu.value = null
  showAddDocsModal.value = true
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


const fileInputRef = ref(null)

const onFileChange = (event) => {
  docsForm.selectedFile = event.target.files[0]
}

const isAddDisabled = computed(() => {
  if (docsForm.importMethod === 'json') {
    return !docsForm.json || addingDocs.value
  } else if (docsForm.importMethod === 'file') {
    return !docsForm.selectedFile || addingDocs.value
  } else if (docsForm.importMethod === 'url') {
    return !docsForm.url || addingDocs.value
  }
  return true
})

const getAddButtonTitle = computed(() => {
  if (docsForm.importMethod === 'json' && !docsForm.json) {
    return settingsStore.t('jsonDocuments') + ' ' + settingsStore.t('required')
  } else if (docsForm.importMethod === 'file' && !docsForm.selectedFile) {
    return settingsStore.t('file') + ' ' + settingsStore.t('required')
  } else if (docsForm.importMethod === 'url' && !docsForm.url) {
    return settingsStore.t('remoteUrl') + ' ' + settingsStore.t('required')
  }
  return ''
})

const addDocuments = async () => {
  if (isAddDisabled.value) return
  addingDocs.value = true
  
  try {
    if (docsForm.importMethod === 'json') {
      // Original JSON method
      const documents = JSON.parse(docsForm.json)
      const primaryKey = selectedIndex.value?.primaryKey || docsForm.primaryKey || null
      await indexApi.addDocuments(projectId.value, selectedIndex.value.uid, documents, primaryKey)
    } else if (docsForm.importMethod === 'file') {
      // File upload method
      const primaryKey = selectedIndex.value?.primaryKey || docsForm.filePrimaryKey || null
      await indexApi.uploadDocumentsFile(projectId.value, selectedIndex.value.uid, docsForm.selectedFile, primaryKey)
    } else if (docsForm.importMethod === 'url') {
      // URL fetch method
      let headersObj = {}
      if (docsForm.headers.trim()) {
        try {
          headersObj = JSON.parse(docsForm.headers)
        } catch {
          alert(settingsStore.t('invalidHeadersFormat'))
          return
        }
      }
      const primaryKey = selectedIndex.value?.primaryKey || docsForm.urlPrimaryKey || null
      await indexApi.fetchDocumentsFromUrl(
        projectId.value, 
        selectedIndex.value.uid, 
        docsForm.url, 
        docsForm.fieldPath,
        primaryKey,
        headersObj
      )
    }
    
    showAddDocsModal.value = false
    fetchIndexes()
    // Reset form
    docsForm.json = ''
    docsForm.selectedFile = null
    docsForm.primaryKey = ''
    docsForm.filePrimaryKey = ''
    docsForm.url = ''
    docsForm.fieldPath = ''
    docsForm.urlPrimaryKey = ''
    docsForm.headers = ''
  } catch (err) {
    console.error('Failed to add documents:', err)
    let errorMsg = err.message || 'Unknown error'
    if (err.response?.data?.error) {
      errorMsg = err.response.data.error
    }
    alert(settingsStore.t('failedToAddDocuments') + ': ' + errorMsg)
  } finally {
    addingDocs.value = false
  }
}

// Call on component mount
onMounted(() => {
  fetchIndexes()
  document.addEventListener('click', closeMenu)
})

</script>
