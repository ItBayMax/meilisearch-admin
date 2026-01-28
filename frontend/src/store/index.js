import { defineStore } from 'pinia'
import { indexApi } from '@/api'

export const useIndexStore = defineStore('index', {
  state: () => ({
    indexes: [],
    currentIndex: null,
    settings: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchIndexes(projectId) {
      this.loading = true
      this.error = null
      try {
        const response = await indexApi.getAll(projectId)
        this.indexes = response.data || []
      } catch (err) {
        this.error = err.message
        console.error('Failed to fetch indexes:', err)
      } finally {
        this.loading = false
      }
    },

    async fetchIndex(projectId, uid) {
      this.loading = true
      this.error = null
      try {
        const response = await indexApi.get(projectId, uid)
        this.currentIndex = response.data
        return response.data
      } catch (err) {
        this.error = err.message
        console.error('Failed to fetch index:', err)
        return null
      } finally {
        this.loading = false
      }
    },

    async createIndex(projectId, uid, primaryKey) {
      try {
        const response = await indexApi.create(projectId, uid, primaryKey)
        return response
      } catch (err) {
        console.error('Failed to create index:', err)
        throw err
      }
    },

    async deleteIndex(projectId, uid) {
      try {
        const response = await indexApi.delete(projectId, uid)
        if (response.success) {
          this.indexes = this.indexes.filter(i => i.uid !== uid)
        }
        return response
      } catch (err) {
        console.error('Failed to delete index:', err)
        throw err
      }
    },

    async fetchSettings(projectId, uid) {
      try {
        const response = await indexApi.getSettings(projectId, uid)
        this.settings = response.data
        return response.data
      } catch (err) {
        console.error('Failed to fetch settings:', err)
        throw err
      }
    },

    async updateSettings(projectId, uid, settings) {
      try {
        const response = await indexApi.updateSettings(projectId, uid, settings)
        return response
      } catch (err) {
        console.error('Failed to update settings:', err)
        throw err
      }
    },

    clearCurrentIndex() {
      this.currentIndex = null
      this.settings = null
    },
  },
})
