--- PolicyDetailView.vue ---
<template>
  <AppNavbar />

  <main class="policy-detail-page" v-if="policy">
    <div class="container">

      <!-- 제목 카드 -->
      <section class="card header-card">
        <span class="badge">{{ policy.lclsfNm }}</span>

        <h1 class="title">{{ policy.plcyNm }}</h1>
        <p class="desc">{{ policy.plcyExplnCn }}</p>

        <!-- ⭐ 좋아요 / 💬 게시글 -->
        <div class="policy-actions">
          <button
            class="like-btn"
            :class="{ liked: policy.is_liked }"
            @click="toggleLike"
          >
            ⭐ {{ policy.liked_count ?? 0 }}
          </button>

          <span
            class="thread-count"
            @click.stop="goPolicyThreads(policy.plcyNo)"
          >
            💬 {{ policy.thread_count ?? 0 }}
          </span>
        </div>
      </section>

      <!-- 핵심 정보 -->
      <section class="card info-grid">
        <div class="info-item">
          <strong>연령</strong>
          <span>{{ policy.sprtTrgtMinAge }} ~ {{ policy.sprtTrgtMaxAge }}</span>
        </div>

        <div class="info-item">
          <strong>사업 기간</strong>
          <span>{{ policy.bizPrdBgngYmd }} ~ {{ policy.bizPrdEndYmd }}</span>
        </div>

        <div class="info-item">
          <strong>주관 기관</strong>
          <span>{{ policy.sprvsnInstCdNm || '정보 없음' }}</span>
        </div>
      </section>

      <!-- 🔥 정책 AI 요약 -->
      <section class="card ai-summary">
        <div class="ai-header">
          <h2 class="section-title">✨ 정책 AI 요약</h2>

          <button
            class="ai-btn"
            @click="fetchSummary"
            :disabled="loadingSummary"
          >
            {{ loadingSummary ? '요약 생성 중...' : 'AI 요약 생성' }}
          </button>
        </div>

        <p v-if="summary" class="summary-text">
          {{ summary }}
        </p>

        <p v-else class="summary-placeholder">
          버튼을 눌러 정책 요약을 확인해보세요.
        </p>
      </section>

      <!-- 지원 내용 -->
      <section class="card">
        <h2 class="section-title">지원 내용</h2>
        <pre class="support-text">{{ policy.plcySprtCn }}</pre>
      </section>

      <!-- 액션 -->
      <div class="actions">
        <button
          v-if="auth.isLogin"
          class="primary"
          @click="goWrite"
        >
          이 정책에 글 쓰기
        </button>

        <button v-else class="disabled" disabled>
          로그인 후 글 작성 가능
        </button>
      </div>

    </div>
  </main>

  <div v-else class="loading">
    정책 정보를 불러오는 중입니다...
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePolicyStore } from '@/stores/policy'
import { useThreadStore } from '@/stores/thread'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/common/AppNavbar.vue'

const route = useRoute()
const router = useRouter()

const policyStore = usePolicyStore()
const threadStore = useThreadStore()
const auth = useAuthStore()

const policy = computed(() => policyStore.policyDetail)

/* 🔥 AI 요약 상태 */
const summary = ref('')
const loadingSummary = ref(false)

watch(
  () => route.params.plcyNo,
  async (plcyNo) => {
    if (!plcyNo) return
    summary.value = ''        // 정책 바뀌면 요약 초기화
    await policyStore.fetchPolicyDetail(plcyNo)
    await threadStore.fetchThreadsByPolicy(plcyNo)
  },
  { immediate: true }
)

const fetchSummary = async () => {
  if (summary.value) return   // 이미 있으면 재요청 X

  try {
    loadingSummary.value = true
    const res = await policyStore.summarizePolicy(policy.value.plcyNo)
    summary.value = res.summary
  } catch (e) {
    alert('AI 요약 생성에 실패했습니다.')
  } finally {
    loadingSummary.value = false
  }
}

const goWrite = () => {
  router.push(`/threads/${route.params.plcyNo}/write`)
}

const toggleLike = async () => {
  if (!auth.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }

  const res = await policyStore.toggleLike(policy.value.plcyNo)
  policyStore.policyDetail.is_liked = res.is_liked
  policyStore.policyDetail.liked_count = res.liked_count
}

const goPolicyThreads = (plcyNo) => {
  router.push({
    path: '/threads',
    query: { policyId: plcyNo },
  })
}
</script>

<style scoped>
.policy-detail-page {
  background: #f8fafc;
  min-height: calc(100vh - 64px);
  padding: 40px 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 카드 공통 */
.card {
  background: #fff;
  border-radius: 12px;
  padding: 28px;
  margin-bottom: 24px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
}

/* 헤더 */
.header-card .badge {
  display: inline-block;
  background: #e0f2fe;
  color: #0284c7;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 13px;
  margin-bottom: 12px;
}

.title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
}

.desc {
  color: #4b5563;
  line-height: 1.6;
}

/* 정보 그리드 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.info-item {
  background: #f9fafb;
  padding: 16px;
  border-radius: 8px;
}

.info-item strong {
  display: block;
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 4px;
}

/* 섹션 제목 */
.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
}

/* 지원 내용 */
.support-text {
  white-space: pre-wrap;
  line-height: 1.6;
  color: #374151;
  font-family: inherit;
}

/* 액션 */
.policy-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
}

.like-btn, .thread-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 14px;
  line-height: 1; /* 🔥 baseline 문제 차단 */
}

.like-btn {
  background: #f3f4f6;
  border: none;
  cursor: pointer;
}

.like-btn.liked {
  background: #fde68a;
  color: #92400e;
}

.thread-count {
  background: #68c2e6ad;
  border: none;
  color: #4e535e;
  cursor: pointer;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}

.primary {
  background: #2563eb;
  color: #fff;
  padding: 12px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.primary:hover {
  background: #1d4ed8;
}

.disabled {
  background: #9ca3af;
  color: #fff;
  padding: 12px 20px;
  border-radius: 8px;
  border: none;
}

/* 로딩 */
.loading {
  padding: 80px;
  text-align: center;
  color: #6b7280;
}

.ai-summary {
  background: #f8fafc;
}

.ai-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ai-btn {
  background: #6366f1;
  color: #fff;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}

.ai-btn:disabled {
  background: #a5b4fc;
  cursor: not-allowed;
}

.summary-text {
  margin-top: 16px;
  line-height: 1.7;
  color: #374151;
}

.summary-placeholder {
  margin-top: 16px;
  font-size: 14px;
  color: #9ca3af;
}

/* 반응형 */
@media (max-width: 768px) {
  .info-grid { grid-template-columns: 1fr; }
}

</style>