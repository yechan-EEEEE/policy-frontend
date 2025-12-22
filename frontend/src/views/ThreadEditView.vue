<template>
  <AppNavbar />

  <main v-if="thread" class="thread-edit-page">
    <section class="thread-edit-container">
      <h1>게시글 수정</h1>

      <form @submit.prevent="submit">
        <input v-model="title" />
        <textarea v-model="content" />

        <button
          class="primary"
          :disabled="loading"
          @click="submit"
        >
          {{ loading ? '수정 중...' : '수정 완료' }}
        </button>

      </form>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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

onMounted(async () => {
  await threadStore.fetchThreadDetail(route.params.threadId)

  const thread = threadStore.threadDetail
  if (!thread) return

  // 본인 글 아니면 접근 차단 (UI 레벨)
  if (auth.user?.id !== thread.author?.id) {
    alert('수정 권한이 없습니다.')
    router.back()
    return
  }

  title.value = thread.title
  content.value = thread.content
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