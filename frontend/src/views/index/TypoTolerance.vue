<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">{{ settingsStore.t('typoTolerance') }}</h3>
        <p class="text-gray-500 text-sm">{{ settingsStore.t('typoToleranceDesc') }}</p>
      </div>
      <button @click="saveSettings" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? settingsStore.t('saving') : settingsStore.t('save') }}
      </button>
    </div>

    <div class="card p-6 space-y-6">
      <!-- Enabled -->
      <div class="flex items-center justify-between">
        <div>
          <h4 class="text-white font-medium">{{ settingsStore.t('enableLabel') }}</h4>
          <p class="text-gray-500 text-sm">{{ settingsStore.t('enableDesc') }}</p>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="config.enabled" class="sr-only peer" />
          <div class="w-11 h-6 bg-dark-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
        </label>
      </div>

      <!-- Min Word Size -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="label">{{ settingsStore.t('minWordOneTypo') }}</label>
          <input
            v-model.number="config.minWordSizeForTypos.oneTypo"
            type="number"
            class="input"
            min="0"
          />
        </div>
        <div>
          <label class="label">{{ settingsStore.t('minWordTwoTypos') }}</label>
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
        <label class="label">{{ settingsStore.t('disableOnWords') }}</label>
        <p class="text-gray-500 text-xs mb-1">{{ settingsStore.t('disableOnWordsDesc') }}</p>
        <textarea
          v-model="disableOnWordsText"
          class="input font-mono text-sm"
          rows="3"
          :placeholder="settingsStore.t('disableOnWordsPlaceholder')"
        ></textarea>
      </div>

      <!-- Disable on Attributes -->
      <div>
        <label class="label">{{ settingsStore.t('disableOnAttributes') }}</label>
        <p class="text-gray-500 text-xs mb-1">{{ settingsStore.t('disableOnAttributesDesc') }}</p>
        <textarea
          v-model="disableOnAttributesText"
          class="input font-mono text-sm"
          rows="3"
          :placeholder="settingsStore.t('disableOnAttributesPlaceholder')"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject, watch, computed } from 'vue'
import { useSettingsStore } from '@/store/settings'
import { indexApi } from '@/api'

const settingsStore = useSettingsStore()

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
