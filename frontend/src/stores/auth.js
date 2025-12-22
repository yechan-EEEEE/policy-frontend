import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLogin: false,
    user: null,
    token: null
  }),

  actions: {
    signup(userData) {
        this.user = userData
        this.token = null
        this.isLogin = true

        localStorage.setItem(
        'auth',
        JSON.stringify({
            user: userData,
            token: null
        })
        )
    },

    login({ user, token }) {
    if (!user || !user.username) {
        console.warn('로그인 실패: 유효하지 않은 사용자')
        return
    }

    this.user = user
    this.token = token
    this.isLogin = true

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
    if (!saved) return

    const { user, token } = JSON.parse(saved)

    if (!user || !user.username) {
        localStorage.removeItem('auth')
        return
    }

    this.user = user
    this.token = token
    this.isLogin = true
    }
    }

})
