<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">{{ settingsStore.t('embedders') }}</h3>
        <p class="text-gray-500 text-sm">{{ settingsStore.t('embeddersDesc') }}</p>
      </div>
      <button @click="openAddModal" class="btn btn-primary text-sm">
        {{ settingsStore.t('addEmbedder') }}
      </button>
    </div>

    <!-- Empty State -->
    <div v-if="Object.keys(embedders).length === 0" class="card p-8">
      <div class="text-center">
        <div class="w-16 h-16 bg-dark-800 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
        <h4 class="text-white font-medium mb-2">{{ settingsStore.t('noEmbedders') }}</h4>
        <p class="text-gray-500 text-sm max-w-md mx-auto">
          {{ settingsStore.t('noEmbeddersDesc') }}
        </p>
      </div>
    </div>

    <!-- Embedders List -->
    <div v-else class="space-y-4">
      <div
        v-for="(config, name) in embedders"
        :key="name"
        class="card p-5"
      >
        <div class="flex items-start justify-between mb-4">
          <div>
            <h4 class="text-white font-medium">{{ name }}</h4>
            <span class="badge badge-info mt-1">{{ getSourceLabel(config.source) }}</span>
          </div>
          <div class="flex space-x-2">
            <button @click="editEmbedder(name, config)" class="btn btn-ghost text-sm">{{ settingsStore.t('edit') }}</button>
            <button @click="confirmDelete(name)" class="btn btn-ghost text-red-400 text-sm">{{ settingsStore.t('delete') }}</button>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
          <div v-if="config.model">
            <span class="text-gray-500">{{ settingsStore.t('modelLabel') }}:</span>
            <span class="text-gray-300 ml-2">{{ config.model }}</span>
          </div>
          <div v-if="config.dimensions">
            <span class="text-gray-500">{{ settingsStore.t('dimensionsLabel') }}:</span>
            <span class="text-gray-300 ml-2">{{ config.dimensions }}</span>
          </div>
          <div v-if="config.url">
            <span class="text-gray-500">URL:</span>
            <span class="text-gray-300 ml-2 truncate">{{ config.url }}</span>
          </div>
          <div v-if="config.revision">
            <span class="text-gray-500">{{ settingsStore.t('revision') }}:</span>
            <span class="text-gray-300 ml-2">{{ config.revision }}</span>
          </div>
          <div v-if="config.documentTemplate" class="col-span-2">
            <span class="text-gray-500">{{ settingsStore.t('documentTemplate') }}:</span>
            <span class="text-gray-300 ml-2 truncate block">{{ config.documentTemplate }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <Modal v-model:visible="showModal" :title="editingName ? settingsStore.t('editEmbedder') : settingsStore.t('addEmbedder')" size="lg">
      <form @submit.prevent="saveEmbedder" class="space-y-4">
        <!-- Embedder Name -->
        <div>
          <label class="label">{{ settingsStore.t('embedderName') }}</label>
          <input
            v-model="form.name"
            type="text"
            class="input"
            placeholder="default"
            :disabled="!!editingName"
            required
          />
          <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('embedderNameHint') }}</p>
        </div>

        <!-- Source Selection -->
        <div>
          <label class="label">{{ settingsStore.t('sourceLabel') }}</label>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
            <button
              v-for="src in sources"
              :key="src.value"
              type="button"
              @click.prevent.stop="selectSource(src.value)"
              class="p-3 rounded-lg border text-center transition-colors"
              :class="form.source === src.value ? 'border-primary-500 bg-primary-500/10 text-primary-400' : 'border-dark-600 hover:border-dark-500 text-gray-400'"
            >
              <div class="text-sm font-medium">{{ src.label }}</div>
            </button>
          </div>
        </div>

        <!-- OpenAI Settings -->
        <template v-if="form.source === 'openAi'">
          <div>
            <label class="label">{{ settingsStore.t('apiKeyLabel') }}</label>
            <input v-model="form.apiKey" type="password" class="input" placeholder="sk-..." />
            <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('apiKeyOptional') }}</p>
          </div>
          <div>
            <label class="label">{{ settingsStore.t('modelLabel') }}</label>
            <select v-model="form.model" class="input">
              <option value="">Default (text-embedding-3-small)</option>
              <option value="text-embedding-3-small">text-embedding-3-small</option>
              <option value="text-embedding-3-large">text-embedding-3-large</option>
              <option value="text-embedding-ada-002">text-embedding-ada-002</option>
            </select>
          </div>
          <div>
            <label class="label">{{ settingsStore.t('urlOptional') }}</label>
            <input v-model="form.url" type="url" class="input" placeholder="https://api.openai.com/v1/embeddings" />
          </div>
        </template>

        <!-- Hugging Face Settings -->
        <template v-if="form.source === 'huggingFace'">
          <div>
            <label class="label">{{ settingsStore.t('modelLabel') }}</label>
            <input v-model="form.model" type="text" class="input" placeholder="BAAI/bge-base-en-v1.5" />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('revision') }}</label>
            <input v-model="form.revision" type="text" class="input" />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('poolingLabel') }}</label>
            <select v-model="form.pooling" class="input">
              <option value="">Default (useModel)</option>
              <option value="useModel">useModel</option>
              <option value="forceMean">forceMean</option>
              <option value="forceCls">forceCls</option>
            </select>
          </div>
        </template>

        <!-- Ollama Settings -->
        <template v-if="form.source === 'ollama'">
          <div>
            <label class="label">{{ settingsStore.t('urlRequired') }}</label>
            <input v-model="form.url" type="url" class="input" placeholder="http://localhost:11434/api/embeddings" required />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('modelRequired') }}</label>
            <input v-model="form.model" type="text" class="input" placeholder="nomic-embed-text" required />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('apiKeyOptional') }}</label>
            <input v-model="form.apiKey" type="password" class="input" />
          </div>
        </template>

        <!-- REST API Settings -->
        <template v-if="form.source === 'rest'">
          <div>
            <label class="label">{{ settingsStore.t('urlRequired') }}</label>
            <input v-model="form.url" type="url" class="input" placeholder="https://api.example.com/embed" required />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('apiKeyLabel') }}</label>
            <input v-model="form.apiKey" type="password" class="input" />
          </div>
          <div>
            <label class="label">{{ settingsStore.t('requestTemplate') }}</label>
            <textarea v-model="form.request" class="input font-mono text-sm" rows="4" placeholder='{"input": "{{text}}", "model": "text-embedding-3-small"}'></textarea>
          </div>
          <div>
            <label class="label">{{ settingsStore.t('responseTemplate') }}</label>
            <textarea v-model="form.response" class="input font-mono text-sm" rows="3" placeholder='{"embeddings": "{{embedding}}"}'></textarea>
          </div>
        </template>

        <!-- User Provided Settings -->
        <template v-if="form.source === 'userProvided'">
          <div class="p-4 bg-dark-800 rounded-lg">
            <p class="text-gray-400 text-sm">
              {{ settingsStore.t('userProvidedInfo') }}
            </p>
          </div>
        </template>

        <!-- Common Settings -->
        <div v-if="form.source" class="border-t border-dark-700 pt-4 space-y-4">
          <h4 class="text-white font-medium">{{ settingsStore.t('commonSettings') }}</h4>
          
          <div>
            <label class="label">{{ settingsStore.t('dimensionsLabel') }}</label>
            <input v-model.number="form.dimensions" type="number" class="input" />
            <p class="text-gray-500 text-xs mt-1">{{ settingsStore.t('dimensionsHint') }}</p>
          </div>

          <div v-if="form.source !== 'userProvided'">
            <label class="label">{{ settingsStore.t('documentTemplate') }}</label>
            <textarea
              v-model="form.documentTemplate"
              class="input font-mono text-sm"
              rows="3"
              placeholder="A document titled '{{doc.title}}' with content: {{doc.content}}"
            ></textarea>
            <p class="text-gray-500 text-xs mt-1" v-html="documentTemplateHelpText"></p>
          </div>

          <div v-if="form.source !== 'userProvided'">
            <label class="label">{{ settingsStore.t('documentTemplateMaxBytes') }}</label>
            <input v-model.number="form.documentTemplateMaxBytes" type="number" class="input" placeholder="400" />
          </div>

          <div class="flex items-center space-x-2">
            <input type="checkbox" v-model="form.binaryQuantized" id="binaryQuantized" class="rounded" />
            <label for="binaryQuantized" class="text-gray-300 text-sm">{{ settingsStore.t('binaryQuantized') }}</label>
          </div>
        </div>
      </form>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="closeModal" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="saveEmbedder" class="btn btn-primary" :disabled="!isValidForm || saving">
            {{ saving ? settingsStore.t('saving') : (editingName ? settingsStore.t('updateBtn') : settingsStore.t('add')) }}
          </button>
        </div>
      </template>
    </Modal>

    <!-- Delete Confirmation -->
    <Modal v-model:visible="showDeleteModal" :title="settingsStore.t('deleteEmbedder')" size="sm">
      <p class="text-gray-300">
        {{ settingsStore.t('deleteEmbedderConfirm') }} "<span class="text-white font-medium">{{ deletingName }}</span>"?
        {{ settingsStore.t('deleteEmbedderWarn') }}
      </p>
      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showDeleteModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="deleteEmbedder" class="btn btn-danger" :disabled="deleting">
            {{ deleting ? settingsStore.t('deleting') : settingsStore.t('delete') }}
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject, watch } from 'vue'
import { useSettingsStore } from '@/store/settings'
import { indexApi } from '@/api'
import Modal from '@/components/common/Modal.vue'

const settingsStore = useSettingsStore()

const projectId = inject('projectId')
const indexId = inject('indexId')
const settings = inject('settings')

const embedders = ref({})
const showModal = ref(false)
const showDeleteModal = ref(false)
const editingName = ref(null)
const deletingName = ref(null)
const saving = ref(false)
const deleting = ref(false)

const sources = [
  { value: 'openAi', label: 'OpenAI' },
  { value: 'huggingFace', label: 'Hugging Face' },
  { value: 'ollama', label: 'Ollama' },
  { value: 'rest', label: 'REST API' },
  { value: 'userProvided', label: 'User Provided' },
]

const form = reactive({
  name: '',
  source: '',
  apiKey: '',
  model: '',
  url: '',
  dimensions: null,
  documentTemplate: '',
  documentTemplateMaxBytes: null,
  revision: '',
  pooling: '',
  request: '',
  response: '',
  binaryQuantized: false,
})

const documentTemplateHelpText = computed(() => {
  return 'Liquid template defining data sent to embedder. Use <code class="text-primary-400">{{"{{doc.field}}"}}</code> to reference fields.'
})

const isValidForm = computed(() => {
  if (!form.name || !form.source) return false
  if (form.source === 'ollama' && (!form.url || !form.model)) return false
  if (form.source === 'rest' && !form.url) return false
  return true
})

const getSourceLabel = (source) => {
  const src = sources.find(s => s.value === source)
  return src ? src.label : source
}

const loadSettings = () => {
  if (settings.value?.embedders) {
    embedders.value = { ...settings.value.embedders }
  }
}

const resetForm = () => {
  form.name = ''
  form.source = ''
  form.apiKey = ''
  form.model = ''
  form.url = ''
  form.dimensions = null
  form.documentTemplate = ''
  form.documentTemplateMaxBytes = null
  form.revision = ''
  form.pooling = ''
  form.request = ''
  form.response = ''
  form.binaryQuantized = false
  editingName.value = null
}

const selectSource = (source) => {
  form.source = source
}

const openAddModal = () => {
  resetForm()
  showModal.value = true
}

const editEmbedder = (name, config) => {
  editingName.value = name
  form.name = name
  form.source = config.source || ''
  form.apiKey = config.apiKey || ''
  form.model = config.model || ''
  form.url = config.url || ''
  form.dimensions = config.dimensions || null
  form.documentTemplate = config.documentTemplate || ''
  form.documentTemplateMaxBytes = config.documentTemplateMaxBytes || null
  form.revision = config.revision || ''
  form.pooling = config.pooling || ''
  form.request = config.request ? JSON.stringify(config.request, null, 2) : ''
  form.response = config.response ? JSON.stringify(config.response, null, 2) : ''
  form.binaryQuantized = config.binaryQuantized || false
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  resetForm()
}

const saveEmbedder = async () => {
  if (!isValidForm.value) return
  saving.value = true
  try {
    const config = { source: form.source }
    
    if (form.apiKey) config.apiKey = form.apiKey
    if (form.model) config.model = form.model
    if (form.url) config.url = form.url
    if (form.dimensions) config.dimensions = form.dimensions
    if (form.documentTemplate) config.documentTemplate = form.documentTemplate
    if (form.documentTemplateMaxBytes) config.documentTemplateMaxBytes = form.documentTemplateMaxBytes
    if (form.revision) config.revision = form.revision
    if (form.pooling) config.pooling = form.pooling
    if (form.binaryQuantized) config.binaryQuantized = form.binaryQuantized
    
    // Parse JSON fields for REST embedder
    if (form.source === 'rest') {
      if (form.request) {
        try { config.request = JSON.parse(form.request) } catch (e) { /* ignore */ }
      }
      if (form.response) {
        try { config.response = JSON.parse(form.response) } catch (e) { /* ignore */ }
      }
    }

    const newEmbedders = { ...embedders.value, [form.name]: config }
    
    await indexApi.updateSettings(projectId.value, indexId.value, {
      embedders: newEmbedders
    })
    
    embedders.value = newEmbedders
    closeModal()
  } catch (err) {
    console.error('Failed to save embedder:', err)
    alert('Failed to save embedder: ' + (err.response?.data?.error || err.message))
  } finally {
    saving.value = false
  }
}

const confirmDelete = (name) => {
  deletingName.value = name
  showDeleteModal.value = true
}

const deleteEmbedder = async () => {
  if (!deletingName.value) return
  deleting.value = true
  try {
    const newEmbedders = { ...embedders.value }
    delete newEmbedders[deletingName.value]
    
    await indexApi.updateSettings(projectId.value, indexId.value, {
      embedders: Object.keys(newEmbedders).length > 0 ? newEmbedders : null
    })
    
    embedders.value = newEmbedders
    showDeleteModal.value = false
    deletingName.value = null
  } catch (err) {
    console.error('Failed to delete embedder:', err)
    alert('Failed to delete embedder: ' + (err.response?.data?.error || err.message))
  } finally {
    deleting.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
