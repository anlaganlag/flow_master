<template>
  <div class="min-h-screen flex items-center justify-center bg-background py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full text-center">
      <h1 class="text-9xl font-bold text-primary">404</h1>
      <h2 class="mt-4 text-3xl font-extrabold text-text">页面未找到</h2>
      <p class="mt-2 text-text/70">
        抱歉，您请求的页面不存在或已被移除。
      </p>
      <div class="mt-6">
        <router-link to="/" class="btn btn-primary">
          返回首页
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// 404页面不需要特殊逻辑
</script>
