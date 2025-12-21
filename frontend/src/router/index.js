import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

import PoliciesListView from '@/views/PoliciesListView.vue'
import PolicyDetailView from '@/views/PolicyDetailView.vue'

import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import MyPageView from '@/views/MyPageView.vue'

import ThreadsListView from '@/views/ThreadsListView.vue'
import ThreadWriteView from '@/views/ThreadWriteView.vue'
import ThreadDetailView from '@/views/ThreadDetailView.vue'
import ThreadEditView from '@/views/ThreadEditView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', name: 'home', component: HomeView},

        { path: '/policies', name: 'policies', component: PoliciesListView},
        { path: '/policies/:policyId', name: 'policyDetail', component: PolicyDetailView},

        { path: '/signup', name: 'signup', component: SignupView},
        { path: '/login', name: 'login', component: LoginView},
        { path: '/mypage', name: 'mypage', component: MyPageView},

        { path: '/threads', name: 'threads', component: ThreadsListView},
        { path: '/threads/:policyId/write', name: 'threadWrite', component: ThreadWriteView},
        { path: '/threads/:threadId', name: 'threadDetail', component: ThreadDetailView},
        { path: '/threads/:threadId/edit', name: 'threadEdit', component: ThreadEditView},

    ]
})

export default router