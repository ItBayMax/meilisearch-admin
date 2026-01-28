import api from './http'

export const projectApi = {
  // Get all projects
  getAll(includeInactive = false) {
    return api.get('/projects', { params: { include_inactive: includeInactive } })
  },

  // Get single project
  get(id) {
    return api.get(`/projects/${id}`)
  },

  // Create project
  create(data) {
    return api.post('/projects', data)
  },

  // Update project
  update(id, data) {
    return api.put(`/projects/${id}`, data)
  },

  // Delete project
  delete(id, hard = false) {
    return api.delete(`/projects/${id}`, { params: { hard } })
  },

  // Test connection
  testConnection(url, apiKey) {
    return api.post('/projects/test-connection', { url, api_key: apiKey })
  },

  // Get project stats
  getStats(id) {
    return api.get(`/projects/${id}/stats`)
  },
}

export const indexApi = {
  // Get all indexes
  getAll(projectId) {
    return api.get(`/projects/${projectId}/indexes`)
  },

  // Get single index
  get(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}`)
  },

  // Create index
  create(projectId, uid, primaryKey) {
    return api.post(`/projects/${projectId}/indexes`, { uid, primaryKey })
  },

  // Delete index
  delete(projectId, uid) {
    return api.delete(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}`)
  },

  // Get index stats
  getStats(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/stats`)
  },

  // Documents
  getDocuments(projectId, uid, params = {}) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/documents`, { params })
  },

  addDocuments(projectId, uid, documents, primaryKey) {
    return api.post(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/documents`, { documents, primaryKey })
  },

  deleteDocument(projectId, uid, docId) {
    return api.delete(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/documents/${encodeURIComponent(docId)}`)
  },

  deleteAllDocuments(projectId, uid) {
    return api.delete(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/documents`)
  },

  // Search
  search(projectId, uid, query, params = {}) {
    return api.post(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/search`, { q: query, ...params })
  },

  // Settings
  getSettings(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings`)
  },

  updateSettings(projectId, uid, settings) {
    return api.patch(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings`, settings)
  },

  resetSettings(projectId, uid) {
    return api.delete(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings`)
  },

  // Individual settings
  getSearchableAttributes(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/searchable-attributes`)
  },

  updateSearchableAttributes(projectId, uid, attrs) {
    return api.put(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/searchable-attributes`, attrs)
  },

  getDisplayedAttributes(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/displayed-attributes`)
  },

  updateDisplayedAttributes(projectId, uid, attrs) {
    return api.put(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/displayed-attributes`, attrs)
  },

  getFilterableAttributes(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/filterable-attributes`)
  },

  updateFilterableAttributes(projectId, uid, attrs) {
    return api.put(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/filterable-attributes`, attrs)
  },

  getSortableAttributes(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/sortable-attributes`)
  },

  updateSortableAttributes(projectId, uid, attrs) {
    return api.put(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/sortable-attributes`, attrs)
  },

  getRankingRules(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/ranking-rules`)
  },

  updateRankingRules(projectId, uid, rules) {
    return api.put(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/ranking-rules`, rules)
  },

  getSynonyms(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/synonyms`)
  },

  updateSynonyms(projectId, uid, synonyms) {
    return api.put(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/synonyms`, synonyms)
  },

  getStopWords(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/stop-words`)
  },

  updateStopWords(projectId, uid, words) {
    return api.put(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/stop-words`, words)
  },

  getTypoTolerance(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/typo-tolerance`)
  },

  updateTypoTolerance(projectId, uid, config) {
    return api.patch(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/typo-tolerance`, config)
  },

  getPagination(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/pagination`)
  },

  updatePagination(projectId, uid, config) {
    return api.patch(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/pagination`, config)
  },

  getFaceting(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/faceting`)
  },

  updateFaceting(projectId, uid, config) {
    return api.patch(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/faceting`, config)
  },

  getDictionary(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/dictionary`)
  },

  updateDictionary(projectId, uid, words) {
    return api.put(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/dictionary`, words)
  },

  getSeparatorTokens(projectId, uid) {
    return api.get(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/separator-tokens`)
  },

  updateSeparatorTokens(projectId, uid, tokens) {
    return api.put(`/projects/${projectId}/indexes/${encodeURIComponent(uid)}/settings/separator-tokens`, tokens)
  },
}

export const taskApi = {
  // Get tasks
  getAll(projectId, params = {}) {
    return api.get(`/projects/${projectId}/tasks`, { params })
  },

  // Get single task
  get(projectId, taskUid) {
    return api.get(`/projects/${projectId}/tasks/${taskUid}`)
  },

  // Cancel tasks
  cancel(projectId, filters) {
    return api.post(`/projects/${projectId}/tasks/cancel`, filters)
  },

  // Delete tasks
  delete(projectId, filters) {
    return api.delete(`/projects/${projectId}/tasks`, { data: filters })
  },

  // Wait for task
  wait(projectId, taskUid, timeout = 5000) {
    return api.post(`/projects/${projectId}/tasks/${taskUid}/wait`, { timeout })
  },
}

export const keyApi = {
  // Get all keys
  getAll(projectId) {
    return api.get(`/projects/${projectId}/keys`)
  },

  // Get single key
  get(projectId, key) {
    return api.get(`/projects/${projectId}/keys/${key}`)
  },

  // Create key
  create(projectId, data) {
    return api.post(`/projects/${projectId}/keys`, data)
  },

  // Update key
  update(projectId, key, data) {
    return api.patch(`/projects/${projectId}/keys/${key}`, data)
  },

  // Delete key
  delete(projectId, key) {
    return api.delete(`/projects/${projectId}/keys/${key}`)
  },
}
