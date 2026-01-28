<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg font-semibold text-white">Faceting</h3>
        <p class="text-gray-500 text-sm">Configure faceting behavior for search results.</p>
      </div>
      <button @click="saveFaceting" class="btn btn-primary text-sm" :disabled="saving">
        {{ saving ? 'Saving...' : 'Save' }}
      </button>
    </div>

    <div class="card p-6 space-y-6">
      <div>
        <label class="label">Max Values Per Facet</label>
        <input
          v-model.number="maxValuesPerFacet"
          type="number"
          class="input"
          min="1"
          max="65535"
        />
        <p class="text-gray-500 text-xs mt-2">
          The maximum number of facet values returned for each facet. Default is 100.
        </p>
      </div>

      <div>
        <label class="label">Sort Facet Values By</label>
        <div class="space-y-2 mt-2">
          <label class="flex items-center space-x-2 cursor-pointer">
            <input
              type="radio"
              v-model="sortFacetValuesBy"
              value="alpha"
              class="text-primary-500"
            />
            <span class="text-gray-300">Alphabetically (alpha)</span>
          </label>
          <label class="flex items-center space-x-2 cursor-pointer">
            <input
              type="radio"
              v-model="sortFacetValuesBy"
              value="count"
              class="text-primary-500"
            />
            <span class="text-gray-300">By count (count)</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, watch } from 'vue'
import { indexApi } from '@/api'

const projectId = inject('projectId')
const indexId = inject('indexId')
const settings = inject('settings')

const maxValuesPerFacet = ref(100)
const sortFacetValuesBy = ref('alpha')
const saving = ref(false)

const loadSettings = () => {
  if (settings.value?.faceting) {
    maxValuesPerFacet.value = settings.value.faceting.maxValuesPerFacet || 100
    const sortBy = settings.value.faceting.sortFacetValuesBy
    if (sortBy && sortBy['*']) {
      sortFacetValuesBy.value = sortBy['*']
    }
  }
}

const saveFaceting = async () => {
  saving.value = true
  try {
    await indexApi.updateFaceting(projectId.value, indexId.value, {
      maxValuesPerFacet: maxValuesPerFacet.value,
      sortFacetValuesBy: {
        '*': sortFacetValuesBy.value
      }
    })
  } catch (err) {
    console.error('Failed to save:', err)
  } finally {
    saving.value = false
  }
}

watch(settings, loadSettings, { immediate: true })
</script>
