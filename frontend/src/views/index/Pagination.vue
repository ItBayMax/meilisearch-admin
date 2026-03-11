<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">{{ settingsStore.t('pagination') }}</h3>
        <p class="text-gray-500 text-sm">{{ settingsStore.t('paginationDesc') }}</p>
      </div>
      <button @click="savePagination" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? settingsStore.t('saving') : settingsStore.t('save') }}
      </button>
    </div>

    <div class="card p-6">
      <div>
        <label class="label">{{ settingsStore.t('maxTotalHits') }}</label>
        <input
          v-model.number="maxTotalHits"
          type="number"
          class="input"
          min="1"
          max="100000"
        />
        <p class="text-gray-500 text-xs mt-2">
          {{ settingsStore.t('paginationHint') }}
        </p>
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

const maxTotalHits = ref(1000)
const saving = ref(false)

const loadSettings = () => {
  if (settings.value?.pagination?.maxTotalHits) {
    maxTotalHits.value = settings.value.pagination.maxTotalHits
  }
}

const savePagination = async () => {
  saving.value = true
  try {
    await indexApi.updatePagination(projectId.value, indexId.value, {
      maxTotalHits: maxTotalHits.value
    })
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    saving.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
