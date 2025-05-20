<template>
  <div class="bg-background min-h-screen py-8">
    <div class="container mx-auto px-4">
      <h1 class="text-3xl font-bold mb-8">仪表盘</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <!-- 今日卡片概览 -->
        <div class="card bg-white col-span-2">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold">今日卡片</h2>
            <router-link to="/daily-card" class="text-primary text-sm">查看详情</router-link>
          </div>
          
          <div v-if="loadingCard" class="py-8 text-center">
            <svg class="animate-spin h-8 w-8 text-primary mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          
          <div v-else-if="!todayCard" class="py-8 text-center">
            <p class="text-text/70 mb-4">您今天还没有创建每日卡片</p>
            <router-link to="/daily-card" class="btn btn-primary">创建今日卡片</router-link>
          </div>
          
          <div v-else>
            <div class="space-y-3 mb-6">
              <div v-for="task in todayCard.tasks" :key="task.task_id" 
                   class="flex items-center p-3 border border-border rounded-md"
                   :class="{ 'bg-secondary/10 border-secondary': task.is_completed }">
                <input type="checkbox" 
                       :checked="task.is_completed"
                       @change="toggleTaskCompletion(task.task_id)"
                       class="h-5 w-5 text-secondary focus:ring-secondary/50 rounded" />
                <span class="ml-3" :class="{ 'line-through text-text/60': task.is_completed }">
                  {{ task.title }}
                </span>
              </div>
            </div>
            
            <div class="flex justify-between items-center text-sm text-text/70">
              <span>{{ completedTasksCount }} / {{ todayCard.tasks.length }} 已完成</span>
              <span>{{ formatDate(todayCard.date) }}</span>
            </div>
          </div>
        </div>
        
        <!-- 任务统计 -->
        <div class="card bg-white">
          <h2 class="text-xl font-semibold mb-4">任务统计</h2>
          
          <div v-if="loadingTasks" class="py-8 text-center">
            <svg class="animate-spin h-8 w-8 text-primary mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          
          <div v-else class="space-y-4">
            <div class="flex justify-between items-center p-3 bg-primary/10 rounded-md">
              <span class="font-medium">待办任务</span>
              <span class="text-lg font-semibold">{{ todoTasksCount }}</span>
            </div>
            
            <div class="flex justify-between items-center p-3 bg-accent/10 rounded-md">
              <span class="font-medium">关注任务</span>
              <span class="text-lg font-semibold">{{ watchTasksCount }}</span>
            </div>
            
            <div class="flex justify-between items-center p-3 bg-secondary/10 rounded-md">
              <span class="font-medium">已完成任务</span>
              <span class="text-lg font-semibold">{{ completedTasksTotal }}</span>
            </div>
            
            <router-link to="/tasks" class="btn btn-outline w-full mt-4">
              管理所有任务
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- 最近任务 -->
      <div class="card bg-white">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">最近任务</h2>
          <router-link to="/tasks" class="text-primary text-sm">查看全部</router-link>
        </div>
        
        <div v-if="loadingTasks" class="py-8 text-center">
          <svg class="animate-spin h-8 w-8 text-primary mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        
        <div v-else-if="recentTasks.length === 0" class="py-8 text-center">
          <p class="text-text/70">暂无任务</p>
          <router-link to="/tasks" class="btn btn-primary mt-4">创建新任务</router-link>
        </div>
        
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-border">
            <thead class="bg-background">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-text/70 uppercase tracking-wider">
                  任务名称
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-text/70 uppercase tracking-wider">
                  列表
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-text/70 uppercase tracking-wider">
                  优先级
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-text/70 uppercase tracking-wider">
                  截止日期
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-text/70 uppercase tracking-wider">
                  状态
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-border">
              <tr v-for="task in recentTasks" :key="task.id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-text">{{ task.title }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                        :class="{
                          'bg-primary/10 text-primary': task.list_type === 'todo',
                          'bg-accent/10 text-accent': task.list_type === 'watch',
                          'bg-gray-100 text-gray-800': task.list_type === 'later'
                        }">
                    {{ listTypeText(task.list_type) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-text/70">
                    {{ task.priority ? `P${task.priority}` : '-' }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-text/70">
                    {{ task.due_date ? formatDate(task.due_date) : '-' }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                        :class="{
                          'bg-secondary/10 text-secondary': task.is_completed,
                          'bg-gray-100 text-gray-800': !task.is_completed
                        }">
                    {{ task.is_completed ? '已完成' : '进行中' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTaskStore } from '@/store/tasks'
import { useDailyCardStore } from '@/store/dailyCard'

const taskStore = useTaskStore()
const dailyCardStore = useDailyCardStore()

// 加载状态
const loadingTasks = computed(() => taskStore.loading)
const loadingCard = computed(() => dailyCardStore.loading)

// 今日卡片
const todayCard = computed(() => dailyCardStore.todayCard)
const completedTasksCount = computed(() => {
  if (!todayCard.value) return 0
  return todayCard.value.tasks.filter(task => task.is_completed).length
})

// 任务统计
const todoTasksCount = computed(() => taskStore.getTodoTasks.length)
const watchTasksCount = computed(() => taskStore.getWatchTasks.length)
const completedTasksTotal = computed(() => {
  return [
    ...taskStore.getTodoTasks,
    ...taskStore.getWatchTasks,
    ...taskStore.getLaterTasks
  ].filter(task => task.is_completed).length
})

// 最近任务
const recentTasks = computed(() => {
  const allTasks = [
    ...taskStore.getTodoTasks,
    ...taskStore.getWatchTasks,
    ...taskStore.getLaterTasks
  ]
  
  // 按创建时间排序，最新的在前
  return allTasks
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, 5) // 只显示最近5个
})

// 方法
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const listTypeText = (type) => {
  const types = {
    todo: '待办',
    watch: '关注',
    later: '稍后'
  }
  return types[type] || type
}

const toggleTaskCompletion = async (taskId) => {
  await dailyCardStore.completeCardTask(taskId)
}

// 生命周期钩子
onMounted(async () => {
  // 获取任务数据
  await taskStore.fetchTasks()
  
  // 获取今日卡片
  await dailyCardStore.fetchTodayCard()
})
</script>
