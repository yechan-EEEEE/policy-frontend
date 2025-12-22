import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import HomeView from '@/views/HomeView.vue'
import PoliciesListView from '@/views/PoliciesListView.vue'
import PolicyDetailView from '@/views/PolicyDetailView.vue'

import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import MyPageView from '@/views/MyPageView.vue'
import MyPageEditView from '@/views/MyPageEditView.vue'

import ThreadsListView from '@/views/ThreadsListView.vue'
import ThreadWriteView from '@/views/ThreadWriteView.vue'
import ThreadDetailView from '@/views/ThreadDetailView.vue'
import ThreadEditView from '@/views/ThreadEditView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },

    { path: '/policies', name: 'policies', component: PoliciesListView },
    { path: '/policies/:policyId', name: 'policyDetail', component: PolicyDetailView },

    { path: '/signup', name: 'signup', component: SignupView, meta: { guestOnly: true } },
    { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },

    { path: '/mypage', name: 'mypage', component: MyPageView, meta: { requiresAuth: true } },
    { path: '/mypage/edit', name: 'mypageEdit', component: MyPageEditView, meta: { requiresAuth: true } },

    { path: '/threads', name: 'threads', component: ThreadsListView },
    { path: '/threads/:policyId/write', name: 'threadWrite', component: ThreadWriteView, meta: { requiresAuth: true } },
    { path: '/threads/:threadId', name: 'threadDetail', component: ThreadDetailView },
    { path: '/threads/:threadId/edit', name: 'threadEdit', component: ThreadEditView, meta: { requiresAuth: true } },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  // 새로고침 시 세션 복구
  if (!auth.isLogin) {
    await auth.fetchUser()
  }

  // 로그인 필요한 페이지
  if (to.meta.requiresAuth && !auth.isLogin) {
    return { name: 'login' }
  }

  // 로그인 상태에서 접근 불가
  if (to.meta.guestOnly && auth.isLogin) {
    return { name: 'home' }
  }
})

export default router
