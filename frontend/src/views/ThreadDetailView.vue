<template>
  <AppNavbar />

  <main class="thread-detail-page" v-if="thread">
    <section class="thread-card">
      <h1 class="thread-title">{{ thread.title }}</h1>

      <div class="thread-meta">
        <span>✍ {{ thread.author_username || thread.author }}</span>
        <span>·</span>
        <span>{{ formatDate(thread.created_at) }}</span>
      </div>

      <div class="thread-content">
        {{ thread.content }}
      </div>

      <div class="thread-actions">
        <button
          class="like-btn"
          :class="{ liked: thread.is_liked }"
          @click="toggleLike"
          :disabled="!auth.isLogin"
        >
          {{ thread.is_liked ? '❤️' : '🤍' }}
          {{ thread.liked_count }}
        </button>

        <button class="ghost" @click="goBack">목록으로</button>

        <button
          v-if="auth.user?.id === thread.author"
          class="primary"
          @click="goEdit"
        >
          수정
        </button>
      </div>

    </section>
  </main>

  <div v-else class="loading">
    게시글을 불러오는 중입니다...
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/thread'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/common/AppNavbar.vue'

const route = useRoute()
const router = useRouter()
const threadStore = useThreadStore()
const auth = useAuthStore()

onMounted(() => {
  threadStore.fetchThreadDetail(route.params.threadId)
})

const thread = computed(() => threadStore.threadDetail)

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString()
}

const goEdit = () => {
  router.push(`/threads/${route.params.threadId}/edit`)
}

const goBack = () => {
  router.push('/threads')
}

const toggleLike = async () => {
  if (!auth.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    const res = await threadStore.toggleLike(thread.value.id)

    // 🔥 즉시 UI 반영
    thread.value.is_liked = res.liked
    thread.value.liked_count = res.liked_count
  } catch (err) {
    console.error(err)
    alert('좋아요 처리에 실패했습니다.')
  }
}

</script>

<style scoped>
.thread-detail-page {
  min-height: calc(100vh - 64px);
  background: radial-gradient(circle at top, #0b1437, #020617);
  padding: 60px 20px;
}

.thread-card {
  max-width: 820px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 16px;
  padding: 36px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
}

.thread-title {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 12px;
}

.thread-meta {
  display: flex;
  gap: 8px;
  font-size: 14px;
  color: #64748b;
  margin-bottom: 24px;
}

.thread-content {
  font-size: 16px;
  line-height: 1.8;
  color: #334155;
  white-space: pre-wrap;
  margin-bottom: 40px;
}

.thread-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

button {
  padding: 10px 18px;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  border: none;
}

button.primary {
  background: #2563eb;
  color: #fff;
}

button.primary:hover {
  background: #1d4ed8;
}

button.ghost {
  background: transparent;
  color: #2563eb;
}

button.ghost:hover {
  background: #eff6ff;
}

.loading {
  padding: 100px;
  text-align: center;
  color: #cbd5f5;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border-radius: 999px;
  font-size: 15px;
  background: #f1f5f9;
  color: #0f172a;
  cursor: pointer;
}

.like-btn.liked {
  background: #fee2e2;
  color: #dc2626;
}

.like-btn:hover {
  background: #e2e8f0;
}

/* 모바일 */
@media (max-width: 640px) {
  .thread-card {
    padding: 24px;
  }

  .thread-title {
    font-size: 22px;
  }
}
</style>
