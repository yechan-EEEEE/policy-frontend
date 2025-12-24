import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useCommentStore = defineStore('comment', {
  state: () => ({
    comments: [],
  }),

  actions: {
    async fetchComments(postId) {
      const res = await api.get(`/community/posts/${postId}/comments/`)
      this.comments = res.data
    },

    async createComment(postId, content) {
      const res = await api.post(
        `/community/posts/${postId}/comments/`,
        { content }
      )
      this.comments.unshift(res.data)
    },

    async updateComment(commentId, content) {
      const res = await api.put(
        `/community/comments/${commentId}/`,
        { content }
      )
      const idx = this.comments.findIndex(c => c.id === commentId)
      if (idx !== -1) this.comments[idx] = res.data
    },

    async deleteComment(commentId) {
      await api.delete(`/community/comments/${commentId}/`)
      this.comments = this.comments.filter(c => c.id !== commentId)
    },

    async toggleLike(commentId) {
      const res = await api.post(`/community/comments/${commentId}/like/`)
      const c = this.comments.find(c => c.id === commentId)
      if (c) {
        c.is_liked = res.data.is_liked
        c.liked_count += res.data.is_liked ? 1 : -1
      }
    },
  },
})
