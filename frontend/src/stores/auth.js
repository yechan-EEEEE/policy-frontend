import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLogin: false,
    user: null,
    token: null
  }),

  actions: {
    login({ user, token }) {
      this.user = user
      this.token = token
      this.isLogin = true

      // ⭐ localStorage 저장
      localStorage.setItem('auth', JSON.stringify({
        user,
        token
      }))
    },

    logout() {
      this.user = null
      this.token = null
      this.isLogin = false
      localStorage.removeItem('auth')
    },

    loadAuth() {
      const saved = localStorage.getItem('auth')
      if (saved) {
        const { user, token } = JSON.parse(saved)
        this.user = user
        this.token = token
        this.isLogin = true
      }
    }
  }
})
