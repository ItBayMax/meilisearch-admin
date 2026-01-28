<template>
  <header class="h-16 bg-dark-900 border-b border-dark-700 flex items-center justify-between px-6">
    <!-- Breadcrumb -->
    <div class="flex items-center space-x-2 text-sm">
      <router-link to="/" class="text-gray-400 hover:text-white transition-colors">
        {{ settingsStore.t('home') }}
      </router-link>
      <template v-for="(crumb, index) in breadcrumbs" :key="index">
        <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <router-link
          v-if="crumb.path"
          :to="crumb.path"
          class="text-gray-400 hover:text-white transition-colors"
        >
          {{ crumb.name }}
        </router-link>
        <span v-else class="text-white">{{ crumb.name }}</span>
      </template>
    </div>

    <!-- Actions -->
    <div class="flex items-center space-x-3">
      <!-- Language Switcher -->
      <div class="relative">
        <button
          @click="showLangMenu = !showLangMenu"
          class="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-dark-800 hover:bg-dark-700 text-gray-300 text-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
          </svg>
          <span>{{ settingsStore.currentLanguage === 'en' ? 'EN English' : 'ZH 中文' }}</span>
        </button>
        <div
          v-if="showLangMenu"
          class="absolute right-0 top-full mt-1 bg-dark-800 rounded-lg shadow-lg border border-dark-600 py-1 z-50 min-w-[100px]"
        >
          <button
            @click="setLanguage('en')"
            class="w-full px-4 py-2 text-left text-sm hover:bg-dark-700 transition-colors"
            :class="settingsStore.currentLanguage === 'en' ? 'text-primary-400' : 'text-gray-300'"
          >
            English
          </button>
          <button
            @click="setLanguage('zh')"
            class="w-full px-4 py-2 text-left text-sm hover:bg-dark-700 transition-colors"
            :class="settingsStore.currentLanguage === 'zh' ? 'text-primary-400' : 'text-gray-300'"
          >
            中文
          </button>
        </div>
      </div>

      <!-- Theme Switcher -->
      <div class="relative">
        <button
          @click="showThemeMenu = !showThemeMenu"
          class="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-dark-800 hover:bg-dark-700 text-gray-300 text-sm transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
          </svg>
          <span class="w-3 h-3 rounded-full" :class="themeColorClass"></span>
        </button>
        <div
          v-if="showThemeMenu"
          class="absolute right-0 top-full mt-1 bg-dark-800 rounded-lg shadow-lg border border-dark-600 py-1 z-50 min-w-[120px]"
        >
          <button
            v-for="theme in themes"
            :key="theme.value"
            @click="setTheme(theme.value)"
            class="w-full px-4 py-2 text-left text-sm hover:bg-dark-700 transition-colors flex items-center space-x-2"
            :class="settingsStore.currentTheme === theme.value ? 'text-primary-400' : 'text-gray-300'"
          >
            <span class="w-3 h-3 rounded-full" :class="theme.colorClass"></span>
            <span>{{ theme.label }}</span>
          </button>
        </div>
      </div>

      <!-- Notification -->
      <button class="btn-ghost p-2 rounded-lg">
        <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
      </button>
      
      <!-- Avatar -->
      <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-indigo-500 rounded-full flex items-center justify-center">
        <span class="text-white text-sm font-medium">A</span>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProjectStore } from '@/store/project'
import { useSettingsStore } from '@/store/settings'

const route = useRoute()
const projectStore = useProjectStore()
const settingsStore = useSettingsStore()

const showLangMenu = ref(false)
const showThemeMenu = ref(false)

const themes = computed(() => [
  { value: 'tech', label: settingsStore.t('themeTech'), colorClass: 'bg-sky-500' },
  { value: 'pink', label: settingsStore.t('themePink'), colorClass: 'bg-pink-500' },
  { value: 'dark', label: settingsStore.t('themeDark'), colorClass: 'bg-gray-800 border border-gray-600' },
  { value: 'light', label: settingsStore.t('themeLight'), colorClass: 'bg-white border border-gray-300' },
])

const themeColorClass = computed(() => {
  const theme = themes.value.find(t => t.value === settingsStore.currentTheme)
  return theme?.colorClass || 'bg-sky-500'
})

const setLanguage = (lang) => {
  settingsStore.setLanguage(lang)
  showLangMenu.value = false
}

const setTheme = (theme) => {
  settingsStore.setTheme(theme)
  showThemeMenu.value = false
}

const closeMenus = (e) => {
  if (!e.target.closest('.relative')) {
    showLangMenu.value = false
    showThemeMenu.value = false
  }
}

const breadcrumbs = computed(() => {
  const crumbs = []
  const path = route.path

  if (path.startsWith('/projects')) {
    crumbs.push({ name: settingsStore.t('projects'), path: '/projects' })

    if (route.params.id) {
      const project = projectStore.currentProject
      crumbs.push({
        name: project?.name || `${settingsStore.t('projects')} ${route.params.id}`,
        path: `/projects/${route.params.id}`
      })

      if (route.name === 'ProjectTasks') {
        crumbs.push({ name: settingsStore.t('tasks') })
      } else if (route.name === 'ProjectSettings') {
        crumbs.push({ name: settingsStore.t('settings') })
      } else if (route.name === 'ProjectKeys') {
        crumbs.push({ name: settingsStore.t('keys') })
      } else if (route.name === 'ProjectSearch') {
        crumbs.push({ name: settingsStore.t('searchPreview') })
      }
    }

    if (route.params.indexId) {
      crumbs.push({
        name: route.params.indexId,
        path: `/projects/${route.params.projectId}/indexes/${route.params.indexId}`
      })
    }
  }

  return crumbs
})

onMounted(() => {
  settingsStore.initTheme()
  document.addEventListener('click', closeMenus)
})

onUnmounted(() => {
  document.removeEventListener('click', closeMenus)
})
</script>
