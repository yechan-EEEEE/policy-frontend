<template>
  <header class="navbar">
    <!-- Left -->
    <div class="nav-left" @click="goHome">
      <span class="logo">PolicyHub</span>
    </div>

    <!-- Center -->
    <nav class="nav-center">
      <span @click="goPolicies">정책</span>
      <span @click="goThreads">게시판</span>
    </nav>

    <!-- Right -->
    <div class="nav-right">
      <button
        v-if="!auth.isLogin"
        class="login-btn"
        @click="goLogin"
      >
        로그인
      </button>

      <span
        v-else
        class="username"
        @click="goMyPage"
      >
        {{ auth.user.username }}
      </span>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const goHome = () => router.push('/')
const goPolicies = () => router.push('/policies')
const goThreads = () => router.push('/threads')
const goLogin = () => router.push('/login')
const goMyPage = () => router.push('/mypage')
</script>

<style scoped>
.navbar {
  height: 64px;
  background: linear-gradient(180deg, #050b1c, #020617);
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: relative;
}

.navbar::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    to right,
    transparent,
    rgba(255,255,255,0.4),
    transparent
  );
}

.logo {
  font-weight: 700;
  font-size: 18px;
  cursor: pointer;
}

.nav-center span {
  margin: 0 16px;
  cursor: pointer;
  font-weight: 500;
}

.nav-right .login-btn {
  border: 1px solid #3b82f6;
  background: transparent;
  color: #3b82f6;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
}

.username {
  color: #60a5fa;
  cursor: pointer;
}
</style>
