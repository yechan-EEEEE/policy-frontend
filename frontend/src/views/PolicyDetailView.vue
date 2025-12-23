<template>
  <AppNavbar />

  <main class="policy-detail-page" v-if="policy">
    <div class="container">

      <!-- 제목 카드 -->
      <section class="card header-card">
        <span class="badge">{{ policy.lclsfNm }}</span>
        <h1 class="title">{{ policy.plcyNm }}</h1>
        <p class="desc">{{ policy.plcyExplnCn }}</p>
      </section>

      <!-- 핵심 정보 -->
      <section class="card info-grid">
        <div class="info-item">
          <strong>연령</strong>
          <span>
            {{ policy.sprtTrgtMinAge }} ~ {{ policy.sprtTrgtMaxAge }}
          </span>
        </div>

        <div class="info-item">
          <strong>사업 기간</strong>
          <span>
            {{ policy.bizPrdBgngYmd }} ~ {{ policy.bizPrdEndYmd }}
          </span>
        </div>

        <div class="info-item">
          <strong>주관 기관</strong>
          <span>{{ policy.sprvsnInstCdNm || '정보 없음' }}</span>
        </div>
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

        <button
          v-else
          class="disabled"
          disabled
        >
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
import { watch, computed } from 'vue'
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

watch(
  () => route.params.plcyNo,
  (plcyNo) => {
    if (!plcyNo) return
    policyStore.fetchPolicyDetail(plcyNo)
    threadStore.fetchThreadsByPolicy(plcyNo)
  },
  { immediate: true }
)

const goWrite = () => {
  router.push(`/threads/${route.params.plcyNo}/write`)
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

/* 반응형 */
@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
