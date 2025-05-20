import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useTaskStore = defineStore('tasks', {
  state: () => ({
    tasks: {
      todo: [],
      watch: [],
      later: []
    },
    loading: false,
    error: null
  }),
  
  getters: {
    getTodoTasks: (state) => state.tasks.todo,
    getWatchTasks: (state) => state.tasks.watch,
    getLaterTasks: (state) => state.tasks.later,
    
    getTaskById: (state) => (id) => {
      const allTasks = [
        ...state.tasks.todo,
        ...state.tasks.watch,
        ...state.tasks.later
      ]
      return allTasks.find(task => task.id === id)
    }
  },
  
  actions: {
    async fetchTasks() {
      this.loading = true
      this.error = null
      
      const authStore = useAuthStore()
      
      try {
        const response = await axios.get('/api/tasks', {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        // 按列表类型分组任务
        const tasks = response.data
        this.tasks = {
          todo: tasks.filter(task => task.list_type === 'todo'),
          watch: tasks.filter(task => task.list_type === 'watch'),
          later: tasks.filter(task => task.list_type === 'later')
        }
      } catch (error) {
        this.error = '获取任务失败'
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    
    async createTask(taskData) {
      this.loading = true
      this.error = null
      
      const authStore = useAuthStore()
      
      try {
        const response = await axios.post('/api/tasks', taskData, {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        const newTask = response.data
        this.tasks[newTask.list_type].push(newTask)
        
        return newTask
      } catch (error) {
        this.error = '创建任务失败'
        console.error(error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async updateTask(id, taskData) {
      this.loading = true
      this.error = null
      
      const authStore = useAuthStore()
      
      try {
        const response = await axios.put(`/api/tasks/${id}`, taskData, {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        const updatedTask = response.data
        
        // 如果列表类型改变，需要从旧列表中移除并添加到新列表
        const oldListType = this.getTaskById(id)?.list_type
        
        if (oldListType && oldListType !== updatedTask.list_type) {
          // 从旧列表中移除
          this.tasks[oldListType] = this.tasks[oldListType].filter(task => task.id !== id)
          // 添加到新列表
          this.tasks[updatedTask.list_type].push(updatedTask)
        } else {
          // 更新现有列表中的任务
          const listType = updatedTask.list_type
          const index = this.tasks[listType].findIndex(task => task.id === id)
          
          if (index !== -1) {
            this.tasks[listType][index] = updatedTask
          }
        }
        
        return updatedTask
      } catch (error) {
        this.error = '更新任务失败'
        console.error(error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async deleteTask(id) {
      this.loading = true
      this.error = null
      
      const authStore = useAuthStore()
      const task = this.getTaskById(id)
      
      if (!task) {
        this.error = '任务不存在'
        this.loading = false
        return false
      }
      
      try {
        await axios.delete(`/api/tasks/${id}`, {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        // 从列表中移除任务
        this.tasks[task.list_type] = this.tasks[task.list_type].filter(t => t.id !== id)
        
        return true
      } catch (error) {
        this.error = '删除任务失败'
        console.error(error)
        return false
      } finally {
        this.loading = false
      }
    },
    
    async completeTask(id) {
      return this.updateTask(id, { is_completed: true })
    },
    
    async moveTask(id, newListType) {
      const task = this.getTaskById(id)
      
      if (!task) {
        this.error = '任务不存在'
        return null
      }
      
      return this.updateTask(id, { list_type: newListType })
    }
  }
})
