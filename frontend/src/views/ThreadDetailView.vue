<template>
  <AppNavbar />

  <main v-if="thread">
    <section class="card">
      <h1>{{ thread.title }}</h1>

      <div class="meta">
        <span>{{ thread.author?.username || thread.author }}</span>
        <span>{{ thread.created_at }}</span>
      </div>

      <p class="content">{{ thread.content }}</p>

      <div class="actions">
        <button @click="goBack">목록으로</button>

        <button
          v-if="auth.user?.id === thread.author?.id"
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

const goEdit = () => {
  router.push(`/threads/${route.params.threadId}/edit`)
}

const goBack = () => {
  router.back()
}
</script>


<style scoped>
.thread-detail-container {
  max-width: 900px;
  margin: 40px auto;
}

.meta {
  display: flex;
  gap: 16px;
  color: #6b7280;
  font-size: 14px;
}

.content {
  margin: 24px 0;
  line-height: 1.7;
}

.actions {
  display: flex;
  gap: 10px;
}

.danger {
  color: white;
  background: #ef4444;
}
</style>
