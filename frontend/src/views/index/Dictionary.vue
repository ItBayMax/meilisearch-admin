<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Dictionary</h3>
        <p class="text-gray-500 text-sm">Define patterns that should be treated as single words.</p>
      </div>
      <button @click="saveDictionary" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save' }}
      </button>
    </div>

    <div class="card p-6">
      <textarea
        v-model="dictionaryText"
        class="input font-mono text-sm"
        rows="10"
        placeholder="Enter dictionary words/patterns, one per line"
      ></textarea>
      <p class="text-gray-500 text-xs mt-2">
        Patterns defined here will be treated as unique words during indexing.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, watch } from 'vue'
import { indexApi } from '@/api'

const projectId = inject('projectId')
const indexId = inject('indexId')
const settings = inject('settings')

const dictionary = ref([])
const saving = ref(false)

const dictionaryText = computed({
  get: () => dictionary.value.join('\n'),
  set: (val) => {
    dictionary.value = val.split('\n').map(s => s.trim()).filter(Boolean)
  }
})

const loadSettings = () => {
  if (settings.value?.dictionary) {
    dictionary.value = [...settings.value.dictionary]
  }
}

const saveDictionary = async () => {
  saving.value = true
  try {
    await indexApi.updateDictionary(projectId.value, indexId.value, dictionary.value)
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    saving.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
