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
          <p class="text-gray-500 text-sm">Attributes that can be used for filtering and faceting.</p>
        </div>
        <button @click="saveFilterable" class="btn btn-primary text-sm" :disabled="savingFilterable">
          {{ savingFilterable ? 'Saving...' : 'Save' }}
        </button>
      </div>
      <textarea
        v-model="filterableText"
        class="input font-mono text-sm"
        rows="4"
        placeholder="Enter attributes, one per line"
      ></textarea>
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
import { ref, inject, watch } from 'vue'
import { indexApi } from '@/api'

const projectId = inject('projectId')
const indexId = inject('indexId')
const settings = inject('settings')

const searchableText = ref('')
const displayedText = ref('')
const filterableText = ref('')
const sortableText = ref('')

const savingSearchable = ref(false)
const savingDisplayed = ref(false)
const savingFilterable = ref(false)
const savingSortable = ref(false)

const loadSettings = () => {
  if (settings.value) {
    searchableText.value = arrayToText(settings.value.searchableAttributes)
    displayedText.value = arrayToText(settings.value.displayedAttributes)
    filterableText.value = arrayToText(settings.value.filterableAttributes)
    sortableText.value = arrayToText(settings.value.sortableAttributes)
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

const saveFilterable = async () => {
  savingFilterable.value = true
  try {
    await indexApi.updateFilterableAttributes(projectId.value, indexId.value, textToArray(filterableText.value))
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
