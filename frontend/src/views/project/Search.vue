<template>
  <SearchLayout ref="searchLayout">
    <template #sidebar-content>
      <!-- Index Selection -->
      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-300">{{ settingsStore.t('selectIndex') }}</label>
        <select 
          v-model="selectedIndex" 
          class="input w-full" 
          @change="onIndexChange"
        >
          <option value="">{{ settingsStore.t('selectIndex') }}</option>
          <option v-for="idx in indexes" :key="idx.uid" :value="idx.uid">
            {{ idx.uid }}
          </option>
        </select>
      </div>

      <!-- Sort Options -->
      <div v-if="sortableAttributes.length" class="space-y-2">
        <label class="block text-sm font-medium text-gray-300">{{ settingsStore.t('sortBy') }}</label>
        <select v-model="sortBy" class="input w-full">
          <option value="">{{ settingsStore.t('sortBy') }}</option>
          <option v-for="attr in sortableAttributes" :key="attr" :value="attr + ':asc'">
            {{ attr }} (ASC)
          </option>
          <option v-for="attr in sortableAttributes" :key="attr + '-desc'" :value="attr + ':desc'">
            {{ attr }} (DESC)
          </option>
        </select>
      </div>

      <!-- Column Selection -->
      <div v-if="allColumns.length" class="space-y-2">
        <div class="flex items-center justify-between">
          <label class="block text-sm font-medium text-gray-300">{{ settingsStore.t('columns') }}</label>
          <span class="text-xs text-gray-500">{{ selectedColumns.length }}/{{ allColumns.length }}</span>
        </div>
        <div class="max-h-40 overflow-y-auto bg-dark-800 rounded border border-dark-700 p-2 space-y-1">
          <label
            v-for="col in allColumns"
            :key="col"
            class="flex items-center p-1 hover:bg-dark-700 rounded cursor-pointer"
          >
            <input type="checkbox" :value="col" v-model="selectedColumns" class="mr-2" />
            <span class="text-sm truncate">{{ col }}</span>
          </label>
        </div>
      </div>

      <!-- View Mode -->
      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-300">{{ settingsStore.t('viewMode') }}</label>
        <div class="flex rounded-lg overflow-hidden border border-dark-600">
          <button
            @click="viewMode = 'table'"
            :class="['flex-1 py-2 text-sm', viewMode === 'table' ? 'bg-primary-500 text-white' : 'text-gray-400 hover:text-white bg-dark-800']"
          >
            {{ settingsStore.t('tableView') }}
          </button>
          <button
            @click="viewMode = 'json'"
            :class="['flex-1 py-2 text-sm', viewMode === 'json' ? 'bg-primary-500 text-white' : 'text-gray-400 hover:text-white bg-dark-800']"
          >
            {{ settingsStore.t('jsonView') }}
          </button>
        </div>
      </div>

      <!-- Ranking Score -->
      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-300">{{ settingsStore.t('rankingScore') }}</label>
        <button
          @click="showRankingScore = !showRankingScore"
          :class="['w-full py-2 rounded-lg flex items-center justify-center', showRankingScore ? 'bg-primary-500 text-white' : 'bg-dark-800 text-gray-400 hover:text-white']"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          {{ showRankingScore ? settingsStore.t('enabled') : settingsStore.t('disabled') }}
        </button>
      </div>


      <!-- Filters Section -->
      <div v-if="filterableAttributes.length" class="space-y-3 pt-4 border-t border-dark-700">
        <div class="flex items-center justify-between">
          <h4 class="text-sm font-medium text-gray-300">{{ settingsStore.t('filters') }}</h4>
          <div class="flex gap-1">
            <button 
              @click="clearAllFilters" 
              class="btn btn-secondary text-xs py-1 px-2 flex items-center gap-1"
              :disabled="filterConditions.length === 1 && !hasValidConditions"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              {{ settingsStore.t('clear') }}
            </button>
            <button 
              @click="addFilterCondition" 
              class="btn btn-secondary text-xs py-1 px-2 flex items-center gap-1"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              {{ settingsStore.t('add') }}
            </button>
          </div>
        </div>
        
        <!-- Filter Conditions -->
        <div class="space-y-2 max-h-60 overflow-y-auto">
          <div 
            v-for="(condition, index) in filterConditions" 
            :key="index" 
            class="flex items-center gap-2 p-2 bg-dark-800 rounded"
          >
            <select 
              v-model="condition.attribute" 
              class="input text-sm flex-1 min-w-[100px]"
              @change="updateConditionOperators(index)"
            >
              <option value="">{{ settingsStore.t('selectAttribute') }}</option>
              <option 
                v-for="attr in filterableAttributes" 
                :key="attr.name" 
                :value="attr.name"
              >
                {{ attr.name }}
              </option>
            </select>
            
            <select 
              v-model="condition.operator" 
              class="input text-sm w-20"
              :disabled="!condition.attribute"
            >
              <option value="">{{ settingsStore.t('operator') }}</option>
              <option 
                v-for="op in getAvailableOperators(condition.attribute)" 
                :key="op.value" 
                :value="op.value"
              >
                {{ op.label }}
              </option>
            </select>
            
            <input
              v-model="condition.value"
              type="text"
              class="input text-sm flex-1 min-w-[80px]"
              :placeholder="settingsStore.t('value')"
              :disabled="!condition.operator"
            />
            
            <button 
              @click="removeFilterCondition(index)" 
              class="text-red-400 hover:text-red-300 p-1"
              :disabled="filterConditions.length <= 1"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
          
          <div v-if="filterConditions.length === 0" class="text-center py-4 text-gray-500 text-sm">
            {{ settingsStore.t('noFilterConditions') }}
          </div>
        </div>
        
        <!-- Apply filters button -->
        <button 
          @click="applyFilters" 
          class="btn btn-primary w-full text-sm"
          :disabled="false"
        >
          {{ settingsStore.t('applyFilters') }}
        </button>
      </div>

      <!-- Vector Search Configuration -->
      <div v-if="selectedIndex && hasEmbeddersConfig" class="space-y-3 pt-4 border-t border-dark-700">
        <h4 class="text-sm font-medium text-gray-300">{{ settingsStore.t('vectorSearch') }}</h4>
        
        <div class="flex items-center justify-between">
          <label class="text-sm text-gray-300">{{ settingsStore.t('enableVectorSearch') }}</label>
          <button 
            @click="enableVectorSearch = !enableVectorSearch" 
            :class="[
              'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none',
              enableVectorSearch ? 'bg-primary-500' : 'bg-dark-600'
            ]"
          >
            <span 
              :class="[
                'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                enableVectorSearch ? 'translate-x-6' : 'translate-x-1'
              ]"
            />
          </button>
        </div>

        <div v-if="enableVectorSearch" class="space-y-2">
          <div class="flex justify-between">
            <label class="text-sm text-gray-300">{{ settingsStore.t('semanticRatio') }}</label>
            <span class="text-sm text-primary-400">{{ semanticRatio }}</span>
          </div>
          <input 
            v-model="semanticRatio" 
            type="range" 
            min="0" 
            max="1" 
            step="0.1"
            class="w-full h-2 bg-dark-700 rounded-lg appearance-none cursor-pointer accent-primary-500"
          />
          <div class="flex justify-between text-xs text-gray-500">
            <span>{{ settingsStore.t('keywordSearch') }}</span>
            <span>{{ settingsStore.t('semanticSearch') }}</span>
          </div>
        </div>

        <!-- Embedder Selection -->
        <div v-if="enableVectorSearch && availableEmbedders.length > 0" class="space-y-2">
          <label class="block text-sm text-gray-300">{{ settingsStore.t('selectEmbedder') }}</label>
          <select v-model="selectedEmbedder" class="input w-full text-sm">
            <option value="">自动选择</option>
            <option v-for="embedder in availableEmbedders" :key="embedder" :value="embedder">
              {{ embedder }}
            </option>
          </select>
        </div>

        <!-- Hybrid Search Info -->
        <div v-if="enableVectorSearch" class="text-xs text-gray-500 bg-dark-800 p-3 rounded-lg">
          <p>• {{ settingsStore.t('hybridSearchInfo1') }}</p>
          <p>• {{ settingsStore.t('hybridSearchInfo2') }}</p>
          <p>• {{ settingsStore.t('hybridSearchInfo3') }}</p>
        </div>
      </div>

      <!-- No Vector Engine Warning -->
      <div v-else-if="selectedIndex && !hasEmbeddersConfig" class="pt-4 border-t border-dark-700">
        <div class="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3">
          <div class="flex items-start gap-2">
            <svg class="w-5 h-5 text-yellow-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div class="flex-1">
              <h4 class="text-sm font-medium text-yellow-500">{{ settingsStore.t('noVectorEngineConfigured') }}</h4>
              <p class="text-xs text-yellow-400 mt-1">{{ settingsStore.t('configureVectorEngineFirst') }}</p>
              <router-link 
                :to="`/projects/${projectId}/indexes/${selectedIndex}/embedders`"
                class="text-xs text-yellow-300 hover:text-yellow-200 underline mt-2 inline-block"
              >
                {{ settingsStore.t('goToEmbeddersSettings') }} →
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Export Query Button -->
      <div class="pt-4 border-t border-dark-700">
        <button 
          @click="showExportModal = true" 
          class="btn btn-primary w-full text-sm py-2 px-3 flex items-center justify-center gap-2 mt-2"
          :title="settingsStore.t('exportQuery')"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          {{ settingsStore.t('exportQuery') }}
        </button>
      </div>
    </template>

    <template #main-content>
      <!-- Search Bar -->
      <div class="mb-6">
        <div class="flex items-center space-x-4">
          <div class="flex-1 relative">
            <svg class="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              class="input pl-12 w-full"
              :placeholder="settingsStore.t('searchDocuments')"
              @keyup.enter="performSearch"
            />
          </div>
          <button @click="performSearch" class="btn btn-primary" :disabled="loading">
            {{ loading ? settingsStore.t('searching') : settingsStore.t('search') }}
          </button>
        </div>
      </div>

      <!-- Loading -->
      <Loading v-if="loading" />

      <!-- Results -->
      <template v-else-if="results">
        <div class="flex items-center justify-between text-sm text-gray-400 mb-4">
          <span>{{ results.estimatedTotalHits || results.hits?.length || 0 }} results ({{ results.processingTimeMs }}ms)</span>
        </div>

        <!-- Table View -->
        <div v-if="viewMode === 'table'" class="flex flex-col flex-1 overflow-hidden">
          <div class="card flex-1 overflow-hidden flex flex-col">
            <div class="overflow-auto flex-1 min-h-0">
              <table class="w-full">
                <thead class="bg-dark-800 sticky top-0 z-10">
                  <tr>
                    <th class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase w-24">{{ settingsStore.t('actions') }}</th>
                    <th v-if="showRankingScore" class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase w-20">{{ settingsStore.t('score') }}</th>
                    <th
                      v-for="col in visibleColumns"
                      :key="col"
                      class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase whitespace-nowrap"
                    >
                      {{ col }}
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-dark-700">
                  <tr
                    v-for="(hit, index) in results.hits"
                    :key="index"
                    class="hover:bg-dark-800/50"
                  >
                    <td class="px-3 py-2">
                      <div class="flex items-center space-x-1">
                        <button @click="copyJson(hit, $event)" class="p-1 text-gray-400 hover:text-white" :title="settingsStore.t('copyJson')">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                          </svg>
                        </button>
                        <button @click="editDocument(hit)" class="p-1 text-gray-400 hover:text-white" :title="settingsStore.t('edit')">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button @click="confirmDeleteDocument(hit)" class="p-1 text-gray-400 hover:text-red-400" :title="settingsStore.t('delete')">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                    <td v-if="showRankingScore" class="px-3 py-2 text-xs text-primary-400 font-mono">
                      {{ hit._rankingScore ? hit._rankingScore.toFixed(4) : '-' }}
                    </td>
                    <td
                      v-for="col in visibleColumns"
                      :key="col"
                      class="px-3 py-2 text-sm text-gray-300 max-w-[120px] w-[120px]"
                    >
                      <CellValue :value="hit[col]" :cellKey="`${index}-${col}`" :medium-length="20" />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- JSON View -->
        <div v-else class="flex flex-col flex-1 overflow-hidden">
          <div class="space-y-3 flex-1 overflow-auto">
            <div
              v-for="(hit, index) in results.hits"
              :key="index"
              class="card p-4"
            >
              <div class="flex items-center justify-between mb-2">
                <span v-if="showRankingScore && hit._rankingScore" class="text-xs text-primary-400 font-mono">
                  Score: {{ hit._rankingScore.toFixed(4) }}
                </span>
                <div class="flex items-center space-x-2">
                  <button @click="copyJson(hit, $event)" class="p-1 text-gray-400 hover:text-white" :title="settingsStore.t('copyJson')">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  </button>
                  <button @click="editDocument(hit)" class="p-1 text-gray-400 hover:text-white" :title="settingsStore.t('edit')">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button @click="confirmDeleteDocument(hit)" class="p-1 text-gray-400 hover:text-red-400" :title="settingsStore.t('delete')">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
              <div class="json-view bg-dark-800 p-4 rounded-lg border border-dark-600 overflow-auto max-h-96">
                <div 
                  v-for="(line, index) in formatJsonLines(cleanHit(hit))" 
                  :key="index" 
                  class="text-gray-300 text-sm font-mono py-0.5"
                  :style="getLineStyle(line)"
                >{{ line }}</div>
              </div>
            </div>
          </div>
        </div>

        <Empty v-if="results.hits?.length === 0" :title="settingsStore.t('noResults')" :description="settingsStore.t('noResults')" />
      </template>

      <Empty v-else :title="settingsStore.t('selectAnIndex')" :description="settingsStore.t('selectAnIndexDesc')" />

      <!-- Modals -->
      <Modal v-model:visible="showEditModal" :title="settingsStore.t('editDocument')" size="lg">
        <div class="space-y-4">
          <textarea
            v-model="editJson"
            class="input font-mono text-sm"
            rows="15"
          ></textarea>
        </div>
        <template #footer>
          <div class="flex justify-end space-x-3">
            <button @click="showEditModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
            <button @click="saveDocument" class="btn btn-primary" :disabled="saving">
              {{ saving ? settingsStore.t('saving') : settingsStore.t('save') }}
            </button>
          </div>
        </template>
      </Modal>

      <Modal v-model:visible="showDeleteModal" :title="settingsStore.t('deleteDocument')" size="sm">
        <p class="text-gray-300">{{ settingsStore.t('deleteConfirm') }}? {{ settingsStore.t('cannotUndo') }}</p>
        <template #footer>
          <div class="flex justify-end space-x-3">
            <button @click="showDeleteModal = false" class="btn btn-secondary">{{ settingsStore.t('cancel') }}</button>
            <button @click="deleteDocument" class="btn btn-danger" :disabled="deleting">
              {{ deleting ? settingsStore.t('deleting') : settingsStore.t('delete') }}
            </button>
          </div>
        </template>
      </Modal>

      <!-- Export Query Modal -->
      <Modal v-model:visible="showExportModal" :title="settingsStore.t('exportQuery')" size="lg">
        <div class="space-y-6">
          <div class="text-gray-300 text-sm">
            {{ settingsStore.t('exportQueryDescription') }}
          </div>
          
          <!-- Query Preview -->
          <div class="bg-dark-800 rounded-lg border border-dark-700 overflow-hidden">
            <div class="flex items-center justify-between px-4 py-2 bg-dark-700 border-b border-dark-600">
              <div class="flex items-center space-x-2">
                <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
                <span class="text-sm font-medium text-gray-200">{{ settingsStore.t('queryPreview') }}</span>
              </div>
              <button 
                @click="copyQueryPreview" 
                class="p-1 text-gray-400 hover:text-white rounded transition-colors"
                :title="settingsStore.t('copyJson')"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </button>
            </div>
            <div class="p-4 font-mono text-sm">
              <pre class="text-gray-200 overflow-x-auto">{{ formatQueryPreview() }}</pre>
            </div>
          </div>
          
          <!-- Export Options -->
          <div class="space-y-3">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <button 
                @click="exportAsCurl" 
                class="btn btn-primary flex items-center justify-center space-x-2 py-3"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
                <span>{{ settingsStore.t('copyCurlCommand') }}</span>
              </button>
              
              <button 
                @click="exportAsPostman" 
                class="btn btn-secondary flex items-center justify-center space-x-2 py-3"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                </svg>
                <span>{{ settingsStore.t('exportAsPostman') }}</span>
              </button>
              
              <button 
                @click="downloadQueryBody" 
                class="btn btn-secondary flex items-center justify-center space-x-2 py-3"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                <span>{{ settingsStore.t('downloadRequestBody') }}</span>
              </button>
              

            </div>
          </div>
        </div>
        
        <template #footer>
          <div class="flex justify-end space-x-3">
            <button @click="showExportModal = false" class="btn btn-secondary">{{ settingsStore.t('close') }}</button>
          </div>
        </template>
      </Modal>
    </template>
  </SearchLayout>
  
  <!-- Copy Success Tip -->
  <div 
    v-if="showCopyTip" 
    class="fixed bg-primary-500 text-white px-3 py-1.5 rounded-lg shadow-lg z-50 fade-in flex items-center space-x-1 text-sm animate-bounce"
    :style="{
      left: copyTipPosition.x + 'px',
      top: copyTipPosition.y + 'px',
      transform: 'translateX(-50%) translateY(-100%)'
    }"
  >
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
    </svg>
    <span>{{ copyTipMessage }}</span>
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSettingsStore } from '@/store/settings'
import { indexApi } from '@/api'
import Loading from '@/components/common/Loading.vue'
import Empty from '@/components/common/Empty.vue'
import Modal from '@/components/common/Modal.vue'
import CellValue from '@/components/common/CellValue.vue'
import SearchLayout from '@/components/layout/SearchLayout.vue'

const route = useRoute()
const settingsStore = useSettingsStore()
const projectId = inject('projectId')

// Refs for components
const searchLayout = ref(null)

const indexes = ref([])
const selectedIndex = ref('')
const searchQuery = ref('')
const results = ref(null)
const loading = ref(false)
const viewMode = ref('table')
const sortBy = ref('')
const showRankingScore = ref(false)
const showColumnSelector = ref(false)
const currentSettings = ref(null)
const showExportModal = ref(false)
const enableVectorSearch = ref(false)
const semanticRatio = ref(0.5)
const selectedEmbedder = ref('')
const availableEmbedders = ref([])

const sortableAttributes = ref([])
const filterableAttributes = ref([])
const displayedAttributes = ref([])
const filters = reactive({})
const embeddersConfig = ref(null)

// Filter conditions for expression builder
const filterConditions = ref([
  { attribute: '', operator: '', value: '' }
])

// Filter panel collapse state
const isFiltersCollapsed = ref(false)

const allColumns = ref([])
const selectedColumns = ref([])

const showEditModal = ref(false)
const showDeleteModal = ref(false)
const editJson = ref('')
const editingDocument = ref(null)
const documentToDelete = ref(null)
const saving = ref(false)
const deleting = ref(false)

const visibleColumns = computed(() => {
  if (selectedColumns.value.length > 0) {
    return selectedColumns.value
  }
  return allColumns.value.slice(0, 6)
})

const hasEmbeddersConfig = computed(() => {
  return embeddersConfig.value && Object.keys(embeddersConfig.value).length > 0
})

// Filter operators based on attribute mode
const equalityOperators = [
  { value: '=', label: '=' },
  { value: '!=', label: '!=' },
  { value: 'IN', label: 'IN' },
  { value: 'NOT IN', label: 'NOT IN' },
  { value: 'EXISTS', label: 'EXISTS' },
  { value: 'IS EMPTY', label: 'IS EMPTY' },
  { value: 'IS NULL', label: 'IS NULL' }
]

const comparisonOperators = [
  { value: '>', label: '>' },
  { value: '<', label: '<' },
  { value: '>=', label: '>=' },
  { value: '<=', label: '<=' },
  { value: 'EXISTS', label: 'EXISTS' },
  { value: 'IS EMPTY', label: 'IS EMPTY' },
  { value: 'IS NULL', label: 'IS NULL' }
]

const getAvailableOperators = (attributeName) => {
  if (!attributeName) return []
  const attr = filterableAttributes.value.find(a => a.name === attributeName)
  return attr?.mode === 'comparison' ? comparisonOperators : equalityOperators
}

const updateConditionOperators = (index) => {
  // Reset operator and value when attribute changes
  filterConditions.value[index].operator = ''
  filterConditions.value[index].value = ''
}

const addFilterCondition = () => {
  filterConditions.value.push({ attribute: '', operator: '', value: '' })
}

const removeFilterCondition = (index) => {
  if (filterConditions.value.length > 1) {
    filterConditions.value.splice(index, 1)
  }
}

const hasValidConditions = computed(() => {
  return filterConditions.value.some(cond => 
    cond.attribute && cond.operator && cond.value
  )
})

const buildFilterExpression = () => {
  const validConditions = filterConditions.value.filter(cond => 
    cond.attribute && cond.operator && cond.value
  )
  
  if (validConditions.length === 0) return ''
  
  return validConditions
    .map(cond => {
      if (cond.operator === 'IN' || cond.operator === 'NOT IN') {
        return `${cond.attribute} ${cond.operator} [${cond.value}]`
      } else if (cond.operator === 'EXISTS' || cond.operator === 'IS EMPTY' || cond.operator === 'IS NULL') {
        return `${cond.attribute} ${cond.operator}`
      } else {
        return `${cond.attribute} ${cond.operator} "${cond.value}"`
      }
    })
    .join(' AND ')
}

const clearAllFilters = () => {
  filterConditions.value = [{ attribute: '', operator: '', value: '' }]
  performSearch() // Clear filters and re-search
}

// Export query functionality
const buildMeilisearchQuery = () => {
  const query = {}
  
  // 添加搜索关键词
  if (searchQuery.value) {
    query.q = searchQuery.value
  }
  
  // 添加排序
  if (sortBy.value) {
    query.sort = [sortBy.value]
  }
  
  // 添加过滤条件
  const filterExpression = buildFilterExpression()
  if (filterExpression) {
    query.filter = filterExpression
  }
  
  // 添加分页
  query.limit = 20
  query.offset = 0
  
  // 添加评分显示
  if (showRankingScore.value) {
    query.showRankingScore = true
  }
  
  // 添加选择的列
  if (selectedColumns.value.length > 0) {
    query.attributesToRetrieve = selectedColumns.value
  }
  
  return query
}

const formatQueryPreview = () => {
  const query = buildMeilisearchQuery()
  return JSON.stringify(query, null, 2)
}

const generateCurlCommand = () => {
  const query = buildMeilisearchQuery()
  const meilisearchUrl = `${currentSettings.value?.host || 'http://localhost:7700'}/indexes/${selectedIndex.value}/search`
  
  return `curl -X POST "${meilisearchUrl}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${currentSettings.value?.apiKey || 'YOUR_API_KEY'}" \
  -d '${JSON.stringify(query, null, 2)}'`
}

const generatePostmanCollection = () => {
  const query = buildMeilisearchQuery()
  const meilisearchUrl = `${currentSettings.value?.host || 'http://localhost:7700'}/indexes/${selectedIndex.value}/search`
  
  return {
    info: {
      name: `Meilisearch Search - ${selectedIndex.value}`,
      schema: "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    item: [
      {
        name: "Search Documents",
        request: {
          method: "POST",
          header: [
            {
              key: "Content-Type",
              value: "application/json"
            },
            {
              key: "Authorization", 
              value: `Bearer ${currentSettings.value?.apiKey || 'YOUR_API_KEY'}`
            }
          ],
          body: {
            mode: "raw",
            raw: JSON.stringify(query, null, 2)
          },
          url: {
            raw: meilisearchUrl,
            protocol: 'https',
            host: [new URL(meilisearchUrl).hostname],
            path: ['indexes', selectedIndex.value, 'search']
          }
        }
      }
    ]
  }
}

const copyQueryPreview = async () => {
  try {
    await navigator.clipboard.writeText(formatQueryPreview())
    showCopySuccessTip(settingsStore.t('copied'))
  } catch (err) {
    console.error('Copy failed:', err)
  }
}

const downloadQueryBody = async () => {
  try {
    const query = buildMeilisearchQuery()
    const blob = new Blob([JSON.stringify(query, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `meilisearch-query-${selectedIndex.value}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    showCopySuccessTip(settingsStore.t('downloaded'))
  } catch (err) {
    console.error('Download failed:', err)
  }
}

const exportAsCurl = async () => {
  try {
    await navigator.clipboard.writeText(generateCurlCommand())
    showCopySuccessTip(settingsStore.t('queryExported'))
  } catch (err) {
    console.error('Copy failed:', err)
  }
}

const exportAsPostman = async () => {
  try {
    const collection = generatePostmanCollection()
    const blob = new Blob([JSON.stringify(collection, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `meilisearch-${selectedIndex.value}-search.postman_collection.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    showCopySuccessTip(settingsStore.t('exported'))
  } catch (err) {
    console.error('Export failed:', err)
  }
}

const applyFilters = () => {
  // Always trigger search, even with empty conditions
  // This allows clearing filters when no valid conditions exist
  performSearch()
}

const fetchIndexes = async () => {
  try {
    const result = await indexApi.getAll(projectId.value)
    indexes.value = result.data || []
    
    if (route.query.index) {
      selectedIndex.value = route.query.index
      onIndexChange()
    }
  } catch (err) {
    console.error('Failed to fetch indexes:', err)
  }
}

const onIndexChange = async () => {
  if (!selectedIndex.value) {
    sortableAttributes.value = []
    filterableAttributes.value = []
    displayedAttributes.value = []
    results.value = null
    allColumns.value = []
    selectedColumns.value = []
    embeddersConfig.value = null
    availableEmbedders.value = []
    selectedEmbedder.value = ''
    enableVectorSearch.value = false
    // Reset filter conditions and selections
    filterConditions.value = [{ attribute: '', operator: '', value: '' }]
    Object.keys(filters).forEach(key => delete filters[key])
    return
  }

  // Reset columns and filters when switching index
  allColumns.value = []
  selectedColumns.value = []
  filterConditions.value = [{ attribute: '', operator: '', value: '' }]
  Object.keys(filters).forEach(key => delete filters[key])
  embeddersConfig.value = null
  availableEmbedders.value = []
  selectedEmbedder.value = ''
  enableVectorSearch.value = false

  try {
    // Fetch general settings
    const settings = await indexApi.getSettings(projectId.value, selectedIndex.value)
    if (settings.success && settings.data) {
      currentSettings.value = settings.data
      sortableAttributes.value = settings.data.sortableAttributes || []
      const fa = settings.data.filterableAttributes || []
      filterableAttributes.value = fa.map(item => {
        if (typeof item === 'string') return { name: item, mode: 'equality' }
        if (item.attributePatterns) return { name: item.attributePatterns[0], mode: 'equality' }
        return item
      }).filter(Boolean)
      displayedAttributes.value = settings.data.displayedAttributes || ['*']
    }
    
    // Check embedders configuration from settings
    if (settings.data && settings.data.embedders) {
      embeddersConfig.value = settings.data.embedders
      availableEmbedders.value = Object.keys(settings.data.embedders)
      if (availableEmbedders.value.length > 0 && !selectedEmbedder.value) {
        selectedEmbedder.value = availableEmbedders.value[0]
      }
    } else {
      embeddersConfig.value = null
      availableEmbedders.value = []
      selectedEmbedder.value = ''
      console.debug('Embedders not configured for this index')
    }
    
    performSearch()
  } catch (err) {
    console.error('Failed to fetch settings:', err)
  }
}

const performSearch = async () => {
  if (!selectedIndex.value) return
  loading.value = true
  try {
    const params = { 
      limit: 20, 
      showRankingScore: true,
      showRankingScoreDetails: true
    }
    
    if (sortBy.value) {
      params.sort = [sortBy.value]
    }

    // Build filter expression from conditions
    const filterExpression = buildFilterExpression()
    if (filterExpression) {
      params.filter = filterExpression
    }

    // Add vector search parameters
    if (enableVectorSearch.value && searchQuery.value && hasEmbeddersConfig.value) {
      params.hybrid = {
        semanticRatio: parseFloat(semanticRatio.value)
      }
      if (selectedEmbedder.value) {
        params.hybrid.embedder = selectedEmbedder.value
      }
    }

    const result = await indexApi.search(projectId.value, selectedIndex.value, searchQuery.value, params)
    results.value = result.data
    
    if (result.data?.hits?.length > 0) {
      const newColumns = Object.keys(result.data.hits[0]).filter(k => !k.startsWith('_'))
      allColumns.value = newColumns
      // Only auto-select columns if none are currently selected
      if (selectedColumns.value.length === 0) {
        selectedColumns.value = newColumns.slice(0, 6)
      } else {
        // Filter out columns that no longer exist in the new data
        selectedColumns.value = selectedColumns.value.filter(col => newColumns.includes(col))
        // If all previously selected columns were removed, select first 6
        if (selectedColumns.value.length === 0) {
          selectedColumns.value = newColumns.slice(0, 6)
        }
      }
    }
  } catch (err) {
    console.error('Search failed:', err)
  } finally {
    loading.value = false
  }
}

const cleanHit = (hit) => {
  const clean = { ...hit }
  delete clean._rankingScore
  delete clean._rankingScoreDetails
  return clean
}

// JSON 格式化函数
const formatJsonLines = (obj) => {
  try {
    const jsonString = JSON.stringify(obj, null, 2)
    return jsonString.split('\n')
  } catch (error) {
    return [String(obj)]
  }
}

// JSON 行样式函数
const getLineStyle = (line) => {
  const trimmed = line.trim()
  
  // 对象键名样式
  if (trimmed.endsWith(':')) {
    return 'color: #9cdcfe;'
  }
  
  // 字符串值样式
  if ((trimmed.startsWith('"') && trimmed.endsWith('"')) || 
      (trimmed.startsWith("'") && trimmed.endsWith("'"))) {
    return 'color: #ce9178;'
  }
  
  // 数字值样式
  if (/^-?\d+(\.\d+)?$/.test(trimmed)) {
    return 'color: #b5cea8;'
  }
  
  // 布尔值和null样式
  if (trimmed === 'true' || trimmed === 'false' || trimmed === 'null') {
    return 'color: #569cd6;'
  }
  
  // 默认样式
  return 'color: #d4d4d4;'
}

const showCopyTip = ref(false)
const copyTipMessage = ref('')
const copyTipPosition = ref({ x: 0, y: 0 })
const copyTipTimeout = ref(null)

const showCopySuccessTip = (message, event) => {
  copyTipMessage.value = message
  
  if (event && event.target) {
    // 获取按钮位置
    const button = event.target.closest('button')
    if (button) {
      const rect = button.getBoundingClientRect()
      copyTipPosition.value = {
        x: rect.left + rect.width / 2,
        y: rect.top - 10
      }
    }
  } else {
    // 如果没有事件，显示在屏幕中央上方
    copyTipPosition.value = {
      x: window.innerWidth / 2,
      y: 100
    }
  }
  
  // 直接显示，避免漂移动画
  showCopyTip.value = true
  
  // 自动隐藏提示
  if (copyTipTimeout.value) {
    clearTimeout(copyTipTimeout.value)
  }
  copyTipTimeout.value = setTimeout(() => {
    showCopyTip.value = false
  }, 2000)
}

const copyJson = async (hit, event) => {
  try {
    await navigator.clipboard.writeText(JSON.stringify(cleanHit(hit), null, 2))
    showCopySuccessTip(settingsStore.t('copySuccess'), event)
  } catch (err) {
    console.error('Copy failed:', err)
  }
}

const editDocument = (hit) => {
  editingDocument.value = hit
  editJson.value = JSON.stringify(cleanHit(hit), null, 2)
  showEditModal.value = true
}

const saveDocument = async () => {
  saving.value = true
  try {
    const doc = JSON.parse(editJson.value)
    await indexApi.addDocuments(projectId.value, selectedIndex.value, [doc])
    showEditModal.value = false
    performSearch()
  } catch (err) {
    console.error('Save failed:', err)
    alert('Invalid JSON or save failed')
  } finally {
    saving.value = false
  }
}

const confirmDeleteDocument = (hit) => {
  documentToDelete.value = hit
  showDeleteModal.value = true
}

const deleteDocument = async () => {
  if (!documentToDelete.value) return
  deleting.value = true
  try {
    const primaryKey = currentSettings.value?.primaryKey || 'id'
    const docId = documentToDelete.value[primaryKey]
    if (docId) {
      await indexApi.deleteDocument(projectId.value, selectedIndex.value, docId)
      showDeleteModal.value = false
      performSearch()
    }
  } catch (err) {
    console.error('Delete failed:', err)
  } finally {
    deleting.value = false
  }
}

const closeColumnSelector = () => {
  showColumnSelector.value = false
}

watch(sortBy, () => {
  if (selectedIndex.value) performSearch()
})

onMounted(() => {
  fetchIndexes()
  document.addEventListener('click', closeColumnSelector)
})

onUnmounted(() => {
  document.removeEventListener('click', closeColumnSelector)
})
</script>