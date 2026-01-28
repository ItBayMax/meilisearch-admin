<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Search Cutoff</h3>
        <p class="text-gray-500 text-sm">Configure the maximum duration of a search query.</p>
      </div>
      <button @click="saveSettings" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save' }}
      </button>
    </div>

    <div class="card p-6 space-y-6">
      <div>
        <label class="label">Search Cutoff (milliseconds)</label>
        <input
          v-model.number="searchCutoffMs"
          type="number"
          class="input"
          min="1"
          max="60000"
          placeholder="1500"
        />
        <p class="text-gray-500 text-xs mt-2">
          Meilisearch will interrupt any search taking longer than this value. Default is 1500ms.
        </p>
      </div>

      <div class="bg-dark-800 rounded-lg p-4">
        <h4 class="text-white font-medium mb-2">Recommended Values</h4>
        <ul class="text-gray-400 text-sm space-y-1">
          <li><code class="text-primary-400">1500</code> - Default, suitable for most use cases</li>
          <li><code class="text-primary-400">500-1000</code> - For real-time search with strict latency requirements</li>
          <li><code class="text-primary-400">3000-5000</code> - For complex queries on large datasets</li>
          <li><code class="text-primary-400">null</code> - Disable cutoff (not recommended for production)</li>
        </ul>
      </div>

      <div class="flex items-center space-x-2">
        <input
          type="checkbox"
          v-model="disableCutoff"
          id="disable-cutoff"
          class="text-primary-500"
        />
        <label for="disable-cutoff" class="text-gray-300 text-sm">
          Disable search cutoff (searches will run until completion)
        </label>
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

const searchCutoffMs = ref(1500)
const disableCutoff = ref(false)
const saving = ref(false)

const loadSettings = () => {
  if (settings.value?.searchCutoffMs !== undefined) {
    if (settings.value.searchCutoffMs === null) {
      disableCutoff.value = true
      searchCutoffMs.value = 1500
    } else {
      disableCutoff.value = false
      searchCutoffMs.value = settings.value.searchCutoffMs
    }
  }
}

const saveSettings = async () => {
  saving.value = true
  try {
    await indexApi.updateSettings(projectId.value, indexId.value, {
      searchCutoffMs: disableCutoff.value ? null : searchCutoffMs.value
    })
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    saving.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
