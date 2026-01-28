<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Typo Tolerance</h3>
        <p class="text-gray-500 text-sm">Configure how Meilisearch handles typos in search queries.</p>
      </div>
      <button @click="saveSettings" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save' }}
      </button>
    </div>

    <div class="card p-6 space-y-6">
      <!-- Enabled -->
      <div class="flex items-center justify-between">
        <div>
          <h4 class="text-white font-medium">Enable Typo Tolerance</h4>
          <p class="text-gray-500 text-sm">Allow matches with typos in search queries.</p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="config.enabled" class="sr-only peer" />
          <div class="w-11 h-6 bg-dark-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
        </label>
      </div>

      <!-- Min Word Size -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">Min Word Size for 1 Typo</label>
          <input
            v-model.number="config.minWordSizeForTypos.oneTypo"
            type="number"
            class="input"
            min="0"
          />
        </div>
        <div>
          <label class="label">Min Word Size for 2 Typos</label>
          <input
            v-model.number="config.minWordSizeForTypos.twoTypos"
            type="number"
            class="input"
            min="0"
          />
        </div>
      </div>

      <!-- Disable on Words -->
      <div>
        <label class="label">Disable on Words</label>
        <textarea
          v-model="disableOnWordsText"
          class="input font-mono text-sm"
          rows="3"
          placeholder="Words to disable typo tolerance on (one per line)"
        ></textarea>
      </div>

      <!-- Disable on Attributes -->
      <div>
        <label class="label">Disable on Attributes</label>
        <textarea
          v-model="disableOnAttributesText"
          class="input font-mono text-sm"
          rows="3"
          placeholder="Attributes to disable typo tolerance on (one per line)"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject, watch, computed } from 'vue'
import { indexApi } from '@/api'

const projectId = inject('projectId')
const indexId = inject('indexId')
const settings = inject('settings')

const config = reactive({
  enabled: true,
  minWordSizeForTypos: {
    oneTypo: 5,
    twoTypos: 9,
  },
  disableOnWords: [],
  disableOnAttributes: [],
})

const saving = ref(false)

const disableOnWordsText = computed({
  get: () => config.disableOnWords.join('\n'),
  set: (val) => {
    config.disableOnWords = val.split('\n').map(s => s.trim()).filter(Boolean)
  }
})

const disableOnAttributesText = computed({
  get: () => config.disableOnAttributes.join('\n'),
  set: (val) => {
    config.disableOnAttributes = val.split('\n').map(s => s.trim()).filter(Boolean)
  }
})

const loadSettings = () => {
  if (settings.value?.typoTolerance) {
    const typo = settings.value.typoTolerance
    config.enabled = typo.enabled ?? true
    config.minWordSizeForTypos = typo.minWordSizeForTypos || { oneTypo: 5, twoTypos: 9 }
    config.disableOnWords = typo.disableOnWords || []
    config.disableOnAttributes = typo.disableOnAttributes || []
  }
}

const saveSettings = async () => {
  saving.value = true
  try {
    await indexApi.updateTypoTolerance(projectId.value, indexId.value, {
      enabled: config.enabled,
      minWordSizeForTypos: config.minWordSizeForTypos,
      disableOnWords: config.disableOnWords,
      disableOnAttributes: config.disableOnAttributes,
    })
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    saving.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
