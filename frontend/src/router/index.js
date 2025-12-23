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
    { path: '/policies/:plcyNo', name: 'policyDetail', component: PolicyDetailView },

    { path: '/signup', name: 'signup', component: SignupView, meta: { guestOnly: true } },
    { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },

    { path: '/mypage', name: 'mypage', component: MyPageView, meta: { requiresAuth: true } },
    { path: '/mypage/edit', name: 'mypageEdit', component: MyPageEditView, meta: { requiresAuth: true } },

    { path: '/threads', name: 'threads', component: ThreadsListView },
    { path: '/threads/:plcyNo/write', name: 'threadWrite', component: ThreadWriteView, meta: { requiresAuth: true } },
    { path: '/threads/:threadId', name: 'threadDetail', component: ThreadDetailView },
    { path: '/threads/:threadId/edit', name: 'threadEdit', component: ThreadEditView, meta: { requiresAuth: true } },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  // 로그인 페이지, 회원가입 페이지에서는 fetchUser 호출 ❌
  if (to.name === 'login' || to.name === 'signup') {
    return true
  }

  // 이미 로그인 상태면 다시 호출 ❌
  if (auth.isLogin) {
    return true
  }

  // 그 외에만 한 번 시도
  try {
    await auth.fetchUser()
  } catch {
    // 로그인 안 된 상태면 그냥 통과
    auth.logout()
  }

  return true
})


export default router
