<template>
  <AppNavbar />

  <main class="thread-detail-page" v-if="thread">
    <section class="thread-card">
      <h1 class="thread-title">{{ thread.title }}</h1>

      <div class="thread-meta">
        <span>✍ {{ thread.author_username ?? '알 수 없음' }}</span>
        <span>·</span>
        <span>{{ formatDate(thread.created_at) }}</span>
      </div>

      <div class="thread-content">
        {{ thread.content }}
      </div>

      <div class="actions">
        <button
          class="like-btn"
          :class="{ liked: thread.is_liked }"
          @click="toggleLike"
        >
          {{ thread.is_liked ? '❤️' : '🤍' }} 좋아요
          {{ thread.liked_count }}
        </button>

        <button @click="goBack">목록으로</button>

        <button
          v-if="auth.user?.username === thread.author_username"
          @click="goEdit"
        >
          수정
        </button>
      </div>
    </section>

    <!-- 댓글 영역 -->
    <section class="comment-section">
      <h3 class="comment-title">
        댓글 <span>{{ commentStore.comments.length }}</span>
      </h3>

      <!-- 댓글 작성 -->
      <div class="comment-write-card">
        <textarea
          v-model="newComment"
          placeholder="댓글을 입력하세요"
        />
        <button
          class="comment-submit"
          :disabled="!newComment.trim()"
          @click="submitComment"
        >
          등록
        </button>
      </div>

      <!-- 댓글 목록 -->
      <div
        v-for="c in commentStore.comments"
        :key="c.id"
        class="comment-card"
      >
        <div class="comment-header">
          <strong class="comment-author">
            {{ c.author_username }}
          </strong>
          <span class="comment-date">
            {{ new Date(c.created_at).toLocaleString() }}
          </span>
        </div>

        <p
          v-if="editingCommentId !== c.id"
          class="comment-content"
        >
          {{ c.content }}
        </p>

        <textarea
          v-else
          v-model="editingContent"
          class="comment-edit-textarea"
        ></textarea>

        <div class="comment-actions">
          <!-- 좋아요 -->
          <button
            class="comment-like"
            :class="{ liked: c.is_liked }"
            @click="toggleCommentLike(c.id)"
          >
            {{ c.is_liked ? '❤️' : '🤍' }}
            {{ c.liked_count }}
          </button>

          <!-- 내 댓글일 때 -->
          <template v-if="auth.user?.id === c.author">
            <!-- 수정 시작 -->
            <button
              v-if="editingCommentId !== c.id"
              class="comment-edit"
              @click="startEditComment(c)"
            >
              수정
            </button>

            <!-- 수정 중 -->
            <template v-else>
              <button
                class="comment-save"
                @click="saveEditComment(c.id)"
              >
                저장
              </button>
              <button
                class="comment-cancel"
                @click="cancelEditComment"
              >
                취소
              </button>
            </template>

            <!-- 삭제 -->
            <button
              v-if="editingCommentId !== c.id"
              class="comment-delete"
              @click="deleteComment(c.id)"
            >
              삭제
            </button>
          </template>
        </div>

      </div>
    </section>
  </main>

  <div v-else class="loading">
    게시글을 불러오는 중입니다...
  </div>

</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/thread'
import { useAuthStore } from '@/stores/auth'
import { useCommentStore } from '@/stores/comment'
import AppNavbar from '@/components/common/AppNavbar.vue'

const route = useRoute()
const router = useRouter()
const threadStore = useThreadStore()
const auth = useAuthStore()
const commentStore = useCommentStore()
const newComment = ref('')
const editingCommentId = ref(null)
const editingContent = ref('')

onMounted(async () => {
  await threadStore.fetchThreadDetail(route.params.threadId)
  await commentStore.fetchComments(route.params.threadId)
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
    const res = await threadStore.toggleLike(route.params.threadId)
    thread.value.is_liked = res.is_liked
    thread.value.liked_count = res.liked_count
  } catch {
    alert('로그인이 필요합니다.')
  }
}
const submitComment = async () => {
  if (!auth.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }

  if (!newComment.value.trim()) return

  await commentStore.createComment(
    route.params.threadId,
    newComment.value
  )
  newComment.value = ''
}

const deleteComment = async (id) => {
  if (!confirm('댓글을 삭제할까요?')) return
  await commentStore.deleteComment(id)
}

const toggleCommentLike = async (id) => {
  if (!auth.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }
  await commentStore.toggleLike(id)
}
const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editingContent.value = comment.content
}

const cancelEditComment = () => {
  editingCommentId.value = null
  editingContent.value = ''
}

const saveEditComment = async (commentId) => {
  if (!editingContent.value.trim()) return

  await commentStore.updateComment(
    commentId,
    editingContent.value
  )

  editingCommentId.value = null
  editingContent.value = ''
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
/* ===== 댓글 섹션 ===== */
.comment-section {
  max-width: 820px;
  margin: 40px auto 0;
}

.comment-title {
  font-size: 20px;
  font-weight: 700;
  color: #f8fafc;
  margin-bottom: 16px;
}

.comment-title span {
  color: #93c5fd;
  font-weight: 600;
}

/* ===== 댓글 작성 카드 ===== */
.comment-write-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 24px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
}

.comment-write-card textarea {
  width: 100%;
  min-height: 90px;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  resize: vertical;
  font-size: 14px;
}

.comment-submit {
  margin-top: 10px;
  padding: 8px 16px;
  border-radius: 999px;
  background: #2563eb;
  color: #fff;
  border: none;
  font-size: 14px;
  cursor: pointer;
}

.comment-submit:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ===== 댓글 카드 ===== */
.comment-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 14px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

/* 헤더 */
.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.comment-author {
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
}

.comment-date {
  font-size: 12px;
  color: #64748b;
}

/* 내용 */
.comment-content {
  font-size: 15px;
  color: #334155;
  line-height: 1.6;
  margin-bottom: 12px;
  white-space: pre-wrap;
}

/* 액션 */
.comment-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.comment-like {
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 13px;
  background: #f1f5f9;
  border: none;
  cursor: pointer;
}

.comment-like.liked {
  background: #fee2e2;
  color: #dc2626;
}

.comment-delete {
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 13px;
  background: #e5e7eb;
  border: none;
  cursor: pointer;
}

.comment-delete:hover {
  background: #fecaca;
  color: #991b1b;
}
.comment-edit-textarea {
  width: 100%;
  min-height: 80px;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  font-size: 14px;
  resize: vertical;
  margin-bottom: 10px;
}

.comment-edit {
  background: #e0f2fe;
  color: #0369a1;
  border-radius: 999px;
  padding: 6px 12px;
}

.comment-save {
  background: #2563eb;
  color: #fff;
  border-radius: 999px;
  padding: 6px 12px;
}

.comment-cancel {
  background: #e5e7eb;
  border-radius: 999px;
  padding: 6px 12px;
}

/* 모바일 */
@media (max-width: 640px) {
  .thread-card {
    padding: 24px;
  }

  .thread-title {
    font-size: 22px;
  }

  .comment-section {
    padding: 0 12px;
  }
}
</style>
