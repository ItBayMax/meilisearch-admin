<template>
  <div class="space-y-6">
    <!-- Filters -->
    <div class="flex flex-wrap items-center gap-4">
      <!-- Status Filter -->
      <div class="relative">
        <button
          @click="showStatusFilter = !showStatusFilter"
          class="btn btn-secondary flex items-center space-x-2"
        >
          <span>{{ settingsStore.t('status') }}</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div
          v-if="showStatusFilter"
          class="absolute top-full mt-2 left-0 bg-dark-800 rounded-lg shadow-lg border border-dark-600 py-2 z-10 min-w-[150px]"
        >
          <label
            v-for="status in statusOptions"
            :key="status"
            class="flex items-center px-4 py-2 hover:bg-dark-700 cursor-pointer"
          >
            <input
              type="checkbox"
              :value="status"
              v-model="filters.statuses"
              class="mr-2"
            />
            <span class="text-sm text-gray-300">{{ status }}</span>
          </label>
        </div>
      </div>

      <!-- Type Filter -->
      <div class="relative">
        <button
          @click="showTypeFilter = !showTypeFilter"
          class="btn btn-secondary flex items-center space-x-2"
        >
          <span>{{ settingsStore.t('type') }}</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div
          v-if="showTypeFilter"
          class="absolute top-full mt-2 left-0 bg-dark-800 rounded-lg shadow-lg border border-dark-600 py-2 z-10 min-w-[200px] max-h-[300px] overflow-y-auto"
        >
          <label
            v-for="type in typeOptions"
            :key="type"
            class="flex items-center px-4 py-2 hover:bg-dark-700 cursor-pointer"
          >
            <input
              type="checkbox"
              :value="type"
              v-model="filters.types"
              class="mr-2"
            />
            <span class="text-sm text-gray-300">{{ type }}</span>
          </label>
        </div>
      </div>

      <!-- Index Filter -->
      <div class="relative">
        <button
          @click="showIndexFilter = !showIndexFilter"
          class="btn btn-secondary flex items-center space-x-2"
        >
          <span>{{ settingsStore.t('index') }}</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div
          v-if="showIndexFilter"
          class="absolute top-full mt-2 left-0 bg-dark-800 rounded-lg shadow-lg border border-dark-600 py-2 z-10 min-w-[150px]"
        >
          <label
            v-for="idx in availableIndexes"
            :key="idx"
            class="flex items-center px-4 py-2 hover:bg-dark-700 cursor-pointer"
          >
            <input
              type="checkbox"
              :value="idx"
              v-model="filters.indexUids"
              class="mr-2"
            />
            <span class="text-sm text-gray-300">{{ idx }}</span>
          </label>
        </div>
      </div>

      <button @click="applyFilters" class="btn btn-primary">{{ settingsStore.t('applyFilters') }}</button>
      <button @click="resetFilters" class="btn btn-ghost">{{ settingsStore.t('reset') }}</button>
    </div>

    <!-- Loading -->
    <Loading v-if="loading" />

    <!-- Tasks Table -->
    <div v-else class="card overflow-hidden">
      <table class="w-full">
        <thead class="bg-dark-800">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">{{ settingsStore.t('status') }}</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">{{ settingsStore.t('type') }}</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">{{ settingsStore.t('index') }}</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">{{ settingsStore.t('uid') }}</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">{{ settingsStore.t('duration') }}</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">{{ settingsStore.t('date') }}</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase">{{ settingsStore.t('actions') }}</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-dark-700">
          <tr
            v-for="task in tasks"
            :key="task.uid"
            class="hover:bg-dark-800/50 cursor-pointer"
            @click="showTaskDetail(task)"
          >
            <td class="px-4 py-3">
              <span :class="getStatusBadgeClass(task.status)">{{ task.status }}</span>
            </td>
            <td class="px-4 py-3 text-gray-300 text-sm">{{ task.type }}</td>
            <td class="px-4 py-3 text-gray-300 text-sm">{{ task.indexUid || '-' }}</td>
            <td class="px-4 py-3 text-gray-400 text-sm font-mono">{{ task.uid }}</td>
            <td class="px-4 py-3 text-gray-400 text-sm">{{ task.duration || '-' }}</td>
            <td class="px-4 py-3 text-gray-400 text-sm">{{ formatDate(task.startedAt || task.enqueuedAt) }}</td>
            <td class="px-4 py-3">
              <button
                v-if="task.status === 'enqueued' || task.status === 'processing'"
                @click.stop="cancelTask(task)"
                class="text-red-400 hover:text-red-300 text-sm"
              >
                {{ settingsStore.t('cancel') }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="tasks.length === 0" class="p-8">
        <Empty :title="settingsStore.t('noTasks')" :description="settingsStore.t('noTasksDesc')" />
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="tasks.length > 0" class="flex items-center justify-between">
      <p class="text-gray-400 text-sm">{{ settingsStore.t('showingTasks').replace('{count}', tasks.length) }}</p>
      <div class="flex space-x-2">
        <button
          @click="loadMore"
          class="btn btn-secondary"
          :disabled="!hasMore"
        >
          {{ settingsStore.t('loadMore') }}
        </button>
      </div>
    </div>

    <!-- Task Detail Modal -->
    <Modal v-model:visible="showDetailModal" :title="settingsStore.t('taskDetails')" size="lg">
      <div v-if="selectedTask" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('uid') }}</label>
            <p class="text-white font-mono">{{ selectedTask.uid }}</p>
          </div>
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('status') }}</label>
            <p><span :class="getStatusBadgeClass(selectedTask.status)">{{ selectedTask.status }}</span></p>
          </div>
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('type') }}</label>
            <p class="text-white">{{ selectedTask.type }}</p>
          </div>
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('index') }}</label>
            <p class="text-white">{{ selectedTask.indexUid || 'N/A' }}</p>
          </div>
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('duration') }}</label>
            <p class="text-white">{{ selectedTask.duration || 'N/A' }}</p>
          </div>
          <div>
            <label class="text-gray-500 text-xs">{{ settingsStore.t('enqueuedAt') }}</label>
            <p class="text-white">{{ formatDate(selectedTask.enqueuedAt) }}</p>
          </div>
        </div>

        <div v-if="selectedTask.error">
          <label class="text-gray-500 text-xs">{{ settingsStore.t('error') }}</label>
          <div class="code-block text-red-400 mt-1">
            <pre>{{ JSON.stringify(selectedTask.error, null, 2) }}</pre>
          </div>
        </div>

        <div>
          <label class="text-gray-500 text-xs">{{ settingsStore.t('fullDetails') }}</label>
          <div class="code-block mt-1">
            <pre class="text-gray-300">{{ JSON.stringify(selectedTask, null, 2) }}</pre>
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted } from 'vue'
import { useSettingsStore } from '@/store/settings'
import { taskApi, indexApi } from '@/api'
import Modal from '@/components/common/Modal.vue'
import Loading from '@/components/common/Loading.vue'
import Empty from '@/components/common/Empty.vue'

const settingsStore = useSettingsStore()
const projectId = inject('projectId')

const tasks = ref([])
const loading = ref(false)
const hasMore = ref(true)
const showDetailModal = ref(false)
const selectedTask = ref(null)

const showStatusFilter = ref(false)
const showTypeFilter = ref(false)
const showIndexFilter = ref(false)

const availableIndexes = ref([])

const statusOptions = ['succeeded', 'failed', 'canceled', 'enqueued', 'processing']
const typeOptions = [
  'indexCreation', 'indexUpdate', 'indexDeletion', 'indexSwap',
  'documentAdditionOrUpdate', 'documentDeletion',
  'settingsUpdate', 'dumpCreation', 'taskCancelation', 'taskDeletion',
  'snapshotCreation'
]

const filters = reactive({
  statuses: [],
  types: [],
  indexUids: [],
  limit: 20,
  from: undefined,
})

const fetchTasks = async (append = false) => {
  loading.value = true
  try {
    const params = { limit: filters.limit }
    if (filters.statuses.length) params.statuses = filters.statuses.join(',')
    if (filters.types.length) params.types = filters.types.join(',')
    if (filters.indexUids.length) params.indexUids = filters.indexUids.join(',')
    if (filters.from !== undefined) params.from = filters.from

    const result = await taskApi.getAll(projectId.value, params)
    const newTasks = result.data?.results || []
    
    if (append) {
      tasks.value = [...tasks.value, ...newTasks]
    } else {
      tasks.value = newTasks
    }
    
    hasMore.value = newTasks.length === filters.limit
    if (newTasks.length > 0) {
      filters.from = newTasks[newTasks.length - 1].uid - 1
    }
  } catch (err) {
    console.error('Failed to fetch tasks:', err)
  } finally {
    loading.value = false
  }
}

const fetchIndexes = async () => {
  try {
    const result = await indexApi.getAll(projectId.value)
    availableIndexes.value = (result.data || []).map(i => i.uid)
  } catch {
    // Ignore
  }
}

const applyFilters = () => {
  filters.from = undefined
  closeAllFilters()
  fetchTasks()
}

const resetFilters = () => {
  filters.statuses = []
  filters.types = []
  filters.indexUids = []
  filters.from = undefined
  closeAllFilters()
  fetchTasks()
}

const loadMore = () => {
  fetchTasks(true)
}

const showTaskDetail = (task) => {
  selectedTask.value = task
  showDetailModal.value = true
}

const cancelTask = async (task) => {
  try {
    await taskApi.cancel(projectId.value, { uids: [task.uid] })
    fetchTasks()
  } catch (err) {
    console.error('Failed to cancel task:', err)
  }
}

const closeAllFilters = () => {
  showStatusFilter.value = false
  showTypeFilter.value = false
  showIndexFilter.value = false
}

const getStatusBadgeClass = (status) => {
  const classes = {
    succeeded: 'badge badge-success',
    failed: 'badge badge-danger',
    canceled: 'badge badge-warning',
    enqueued: 'badge badge-info',
    processing: 'badge badge-info',
  }
  return classes[status] || 'badge'
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  fetchTasks()
  fetchIndexes()
})
</script>
