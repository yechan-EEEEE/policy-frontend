<template>
  <AppNavbar />

  <main class="home">
    <span class="badge">Policy Community</span>

    <!-- 로그인 상태 -->
    <section v-if="auth.isLogin">
      <h1>{{ auth.user.username }}님에게 맞는 정책을 찾아보세요</h1>
      <p class="sub">
        나이 {{ auth.user.age }}, 지역 {{ auth.user.region }} 기준으로
        맞춤 정책을 추천해드립니다.
      </p>
    </section>

    <!-- 비로그인 상태 -->
    <section v-else>
      <h1>나에게 맞는 정책을 더 쉽게 찾다</h1>
      <p class="sub">
        청년 정책 정보를 한눈에 확인하고 실제 이용자들의 후기를 통해
        나에게 맞는 정책을 찾아보세요.
      </p>
    </section>

    <!-- ✅ 추천 정책 카드 -->
    <div class="policy-cards">
      <div
        v-for="p in recommendedPolicies"
        :key="p.pk"
        class="policy-card"
        @click="goPolicy(p.pk)"
      >
        <!-- 상단: 제목 / 분류 -->
        <div class="card-body">
          <h3 class="policy-title">{{ p.title }}</h3>
          <p class="policy-sub">
            {{ p.category }} / {{ p.subTitle }}
          </p>
        </div>

        <!-- 하단: 메타 정보 -->
        <div class="card-footer">
          <span class="policy-like">
            ⭐ {{ p.liked_users?.length || 0 }}
          </span>

          <span
            class="policy-threads"
            @click.stop="goPolicyThreads(p.pk)"
          >
            💬 {{ p.thread_count || 0 }}
          </span>
        </div>
      </div>


      <p v-if="recommendedPolicies.length === 0" class="empty-text">
        추천할 정책이 아직 없습니다.
      </p>
    </div>

    <button class="primary-btn" @click="goPolicies">
      정책 둘러보기
    </button>

    <!-- ✅ 인기 게시글 (로그인/로그아웃 무관) -->
    <div class="threads">
      <div
        v-for="t in recommendedThreads"
        :key="t.id"
        class="thread"
        @click="goThread(t.id)"
      >
        <div class="thread-title">{{ t.title }}</div>
        <div class="thread-meta">
          👀 {{ t.view_count || 0 }} · ❤️ {{ (t.liked_users?.length || 0) }}
        </div>
      </div>

      <p v-if="recommendedThreads.length === 0" class="empty-text">
        아직 인기 게시글이 없습니다.
      </p>
    </div>

    <button class="ghost-btn" @click="goThreads">
      게시글 보기
    </button>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { computed, onMounted } from 'vue'

import AppNavbar from '@/components/common/AppNavbar.vue'
import { useAuthStore } from '@/stores/auth'
import { usePolicyStore } from '@/stores/policy'
import { useThreadStore } from '@/stores/thread'

const router = useRouter()
const auth = useAuthStore()
const policyStore = usePolicyStore()
const threadStore = useThreadStore()

onMounted(() => {
  policyStore.loadPolicies()
  threadStore.loadThreads()
})

/**
 * ✅ 추천 정책 (로그인: 조건 맞는 정책 중 liked_users 많은 순 TOP 4)
 * ✅ 비로그인: 전체 정책 중 liked_users 많은 순 TOP 4
 */
const recommendedPolicies = computed(() => {
  let list = Array.isArray(policyStore.policies) ? [...policyStore.policies] : []

  if (auth.isLogin && auth.user) {
    const age = auth.user.age
    list = list.filter(p => {
      if (p.sprtTrgtMinAge && age < p.sprtTrgtMinAge) return false
      if (p.sprtTrgtMaxAge && age > p.sprtTrgtMaxAge) return false
      return true
    })
  }

  list.sort((a, b) => (b.liked_users?.length || 0) - (a.liked_users?.length || 0))
  return list.slice(0, 4)
})

/**
 * ✅ 인기 게시글 (로그인/로그아웃 무관)
 * 기준: view_count + liked_users.length 높은 순 TOP 4
 */
const recommendedThreads = computed(() => {
  const list = Array.isArray(threadStore.threads) ? [...threadStore.threads] : []

  list.sort((a, b) => {
    const scoreA = (a.view_count || 0) + (a.liked_users?.length || 0)
    const scoreB = (b.view_count || 0) + (b.liked_users?.length || 0)
    return scoreB - scoreA
  })

  return list.slice(0, 4)
})

const goPolicyThreads = (policyPk) => {
  router.push({
    path: '/threads',
    query: { policyId: policyPk }
  })
}

const goPolicy = (pk) => router.push(`/policies/${pk}`)
const goPolicies = () => router.push('/policies')
const goThread = (id) => router.push(`/threads/${id}`)
const goThreads = () => router.push('/threads')
</script>

<style scoped>
.home {
  background: radial-gradient(circle at top, #0b122f, #020617);
  min-height: calc(100vh - 64px);
  padding: 80px 120px;
  color: white;
}

.badge {
  display: inline-block;
  padding: 6px 14px;
  background: #1f2937;
  border-radius: 999px;
  font-size: 12px;
  margin-bottom: 16px;
}

h1 {
  font-size: 36px;
  margin-bottom: 12px;
}

.sub {
  color: #cbd5f5;
  margin-bottom: 40px;
}

/* 정책 카드 */
.policy-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.policy-card {
  height: 160px;
  background: #f8fafc;
  border-radius: 12px;
  cursor: pointer;
  padding: 16px;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  transition: transform 0.15s ease, box-shadow 0.15s ease;
  color: #020617;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.policy-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 24px rgba(0,0,0,0.18);
}

.policy-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
  line-height: 1.3;
}

.policy-sub {
  font-size: 13px;
  color: #475569;
  margin-bottom: 10px;
}

.policy-like {
  font-size: 15px;
  color: #facc15;
}

.policy-threads {
  color: #475569;
  font-size: 15px;
  cursor: pointer;
}

.policy-threads:hover {
  text-decoration: underline;
}

/* 버튼 */
.primary-btn {
  background: #3b82f6;
  padding: 10px 18px;
  border-radius: 8px;
  color: white;
  border: none;
  margin-bottom: 40px;
  cursor: pointer;
}

/* 게시글 */
.threads {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.thread {
  background: #f8fafc;
  color: #020617;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.thread:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0,0,0,0.18);
}

.thread-title {
  font-weight: 700;
  margin-bottom: 6px;
}

.thread-meta {
  font-size: 12px;
  color: #475569;
}

.ghost-btn {
  border: 2px solid #94a3b8;
  color: black;
  padding: 8px 16px;
  background: white;
  border-radius: 6px;
  font-weight: bolder;
  cursor: pointer;
}

.empty-text {
  grid-column: 1 / -1;
  color: #cbd5f5;
  font-size: 14px;
  opacity: 0.8;
}
</style>
