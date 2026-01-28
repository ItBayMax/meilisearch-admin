<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Ranking Rules</h3>
        <p class="text-gray-500 text-sm">Rules that determine the relevancy of search results. Order matters.</p>
      </div>
      <div class="flex space-x-2">
        <button @click="resetRules" class="btn btn-secondary text-sm">Reset to Default</button>
        <button @click="saveRules" class="btn btn-primary text-sm" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save' }}
        </button>
      </div>
    </div>

    <div class="card p-4">
      <p class="text-gray-400 text-sm mb-4">
        Drag to reorder. The first rule has the most impact on relevancy.
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
        + Add Custom Rule
      </button>
    </div>

    <div class="card p-4">
      <h4 class="text-white font-medium mb-2">Default Rules</h4>
      <ul class="text-gray-400 text-sm space-y-1">
        <li><code class="text-primary-400">words</code> - Number of query words found</li>
        <li><code class="text-primary-400">typo</code> - Number of typos</li>
        <li><code class="text-primary-400">proximity</code> - Distance between query words</li>
        <li><code class="text-primary-400">attribute</code> - Attribute ranking order</li>
        <li><code class="text-primary-400">sort</code> - User-defined sort order</li>
        <li><code class="text-primary-400">exactness</code> - Similarity of matched words</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, watch } from 'vue'
import { indexApi } from '@/api'

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
