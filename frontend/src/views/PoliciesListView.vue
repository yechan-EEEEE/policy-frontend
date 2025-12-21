<template>
  <AppNavbar />

  <main class="policy-page">
    <section class="policy-container">
      <h1 class="page-title">정책 목록</h1>

      <!-- 검색 -->
      <input
        v-model="keyword"
        class="search-input"
        placeholder="정책 제목 또는 설명 검색"
      />

      <!-- 맞춤 필터 -->
      <div class="custom-filter">
        <button
          class="filter-chip"
          :class="{ active: onlyMatched }"
          @click="toggleMatched"
        >
          🎯 내 조건에 맞는 정책
        </button>

        <button
          class="filter-chip"
          :class="{ active: hideExpired }"
          @click="hideExpired = !hideExpired"
        >
          ⏰ 신청기간 지난 정책 숨기기
        </button>

        <span
          v-if="onlyMatched && auth.isLogin"
          class="filter-desc"
        >
          나이 {{ auth.user.age }},
          지역 {{ auth.user.region }} 기준
        </span>

        <div
          v-if="onlyMatched && auth.isLogin"
          class="match-summary"
        >
          총 <strong>{{ filteredPolicies.length }}</strong>개의 정책이
          내 조건에 맞습니다.
        </div>

        <span
          v-if="!auth.isLogin"
          class="filter-disabled"
        >
          로그인 후 사용 가능
        </span>
      </div>

      <!-- 대분류 -->
      <div class="filter-group">
        <strong>대분류</strong>
        <div class="filter-buttons">
          <button
            v-for="cat in mainCategories"
            :key="cat"
            :class="{ active: selectedCategory === cat }"
            @click="selectCategory(cat)"
          >
            {{ cat }}
          </button>
          <button
            :class="{ active: selectedCategory === '' }"
            @click="selectCategory('')"
          >
            전체
          </button>
        </div>
      </div>

      <!-- 소분류 -->
      <div
        class="filter-group"
        v-if="subCategories.length"
      >
        <strong>소분류</strong>
        <div class="filter-buttons">
          <button
            v-for="sub in subCategories"
            :key="sub"
            :class="{ active: selectedSubCategory === sub }"
            @click="selectedSubCategory = sub"
          >
            {{ sub }}
          </button>
          <button
            :class="{ active: selectedSubCategory === '' }"
            @click="selectedSubCategory = ''"
          >
            전체
          </button>
        </div>
      </div>

      <hr />

      <!-- 정책 카드 -->
      <div class="card-list">
        <div
          v-for="policy in filteredPolicies"
          :key="policy.pk"
          class="policy-card"
          @click="goDetail(policy.pk)"
        >
          <h3 class="card-title">{{ policy.title }}</h3>
          <p class="card-desc">{{ policy.description }}</p>
          <span class="card-meta">
            {{ policy.category }} / {{ policy.subTitle }}
          </span>
        </div>

        <p
          v-if="filteredPolicies.length === 0"
          class="empty-text"
        >
          조건에 맞는 정책이 없습니다.
        </p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePolicyStore } from '@/stores/policy'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/common/AppNavbar.vue'

const router = useRouter()
const policyStore = usePolicyStore()
const auth = useAuthStore()

const keyword = ref('')
const onlyMatched = ref(false)
const hideExpired = ref(false)
const selectedCategory = ref('')
const selectedSubCategory = ref('')

onMounted(() => {
  if (!policyStore.policies.length) {
    policyStore.loadPolicies()
  }
})

const policies = computed(() => policyStore.policies)

// 대분류
const mainCategories = computed(() => {
  const set = new Set()
  policies.value.forEach(p => set.add(p.category))
  return [...set]
})

// 소분류
const subCategories = computed(() => {
  if (!selectedCategory.value) return []
  const set = new Set()
  policies.value.forEach(p => {
    if (p.category === selectedCategory.value) {
      set.add(p.subTitle)
    }
  })
  return [...set]
})

// 필터링
const filteredPolicies = computed(() => {
  return policies.value.filter(p => {
    if (selectedCategory.value && p.category !== selectedCategory.value) {
      return false
    }

    if (selectedSubCategory.value && p.subTitle !== selectedSubCategory.value) {
      return false
    }

    if (
      keyword.value &&
      !p.title.includes(keyword.value) &&
      !p.description.includes(keyword.value)
    ) {
      return false
    }

    if (hideExpired.value && isExpired(p.aplyYmd)) {
      return false
    }

    if (onlyMatched.value && auth.isLogin) {
      const age = auth.user.age
      const min = Number(p.sprtTrgtMinAge)
      const max = Number(p.sprtTrgtMaxAge)
      if ((min && age < min) || (max && age > max)) {
        return false
      }
    }

    return true
  })
})

const toggleMatched = () => {
  if (!auth.isLogin) return
  onlyMatched.value = !onlyMatched.value
}

const selectCategory = (cat) => {
  selectedCategory.value = cat
  selectedSubCategory.value = ''
}

const goDetail = (pk) => {
  router.push(`/policies/${pk}`)
}

const isExpired = (aplyYmd) => {
  if (!aplyYmd) return false
  const parts = aplyYmd.split('~')
  if (parts.length !== 2) return false

  const end = parts[1].trim()
  const endDate = new Date(
    end.slice(0, 4),
    Number(end.slice(4, 6)) - 1,
    end.slice(6, 8)
  )

  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return endDate < today
}
</script>

<style scoped>
/* 전체 페이지 */
.policy-page {
  min-height: 100vh;
  background: #f8fafc;
}

/* 컨테이너 */
.policy-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
  background: #ffffff;
  border-radius: 12px;
}

/* 제목 */
.page-title {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 16px;
}

/* 검색 */
.search-input {
  width: 100%;
  padding: 12px 14px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  margin-bottom: 20px;
}

/* 필터 */
.custom-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-bottom: 20px;
}

.filter-chip {
  padding: 8px 14px;
  border-radius: 20px;
  border: 1px solid #d1d5db;
  background: #f1f5f9;
  cursor: pointer;
  font-size: 13px;
}

.filter-chip.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.filter-desc {
  font-size: 13px;
  color: #374151;
}

.match-summary {
  font-size: 13px;
  color: #1f2937;
}

.filter-disabled {
  font-size: 13px;
  color: #9ca3af;
}

/* 분류 */
.filter-group {
  margin-top: 20px;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.filter-buttons button {
  padding: 6px 14px;
  border-radius: 16px;
  border: 1px solid #d1d5db;
  background: #f9fafb;
  cursor: pointer;
  font-size: 13px;
}

.filter-buttons button.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

hr {
    margin: 32px 0;
}

/* 카드 */
.card-list {
  margin-top: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
  gap: 16px;
}

.policy-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.policy-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.card-title {
  font-size: 18px;
  margin-bottom: 8px;
}

.card-desc {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
}

.card-meta {
  display: block;
  margin-top: 10px;
  font-size: 13px;
  color: #6b7280;
}

.empty-text {
  color: #6b7280;
  font-size: 14px;
}
</style>
