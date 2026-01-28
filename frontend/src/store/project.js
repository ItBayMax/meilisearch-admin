import { defineStore } from 'pinia'
import { projectApi } from '@/api'

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [],
    currentProject: null,
    loading: false,
    error: null,
  }),

  getters: {
    getProjectById: (state) => (id) => {
      return state.projects.find(p => p.id === parseInt(id))
    },
  },

  actions: {
    async fetchProjects() {
      this.loading = true
      this.error = null
      try {
        const response = await projectApi.getAll()
        this.projects = response.data || []
      } catch (err) {
        this.error = err.message
        console.error('Failed to fetch projects:', err)
      } finally {
        this.loading = false
      }
    },

    async fetchProject(id) {
      this.loading = true
      this.error = null
      try {
        const response = await projectApi.get(id)
        this.currentProject = response.data
        return response.data
      } catch (err) {
        this.error = err.message
        console.error('Failed to fetch project:', err)
        return null
      } finally {
        this.loading = false
      }
    },

    async createProject(data) {
      try {
        const response = await projectApi.create(data)
        if (response.success) {
          this.projects.unshift(response.data)
        }
        return response
      } catch (err) {
        console.error('Failed to create project:', err)
        throw err
      }
    },

    async updateProject(id, data) {
      try {
        const response = await projectApi.update(id, data)
        if (response.success) {
          const index = this.projects.findIndex(p => p.id === id)
          if (index !== -1) {
            this.projects[index] = response.data
          }
          if (this.currentProject?.id === id) {
            this.currentProject = response.data
          }
        }
        return response
      } catch (err) {
        console.error('Failed to update project:', err)
        throw err
      }
    },

    async deleteProject(id) {
      try {
        const response = await projectApi.delete(id)
        if (response.success) {
          this.projects = this.projects.filter(p => p.id !== id)
          if (this.currentProject?.id === id) {
            this.currentProject = null
          }
        }
        return response
      } catch (err) {
        console.error('Failed to delete project:', err)
        throw err
      }
    },

    setCurrentProject(project) {
      this.currentProject = project
    },

    clearCurrentProject() {
      this.currentProject = null
    },
  },
})
