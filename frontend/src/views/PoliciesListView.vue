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
          🎯 나이 기준에 맞는 정책
        </button>

        <button
          class="filter-chip"
          :class="{ active: hideExpired }"
          @click="hideExpired = !hideExpired"
        >
          ⏰ 사업기간 지난 정책 숨기기
        </button>

        <span
          v-if="onlyMatched && auth.isLogin"
          class="filter-desc"
        >
          나이 {{ userAge ?? '-' }},
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
          v-for="policy in pagedPolicies"
          :key="policy.plcyNo"
          class="policy-card"
          @click="goDetail(policy.plcyNo)"
        >
          <h3 class="card-title">{{ policy.plcyNm }}</h3>
          <p class="card-desc">{{ policy.plcyExplnCn }}</p>

          <!-- 분류 -->
          <div class="card-meta">
            {{ policy.lclsfNm }} / {{ policy.mclsfNm }}
          </div>

          <!-- 🔥 좋아요 / 관련 글 -->
          <div class="card-stats">
            <span class="like">
              ⭐ {{ policy.liked_count ?? 0 }}
            </span>
          </div>
        </div>

        <p
          v-if="filteredPolicies.length === 0"
          class="empty-text"
        >
          조건에 맞는 정책이 없습니다.
        </p>
      </div>

      <!-- 페이지네이션 -->
      <div class="pagination" v-if="totalPages > 1">

        <!-- 처음 -->
        <button
          class="arrow"
          :disabled="currentPage === 1"
          @click="goFirst"
        >
          &laquo;
        </button>

        <!-- 이전 그룹 -->
        <button
          class="arrow"
          :disabled="currentGroup === 0"
          @click="prevGroup"
        >
          &lsaquo;
        </button>

        <!-- 페이지 번호 -->
        <button
          v-for="page in visiblePages"
          :key="page"
          :class="{ active: page === currentPage }"
          @click="goPage(page)"
        >
          {{ page }}
        </button>

        <!-- 다음 그룹 -->
        <button
          class="arrow"
          :disabled="(currentGroup + 1) * PAGES_PER_GROUP >= totalPages"
          @click="nextGroup"
        >
          &rsaquo;
        </button>

        <!-- 끝 -->
        <button
          class="arrow"
          :disabled="currentPage === totalPages"
          @click="goLast"
        >
          &raquo;
        </button>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePolicyStore } from '@/stores/policy'
import { useAuthStore } from '@/stores/auth'
import { watch } from 'vue'
import AppNavbar from '@/components/common/AppNavbar.vue'

const router = useRouter()
const route = useRoute()
const policyStore = usePolicyStore()
const auth = useAuthStore()

const keyword = ref('')
const onlyMatched = ref(false)
const hideExpired = ref(false)
const selectedCategory = ref('')
const selectedSubCategory = ref('')

watch(
  () => [
    keyword.value,
    selectedCategory.value,
    selectedSubCategory.value,
    hideExpired.value,
    onlyMatched.value,
  ],
  () => {
    router.push({
      path: '/policies',
      query: {
        ...route.query,
        page: 1,
      },
    })
  }
)

onMounted(() => {
  policyStore.fetchPolicies()
})

const policies = computed(() => policyStore.policies)
const userAge = computed(() => {
  if (!auth.user?.birth_date) return null
  const birthYear = new Date(auth.user.birth_date).getFullYear()
  return new Date().getFullYear() - birthYear + 1
})

// 대분류
const mainCategories = computed(() => {
  return [...new Set(policies.value.map(p => p.lclsfNm).filter(Boolean))]
})

// 소분류
const subCategories = computed(() => {
  if (!selectedCategory.value) return []
  return [
    ...new Set(
      policies.value
        .filter(p => p.lclsfNm === selectedCategory.value)
        .map(p => p.mclsfNm)
        .filter(Boolean)
    ),
  ]
})

// 필터링
const filteredPolicies = computed(() => {
  return policies.value.filter(p => {
    if (
      keyword.value &&
      !p.plcyNm.includes(keyword.value) &&
      !p.plcyExplnCn.includes(keyword.value)
    ) {
      return false
    }

    if (selectedCategory.value && p.lclsfNm !== selectedCategory.value) return false
    if (selectedSubCategory.value && p.mclsfNm !== selectedSubCategory.value) return false

    // 🚧 서버 필드 미제공 → 임시 통과
    if (onlyMatched.value && auth.isLogin) return true
    if (hideExpired.value) return true

    return true
  })
})


const isExpired = (endYmd) => {
  if (!endYmd) return false

  // "20250720" -> Date(2025, 6, 20)
  const y = Number(endYmd.slice(0, 4))
  const m = Number(endYmd.slice(4, 6)) - 1
  const d = Number(endYmd.slice(6, 8))

  if (!y || m < 0 || !d) return false

  const endDate = new Date(y, m, d)
  endDate.setHours(23, 59, 59, 999) // 해당 날짜 끝까지 유효

  return endDate < new Date()
}

const toggleMatched = () => {
  if (!auth.isLogin) return
  onlyMatched.value = !onlyMatched.value
}

const selectCategory = (cat) => {
  selectedCategory.value = cat
  selectedSubCategory.value = ''
}

const goDetail = (plcyNo) => {
  router.push(`/policies/${plcyNo}`)
}

const ITEMS_PER_PAGE = 10
const PAGES_PER_GROUP = 10

const currentPage = computed(() => {
  return Number(route.query.page) || 1
})

const totalPages = computed(() => {
  return Math.ceil(filteredPolicies.value.length / ITEMS_PER_PAGE)
})

// 🔥 현재 페이지가 속한 그룹 (0부터 시작)
const currentGroup = computed(() => {
  return Math.floor((currentPage.value - 1) / PAGES_PER_GROUP)
})

const pagedPolicies = computed(() => {
  const start = (currentPage.value - 1) * ITEMS_PER_PAGE
  const end = start + ITEMS_PER_PAGE
  return filteredPolicies.value.slice(start, end)
})

const visiblePages = computed(() => {
  const start =
    currentGroup.value * PAGES_PER_GROUP + 1
  const end = Math.min(
    start + PAGES_PER_GROUP - 1,
    totalPages.value
  )

  const pages = []
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const goPage = (page) => {
  router.push({
    path: '/policies',
    query: {
      ...route.query,
      page,
    },
  })
}

const prevGroup = () => {
  if (currentGroup.value === 0) return
  goPage(currentGroup.value * PAGES_PER_GROUP)
}

const nextGroup = () => {
  const nextStart =
    (currentGroup.value + 1) * PAGES_PER_GROUP + 1
  if (nextStart > totalPages.value) return
  goPage(nextStart)
}
const goFirst = () => {
  goPage(1)
}

const goLast = () => {
  goPage(totalPages.value)
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

.card-stats {
  display: flex;
  gap: 14px;
  margin-top: 8px;
  font-size: 14px;
  color: #6b7280;
}

.card-stats .like {
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-stats .threads {
  display: flex;
  align-items: center;
  gap: 4px;
}

.policy-card {
  height: 180px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  background: #ffffff;
  cursor: pointer;
}

.policy-card h3 {
  font-size: 16px;
  font-weight: 700;

  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.policy-card .card-desc {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.policy-card .card-meta {
  font-size: 13px;
  color: #6b7280;
  margin-top: auto;
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

.pagination {
  display: flex;
  gap: 6px;
  justify-content: center;
  margin-top: 24px;
  flex-wrap: wrap;
}

.pagination button {
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  background: white;
  cursor: pointer;
}

.pagination button.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

.pagination button.arrow {
  font-weight: bold;
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

</style>