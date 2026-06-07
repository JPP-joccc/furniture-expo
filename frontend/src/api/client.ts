import axios from 'axios'
import { ElMessage } from 'element-plus'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/',
  timeout: 15000,
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || '请求失败，请稍后重试'
    const detail = typeof message === 'string' ? message : JSON.stringify(message)
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      if (!window.location.pathname.includes('/login')) {
        ElMessage.warning('登录已过期，请重新登录')
      }
    } else {
      ElMessage.error(detail)
    }
    return Promise.reject(error)
  },
)

export default client
