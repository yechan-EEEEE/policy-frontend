import { defineStore } from 'pinia'
import api from '@/api/axios'   // ⚠️ axios 인스턴스 사용

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLogin: false,
    user: null,
    isFetched: false,
  }),

  actions: {
    // 회원가입
    async signup(userData) {
      await api.post('/accounts/signup/', userData)
      // 회원가입 후 바로 로그인 시도
      await this.login({
        username: userData.username,
        password: userData.password,
      })
    },

    // 로그인
    async login(credentials) {
      const res = await api.post('/accounts/login/', credentials)

      // 백엔드가 user 정보를 내려준다고 가정
      this.user = res.data
      this.isLogin = true
    },

    // 로그아웃
    async logout() {
      await api.post('/accounts/logout/')
      this.user = null
      this.isLogin = false
    },

    // 새로고침 시 로그인 상태 복구
    async fetchUser() {
      try {
        const res = await api.get('/accounts/profile/')
        this.user = res.data
        this.isLogin = true
      } catch {
        this.user = null
        this.isLogin = false
      } finally {
        this.isFetched = true // 🔥 중요
      }
    },

    // 회원 탈퇴
    async clearAuth() {
      this.user = null
      this.isLogin = false
    },
  },
})
