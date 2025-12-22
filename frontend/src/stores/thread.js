import { defineStore } from 'pinia'
import axios from 'axios'

export const useThreadStore = defineStore('thread', {
  state: () => ({
    threads: [],
  }),

  getters: {
    getById: (state) => (id) => {
      return state.threads.find(t => String(t.id) === String(id))
    },
  },

  actions: {
    async loadThreads() {
      const res = await axios.get('/api/threads/')

      // 🔥 백엔드 데이터 → 프론트용으로 정규화
      this.threads = Array.isArray(res.data)
        ? res.data.map(t => ({
            id: t.pk,
            title: t.fields.title,
            content: t.fields.content,
            author: t.fields.author,
            created_at: t.fields.created_at,
            updated_at: t.fields.updated_at,
            view_count: t.fields.view_count ?? 0,
            liked_users: t.fields.liked_users ?? [],
          }))
        : []
    },

    async createThread(payload) {
      /**
       * payload: { title, content, policy }
       */

      // 🔸 mock 생성 (HomeView 기준 필드 맞춤)
      const newThread = {
        id: Date.now(),
        title: payload.title,
        content: payload.content,
        author: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        view_count: 0,
        liked_users: [],
        policy: {
          pk: payload.policy,
        },
      }

      this.threads.unshift(newThread)

      // 🔸 나중에 API 연동 시
      // const res = await axios.post('/api/threads/', payload)
      // this.threads.unshift(normalize(res.data))
    },
  },
})
