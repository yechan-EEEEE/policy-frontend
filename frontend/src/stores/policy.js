import { defineStore } from 'pinia'
import policiesData from '@/assets/data/edit_policies.json' 
// ↑ 임시 mock 데이터 (나중에 API로 교체)

export const usePolicyStore = defineStore('policy', {
  state: () => ({
    policies: [],
    isLoaded: false,
  }),

  getters: {
    /**
     * 정책 PK로 단일 정책 조회
     */
    getById: (state) => (policyId) => {
      return state.policies.find(p => p.pk === policyId)
    },

    /**
     * 전체 대분류 목록 (중복 제거)
     */
    categories: (state) => {
      return [...new Set(state.policies.map(p => p.category))]
    },

    /**
     * 특정 대분류에 해당하는 소분류 목록
     */
    subCategories: (state) => (category) => {
      if (!category) return []
      return [
        ...new Set(
          state.policies
            .filter(p => p.category === category)
            .map(p => p.subTitle)
        )
      ]
    },
  },

  actions: {
    /**
     * 정책 데이터 로드 (mock → API 교체 예정)
     */
    loadPolicies() {
      if (this.isLoaded) return

      this.policies = (policiesData || []).map(p => ({
        pk: p.pk,
        title: p.title,
        description: p.description,
        category: p.category,
        subTitle: p.subTitle,

        // 지원 내용
        plcySprtCn: p.plcySprtCn,

        // 연령 조건
        sprtTrgtMinAge: Number(p.sprtTrgtMinAge) || null,
        sprtTrgtMaxAge: Number(p.sprtTrgtMaxAge) || null,
        sprtTrgtAgeLmtYn: p.sprtTrgtAgeLmtYn,

        // 신청 기간
        aplyYmd: p.aplyYmd,

        // 기관
        publisher: p.publisher,

        // 게시 날짜
        pub_date: p.pub_date,
      }))

      this.isLoaded = true
    },

    /**
     * 🔮 (나중에 API 붙을 때)
     * async fetchPolicies() {}
     */
  },
})
