import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useDailyCardStore = defineStore('dailyCard', {
  state: () => ({
    todayCard: null,
    loading: false,
    error: null
  }),
  
  getters: {
    getTodayCard: (state) => state.todayCard,
    getCardTasks: (state) => state.todayCard?.tasks || [],
    getAccomplishments: (state) => state.todayCard?.accomplishments || []
  },
  
  actions: {
    async fetchTodayCard() {
      this.loading = true
      this.error = null
      
      const authStore = useAuthStore()
      
      try {
        const response = await axios.get('/api/daily-cards/today', {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        this.todayCard = response.data
      } catch (error) {
        // 如果是404错误，说明今天还没有卡片，这不是真正的错误
        if (error.response?.status === 404) {
          this.todayCard = null
        } else {
          this.error = '获取今日卡片失败'
          console.error(error)
        }
      } finally {
        this.loading = false
      }
    },
    
    async createDailyCard(cardData) {
      this.loading = true
      this.error = null
      
      const authStore = useAuthStore()
      
      try {
        const response = await axios.post('/api/daily-cards', cardData, {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        this.todayCard = response.data
        return this.todayCard
      } catch (error) {
        this.error = '创建每日卡片失败'
        console.error(error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async updateDailyCard(cardData) {
      if (!this.todayCard) {
        this.error = '没有今日卡片可更新'
        return null
      }
      
      this.loading = true
      this.error = null
      
      const authStore = useAuthStore()
      
      try {
        const response = await axios.put(`/api/daily-cards/${this.todayCard.id}`, cardData, {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        this.todayCard = response.data
        return this.todayCard
      } catch (error) {
        this.error = '更新每日卡片失败'
        console.error(error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async addAccomplishment(accomplishmentData) {
      if (!this.todayCard) {
        this.error = '没有今日卡片可添加成就'
        return null
      }
      
      this.loading = true
      this.error = null
      
      const authStore = useAuthStore()
      
      try {
        const response = await axios.post(`/api/daily-cards/${this.todayCard.id}/accomplishments`, accomplishmentData, {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        // 更新本地卡片数据
        if (this.todayCard.accomplishments) {
          this.todayCard.accomplishments.push(response.data)
        } else {
          this.todayCard.accomplishments = [response.data]
        }
        
        return response.data
      } catch (error) {
        this.error = '添加成就失败'
        console.error(error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async completeCardTask(taskId) {
      if (!this.todayCard) {
        this.error = '没有今日卡片可更新任务'
        return false
      }
      
      const taskIndex = this.todayCard.tasks.findIndex(task => task.task_id === taskId)
      
      if (taskIndex === -1) {
        this.error = '卡片中不存在该任务'
        return false
      }
      
      // 创建更新后的任务数组
      const updatedTasks = [...this.todayCard.tasks]
      updatedTasks[taskIndex] = {
        ...updatedTasks[taskIndex],
        is_completed: true
      }
      
      // 更新卡片
      const result = await this.updateDailyCard({
        tasks: updatedTasks
      })
      
      return !!result
    }
  }
})
