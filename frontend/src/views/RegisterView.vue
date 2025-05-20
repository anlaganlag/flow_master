<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-primary/10 to-background py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-text">
          创建新账户
        </h2>
        <p class="mt-2 text-center text-sm text-text/70">
          或
          <router-link to="/login" class="font-medium text-primary hover:text-primary/80">
            登录现有账户
          </router-link>
        </p>
      </div>
      
      <div v-if="error" class="bg-error/10 border border-error text-error px-4 py-3 rounded relative" role="alert">
        <span class="block sm:inline">{{ error }}</span>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="rounded-md shadow-sm space-y-4">
          <div>
            <label for="username" class="form-label">用户名</label>
            <input id="username" name="username" type="text" autocomplete="username" required
                   v-model="username"
                   class="form-input" />
          </div>
          
          <div>
            <label for="email" class="form-label">邮箱地址</label>
            <input id="email" name="email" type="email" autocomplete="email" required
                   v-model="email"
                   class="form-input" />
          </div>
          
          <div>
            <label for="password" class="form-label">密码</label>
            <input id="password" name="password" type="password" autocomplete="new-password" required
                   v-model="password"
                   class="form-input" />
            <p class="mt-1 text-sm text-text/70">密码至少需要8个字符</p>
          </div>
          
          <div>
            <label for="confirmPassword" class="form-label">确认密码</label>
            <input id="confirmPassword" name="confirmPassword" type="password" autocomplete="new-password" required
                   v-model="confirmPassword"
                   class="form-input" />
          </div>
        </div>

        <div class="flex items-center">
          <input id="terms" name="terms" type="checkbox" required
                 v-model="agreeTerms"
                 class="h-4 w-4 text-primary focus:ring-primary/50 border-border rounded" />
          <label for="terms" class="ml-2 block text-sm text-text/80">
            我同意 <a href="#" class="text-primary">服务条款</a> 和 <a href="#" class="text-primary">隐私政策</a>
          </label>
        </div>

        <div>
          <button type="submit" 
                  :disabled="loading || !isFormValid"
                  class="w-full btn btn-primary py-3 relative">
            <span v-if="loading" class="absolute left-4 top-1/2 transform -translate-y-1/2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()

// 表单数据
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const agreeTerms = ref(false)

// 计算属性
const loading = computed(() => authStore.loading)
const error = computed(() => authStore.error)

// 表单验证
const isFormValid = computed(() => {
  return (
    username.value.length >= 3 &&
    email.value.includes('@') &&
    password.value.length >= 8 &&
    password.value === confirmPassword.value &&
    agreeTerms.value
  )
})

// 处理注册
const handleRegister = async () => {
  if (!isFormValid.value) return
  
  const success = await authStore.register({
    username: username.value,
    email: email.value,
    password: password.value
  })
  
  if (success) {
    router.push('/dashboard')
  }
}
</script>
