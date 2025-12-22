<template>
  <AppNavbar />

  <main v-if="thread" class="thread-edit-page">
    <section class="thread-edit-container">
      <h1>게시글 수정</h1>

      <form @submit.prevent="submit">
        <input v-model="title" />
        <textarea v-model="content" />

        <button>수정 완료</button>
      </form>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/thread'
import AppNavbar from '@/components/common/AppNavbar.vue'

const route = useRoute()
const router = useRouter()
const store = useThreadStore()

const id = route.params.id

const title = ref('')
const content = ref('')
const thread = ref(null)

onMounted(async () => {
  thread.value = await store.fetchThread(id)
  title.value = thread.value.title
  content.value = thread.value.content
})

const submit = async () => {
  await store.updateThread(id, {
    title: title.value,
    content: content.value,
  })
  router.push(`/threads/${id}`)
}
</script>
