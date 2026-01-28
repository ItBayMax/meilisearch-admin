<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Synonyms</h3>
        <p class="text-gray-500 text-sm">Define words that should be considered equivalent in searches.</p>
      </div>
      <button @click="saveSynonyms" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save' }}
      </button>
    </div>

    <div class="card p-4 space-y-4">
      <div v-for="(values, key, index) in synonyms" :key="index" class="flex items-start space-x-3">
        <div class="flex-1 grid grid-cols-2 gap-3">
          <input
            :value="key"
            @input="updateKey(key, $event.target.value)"
            type="text"
            class="input text-sm"
            placeholder="Word"
          />
          <input
            :value="values.join(', ')"
            @input="updateValues(key, $event.target.value)"
            type="text"
            class="input text-sm"
            placeholder="Synonyms (comma separated)"
          />
        </div>
        <button @click="removeSynonym(key)" class="p-2 rounded hover:bg-dark-700 text-red-400">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <button @click="addSynonym" class="btn btn-ghost text-sm">
        + Add Synonym
      </button>
    </div>

    <div class="card p-4">
      <h4 class="text-white font-medium mb-2">Example</h4>
      <p class="text-gray-400 text-sm">
        If you set <code class="text-primary-400">phone</code> with synonyms <code class="text-primary-400">mobile, cellphone</code>,
        searching for "phone" will also return results containing "mobile" or "cellphone".
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject, watch } from 'vue'
import { indexApi } from '@/api'

const projectId = inject('projectId')
const indexId = inject('indexId')
const settings = inject('settings')

const synonyms = reactive({})
const saving = ref(false)

const loadSettings = () => {
  Object.keys(synonyms).forEach(key => delete synonyms[key])
  if (settings.value?.synonyms) {
    Object.assign(synonyms, settings.value.synonyms)
  }
}

const addSynonym = () => {
  const key = `word_${Date.now()}`
  synonyms[key] = []
}

const removeSynonym = (key) => {
  delete synonyms[key]
}

const updateKey = (oldKey, newKey) => {
  if (oldKey === newKey) return
  const values = synonyms[oldKey]
  delete synonyms[oldKey]
  synonyms[newKey] = values
}

const updateValues = (key, value) => {
  synonyms[key] = value.split(',').map(s => s.trim()).filter(Boolean)
}

const saveSynonyms = async () => {
  saving.value = true
  try {
    // Clean up empty or invalid entries
    const cleanSynonyms = {}
    for (const [key, values] of Object.entries(synonyms)) {
      if (key.trim() && values.length > 0) {
        cleanSynonyms[key.trim()] = values
      }
    }
    await indexApi.updateSynonyms(projectId.value, indexId.value, cleanSynonyms)
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    saving.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
