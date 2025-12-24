<template>
  <AppNavbar />

  <main class="home">
    <span class="badge">Policy Community</span>

    <!-- 로그인 상태 -->
    <section v-if="auth.isLogin">
      <h1>{{ auth.user.username }}님을 위한 추천 정책</h1>
      <p class="sub">
        AI 추천 · 나이 {{ userAge ?? '-' }}세 기준 · 관심도 높은 정책
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
        :key="p.plcyNo"
        class="policy-card"
        @click="goPolicy(p.plcyNo)"
      >
        <!-- 상단: 제목 / 분류 -->
        <div class="card-body">
          <h3 class="policy-title">{{ p.plcyNm }}</h3>
          <p class="policy-sub">
            {{ p.lclsfNm }} / {{ p.mclsfNm }}
          </p>
        </div>

        <!-- 하단: 메타 정보 -->
        <div class="card-footer">
          <span
            class="policy-like"
            @click.stop="togglePolicyLike(p)"
          >
            ⭐ {{ p.liked_count ?? 0 }}
          </span>

          <span
            class="policy-threads"
            >
            💬 {{ p.thread_count ?? 0 }}
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
          👀 {{ t.view_count || 0 }} · ❤️ {{ (t.liked_count || 0) }}
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
  if (!policyStore.policies.length) {
    policyStore.fetchPolicies()
  }
    threadStore.fetchThreads()
})

const userAge = computed(() => {
  if (!auth.user?.birth_date) return null
  const birthYear = new Date(auth.user.birth_date).getFullYear()
  return new Date().getFullYear() - birthYear + 1
})

const recommendedPolicies = computed(() => {
  let list = [...(policyStore.policies || [])]

  if (auth.isLogin && userAge.value) {
    list = list.filter(p => {
      if (p.sprtTrgtMinAge && userAge.value < p.sprtTrgtMinAge) return false
      if (p.sprtTrgtMaxAge && userAge.value > p.sprtTrgtMaxAge) return false
      return true
    })
  }

  list.sort(
    (a, b) =>
      (b.liked_count ?? 0) - (a.liked_count ?? 0)
  )

  return list.slice(0, 4)
})

const recommendedThreads = computed(() => {
  const list = [...(threadStore.threads || [])]

  list.sort((a, b) => {
    const scoreA = (a.view_count || 0) + (a.like_count || 0)
    const scoreB = (b.view_count || 0) + (b.like_count || 0)
    return scoreB - scoreA
  })

  return list.slice(0, 4)
})

const togglePolicyLike = async (policy) => {
  if (!auth.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }

  const res = await policyStore.toggleLike(policy.plcyNo)
  policy.liked_count = res.liked_count
  policy.is_liked = res.is_liked
}

const goPolicy = (plcyNo) => router.push(`/policies/${plcyNo}`)
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
