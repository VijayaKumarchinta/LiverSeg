import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' }
})

// Request interceptor — attach JWT token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('liverseg_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
}, error => Promise.reject(error))

// Response interceptor — handle 401s
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('liverseg_token')
      localStorage.removeItem('liverseg_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
