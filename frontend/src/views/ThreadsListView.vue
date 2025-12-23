<template>
  <AppNavbar />

  <main class="thread-page">
    <section class="thread-container">
      <h1 class="page-title">게시글 목록</h1>

      <!-- 검색 -->
      <input
        v-model="keyword"
        class="search-input"
        placeholder="게시글 제목 또는 내용 검색"
      />

      <!-- 맞춤 필터 -->
      <div class="custom-filter">
        <button
          class="filter-chip"
          :class="{ active: onlyMatched }"
          @click="toggleMatched"
        >
          🎯 내 조건에 맞는 게시글
        </button>

        <div v-if="onlyMatched && auth.isLogin" class="match-summary">
          총 <strong>{{ filteredThreads.length }}</strong>개의 게시글이 내 조건에 맞습니다.
        </div>

        <span v-if="!auth.isLogin" class="filter-disabled">
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
      <div v-if="subCategories.length" class="filter-group">
        <strong>소분류</strong>
        <div class="filter-buttons">
          <button
            v-for="sub in subCategories"
            :key="sub"
            :class="{ active: selectedSubCategory === sub }"
            @click="selectSubCategory(sub)"
          >
            {{ sub }}
          </button>
          <button
            :class="{ active: selectedSubCategory === '' }"
            @click="selectSubCategory('')"
          >
            전체
          </button>
        </div>
      </div>

      <hr />

      <!-- 게시글 카드 -->
      <div class="card-list">
        <div
          v-for="thread in filteredThreads"
          :key="thread.id"
          class="thread-card"
          @click="goDetail(thread.id)"
        >
          <h3 class="card-title">{{ thread.title }}</h3>
          <p class="card-desc">{{ thread.content }}</p>
          <div class="card-meta">
            <span>
              {{ policyStore.getByPlcyNo(thread.policy)?.lclsfNm }}
              /
              {{ policyStore.getByPlcyNo(thread.policy)?.mclsfNm }}
            </span>
            <span>👍 {{ thread.like_count ?? 0 }}</span>
          </div>
        </div>

        <p v-if="filteredThreads.length === 0" class="empty-text">
          조건에 맞는 게시글이 없습니다.
        </p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useThreadStore } from '@/stores/thread'
import { usePolicyStore } from '@/stores/policy'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/common/AppNavbar.vue'

const router = useRouter()
const route = useRoute()
const threadStore = useThreadStore()
const policyStore = usePolicyStore()
const auth = useAuthStore()

const keyword = ref('')
const onlyMatched = ref(false)
const selectedCategory = ref('')
const selectedSubCategory = ref('')

onMounted(async () => {
  await policyStore.fetchPolicies()

  // 정책 기준 목록 or 전체
  if (route.query.policyId) {
    await threadStore.fetchThreadsByPolicy(route.query.policyId)
  } else {
    await threadStore.fetchThreads()
  }
})

const threads = computed(() => threadStore.threads)

/* 대분류 / 소분류는 정책 기준 */
const mainCategories = computed(() => policyStore.categories)

const subCategories = computed(() => {
  if (!selectedCategory.value) return []
  return policyStore.subCategories(selectedCategory.value)
})

/* 필터링 */
const filteredThreads = computed(() => {
  return threads.value.filter(t => {
    const policy = policyStore.getByPlcyNo?.(t.policy)

    // 🔥 정책 아직 로딩 안 됐으면 그냥 보여줌
    if (!policyStore.isLoaded) return threads.value

    if (selectedCategory.value && policy.lclsfNm !== selectedCategory.value) {
      return false
    }

    if (selectedSubCategory.value && policy.mclsfNm !== selectedSubCategory.value) {
      return false
    }

    if (
      keyword.value &&
      !t.title.includes(keyword.value) &&
      !t.content.includes(keyword.value)
    ) {
      return false
    }

    return true
  })
})


const selectCategory = (cat) => {
  selectedCategory.value = cat
  selectedSubCategory.value = ''
}

const selectSubCategory = (sub) => {
  selectedSubCategory.value = sub
}

const goDetail = (threadId) => {
  router.push(`/threads/${threadId}`)
}
</script>



<style scoped>
/* 전체 페이지 */
.thread-page {
  min-height: 100vh;
  background: #f8fafc;
}

/* 컨테이너 */
.thread-container {
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

.thread-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.thread-card:hover {
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
