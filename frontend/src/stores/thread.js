import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useThreadStore = defineStore('thread', {
  state: () => ({
    threads: [],
    threadDetail: null,
  }),

  getters: {
    getById: (state) => (id) =>
      state.threads.find(t => String(t.id) === String(id)),
  },

  actions: {
    async fetchThreads(params = {}) {
      const res = await api.get('/community/posts/', { params })
      this.threads = res.data
    },

    async fetchThreadsByPolicy(plcyNo) {
      const res = await api.get('/community/posts/', {
        params: { policy: plcyNo },
      })
      this.threads = res.data
    },

    async fetchThreadDetail(postId) {
      const res = await api.get(`/community/posts/${postId}/`)
      this.threadDetail = res.data
    },

    async createThread(payload) {
      return (await api.post('/community/posts/', payload)).data
    },

    async toggleLike(postId) {
      return (await api.post(`/community/posts/${postId}/like/`)).data
    },

    async updateThread(postId, payload) {
      return (await api.put(`/community/posts/${postId}/`, payload)).data
    },

    async deleteThread(postId) {
      await api.delete(`/community/posts/${postId}/`)
      this.threads = this.threads.filter(t => t.id !== postId)
    },
  },
})
