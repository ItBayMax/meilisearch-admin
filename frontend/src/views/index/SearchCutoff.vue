<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">{{ settingsStore.t('searchCutoff') }}</h3>
        <p class="text-gray-500 text-sm">{{ settingsStore.t('searchCutoffDesc') }}</p>
      </div>
      <button @click="saveSettings" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? settingsStore.t('saving') : settingsStore.t('save') }}
      </button>
    </div>

    <div class="card p-6 space-y-6">
      <div>
        <label class="label">{{ settingsStore.t('cutoffDuration') }}</label>
        <input
          v-model.number="searchCutoffMs"
          type="number"
          class="input"
          min="1"
          max="60000"
          placeholder="1500"
        />
        <p class="text-gray-500 text-xs mt-2">
          {{ settingsStore.t('cutoffHint') }}
        </p>
      </div>

      <div class="bg-dark-800 rounded-lg p-4">
        <h4 class="text-white font-medium mb-2">{{ settingsStore.t('recommendedValues') }}</h4>
        <ul class="text-gray-400 text-sm space-y-1">
          <li><code class="text-primary-400">1500</code> - {{ settingsStore.t('rec1500') }}</li>
          <li><code class="text-primary-400">500-1000</code> - {{ settingsStore.t('rec500') }}</li>
          <li><code class="text-primary-400">3000-5000</code> - {{ settingsStore.t('rec3000') }}</li>
          <li><code class="text-primary-400">null</code> - {{ settingsStore.t('recNull') }}</li>
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
          {{ settingsStore.t('disableCutoff') }}
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, watch } from 'vue'
import { useSettingsStore } from '@/store/settings'
import { indexApi } from '@/api'

const settingsStore = useSettingsStore()

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
