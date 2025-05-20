<template>
  <div class="bg-gradient-to-b from-primary/10 to-background min-h-screen">
    <div class="container mx-auto px-4 py-16">
      <div class="max-w-4xl mx-auto text-center">
        <h1 class="text-4xl md:text-5xl font-bold text-text mb-6">
          高效管理任务，专注于重要事务
        </h1>
        <p class="text-xl text-text/80 mb-10">
          FlowMaster帮助您优先处理有意义的工作，通过灵活、直观的时间和任务管理方法减少干扰，提高工作效率。
        </p>
        
        <div class="flex flex-col sm:flex-row justify-center gap-4 mb-16">
          <router-link to="/register" class="btn btn-primary text-lg px-8 py-3">
            免费开始使用
          </router-link>
          <router-link to="/login" class="btn btn-outline text-lg px-8 py-3">
            登录账户
          </router-link>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8 text-left">
          <div class="card bg-white/80 backdrop-blur">
            <div class="text-primary text-2xl mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">三列表系统</h3>
            <p class="text-text/80">
              将任务组织到待办、关注和稍后三个列表中，确保您始终关注最重要的事务。
            </p>
          </div>
          
          <div class="card bg-white/80 backdrop-blur">
            <div class="text-secondary text-2xl mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">每日卡片系统</h3>
            <p class="text-text/80">
              每天创建一张限制为3-5个关键任务的数字卡片，帮助您专注于当天最重要的工作。
            </p>
          </div>
          
          <div class="card bg-white/80 backdrop-blur">
            <div class="text-accent text-2xl mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">智能任务优先级</h3>
            <p class="text-text/80">
              基于您的习惯和行为模式，智能推荐任务优先级和每日计划，帮助您做出更好的决策。
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 首页不需要特殊逻辑
</script>
