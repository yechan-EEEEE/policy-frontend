import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useThreadStore = defineStore('thread', {
  state: () => ({
    threads: [],
    threadDetail: null,
  }),

  getters: {
    getById: (state) => (id) => {
      return state.threads.find(t => String(t.id) === String(id))
    },
  },

  actions: {
    /** 전체 스레드 목록 */
    async fetchThreads(params = {}) {
      const res = await api.get('/community/threads/', { params })
      this.threads = res.data
    },

    /** 특정 정책의 스레드 목록 */
    async fetchThreadsByPolicy(plcyNo) {
      const res = await api.get(`/community/policies/${plcyNo}/threads/`)
      this.threads = res.data
    },

    /** 스레드 상세 */
    async fetchThreadDetail(threadId) {
      const res = await api.get(`/community/threads/${threadId}/`)
      this.threadDetail = res.data
    },

    /** 스레드 생성 */
    async createThread(payload) {
      /**
       * payload: { title, content, policy }
       * policy === plcyNo
       */
      const res = await api.post('/community/threads/', payload)
      return res.data
    },

    /** 좋아요 토글 */
    async toggleLike(threadId) {
      const res = await api.post(`/community/threads/${threadId}/like/`)
      return res.data
    },

    /** 스레드 수정 */
    async updateThread(threadId, payload) {
      const res = await api.put(`/community/threads/${threadId}/`, payload)
      return res.data
    },

    /** 스레드 삭제 */
    async deleteThread(threadId) {
      await api.delete(`/community/threads/${threadId}/`)
      this.threads = this.threads.filter(t => t.id !== threadId)
    },
  },
})
