import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLogin: false,
    user: null,
    token: null
  }),

  actions: {
    signup(userData) {
      // Mock 단계: 서버 없이 바로 로그인 처리
      this.user = userData
      this.isLogin = true
    },

    login({ user, token }) {
      this.user = user
      this.token = token
      this.isLogin = true
    },

    logout() {
      this.user = null
      this.token = null
      this.isLogin = false
    }
  }
})
