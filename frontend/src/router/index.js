import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('@/views/Projects.vue'),
  },
  {
    path: '/projects/:id',
    name: 'ProjectDetail',
    component: () => import('@/views/ProjectDetail.vue'),
    children: [
      {
        path: '',
        name: 'ProjectIndexes',
        component: () => import('@/views/project/Indexes.vue'),
      },
      {
        path: 'tasks',
        name: 'ProjectTasks',
        component: () => import('@/views/project/Tasks.vue'),
      },
      {
        path: 'settings',
        name: 'ProjectSettings',
        component: () => import('@/views/project/Settings.vue'),
      },
      {
        path: 'keys',
        name: 'ProjectKeys',
        component: () => import('@/views/project/Keys.vue'),
      },
      {
        path: 'search',
        name: 'ProjectSearch',
        component: () => import('@/views/project/Search.vue'),
      },
    ],
  },
  {
    path: '/projects/:projectId/indexes/:indexId',
    name: 'IndexDetail',
    component: () => import('@/views/IndexDetail.vue'),
    children: [
      {
        path: '',
        name: 'IndexGeneral',
        component: () => import('@/views/index/General.vue'),
      },
      {
        path: 'attributes',
        name: 'IndexAttributes',
        component: () => import('@/views/index/Attributes.vue'),
      },
      {
        path: 'ranking-rules',
        name: 'IndexRankingRules',
        component: () => import('@/views/index/RankingRules.vue'),
      },
      {
        path: 'synonyms',
        name: 'IndexSynonyms',
        component: () => import('@/views/index/Synonyms.vue'),
      },
      {
        path: 'typo-tolerance',
        name: 'IndexTypoTolerance',
        component: () => import('@/views/index/TypoTolerance.vue'),
      },
      {
        path: 'prefix-search',
        name: 'IndexPrefixSearch',
        component: () => import('@/views/index/PrefixSearch.vue'),
      },
      {
        path: 'stop-words',
        name: 'IndexStopWords',
        component: () => import('@/views/index/StopWords.vue'),
      },
      {
        path: 'separators',
        name: 'IndexSeparators',
        component: () => import('@/views/index/Separators.vue'),
      },
      {
        path: 'dictionary',
        name: 'IndexDictionary',
        component: () => import('@/views/index/Dictionary.vue'),
      },
      {
        path: 'pagination',
        name: 'IndexPagination',
        component: () => import('@/views/index/Pagination.vue'),
      },
      {
        path: 'faceting',
        name: 'IndexFaceting',
        component: () => import('@/views/index/Faceting.vue'),
      },
      {
        path: 'search-cutoff',
        name: 'IndexSearchCutoff',
        component: () => import('@/views/index/SearchCutoff.vue'),
      },
      {
        path: 'embedders',
        name: 'IndexEmbedders',
        component: () => import('@/views/index/Embedders.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
