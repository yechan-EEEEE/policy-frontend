<template>
  <AppNavbar />

  <main class="thread-page">
    <section class="thread-container">
      <h1 class="page-title">게시글 목록</h1>

      <!-- 🔥 정책 필터 안내 -->
      <p v-if="currentPolicy" class="policy-filter-title">
        <strong>{{ currentPolicy.plcyNm }}</strong> 정책의 게시글
      </p>

      <!-- 🔍 제목 검색 -->
      <input
        v-model="keyword"
        class="search-input"
        placeholder="게시글 제목 검색"
      />

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

          <div class="card-meta">
            <span>👁 {{ thread.view_count }}</span>
            <span>❤️ {{ thread.liked_count }}</span>
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
import AppNavbar from '@/components/common/AppNavbar.vue'

const router = useRouter()
const route = useRoute()
const threadStore = useThreadStore()
const policyStore = usePolicyStore()

/* 🔍 검색어 */
const keyword = ref('')

/* 초기 로딩 */
onMounted(async () => {
  if (!policyStore.policies.length) {
    await policyStore.fetchPolicies()
  }

  if (route.query.policyId) {
    await threadStore.fetchThreadsByPolicy(route.query.policyId)
  } else {
    await threadStore.fetchThreads()
  }
})

/* thread 목록 */
const threads = computed(() => threadStore.threads)

/* 🔍 제목 검색 필터 */
const filteredThreads = computed(() => {
  return threads.value.filter(t => {
    if (
      keyword.value &&
      !t.title.toLowerCase().includes(keyword.value.toLowerCase())
    ) {
      return false
    }
    return true
  })
})

/* 정책 정보 (상단 안내용) */
const currentPolicy = computed(() => {
  const plcyNo = route.query.policyId
  if (!plcyNo) return null

  return policyStore.policies.find(
    p => String(p.plcyNo) === String(plcyNo)
  )
})

/* 상세 페이지 이동 */
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

/* 카드 영역 */
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
  margin-bottom: 10px;
}

.card-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #6b7280;
}

.empty-text {
  color: #6b7280;
  font-size: 14px;
  margin-top: 20px;
}

.policy-filter-title {
  margin: 8px 0 20px;
  color: #2563eb;
  font-size: 15px;
}
</style>
