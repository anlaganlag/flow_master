<template>
  <div class="min-h-screen flex flex-col">
    <header v-if="showHeader" class="bg-white shadow">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <router-link to="/" class="text-2xl font-bold text-primary">FlowMaster</router-link>
        
        <nav v-if="isAuthenticated" class="hidden md:flex space-x-6">
          <router-link to="/dashboard" class="text-text hover:text-primary">仪表盘</router-link>
          <router-link to="/tasks" class="text-text hover:text-primary">任务管理</router-link>
          <router-link to="/daily-card" class="text-text hover:text-primary">每日卡片</router-link>
        </nav>
        
        <div class="flex items-center space-x-4">
          <template v-if="isAuthenticated">
            <button @click="logout" class="btn btn-outline">退出登录</button>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-outline">登录</router-link>
            <router-link to="/register" class="btn btn-primary">注册</router-link>
          </template>
        </div>
      </div>
    </header>
    
    <main class="flex-grow">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <footer v-if="showFooter" class="bg-white border-t border-border py-6">
      <div class="container mx-auto px-4 text-center text-sm text-gray-500">
        <p>&copy; {{ new Date().getFullYear() }} FlowMaster. 保留所有权利。</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 计算属性：是否显示页眉
const showHeader = computed(() => {
  return !['Login', 'Register'].includes(route.name)
})

// 计算属性：是否显示页脚
const showFooter = computed(() => {
  return !['Login', 'Register'].includes(route.name)
})

// 计算属性：用户是否已认证
const isAuthenticated = computed(() => {
  return authStore.isAuthenticated
})

// 方法：退出登录
const logout = () => {
  authStore.logout()
  router.push('/login')
}

// 监听认证状态变化
watch(() => authStore.token, (newToken) => {
  if (newToken) {
    authStore.fetchUserProfile()
  }
})

// 组件挂载时，如果用户已登录，则获取用户信息
if (authStore.token) {
  authStore.fetchUserProfile()
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
