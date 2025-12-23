<template>
  <AppNavbar />

  <main class="thread-page">
    <section class="thread-container">
      <h1 class="page-title">게시글 목록</h1>

      <div class="thread-actions">
        <button
          v-if="false"
          class="write-btn"
          :disabled="!auth.isLogin"
          @click="goWrite"
        >
          ✏️ 게시글 작성
        </button>
      </div>

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
          v-for="thread in pagedThreads"
          :key="thread.id"
          class="thread-card"
          @click="goDetail(thread.id)"
        >
          <h3 class="card-title">{{ thread.title }}</h3>

          <div class="card-meta">
            <span>👁 {{ thread.view_count }}</span>
            <span>❤️ {{ thread.liked_count }}</span>
            <span>💬 {{ thread.comment_count ?? 0 }}</span>
          </div>
        </div>

        <p v-if="filteredThreads.length === 0" class="empty-text">
          조건에 맞는 게시글이 없습니다.
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
import { ref, computed, onMounted, watch } from 'vue'
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
const ITEMS_PER_PAGE = 10
const PAGES_PER_GROUP = 10

const goWrite = () => {
  router.push('/threads/write')
}

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
const currentPage = computed(() => {
  return Number(route.query.page) || 1
})
const totalPages = computed(() => {
  return Math.ceil(filteredThreads.value.length / ITEMS_PER_PAGE)
})
const currentGroup = computed(() => {
  return Math.floor((currentPage.value - 1) / PAGES_PER_GROUP)
})
const pagedThreads = computed(() => {
  const start = (currentPage.value - 1) * ITEMS_PER_PAGE
  const end = start + ITEMS_PER_PAGE
  return filteredThreads.value.slice(start, end)
})
const visiblePages = computed(() => {
  const start = currentGroup.value * PAGES_PER_GROUP + 1
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
    path: '/threads',
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

const goFirst = () => goPage(1)
const goLast = () => goPage(totalPages.value)

watch(keyword, () => {
  router.push({
    path: '/threads',
    query: {
      ...route.query,
      page: 1,
    },
  })
})

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
.card-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
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
.pagination {
  margin-top: 40px;
  display: flex;
  justify-content: center;
  gap: 6px;
}

.pagination button {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  background: #fff;
  cursor: pointer;
}

.pagination button.active {
  background: #2563eb;
  color: #fff;
  border-color: #2563eb;
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.thread-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}

.write-btn {
  padding: 10px 16px;
  border-radius: 8px;
  background: #2563eb;
  color: white;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.write-btn:hover {
  background: #1d4ed8;
}
.write-btn:disabled {
  background: #cbd5f5;
  cursor: not-allowed;
}

</style>
