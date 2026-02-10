<template>
  <div class="space-y-6">
    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="card p-4">
        <label class="text-gray-500 text-xs">{{ settingsStore.t('documents') }}</label>
        <p class="text-2xl font-bold text-white">{{ stats?.numberOfDocuments || 0 }}</p>
      </div>
      <div class="card p-4">
        <label class="text-gray-500 text-xs">{{ settingsStore.t('primaryKey') }}</label>
        <p class="text-lg font-semibold text-white">{{ indexData?.primaryKey || settingsStore.t('notSet') }}</p>
      </div>
      <div class="card p-4">
        <label class="text-gray-500 text-xs">{{ settingsStore.t('status') }}</label>
        <p><span class="badge badge-success">{{ settingsStore.t('indexing') }}</span></p>
      </div>
    </div>

    <!-- Field Distribution -->
    <div v-if="stats?.fieldDistribution" class="card p-6">
      <h3 class="text-lg font-semibold text-white mb-4">{{ settingsStore.t('fieldDistribution') }}</h3>
      <div class="space-y-3">
        <div
          v-for="(count, field) in stats.fieldDistribution"
          :key="field"
          class="flex items-center justify-between"
        >
          <span class="text-gray-300">{{ field }}</span>
          <span class="text-gray-500 font-mono text-sm">{{ count }}</span>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="card p-6">
      <h3 class="text-lg font-semibold text-white mb-4">{{ settingsStore.t('actions') }}</h3>
      <div class="flex flex-wrap gap-3">
        <button @click="showAddDocsModal = true" class="btn btn-primary">
          {{ settingsStore.t('addDocuments') }}
        </button>
        <button @click="showDeleteDocsModal = true" class="btn btn-secondary">
          {{ settingsStore.t('deleteAllDocuments') }}
        </button>
        <button @click="showDeleteModal = true" class="btn btn-danger">
          {{ settingsStore.t('deleteIndex') }}
        </button>
      </div>
    </div>

    <!-- Add Documents Modal -->
    <Modal v-model:visible="showAddDocsModal" :title="settingsStore.t('addDocuments')" size="lg">
      <div class="space-y-4">
        <!-- Tabs for import method selection -->
        <div class="flex border-b border-dark-600 mb-4">
          <button
            @click="addDocsForm.importMethod = 'json'"
            :class="['px-4 py-2 font-medium text-sm', addDocsForm.importMethod === 'json' ? 'text-white border-b-2 border-primary-500' : 'text-gray-400 hover:text-white']"
          >
            {{ settingsStore.t('jsonTabLabel') }}
          </button>
          <button
            @click="addDocsForm.importMethod = 'file'"
            :class="['px-4 py-2 font-medium text-sm', addDocsForm.importMethod === 'file' ? 'text-white border-b-2 border-primary-500' : 'text-gray-400 hover:text-white']"
          >
            {{ settingsStore.t('fileTabLabel') }}
          </button>
          <button
            @click="addDocsForm.importMethod = 'url'"
            :class="['px-4 py-2 font-medium text-sm', addDocsForm.importMethod === 'url' ? 'text-white border-b-2 border-primary-500' : 'text-gray-400 hover:text-white']"
          >
            {{ settingsStore.t('urlTabLabel') }}
          </button>
        </div>

        <!-- Primary Key Info (always visible) -->
        <div v-if="indexData?.primaryKey" class="bg-dark-800 rounded-lg p-3 flex items-center space-x-2 mb-4">
          <svg class="w-5 h-5 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-gray-300 text-sm">{{ settingsStore.t('primaryKey') }}: <code class="text-primary-400">{{ indexData.primaryKey }}</code></span>
        </div>

        <!-- JSON Input Tab -->
        <div v-show="addDocsForm.importMethod === 'json'" class="space-y-4">
          <div v-if="!indexData?.primaryKey">
            <label class="label">{{ settingsStore.t('primaryKey') }}</label>
            <input
              v-model="addDocsForm.primaryKey"
              type="text"
              class="input"
              :placeholder="settingsStore.t('optional')"
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('pasteJson') }}</label>
            <textarea
              v-model="addDocsForm.json"
              class="input font-mono text-sm"
              rows="12"
              :placeholder="settingsStore.t('jsonDocuments') + ' [{\'id\': 1, \'title\': \'Document 1\'}]'"
            ></textarea>
          </div>
        </div>

        <!-- File Upload Tab -->
        <div v-show="addDocsForm.importMethod === 'file'" class="space-y-4">
          <div v-if="!indexData?.primaryKey">
            <label class="label">{{ settingsStore.t('primaryKey') }}</label>
            <input
              v-model="addDocsForm.filePrimaryKey"
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
                {{ addDocsForm.selectedFile ? addDocsForm.selectedFile.name : settingsStore.t('chooseFile') }}
              </button>
              <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('uploadJsonCsv') }}</p>
            </div>
          </div>
        </div>

        <!-- URL Fetch Tab -->
        <div v-show="addDocsForm.importMethod === 'url'" class="space-y-4">
          <div v-if="!indexData?.primaryKey">
            <label class="label">{{ settingsStore.t('primaryKey') }}</label>
            <input
              v-model="addDocsForm.urlPrimaryKey"
              type="text"
              class="input"
              :placeholder="settingsStore.t('optional')"
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('remoteUrl') }}</label>
            <input
              v-model="addDocsForm.url"
              type="url"
              class="input"
              :placeholder="settingsStore.t('enterValidUrl')"
              required
            />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('fieldPath') }}</label>
            <input
              v-model="addDocsForm.fieldPath"
              type="text"
              class="input"
              :placeholder="settingsStore.t('fieldPathPlaceholder')"
            />
            <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('fieldPathHint') }}</p>
          </div>
          <div>
            <label class="label">{{ settingsStore.t('headers') }}</label>
            <textarea
              v-model="addDocsForm.headers"
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
            {{ adding ? settingsStore.t('adding') : settingsStore.t('import') }}
          </button>
        </div>
      </template>
    </Modal>

    <!-- Delete Documents Modal -->
    <Modal v-model:visible="showDeleteDocsModal" :title="settingsStore.t('deleteAllDocuments')" size="sm">
      <p class="text-gray-300">{{ settingsStore.t('deleteAllDocsConfirm') }}</p>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showDeleteDocsModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="deleteAllDocuments" class="btn btn-danger" :disabled="deletingDocs">
            {{ deletingDocs ? settingsStore.t('deleting') : settingsStore.t('deleteAll') }}
          </button>
        </div>
      </template>
    </Modal>

    <!-- Delete Index Modal -->
    <Modal v-model:visible="showDeleteModal" :title="settingsStore.t('deleteIndex')" size="sm">
      <p class="text-gray-300">{{ settingsStore.t('deleteIndexConfirm') }}</p>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showDeleteModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="deleteIndex" class="btn btn-danger" :disabled="deleting">
            {{ deleting ? settingsStore.t('deleting') : settingsStore.t('deleteIndex') }}
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSettingsStore } from '@/store/settings'
import { indexApi } from '@/api'
import Modal from '@/components/common/Modal.vue'

const router = useRouter()
const settingsStore = useSettingsStore()
const projectId = inject('projectId')
const indexId = inject('indexId')
const indexData = inject('indexData')

const stats = ref(null)
const addDocsForm = ref({
  importMethod: 'json',  // json, file, or url
  json: '',
  selectedFile: null,
  primaryKey: '',
  filePrimaryKey: '',
  url: '',
  fieldPath: '',
  urlPrimaryKey: '',
  headers: ''
})
const adding = ref(false)
const deleting = ref(false)
const deletingDocs = ref(false)
const showAddDocsModal = ref(false)
const showDeleteDocsModal = ref(false)
const showDeleteModal = ref(false)

const fetchStats = async () => {
  try {
    const result = await indexApi.getStats(projectId.value, indexId.value)
    if (result.success) {
      stats.value = result.data
    }
  } catch (err) {
    console.error('Failed to fetch stats:', err)
  }
}

const fileInputRef = ref(null)

const onFileChange = (event) => {
  addDocsForm.value.selectedFile = event.target.files[0]
}

const isAddDisabled = computed(() => {
  if (addDocsForm.value.importMethod === 'json') {
    return !addDocsForm.value.json || adding.value
  } else if (addDocsForm.value.importMethod === 'file') {
    return !addDocsForm.value.selectedFile || adding.value
  } else if (addDocsForm.value.importMethod === 'url') {
    return !addDocsForm.value.url || adding.value
  }
  return true
})

const getAddButtonTitle = computed(() => {
  if (addDocsForm.value.importMethod === 'json' && !addDocsForm.value.json) {
    return settingsStore.t('jsonDocuments') + ' ' + settingsStore.t('required')
  } else if (addDocsForm.value.importMethod === 'file' && !addDocsForm.value.selectedFile) {
    return settingsStore.t('file') + ' ' + settingsStore.t('required')
  } else if (addDocsForm.value.importMethod === 'url' && !addDocsForm.value.url) {
    return settingsStore.t('remoteUrl') + ' ' + settingsStore.t('required')
  }
  return ''
})

const addDocuments = async () => {
  if (isAddDisabled.value) return
  adding.value = true
  
  try {
    if (addDocsForm.value.importMethod === 'json') {
      // Original JSON method
      const documents = JSON.parse(addDocsForm.value.json)
      await indexApi.addDocuments(projectId.value, indexId.value, documents)
    } else if (addDocsForm.value.importMethod === 'file') {
      // File upload method
      const primaryKey = indexData.value?.primaryKey || addDocsForm.value.filePrimaryKey || null
      await indexApi.uploadDocumentsFile(projectId.value, indexId.value, addDocsForm.value.selectedFile, primaryKey)
    } else if (addDocsForm.value.importMethod === 'url') {
      // URL fetch method
      let headersObj = {}
      if (addDocsForm.value.headers.trim()) {
        try {
          headersObj = JSON.parse(addDocsForm.value.headers)
        } catch {
          alert(settingsStore.t('invalidHeadersFormat'))
          return
        }
      }
      const primaryKey = indexData.value?.primaryKey || addDocsForm.value.urlPrimaryKey || null
      await indexApi.fetchDocumentsFromUrl(
        projectId.value, 
        indexId.value, 
        addDocsForm.value.url, 
        addDocsForm.value.fieldPath,
        primaryKey,
        headersObj
      )
    }
    
    showAddDocsModal.value = false
    fetchStats()
    // Reset form
    addDocsForm.value.json = ''
    addDocsForm.value.selectedFile = null
    addDocsForm.value.primaryKey = ''
    addDocsForm.value.filePrimaryKey = ''
    addDocsForm.value.url = ''
    addDocsForm.value.fieldPath = ''
    addDocsForm.value.urlPrimaryKey = ''
    addDocsForm.value.headers = ''
  } catch (err) {
    console.error('Failed to add documents:', err)
    let errorMsg = err.message || 'Unknown error'
    if (err.response?.data?.error) {
      errorMsg = err.response.data.error
    }
    alert(settingsStore.t('failedToAddDocuments') + ': ' + errorMsg)
  } finally {
    adding.value = false
  }
}

const deleteAllDocuments = async () => {
  deletingDocs.value = true
  try {
    await indexApi.deleteAllDocuments(projectId.value, indexId.value)
    showDeleteDocsModal.value = false
    fetchStats()
  } catch (err) {
    console.error('Failed to delete documents:', err)
  } finally {
    deletingDocs.value = false
  }
}

const deleteIndex = async () => {
  deleting.value = true
  try {
    await indexApi.delete(projectId.value, indexId.value)
    router.push(`/projects/${projectId.value}`)
  } catch (err) {
    console.error('Failed to delete index:', err)
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>
