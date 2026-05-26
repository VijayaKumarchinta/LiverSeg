import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  
  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || 'radiologist')

  const userName = computed(() => {
    if (!user.value) return ''
    const fullName = `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim()
    return fullName || user.value.username || ''
  })

  const userUsername = computed(() => user.value?.username || '')

  const userInitials = computed(() => {
    if (!user.value) return ''
    const name = `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim() || user.value.username || ''
    return name
      .split(' ')
      .filter(Boolean)
      .map(part => part[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  })

  async function login(username, password) {
    try {
      const res = await api.post('/users/login/', { username, password })
      if (res.data) {
        const data = res.data
        token.value = data.token
        user.value = data.user
        localStorage.setItem('token', data.token)
        localStorage.setItem('user', JSON.stringify(data.user))
        return true
      }
    } catch (err) {
      console.error('Login error:', err.response?.data || err.message)
    }
    return false
  }

  async function register(name, username, hospital, role, password) {
    try {
      const res = await api.post('/users/register/', { name, username, hospital, role, password })
      if (res.data) {
        const data = res.data
        token.value = data.token
        user.value = data.user
        localStorage.setItem('token', data.token)
        localStorage.setItem('user', JSON.stringify(data.user))
        return true
      }
    } catch (err) {
      console.error('Registration error:', err.response?.data || err.message)
    }
    return false
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token,
    user,
    isAuthenticated,
    userRole,
    userName,
    userUsername,
    userInitials,
    login,
    register,
    logout
  }
})
