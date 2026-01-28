<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Embedders</h3>
        <p class="text-gray-500 text-sm">Configure vector embedders for AI-powered search.</p>
      </div>
      <button @click="openAddModal" class="btn btn-primary text-sm">
        Add Embedder
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
        <h4 class="text-white font-medium mb-2">No Embedders Configured</h4>
        <p class="text-gray-500 text-sm max-w-md mx-auto">
          Embedders generate vector data from your documents for AI-powered semantic search.
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
            <button @click="editEmbedder(name, config)" class="btn btn-ghost text-sm">Edit</button>
            <button @click="confirmDelete(name)" class="btn btn-ghost text-red-400 text-sm">Delete</button>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
          <div v-if="config.model">
            <span class="text-gray-500">Model:</span>
            <span class="text-gray-300 ml-2">{{ config.model }}</span>
          </div>
          <div v-if="config.dimensions">
            <span class="text-gray-500">Dimensions:</span>
            <span class="text-gray-300 ml-2">{{ config.dimensions }}</span>
          </div>
          <div v-if="config.url">
            <span class="text-gray-500">URL:</span>
            <span class="text-gray-300 ml-2 truncate">{{ config.url }}</span>
          </div>
          <div v-if="config.revision">
            <span class="text-gray-500">Revision:</span>
            <span class="text-gray-300 ml-2">{{ config.revision }}</span>
          </div>
          <div v-if="config.documentTemplate" class="col-span-2">
            <span class="text-gray-500">Template:</span>
            <span class="text-gray-300 ml-2 truncate block">{{ config.documentTemplate }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <Modal v-model:visible="showModal" :title="editingName ? 'Edit Embedder' : 'Add Embedder'" size="lg">
      <form @submit.prevent="saveEmbedder" class="space-y-4">
        <!-- Embedder Name -->
        <div>
          <label class="label">Embedder Name *</label>
          <input
            v-model="form.name"
            type="text"
            class="input"
            placeholder="default"
            :disabled="!!editingName"
            required
          />
          <p class="text-gray-500 text-xs mt-1">Unique identifier for this embedder</p>
        </div>

        <!-- Source Selection -->
        <div>
          <label class="label">Source *</label>
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
            <label class="label">API Key</label>
            <input v-model="form.apiKey" type="password" class="input" placeholder="sk-..." />
            <p class="text-gray-500 text-xs mt-1">Leave empty to use OPENAI_API_KEY environment variable</p>
          </div>
          <div>
            <label class="label">Model</label>
            <select v-model="form.model" class="input">
              <option value="">Default (text-embedding-3-small)</option>
              <option value="text-embedding-3-small">text-embedding-3-small</option>
              <option value="text-embedding-3-large">text-embedding-3-large</option>
              <option value="text-embedding-ada-002">text-embedding-ada-002</option>
            </select>
          </div>
          <div>
            <label class="label">URL (Optional)</label>
            <input v-model="form.url" type="url" class="input" placeholder="https://api.openai.com/v1/embeddings" />
            <p class="text-gray-500 text-xs mt-1">Use for proxies or custom OpenAI-compatible endpoints</p>
          </div>
        </template>

        <!-- Hugging Face Settings -->
        <template v-if="form.source === 'huggingFace'">
          <div>
            <label class="label">Model</label>
            <input v-model="form.model" type="text" class="input" placeholder="BAAI/bge-base-en-v1.5" />
            <p class="text-gray-500 text-xs mt-1">Default: BAAI/bge-base-en-v1.5</p>
          </div>
          <div>
            <label class="label">Revision</label>
            <input v-model="form.revision" type="text" class="input" placeholder="Model revision hash" />
          </div>
          <div>
            <label class="label">Pooling</label>
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
            <label class="label">URL *</label>
            <input v-model="form.url" type="url" class="input" placeholder="http://localhost:11434/api/embeddings" required />
          </div>
          <div>
            <label class="label">Model *</label>
            <input v-model="form.model" type="text" class="input" placeholder="nomic-embed-text" required />
          </div>
          <div>
            <label class="label">API Key (Optional)</label>
            <input v-model="form.apiKey" type="password" class="input" placeholder="If authentication required" />
          </div>
        </template>

        <!-- REST API Settings -->
        <template v-if="form.source === 'rest'">
          <div>
            <label class="label">URL *</label>
            <input v-model="form.url" type="url" class="input" placeholder="https://api.example.com/embed" required />
          </div>
          <div>
            <label class="label">API Key</label>
            <input v-model="form.apiKey" type="password" class="input" placeholder="Bearer token or API key" />
          </div>
          <div>
            <label class="label">Request Template (JSON)</label>
            <textarea v-model="form.request" class="input font-mono text-sm" rows="4" placeholder='{"input": "{{text}}", "model": "text-embedding-3-small"}'></textarea>
            <p class="text-gray-500 text-xs mt-1">JSON template for the request body. Use {"{{text}}"} placeholder.</p>
          </div>
          <div>
            <label class="label">Response Path (JSON)</label>
            <textarea v-model="form.response" class="input font-mono text-sm" rows="3" placeholder='{"embeddings": "{{embedding}}"}'></textarea>
            <p class="text-gray-500 text-xs mt-1">JSON template to extract embeddings from response.</p>
          </div>
        </template>

        <!-- User Provided Settings -->
        <template v-if="form.source === 'userProvided'">
          <div class="p-4 bg-dark-800 rounded-lg">
            <p class="text-gray-400 text-sm">
              With user-provided embeddings, you must include vector data in your documents' <code class="text-primary-400">_vectors</code> field and generate vectors for search queries manually.
            </p>
          </div>
        </template>

        <!-- Common Settings -->
        <div v-if="form.source" class="border-t border-dark-700 pt-4 space-y-4">
          <h4 class="text-white font-medium">Common Settings</h4>
          
          <div>
            <label class="label">Dimensions</label>
            <input v-model.number="form.dimensions" type="number" class="input" placeholder="Auto-detected if not specified" />
            <p class="text-gray-500 text-xs mt-1">Number of dimensions in the embedding vectors</p>
          </div>

          <div v-if="form.source !== 'userProvided'">
            <label class="label">Document Template</label>
            <textarea
              v-model="form.documentTemplate"
              class="input font-mono text-sm"
              rows="3"
              placeholder="A document titled '{{doc.title}}' with content: {{doc.content}}"
            ></textarea>
            <p class="text-gray-500 text-xs mt-1">
              Liquid template defining data sent to embedder. Use <code class="text-primary-400">{"{{doc.field}}"}</code> to reference fields.
            </p>
          </div>

          <div v-if="form.source !== 'userProvided'">
            <label class="label">Document Template Max Bytes</label>
            <input v-model.number="form.documentTemplateMaxBytes" type="number" class="input" placeholder="400" />
          </div>

          <div class="flex items-center space-x-2">
            <input type="checkbox" v-model="form.binaryQuantized" id="binaryQuantized" class="rounded" />
            <label for="binaryQuantized" class="text-gray-300 text-sm">Binary Quantized (irreversible)</label>
          </div>
        </div>
      </form>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="closeModal" class="btn btn-secondary">Cancel</button>
          <button @click="saveEmbedder" class="btn btn-primary" :disabled="!isValidForm || saving">
            {{ saving ? 'Saving...' : (editingName ? 'Update' : 'Add') }}
          </button>
        </div>
      </template>
    </Modal>

    <!-- Delete Confirmation -->
    <Modal v-model:visible="showDeleteModal" title="Delete Embedder" size="sm">
      <p class="text-gray-300">
        Are you sure you want to delete embedder "<span class="text-white font-medium">{{ deletingName }}</span>"? 
        This may trigger reindexing of all documents.
      </p>
      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showDeleteModal = false" class="btn btn-secondary">Cancel</button>
          <button @click="deleteEmbedder" class="btn btn-danger" :disabled="deleting">
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject, watch } from 'vue'
import { indexApi } from '@/api'
import Modal from '@/components/common/Modal.vue'

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
