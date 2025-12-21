<template>
  <AppNavbar />

  <main class="signup-page">
    <div class="signup-container">
      <!-- LEFT: SIGNUP FORM -->
      <section class="signup-box">
        <h1>회원가입</h1>

        <input v-model="username" type="text" placeholder="아이디" />
        <input v-model="password" type="password" placeholder="비밀번호" />
        <input v-model="passwordConfirm" type="password" placeholder="비밀번호 확인" />
        <p v-if="password && passwordConfirm && password !== passwordConfirm" class="error-text">
        비밀번호가 일치하지 않습니다.
        </p>
        <input v-model="realName" type="text" placeholder="이름" />
        <label class="field-label">생년월일</label>
        <input v-model="birthDate" type="date" />

        <select v-model="region">
          <option disabled value="">지역 선택</option>
          <option value="서울">서울</option>
          <option value="경기">경기</option>
          <option value="인천">인천</option>
          <option value="부산">부산</option>
        </select>

        <select v-model="job">
        <option disabled value="">직업 선택</option>
        <option value="학생">학생</option>
        <option value="취업준비생">취업준비생</option>
        <option value="직장인">직장인</option>
        <option value="자영업자">자영업자</option>
        <option value="프리랜서">프리랜서</option>
        <option value="기타">기타</option>
        </select>

        <!-- Gender -->
        <select v-model="gender">
          <option disabled value="">성별 선택</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>

        <button
          class="signup-btn"
          :disabled="!isValid"
          @click="submitSignup"
        >
          회원가입
        </button>

        <p class="login-link">
          이미 계정이 있나요?
          <span @click="goLogin">로그인</span>
        </p>
      </section>

      <!-- RIGHT: AD -->
      <section class="ad-box">
        <div class="ad-placeholder">AD</div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppNavbar from '@/components/common/AppNavbar.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const passwordConfirm = ref('')
const realName = ref('')
const birthDate = ref('')
const region = ref('')
const job = ref('')
const gender = ref('')

const isValid = computed(() => {
  return (
    username.value &&
    password.value &&
    passwordConfirm.value &&
    password.value === passwordConfirm.value &&
    realName.value &&
    birthDate.value &&
    region.value &&
    job.value &&
    gender.value
  )
})


const submitSignup = () => {
  const age =
    new Date().getFullYear() -
    new Date(birthDate.value).getFullYear()

  auth.signup({
    username: username.value,
    real_name: realName.value,
    birth_date: birthDate.value,
    age,
    region: region.value,
    job: job.value,
    gender: gender.value
  })

  router.push('/')
}

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.signup-page {
  width: 100%;
  min-height: calc(100vh - 64px);
  background: #f8fafc;

  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 40px;
}

.signup-container {
  width: 100%;
  max-width: 1100px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  padding: 40px;
}

/* LEFT */
.signup-box h1 {
  font-size: 28px;
  margin-bottom: 24px;
}

.signup-box input,
.signup-box select {
  width: 100%;
  padding: 12px 14px;
  margin-bottom: 12px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  font-size: 14px;
}

.gender-box {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
}

.gender-box label {
  font-size: 14px;
  cursor: pointer;
}

.signup-btn {
  width: 100%;
  background: #3b82f6;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.signup-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.signup-btn:hover:not(:disabled) {
  background: #2563eb;
}

.login-link {
  margin-top: 16px;
  font-size: 14px;
  color: #6b7280;
}

.login-link span {
  color: #3b82f6;
  cursor: pointer;
  margin-left: 4px;
}

.field-label {
  display: block;
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 6px;
}

.error-text {
  font-size: 12px;
  color: #ef4444;
  margin-bottom: 8px;
}


/* RIGHT */
.ad-box {
  display: flex;
  justify-content: center;
  align-items: top;
  padding-top: 65px;
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

/* MOBILE */
@media (max-width: 768px) {
  .signup-container {
    grid-template-columns: 1fr;
  }

  .ad-box {
    display: none;
  }
}
</style>
