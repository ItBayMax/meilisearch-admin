<template>
  <div class="space-y-6">
    <!-- Searchable Attributes -->
    <div class="card p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="text-lg font-semibold text-white">{{ settingsStore.t('searchableAttributes') }}</h3>
          <p class="text-gray-500 text-sm">{{ settingsStore.t('searchableAttributesDesc') }}</p>
        </div>
        <button @click="saveSearchable" class="btn btn-primary text-sm" :disabled="savingSearchable">
          {{ savingSearchable ? settingsStore.t('saving') : settingsStore.t('save') }}
        </button>
      </div>
      
      <!-- Add new searchable attribute -->
      <div class="mb-4 p-3 bg-dark-800 rounded-lg">
        <h4 class="text-sm font-medium text-gray-300 mb-2">{{ settingsStore.t('addSearchableAttribute') }}</h4>
        <div class="flex gap-2">
          <select 
            v-model="newSearchableName" 
            class="input text-sm flex-1"
            :disabled="availableSearchableAttributes.length === 0"
          >
            <option value="">{{ settingsStore.t('selectAttribute') }}</option>
            <option 
              v-for="attr in availableSearchableAttributes" 
              :key="attr" 
              :value="attr"
            >
              {{ attr }}
            </option>
          </select>
          <button 
            @click="addSearchableAttribute" 
            class="btn btn-primary text-sm"
            :disabled="!newSearchableName"
          >
            {{ settingsStore.t('add') }}
          </button>
        </div>
        <div v-if="availableSearchableAttributes.length === 0" class="text-xs text-yellow-500 mt-2">
          {{ settingsStore.t('noAvailableAttributes') }}
        </div>
      </div>
      
      <!-- Searchable attributes list -->
      <div class="space-y-3">
        <div 
          v-for="(attr, index) in searchableAttributes" 
          :key="index" 
          class="p-3 bg-dark-800 rounded-lg border border-dark-700 flex items-center justify-between"
        >
          <span class="font-medium text-white">{{ attr }}</span>
          <button 
            @click="removeSearchableAttribute(index)" 
            class="text-red-400 hover:text-red-300"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
        
        <div v-if="searchableAttributes.length === 0" class="text-center py-8 text-gray-500">
          {{ settingsStore.t('noSearchableAttributes') }}
        </div>
      </div>
    </div>

    <!-- Displayed Attributes -->
    <div class="card p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="text-lg font-semibold text-white">{{ settingsStore.t('displayedAttributes') }}</h3>
          <p class="text-gray-500 text-sm">{{ settingsStore.t('displayedAttributesDesc') }}</p>
        </div>
        <button @click="saveDisplayed" class="btn btn-primary text-sm" :disabled="savingDisplayed">
          {{ savingDisplayed ? settingsStore.t('saving') : settingsStore.t('save') }}
        </button>
      </div>
      
      <!-- Add new displayed attribute -->
      <div class="mb-4 p-3 bg-dark-800 rounded-lg">
        <h4 class="text-sm font-medium text-gray-300 mb-2">{{ settingsStore.t('addDisplayedAttribute') }}</h4>
        <div class="flex gap-2">
          <select 
            v-model="newDisplayedName" 
            class="input text-sm flex-1"
            :disabled="availableDisplayedAttributes.length === 0"
          >
            <option value="">{{ settingsStore.t('selectAttribute') }}</option>
            <option 
              v-for="attr in availableDisplayedAttributes" 
              :key="attr" 
              :value="attr"
            >
              {{ attr }}
            </option>
          </select>
          <button 
            @click="addDisplayedAttribute" 
            class="btn btn-primary text-sm"
            :disabled="!newDisplayedName"
          >
            {{ settingsStore.t('add') }}
          </button>
        </div>
        <div v-if="availableDisplayedAttributes.length === 0" class="text-xs text-yellow-500 mt-2">
          {{ settingsStore.t('noAvailableAttributes') }}
        </div>
      </div>
      
      <!-- Displayed attributes list -->
      <div class="space-y-3">
        <div 
          v-for="(attr, index) in displayedAttributes" 
          :key="index" 
          class="p-3 bg-dark-800 rounded-lg border border-dark-700 flex items-center justify-between"
        >
          <span class="font-medium text-white">{{ attr }}</span>
          <button 
            @click="removeDisplayedAttribute(index)" 
            class="text-red-400 hover:text-red-300"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
        
        <div v-if="displayedAttributes.length === 0" class="text-center py-8 text-gray-500">
          {{ settingsStore.t('noDisplayedAttributes') }}
        </div>
      </div>
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
            :disabled="availableFilterAttributes.length === 0"
          >
            <option value="">{{ settingsStore.t('selectAttribute') }}</option>
            <option 
              v-for="attr in availableFilterAttributes" 
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
        <div v-if="availableFilterAttributes.length === 0" class="text-xs text-yellow-500 mt-2">
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
          <h3 class="text-lg font-semibold text-white">{{ settingsStore.t('sortableAttributes') }}</h3>
          <p class="text-gray-500 text-sm">{{ settingsStore.t('sortableAttributesDesc') }}</p>
        </div>
        <button @click="saveSortable" class="btn btn-primary text-sm" :disabled="savingSortable">
          {{ savingSortable ? settingsStore.t('saving') : settingsStore.t('save') }}
        </button>
      </div>
      
      <!-- Add new sortable attribute -->
      <div class="mb-4 p-3 bg-dark-800 rounded-lg">
        <h4 class="text-sm font-medium text-gray-300 mb-2">{{ settingsStore.t('addSortableAttribute') }}</h4>
        <div class="flex gap-2">
          <select 
            v-model="newSortName" 
            class="input text-sm flex-1"
            :disabled="availableSortAttributes.length === 0"
          >
            <option value="">{{ settingsStore.t('selectAttribute') }}</option>
            <option 
              v-for="attr in availableSortAttributes" 
              :key="attr" 
              :value="attr"
            >
              {{ attr }}
            </option>
          </select>
          <button 
            @click="addSortAttribute" 
            class="btn btn-primary text-sm"
            :disabled="!newSortName"
          >
            {{ settingsStore.t('add') }}
          </button>
        </div>
        <div v-if="availableSortAttributes.length === 0" class="text-xs text-yellow-500 mt-2">
          {{ settingsStore.t('noAvailableAttributes') }}
        </div>
      </div>
      
      <!-- Sortable attributes list -->
      <div class="space-y-3">
        <div 
          v-for="(attr, index) in sortAttributes" 
          :key="index" 
          class="p-3 bg-dark-800 rounded-lg border border-dark-700 flex items-center justify-between"
        >
          <span class="font-medium text-white">{{ attr }}</span>
          <button 
            @click="removeSortAttribute(index)" 
            class="text-red-400 hover:text-red-300"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
        
        <div v-if="sortAttributes.length === 0" class="text-center py-8 text-gray-500">
          {{ settingsStore.t('noSortAttributes') }}
        </div>
      </div>
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

// Searchable attributes
const searchableAttributes = ref([])
const newSearchableName = ref('')

// Displayed attributes
const displayedAttributes = ref([])
const newDisplayedName = ref('')

// Sortable attributes
const sortAttributes = ref([])
const newSortName = ref('')

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
const availableSearchableAttributes = computed(() => {
  return documentFields.value
    .filter(attr => !searchableAttributes.value.includes(attr))
})

const availableDisplayedAttributes = computed(() => {
  return documentFields.value
    .filter(attr => !displayedAttributes.value.includes(attr))
})

const availableSortAttributes = computed(() => {
  return documentFields.value
    .filter(attr => !sortAttributes.value.includes(attr))
})

const availableFilterAttributes = computed(() => {
  return documentFields.value
    .filter(attr => !filterableAttributes.value.some(fa => fa.name === attr))
})

const loadSettings = () => {
  if (settings.value) {
    // Load searchable attributes
    searchableAttributes.value = settings.value.searchableAttributes || []
    
    // Load displayed attributes
    displayedAttributes.value = settings.value.displayedAttributes || []
    
    // Load filterable attributes with mode information
    if (settings.value.filterableAttributes) {
      filterableAttributes.value = settings.value.filterableAttributes.map(attr => {
        if (typeof attr === 'string') {
          return { name: attr, mode: 'equality' } // default mode
        }
        return attr
      })
    }
    
    // Load sortable attributes
    sortAttributes.value = settings.value.sortableAttributes || []
    
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



const saveSearchable = async () => {
  savingSearchable.value = true
  try {
    await indexApi.updateSearchableAttributes(projectId.value, indexId.value, searchableAttributes.value)
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    savingSearchable.value = false
  }
}

const saveDisplayed = async () => {
  savingDisplayed.value = true
  try {
    await indexApi.updateDisplayedAttributes(projectId.value, indexId.value, displayedAttributes.value)
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    savingDisplayed.value = false
  }
}

const addSearchableAttribute = () => {
  if (!newSearchableName.value) return
  
  const existing = searchableAttributes.value.includes(newSearchableName.value)
  if (existing) {
    alert(settingsStore.t('attributeAlreadyExists'))
    return
  }
  
  searchableAttributes.value.push(newSearchableName.value)
  newSearchableName.value = ''
}

const addDisplayedAttribute = () => {
  if (!newDisplayedName.value) return
  
  const existing = displayedAttributes.value.includes(newDisplayedName.value)
  if (existing) {
    alert(settingsStore.t('attributeAlreadyExists'))
    return
  }
  
  displayedAttributes.value.push(newDisplayedName.value)
  newDisplayedName.value = ''
}

const addSortAttribute = () => {
  if (!newSortName.value) return
  
  const existing = sortAttributes.value.includes(newSortName.value)
  if (existing) {
    alert(settingsStore.t('attributeAlreadyExists'))
    return
  }
  
  sortAttributes.value.push(newSortName.value)
  newSortName.value = ''
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

const removeSearchableAttribute = (index) => {
  searchableAttributes.value.splice(index, 1)
}

const removeDisplayedAttribute = (index) => {
  displayedAttributes.value.splice(index, 1)
}

const removeSortAttribute = (index) => {
  sortAttributes.value.splice(index, 1)
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
    await indexApi.updateSortableAttributes(projectId.value, indexId.value, sortAttributes.value)
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    savingSortable.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
