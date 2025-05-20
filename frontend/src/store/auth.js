import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    getUser: (state) => state.user
  },
  
  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/auth/login', credentials)
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        
        // 获取用户信息
        await this.fetchUserProfile()
        
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || '登录失败，请检查您的凭据'
        return false
      } finally {
        this.loading = false
      }
    },
    
    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/auth/register', userData)
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        
        // 获取用户信息
        await this.fetchUserProfile()
        
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || '注册失败，请稍后再试'
        return false
      } finally {
        this.loading = false
      }
    },
    
    async fetchUserProfile() {
      if (!this.token) return
      
      this.loading = true
      
      try {
        const response = await axios.get('/api/auth/me', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        
        this.user = response.data
      } catch (error) {
        this.error = '获取用户信息失败'
        // 如果令牌无效，则注销
        if (error.response?.status === 401) {
          this.logout()
        }
      } finally {
        this.loading = false
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})
