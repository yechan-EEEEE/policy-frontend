import { defineStore } from 'pinia'
import api from '@/api/axios'

export const usePolicyStore = defineStore('policy', {
  state: () => ({
    policies: [],
    policyDetail: null,
    isLoaded: false,
  }),

  getters: {
    getByPlcyNo: (state) => (plcyNo) =>
      state.policies.find(p => String(p.plcyNo) === String(plcyNo)),

    categories: (state) =>
      [...new Set(state.policies.map(p => p.lclsfNm).filter(Boolean))],

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
  },

  actions: {
    async fetchPolicies(params = {}) {
      const res = await api.get('/policies/list/', { params })
      this.policies = res.data
      this.isLoaded = true
    },

    async fetchPolicyDetail(plcyNo) {
      const res = await api.get(`/policies/${plcyNo}/`)
      this.policyDetail = res.data
    },

    async toggleLike(plcyNo) {
      return (await api.post(`/policies/${plcyNo}/like/`)).data
    },

    async fetchRecommendPolicies() {
      return (await api.get('/policies/recommend/ai/')).data
    },

    async summarizePolicy(plcyNo) {
      return (await api.post(`/policies/${plcyNo}/summarize/`)).data
    },
  },
})
