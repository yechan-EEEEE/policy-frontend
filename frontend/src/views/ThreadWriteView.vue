<template>
  <AppNavbar />

  <main class="thread-write-page">
    <section class="thread-write-container">
      <h1 class="page-title">게시글 작성</h1>

      <!-- ✅ 정책 이름 표시 -->
      <p class="policy-info" v-if="policy">
        관련 정책: <strong>{{ policy.plcyNm }}</strong>
      </p>

      <form @submit.prevent="submit">
        <!-- 제목 -->
        <div class="form-group">
          <label>제목</label>
          <input
            v-model="title"
            placeholder="게시글 제목을 입력하세요"
            required
          />
        </div>

        <!-- 내용 -->
        <div class="form-group">
          <label>내용</label>
          <textarea
            v-model="content"
            placeholder="게시글 내용을 입력하세요"
            required
          />
        </div>

        <button class="primary" :disabled="loading">
          {{ loading ? '작성 중...' : '등록하기' }}
        </button>
      </form>
    </section>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/thread'
import { usePolicyStore } from '@/stores/policy'
import AppNavbar from '@/components/common/AppNavbar.vue'

const route = useRoute()
const router = useRouter()

const threadStore = useThreadStore()
const policyStore = usePolicyStore()

const plcyNo = route.params.plcyNo

const title = ref('')
const content = ref('')
const loading = ref(false)

// ✅ 정책 상세 가져오기
onMounted(() => {
  policyStore.fetchPolicyDetail(plcyNo)
})

const policy = computed(() => policyStore.policyDetail)

const submit = async () => {
  if (!title.value || !content.value) return

  loading.value = true
  try {
    await threadStore.createThread({
      title: title.value,
      content: content.value,
      policy: plcyNo,
    })

    // 작성 후 정책 상세로 이동
    router.push(`/policies/${plcyNo}`)
  } catch (err) {
    console.error(err)
    alert('글 작성에 실패했습니다.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.thread-write-page {
  min-height: 100vh;
  background: #f8fafc;
}

.thread-write-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 24px;
  background: #ffffff;
  border-radius: 12px;
}

.page-title {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 16px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-size: 14px;
  font-weight: 600;
}

input, textarea, select {
  width: 100%;
  padding: 12px 14px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

textarea {
  min-height: 160px;
}

.policy-meta {
  margin-top: 6px;
  font-size: 13px;
  color: #6b7280;
}

.submit-btn {
  width: 100%;
  padding: 14px;
  border-radius: 8px;
  background: #2563eb;
  color: white;
  font-size: 16px;
  border: none;
  cursor: pointer;
}

.submit-btn:hover {
  background: #1d4ed8;
}
</style>
