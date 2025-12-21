<template>
  <AppNavbar />

  <main class="edit-page">
    <div class="edit-container">
      <section class="edit-box">
        <h1>정보 수정</h1>

        <div class="form-group">
            <label>아이디</label>
            <input v-model="username" disabled />
        </div>

        <div class="form-group">
            <label>비밀번호 변경</label>
            <input
            v-model="password"
            type="password"
            placeholder="새 비밀번호 (변경 시 입력)"
            />
            <input
            v-model="passwordConfirm"
            type="password"
            placeholder="비밀번호 확인"
            />
        </div>

        <div class="form-group">
            <label>이름</label>
            <input v-model="realName" />
        </div>

        <div class="form-group">
            <label>생년월일</label>
            <div class="birth-select">
        <select v-model="birthYear">
            <option disabled value="">연도</option>
            <option
            v-for="year in years"
            :key="year"
            :value="year"
            >
            {{ year }}
            </option>
        </select>

        <select v-model="birthMonth">
            <option disabled value="">월</option>
            <option
            v-for="month in 12"
            :key="month"
            :value="month"
            >
            {{ month }}
            </option>
        </select>

        <select v-model="birthDay">
            <option disabled value="">일</option>
            <option
            v-for="day in daysInMonth"
            :key="day"
            :value="day"
            >
            {{ day }}
            </option>
        </select>
        </div>
        </div>

        <div class="form-group">
            <label>지역</label>
            <select v-model="region">
          <option disabled value="">지역 선택</option>
          <option value="서울">서울</option>
          <option value="경기">경기</option>
          <option value="인천">인천</option>
          <option value="부산">부산</option>
        </select>
        </div>

        <div class="form-group">
            <label>직업</label>
            <select v-model="job">
        <option disabled value="">직업 선택</option>
        <option value="학생">학생</option>
        <option value="취업준비생">취업준비생</option>
        <option value="직장인">직장인</option>
        <option value="자영업자">자영업자</option>
        <option value="프리랜서">프리랜서</option>
        <option value="기타">기타</option>
        </select>
        </div>

        <div class="form-group">
            <label>성별</label>
            <select v-model="gender">
          <option disabled value="">성별 선택</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>
        </div>

        <button
            class="save-btn"
            :disabled="!isValid"
            @click="submitEdit"
        >
            저장
        </button>
        </section>

    </div>
  </main>
</template>


<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/common/AppNavbar.vue'

const router = useRouter()
const auth = useAuthStore()

// auth.user 방어
const user = computed(() => auth.user || {})

// 기본 정보
const username = ref(user.value.username || '')
const realName = ref(user.value.real_name || '')
const region = ref(user.value.region || '')
const job = ref(user.value.job || '')
const gender = ref(user.value.gender || '')

const password = ref('')
const passwordConfirm = ref('')

// ⭐ 생년월일 안전 처리 (핵심)
const birthDate = user.value.birth_date || '2000-01-01'
const [y, m, d] = birthDate.split('-')

const birthYear = ref(Number(y))
const birthMonth = ref(Number(m))
const birthDay = ref(Number(d))

const currentYear = new Date().getFullYear()
const years = Array.from({ length: currentYear - 1949 }, (_, i) => currentYear - i)

const daysInMonth = computed(() => {
  if (!birthYear.value || !birthMonth.value) return []
  return new Date(birthYear.value, birthMonth.value, 0).getDate()
})

const isValid = computed(() => {
  if (password.value || passwordConfirm.value) {
    if (password.value !== passwordConfirm.value) return false
  }

  return (
    realName.value &&
    birthYear.value &&
    birthMonth.value &&
    birthDay.value &&
    region.value &&
    job.value &&
    gender.value
  )
})

const submitEdit = () => {
  const birth_date =
    `${birthYear.value}-${String(birthMonth.value).padStart(2, '0')}-${String(birthDay.value).padStart(2, '0')}`

  const age = new Date().getFullYear() - new Date(birth_date).getFullYear()

  auth.login({
    user: {
      ...user.value,
      real_name: realName.value,
      birth_date,
      age,
      region: region.value,
      job: job.value,
      gender: gender.value
    },
    token: auth.token
  })

  router.push('/mypage')
}
</script>



<style scoped>
.edit-page {
  width: 100%;
  min-height: calc(100vh - 64px);
  background: #f8fafc;
  display: flex;
  justify-content: center;
  padding-top: 30px;
}

.edit-container {
  width: 100%;
  max-width: 520px;
  padding: 0 20px;
}

/* 카드 느낌 */
.edit-box {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 32px;
}

.edit-box h1 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 28px;
}

/* 폼 그룹 */
.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 6px;
}

.edit-box input,
.edit-box select {
  width: 100%;
  padding: 12px 14px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  font-size: 14px;
}

/* 생년월일 */
.birth-select {
  display: flex;
  gap: 8px;
}

.birth-select select {
  flex: 1;
}

/* 저장 버튼 */
.save-btn {
  width: 100%;
  margin-top: 12px;
  padding: 12px;
  border-radius: 8px;
  background: #2563eb;
  color: white;
  font-size: 15px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.save-btn:hover:not(:disabled) {
  background: #1d4ed8;
}

.save-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

</style>