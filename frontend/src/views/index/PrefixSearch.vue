<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Prefix Search</h3>
        <p class="text-gray-500 text-sm">Configure how Meilisearch handles prefix matching during search.</p>
      </div>
      <button @click="saveSettings" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save' }}
      </button>
    </div>

    <div class="card p-6 space-y-6">
      <div>
        <h4 class="text-white font-medium mb-4">Prefix Search Mode</h4>
        <div class="space-y-3">
          <label class="flex items-start space-x-3 p-4 bg-dark-800 rounded-lg cursor-pointer hover:bg-dark-700 transition-colors">
            <input
              type="radio"
              v-model="prefixSearch"
              value="indexingTime"
              class="mt-1 text-primary-500"
            />
            <div>
              <span class="text-white font-medium">Indexing Time (Default)</span>
              <p class="text-gray-500 text-sm mt-1">
                Prefix search data is computed during indexing. This uses more storage but provides faster search performance.
              </p>
            </div>
          </label>

          <label class="flex items-start space-x-3 p-4 bg-dark-800 rounded-lg cursor-pointer hover:bg-dark-700 transition-colors">
            <input
              type="radio"
              v-model="prefixSearch"
              value="disabled"
              class="mt-1 text-primary-500"
            />
            <div>
              <span class="text-white font-medium">Disabled</span>
              <p class="text-gray-500 text-sm mt-1">
                Prefix search is disabled. Only exact word matches will be returned. This reduces storage but may affect search relevancy.
              </p>
            </div>
          </label>
        </div>
      </div>

      <div class="bg-dark-800 rounded-lg p-4">
        <h4 class="text-white font-medium mb-2">What is Prefix Search?</h4>
        <p class="text-gray-400 text-sm">
          Prefix search allows matching documents that begin with a specific query term. 
          For example, searching for "hel" would match "hello", "help", "helicopter", etc.
          This is enabled by default and computed during indexing for optimal performance.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, watch } from 'vue'
import { indexApi } from '@/api'

const projectId = inject('projectId')
const indexId = inject('indexId')
const settings = inject('settings')

const prefixSearch = ref('indexingTime')
const saving = ref(false)

const loadSettings = () => {
  if (settings.value?.prefixSearch) {
    prefixSearch.value = settings.value.prefixSearch
  }
}

const saveSettings = async () => {
  saving.value = true
  try {
    await indexApi.updateSettings(projectId.value, indexId.value, {
      prefixSearch: prefixSearch.value
    })
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    saving.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
