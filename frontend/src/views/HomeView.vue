<template>
  <AppNavbar />

  <main class="home">
    <span class="badge">Policy Community</span>

    <!-- 로그인 상태 -->
    <section v-if="auth.isLogin">
      <h1>
        {{ auth.user.username }}님에게 맞는 정책을 찾아보세요
      </h1>
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

    <!-- 정책 카드 -->
    <div class="policy-cards">
      <div
        v-for="p in policies"
        :key="p.id"
        class="policy-card"
        @click="goPolicy(p.id)"
      />
    </div>

    <button class="primary-btn" @click="goPolicies">
      정책 둘러보기
    </button>

    <!-- 게시글 -->
    <div class="threads">
      <div
        v-for="t in threads"
        :key="t.id"
        class="thread"
        @click="goThread(t.id)"
      >
        {{ t.title }}
      </div>
    </div>

    <button class="ghost-btn" @click="goThreads">
      게시글 보기
    </button>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/common/AppNavbar.vue'

const router = useRouter()
const auth = useAuthStore()

// Mock 데이터
const policies = [1, 2, 3, 4].map((id) => ({ id }))
const threads = Array.from({ length: 6 }).map((_, i) => ({
  id: i + 1,
  title: `게시글 제목 ${i + 1}`
}))

const goPolicy = (id) => router.push(`/policies/${id}`)
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
}

.primary-btn {
  background: #3b82f6;
  padding: 10px 18px;
  border-radius: 8px;
  color: white;
  border: none;
  margin-bottom: 40px;
  cursor: pointer;
}

.threads {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.thread {
  background: #f8fafc;
  color: #020617;
  padding: 10px;
  border-radius: 6px;
  cursor: pointer;
}

.ghost-btn {
  border: 1px solid #94a3b8;
  color: #94a3b8;
  padding: 8px 16px;
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
}
</style>
