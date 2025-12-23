<template>
  <AppNavbar />

  <main class="mypage">
    <div class="container">
      <h1>마이페이지</h1>

      <!-- 내 정보 카드 -->
      <section v-if="auth.user" class="info-card">
        <h2>내 정보</h2>

        <div class="info-row">
          <span class="label">닉네임</span>
          <span class="value">{{ auth.user.username }}</span>
        </div>

        <div class="info-row">
          <span class="label">나이</span>
          <span class="value">{{ age }}세</span>
        </div>

        <div class="info-row">
          <span class="label">지역</span>
          <span class="value">{{ auth.user.region }}</span>
        </div>

        <div class="info-row">
          <span class="label">재직 상태</span>
          <span class="value">{{ auth.user.job }}</span>
        </div>
      </section>
      <div v-else class="loading">
        사용자 정보를 불러오는 중입니다...
      </div>

      <!-- 하단 버튼 -->
      <div class="actions">
        <div class="left">
          <button class="primary" @click="goEdit">
            정보 수정
          </button>
          <button class="secondary" @click="logout">
            로그아웃
          </button>
        </div>

        <button class="danger" @click="withdraw">
          회원 탈퇴
        </button>
      </div>

      
    </div>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/common/AppNavbar.vue'
import { computed } from 'vue'
import api from '@/api/axios'

const age = computed(() => {
  if (!auth.user?.birth_date) return '-'

  const birthYear = new Date(auth.user.birth_date).getFullYear()
  const currentYear = new Date().getFullYear()
  return currentYear - birthYear + 1
})

const router = useRouter()
const auth = useAuthStore()

const goEdit = () => {
  router.push('/mypage/edit')
}

const logout = async () => {
  await auth.logout()
  router.push('/login')
}

const withdraw = async () => {
  const ok = confirm(
    '정말 회원 탈퇴하시겠습니까?\n이 작업은 되돌릴 수 없습니다.'
  )
  if (!ok) return

  try {
    await api.delete('/accounts/delete/')
    auth.clearAuth()
    alert('회원 탈퇴가 완료되었습니다.')
    router.push('/')
  } catch (e) {
    alert('회원 탈퇴에 실패했습니다.')
    console.error(e)
  }
}

</script>

<style scoped>
.mypage {
  width: 100%;
  min-height: calc(100vh - 64px);
  background: #f8fafc;
  display: flex;
  justify-content: center;
  padding-top: 80px;
}

.container {
  width: 100%;
  max-width: 900px;
  padding: 0 24px;
}

h1 {
  font-size: 28px;
  margin-bottom: 24px;
}

/* 정보 카드 */
.info-card {
  background: white;
  border-radius: 10px;
  padding: 24px;
  margin-bottom: 32px;
  border: 1px solid #e5e7eb;
}

.info-card h2 {
  font-size: 18px;
  margin-bottom: 16px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #e5e7eb;
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  color: #374151;
  font-weight: 500;
}

.value {
  color: #111827;
}

/* 하단 버튼 */
.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  gap: 12px;
}

button {
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  border: none;
}

.primary {
  background: #2563eb;
  color: white;
}

.primary:hover {
  background: #1d4ed8;
}

.secondary {
  background: #3b82f6;
  color: white;
}

.secondary:hover {
  background: #2563eb;
}

.danger {
  background: #ef4444;
  color: white;
}

.danger:hover {
  background: #dc2626;
}
</style>
