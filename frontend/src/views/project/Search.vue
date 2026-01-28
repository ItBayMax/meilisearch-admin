<template>
  <div class="space-y-4 h-full flex flex-col">
    <!-- Search Bar -->
    <div class="flex items-center space-x-4">
      <div class="flex-1 relative">
        <svg class="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          class="input pl-12"
          :placeholder="settingsStore.t('searchDocuments')"
          @keyup.enter="performSearch"
        />
      </div>
      <button @click="performSearch" class="btn btn-primary" :disabled="loading">
        {{ loading ? settingsStore.t('searching') : settingsStore.t('search') }}
      </button>
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap items-center gap-3">
      <!-- Index Select -->
      <div>
        <select v-model="selectedIndex" class="input py-1.5 text-sm" @change="onIndexChange">
          <option value="">{{ settingsStore.t('selectIndex') }}</option>
          <option v-for="idx in indexes" :key="idx.uid" :value="idx.uid">
            {{ idx.uid }}
          </option>
        </select>
      </div>

      <!-- Sort -->
      <div v-if="sortableAttributes.length">
        <select v-model="sortBy" class="input py-1.5 text-sm">
          <option value="">{{ settingsStore.t('sortBy') }}</option>
          <option v-for="attr in sortableAttributes" :key="attr" :value="attr + ':asc'">
            {{ attr }} (ASC)
          </option>
          <option v-for="attr in sortableAttributes" :key="attr + '-desc'" :value="attr + ':desc'">
            {{ attr }} (DESC)
          </option>
        </select>
      </div>

      <!-- Column Selector -->
      <div v-if="allColumns.length" class="relative" @click.stop>
        <button
          @click="showColumnSelector = !showColumnSelector"
          class="btn btn-secondary py-1.5 text-sm flex items-center space-x-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
          </svg>
          <span>{{ settingsStore.t('columns') }}</span>
        </button>
        <div
          v-if="showColumnSelector"
          class="absolute left-0 top-full mt-1 bg-dark-800 rounded-lg shadow-lg border border-dark-600 py-2 z-50 min-w-[200px] max-h-[300px] overflow-y-auto"
        >
          <label
            v-for="col in allColumns"
            :key="col"
            class="flex items-center px-4 py-1.5 hover:bg-dark-700 cursor-pointer"
          >
            <input type="checkbox" :value="col" v-model="selectedColumns" class="mr-2" />
            <span class="text-sm text-gray-300">{{ col }}</span>
          </label>
        </div>
      </div>

      <!-- View Mode -->
      <div class="flex items-center space-x-1 ml-auto">
        <button
          @click="viewMode = 'table'"
          :class="['btn btn-ghost p-2', viewMode === 'table' ? 'text-primary-400' : 'text-gray-400']"
          :title="settingsStore.t('tableView')"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
          </svg>
        </button>
        <button
          @click="viewMode = 'json'"
          :class="['btn btn-ghost p-2', viewMode === 'json' ? 'text-primary-400' : 'text-gray-400']"
          :title="settingsStore.t('jsonView')"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
        </button>
        <button
          @click="showRankingScore = !showRankingScore"
          :class="['btn btn-ghost p-2', showRankingScore ? 'text-primary-400' : 'text-gray-400']"
          :title="settingsStore.t('rankingScore')"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Filters Panel -->
    <div v-if="filterableAttributes.length" class="card p-3">
      <h4 class="text-sm font-medium text-gray-400 mb-2">{{ settingsStore.t('filters') }}</h4>
      <div class="flex flex-wrap gap-2">
        <div v-for="attr in filterableAttributes" :key="attr">
          <input
            v-model="filters[attr]"
            type="text"
            class="input text-sm py-1 px-2"
            :placeholder="attr"
            style="width: 140px;"
            @keyup.enter="performSearch"
          />
        </div>
      </div>
    </div>

    <!-- Loading -->
    <Loading v-if="loading" />

    <!-- Results -->
    <template v-else-if="results">
      <div class="flex items-center justify-between text-sm text-gray-400">
        <span>{{ results.estimatedTotalHits || results.hits?.length || 0 }} results ({{ results.processingTimeMs }}ms)</span>
      </div>

      <!-- Table View -->
      <div v-if="viewMode === 'table'" class="card flex-1 overflow-hidden flex flex-col min-h-0">
        <div class="overflow-auto flex-1">
          <table class="w-full">
            <thead class="bg-dark-800 sticky top-0 z-10">
              <tr>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase w-24">{{ settingsStore.t('actions') }}</th>
                <th v-if="showRankingScore" class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase w-20">{{ settingsStore.t('score') }}</th>
                <th
                  v-for="col in visibleColumns"
                  :key="col"
                  class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase whitespace-nowrap"
                >
                  {{ col }}
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-dark-700">
              <tr
                v-for="(hit, index) in results.hits"
                :key="index"
                class="hover:bg-dark-800/50"
              >
                <td class="px-3 py-2">
                  <div class="flex items-center space-x-1">
                    <button @click="copyJson(hit)" class="p-1 text-gray-400 hover:text-white" :title="settingsStore.t('copyJson')">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                    </button>
                    <button @click="editDocument(hit)" class="p-1 text-gray-400 hover:text-white" :title="settingsStore.t('edit')">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button @click="confirmDeleteDocument(hit)" class="p-1 text-gray-400 hover:text-red-400" :title="settingsStore.t('delete')">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
                <td v-if="showRankingScore" class="px-3 py-2 text-xs text-primary-400 font-mono">
                  {{ hit._rankingScore ? hit._rankingScore.toFixed(4) : '-' }}
                </td>
                <td
                  v-for="col in visibleColumns"
                  :key="col"
                  class="px-3 py-2 text-sm text-gray-300 max-w-[200px]"
                >
                  <CellValue :value="hit[col]" :cellKey="`${index}-${col}`" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- JSON View -->
      <div v-else class="space-y-3 flex-1 overflow-auto">
        <div
          v-for="(hit, index) in results.hits"
          :key="index"
          class="card p-4"
        >
          <div class="flex items-center justify-between mb-2">
            <span v-if="showRankingScore && hit._rankingScore" class="text-xs text-primary-400 font-mono">
              Score: {{ hit._rankingScore.toFixed(4) }}
            </span>
            <div class="flex items-center space-x-2">
              <button @click="copyJson(hit)" class="p-1 text-gray-400 hover:text-white" :title="settingsStore.t('copyJson')">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </button>
              <button @click="editDocument(hit)" class="p-1 text-gray-400 hover:text-white" :title="settingsStore.t('edit')">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button @click="confirmDeleteDocument(hit)" class="p-1 text-gray-400 hover:text-red-400" :title="settingsStore.t('delete')">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
          <pre class="text-gray-300 text-sm overflow-x-auto">{{ JSON.stringify(cleanHit(hit), null, 2) }}</pre>
        </div>
      </div>

      <Empty v-if="results.hits?.length === 0" :title="settingsStore.t('noResults')" :description="settingsStore.t('noResults')" />
    </template>

    <Empty v-else :title="settingsStore.t('selectAnIndex')" :description="settingsStore.t('selectAnIndexDesc')" />

    <!-- Edit Document Modal -->
    <Modal v-model:visible="showEditModal" :title="settingsStore.t('editDocument')" size="lg">
      <div class="space-y-4">
        <textarea
          v-model="editJson"
          class="input font-mono text-sm"
          rows="15"
        ></textarea>
      </div>
      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showEditModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="saveDocument" class="btn btn-primary" :disabled="saving">
            {{ saving ? settingsStore.t('saving') : settingsStore.t('save') }}
          </button>
        </div>
      </template>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal v-model:visible="showDeleteModal" :title="settingsStore.t('deleteDocument')" size="sm">
      <p class="text-gray-300">{{ settingsStore.t('deleteConfirm') }}? {{ settingsStore.t('cannotUndo') }}</p>
      <template #footer>
        <div class="flex justify-end space-x-3">
          <button @click="showDeleteModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
          <button @click="deleteDocument" class="btn btn-danger" :disabled="deleting">
            {{ deleting ? settingsStore.t('deleting') : settingsStore.t('delete') }}
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSettingsStore } from '@/store/settings'
import { indexApi } from '@/api'
import Loading from '@/components/common/Loading.vue'
import Empty from '@/components/common/Empty.vue'
import Modal from '@/components/common/Modal.vue'
import CellValue from '@/components/common/CellValue.vue'

const route = useRoute()
const settingsStore = useSettingsStore()
const projectId = inject('projectId')

const indexes = ref([])
const selectedIndex = ref('')
const searchQuery = ref('')
const results = ref(null)
const loading = ref(false)
const viewMode = ref('table')
const sortBy = ref('')
const showRankingScore = ref(false)
const showColumnSelector = ref(false)
const currentSettings = ref(null)

const sortableAttributes = ref([])
const filterableAttributes = ref([])
const displayedAttributes = ref([])
const filters = reactive({})

const allColumns = ref([])
const selectedColumns = ref([])

const showEditModal = ref(false)
const showDeleteModal = ref(false)
const editJson = ref('')
const editingDocument = ref(null)
const documentToDelete = ref(null)
const saving = ref(false)
const deleting = ref(false)

const visibleColumns = computed(() => {
  if (selectedColumns.value.length > 0) {
    return selectedColumns.value
  }
  return allColumns.value.slice(0, 6)
})

const fetchIndexes = async () => {
  try {
    const result = await indexApi.getAll(projectId.value)
    indexes.value = result.data || []
    
    if (route.query.index) {
      selectedIndex.value = route.query.index
      onIndexChange()
    }
  } catch (err) {
    console.error('Failed to fetch indexes:', err)
  }
}

const onIndexChange = async () => {
  if (!selectedIndex.value) {
    sortableAttributes.value = []
    filterableAttributes.value = []
    displayedAttributes.value = []
    results.value = null
    allColumns.value = []
    selectedColumns.value = []
    return
  }

  // Reset columns when switching index
  allColumns.value = []
  selectedColumns.value = []

  try {
    const settings = await indexApi.getSettings(projectId.value, selectedIndex.value)
    if (settings.success && settings.data) {
      currentSettings.value = settings.data
      sortableAttributes.value = settings.data.sortableAttributes || []
      const fa = settings.data.filterableAttributes || []
      filterableAttributes.value = fa.map(item => {
        if (typeof item === 'string') return item
        if (item.attributePatterns) return item.attributePatterns[0]
        return item
      }).filter(Boolean)
      displayedAttributes.value = settings.data.displayedAttributes || ['*']
    }
    performSearch()
  } catch (err) {
    console.error('Failed to fetch settings:', err)
  }
}

const performSearch = async () => {
  if (!selectedIndex.value) return
  loading.value = true
  try {
    const params = { limit: 20, showRankingScore: true }
    
    if (sortBy.value) {
      params.sort = [sortBy.value]
    }

    const filterParts = []
    for (const [key, value] of Object.entries(filters)) {
      if (value) {
        filterParts.push(`${key} = "${value}"`)
      }
    }
    if (filterParts.length) {
      params.filter = filterParts.join(' AND ')
    }

    const result = await indexApi.search(projectId.value, selectedIndex.value, searchQuery.value, params)
    results.value = result.data
    
    if (result.data?.hits?.length > 0) {
      const newColumns = Object.keys(result.data.hits[0]).filter(k => !k.startsWith('_'))
      allColumns.value = newColumns
      // Only auto-select columns if none are currently selected
      if (selectedColumns.value.length === 0) {
        selectedColumns.value = newColumns.slice(0, 6)
      } else {
        // Filter out columns that no longer exist in the new data
        selectedColumns.value = selectedColumns.value.filter(col => newColumns.includes(col))
        // If all previously selected columns were removed, select first 6
        if (selectedColumns.value.length === 0) {
          selectedColumns.value = newColumns.slice(0, 6)
        }
      }
    }
  } catch (err) {
    console.error('Search failed:', err)
  } finally {
    loading.value = false
  }
}

const cleanHit = (hit) => {
  const clean = { ...hit }
  delete clean._rankingScore
  delete clean._rankingScoreDetails
  return clean
}

const copyJson = async (hit) => {
  try {
    await navigator.clipboard.writeText(JSON.stringify(cleanHit(hit), null, 2))
  } catch (err) {
    console.error('Copy failed:', err)
  }
}

const editDocument = (hit) => {
  editingDocument.value = hit
  editJson.value = JSON.stringify(cleanHit(hit), null, 2)
  showEditModal.value = true
}

const saveDocument = async () => {
  saving.value = true
  try {
    const doc = JSON.parse(editJson.value)
    await indexApi.addDocuments(projectId.value, selectedIndex.value, [doc])
    showEditModal.value = false
    performSearch()
  } catch (err) {
    console.error('Save failed:', err)
    alert('Invalid JSON or save failed')
  } finally {
    saving.value = false
  }
}

const confirmDeleteDocument = (hit) => {
  documentToDelete.value = hit
  showDeleteModal.value = true
}

const deleteDocument = async () => {
  if (!documentToDelete.value) return
  deleting.value = true
  try {
    const primaryKey = currentSettings.value?.primaryKey || 'id'
    const docId = documentToDelete.value[primaryKey]
    if (docId) {
      await indexApi.deleteDocument(projectId.value, selectedIndex.value, docId)
      showDeleteModal.value = false
      performSearch()
    }
  } catch (err) {
    console.error('Delete failed:', err)
  } finally {
    deleting.value = false
  }
}

const closeColumnSelector = () => {
  showColumnSelector.value = false
}

watch(sortBy, () => {
  if (selectedIndex.value) performSearch()
})

onMounted(() => {
  fetchIndexes()
  document.addEventListener('click', closeColumnSelector)
})

onUnmounted(() => {
  document.removeEventListener('click', closeColumnSelector)
})
</script>
