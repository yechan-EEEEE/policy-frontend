<template>
  <AppNavbar />

  <main class="thread-edit-page">
    <section v-if="thread" class="thread-edit-card">
      <h1 class="edit-title">게시글 수정</h1>

      <form @submit.prevent="submit" class="edit-form">
        <label class="label">제목</label>
        <input
          v-model="title"
          class="input"
          placeholder="제목을 입력하세요"
        />

        <label class="label">내용</label>
        <textarea
          v-model="content"
          class="textarea"
          placeholder="내용을 입력하세요"
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
            {{ loading ? '수정 중...' : '수정 완료' }}
          </button>
        </div>
      </form>
    </section>

    <div v-else class="loading">
      게시글을 불러오는 중입니다...
    </div>
  </main>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/thread'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/common/AppNavbar.vue'

const route = useRoute()
const router = useRouter()
const threadStore = useThreadStore()
const auth = useAuthStore()

const title = ref('')
const content = ref('')
const loading = ref(false)
const thread = computed(() => threadStore.threadDetail)

onMounted(async () => {
  await threadStore.fetchThreadDetail(route.params.threadId)

  const t = threadStore.threadDetail
  if (!t) {
    loadingPage.value = false
    return
  }

  if (auth.user?.id !== t.author) {
    alert('수정 권한이 없습니다.')
    router.back()
    return
  }

  title.value = t.title
  content.value = t.content
  loadingPage.value = false
})

const submit = async () => {
  if (!title.value || !content.value) return

  loading.value = true
  try {
    await threadStore.updateThread(route.params.threadId, {
      title: title.value,
      content: content.value,
    })

    router.push(`/threads/${route.params.threadId}`)
  } catch (err) {
    alert('수정에 실패했습니다.')
  } finally {
    loading.value = false
  }
}
</script>

<style>
/* 전체 배경 */
.thread-edit-page {
  min-height: calc(100vh - 64px);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 60px 16px;
}

/* 카드 */
.thread-edit-card {
  width: 100%;
  max-width: 720px;
  background: #ffffff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

/* 제목 */
.edit-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 24px;
  color: #111827;
}

/* 폼 */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

/* 입력 */
.input,
.textarea {
  width: 100%;
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  font-size: 15px;
  transition: border 0.2s, box-shadow 0.2s;
}

.input:focus,
.textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.textarea {
  min-height: 220px;
  resize: vertical;
}

/* 버튼 영역 */
.actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 버튼 */
.primary {
  background: #2563eb;
  color: #fff;
  border: none;
  padding: 12px 20px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.ghost {
  background: transparent;
  border: 1px solid #d1d5db;
  color: #374151;
  padding: 12px 18px;
  border-radius: 10px;
  cursor: pointer;
}

.ghost:hover {
  background: #f3f4f6;
}

/* 로딩 */
.loading {
  margin-top: 120px;
  color: #9ca3af;
  font-size: 16px;
}
</style>