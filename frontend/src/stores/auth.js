import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'
import { jwtDecode } from 'jwt-decode'

export const useAuthStore = defineStore('auth', () => {
  const access = ref(localStorage.getItem('access') || null)
  const refresh = ref(localStorage.getItem('refresh') || null)

  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  function isTokenExpired(token) {
    try {
      const decoded = jwtDecode(token)

      if (!decoded.exp) {
        return true
      }

      return decoded.exp * 1000 < Date.now()

    } catch {
      return true
    }
  }

  if (!access.value || !refresh.value || isTokenExpired(refresh.value)) {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    localStorage.removeItem('user')
    access.value = null
    refresh.value = null
    user.value = null
  }

  const isAuthenticated = computed(() => !!access.value)
  const userRole = computed(() => user.value?.role || null)

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
        access.value = data.access
        refresh.value = data.refresh
        user.value = data.user
        localStorage.setItem('access', data.access)
        localStorage.setItem('refresh', data.refresh)
        localStorage.setItem('user', JSON.stringify(data.user))
        return true
      }
    } catch (err) {
      console.error('Login error:', err.response?.data || err.message)
    }
    return false
  }

  async function register(name, username, role, password) {
    try {
      const res = await api.post('/users/register/', { name, username, role, password })
      if (res.data) {
        const data = res.data
        access.value = data.access
        refresh.value = data.refresh
        user.value = data.user
        localStorage.setItem('access', data.access)
        localStorage.setItem('refresh', data.refresh)
        localStorage.setItem('user', JSON.stringify(data.user))
        return true
      }
    } catch (err) {
      console.error('Registration error:', err.response?.data || err.message)
    }
    return false
  }

  function logout() {
    access.value = null
    refresh.value = null
    user.value = null
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    localStorage.removeItem('user')
  }

  return {
    access,
    refresh,
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
