<template>
  <AppNavbar />

  <main class="login-page">
    <div class="login-container">
      <!-- LEFT: LOGIN FORM -->
      <form class="login-box" @submit.prevent="submitLogin">
        <h1>로그인</h1>

        <input
            v-model="username"
            type="text"
            placeholder="아이디"
        />

        <input
            v-model="password"
            type="password"
            placeholder="비밀번호"
        />

        <button type="submit" class="login-btn">
            로그인
        </button>

        <p class="signup-link">
            계정이 없나요?
            <span @click="goSignup">회원가입</span>
        </p>
      </form>

      <!-- RIGHT: AD -->
      <section class="ad-box">
        <div class="ad-placeholder">
          AD
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppNavbar from '@/components/common/AppNavbar.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')

const submitLogin = () => {
  if (!username.value.trim() || !password.value.trim()) {
    alert('아이디와 비밀번호를 입력해주세요.')
    return
  }

  // 🔥 Mock 로그인 (임시)
  auth.login({
    user: {
      username: username.value,
      age: 27,
      region: '경기도',
      job: '취업준비생',
      gender: 'M'
    },
    token: 'mock-token'
  })

  router.push('/')
}


const goSignup = () => {
  router.push('/signup')
}
</script>

<style scoped>
.login-page {
  width: 100%;
  min-height: calc(100vh - 64px);
  background: #f8fafc;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 80px;
}

.login-container {
  width: 100%;
  max-width: 1100px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  padding: 40px;
}

/* LEFT */
.login-box h1 {
  font-size: 28px;
  margin-bottom: 24px;
}

.login-box input {
  width: 100%;
  padding: 12px 14px;
  margin-bottom: 12px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  font-size: 14px;
}

.login-btn {
  width: 100%;
  background: #3b82f6;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 6px;
  margin-top: 8px;
  cursor: pointer;
}

.login-btn:hover {
  background: #2563eb;
}

.signup-link {
  margin-top: 16px;
  font-size: 14px;
  color: #6b7280;
}

.signup-link span {
  color: #3b82f6;
  cursor: pointer;
  margin-left: 4px;
}

/* RIGHT */
.ad-box {
  display: flex;
  justify-content: center;
  align-items: center;
}

.ad-placeholder {
  width: 100%;
  height: 260px;
  border: 3px solid #000;
  font-size: 36px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
