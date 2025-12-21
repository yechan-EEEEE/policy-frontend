<template>
    <div>
        <h1>Signup</h1>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const birthDate = ref('')
const region = ref('')

const submitSignup = () => {
  const age =
    new Date().getFullYear() -
    new Date(birthDate.value).getFullYear()

  auth.signup({
    username: username.value,
    age,
    region: region.value
  })

  router.push('/')
}
</script>


<style scoped>

</style>