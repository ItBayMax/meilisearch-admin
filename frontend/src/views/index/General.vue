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
        <div v-if="indexData?.primaryKey" class="bg-dark-800 rounded-lg p-3">
          <span class="text-gray-300 text-sm">{{ settingsStore.t('primaryKey') }}: <code class="text-primary-400">{{ indexData.primaryKey }}</code></span>
        </div>
        <div>
          <label class="label">{{ settingsStore.t('jsonDocuments') }}</label>
          <textarea
            v-model="docsJson"
            class="input font-mono text-sm"
            rows="12"
            placeholder='[{"id": 1, "title": "Document 1"}]'
          ></textarea>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showAddDocsModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="addDocuments" class="btn btn-primary" :disabled="!docsJson || adding">
            {{ adding ? settingsStore.t('adding') : settingsStore.t('addDocuments') }}
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
import { ref, inject, onMounted } from 'vue'
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
const docsJson = ref('')
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

const addDocuments = async () => {
  if (!docsJson.value) return
  adding.value = true
  try {
    const documents = JSON.parse(docsJson.value)
    await indexApi.addDocuments(projectId.value, indexId.value, documents)
    showAddDocsModal.value = false
    docsJson.value = ''
    fetchStats()
  } catch (err) {
    console.error('Failed to add documents:', err)
    alert('Invalid JSON or failed to add documents')
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
