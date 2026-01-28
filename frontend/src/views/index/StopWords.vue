<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Stop Words</h3>
        <p class="text-gray-500 text-sm">Words that are ignored during search. Common words like "the", "a", "is" are typical stop words.</p>
      </div>
      <button @click="saveStopWords" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save' }}
      </button>
    </div>

    <div class="card p-6">
      <textarea
        v-model="stopWordsText"
        class="input font-mono text-sm"
        rows="10"
        placeholder="Enter stop words, one per line"
      ></textarea>
      <p class="text-gray-500 text-xs mt-2">
        Stop words are ignored during search and do not contribute to relevancy scoring.
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

const stopWords = ref([])
const saving = ref(false)

const stopWordsText = computed({
  get: () => stopWords.value.join('\n'),
  set: (val) => {
    stopWords.value = val.split('\n').map(s => s.trim()).filter(Boolean)
  }
})

const loadSettings = () => {
  if (settings.value?.stopWords) {
    stopWords.value = [...settings.value.stopWords]
  }
}

const saveStopWords = async () => {
  saving.value = true
  try {
    await indexApi.updateStopWords(projectId.value, indexId.value, stopWords.value)
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    saving.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
