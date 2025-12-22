<template>
  <AppNavbar />

  <main class="thread-detail-page" v-if="thread">
    <section class="thread-detail-container">
      <h1 class="title">{{ thread.title }}</h1>

      <div class="meta">
        <span>{{ thread.policy.category }} / {{ thread.policy.subTitle }}</span>
        <span>👍 {{ thread.likes_count }}</span>
      </div>

      <div class="content">
        {{ thread.content }}
      </div>

      <div class="actions" v-if="isAuthor">
        <button @click="goEdit">수정</button>
        <button class="danger" @click="remove">삭제</button>
      </div>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/thread'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/common/AppNavbar.vue'

const route = useRoute()
const router = useRouter()
const threadStore = useThreadStore()
const auth = useAuthStore()

const threadId = route.params.id

onMounted(async () => {
  await threadStore.fetchThread(threadId)
})

const thread = computed(() =>
  threadStore.getById(threadId)
)

const isAuthor = computed(() =>
  auth.user && thread.value?.author?.id === auth.user.id
)

const goEdit = () => {
  router.push(`/threads/${threadId}/edit`)
}

const remove = async () => {
  if (!confirm('정말 삭제할까요?')) return
  await threadStore.deleteThread(threadId)
  router.push('/threads')
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
