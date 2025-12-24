<template>
  <AppNavbar />

  <main class="thread-edit-page">
    <section class="thread-edit-card">
      <h1 class="edit-title">게시글 작성</h1>

      <!-- ✅ 관련 정책 표시 -->
      <p v-if="policy" class="policy-info">
        관련 정책: <strong>{{ policy.plcyNm }}</strong>
      </p>
      
      <form @submit.prevent="submit" class="edit-form">
        <!-- 제목 -->
        <label class="label">제목</label>
        <input
          v-model="title"
          class="input"
          placeholder="게시글 제목을 입력하세요"
          required
        />

        <!-- 내용 -->
        <label class="label">내용</label>
        <textarea
          v-model="content"
          class="textarea"
          placeholder="게시글 내용을 입력하세요"
          required
        />

        <div class="actions">
          <button
            type="button"
            class="ghost"
            @click="router.back()"
          >
            취소
          </button>

          <button
            type="submit"
            class="primary"
            :disabled="loading"
          >
            {{ loading ? '작성 중...' : '등록하기' }}
          </button>
        </div>
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
    })

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
.thread-edit-page {
  min-height: 100vh;
  background: #f8fafc;
}

.thread-edit-card {
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
