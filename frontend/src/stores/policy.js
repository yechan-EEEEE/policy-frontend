import { defineStore } from 'pinia'
import api from '@/api/axios'

export const usePolicyStore = defineStore('policy', {
  state: () => ({
    policies: [],
    policyDetail: null,
    isLoaded: false,
  }),

  getters: {
    getByPlcyNo: (state) => (plcyNo) => {
      return state.policies.find(
        p => String(p.plcyNo) === String(plcyNo)
      )
    },

    categories: (state) => {
      return [...new Set(state.policies.map(p => p.lclsfNm).filter(Boolean))]
    },

    subCategories: (state) => (category) => {
      if (!category) return []
      return [
        ...new Set(
          state.policies
            .filter(p => p.lclsfNm === category)
            .map(p => p.mclsfNm)
            .filter(Boolean)
        )
      ]
    },

    getById: (state) => (id) =>
    state.policies.find(p => p.id === id),    
  },

  actions: {
    /** 정책 목록 조회 */
    async fetchPolicies(params = {}) {
      const res = await api.get('/policies/', { params })
      this.policies = res.data
      this.isLoaded = true
    },

    /** 정책 상세 조회 */
    async fetchPolicyDetail(plcyNo) {
      const res = await api.get(`/policies/${plcyNo}/`)
      this.policyDetail = res.data
    },

    /** 정책 좋아요 */
    async toggleLike(plcyNo) {
      const res = await api.post(`/policies/${plcyNo}/like/`)
      return res.data
    },

    /** 정책 추천 */
    async fetchRecommendPolicies() {
      const res = await api.get('/policies/recommend/')
      return res.data
    },

    /** 정책 요약 (AI) */
    async summarizePolicy(plcyNo) {
      const res = await api.get(`/policies/${plcyNo}/summarize/`)
      return res.data
    },
  },
})
