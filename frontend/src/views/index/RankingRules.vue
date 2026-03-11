<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">{{ settingsStore.t('rankingRules') }}</h3>
        <p class="text-gray-500 text-sm">{{ settingsStore.t('rankingRulesDesc') }}</p>
      </div>
      <div class="flex space-x-2">
        <button @click="resetRules" class="btn btn-secondary text-sm">{{ settingsStore.t('resetToDefault') }}</button>
        <button @click="saveRules" class="btn btn-primary text-sm" :disabled="saving">
          {{ saving ? settingsStore.t('saving') : settingsStore.t('save') }}
        </button>
      </div>
    </div>

    <div class="card p-4">
      <p class="text-gray-400 text-sm mb-4">
        {{ settingsStore.t('dragToReorder') }}
      </p>

      <div class="space-y-2">
        <div
          v-for="(rule, index) in rules"
          :key="index"
          class="flex items-center space-x-3 p-3 bg-dark-800 rounded-lg"
        >
          <span class="text-gray-500 font-mono text-sm w-6">{{ index + 1 }}.</span>
          <div class="flex-1">
            <input
              v-model="rules[index]"
              type="text"
              class="input text-sm"
              placeholder="Rule"
            />
          </div>
          <button
            @click="moveUp(index)"
            :disabled="index === 0"
            class="p-1.5 rounded hover:bg-dark-700 text-gray-400 disabled:opacity-30"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
            </svg>
          </button>
          <button
            @click="moveDown(index)"
            :disabled="index === rules.length - 1"
            class="p-1.5 rounded hover:bg-dark-700 text-gray-400 disabled:opacity-30"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <button @click="removeRule(index)" class="p-1.5 rounded hover:bg-dark-700 text-red-400">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <button @click="addRule" class="btn btn-ghost mt-4 text-sm">
        {{ settingsStore.t('addCustomRule') }}
      </button>
    </div>

    <div class="card p-4">
      <h4 class="text-white font-medium mb-2">{{ settingsStore.t('defaultRulesLabel') }}</h4>
      <ul class="text-gray-400 text-sm space-y-1">
        <li><code class="text-primary-400">words</code> - {{ settingsStore.t('ruleWords') }}</li>
        <li><code class="text-primary-400">typo</code> - {{ settingsStore.t('ruleTypo') }}</li>
        <li><code class="text-primary-400">proximity</code> - {{ settingsStore.t('ruleProximity') }}</li>
        <li><code class="text-primary-400">attribute</code> - {{ settingsStore.t('ruleAttribute') }}</li>
        <li><code class="text-primary-400">sort</code> - {{ settingsStore.t('ruleSort') }}</li>
        <li><code class="text-primary-400">exactness</code> - {{ settingsStore.t('ruleExactness') }}</li>
      </ul>
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

const rules = ref([])
const saving = ref(false)

const defaultRules = ['words', 'typo', 'proximity', 'attribute', 'sort', 'exactness']

const loadSettings = () => {
  if (settings.value?.rankingRules) {
    rules.value = [...settings.value.rankingRules]
  } else {
    rules.value = [...defaultRules]
  }
}

const moveUp = (index) => {
  if (index > 0) {
    const temp = rules.value[index]
    rules.value[index] = rules.value[index - 1]
    rules.value[index - 1] = temp
  }
}

const moveDown = (index) => {
  if (index < rules.value.length - 1) {
    const temp = rules.value[index]
    rules.value[index] = rules.value[index + 1]
    rules.value[index + 1] = temp
  }
}

const removeRule = (index) => {
  rules.value.splice(index, 1)
}

const addRule = () => {
  rules.value.push('')
}

const resetRules = () => {
  rules.value = [...defaultRules]
}

const saveRules = async () => {
  saving.value = true
  try {
    const validRules = rules.value.filter(r => r.trim())
    await indexApi.updateRankingRules(projectId.value, indexId.value, validRules)
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    saving.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
