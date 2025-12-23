<template>
  <AppNavbar />

  <main class="edit-page">
    <div class="edit-container">
      <section class="edit-box" v-if="auth.user">
        <h1>정보 수정</h1>

        <!-- 아이디 (수정 불가) -->
        <div class="form-group">
          <label>아이디</label>
          <input :value="auth.user.username" disabled />
        </div>

        <!-- 이름 -->
        <div class="form-group">
          <label>이름</label>
          <input v-model="form.real_name" />
        </div>

        <!-- 생년월일 -->
        <div class="form-group">
          <label>생년월일</label>
          <div class="birth-select">
            <select v-model="birthYear">
              <option disabled value="">연도</option>
              <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
            </select>

            <select v-model="birthMonth">
              <option disabled value="">월</option>
              <option v-for="m in 12" :key="m" :value="m">{{ m }}</option>
            </select>

            <select v-model="birthDay">
              <option disabled value="">일</option>
              <option v-for="d in daysInMonth" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>
        </div>

        <!-- 지역 -->
        <div class="form-group">
          <label>지역</label>
          <select v-model="form.region">
            <option disabled value="">지역 선택</option>

            <option value="서울특별시">서울특별시</option>
            <option value="부산광역시">부산광역시</option>
            <option value="대구광역시">대구광역시</option>
            <option value="인천광역시">인천광역시</option>
            <option value="광주광역시">광주광역시</option>
            <option value="대전광역시">대전광역시</option>
            <option value="울산광역시">울산광역시</option>
            <option value="세종특별자치시">세종특별자치시</option>
            <option value="경기도">경기도</option>
            <option value="강원특별자치도">강원특별자치도</option>
            <option value="충청북도">충청북도</option>
            <option value="충청남도">충청남도</option>
            <option value="전북특별자치도">전북특별자치도</option>
            <option value="전라남도">전라남도</option>
            <option value="경상북도">경상북도</option>
            <option value="경상남도">경상남도</option>
            <option value="제주특별자치도">제주특별자치도</option>
          </select>
        </div>


        <!-- 직업 -->
        <div class="form-group">
          <label>직업</label>
          <select v-model="form.job">
            <option disabled value="">직업 선택</option>
            <option value="학생">학생</option>
            <option value="취업준비생">취업준비생</option>
            <option value="직장인">직장인</option>
            <option value="자영업자">자영업자</option>
            <option value="프리랜서">프리랜서</option>
            <option value="기타">기타</option>
          </select>
        </div>

        <!-- 성별 -->
        <div class="form-group">
          <label>성별</label>
          <select v-model="form.gender">
            <option disabled value="">성별 선택</option>
            <option value="M">남성</option>
            <option value="F">여성</option>
          </select>
        </div>

        <button
          class="save-btn"
          :disabled="loading"
          @click="submit"
        >
          {{ loading ? '저장 중...' : '저장' }}
        </button>
      </section>

      <div v-else class="loading">
        사용자 정보를 불러오는 중입니다...
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import AppNavbar from '@/components/common/AppNavbar.vue'

const router = useRouter()
const auth = useAuthStore()

/* ===== 로컬 form state (serializer 기준) ===== */
const form = ref({
  real_name: '',
  birth_date: '',
  region: '',
  job: '',
  gender: '',
})

/* ===== 생년월일 분해용 ===== */
const birthYear = ref('')
const birthMonth = ref('')
const birthDay = ref('')

const loading = ref(false)

/* ===== 연도/일 계산 ===== */
const years = computed(() => {
  const current = new Date().getFullYear()
  return Array.from({ length: 80 }, (_, i) => current - i)
})

const daysInMonth = computed(() => {
  if (!birthYear.value || !birthMonth.value) return []
  return new Date(birthYear.value, birthMonth.value, 0).getDate()
})

/* ===== 초기 값 세팅 ===== */
onMounted(() => {
  if (!auth.user) return

  form.value.real_name = auth.user.real_name || ''
  form.value.region = auth.user.region || ''
  form.value.job = auth.user.job || ''
  form.value.gender = auth.user.gender || ''

  if (auth.user.birth_date) {
    const [y, m, d] = auth.user.birth_date.split('-')
    birthYear.value = y
    birthMonth.value = Number(m)
    birthDay.value = Number(d)
  }
})

/* ===== 저장 ===== */
const submit = async () => {
  loading.value = true
  try {
    if (birthYear.value && birthMonth.value && birthDay.value) {
      form.value.birth_date =
        `${birthYear.value}-${String(birthMonth.value).padStart(2,'0')}-${String(birthDay.value).padStart(2,'0')}`
    }

    const res = await api.patch('/accounts/profile/', {
      real_name: form.value.real_name,
      birth_date: form.value.birth_date,
      region: form.value.region,
      job: form.value.job,
      gender: form.value.gender,
    })

    auth.user = res.data
    router.push('/mypage')
  } catch (e) {
    alert('회원 정보 수정에 실패했습니다.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.edit-page {
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

.birth-select {
  display: flex;
  gap: 8px;
}

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
}

.save-btn:disabled {
  background: #94a3b8;
}
</style>
