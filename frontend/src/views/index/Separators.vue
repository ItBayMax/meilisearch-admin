<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Separators</h3>
        <p class="text-gray-500 text-sm">Configure separator tokens for word segmentation.</p>
      </div>
      <button @click="saveSeparators" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save' }}
      </button>
    </div>

    <div class="card p-6 space-y-6">
      <div>
        <label class="label">Separator Tokens</label>
        <textarea
          v-model="separatorTokensText"
          class="input font-mono text-sm"
          rows="4"
          placeholder="Characters that separate words (one per line)"
        ></textarea>
        <p class="text-gray-500 text-xs mt-1">Additional characters that should be treated as word separators.</p>
      </div>

      <div>
        <label class="label">Non-Separator Tokens</label>
        <textarea
          v-model="nonSeparatorTokensText"
          class="input font-mono text-sm"
          rows="4"
          placeholder="Characters that should NOT separate words (one per line)"
        ></textarea>
        <p class="text-gray-500 text-xs mt-1">Characters that should be kept as part of words.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, watch } from 'vue'
import { indexApi } from '@/api'

const projectId = inject('projectId')
const indexId = inject('indexId')
const settings = inject('settings')

const separatorTokens = ref([])
const nonSeparatorTokens = ref([])
const saving = ref(false)

const separatorTokensText = computed({
  get: () => separatorTokens.value.join('\n'),
  set: (val) => {
    separatorTokens.value = val.split('\n').filter(s => s)
  }
})

const nonSeparatorTokensText = computed({
  get: () => nonSeparatorTokens.value.join('\n'),
  set: (val) => {
    nonSeparatorTokens.value = val.split('\n').filter(s => s)
  }
})

const loadSettings = () => {
  if (settings.value) {
    separatorTokens.value = settings.value.separatorTokens || []
    nonSeparatorTokens.value = settings.value.nonSeparatorTokens || []
  }
}

const saveSeparators = async () => {
  saving.value = true
  try {
    await indexApi.updateSeparatorTokens(projectId.value, indexId.value, separatorTokens.value)
    await indexApi.updateNonSeparatorTokens(projectId.value, indexId.value, nonSeparatorTokens.value)
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    saving.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
