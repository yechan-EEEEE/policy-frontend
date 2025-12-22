<template>
  <AppNavbar />

  <main class="thread-write-page">
    <section class="thread-write-container">
      <h1 class="page-title">게시글 작성</h1>

      <form @submit.prevent="submitThread">
        <!-- 정책 선택 -->
        <div class="form-group">
          <label>관련 정책</label>
          <select v-model="selectedPolicyPk" required>
            <option value="">정책을 선택하세요</option>
            <option
              v-for="p in policies"
              :key="p.pk"
              :value="p.pk"
            >
              {{ p.title }}
            </option>
          </select>

          <!-- 선택된 정책 분류 표시 -->
          <p v-if="selectedPolicy" class="policy-meta">
            {{ selectedPolicy.category }} / {{ selectedPolicy.subTitle }}
          </p>
        </div>

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

        <button class="submit-btn">작성하기</button>
      </form>
    </section>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useThreadStore } from '@/stores/thread'
import { usePolicyStore } from '@/stores/policy'
import AppNavbar from '@/components/common/AppNavbar.vue'

const router = useRouter()
const route = useRoute()
const threadStore = useThreadStore()
const policyStore = usePolicyStore()

const title = ref('')
const content = ref('')
const selectedPolicyPk = ref('')

onMounted(() => {
  policyStore.loadPolicies()
  selectedPolicyPk.value = route.params.policyId
})

const policies = computed(() => policyStore.policies)

const selectedPolicy = computed(() => {
  return policyStore.getById(selectedPolicyPk.value)
})

const submitThread = async () => {
  await threadStore.createThread({
    title: title.value,
    content: content.value,
    policy: selectedPolicyPk.value,
  })

  // ✅ 작성 후 목록으로 이동
  router.push('/threads')
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
