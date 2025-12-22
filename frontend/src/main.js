import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css'
import App from './App.vue'
import { useAuthStore } from '@/stores/auth'

const app = createApp(App)
const pinia = createPinia()

app.use(createPinia())
app.use(router)

const auth = useAuthStore()
auth.fetchUser()

app.mount('#app')