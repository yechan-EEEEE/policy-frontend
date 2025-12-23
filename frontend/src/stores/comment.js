import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useCommentStore = defineStore('comment', {
  state: () => ({
    comments: [],
  }),

  actions: {
    // 댓글 목록 조회
    async fetchComments(threadId) {
      const res = await api.get(`/community/threads/${threadId}/comments/`)
      this.comments = res.data
    },

    // 댓글 작성
    async createComment(threadId, content) {
      const res = await api.post(
        `/community/threads/${threadId}/comments/`,
        { content }
      )
      this.comments.unshift(res.data)
    },

    // 댓글 수정
    async updateComment(commentId, content) {
        const res = await api.put(
            `/community/comments/${commentId}/`,
            { content }
        )

        const idx = this.comments.findIndex(c => c.id === commentId)
        if (idx !== -1) {
            this.comments[idx] = res.data
        }
    },

    // 댓글 삭제
    async deleteComment(commentId) {
      await api.delete(`/community/comments/${commentId}/`)
      this.comments = this.comments.filter(c => c.id !== commentId)
    },

    // 댓글 좋아요 토글
    async toggleLike(commentId) {
      const res = await api.post(
        `/community/comments/${commentId}/like/`
      )

      const comment = this.comments.find(c => c.id === commentId)
      if (comment) {
        comment.is_liked = res.data.is_liked
        comment.liked_count += res.data.is_liked ? 1 : -1
      }
    },
  },
})
