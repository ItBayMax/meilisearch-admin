<template>
  <div class="space-y-6">
    <!-- Searchable Attributes -->
    <div class="card p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="text-lg font-semibold text-white">Searchable Attributes</h3>
          <p class="text-gray-500 text-sm">Attributes that can be searched. Order determines relevancy impact.</p>
        </div>
        <button @click="saveSearchable" class="btn btn-primary text-sm" :disabled="savingSearchable">
          {{ savingSearchable ? 'Saving...' : 'Save' }}
        </button>
      </div>
      <textarea
        v-model="searchableText"
        class="input font-mono text-sm"
        rows="4"
        placeholder="Enter attributes, one per line or ['*'] for all"
      ></textarea>
    </div>

    <!-- Displayed Attributes -->
    <div class="card p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="text-lg font-semibold text-white">Displayed Attributes</h3>
          <p class="text-gray-500 text-sm">Attributes returned in search results.</p>
        </div>
        <button @click="saveDisplayed" class="btn btn-primary text-sm" :disabled="savingDisplayed">
          {{ savingDisplayed ? 'Saving...' : 'Save' }}
        </button>
      </div>
      <textarea
        v-model="displayedText"
        class="input font-mono text-sm"
        rows="4"
        placeholder="Enter attributes, one per line or ['*'] for all"
      ></textarea>
    </div>

    <!-- Filterable Attributes -->
    <div class="card p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="text-lg font-semibold text-white">Filterable Attributes</h3>
          <p class="text-gray-500 text-sm">Configure attributes that can be used for filtering and faceting.</p>
        </div>
        <button @click="saveFilterable" class="btn btn-primary text-sm" :disabled="savingFilterable">
          {{ savingFilterable ? settingsStore.t('saving') : settingsStore.t('save') }}
        </button>
      </div>
      
      <!-- Add new filter attribute -->
      <div class="mb-4 p-3 bg-dark-800 rounded-lg">
        <h4 class="text-sm font-medium text-gray-300 mb-2">{{ settingsStore.t('addFilterAttribute') }}</h4>
        <div class="flex gap-2">
          <select 
            v-model="newAttributeName" 
            class="input text-sm flex-1"
            :disabled="availableAttributes.length === 0"
          >
            <option value="">{{ settingsStore.t('selectAttribute') }}</option>
            <option 
              v-for="attr in availableAttributes" 
              :key="attr" 
              :value="attr"
            >
              {{ attr }}
            </option>
          </select>
          <select v-model="newFilterMode" class="input text-sm w-32">
            <option value="equality">{{ settingsStore.t('equality') }}</option>
            <option value="comparison">{{ settingsStore.t('comparison') }}</option>
          </select>
          <button 
            @click="addFilterAttribute" 
            class="btn btn-primary text-sm"
            :disabled="!newAttributeName"
          >
            {{ settingsStore.t('add') }}
          </button>
        </div>
        <div v-if="availableAttributes.length === 0" class="text-xs text-yellow-500 mt-2">
          {{ settingsStore.t('noAvailableAttributes') }}
        </div>
      </div>
      
      <!-- Filter attributes list -->
      <div class="space-y-3">
        <div 
          v-for="(attr, index) in filterableAttributes" 
          :key="index" 
          class="p-3 bg-dark-800 rounded-lg border border-dark-700"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-3">
              <span class="font-medium text-white">{{ attr.name }}</span>
              <span class="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded">
                {{ attr.mode === 'equality' ? settingsStore.t('equality') : settingsStore.t('comparison') }}
              </span>
            </div>
            <button 
              @click="removeFilterAttribute(index)" 
              class="text-red-400 hover:text-red-300"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
          
          <!-- Supported operators -->
          <div class="text-xs text-gray-400">
            <span class="font-medium">{{ settingsStore.t('supportedOperators') }}:</span>
            <span v-if="attr.mode === 'equality'"> =, !=, IN, AND, OR, NOT, EXISTS, IS EMPTY, IS NULL</span>
            <span v-else>>, <, >=, <=, AND, OR, NOT, EXISTS, IS EMPTY, IS NULL</span>
          </div>
        </div>
        
        <div v-if="filterableAttributes.length === 0" class="text-center py-8 text-gray-500">
          {{ settingsStore.t('noFilterAttributes') }}
        </div>
      </div>
    </div>

    <!-- Sortable Attributes -->
    <div class="card p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="text-lg font-semibold text-white">Sortable Attributes</h3>
          <p class="text-gray-500 text-sm">Attributes that can be used for sorting search results.</p>
        </div>
        <button @click="saveSortable" class="btn btn-primary text-sm" :disabled="savingSortable">
          {{ savingSortable ? 'Saving...' : 'Save' }}
        </button>
      </div>
      <textarea
        v-model="sortableText"
        class="input font-mono text-sm"
        rows="4"
        placeholder="Enter attributes, one per line"
      ></textarea>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, watch } from 'vue'
import { useSettingsStore } from '@/store/settings'
import { indexApi } from '@/api'

const settingsStore = useSettingsStore()
const projectId = inject('projectId')
const indexId = inject('indexId')
const settings = inject('settings')

const searchableText = ref('')
const displayedText = ref('')
const sortableText = ref('')

const savingSearchable = ref(false)
const savingDisplayed = ref(false)
const savingFilterable = ref(false)
const savingSortable = ref(false)

// Filterable attributes with mode
const filterableAttributes = ref([])
const newAttributeName = ref('')
const newFilterMode = ref('equality')

// Document fields extracted from index documents
const documentFields = ref([])

// Available attributes for selection (from actual document fields)
const availableAttributes = computed(() => {
  return documentFields.value
    .filter(attr => !filterableAttributes.value.some(fa => fa.name === attr))
})

const loadSettings = () => {
  if (settings.value) {
    searchableText.value = arrayToText(settings.value.searchableAttributes)
    displayedText.value = arrayToText(settings.value.displayedAttributes)
    // Load filterable attributes with mode information
    if (settings.value.filterableAttributes) {
      filterableAttributes.value = settings.value.filterableAttributes.map(attr => {
        if (typeof attr === 'string') {
          return { name: attr, mode: 'equality' } // default mode
        }
        return attr
      })
    }
    sortableText.value = arrayToText(settings.value.sortableAttributes)
    
    // Extract document fields from sample documents
    extractDocumentFields()
  }
}

const extractDocumentFields = async () => {
  try {
    // Get a sample of documents to extract field names
    const result = await indexApi.search(projectId.value, indexId.value, '', { limit: 1 })
    if (result.data?.hits?.length > 0) {
      const sampleDoc = result.data.hits[0]
      // Extract all non-private fields (not starting with _)
      const fields = Object.keys(sampleDoc)
        .filter(key => !key.startsWith('_'))
        .sort()
      documentFields.value = fields
    } else {
      // If no documents, fall back to common field names
      documentFields.value = ['id', 'title', 'content', 'name', 'description']
    }
  } catch (err) {
    console.warn('Failed to extract document fields:', err)
    // Fallback to common field names
    documentFields.value = ['id', 'title', 'content', 'name', 'description']
  }
}

const arrayToText = (arr) => {
  if (!arr) return ''
  if (arr.length === 1 && arr[0] === '*') return '*'
  return arr.join('\n')
}

const textToArray = (text) => {
  if (!text.trim()) return []
  if (text.trim() === '*') return ['*']
  return text.split('\n').map(s => s.trim()).filter(Boolean)
}

const saveSearchable = async () => {
  savingSearchable.value = true
  try {
    await indexApi.updateSearchableAttributes(projectId.value, indexId.value, textToArray(searchableText.value))
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    savingSearchable.value = false
  }
}

const saveDisplayed = async () => {
  savingDisplayed.value = true
  try {
    await indexApi.updateDisplayedAttributes(projectId.value, indexId.value, textToArray(displayedText.value))
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    savingDisplayed.value = false
  }
}

const addFilterAttribute = () => {
  if (!newAttributeName.value) return
  
  const existing = filterableAttributes.value.find(attr => attr.name === newAttributeName.value)
  if (existing) {
    alert(settingsStore.t('attributeAlreadyExists'))
    return
  }
  
  filterableAttributes.value.push({
    name: newAttributeName.value,
    mode: newFilterMode.value
  })
  
  newAttributeName.value = ''
  newFilterMode.value = 'equality'
}

const removeFilterAttribute = (index) => {
  filterableAttributes.value.splice(index, 1)
}

const saveFilterable = async () => {
  savingFilterable.value = true
  try {
    // Save as array of attribute names (keeping compatibility)
    const attributeNames = filterableAttributes.value.map(attr => attr.name)
    await indexApi.updateFilterableAttributes(projectId.value, indexId.value, attributeNames)
    
    // Also save the extended configuration somewhere if needed
    // This could be saved to a separate endpoint or stored locally
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    savingFilterable.value = false
  }
}

const saveSortable = async () => {
  savingSortable.value = true
  try {
    await indexApi.updateSortableAttributes(projectId.value, indexId.value, textToArray(sortableText.value))
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    savingSortable.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
